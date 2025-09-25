import pandas as pd
from sqlalchemy import create_engine, inspect, text
from pathlib import Path

# === Configuración BD (ajusta usuario, contraseña, host y puerto) ===
USER = "sised_user"
PWD  = "TuPasswordFuerte"
HOST = "localhost"
PORT = 3307   # ⚠️ el tuyo es 3307
DB   = "sised"

engine = create_engine(f"mysql+pymysql://{USER}:{PWD}@{HOST}:{PORT}/{DB}")

# === Rutas de Excel depurados ===
BASE = Path(__file__).resolve().parent
DEPURADO = BASE / "transformacion" / "staging" / "depurado"

archivos = {
    "stg_fuente_estrategias": DEPURADO / "fact_fuente_estrategias_depurado.xlsx",
    "stg_proyectos_estrategias": DEPURADO / "fact_proyectos_estrategias_depurado.xlsx",
    "stg_actividades_estrategias": DEPURADO / "fact_actividades_estrategias_depurado.xlsx",
    "stg_beneficiarios_estrategias": DEPURADO / "fact_beneficiarios_estrategias_depurado.xlsx",
}

# === Función auxiliar: obtener columnas válidas de la BD ===
def columnas_validas(tabla):
    insp = inspect(engine)
    cols = [col["name"] for col in insp.get_columns(tabla)]
    return cols

# === Normalización especial para fact_actividades_estrategias ===
def normalizar_actividades(df):
    # 1. Corregir Total Ejecutado (si hay texto → mover a "¿A qué actor va dirigida?")
    if "Total Ejecutado" in df.columns and "¿A qué actor va dirigida?" in df.columns:
        mask = pd.to_numeric(df["Total Ejecutado"], errors="coerce").isna()
        df.loc[mask, "¿A qué actor va dirigida?"] = df.loc[mask, "Total Ejecutado"]
        df.loc[mask, "Total Ejecutado"] = None

    # 2. Corregir Número de Beneficiarios (si hay texto → mover a "Descripción de la Dotación Entregada")
    if "Número de Beneficiarios" in df.columns and "Descripción de la Dotación Entregada" in df.columns:
        mask = pd.to_numeric(df["Número de Beneficiarios"], errors="coerce").isna()
        df.loc[mask, "Descripción de la Dotación Entregada"] = (
            df.loc[mask, "Descripción de la Dotación Entregada"].astype(str).replace("nan", "") + 
            " | " + df.loc[mask, "Número de Beneficiarios"].astype(str)
        ).str.strip(" |nan")
        df.loc[mask, "Número de Beneficiarios"] = None

    # 3. Limpiar Entrega Dotación (solo SI/NO válidos)
    if "Entrega Dotación (SI / NO)" in df.columns:
        df["Entrega Dotación (SI / NO)"] = df["Entrega Dotación (SI / NO)"].where(
            df["Entrega Dotación (SI / NO)"].isin(["SI", "NO"])
        )

    # 4. Convertir campos numéricos
    if "Total Ejecutado" in df.columns:
        df["Total Ejecutado"] = pd.to_numeric(df["Total Ejecutado"], errors="coerce")
    if "Número de Beneficiarios" in df.columns:
        df["Número de Beneficiarios"] = pd.to_numeric(df["Número de Beneficiarios"], errors="coerce")

    return df

# === Cargar cada Excel a su tabla staging ===
with engine.begin() as conn:
    for tabla, ruta_excel in archivos.items():
        print(f"\n🚀 Procesando {tabla} desde {ruta_excel.name}")
        df = pd.read_excel(ruta_excel)

        # Normalización especial si es actividades
        if tabla == "stg_actividades_estrategias":
            df = normalizar_actividades(df)

        # Filtrar columnas válidas según la BD
        cols_bd = columnas_validas(tabla)
        df = df[[c for c in df.columns if c in cols_bd]]

        # TRUNCATE antes de cargar
        conn.execute(text(f"TRUNCATE TABLE {tabla}"))

        # Insertar
        df.to_sql(tabla, engine, if_exists="append", index=False, method="multi", chunksize=1000)
        print(f"✅ {len(df)} filas insertadas en {tabla}")
