USE sised;



CREATE TABLE dim_fuente_poai_2025 (
    id_fuente INT AUTO_INCREMENT PRIMARY KEY,
    nombre_fuente VARCHAR(255),
    tipo_fuente VARCHAR(100),
    fuente VARCHAR(100),
    anio VARCHAR(4) DEFAULT '2025'
) ENGINE=InnoDB;




CREATE TABLE dim_proyecto_poai_2025 (
    id_proyecto VARCHAR(20) PRIMARY KEY,
    codigo_bpin VARCHAR(20),
    nombre_proyecto VARCHAR(255),
    responsable VARCHAR(255),
    enlace_tecnico VARCHAR(255),
    sector VARCHAR(100),
    apropiacion_pptal DECIMAL(15,2),
    adicion_pptal DECIMAL(15,2),
    total_ejecutado DECIMAL(15,2),
    documentos_proyecto TEXT,
    avance_avance DECIMAL(5,2),
    hoja_proyectos VARCHAR(100),
    hoja_fuentes VARCHAR(100)
) ENGINE=InnoDB;




CREATE TABLE dim_actividad_poai_2025 (
    id_actividad INT AUTO_INCREMENT PRIMARY KEY,
    consecutivo INT NOT NULL,
    nombre_actividad TEXT NOT NULL,
    hoja_proyectos VARCHAR(100)
) ENGINE=InnoDB
AUTO_INCREMENT=100
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;




CREATE TABLE dim_municipio_poai_2025 (
    id_municipio INT AUTO_INCREMENT PRIMARY KEY,
    nombre_municipio VARCHAR(255),
    departamento VARCHAR(255),
    region VARCHAR(255)
) ENGINE=InnoDB;




CREATE TABLE dim_institucion_poai_2025 (
    id_institucion VARCHAR(50) PRIMARY KEY,
    nombre_ieo VARCHAR(255),
    codigo_dane VARCHAR(50),
    tipo VARCHAR(50) DEFAULT 'IEO',
    id_municipio INT,
    FOREIGN KEY (id_municipio) REFERENCES dim_municipio_poai_2025(id_municipio)
) ENGINE=InnoDB;




CREATE TABLE dim_meta_poai_2025 (
    id_meta INT PRIMARY KEY,
    descripcion_meta VARCHAR(500),
    unidad VARCHAR(100),
    valor_programado DECIMAL(15,2),
    valor_logrado DECIMAL(15,2),
    hoja_proyectos VARCHAR(100)
) ENGINE=InnoDB;




CREATE TABLE dim_tiempo_poai_2025 (
    id_fecha INT PRIMARY KEY,
    anio INT,
    mes INT,
    trimestre INT,
    fecha_completa DATE
) ENGINE=InnoDB;




CREATE TABLE fact_actividades_poai_2025 (
    id_fact INT AUTO_INCREMENT PRIMARY KEY,
    id_proyecto VARCHAR(20),
    id_actividad int,
    total_ejecutado DECIMAL(15,2),
    tipo_actividad VARCHAR(100),
    actor VARCHAR(255),
    beneficiarios TEXT,
    dotacion VARCHAR(100),
    descripcion_dotacion TEXT,
    evidencia_URL TEXT,
    id_fecha INT,
    FOREIGN KEY (id_proyecto) REFERENCES dim_proyecto_poai_2025(id_proyecto),
    FOREIGN KEY (id_fecha) REFERENCES dim_tiempo_poai_2025(id_fecha)
) ENGINE=InnoDB;



CREATE TABLE fact_proyecto_meta_poai_2025 (
    id_fact INT AUTO_INCREMENT PRIMARY KEY,
    id_proyecto VARCHAR(20),
    id_meta INT,
    id_fecha INT,
    FOREIGN KEY (id_proyecto) REFERENCES dim_proyecto_poai_2025(id_proyecto),
    FOREIGN KEY (id_meta) REFERENCES dim_meta_poai_2025(id_meta),
    FOREIGN KEY (id_fecha) REFERENCES dim_tiempo_poai_2025(id_fecha)
) ENGINE=InnoDB;




CREATE TABLE fact_proyecto_institucion_poai_2025 (
    id_fact INT AUTO_INCREMENT PRIMARY KEY,
    id_proyecto VARCHAR(20) NOT NULL,
    id_institucion VARCHAR(50) NOT NULL,
    id_municipio INT NULL,
    hoja_origen VARCHAR(100) NULL,
    id_fecha INT NULL,
    FOREIGN KEY (id_proyecto) REFERENCES dim_proyecto_poai_2025(id_proyecto),
    FOREIGN KEY (id_institucion) REFERENCES dim_institucion_poai_2025(id_institucion),
    FOREIGN KEY (id_municipio) REFERENCES dim_municipio_poai_2025(id_municipio),
    FOREIGN KEY (id_fecha) REFERENCES dim_tiempo_poai_2025(id_fecha)
) ENGINE=InnoDB;




CREATE TABLE fact_proyecto_beneficiario_poai_2025 (
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
    id_fecha INT,
    FOREIGN KEY (id_proyecto) REFERENCES dim_proyecto_poai_2025(id_proyecto),
    FOREIGN KEY (id_institucion) REFERENCES dim_institucion_poai_2025(id_institucion),
    FOREIGN KEY (id_fecha) REFERENCES dim_tiempo_poai_2025(id_fecha)
) ENGINE=InnoDB;

