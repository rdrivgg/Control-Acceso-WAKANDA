@echo off
echo ========================================
echo    CONFIGURACION MYSQL - WAKANDA GYM
echo ========================================
echo.

echo 1. Conectando a MySQL como root...
echo    (Ingresa la contraseña de root que configuraste)
echo.

mysql -u root -p < setup_database.sql

echo.
echo 2. Verificando configuracion...
mysql -u gym_admin -pgym123456 -D wakanda_gym -e "SELECT 'Conexion exitosa como gym_admin' as Estado;"

if %ERRORLEVEL% == 0 (
    echo.
    echo ✅ CONFIGURACION COMPLETADA EXITOSAMENTE
    echo    Base de datos: wakanda_gym
    echo    Usuario: gym_admin
    echo    Password: gym123456
    echo.
    echo 🚀 Ahora puedes ejecutar: python main.py
) else (
    echo.
    echo ❌ ERROR EN LA CONFIGURACION
    echo    Verifica que MySQL este ejecutandose
    echo    y que la contraseña de root sea correcta
)

echo.
pause