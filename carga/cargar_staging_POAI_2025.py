import pandas as pd
from sqlalchemy import create_engine, inspect, text
from pathlib import Path
import numpy as np

# === Configuración de la conexión a la BD ===
USER = "sised_user"
PWD  = "TuPasswordFuerte"
HOST = "localhost"
PORT = 3307
DB   = "sised"

# Crear motor de conexión con SQLAlchemy
engine = create_engine(f"mysql+pymysql://{USER}:{PWD}@{HOST}:{PORT}/{DB}")

# === Rutas de los Excel depurados ===
BASE = Path(__file__).resolve().parent
DEPURADO = BASE / "transformacion" / "staging" / "depurado"

archivos = {
    "stg_fuente_poai_2025": DEPURADO / "stg_fuente_poai_2025_depurado.xlsx",
    "stg_proyectos_poai_2025": DEPURADO / "stg_proyectos_poai_2025_depurado.xlsx",
    "stg_actividades_poai_2025": DEPURADO / "stg_actividades_poai_2025_depurado.xlsx",
    "stg_beneficiarios_poai_2025": DEPURADO / "stg_beneficiarios_poai_2025_depurado.xlsx",
    "stg_metas_poai_2025": DEPURADO / "stg_metas_poai_2025_depurado.xlsx",
}


# === Función genérica para cargar un DataFrame a SQL ===
def cargar_tabla(tabla, ruta_excel, engine):
    print(f"\n🚀 Procesando {tabla} desde {ruta_excel.name}")
    df = pd.read_excel(ruta_excel)

    # 1. Quitar columnas basura
    df = df.loc[:, ~df.columns.str.contains("^Unnamed|^Col")]

    # 2. Renombres genéricos
    renombres = {
        "Apropiación Definitiva 2025": "Apropiación Definitiva",
        "Total Ejecutado 2025": "Total Ejecutado",
        "Difrencia \nApro - Ejec": "Difrencia Apro - Ejec",
        "Responsable": "Responsable SED",
        "Enlace Técnico": "Enlace Técnico SED",
        "MUNICIO": "MUNICIPIO",
    }
    df = df.rename(columns=renombres)

    # 3. Filtrar SOLO las columnas válidas en la BD
    insp = inspect(engine)
    cols_bd = [col["name"] for col in insp.get_columns(tabla)]
    df = df[[c for c in df.columns if c in cols_bd]]

    # 4. Limpiar strings
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # 5. Limpieza específica para beneficiarios (convertir "No reportado" en 0)
    if "beneficiarios" in tabla:
        cols_numericas = [
            "# Directivos Beneficiados",
            "# Administrativos Beneficiados",
            "# Docentes Beneficiados",
            "# Estudiantes Beneficiados"
        ]
        for col in cols_numericas:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

    # 6. TRUNCATE y carga
    with engine.begin() as conn:
        conn.execute(text(f"TRUNCATE TABLE {tabla}"))

    df.to_sql(tabla, engine, if_exists="append", index=False, method="multi", chunksize=1000)
    print(f"\n✅ {len(df)} filas insertadas en {tabla}")
    print(f'\n{df.head()}')


# === Proceso principal ===
if __name__ == "__main__":
    for tabla, ruta_excel in archivos.items():
        cargar_tabla(tabla, ruta_excel, engine)
