#!/usr/bin/env python3
"""
Script para probar la conexión a MySQL
"""

try:
    from database import GymDatabase
    print("Probando conexion a MySQL...")
    
    db = GymDatabase()
    print("Conexion exitosa!")
    print("Base de datos configurada correctamente")
    
    # Probar algunas operaciones basicas
    usuarios = db.obtener_todos_usuarios()
    print(f"Usuarios registrados: {len(usuarios)}")
    
    print("\nSISTEMA LISTO PARA USAR!")
    print("Ejecuta: python main.py")
    
except Exception as e:
    print(f"Error de conexion: {e}")
    print("\nPosibles soluciones:")
    print("1. Verificar que MySQL este ejecutandose")
    print("2. Verificar credenciales en archivo .env")
    print("3. Verificar que el usuario gym_admin existe")