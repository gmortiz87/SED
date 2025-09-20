import pandas as pd
from pathlib import Path

# === Configuración ===
# STAGING_DIR = Path("staging")
BASE_DIR = Path(__file__).resolve().parents[0]
STAGING_DIR = BASE_DIR / "staging"

DEPURADO_DIR = STAGING_DIR / "depurado"
DEPURADO_DIR.mkdir(exist_ok=True)
OUTPUT_FILE = STAGING_DIR / "control_y_depuracion.xlsx"

PRIMARY_KEYS = {
    "fact_fuente": "ID_Fuente",
    "fact_proyectos": "ID_Proyecto",
    "fact_beneficiarios": "ID_Beneficiario",
}
FOREIGN_KEYS = {
    "fact_proyectos": {"ID_Fuente": "fact_fuente"},
    "fact_beneficiarios": {"ID_Proyecto": "fact_proyectos"},
}
CAMPOS_TEXTO = ["Nombre_Proyecto", "Nombre_Estrategia"]

# === Cargar archivos ===
def cargar_staging():
    archivos = list(STAGING_DIR.glob("fact_*.xlsx"))
    return {a.stem: pd.read_excel(a) for a in archivos}

# === Validación de calidad ===
def validar_dataframe(nombre, df):
    pk = next((PRIMARY_KEYS[k] for k in PRIMARY_KEYS if nombre.startswith(k)), None)
    return {
        "tabla": nombre,
        "total_registros": len(df),
        "nulos": df.isnull().sum().to_dict(),
        "duplicados": df.duplicated().sum(),
        "unicidad_PK": df[pk].is_unique if pk and pk in df.columns else "PK no encontrada"
    }

def validar_relaciones(dfs):
    errores_fk = []
    for tabla, claves in FOREIGN_KEYS.items():
        if tabla not in dfs: continue
        for fk, tabla_ref in claves.items():
            if fk not in dfs[tabla].columns or tabla_ref not in dfs: continue
            faltantes = set(dfs[tabla][fk].dropna()) - set(dfs[tabla_ref][PRIMARY_KEYS[tabla_ref]])
            if faltantes:
                errores_fk.append({
                    "tabla": tabla, "columna": fk,
                    "tabla_referencia": tabla_ref,
                    "registros_invalidos": len(faltantes),
                    "muestra": list(faltantes)[:10]
                })
    return errores_fk

# === Depuración ===
def depurar_campos(dfs):
    resumen = []
    for nombre, df in dfs.items():
        orig = len(df)

        # --- 1. Consolidar Nombre_Proyecto ---
        if "Nombre Proyecto_x" in df.columns or "Nombre Proyecto_y" in df.columns:
            df["Nombre_Proyecto"] = df.get("Nombre Proyecto_x", "").fillna("") \
                                       .astype(str).str.strip()
            if "Nombre Proyecto_y" in df.columns:
                df["Nombre_Proyecto"] = df["Nombre_Proyecto"].replace("", None)
                df["Nombre_Proyecto"] = df["Nombre_Proyecto"].fillna(
                    df["Nombre Proyecto_y"].astype(str).str.strip()
                )
            df.drop(columns=[c for c in ["Nombre Proyecto_x","Nombre Proyecto_y"] if c in df.columns], inplace=True)

        # --- 2. Eliminar filas con Nombre_Proyecto vacío ---
        if "Nombre_Proyecto" in df.columns:
            df["Nombre_Proyecto"] = df["Nombre_Proyecto"].astype(str).str.strip()
            df = df[df["Nombre_Proyecto"] != ""]

        # --- 3. Imputar nulos numéricos con 0 ---
        for col in df.select_dtypes(include=["int64","float64"]).columns:
            df[col] = df[col].fillna(0)

        # --- 4. Rellenar textos vacíos con "No reportado" ---
        for col in df.select_dtypes(include=["object"]).columns:
            df[col] = df[col].fillna("No reportado").astype(str).str.strip()
            df[col] = df[col].replace("", "No reportado")

        depurado = len(df)
        eliminados = orig - depurado
        resumen.append({
            "tabla": nombre,
            "filas_originales": orig,
            "filas_depuradas": depurado,
            "eliminados": eliminados
        })
        df.to_excel(DEPURADO_DIR / f"{nombre}_depurado.xlsx", index=False)

    return pd.DataFrame(resumen)

# === Ejecución completa ===
def ejecutar():
    dfs = cargar_staging()
    resumen_calidad = [validar_dataframe(n, df) for n, df in dfs.items()]
    errores_fk = validar_relaciones(dfs)
    resumen_depuracion = depurar_campos(dfs)

    # Exportar resumen conjunto
    with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
        pd.DataFrame(resumen_calidad).to_excel(writer, sheet_name="Resumen_Calidad", index=False)
        pd.DataFrame(errores_fk).to_excel(writer, sheet_name="Errores_FK", index=False)
        resumen_depuracion.to_excel(writer, sheet_name="Resumen_Depuracion", index=False)

    print(f"✅ Flujo completo ejecutado. Resultados en: {OUTPUT_FILE} y {DEPURADO_DIR}")

if __name__ == "__main__":
    ejecutar()
