USE sised;

-- ========================
-- stg_fuente_estrategias
-- ========================
DROP TABLE IF EXISTS stg_fuente_estrategias;
CREATE TABLE stg_fuente_estrategias (
  `N°` INT,
  `Nombre Proyecto` VARCHAR(255),
  `VIGENCIA` VARCHAR(50),
  `ENTIDAD ALIADA` VARCHAR(255),
  `Responsable SED` VARCHAR(255),
  `Enlace Técnico SED` VARCHAR(255),
  `INFORMACIÓN ESTRATEGIA` TEXT,
  `ENLACE BENEFICIARIOS` TEXT,
  `Documentos de la Estrategia` TEXT,
  `Avance en el Cargue de información` DECIMAL(5,2),
  `Hoja` VARCHAR(100)
) ENGINE=InnoDB;

-- ========================
-- stg_proyectos_estrategias
-- (esta tabla antes estaba mal: FUENTES, PROYECTOS, BENEFICIARIOS no corresponden)
-- ========================
DROP TABLE IF EXISTS stg_proyectos_estrategias;
CREATE TABLE stg_proyectos_estrategias (
    `Hoja` VARCHAR(100) PRIMARY KEY,
    `Fuente` VARCHAR(50),
    `Proyecto_Cod` VARCHAR(100),
    `Beneficiarios` VARCHAR(100),
    `Nombre_Proyecto` VARCHAR(255)
) ENGINE=InnoDB;


-- ========================
-- stg_actividades_estrategias
-- (corregido: quitamos DECIMAL de Total Ejecutado y renombramos campos según Excel real)
-- ========================
DROP TABLE IF EXISTS stg_actividades_estrategias;
CREATE TABLE stg_actividades_estrategias (
  `N°` INT,
  `Actividad del Proyecto` TEXT,
  `¿A qué actor va dirigida?` VARCHAR(255),
  `Número de Beneficiarios` TEXT,
  `Entrega Dotación (SI / NO)` VARCHAR(50),
  `Descripción de la Dotación Entregada` TEXT,
  `Evidencia de la Actividad` TEXT,
  `Evidencia_URL` TEXT,
  `Observaciones Generales` TEXT,
  `Hoja` VARCHAR(100),
  `PROYECTOS` VARCHAR(100),
  `Nombre_Proyecto` VARCHAR(255)
) ENGINE=InnoDB;

-- ========================
-- stg_beneficiariosstg_actividades_estrategias_estrategias
-- ========================
DROP TABLE IF EXISTS stg_beneficiarios_estrategias;
CREATE TABLE stg_beneficiarios_estrategias (
  `N°` INT,
  `DANE IEO` VARCHAR(50),
  `MUNICIO` VARCHAR(100),
  `NOMBRE_IEO` VARCHAR(255),
  `# Directivos Beneficiados` INT,
  `# Administrativos Beneficiados` INT,
  `# Docentes Beneficiados` INT,
  `# Estudiantes Beneficiados` INT,
  `¿Recibió Asistencia Técnica?` varchar(50),
  `Modalidad de la Asistencia Técnica` VARCHAR(255),
  `¿Recibió Dotación?` VARCHAR(50),
  `Dotación Recibida` TEXT,
  `Hoja` VARCHAR(100),
  `Nombre Proyecto` VARCHAR(255)
) ENGINE=InnoDB;

