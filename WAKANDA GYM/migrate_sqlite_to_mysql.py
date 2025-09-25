#!/usr/bin/env python3
"""
Script de migración de SQLite a MySQL para WAKANDA GYM
Migra todos los datos existentes del archivo gym_control.db a MySQL
"""

import sqlite3
import mysql.connector
from mysql.connector import Error
import os
from config import db_config

class SQLiteToMySQLMigrator:
    def __init__(self):
        self.sqlite_file = 'gym_control.db'
        self.mysql_config = db_config.get_connection_params()
    
    def migrate(self):
        """Ejecuta la migración completa"""
        print("🔄 Iniciando migración de SQLite a MySQL...")
        
        if not os.path.exists(self.sqlite_file):
            print("❌ No se encontró el archivo gym_control.db")
            return False
        
        try:
            # Conectar a SQLite
            sqlite_conn = sqlite3.connect(self.sqlite_file)
            sqlite_cursor = sqlite_conn.cursor()
            
            # Conectar a MySQL
            mysql_conn = mysql.connector.connect(**self.mysql_config)
            mysql_cursor = mysql_conn.cursor()
            
            # Migrar usuarios
            self.migrate_usuarios(sqlite_cursor, mysql_cursor, mysql_conn)
            
            # Migrar accesos
            self.migrate_accesos(sqlite_cursor, mysql_cursor, mysql_conn)
            
            # Migrar configuración
            self.migrate_configuracion(sqlite_cursor, mysql_cursor, mysql_conn)
            
            print("✅ Migración completada exitosamente")
            
            # Crear backup del archivo SQLite
            backup_name = f"gym_control_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            os.rename(self.sqlite_file, backup_name)
            print(f"📦 Archivo SQLite renombrado a: {backup_name}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error durante la migración: {e}")
            return False
        finally:
            if 'sqlite_conn' in locals():
                sqlite_conn.close()
            if 'mysql_conn' in locals():
                mysql_conn.close()
    
    def migrate_usuarios(self, sqlite_cursor, mysql_cursor, mysql_conn):
        """Migra la tabla usuarios"""
        print("👥 Migrando usuarios...")
        
        sqlite_cursor.execute("SELECT * FROM usuarios")
        usuarios = sqlite_cursor.fetchall()
        
        for usuario in usuarios:
            try:
                mysql_cursor.execute('''
                    INSERT IGNORE INTO usuarios 
                    (id, codigo_barras, nombre, apellido, telefono, email, estado_pago, fecha_registro, activo)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', usuario)
            except Error as e:
                print(f"⚠️  Error migrando usuario {usuario[1]}: {e}")
        
        mysql_conn.commit()
        print(f"   ✓ {len(usuarios)} usuarios migrados")
    
    def migrate_accesos(self, sqlite_cursor, mysql_cursor, mysql_conn):
        """Migra la tabla accesos"""
        print("🚪 Migrando accesos...")
        
        sqlite_cursor.execute("SELECT * FROM accesos")
        accesos = sqlite_cursor.fetchall()
        
        for acceso in accesos:
            try:
                mysql_cursor.execute('''
                    INSERT IGNORE INTO accesos 
                    (id, usuario_id, tipo, fecha_hora)
                    VALUES (%s, %s, %s, %s)
                ''', acceso)
            except Error as e:
                print(f"⚠️  Error migrando acceso {acceso[0]}: {e}")
        
        mysql_conn.commit()
        print(f"   ✓ {len(accesos)} accesos migrados")
    
    def migrate_configuracion(self, sqlite_cursor, mysql_cursor, mysql_conn):
        """Migra la tabla configuración"""
        print("⚙️  Migrando configuración...")
        
        try:
            sqlite_cursor.execute("SELECT * FROM configuracion")
            configuraciones = sqlite_cursor.fetchall()
            
            for config in configuraciones:
                try:
                    mysql_cursor.execute('''
                        INSERT INTO configuracion (clave, valor)
                        VALUES (%s, %s)
                        ON DUPLICATE KEY UPDATE valor = VALUES(valor)
                    ''', (config[1], config[2]))  # Omitir ID auto-increment
                except Error as e:
                    print(f"⚠️  Error migrando configuración {config[1]}: {e}")
            
            mysql_conn.commit()
            print(f"   ✓ {len(configuraciones)} configuraciones migradas")
            
        except sqlite3.OperationalError:
            print("   ⚠️  Tabla configuración no existe en SQLite, creando valores por defecto")

if __name__ == "__main__":
    from datetime import datetime
    
    migrator = SQLiteToMySQLMigrator()
    success = migrator.migrate()
    
    if success:
        print("\n🎉 ¡Migración completada! El sistema ahora usa MySQL.")
        print("💡 Recuerda configurar tu archivo .env con los datos de conexión.")
    else:
        print("\n❌ La migración falló. Revisa los errores arriba.")