USE sised;

-- 6.1 Fuente
INSERT INTO fact_fuente_estrategias (Nombre_Proyecto, Vigencia, Entidad_Aliada, Responsable_SED, Enlace_Tecnico_SED, Info_Estrategia)
SELECT DISTINCT
  `Nombre Proyecto`, Vigencia, `ENTIDAD ALIADA`, `Responsable SED`, `Enlace Técnico SED`, `INFORMACIÓN ESTRATEGIA`
FROM stg_fuente_estrategias s
WHERE `Nombre Proyecto` IS NOT NULL
ON DUPLICATE KEY UPDATE
  Vigencia = VALUES(Vigencia),
  Entidad_Aliada = VALUES(Entidad_Aliada),
  Responsable_SED = VALUES(Responsable_SED),
  Enlace_Tecnico_SED = VALUES(Enlace_Tecnico_SED),
  Info_Estrategia = VALUES(Info_Estrategia);

-- 6.2 Proyectos
INSERT INTO fact_proyectos_estrategias (ID_Fuente, Nombre_Proyecto, Hoja)
SELECT f.ID_Fuente, p.Nombre_Proyecto, p.Hoja
FROM (
  SELECT DISTINCT COALESCE(`Nombre_Proyecto`, `Nombre Proyecto`) AS Nombre_Proyecto, Hoja
  FROM stg_proyectos_estrategias
) p
JOIN fact_fuente_estrategias f ON f.Nombre_Proyecto = p.Nombre_Proyecto
ON DUPLICATE KEY UPDATE
  Hoja = VALUES(Hoja), ID_Fuente = VALUES(ID_Fuente);

-- 6.3 Actividades
INSERT INTO fact_actividades_estrategias (ID_Proyecto, Actividad, Total_Ejecutado, Componente_PAM, Actor_Dirigido, Numero_Beneficiarios, Hoja)
SELECT pr.ID_Proyecto,
       a.`Actividad del Proyecto`,
       a.`Total Ejecutado`,
       a.`Componente PAM`,
       a.`¿A qué actor va dirigida?`,
       a.`Número de Beneficiarios`,
       a.Hoja
FROM stg_actividades_estrategias a
JOIN fact_proyectos_estrategias pr
  ON pr.Hoja = a.PROYECTOS  -- tu regla de empareje "Hoja del proyecto"
;

-- 6.4 Beneficiarios
INSERT INTO fact_beneficiarios_estrategias
  (ID_Proyecto, DANE_IEO, Municipio, Nombre_IEO,
   Directivos_Beneficiados, Docentes_Beneficiados, Estudiantes_Beneficiados, Administrativos_Beneficiados,
   Recibio_Asistencia, Recibio_Dotacion, Hoja)
SELECT pr.ID_Proyecto,
       b.`DANE IEO`, b.`MUNICIO`, b.`NOMBRE_IEO`,
       b.`# Directivos Beneficiados`, b.`# Docentes Beneficiados`, b.`# Estudiantes Beneficiados`, b.`# Administrativos Beneficiados`,
       (CASE WHEN b.`¿Recibió Asistencia Técnica?` IN ('SI','Sí','YES','True','1') THEN 1 ELSE 0 END),
       (CASE WHEN b.`¿Recibió Dotación?` IN ('SI','Sí','YES','True','1') THEN 1 ELSE 0 END),
       b.PROYECTOS
FROM stg_beneficiarios_estrategias b
JOIN fact_proyectos_estrategias pr
  ON pr.Hoja = b.PROYECTOS
;

-- 6.5 Puente Actividad–Beneficiario (N:N) por "Hoja"
-- ATENCIÓN: Esto crea todas las combinaciones Actividad x Beneficiario dentro de la misma Hoja.
-- Verifica que tu lógica de negocio lo permita para evitar "explosión" de filas.
INSERT IGNORE INTO fact_beneficiarios_actividades (ID_Actividad, ID_Beneficiario, Numero_Beneficiarios)
SELECT a.ID_Actividad, bn.ID_Beneficiario,
       COALESCE(a.Numero_Beneficiarios, 0)
FROM fact_actividades_estrategias a
JOIN fact_beneficiarios_estrategias bn
  ON a.Hoja = bn.Hoja;
