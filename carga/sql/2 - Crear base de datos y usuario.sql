-- Crea BD y usuario (ajusta nombre y contraseña)
CREATE DATABASE IF NOT EXISTS sised
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'sised_user'@'%' IDENTIFIED BY 'TuPasswordFuerte';
GRANT ALL PRIVILEGES ON sised.* TO 'sised_user'@'%';
FLUSH PRIVILEGES;

DROP DATABASE SISED;