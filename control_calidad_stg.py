import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path

# === Configuración BD ===
USER = "sised_user"
PWD  = "TuPasswordFuerte"
HOST = "localhost"
PORT = 3307
DB   = "sised"

engine = create_engine(f"mysql+pymysql://{USER}:{PWD}@{HOST}:{PORT}/{DB}")

# === Tablas a validar ===
tablas = [
    "stg_fuente_poai_2024",
    "stg_proyectos_poai_2024",
    "stg_actividades_poai_2024",
    "stg_beneficiarios_poai_2024",
    "stg_metas_poai_2024",
]

# === Reglas de calidad (puedes ampliarlas) ===
def validar_df(tabla, df):
    problemas = []

    # 1. Columnas críticas (ajusta por tabla)
    campos_obligatorios = {
        "stg_fuente_poai_2024": ["Nombre Proyecto", "Código BPIN"],
        "stg_proyectos_poai_2024": ["Nombre_Proyecto", "Código BPIN"],
        "stg_actividades_poai_2024": ["Nombre_Proyecto", "Actividad del Proyecto"],
        "stg_beneficiarios_poai_2024": ["Nombre Proyecto", "NOMBRE_IEO"],
        "stg_metas_poai_2024": ["Descripción"],
    }

    # 2. Validar vacíos
    for col in campos_obligatorios.get(tabla, []):
        vacios = df[df[col].isna()]
        if not vacios.empty:
            problemas.append((col, f"{len(vacios)} registros vacíos"))

    # 3. Validar "No reportado"
    for col in df.columns:
        if df[col].dtype == object:  # solo texto
            no_rep = df[df[col].astype(str).str.contains("No reportado", case=False, na=False)]
            if not no_rep.empty:
                problemas.append((col, f"{len(no_rep)} registros con 'No reportado'"))

    # 4. Duplicados por combinaciones clave
    if "Código BPIN" in df.columns:
        dups = df[df.duplicated(["Código BPIN"], keep=False)]
        if not dups.empty:
            problemas.append(("Código BPIN", f"{len(dups)} duplicados"))

    return problemas

# === Ejecución ===
reporte = []

with engine.connect() as conn:
    for tabla in tablas:
        df = pd.read_sql(text(f"SELECT * FROM {tabla}"), conn)
        problemas = validar_df(tabla, df)
        for campo, detalle in problemas:
            reporte.append([tabla, campo, detalle])

# === Exportar a Excel ===
df_reporte = pd.DataFrame(reporte, columns=["Tabla", "Campo", "Problema"])
output_file = Path("reporte_calidad_stg.xlsx")
df_reporte.to_excel(output_file, index=False)

print(df_reporte.head())

print(f"✅ Reporte generado: {output_file}")
