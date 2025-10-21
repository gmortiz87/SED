import subprocess, sys, os
from pathlib import Path
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

# ========= Config BD =========
USER = "sised_user"
PWD  = "TuPasswordFuerte"  # si tiene @ u otros, lo codificamos:
PWD_ENC = quote_plus(PWD)
HOST = "localhost"
PORT = 3306
DB   = "sised"

ENGINE_URL = f"mysql+pymysql://{USER}:{PWD_ENC}@{HOST}:{PORT}/{DB}"
engine = create_engine(ENGINE_URL, pool_pre_ping=True, future=True)

# ========= Rutas =========
ROOT = Path(__file__).resolve().parent              # SED/carga
SQL_DIR = ROOT / "sql"
DROPS_DIR = SQL_DIR / "drops"

# loaders (staging)
LOADERS = [
    ROOT / "cargar_staging_POAI_2024.py",
    ROOT / "cargar_staging_POAI_2025.py",
    ROOT / "cargar_staging_estrategias.py",
    ROOT / "cargar_staging_regalias.py",
]

# secuencia por modelo (DROP → TABLAS → INSERT)
JOBS = [
    # (nombre, drop, tablas, insert)
    ("POAI_2024",
     DROPS_DIR / "drop_poai_2024.sql",
     SQL_DIR / "4_Tablas_POAI_2024.sql",
     SQL_DIR / "4_Insert_POAI_2024.sql"),
    ("POAI_2025",
     DROPS_DIR / "drop_poai_2025.sql",
     SQL_DIR / "5_Tablas_POAI_2025.sql",
     SQL_DIR / "5_Insert_POAI_2025.sql"),
    ("ESTRATEGIAS",
     DROPS_DIR / "drop_estrategias.sql",
     SQL_DIR / "6_Tablas_Estrategia.sql",
     SQL_DIR / "6_Insert_Estrategia.sql"),
    ("REGALIAS",
     DROPS_DIR / "drop_regalias.sql",
     SQL_DIR / "3_Tablas_Regalias.sql",
     SQL_DIR / "3_Insert_Regalias.sql"),
]

def run_py(script_path: Path):
    print(f"\n=== STAGING: {script_path.name} ===")
    if not script_path.exists():
        raise FileNotFoundError(f"No existe: {script_path}")
    # usar el mismo intérprete que ejecuta este script (venv)
    cmd = [sys.executable, str(script_path)]
    subprocess.run(cmd, check=True)
    print(f"OK: {script_path.name}")

def run_sql_file(path):
    print(f"\n--- Ejecutando archivo SQL: {path} ---")

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Limpieza: eliminar comentarios tipo "--" y líneas vacías
    cleaned = []
    for line in content.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith('--'):
            cleaned.append(stripped)
    sql_text = ' '.join(cleaned)

    # Separar sentencias completas por ';' pero sin perder continuidad
    statements = [s.strip() for s in sql_text.split(';') if s.strip()]

    with engine.begin() as conn:
        for stmt in statements:
            try:
                conn.execute(text(stmt))
                print(f"✅ Ejecutado: {stmt[:60]}...")
            except Exception as e:
                print(f"⚠️ Error ejecutando sentencia: {stmt[:60]}... → {e}")

def run_job(name, drop, tablas, insert):
    print(f"\n=======================")
    print(f"   MODELO: {name}")
    print(f"=======================\n")

    # -------------------------------
    # 🧹 LIMPIEZA PREVIA AUTOMÁTICA
    # -------------------------------
    print(f"--- Reiniciando modelo {name} ---")
    with engine.begin() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
        tablas_dim_fact = [
            "dim_fuente", "dim_proyecto", "dim_actividad", "dim_meta",
            "dim_institucion", "dim_municipio", "dim_tiempo",
            "fact_actividades", "fact_proyecto_meta",
            "fact_proyecto_institucion", "fact_proyecto_beneficiario"
        ]
        for t in tablas_dim_fact:
            full_name = f"{t}_{name.lower()}"
            try:
                conn.execute(text(f"DROP TABLE IF EXISTS {full_name};"))
                print(f"✅ {full_name} eliminada (si existía)")
            except Exception as e:
                print(f"⚠️ No se pudo eliminar {full_name}: {e}")
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))

    # -------------------------------
    # 🏗️ EJECUCIÓN NORMAL DEL MODELO
    # -------------------------------
    print(f"\n--- Cargando estructura de tablas ({tablas}) ---")
    run_sql_file(tablas)

    print(f"\n--- Insertando datos en modelo ({insert}) ---")
    run_sql_file(insert)

    print(f"\n✅ Modelo {name} cargado correctamente\n")

def validate_counts(model_tag: str):
    # ejemplo simple: ver cuántas tablas del modelo existen
    q = text("""
        SELECT COUNT(*) AS n
        FROM information_schema.tables
        WHERE table_schema = :db AND table_name LIKE :pat
    """)
    with engine.begin() as conn:
        n = conn.execute(q, {"db": DB, "pat": f"%{model_tag}%"}).scalar()
    print(f"Tablas con patrón %{model_tag}%: {n}")

if __name__ == "__main__":
    print(">>> FASE A: STAGING")
    for loader in LOADERS:
        run_py(loader)  # usa tus 4 scripts de carga
    print("\n>>> FASE B: MODELO DIMENSIONAL")
    for (name, drop, tablas, insert) in JOBS:
        run_job(name, drop, tablas, insert)
        validate_counts(name.lower())

    print("\n>>> FASE C: VALIDACIÓN FINAL")
    with engine.begin() as conn:
        for pat in ("%poai_2024%", "%poai_2025%", "%estrategias%", "%regalias%"):
            n = conn.execute(text("""
                SELECT COUNT(*) FROM information_schema.tables
                WHERE table_schema=:db AND table_name LIKE :pat
            """), {"db": DB, "pat": pat}).scalar()
            print(f"{pat}: {n} tablas")
    print("\n✅ Pipeline COMPLETO.")
