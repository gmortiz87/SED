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
    Prepara las tablas de Fuente, Proyectos, Actividades y Beneficiarios
    sin unirlas directamente (se relacionarán luego en DWH/BI).
    """
    df_rel = cargar_relacion()

    # === Cargar entradas ===
    sufijo = f"_{anio}" if anio else ""

    df_fuente = pd.read_excel(OUTPUT_DIR / f"Registros_Fuente_{nombre_fuente}{sufijo}.xlsx")
    df_proy = pd.read_excel(
        OUTPUT_DIR / f"Registro_Proyectos_Actividades_{nombre_fuente}{sufijo}.xlsx",
        sheet_name="Info_Proyectos"
    )
    df_act = pd.read_excel(
        OUTPUT_DIR / f"Registro_Proyectos_Actividades_{nombre_fuente}{sufijo}.xlsx",
        sheet_name="Actividades"
    )
    df_ben = pd.read_excel(
        OUTPUT_DIR / f"Registro_Beneficiarios_{nombre_fuente}{sufijo}.xlsx",
        sheet_name="Beneficiarios"
    )

    # === Normalizar columnas clave ===
    renombres = {
        "Nombre del Proyecto": "Nombre Proyecto",
        "Nombre de la Estrategia": "Nombre Proyecto",
        "Nombre Estrategia": "Nombre Proyecto"
    }
    df_fuente.rename(columns=renombres, inplace=True)
    df_proy.rename(columns=renombres, inplace=True)
    df_act.rename(columns=renombres, inplace=True)

    # === Enlazar con maestro solo en proyectos, actividades y beneficiarios ===
    df_fuente_rel = df_fuente.copy()  # SIN merge, se mantiene tal cual
    df_proy_rel = df_proy.merge(df_rel, left_on="Hoja", right_on="PROYECTOS", how="left")
    df_act_rel = df_act.merge(df_rel, left_on="Hoja", right_on="PROYECTOS", how="left")
    df_ben_rel = df_ben.merge(df_rel, left_on="Hoja", right_on="BENEFICIARIOS", how="left")

    # === Guardar outputs por separado ===
    STAGING_DIR.mkdir(parents=True, exist_ok=True)

    suf = f"_{anio}" if anio else ""
    out_fuente = STAGING_DIR / f"fact_fuente_{nombre_fuente.lower()}{suf}.xlsx"
    out_proy = STAGING_DIR / f"fact_proyectos_{nombre_fuente.lower()}{suf}.xlsx"
    out_act = STAGING_DIR / f"fact_actividades_{nombre_fuente.lower()}{suf}.xlsx"
    out_ben = STAGING_DIR / f"fact_beneficiarios_{nombre_fuente.lower()}{suf}.xlsx"

    df_fuente_rel.to_excel(out_fuente, index=False)
    df_proy_rel.to_excel(out_proy, index=False)
    df_act_rel.to_excel(out_act, index=False)
    df_ben_rel.to_excel(out_ben, index=False)

    print(f"[OK] Fuente guardada en: {out_fuente} ({len(df_fuente_rel)} filas)")
    print(f"[OK] Proyectos guardados en: {out_proy} ({len(df_proy_rel)} filas)")
    print(f"[OK] Actividades guardadas en: {out_act} ({len(df_act_rel)} filas)")
    print(f"[OK] Beneficiarios guardados en: {out_ben} ({len(df_ben_rel)} filas)")

    return df_fuente_rel, df_proy_rel, df_act_rel, df_ben_rel
