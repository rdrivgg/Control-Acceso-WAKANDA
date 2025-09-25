@echo off
cd /d "C:\Users\Informatica Larnet\Desktop\WAKANDA GYM"

echo ========================================
echo    CONFIGURANDO MYSQL - WAKANDA GYM
echo ========================================
echo.

echo Ejecutando configuracion...
echo adminwakanda | "C:\Program Files\MySQL\MySQL Server 9.4\bin\mysql.exe" -u root -p < setup_quick.sql

echo.
echo Verificando conexion como gym_admin...
echo gym123456 | "C:\Program Files\MySQL\MySQL Server 9.4\bin\mysql.exe" -u gym_admin -p -D wakanda_gym -e "SELECT 'Conexion exitosa' as Estado;"

echo.
echo ✅ CONFIGURACION COMPLETADA
pause