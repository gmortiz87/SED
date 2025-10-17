import pandas as pd
from sqlalchemy import create_engine, text

# === Conexión BD ===
USER = "sised_user"
PWD  = "TuPasswordFuerte"
HOST = "localhost"
PORT = 3307
DB   = "sised"

engine = create_engine(f"mysql+pymysql://{USER}:{PWD}@{HOST}:{PORT}/{DB}")

# === Definir validaciones ===
validaciones = {
    "dimensiones_con_registros": """
        SELECT 
          'dim_fuente_estrategias' AS tabla, COUNT(*) AS registros FROM dim_fuente_estrategias
        UNION ALL
        SELECT 'dim_proyecto_estrategias', COUNT(*) FROM dim_proyecto_estrategias
        UNION ALL
        SELECT 'dim_actividad_estrategias', COUNT(*) FROM dim_actividad_estrategias
        UNION ALL
        SELECT 'dim_institucion_estrategias', COUNT(*) FROM dim_institucion_estrategias
        UNION ALL
        SELECT 'dim_municipio_estrategias', COUNT(*) FROM dim_municipio_estrategias
        UNION ALL
        SELECT 'dim_tiempo_estrategias', COUNT(*) FROM dim_tiempo_estrategias;
    """,

    "hechos_vs_proyecto": """
        SELECT COUNT(*) AS hechos_sin_proyecto
        FROM fact_actividades_estrategias f
        LEFT JOIN dim_proyecto_estrategias p ON f.id_proyecto = p.id_proyecto
        WHERE p.id_proyecto IS NULL;
    """,

    "hechos_vs_actividad": """
        SELECT COUNT(*) AS hechos_sin_actividad
        FROM fact_actividades_estrategias f
        LEFT JOIN dim_actividad_estrategias a ON f.id_actividad = a.id_actividad
        WHERE a.id_actividad IS NULL;
    """,

    "integridad_fact_institucion": """
        SELECT
          SUM(CASE WHEN p.id_proyecto IS NULL THEN 1 ELSE 0 END) AS sin_proyecto,
          SUM(CASE WHEN i.id_institucion IS NULL THEN 1 ELSE 0 END) AS sin_institucion,
          SUM(CASE WHEN m.id_municipio IS NULL THEN 1 ELSE 0 END) AS sin_municipio
        FROM fact_proyecto_institucion_estrategias f
        LEFT JOIN dim_proyecto_estrategias p ON f.id_proyecto = p.id_proyecto
        LEFT JOIN dim_institucion_estrategias i ON f.id_institucion = i.id_institucion
        LEFT JOIN dim_municipio_estrategias m ON f.id_municipio = m.id_municipio;
    """,

    "resumen_global": """
        SELECT 
          p.id_proyecto,
          p.nombre_proyecto,
          COUNT(DISTINCT fa.id_fact) AS actividades,
          COUNT(DISTINCT fi.id_fact) AS instituciones,
          COUNT(DISTINCT fb.id_fact) AS beneficiarios
        FROM dim_proyecto_estrategias p
        LEFT JOIN fact_actividades_estrategias fa ON p.id_proyecto = fa.id_proyecto
        LEFT JOIN fact_proyecto_institucion_estrategias fi ON p.id_proyecto = fi.id_proyecto
        LEFT JOIN fact_proyecto_beneficiario_estrategias fb ON p.id_proyecto = fb.id_proyecto
        GROUP BY p.id_proyecto, p.nombre_proyecto
        ORDER BY p.id_proyecto;
    """
}

# === Ejecutar validaciones ===
with engine.connect() as conn:
    print("\n🔍 Ejecutando validaciones de modelo de datos...\n")

    # 1️⃣ Validar dimensiones
    df_dims = pd.read_sql(text(validaciones["dimensiones_con_registros"]), conn)
    print("📊 Registros por dimensión:")
    print(df_dims, "\n")

    # 2️⃣ Validar hechos sin FK
    fk_checks = {}
    for nombre, sql in [
        ("hechos_sin_proyecto", "hechos_vs_proyecto"),
        ("hechos_sin_actividad", "hechos_vs_actividad"),
    ]:
        resultado = pd.read_sql(text(validaciones[sql]), conn).iloc[0, 0]
        fk_checks[nombre] = int(resultado)

    fk_inst = pd.read_sql(text(validaciones["integridad_fact_institucion"]), conn).iloc[0].to_dict()

    # 3️⃣ Consolidar resultados
    resumen_fk = {
        "Hechos sin Proyecto": fk_checks["hechos_sin_proyecto"],
        "Hechos sin Actividad": fk_checks["hechos_sin_actividad"],
        "Fact Institución sin Proyecto": fk_inst["sin_proyecto"],
        "Fact Institución sin Institución": fk_inst["sin_institucion"],
        "Fact Institución sin Municipio": fk_inst["sin_municipio"]
    }
    df_resumen_fk = pd.DataFrame.from_dict(resumen_fk, orient="index", columns=["Registros con error"])
    df_resumen_fk["Estado"] = df_resumen_fk["Registros con error"].apply(lambda x: "✅ OK" if x == 0 else "⚠️ Revisión necesaria")

    print("🔎 Validaciones de integridad referencial:")
    print(df_resumen_fk, "\n")

    # 4️⃣ Resumen global de integraciones
    df_global = pd.read_sql(text(validaciones["resumen_global"]), conn)
    print("🌐 Resumen de integridad global por proyecto:")
    print(df_global.head(10))  # muestra los primeros 10 proyectos

print("\n✅ Validaciones completadas.")
