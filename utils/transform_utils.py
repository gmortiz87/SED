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
    Prepara las tablas de Fuente, Proyectos, Actividades, Beneficiarios y Metas
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
    df_metas = pd.DataFrame()
    if not nombre_fuente.upper().startswith("ESTRATEGIAS"):
        df_metas = pd.read_excel(
            OUTPUT_DIR / f"Registro_Proyectos_Actividades_{nombre_fuente}{sufijo}.xlsx",
            sheet_name="Metas"
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
    df_metas.rename(columns=renombres, inplace=True)

    # === Enlazar con maestro ===
    df_fuente_rel = df_fuente.copy()  # SIN merge, se mantiene tal cual
    df_proy_rel = df_proy.merge(df_rel, left_on="Hoja", right_on="PROYECTOS", how="left")

    df_act_rel = df_act.merge(df_rel, left_on="Hoja", right_on="PROYECTOS", how="left")
    df_ben_rel = df_ben.merge(df_rel, left_on="Hoja", right_on="BENEFICIARIOS", how="left")

    # Metas: merge con proyectos para traer ID_Proyecto
    df_metas_rel = pd.DataFrame()
    if not df_metas.empty:
        # Nos quedamos solo con las columnas mínimas de proyectos
        if "ID_Proyecto" in df_proy_rel.columns:
            df_proy_min = df_proy_rel[["Hoja", "Nombre_Proyecto", "ID_Proyecto"]]
        else:
            df_proy_min = df_proy_rel[["Hoja", "Nombre_Proyecto"]]

        
        # Hacemos el merge usando Hoja + Nombre_Proyecto
        df_metas_rel = df_metas.merge(
            df_proy_min,
            on=["Hoja", "Nombre_Proyecto"],
            how="left"
        )

        # Crear ID_Meta consecutivo si no existe
        if "ID_Meta" not in df_metas_rel.columns:
            df_metas_rel.insert(0, "ID_Meta", range(1, len(df_metas_rel) + 1))

    # === Guardar outputs por separado ===
    STAGING_DIR.mkdir(parents=True, exist_ok=True)

    suf = f"_{anio}" if anio else ""
    out_fuente = STAGING_DIR / f"stg_fuente_{nombre_fuente.lower()}{suf}.xlsx"
    out_proy = STAGING_DIR / f"stg_proyectos_{nombre_fuente.lower()}{suf}.xlsx"
    out_act = STAGING_DIR / f"stg_actividades_{nombre_fuente.lower()}{suf}.xlsx"
    out_ben = STAGING_DIR / f"stg_beneficiarios_{nombre_fuente.lower()}{suf}.xlsx"
    out_metas = STAGING_DIR / f"stg_metas_{nombre_fuente.lower()}{suf}.xlsx"

    df_fuente_rel.to_excel(out_fuente, index=False)
    df_proy_rel.to_excel(out_proy, index=False)
    df_act_rel.to_excel(out_act, index=False)
    df_ben_rel.to_excel(out_ben, index=False)
    df_metas_rel.to_excel(out_metas, index=False)

    print(f"[OK] Fuente guardada en: {out_fuente} ({len(df_fuente_rel)} filas)")
    print(f"[OK] Proyectos guardados en: {out_proy} ({len(df_proy_rel)} filas)")
    print(f"[OK] Actividades guardadas en: {out_act} ({len(df_act_rel)} filas)")
    print(f"[OK] Beneficiarios guardados en: {out_ben} ({len(df_ben_rel)} filas)")
    print(f"[OK] Metas guardadas en: {out_metas} ({len(df_metas_rel)} filas)")

    return df_fuente_rel, df_proy_rel, df_act_rel, df_ben_rel, df_metas_rel
