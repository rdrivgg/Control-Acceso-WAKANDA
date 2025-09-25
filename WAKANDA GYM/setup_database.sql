-- Script de configuración inicial para WAKANDA GYM
-- Ejecutar como usuario root después de instalar MySQL

-- Crear base de datos
CREATE DATABASE IF NOT EXISTS wakanda_gym CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Crear usuario dedicado para la aplicación
CREATE USER IF NOT EXISTS 'gym_admin'@'%' IDENTIFIED BY 'gym123456';
CREATE USER IF NOT EXISTS 'gym_admin'@'localhost' IDENTIFIED BY 'gym123456';

-- Otorgar permisos completos sobre la base de datos
GRANT ALL PRIVILEGES ON wakanda_gym.* TO 'gym_admin'@'%';
GRANT ALL PRIVILEGES ON wakanda_gym.* TO 'gym_admin'@'localhost';

-- Aplicar cambios
FLUSH PRIVILEGES;

-- Verificar creación
USE wakanda_gym;
SHOW TABLES;

-- Mostrar usuarios creados
SELECT User, Host FROM mysql.user WHERE User = 'gym_admin';

-- Mostrar permisos
SHOW GRANTS FOR 'gym_admin'@'localhost';