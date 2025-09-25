-- Configuración rápida para WAKANDA GYM
CREATE DATABASE IF NOT EXISTS wakanda_gym CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'gym_admin'@'%' IDENTIFIED BY 'gym123456';
CREATE USER IF NOT EXISTS 'gym_admin'@'localhost' IDENTIFIED BY 'gym123456';
GRANT ALL PRIVILEGES ON wakanda_gym.* TO 'gym_admin'@'%';
GRANT ALL PRIVILEGES ON wakanda_gym.* TO 'gym_admin'@'localhost';
FLUSH PRIVILEGES;
USE wakanda_gym;
SELECT 'Base de datos wakanda_gym configurada exitosamente' as Estado;