USE sised;

-- =====================================================
-- 🔹 CARGA DE DIMENSIONES
-- =====================================================

-- ========================
-- DIM FUENTE
-- ========================

TRUNCATE TABLE dim_fuente_regalias;
INSERT INTO dim_fuente_regalias (nombre_fuente, tipo_fuente, fuente, anio)
SELECT DISTINCT 
    TRIM(`Hoja`) AS nombre_fuente,
    TRIM(`RECURSOS`) AS tipo_fuente,
    'REGALIAS' AS fuente,
    '2025' AS anio
FROM stg_fuente_regalias
WHERE `Hoja` IS NOT NULL AND `Hoja` <> 'No reportado';

-- ========================
-- DIM PROYECTO
-- ========================

TRUNCATE TABLE dim_proyecto_regalias;
INSERT INTO dim_proyecto_regalias (
    id_proyecto, codigo_bpin, vigencia, nombre_proyecto, responsable,
    enlace_tecnico, apropiacion_pptal, total_ejecutado,
    documentos_proyecto, avance_avance, hoja_proyectos, hoja_fuentes
)
SELECT DISTINCT 
    p.`Código PI`,
    p.`Código BPIN`,
    p.`Vigencia`,
    p.`Nombre_Proyecto`,
    f.`Responsable SED`,
    f.`Enlace Técnico SED`,
    f.`Valor Total`,
    f.`Total Ejecutado`,
    f.`Documentos del Proyecto`,
    f.`Avance en el Cargue de información`,
    p.`Hoja`,
    p.`FUENTES`
FROM stg_proyectos_regalias p
LEFT JOIN stg_fuente_regalias f 
    ON TRIM(UPPER(p.`Nombre_Proyecto`)) = TRIM(UPPER(f.`Nombre Proyecto`))
WHERE p.`Nombre_Proyecto` IS NOT NULL
  AND p.`Nombre_Proyecto` <> 'No reportado'
  AND p.`Código PI` IS NOT NULL;

-- ========================
-- DIM ACTIVIDAD
-- ========================

TRUNCATE TABLE dim_actividad_regalias;
INSERT INTO dim_actividad_regalias (consecutivo, nombre_actividad, hoja_proyectos)
SELECT DISTINCT 
    a.`N°`,
    TRIM(a.`Actividad del Proyecto`),
    a.`Hoja`
FROM stg_actividades_regalias a
WHERE a.`Actividad del Proyecto` IS NOT NULL
  AND a.`Actividad del Proyecto` <> 'No reportado';

-- ========================
-- DIM MUNICIPIO
-- ========================

TRUNCATE TABLE dim_municipio_regalias;
INSERT INTO dim_municipio_regalias (nombre_municipio, departamento, region)
SELECT DISTINCT 
    TRIM(b.`MUNICIO`),
    NULL AS departamento,
    NULL AS region
FROM stg_beneficiarios_regalias b
WHERE b.`MUNICIO` IS NOT NULL
  AND b.`MUNICIO` <> 'No reportado';

-- ========================
-- DIM INSTITUCION
-- ========================

TRUNCATE TABLE dim_institucion_regalias;
INSERT INTO dim_institucion_regalias (id_institucion, nombre_ieo, codigo_dane, tipo, id_municipio)
SELECT 
    b.`DANE IEO` AS id_institucion,
    MAX(TRIM(b.`NOMBRE_IEO`)) AS nombre_ieo,
    b.`DANE IEO` AS codigo_dane,
    'IEO' AS tipo,
    MAX(m.id_municipio) AS id_municipio
FROM stg_beneficiarios_regalias b
LEFT JOIN dim_municipio_regalias m 
    ON TRIM(LOWER(b.`MUNICIO`)) = TRIM(LOWER(m.nombre_municipio))
WHERE b.`DANE IEO` IS NOT NULL
GROUP BY b.`DANE IEO`;

-- ========================
-- DIM META
-- ========================

TRUNCATE TABLE dim_meta_regalias;
INSERT INTO dim_meta_regalias (id_meta, descripcion_meta, unidad, valor_programado, valor_logrado, hoja_proyectos)
SELECT DISTINCT 
    m.`ID_Meta`,
    TRIM(m.`Descripción`) AS descripcion_meta,
    NULL AS unidad,
    NULL AS valor_programado,
    NULL AS valor_logrado,
    m.`Hoja`
FROM stg_metas_regalias m
WHERE m.`ID_Meta` IS NOT NULL
  AND TRIM(m.`Descripción`) <> '(sin descripción)'
  AND TRIM(m.`Descripción`) <> '';

-- ========================
-- DIM TIEMPO
-- ========================

TRUNCATE TABLE dim_tiempo_regalias;
INSERT INTO dim_tiempo_regalias (id_fecha, anio, mes, trimestre, fecha_completa)
SELECT 
    DATE_FORMAT(CURDATE(), '%Y%m%d'),
    YEAR(CURDATE()),
    MONTH(CURDATE()),
    QUARTER(CURDATE()),
    CURDATE();

-- =====================================================
-- 🔹 CARGA DE TABLAS DE HECHOS
-- =====================================================

-- ========================
-- FACT ACTIVIDADES
-- ========================

TRUNCATE TABLE fact_actividades_regalias;
INSERT INTO fact_actividades_regalias (
    id_proyecto, id_actividad, total_ejecutado,
    tipo_actividad, actor, beneficiarios,
    dotacion, descripcion_dotacion, evidencia_URL, id_fecha
)
SELECT 
    p.`Código PI`,
    a.`N°`,
    a.`Total Ejecutado`,
    a.`Componente PAM`,
    a.`¿A qué actor va dirigida?`,
    a.`Número de Beneficiarios`,
    a.`Entrega Dotación (SI / NO)`,
    a.`Descripción de la Dotación Entregada`,
    a.`Evidencia_URL`,
    DATE_FORMAT(CURDATE(), '%Y%m%d')
FROM stg_actividades_regalias a
JOIN stg_proyectos_regalias p 
    ON TRIM(UPPER(a.`Nombre_Proyecto`)) = TRIM(UPPER(p.`Nombre_Proyecto`))
WHERE p.`Código PI` IN (SELECT id_proyecto FROM dim_proyecto_regalias);

-- ========================
-- FACT PROYECTO-META
-- ========================

TRUNCATE TABLE fact_proyecto_meta_regalias;
INSERT INTO fact_proyecto_meta_regalias (id_proyecto, id_meta, id_fecha)
SELECT 
    p.`Código PI`,
    d.`id_meta`,
    DATE_FORMAT(CURDATE(), '%Y%m%d')
FROM stg_metas_regalias m
LEFT JOIN stg_proyectos_regalias p 
    ON TRIM(UPPER(m.`Nombre_Proyecto`)) = TRIM(UPPER(p.`Nombre_Proyecto`))
LEFT JOIN dim_meta_regalias d 
    ON TRIM(m.`Descripción`) = TRIM(d.`descripcion_meta`)
WHERE p.`Código PI` IN (SELECT id_proyecto FROM dim_proyecto_regalias)
  AND d.`id_meta` IS NOT NULL;   -- 🔹 evita insertar huérfanos
  
-- ========================
-- FACT PROYECTO-INSTITUCIÓN
-- ========================

TRUNCATE TABLE fact_proyecto_institucion_regalias;
INSERT INTO fact_proyecto_institucion_regalias (
    id_proyecto, id_institucion, id_municipio, hoja_origen, id_fecha
)
SELECT DISTINCT 
    p.`Código PI`,
    b.`DANE IEO`,
    m.id_municipio,
    b.`Hoja`,
    DATE_FORMAT(CURDATE(), '%Y%m%d')
FROM stg_beneficiarios_regalias b
JOIN stg_proyectos_regalias p 
    ON TRIM(UPPER(b.`PROYECTOS`)) = TRIM(UPPER(p.`Hoja`))
LEFT JOIN dim_municipio_regalias m 
    ON TRIM(UPPER(b.`MUNICIO`)) = TRIM(UPPER(m.nombre_municipio))
WHERE p.`Código PI` IN (SELECT id_proyecto FROM dim_proyecto_regalias)
  AND b.`DANE IEO` IN (SELECT id_institucion FROM dim_institucion_regalias);

-- ========================
-- FACT PROYECTO-BENEFICIARIOS
-- ========================

TRUNCATE TABLE fact_proyecto_beneficiario_regalias;
INSERT INTO fact_proyecto_beneficiario_regalias (
    id_proyecto, id_institucion,
    directivos_benef, administrativos_benef,
    docentes_benef, estudiantes_benef,
    asistencia_tecnica, modalidad_asistencia, 
    recibio_dotacion, dotacion_recibida, 
    acudientes_beneficiados, id_fecha
)
SELECT DISTINCT 
    p.`Código PI`,
    b.`DANE IEO`,
    b.`# Directivos Beneficiados`,
    b.`# Administrativos Beneficiados`,
    b.`# Docentes Beneficiados`,
    b.`# Estudiantes Beneficiados`,
    b.`¿Recibió Asistencia Técnica?`,
    b.`Modalidad de la Asistencia Técnica`,
    b.`¿Recibió Dotación?`,
    b.`Dotación Recibida`,
    b.`# Acudientes Beneficiados`,
    DATE_FORMAT(CURDATE(), '%Y%m%d')
FROM stg_beneficiarios_regalias b
LEFT JOIN stg_proyectos_regalias p 
    ON TRIM(UPPER(b.`PROYECTOS`)) = TRIM(UPPER(p.`Hoja`))
WHERE p.`Código PI` IN (SELECT id_proyecto FROM dim_proyecto_regalias)
  AND b.`DANE IEO` IN (SELECT id_institucion FROM dim_institucion_regalias);

-- =====================================================
-- 🔎 VALIDACIONES BÁSICAS
-- =====================================================
SELECT 'dim_fuente' AS tabla, COUNT(*) FROM dim_fuente_regalias
UNION ALL SELECT 'dim_proyecto', COUNT(*) FROM dim_proyecto_regalias
UNION ALL SELECT 'dim_institucion', COUNT(*) FROM dim_institucion_regalias
UNION ALL SELECT 'dim_meta', COUNT(*) FROM dim_meta_regalias
UNION ALL SELECT 'fact_actividades', COUNT(*) FROM fact_actividades_regalias
UNION ALL SELECT 'fact_beneficiarios', COUNT(*) FROM fact_proyecto_beneficiario_regalias;



-- =====================================================
-- 🔹 ELIMINACIÓN CONTROLADA DEL MODELO DIMENSIONAL REGALÍAS
-- =====================================================

-- ========================
-- 1️⃣ TABLAS DE HECHOS
-- ========================
DROP TABLE IF EXISTS fact_proyecto_beneficiario_regalias;
DROP TABLE IF EXISTS fact_proyecto_institucion_regalias;
DROP TABLE IF EXISTS fact_proyecto_meta_regalias;
DROP TABLE IF EXISTS fact_actividades_regalias;

-- ========================
-- 2️⃣ DIMENSIONES CON DEPENDENCIAS
-- ========================
DROP TABLE IF EXISTS dim_institucion_regalias;
DROP TABLE IF EXISTS dim_municipio_regalias;
DROP TABLE IF EXISTS dim_actividad_regalias;
DROP TABLE IF EXISTS dim_meta_regalias;
DROP TABLE IF EXISTS dim_tiempo_regalias;

-- ========================
-- 3️⃣ DIMENSIONES BASE (PADRES)
-- ========================
DROP TABLE IF EXISTS dim_proyecto_regalias;
DROP TABLE IF EXISTS dim_fuente_regalias;

-- =====================================================
-- 🔍 VERIFICACIÓN
-- =====================================================
SHOW TABLES LIKE '%regalias%';

