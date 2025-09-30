import pandas as pd
from sqlalchemy import create_engine, inspect, text
from pathlib import Path

# === Configuración BD (ajusta usuario, contraseña, host y puerto) ===
USER = "sised_user"
PWD  = "TuPasswordFuerte"
HOST = "localhost"
PORT = 3307
DB   = "sised"

engine = create_engine(f"mysql+pymysql://{USER}:{PWD}@{HOST}:{PORT}/{DB}")

# === Rutas de Excel depurados ===
BASE = Path(__file__).resolve().parent
DEPURADO = BASE / "transformacion" / "staging" / "depurado"

archivos = {
    "stg_actividades_estrategias": DEPURADO / "stg_actividades_estrategias_depurado.xlsx",
    "stg_fuente_estrategias": DEPURADO / "stg_fuente_estrategias_depurado.xlsx",
    "stg_proyectos_estrategias": DEPURADO / "stg_proyectos_estrategias_depurado.xlsx",
    "stg_beneficiarios_estrategias": DEPURADO / "stg_beneficiarios_estrategias_depurado.xlsx",
}

# === Función auxiliar: obtener columnas válidas de la BD ===
def columnas_validas(tabla):
    insp = inspect(engine)
    return [col["name"] for col in insp.get_columns(tabla)]

# === Normalización de datos específicos de actividades ===
def normalizar_actividades(df):
    # Validar SI/NO en Entrega Dotación
    if "Entrega Dotación (SI / NO)" in df.columns:
        df["Entrega Dotación (SI / NO)"] = df["Entrega Dotación (SI / NO)"].where(
            df["Entrega Dotación (SI / NO)"].isin(["SI", "NO"])
        )
    return df

# === Cargar Excel a tabla staging ===
with engine.begin() as conn:
    for tabla, ruta_excel in archivos.items():
        print(f"\n🚀 Procesando {tabla} desde {ruta_excel.name}")
        df = pd.read_excel(ruta_excel)

        # Normalización especial si es actividades
        if tabla == "stg_actividades_estrategias":
            df = normalizar_actividades(df)

        # Eliminar columnas sobrantes
        cols_drop = [c for c in df.columns if "Unnamed" in c or c in ["Evidencia_URL", "FUENTES", "BENEFICIARIOS"]]
        df = df.drop(columns=cols_drop, errors="ignore")

        # Filtrar columnas válidas según BD
        cols_bd = columnas_validas(tabla)
        df = df[[c for c in df.columns if c in cols_bd]]

        # TRUNCATE antes de cargar
        conn.execute(text(f"TRUNCATE TABLE {tabla}"))

        # Insertar
        df.to_sql(tabla, engine, if_exists="append", index=False, method="multi", chunksize=1000)
        print(f"✅ {len(df)} filas insertadas en {tabla}")
