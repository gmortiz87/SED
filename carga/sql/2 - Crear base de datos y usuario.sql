-- ================================================
-- ⚙️ CONFIGURACIÓN INICIAL DE BASE DE DATOS SISED
-- ================================================

-- Crear base de datos principal
CREATE DATABASE IF NOT EXISTS sised
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- Crear usuario de aplicación (ajusta la contraseña)
CREATE USER IF NOT EXISTS 'sised_user'@'localhost' IDENTIFIED BY 'L@Upadaka3009';

-- Otorgar permisos completos sobre la base
GRANT ALL PRIVILEGES ON sised.* TO 'sised_user'@'localhost';

-- Aplicar cambios
FLUSH PRIVILEGES;

-- Confirmar acceso y base actual
USE sised;
SHOW DATABASES;


