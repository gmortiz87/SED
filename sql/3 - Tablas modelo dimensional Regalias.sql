USE sised;

-- =====================================================
--  MODELO DIMENSIONAL REGALÍAS
-- =====================================================

-- =====================================================
-- 🔹 DIMENSIONES
-- =====================================================

-- ========================
-- dim_fuente_regalias
-- ========================
DROP TABLE IF EXISTS dim_fuente_regalias;
CREATE TABLE dim_fuente_regalias (
    id_fuente INT AUTO_INCREMENT PRIMARY KEY,
    nombre_fuente VARCHAR(255),
    tipo_fuente VARCHAR(100),
    fuente VARCHAR(100),
    anio VARCHAR(4) DEFAULT '2025'
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;

-- ========================
-- dim_proyecto_regalias
-- ========================
DROP TABLE IF EXISTS dim_proyecto_regalias;
CREATE TABLE dim_proyecto_regalias (
    id_proyecto VARCHAR(20) PRIMARY KEY,         -- Código PI
    codigo_bpin VARCHAR(20),
    vigencia VARCHAR(50),
    nombre_proyecto VARCHAR(255),
    responsable VARCHAR(255),
    enlace_tecnico VARCHAR(255),
    apropiacion_pptal DECIMAL(15,2),             -- Valor total
    total_ejecutado DECIMAL(15,2),
    documentos_proyecto TEXT,
    avance_avance DECIMAL(5,2),
    hoja_proyectos VARCHAR(100),
    hoja_fuentes VARCHAR(100)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;

-- ========================
-- dim_municipio_regalias
-- ========================
DROP TABLE IF EXISTS dim_municipio_regalias;
CREATE TABLE dim_municipio_regalias (
    id_municipio INT AUTO_INCREMENT PRIMARY KEY,
    nombre_municipio VARCHAR(255),
    departamento VARCHAR(255),
    region VARCHAR(255)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;

-- ========================
-- dim_institucion_regalias
-- ========================
DROP TABLE IF EXISTS dim_institucion_regalias;
CREATE TABLE dim_institucion_regalias (
    id_institucion VARCHAR(50) PRIMARY KEY,  
    nombre_ieo VARCHAR(255),
    codigo_dane VARCHAR(50),
    tipo VARCHAR(50) DEFAULT 'IEO',
    id_municipio INT,
    FOREIGN KEY (id_municipio) REFERENCES dim_municipio_regalias(id_municipio)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;

-- ========================
-- dim_actividad_regalias
-- ========================
DROP TABLE IF EXISTS dim_actividad_regalias;
CREATE TABLE dim_actividad_regalias (
    id_actividad INT NOT NULL AUTO_INCREMENT,
    consecutivo INT NOT NULL,
    nombre_actividad TEXT NOT NULL,
    hoja_proyectos VARCHAR(100),
    PRIMARY KEY (id_actividad)
) ENGINE=InnoDB
AUTO_INCREMENT=100
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;

-- ========================
-- dim_meta_regalias
-- ========================
DROP TABLE IF EXISTS dim_meta_regalias;
CREATE TABLE dim_meta_regalias (
    id_meta INT PRIMARY KEY,
    descripcion_meta VARCHAR(500),
    unidad VARCHAR(100) NULL,
    valor_programado DECIMAL(15,2) NULL,
    valor_logrado DECIMAL(15,2) NULL,
    hoja_proyectos VARCHAR(100)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;

-- ========================
-- dim_tiempo_regalias
-- ========================
DROP TABLE IF EXISTS dim_tiempo_regalias;
CREATE TABLE dim_tiempo_regalias (
    id_fecha INT PRIMARY KEY,
    anio INT,
    mes INT,
    trimestre INT,
    fecha_completa DATE
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- 🔹 TABLAS DE HECHOS
-- =====================================================

-- ========================
-- fact_actividades_regalias
-- ========================
DROP TABLE IF EXISTS fact_actividades_regalias;
CREATE TABLE fact_actividades_regalias (
    id_fact INT AUTO_INCREMENT PRIMARY KEY,
    id_proyecto VARCHAR(20),
    id_actividad INT,
    total_ejecutado DECIMAL(15,2),
    tipo_actividad VARCHAR(100),
    actor VARCHAR(255),
    beneficiarios TEXT,
    dotacion VARCHAR(100),
    descripcion_dotacion TEXT,
    evidencia_URL TEXT,
    id_fecha INT,
    FOREIGN KEY (id_proyecto) REFERENCES dim_proyecto_regalias(id_proyecto),
    FOREIGN KEY (id_fecha) REFERENCES dim_tiempo_regalias(id_fecha)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;

-- ========================
-- fact_proyecto_meta_regalias
-- ========================
DROP TABLE IF EXISTS fact_proyecto_meta_regalias;
CREATE TABLE fact_proyecto_meta_regalias (
    id_fact INT AUTO_INCREMENT PRIMARY KEY,
    id_proyecto VARCHAR(20),
    id_meta INT,
    id_fecha INT,
    FOREIGN KEY (id_proyecto) REFERENCES dim_proyecto_regalias(id_proyecto),
    FOREIGN KEY (id_meta) REFERENCES dim_meta_regalias(id_meta),
    FOREIGN KEY (id_fecha) REFERENCES dim_tiempo_regalias(id_fecha)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;

-- ========================
-- fact_proyecto_institucion_regalias
-- ========================
DROP TABLE IF EXISTS fact_proyecto_institucion_regalias;
CREATE TABLE fact_proyecto_institucion_regalias (
    id_fact INT AUTO_INCREMENT PRIMARY KEY,
    id_proyecto VARCHAR(20) NOT NULL,
    id_institucion VARCHAR(50) NOT NULL,
    id_municipio INT NULL,
    hoja_origen VARCHAR(100) NULL,
    id_fecha INT NULL,
    FOREIGN KEY (id_proyecto) REFERENCES dim_proyecto_regalias(id_proyecto),
    FOREIGN KEY (id_institucion) REFERENCES dim_institucion_regalias(id_institucion),
    FOREIGN KEY (id_municipio) REFERENCES dim_municipio_regalias(id_municipio),
    FOREIGN KEY (id_fecha) REFERENCES dim_tiempo_regalias(id_fecha)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;

-- ========================
-- fact_proyecto_beneficiario_regalias
-- ========================
DROP TABLE IF EXISTS fact_proyecto_beneficiario_regalias;
CREATE TABLE fact_proyecto_beneficiario_regalias (
    id_fact INT AUTO_INCREMENT PRIMARY KEY,
    id_proyecto VARCHAR(20),
    id_institucion VARCHAR(50),
    directivos_benef INT,
    administrativos_benef INT,
    docentes_benef INT,
    estudiantes_benef INT,
    asistencia_tecnica VARCHAR(50),
    modalidad_asistencia VARCHAR(255),
    recibio_dotacion VARCHAR(50),
    dotacion_recibida TEXT,
    acudientes_beneficiados INT,
    id_fecha INT,
    FOREIGN KEY (id_proyecto) REFERENCES dim_proyecto_regalias(id_proyecto),
    FOREIGN KEY (id_institucion) REFERENCES dim_institucion_regalias(id_institucion),
    FOREIGN KEY (id_fecha) REFERENCES dim_tiempo_regalias(id_fecha)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- 🔍 VALIDACIONES BÁSICAS DE REFERENCIA
-- =====================================================
-- select * from stg_fuente_regalias;
-- select * from stg_proyectos_regalias;
-- select * from stg_actividades_regalias;
-- select * from stg_beneficiarios_regalias;
-- select * from stg_metas_regalias;
