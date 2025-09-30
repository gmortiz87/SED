-- Conteos
SELECT 'Fuente' as tabla, COUNT(*) FROM fact_fuente_estrategias
UNION ALL SELECT 'Proyectos', COUNT(*) FROM fact_proyectos_estrategias
UNION ALL SELECT 'Actividades', COUNT(*) FROM fact_actividades_estrategias
UNION ALL SELECT 'Beneficiarios', COUNT(*) FROM fact_beneficiarios_estrategias
UNION ALL SELECT 'Puente', COUNT(*) FROM fact_beneficiarios_actividades;

-- Beneficiarios sin proyecto (no debería haber)
SELECT * FROM fact_beneficiarios_estrategias b
LEFT JOIN fact_proyectos_estrategias p ON p.ID_Proyecto = b.ID_Proyecto
WHERE p.ID_Proyecto IS NULL;

-- Actividades sin proyecto (no debería haber)
SELECT * FROM fact_actividades_estrategias a
LEFT JOIN fact_proyectos_estrategias p ON p.ID_Proyecto = a.ID_Proyecto
WHERE p.ID_Proyecto IS NULL;
