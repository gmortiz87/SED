USE sised;

-- =====================================================
-- 🧱 ETL: DIMENSIONES
-- =====================================================

-- ========================
-- DIM FUENTE
-- ========================
TRUNCATE TABLE dim_fuente_estrategias;

INSERT INTO dim_fuente_estrategias (nombre_fuente, fuente, anio)
SELECT DISTINCT 
    `Nombre Proyecto` AS nombre_fuente,
    `Hoja` AS fuente,
    '2025' AS anio
FROM stg_fuente_estrategias
WHERE `Nombre Proyecto` IS NOT NULL
  AND `Nombre Proyecto` <> 'No reportado';

-- ========================
-- DIM PROYECTO
-- ========================
TRUNCATE TABLE dim_proyecto_estrategias;

INSERT INTO dim_proyecto_estrategias (
    id_proyecto, nombre_proyecto, entidad_aliada, responsable,
    enlace_tecnico, documentos_proyecto, avance, hoja_proyectos, hoja_fuentes
)
SELECT DISTINCT 
    p.id_proyecto,
    COALESCE(p.`Nombre_Proyecto`, CONCAT('Proyecto_', p.id_proyecto)) AS nombre_proyecto,
    f.`ENTIDAD ALIADA`,
    f.`Responsable SED`,
    f.`Enlace Técnico SED`,
    f.`Documentos de la Estrategia`,
    f.`Avance en el Cargue de información`,
    p.`Hoja`,
    f.`Hoja`
FROM stg_proyectos_estrategias p
LEFT JOIN stg_fuente_estrategias f 
    ON p.`Nombre_Proyecto` = f.`Nombre Proyecto`;

-- ========================
-- DIM ACTIVIDAD
-- ========================
TRUNCATE TABLE dim_actividad_estrategias;

INSERT INTO dim_actividad_estrategias (
    consecutivo, nombre_actividad, hoja_proyectos
)
SELECT DISTINCT 
    a.`N°`,
    a.`Actividad del Proyecto`,
    a.`Hoja`
FROM stg_actividades_estrategias a
WHERE a.`Actividad del Proyecto` IS NOT NULL
  AND a.`Actividad del Proyecto` <> 'No reportado';

-- ========================
-- DIM MUNICIPIO
-- ========================
TRUNCATE TABLE dim_municipio_estrategias;

INSERT INTO dim_municipio_estrategias (
    nombre_municipio, departamento, region
)
SELECT DISTINCT 
    TRIM(b.`MUNICIO`) AS nombre_municipio,
    NULL AS departamento,
    NULL AS region
FROM stg_beneficiarios_estrategias b
WHERE b.`MUNICIO` IS NOT NULL
  AND b.`MUNICIO` <> 'No reportado';

-- ========================
-- DIM INSTITUCION
-- ========================
TRUNCATE TABLE dim_institucion_estrategias;

INSERT INTO dim_institucion_estrategias (
    id_institucion, nombre_ieo, codigo_dane, tipo, id_municipio
)
SELECT 
    b.`DANE IEO` AS id_institucion,
    MAX(b.`NOMBRE_IEO`) AS nombre_ieo,
    b.`DANE IEO` AS codigo_dane,
    'IEO' AS tipo,
    MAX(m.id_municipio) AS id_municipio
FROM stg_beneficiarios_estrategias b
LEFT JOIN dim_municipio_estrategias m 
    ON TRIM(LOWER(b.`MUNICIO`)) = TRIM(LOWER(m.nombre_municipio))
WHERE b.`DANE IEO` IS NOT NULL
GROUP BY b.`DANE IEO`;

-- ========================
-- DIM TIEMPO (Carga por defecto)
-- ========================
TRUNCATE TABLE dim_tiempo_estrategias;
INSERT INTO dim_tiempo_estrategias (id_fecha, anio, mes, trimestre, fecha_completa)
SELECT DISTINCT
    DATE_FORMAT(CURDATE(), '%Y%m%d') AS id_fecha,
    YEAR(CURDATE()) AS anio,
    MONTH(CURDATE()) AS mes,
    QUARTER(CURDATE()) AS trimestre,
    CURDATE() AS fecha_completa;

-- =====================================================
-- 🧩 CARGA DE TABLAS DE HECHOS 2025
-- =====================================================

-- ========================
-- FACT ACTIVIDADES
-- ========================

TRUNCATE TABLE fact_actividades_estrategias;
INSERT INTO fact_actividades_estrategias (
    id_proyecto, id_actividad, actor, beneficiarios,
    dotacion, descripcion_dotacion, evidencia_URL, hoja, id_fecha
)
SELECT 
    d.id_proyecto,
    a_dim.id_actividad,
    a.`¿A qué actor va dirigida?` AS actor,
    a.`Número de Beneficiarios` AS beneficiarios,
    a.`Entrega Dotación (SI / NO)` AS dotacion,
    a.`Descripción de la Dotación Entregada` AS descripcion_dotacion,
    a.`Evidencia_URL`,
    a.`Hoja`,
    DATE_FORMAT(CURDATE(), '%Y%m%d') AS id_fecha
FROM stg_actividades_estrategias a
LEFT JOIN stg_proyectos_estrategias p ON a.Hoja = p.Hoja
LEFT JOIN dim_proyecto_estrategias d ON p.id_proyecto = d.id_proyecto
LEFT JOIN dim_actividad_estrategias a_dim 
    ON TRIM(LOWER(a.`Actividad del Proyecto`)) = TRIM(LOWER(a_dim.nombre_actividad))
WHERE d.id_proyecto IS NOT NULL
  AND a_dim.id_actividad IS NOT NULL;

-- ========================
-- FACT PROYECTO - INSTITUCION
-- ========================

TRUNCATE TABLE fact_proyecto_institucion_estrategias;
INSERT INTO fact_proyecto_institucion_estrategias (
    id_proyecto, id_institucion, id_municipio, hoja_origen, hoja_proyecto, id_fecha
)
SELECT DISTINCT 
    p.id_proyecto,
    i.id_institucion,
    m.id_municipio,
    b.`Hoja` AS hoja_origen,
    p.`Hoja` AS hoja_proyecto,
    DATE_FORMAT(CURDATE(), '%Y%m%d') AS id_fecha
FROM stg_beneficiarios_estrategias b
LEFT JOIN stg_proyectos_estrategias p 
    ON TRIM(LOWER(b.`Nombre Proyecto`)) = TRIM(LOWER(p.`Nombre_Proyecto`))
LEFT JOIN dim_institucion_estrategias i ON b.`DANE IEO` = i.id_institucion
LEFT JOIN dim_municipio_estrategias m ON TRIM(LOWER(b.`MUNICIO`)) = TRIM(LOWER(m.nombre_municipio))
WHERE p.id_proyecto IS NOT NULL
  AND b.`DANE IEO` IN (SELECT id_institucion FROM dim_institucion_estrategias); --

-- ========================
-- FACT PROYECTO - BENEFICIARIO
-- ========================
TRUNCATE TABLE fact_proyecto_beneficiario_estrategias;
INSERT INTO fact_proyecto_beneficiario_estrategias (
    id_proyecto, id_institucion, directivos_benef, administrativos_benef, 
    docentes_benef, estudiantes_benef, asistencia_tecnica, modalidad_asistencia, 
    recibio_dotacion, dotacion_recibida, id_fecha
)
SELECT DISTINCT 
    p.id_proyecto,
    b.`DANE IEO` AS id_institucion,
    b.`# Directivos Beneficiados`,
    b.`# Administrativos Beneficiados`,
    b.`# Docentes Beneficiados`,
    b.`# Estudiantes Beneficiados`,
    b.`¿Recibió Asistencia Técnica?`,
    b.`Modalidad de la Asistencia Técnica`,
    b.`¿Recibió Dotación?`,
    b.`Dotación Recibida`,
    DATE_FORMAT(CURDATE(), '%Y%m%d') AS id_fecha
FROM stg_beneficiarios_estrategias b
LEFT JOIN stg_proyectos_estrategias p 
    ON TRIM(LOWER(b.`Nombre Proyecto`)) = TRIM(LOWER(p.`Nombre_Proyecto`))
WHERE p.id_proyecto IS NOT NULL
AND b.`DANE IEO` IN (SELECT id_institucion FROM dim_institucion_estrategias); --

-- =====================================================
-- ✅ RESUMEN GENERAL
-- =====================================================
SELECT 'dim_fuente_estrategias' AS tabla, COUNT(*) AS filas FROM dim_fuente_estrategias
UNION ALL SELECT 'dim_proyecto_estrategias', COUNT(*) FROM dim_proyecto_estrategias
UNION ALL SELECT 'dim_actividad_estrategias', COUNT(*) FROM dim_actividad_estrategias
UNION ALL SELECT 'dim_municipio_estrategias', COUNT(*) FROM dim_municipio_estrategias
UNION ALL SELECT 'dim_institucion_estrategias', COUNT(*) FROM dim_institucion_estrategias
UNION ALL SELECT 'dim_tiempo_estrategias', COUNT(*) FROM dim_tiempo_estrategias
UNION ALL SELECT 'fact_actividades_estrategias', COUNT(*) FROM fact_actividades_estrategias
UNION ALL SELECT 'fact_proyecto_institucion_estrategias', COUNT(*) FROM fact_proyecto_institucion_estrategias
UNION ALL SELECT 'fact_proyecto_beneficiario_estrategias', COUNT(*) FROM fact_proyecto_beneficiario_estrategias;

