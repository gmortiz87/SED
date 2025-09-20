import pandas as pd
from pathlib import Path

# === Configuración ===
STAGING_DIR = Path("staging")
OUTPUT_FILE = STAGING_DIR / "control_calidad_staging.xlsx"

# Definición de campos clave
PRIMARY_KEYS = {
    "fact_fuente": "ID_Fuente",
    "fact_proyectos": "ID_Proyecto",
    "fact_beneficiarios": "ID_Beneficiario",
}
FOREIGN_KEYS = {
    "fact_proyectos": {"ID_Fuente": "fact_fuente"},
    "fact_beneficiarios": {"ID_Proyecto": "fact_proyectos"},
}

# === Cargar archivos ===
def cargar_staging():
    archivos = list(STAGING_DIR.glob("fact_*.xlsx"))
    dataframes = {}
    for archivo in archivos:
        nombre = archivo.stem  # ej: fact_proyectos_poai_2024
        df = pd.read_excel(archivo)
        dataframes[nombre] = df
    return dataframes

# === Validaciones de calidad ===
def validar_dataframe(nombre, df):
    resultados = {}
    pk = None
    # Identificar tipo de tabla
    for clave in PRIMARY_KEYS:
        if nombre.startswith(clave):
            pk = PRIMARY_KEYS[clave]

    # Conteos básicos
    resultados["total_registros"] = len(df)
    resultados["nulos"] = df.isnull().sum().to_dict()
    resultados["duplicados"] = df.duplicated().sum()

    # Validar llave primaria
    if pk and pk in df.columns:
        resultados["unicidad_PK"] = df[pk].is_unique
    else:
        resultados["unicidad_PK"] = "PK no encontrada"

    return resultados

# === Validar relaciones FK ===
def validar_relaciones(dfs):
    errores_fk = []
    for tabla, claves in FOREIGN_KEYS.items():
        if tabla not in dfs:
            continue
        for fk, tabla_ref in claves.items():
            if fk not in dfs[tabla].columns:
                continue
            valores_fk = dfs[tabla][fk].dropna().unique()
            if tabla_ref not in dfs:
                continue
            valores_ref = dfs[tabla_ref][PRIMARY_KEYS[tabla_ref]].unique()
            faltantes = set(valores_fk) - set(valores_ref)
            if faltantes:
                errores_fk.append({
                    "tabla": tabla,
                    "columna": fk,
                    "tabla_referencia": tabla_ref,
                    "registros_invalidos": len(faltantes),
                    "muestra": list(faltantes)[:10]  # primeras 10 inconsistencias
                })
    return errores_fk

# === Ejecutar validación completa ===
def ejecutar_control():
    dfs = cargar_staging()

    # Resumen general
    resumen = []
    errores_detalle = []

    for nombre, df in dfs.items():
        resultado = validar_dataframe(nombre, df)
        resumen.append({"tabla": nombre, **resultado})

        # Guardar filas con nulos en campos obligatorios
        for col, nulos in resultado["nulos"].items():
            if nulos > 0:
                filas = df[df[col].isnull()]
                filas["Error"] = f"Nulos en {col}"
                errores_detalle.append((nombre, filas))

        # Guardar duplicados
        if resultado["duplicados"] > 0:
            filas = df[df.duplicated()]
            filas["Error"] = "Duplicado"
            errores_detalle.append((nombre, filas))

    # Validación de FK
    errores_fk = validar_relaciones(dfs)
    for e in errores_fk:
        errores_detalle.append((e["tabla"], pd.DataFrame([e])))

    # === Exportar reporte a Excel ===
    with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
        pd.DataFrame(resumen).to_excel(writer, sheet_name="Resumen", index=False)
        if errores_detalle:
            for nombre, df_err in errores_detalle:
                df_err.to_excel(writer, sheet_name=f"Errores_{nombre[:20]}", index=False)
        pd.DataFrame(errores_fk).to_excel(writer, sheet_name="Errores_FK", index=False)

    print(f"\n✅ Reporte de control generado en: {OUTPUT_FILE}")
    

# === Ejecutar ===
if __name__ == "__main__":
    ejecutar_control()
