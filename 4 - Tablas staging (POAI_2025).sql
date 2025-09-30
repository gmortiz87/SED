USE sised;

-- ========================
-- stg_fuente_poai
-- ========================
DROP TABLE IF EXISTS stg_fuente_poai_2025;
CREATE TABLE stg_fuente_poai_2025 (
  `N°` INT,
  `Nombre Proyecto` VARCHAR(255),
  `Código BPIN` VARCHAR(20),
  `Código PI` VARCHAR(20),
  `Apropiación Definitiva` DECIMAL(15,2), -- 🔹 corregido
  `Adición` DECIMAL(15,2),
  `Total Ejecutado` DECIMAL(15,2),        -- 🔹 nombre más genérico
  `Difrencia Apro - Ejec` DECIMAL(15,2),
  `Porcentaje de Ejecución` DECIMAL(5,2),
  `RECURSOS` VARCHAR(50),
  `Responsable SED` VARCHAR(255),
  `Enlace Técnico SED` VARCHAR(255),
  `Documentos del Proyecto` TEXT,
  `IGP` TEXT,
  `Avance en el Cargue de información` DECIMAL(5,2),
  `Hoja` VARCHAR(100)
) ENGINE=InnoDB;

-- ========================
-- stg_proyectos_poai
-- ========================
DROP TABLE IF EXISTS stg_proyectos_poai_2025;
CREATE TABLE stg_proyectos_poai_2025 (
  `Vigencia` VARCHAR(4),
  `Código BPIN` VARCHAR(20),   -- 🔹 más largo
  `Código PI` VARCHAR(20),     -- 🔹 más largo
  `Total Ejecutado` DECIMAL(15,2),
  `RECURSOS` VARCHAR(50),
  `Hoja` VARCHAR(100),
  `FUENTES` VARCHAR(100),
  `PROYECTOS` VARCHAR(100),
  `BENEFICIARIOS` VARCHAR(100),
  `Nombre_Proyecto` VARCHAR(255)  -- 🔹 ampliado
) ENGINE=InnoDB;

-- ========================
-- stg_actividades_poai
-- ========================
DROP TABLE IF EXISTS stg_actividades_poai_2025;
CREATE TABLE stg_actividades_poai_2025 (
  `N°` INT,
  `Actividad del Proyecto` TEXT,
  `Total Ejecutado` DECIMAL(18,2),
  `Componente PAM` VARCHAR(100),
  `¿A qué actor va dirigida?` VARCHAR(255),
  `Número de Beneficiarios` TEXT,
  `Entrega Dotación (SI / NO)` VARCHAR(50),
  `Descripción de la Dotación Entregada` TEXT,
  `Evidencia de la Actividad` TEXT,
  `Evidencia_URL` TEXT,
  `Observaciones Generales` TEXT,
  `Hoja` VARCHAR(100),
  `FUENTES` VARCHAR(100),
  `PROYECTOS` VARCHAR(100),
  `Nombre_Proyecto` VARCHAR(255)
) ENGINE=InnoDB;

-- ========================
-- stg_beneficiarios_poai
-- ========================
DROP TABLE IF EXISTS stg_beneficiarios_poai_2025;
CREATE TABLE stg_beneficiarios_poai_2025 (
  `N°` INT,
  `DANE IEO` VARCHAR(50),
  `MUNICIO` VARCHAR(100),  -- VALIDAR EL NOMBRE DE MUNICIPIO. ESTA MAL REDACTADO DE LA FUENTE. 
  `NOMBRE_IEO` VARCHAR(255),
  `# Directivos Beneficiados` INT,
  `# Administrativos Beneficiados` INT,
  `# Docentes Beneficiados` INT,
  `# Estudiantes Beneficiados` INT,
  `¿Recibió Asistencia Técnica?` VARCHAR(50),
  `Modalidad de la Asistencia Técnica` VARCHAR(255),
  `¿Recibió Dotación?` VARCHAR(50),
  `Dotación Recibida` TEXT,
  `Hoja` VARCHAR(100),
  `¿Asistencia Técnica?` VARCHAR(100),
  `# AFA Beneficiadas` VARCHAR(100),
  `¿Asistencia Técnica In Situ?` VARCHAR(100),
  `¿IEO BENEFICIADA?` VARCHAR(100),
  `IEO Beneficiada` VARCHAR(100),
  `# Padres, Madres y Cuidadores Beneficiados` VARCHAR(100),
  `Nombre Proyecto` VARCHAR(255),
  `FUENTES` VARCHAR(100),
  `PROYECTOS` VARCHAR(100)
) ENGINE=InnoDB;


-- ========================
-- stg_metas_poai
-- ========================
DROP TABLE IF EXISTS stg_metas_poai_2025;
CREATE TABLE stg_metas_poai_2025 (
  `ID_Meta` INT,
  `Hoja` VARCHAR(100),
  `Nombre_Proyecto` VARCHAR(255),
  `Descripción` VARCHAR(500)
) ENGINE=InnoDB;
