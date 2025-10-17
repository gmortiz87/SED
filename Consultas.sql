use sised;
show tables;

SELECT * FROM stg_beneficiarios_poai_2025; -- t5
SELECT * FROM stg_metas_poai_2025; -- t4
SELECT * FROM stg_actividades_poai_2025; -- t3
SELECT * FROM stg_proyectos_poai_2025; -- t2
SELECT * FROM stg_fuente_poai_2025; -- t1


-- ::::::::::::::::::::::
SELECT
	t1.`Código PI` AS ID_Proyecto,
    t1.`Nombre Proyecto` AS Proyecto,
	t1.`Apropiación Definitiva` AS Apr_Def,
    t1.`Adición` AS Adición,
    t1.`Difrencia Apro - Ejec` as Diferencia_Apr_Ejc,
    t1.`Porcentaje de Ejecución` * 100  as Porcentaje_Ejec,
    t1.`RECURSOS`, 
    t1.`Responsable SED`, 
    t1.`Enlace Técnico SED`, 
    t1.`Documentos del Proyecto`, 
    t1.`Avance en el Cargue de información` * 100 AS Avance_Carga,
    t1.`Hoja` AS Fuente,
    t2.`Hoja` AS ID_proyecto, 
    t2.`Vigencia`,
    t2.`Código BPIN`,
    t2.`Total Ejecutado`,
    t3.`Actividad del Proyecto`,
    t3.`Total Ejecutado`,
    t3.`Componente PAM`,
    t3.`¿A qué actor va dirigida?`,
    t3.`Número de Beneficiarios`,
    t3.`Entrega Dotación (SI / NO)`
FROM
	stg_actividades_poai_2025 AS t3 
JOIN 
    stg_proyectos_poai_2025 AS t2
ON t2.`Hoja` = t3.`Hoja`
JOIN
    stg_fuente_poai_2025 AS t1 
ON t1.`Código PI` = t2.`Código PI`
-- where t1.`Responsable SED` like '%Sara%'
;
-- WHERE t1.`Código PI` = '102569';

-- :::::::::::::::::::::: relación general

SELECT
    t1.`Código PI` AS ID_Proyecto,
    t1.`Nombre Proyecto` AS Proyecto,
    t1.`Apropiación Definitiva` AS Apr_Def,
    t1.`Adición` AS Adición,
    t1.`Difrencia Apro - Ejec` AS Diferencia_Apr_Ejc,
    t1.`Porcentaje de Ejecución` * 100 AS Porcentaje_Ejec,
    t1.`RECURSOS`,
    t1.`Responsable SED`,
    t1.`Enlace Técnico SED`,
    t1.`Documentos del Proyecto`,
    t1.`Avance en el Cargue de información` * 100 AS Avance_Carga,
    t1.`Hoja` AS Fuente_Financiera, -- Alias corregido
    t2.`Hoja` AS ID_proyecto_Hoja, -- Alias corregido
    t2.`Vigencia`,
    t2.`Código BPIN`,
    t2.`Total Ejecutado` AS Total_Ejecutado_Proy, -- Alias corregido
    t3.`Actividad del Proyecto`,
    t3.`Total Ejecutado` AS Total_Ejecutado_Act, -- Alias corregido
    t3.`Componente PAM`,
    t3.`¿A qué actor va dirigida?`,
    t3.`Número de Beneficiarios`,
    t3.`Entrega Dotación (SI / NO)`,
    t3.`Evidencia_URL`,
    t4.`Descripción` AS Meta_Producto,
    t5.`MUNICIPIO` AS MUNICIPIO,
    t5.`NOMBRE_IEO` AS MUNICIPIO
FROM
    stg_fuente_poai_2025 AS t1 -- Tabla base: Información financiera y general (Fuente)
JOIN
    stg_proyectos_poai_2025 AS t2 -- Unir con la tabla de Proyectos
    ON t1.`Código PI` = t2.`Código PI` -- Unir proyectos y su fuente por Código PI
JOIN
    stg_actividades_poai_2025 AS t3 -- Unir con la tabla de Actividades
    ON t2.`Hoja` = t3.`Hoja` -- Asumo que Hoja es la clave de unión entre Proyectos y Actividades
JOIN
    stg_metas_poai_2025 AS t4 -- Unir con la tabla de Metas
    ON t2.`Hoja` = t4.`Hoja` -- Asumo que Hoja es la clave de unión entre Proyectos y Metas
JOIN
    stg_beneficiarios_poai_2025 AS t5 -- Unir con la tabla de Metas
    ON t2.`Hoja` = t5.`PROYECTOS` -- Asumo que Hoja es la clave de unión entre Proyectos y Metas
;

