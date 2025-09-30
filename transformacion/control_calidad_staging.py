import pandas as pd
from pathlib import Path

# === Configuración ===
BASE_DIR = Path(__file__).resolve().parents[0]  # carpeta transformacion
STAGING_DIR = BASE_DIR / "staging"
STAGING_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = STAGING_DIR / "control_calidad_staging.xlsx"

PRIMARY_KEYS = {
    "stg_fuente": "ID_Fuente",
    "stg_proyectos": "ID_Proyecto",
    "stg_beneficiarios": "ID_Beneficiario",
    "stg_metas": "ID_Meta",  # nuevo
}
FOREIGN_KEYS = {
    "stg_proyectos": {"ID_Fuente": "stg_fuente"},
    "stg_beneficiarios": {"ID_Proyecto": "stg_proyectos"},
    "stg_metas": {"ID_Proyecto": "stg_proyectos"},  # nuevo
}

def cargar_staging():
    archivos = list(STAGING_DIR.glob("stg_*.xlsx"))
    dataframes = {}
    for archivo in archivos:
        nombre = archivo.stem
        df = pd.read_excel(archivo)
        dataframes[nombre] = df
    return dataframes

def validar_dataframe(nombre, df):
    resultados = {}
    pk = None
    for clave in PRIMARY_KEYS:
        if nombre.startswith(clave):
            pk = PRIMARY_KEYS[clave]

    resultados["total_registros"] = len(df)
    resultados["nulos"] = df.isnull().sum().to_dict()
    resultados["duplicados"] = df.duplicated().sum()

    if pk and pk in df.columns:
        resultados["unicidad_PK"] = df[pk].is_unique
    else:
        resultados["unicidad_PK"] = "PK no encontrada"

    return resultados

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
                    "muestra": list(faltantes)[:10]
                })
    return errores_fk

def ejecutar_control():
    dfs = cargar_staging()
    resumen = []
    errores_detalle = []

    for nombre, df in dfs.items():
        resultado = validar_dataframe(nombre, df)
        resumen.append({"tabla": nombre, **resultado})

        for col, nulos in resultado["nulos"].items():
            if nulos > 0:
                filas = df[df[col].isna()].copy()
                filas["Error"] = f"Nulos en {col}"
                errores_detalle.append((nombre, filas))

        if resultado["duplicados"] > 0:
            filas = df[df.duplicated()]
            filas["Error"] = "Duplicado"
            errores_detalle.append((nombre, filas))

    errores_fk = validar_relaciones(dfs)
    for e in errores_fk:
        errores_detalle.append((e["tabla"], pd.DataFrame([e])))

    with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
        pd.DataFrame(resumen).to_excel(writer, sheet_name="Resumen", index=False)
        if errores_detalle:
            for nombre, df_err in errores_detalle:
                df_err.to_excel(writer, sheet_name=f"Errores_{nombre[:20]}", index=False)
        pd.DataFrame(errores_fk).to_excel(writer, sheet_name="Errores_FK", index=False)

    print(f"\n✅ Reporte de control generado en: {OUTPUT_FILE}")

if __name__ == "__main__":
    ejecutar_control()
