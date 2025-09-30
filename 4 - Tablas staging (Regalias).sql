USE sised;

-- ========================
-- stg_fuente_regalias
-- ========================
DROP TABLE IF EXISTS stg_fuente_regalias;
CREATE TABLE stg_fuente_regalias (
  `N°` INT,
  `Nombre Proyecto` VARCHAR(255),
  `Código BPIN` VARCHAR(20),
  `Vigencia` VARCHAR(100),
  `Valor Total` DECIMAL(15,2), -- 🔹 corregido
  `Total Ejecutado` DECIMAL(15,2),
  `Difrencia Apro - Ejec` DECIMAL(15,2),
  `Porcentaje de Ejecución` DECIMAL(5,2),
  `RECURSOS` VARCHAR(50),
  `Responsable SED` VARCHAR(100),
  `Enlace Técnico SED` VARCHAR(100),
  `Documentos del Proyecto` TEXT,
  `Avance en el Cargue de información` DECIMAL(5,2),
  `Hoja` VARCHAR(100)
) ENGINE=InnoDB;

-- ========================
-- stg_proyectos_regalias
-- ========================
DROP TABLE IF EXISTS stg_proyectos_regalias;
CREATE TABLE stg_proyectos_regalias (
  `Vigencia` VARCHAR(100),
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
DROP TABLE IF EXISTS stg_actividades_regalias;
CREATE TABLE stg_actividades_regalias (
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
-- stg_beneficiarios_regalias
-- ========================
DROP TABLE IF EXISTS stg_beneficiarios_regalias;
CREATE TABLE stg_beneficiarios_regalias (
  `N°` INT,
  `DANE IEO` VARCHAR(50),
  `MUNICIO` VARCHAR(100),
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
  `# Acudientes Beneficiados` VARCHAR(100), -- 🔹 dejar texto porque había registros no numéricos
  `Nombre Proyecto` VARCHAR(255),
  `FUENTES` VARCHAR(100),
  `PROYECTOS` VARCHAR(100),
  `BENEFICIARIOS` VARCHAR(100)
) ENGINE=InnoDB;

-- ========================
-- stg_metas_poai
-- ========================
DROP TABLE IF EXISTS stg_metas_regalias;
CREATE TABLE stg_metas_regalias (
  `ID_Meta` INT,
  `Hoja` VARCHAR(100),
  `Nombre_Proyecto` VARCHAR(255),
  `Descripción` VARCHAR(500)
) ENGINE=InnoDB;