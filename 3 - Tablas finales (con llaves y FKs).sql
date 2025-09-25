USE sised;

-- ==========================
-- 3.1 Fuente (única por proyecto)
-- ==========================
CREATE TABLE IF NOT EXISTS fact_fuente_estrategias (
  ID_Fuente INT PRIMARY KEY AUTO_INCREMENT,
  Nombre_Proyecto VARCHAR(255) NOT NULL,
  Vigencia VARCHAR(10),
  Entidad_Aliada VARCHAR(255),
  Responsable_SED VARCHAR(255),
  Enlace_Tecnico_SED VARCHAR(255),
  Info_Estrategia TEXT,
  UNIQUE KEY uk_fuente_nombre (Nombre_Proyecto)
) ENGINE=InnoDB;

-- ==========================
-- 3.2 Proyectos
-- ==========================
CREATE TABLE IF NOT EXISTS fact_proyectos_estrategias (
  ID_Proyecto INT PRIMARY KEY AUTO_INCREMENT,
  ID_Fuente INT NOT NULL,
  Nombre_Proyecto VARCHAR(255) NOT NULL,
  Hoja VARCHAR(100),
  FOREIGN KEY (ID_Fuente) REFERENCES fact_fuente_estrategias(ID_Fuente),
  INDEX ix_proy_hoja (Hoja),
  UNIQUE KEY uk_proy_nombre (Nombre_Proyecto)
) ENGINE=InnoDB;

-- ==========================
-- 3.3 Actividades
-- (si no hay ID natural de actividad, creamos surrogate + una regla de unicidad razonable)
-- ==========================
CREATE TABLE IF NOT EXISTS fact_actividades_estrategias (
  ID_Actividad INT PRIMARY KEY AUTO_INCREMENT,
  ID_Proyecto INT NOT NULL,
  Actividad VARCHAR(255),
  Total_Ejecutado DECIMAL(18,2),
  Componente_PAM VARCHAR(255),
  Actor_Dirigido VARCHAR(255),
  Numero_Beneficiarios INT,
  Hoja VARCHAR(100),
  FOREIGN KEY (ID_Proyecto) REFERENCES fact_proyectos_estrategias(ID_Proyecto),
  INDEX ix_act_hoja (Hoja)
) ENGINE=InnoDB;

-- ==========================
-- 3.4 Beneficiarios
-- (único por proyecto + IEO; ajusta la unicidad a tu realidad)
-- ==========================
CREATE TABLE IF NOT EXISTS fact_beneficiarios_estrategias (
  ID_Beneficiario INT PRIMARY KEY AUTO_INCREMENT,
  ID_Proyecto INT NOT NULL,
  DANE_IEO VARCHAR(50),
  Municipio VARCHAR(255),
  Nombre_IEO VARCHAR(255),
  Directivos_Beneficiados INT,
  Docentes_Beneficiados INT,
  Estudiantes_Beneficiados INT,
  Administrativos_Beneficiados INT,
  Recibio_Asistencia TINYINT(1),
  Recibio_Dotacion TINYINT(1),
  Hoja VARCHAR(100),
  FOREIGN KEY (ID_Proyecto) REFERENCES fact_proyectos_estrategias(ID_Proyecto),
  INDEX ix_ben_hoja (Hoja)
) ENGINE=InnoDB;

-- ==========================
-- 3.5 Puente Actividad–Beneficiario (N:N)
-- Relacionamos por HOJA si ese es tu punto común (ojo con "explosión combinatoria").
-- ==========================
CREATE TABLE IF NOT EXISTS fact_beneficiarios_actividades (
  ID_Relacion INT PRIMARY KEY AUTO_INCREMENT,
  ID_Actividad INT NOT NULL,
  ID_Beneficiario INT NOT NULL,
  Numero_Beneficiarios INT,
  FOREIGN KEY (ID_Actividad) REFERENCES fact_actividades_estrategias(ID_Actividad),
  FOREIGN KEY (ID_Beneficiario) REFERENCES fact_beneficiarios_estrategias(ID_Beneficiario),
  UNIQUE KEY uk_rel (ID_Actividad, ID_Beneficiario)
) ENGINE=InnoDB;
