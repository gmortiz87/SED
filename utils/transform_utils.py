import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "extraccion" / "outputs"
STAGING_DIR = BASE_DIR / "transformacion" / "staging"
RELACION_FILE = BASE_DIR / "relacion" / "Relación entre fuentes.xlsx"

def cargar_relacion():
    """Carga el archivo maestro de relación"""
    return pd.read_excel(RELACION_FILE, sheet_name="RELACION")

def transformar_fuente(nombre_fuente: str, anio: str = None):
    """
    Prepara las tablas:
    - Merge entre Fuente y Proyectos+Actividades
    - Beneficiarios aparte
    """
    df_rel = cargar_relacion()

    # === Cargar entradas ===
    if anio:
        sufijo = f"_{anio}"
    else:
        sufijo = ""

    df_fuente = pd.read_excel(OUTPUT_DIR / f"Registros_Fuente_{nombre_fuente}{sufijo}.xlsx")
    df_proy = pd.read_excel(
        OUTPUT_DIR / f"Registro_Proyectos_Actividades_{nombre_fuente}{sufijo}.xlsx",
        sheet_name="Info_Proyectos"
    )
    df_actividades = pd.read_excel(
        OUTPUT_DIR / f"Registro_Proyectos_Actividades_{nombre_fuente}{sufijo}.xlsx",
        sheet_name="Actividades"
    )
    df_ben = pd.read_excel(
        OUTPUT_DIR / f"Registro_Beneficiarios_{nombre_fuente}{sufijo}.xlsx",
        sheet_name="Beneficiarios"
    )

    # === Normalizar nombres de columnas ===
    renombres = {
        "Nombre del Proyecto": "Nombre Proyecto",
        "Nombre de la Estrategia": "Nombre Proyecto",
        "Nombre Estrategia": "Nombre Proyecto"
    }
    df_fuente.rename(columns=renombres, inplace=True)
    df_proy.rename(columns=renombres, inplace=True)
    df_actividades.rename(columns=renombres, inplace=True)

    # === Garantizar que Actividades tenga "Nombre Proyecto" ===
    if "Nombre Proyecto" not in df_actividades.columns:
        if "Hoja" in df_actividades.columns and "Nombre Proyecto" in df_proy.columns:
            mapping = df_proy.set_index("Hoja")["Nombre Proyecto"].to_dict()
            df_actividades["Nombre Proyecto"] = df_actividades["Hoja"].map(mapping)

    # === Enlazar con maestro ===
    df_fuente_rel = df_fuente.merge(df_rel, left_on="Hoja", right_on="FUENTES", how="left")
    df_proy_rel = df_proy.merge(df_rel, left_on="Hoja", right_on="PROYECTOS", how="left")
    df_actividades_rel = df_actividades.merge(df_rel, left_on="Hoja", right_on="PROYECTOS", how="left")
    df_ben_rel = df_ben.merge(df_rel, left_on="Hoja", right_on="BENEFICIARIOS", how="left")

    # === Merge Fuente + Proyectos ===
    df_fuente_proy = df_fuente_rel.merge(
        df_proy_rel, on=["FUENTES", "Hoja"], suffixes=("_fuente", "_proy")
    )

    # === Merge Proyectos + Actividades ===
    df_proy_activ = df_proy_rel.merge(
        df_actividades_rel, on=["Hoja", "Nombre Proyecto"], suffixes=("_proy", "_act")
    )

    # === Guardar resultados ===
    STAGING_DIR.mkdir(parents=True, exist_ok=True)
    suf = f"_{anio}" if anio else ""

    out_fuente_proy = STAGING_DIR / f"fact_fuente_proyectos_{nombre_fuente.lower()}{suf}.xlsx"
    out_proy_activ = STAGING_DIR / f"fact_proyectos_actividades_{nombre_fuente.lower()}{suf}.xlsx"
    out_ben = STAGING_DIR / f"fact_beneficiarios_{nombre_fuente.lower()}{suf}.xlsx"

    df_fuente_proy.to_excel(out_fuente_proy, index=False)
    df_proy_activ.to_excel(out_proy_activ, index=False)
    df_ben_rel.to_excel(out_ben, index=False)

    print(f"[OK] Fuente+Proyectos guardado en: {out_fuente_proy} ({len(df_fuente_proy)} filas)")
    print(f"[OK] Proyectos+Actividades guardado en: {out_proy_activ} ({len(df_proy_activ)} filas)")
    print(f"[OK] Beneficiarios guardado en: {out_ben} ({len(df_ben_rel)} filas)")

    return df_fuente_proy, df_proy_activ, df_ben_rel
