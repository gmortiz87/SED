USE sised;



INSERT INTO dim_fuente_poai_2025 (nombre_fuente, tipo_fuente, fuente, anio)
SELECT DISTINCT 
    `Hoja` AS nombre_fuente,
    `RECURSOS` AS tipo_fuente,
    'POAI' AS fuente,
    '2025' AS anio
FROM stg_fuente_poai_2025
WHERE `Hoja` IS NOT NULL AND `Hoja` <> '';



INSERT INTO dim_proyecto_poai_2025 (
    id_proyecto, codigo_bpin, nombre_proyecto, responsable,
    enlace_tecnico, sector, apropiacion_pptal, adicion_pptal, total_ejecutado,
    documentos_proyecto, avance_avance, hoja_proyectos, hoja_fuentes
)
SELECT DISTINCT 
    p.`Código PI`,
    p.`Código BPIN`,
    TRIM(p.`Nombre_Proyecto`),
    f.`Responsable SED`,
    f.`Enlace Técnico SED`,
    NULL AS sector,
    f.`Apropiación Definitiva`,
    f.`Adición`,
    f.`Total Ejecutado`,
    f.`Documentos del Proyecto`,
    f.`Avance en el Cargue de información`,
    p.`Hoja`,
    p.`FUENTES`
FROM stg_proyectos_poai_2025 p
LEFT JOIN stg_fuente_poai_2025 f 
    ON TRIM(UPPER(p.`Nombre_Proyecto`)) = TRIM(UPPER(f.`Nombre Proyecto`))
WHERE p.`Código PI` IS NOT NULL
  AND p.`Nombre_Proyecto` <> 'No reportado';
  
  select * from dim_proyecto_poai_2025;



INSERT INTO dim_actividad_poai_2025 (consecutivo, nombre_actividad, hoja_proyectos)
SELECT DISTINCT 
    a.`N°`,
    TRIM(a.`Actividad del Proyecto`),
    a.`Hoja`
FROM stg_actividades_poai_2025 a
WHERE a.`Actividad del Proyecto` IS NOT NULL
  AND a.`Actividad del Proyecto` <> 'No reportado';
  
SELECT * FROM dim_actividad_poai_2025 d;




INSERT INTO dim_municipio_poai_2025 (nombre_municipio, departamento, region)
SELECT DISTINCT 
    TRIM(b.`MUNICIPIO`),
    NULL AS departamento,
    NULL AS region
FROM stg_beneficiarios_poai_2025 b
WHERE b.`MUNICIPIO` IS NOT NULL AND b.`MUNICIPIO` <> '';



INSERT INTO dim_institucion_poai_2025 (id_institucion, nombre_ieo, codigo_dane, tipo, id_municipio)
SELECT DISTINCT 
    b.`DANE IEO`,
    TRIM(b.`NOMBRE_IEO`),
    b.`DANE IEO`,
    'IEO',
    m.id_municipio
FROM stg_beneficiarios_poai_2025 b
LEFT JOIN dim_municipio_poai_2025 m 
    ON TRIM(UPPER(b.`MUNICIPIO`)) = TRIM(UPPER(m.nombre_municipio))
WHERE b.`DANE IEO` IS NOT NULL
  AND b.`DANE IEO` <> '';
  


INSERT INTO dim_meta_poai_2025 (id_meta, descripcion_meta, unidad, valor_programado, valor_logrado, hoja_proyectos)
SELECT DISTINCT 
    m.`ID_Meta`,
    CASE 
        WHEN TRIM(m.`Descripción`) = '' THEN '(sin descripción)'
        ELSE TRIM(m.`Descripción`)
    END AS descripcion_meta,
    NULL AS unidad,
    NULL AS valor_programado,
    NULL AS valor_logrado,
    m.`Hoja`
FROM stg_metas_poai_2025 m
WHERE m.`ID_Meta` IS NOT NULL;



INSERT INTO dim_tiempo_poai_2025 (id_fecha, anio, mes, trimestre, fecha_completa)
SELECT 
    DATE_FORMAT(CURDATE(), '%Y%m%d'),
    YEAR(CURDATE()),
    MONTH(CURDATE()),
    QUARTER(CURDATE()),
    CURDATE();




INSERT INTO fact_actividades_poai_2025 (
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
    CASE 
        WHEN a.`Número de Beneficiarios` REGEXP '^[0-9]+$'
             THEN CAST(a.`Número de Beneficiarios` AS SIGNED)
        ELSE NULL
    END AS beneficiarios,
    a.`Entrega Dotación (SI / NO)`,
    a.`Descripción de la Dotación Entregada`,
    a.`Evidencia_URL`,
    DATE_FORMAT(CURDATE(), '%Y%m%d')
FROM stg_actividades_poai_2025 a
LEFT JOIN stg_proyectos_poai_2025 p 
    ON TRIM(UPPER(a.`Nombre_Proyecto`)) = TRIM(UPPER(p.`Nombre_Proyecto`))
WHERE p.`Código PI` IN (SELECT id_proyecto FROM dim_proyecto_poai_2025);




INSERT INTO fact_proyecto_meta_poai_2025 (id_proyecto, id_meta, id_fecha)
SELECT 
    p.`Código PI`,
    m.`ID_Meta`,
    DATE_FORMAT(CURDATE(), '%Y%m%d')
FROM stg_metas_poai_2025 m
LEFT JOIN stg_proyectos_poai_2025 p 
    ON TRIM(UPPER(m.`Nombre_Proyecto`)) = TRIM(UPPER(p.`Nombre_Proyecto`))
WHERE p.`Código PI` IS NOT NULL;

select * from fact_proyecto_meta_poai_2025;



INSERT INTO fact_proyecto_institucion_poai_2025 (
    id_proyecto, id_institucion, id_municipio, hoja_origen, id_fecha
)
SELECT DISTINCT 
    p.`Código PI`,
    b.`DANE IEO`,
    m.id_municipio,
    b.`Hoja`,
    DATE_FORMAT(CURDATE(), '%Y%m%d')
FROM stg_beneficiarios_poai_2025 b
JOIN stg_proyectos_poai_2025 p 
    ON TRIM(UPPER(b.`PROYECTOS`)) = TRIM(UPPER(p.`Hoja`))
LEFT JOIN dim_municipio_poai_2025 m 
    ON TRIM(UPPER(b.`MUNICIPIO`)) = TRIM(UPPER(m.nombre_municipio))
WHERE p.`Código PI` IN (SELECT id_proyecto FROM dim_proyecto_poai_2025)
  AND b.`DANE IEO` IN (SELECT id_institucion FROM dim_institucion_poai_2025);




INSERT INTO fact_proyecto_beneficiario_poai_2025 (
    id_proyecto, id_institucion,
    directivos_benef, administrativos_benef,
    docentes_benef, estudiantes_benef,
    asistencia_tecnica, modalidad_asistencia,
    recibio_dotacion, dotacion_recibida, id_fecha
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
    DATE_FORMAT(CURDATE(), '%Y%m%d')
FROM stg_beneficiarios_poai_2025 b
LEFT JOIN stg_proyectos_poai_2025 p 
    ON TRIM(UPPER(b.`PROYECTOS`)) = TRIM(UPPER(p.`Hoja`))
WHERE p.`Código PI` IN (SELECT id_proyecto FROM dim_proyecto_poai_2025)
  AND b.`DANE IEO` IN (SELECT id_institucion FROM dim_institucion_poai_2025);

