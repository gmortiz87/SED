-- ============================================================
-- 🧠 SCRIPT MAESTRO: MODELOS DIMENSIONALES - SISGED / SISED
-- ============================================================
-- Este script crea y carga los modelos dimensionales de:
--   1️⃣ POAI_2024
--   2️⃣ POAI_2025
--   3️⃣ ESTRATEGIAS
--   4️⃣ REGALÍAS
-- Incluye DROP controlado, creación de tablas y carga desde staging.
-- ============================================================

USE sised;

-- ============================================================
-- 🔹 BLOQUE 1: POAI_2024
-- ============================================================
SOURCE 'C:/Users/Adminstrador/Documents/3 - Ave Fenix/Propuesta/SED/carga/sql/4 - Tablas modelo dimensional POAI_2024.sql';
SOURCE 'C:/Users/Adminstrador/Documents/3 - Ave Fenix/Propuesta/SED/carga/sql/4 - Insert Select POAI_2024.sql';

-- ============================================================
-- 🔹 BLOQUE 2: POAI_2025
-- ============================================================
SOURCE 'C:/Users/Adminstrador/Documents/3 - Ave Fenix/Propuesta/SED/carga/sql/5 - Tablas modelo dimensional POAI_2025.sql';
SOURCE 'C:/Users/Adminstrador/Documents/3 - Ave Fenix/Propuesta/SED/carga/sql/5 - Insert Select POAI_2025.sql';

-- ============================================================
-- 🔹 BLOQUE 3: ESTRATEGIAS
-- ============================================================
SOURCE 'C:/Users/Adminstrador/Documents/3 - Ave Fenix/Propuesta/SED/carga/sql/6 - Tablas modelo dimensional Estrategia.sql';
SOURCE 'C:/Users/Adminstrador/Documents/3 - Ave Fenix/Propuesta/SED/carga/sql/6 - Insert Select Estrategia.sql';

-- ============================================================
-- 🔹 BLOQUE 4: REGALÍAS
-- ============================================================
SOURCE 'C:/Users/Adminstrador/Documents/3 - Ave Fenix/Propuesta/SED/carga/sql/3 - Tablas modelo dimensional Regalias.sql';
SOURCE 'C:/Users/Adminstrador/Documents/3 - Ave Fenix/Propuesta/SED/carga/sql/3 - Insert Select Regalias.sql';

-- ============================================================
-- ✅ VERIFICACIÓN FINAL DE TODAS LAS TABLAS
-- ============================================================
SHOW TABLES LIKE '%poai_2024%';
SHOW TABLES LIKE '%poai_2025%';
SHOW TABLES LIKE '%estrategias%';
SHOW TABLES LIKE '%regalias%';

-- Fin del script maestro.
