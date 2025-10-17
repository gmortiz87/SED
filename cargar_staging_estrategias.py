import pandas as pd
from sqlalchemy import create_engine, inspect, text
from pathlib import Path

# === Configuración BD ===
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
    if "Entrega Dotación (SI / NO)" in df.columns:
        df["Entrega Dotación (SI / NO)"] = df["Entrega Dotación (SI / NO)"].where(
            df["Entrega Dotación (SI / NO)"].isin(["SI", "NO"])
        )
    return df

# === Carga principal ===
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

        # Insertar datos
        df.to_sql(tabla, engine, if_exists="append", index=False, method="multi", chunksize=1000)
        print(f'\n{df.head()}')

        print(f"✅ {len(df)} filas insertadas en {tabla}")

        # === Generar ID secuencial para proyectos ===
        if tabla == "stg_proyectos_estrategias":
            print("Verificando columna y generando id_proyecto secuencial...")

            # Verificar si existe la columna id_proyecto antes de crearla
            resultado = conn.execute(text("""
                SELECT COUNT(*) AS existe 
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = :db
                  AND TABLE_NAME = 'stg_proyectos_estrategias'
                  AND COLUMN_NAME = 'id_proyecto';
            """), {"db": DB}).scalar()

            if resultado == 0:
                print("Creando columna id_proyecto (no existía)...")
                conn.execute(text("ALTER TABLE stg_proyectos_estrategias ADD COLUMN id_proyecto INT NULL;"))
            else:
                print("Columna id_proyecto ya existe.")

            # Asignar IDs incrementales a partir de 100
            conn.execute(text("SET @rownum := 100;"))
            conn.execute(text("""
                UPDATE stg_proyectos_estrategias
                SET id_proyecto = (@rownum := @rownum + 1)
                WHERE Hoja IS NOT NULL;
            """))

            print("id_proyecto generado correctamente.\n")

print("\nCarga staging completa. Todas las tablas actualizadas exitosamente.")
