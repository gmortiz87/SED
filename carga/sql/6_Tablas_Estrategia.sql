USE sised;



DROP TABLE IF EXISTS dim_fuente_estrategias;
CREATE TABLE dim_fuente_estrategias (
    id_fuente INT AUTO_INCREMENT PRIMARY KEY,
    nombre_fuente VARCHAR(255) UNIQUE,
    fuente VARCHAR(100),
    anio VARCHAR(4) DEFAULT '2025'
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;




CREATE TABLE dim_proyecto_estrategias (
    id_proyecto INT PRIMARY KEY,
    nombre_proyecto VARCHAR(255),
    entidad_aliada VARCHAR(255),
    responsable VARCHAR(255),
    enlace_tecnico VARCHAR(255),
    documentos_proyecto TEXT,
    avance DECIMAL(5,2),
    hoja_proyectos VARCHAR(100),
    hoja_fuentes VARCHAR(100)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;



CREATE TABLE dim_actividad_estrategias (
    consecutivo INT NOT NULL,
    nombre_actividad TEXT NOT NULL,
    hoja_proyectos VARCHAR(100),
    id_actividad INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (id_actividad)
) ENGINE=InnoDB
AUTO_INCREMENT=100
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;



CREATE TABLE dim_municipio_estrategias (
    id_municipio INT AUTO_INCREMENT PRIMARY KEY,
    nombre_municipio VARCHAR(255),
    departamento VARCHAR(255),
    region VARCHAR(255)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;




CREATE TABLE dim_institucion_estrategias (
    id_institucion VARCHAR(50) PRIMARY KEY,  
    nombre_ieo VARCHAR(255),
    codigo_dane VARCHAR(50),
    tipo VARCHAR(50) DEFAULT 'IEO',
    id_municipio INT,
    FOREIGN KEY (id_municipio) REFERENCES dim_municipio_estrategias(id_municipio)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;



CREATE TABLE dim_tiempo_estrategias (
    id_fecha INT PRIMARY KEY,
    anio INT,
    mes INT,
    trimestre INT,
    fecha_completa DATE
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;



CREATE TABLE fact_actividades_estrategias (
    id_fact INT AUTO_INCREMENT PRIMARY KEY,
    id_proyecto INT,
    id_actividad INT,
    actor VARCHAR(255),
    beneficiarios TEXT,
    dotacion VARCHAR(100),
    descripcion_dotacion TEXT,
    evidencia_URL TEXT,
    hoja VARCHAR(250),
    id_fecha INT,
    FOREIGN KEY (id_proyecto) REFERENCES dim_proyecto_estrategias(id_proyecto),
    FOREIGN KEY (id_actividad) REFERENCES dim_actividad_estrategias(id_actividad),
    FOREIGN KEY (id_fecha) REFERENCES dim_tiempo_estrategias(id_fecha)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;



CREATE TABLE fact_proyecto_institucion_estrategias (
    id_fact INT AUTO_INCREMENT PRIMARY KEY,
    id_proyecto INT NOT NULL,
    id_institucion VARCHAR(50) NOT NULL,
    id_municipio INT NULL,
    hoja_origen VARCHAR(100) NULL,
    hoja_proyecto VARCHAR(100) NULL,
    id_fecha INT NULL,
    FOREIGN KEY (id_proyecto) REFERENCES dim_proyecto_estrategias(id_proyecto),
    FOREIGN KEY (id_institucion) REFERENCES dim_institucion_estrategias(id_institucion),
    FOREIGN KEY (id_municipio) REFERENCES dim_municipio_estrategias(id_municipio),
    FOREIGN KEY (id_fecha) REFERENCES dim_tiempo_estrategias(id_fecha)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;




CREATE TABLE fact_proyecto_beneficiario_estrategias (
    id_fact INT AUTO_INCREMENT PRIMARY KEY,
    id_proyecto INT,
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
    FOREIGN KEY (id_proyecto) REFERENCES dim_proyecto_estrategias(id_proyecto),
    FOREIGN KEY (id_institucion) REFERENCES dim_institucion_estrategias(id_institucion),
    FOREIGN KEY (id_fecha) REFERENCES dim_tiempo_estrategias(id_fecha)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;





