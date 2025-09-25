import mysql.connector
from mysql.connector import pooling, Error
from datetime import datetime, date
import os
from config import db_config

class GymDatabase:
    def __init__(self):
        self.config = db_config.get_pool_params()
        self.connection_pool = None
        self.init_connection_pool()
        self.init_database()
    
    def init_connection_pool(self):
        """Inicializa el pool de conexiones MySQL"""
        try:
            self.connection_pool = pooling.MySQLConnectionPool(
                pool_name="gym_pool",
                **self.config
            )
        except Error as e:
            print(f"Error creando pool de conexiones: {e}")
            raise
    
    def get_connection(self):
        """Obtiene una conexión del pool"""
        try:
            return self.connection_pool.get_connection()
        except Error as e:
            print(f"Error obteniendo conexión: {e}")
            raise
    
    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    codigo_barras VARCHAR(50) UNIQUE NOT NULL,
                    nombre VARCHAR(100) NOT NULL,
                    apellido VARCHAR(100) NOT NULL,
                    telefono VARCHAR(20),
                    email VARCHAR(150),
                    estado_pago ENUM('pendiente', 'pagado') DEFAULT 'pendiente',
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    activo BOOLEAN DEFAULT TRUE
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS accesos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    usuario_id INT,
                    tipo ENUM('entrada', 'salida') NOT NULL,
                    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS configuracion (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    clave VARCHAR(100) UNIQUE NOT NULL,
                    valor TEXT NOT NULL
                )
            ''')
            
            cursor.execute('''
                INSERT IGNORE INTO configuracion (clave, valor) 
                VALUES 
                ('admin_phone', '+1234567890'),
                ('sms_enabled', 'false')
            ''')
            
            conn.commit()
        except Error as e:
            print(f"Error inicializando base de datos: {e}")
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()
    
    def agregar_usuario(self, codigo_barras, nombre, apellido, telefono=None, email=None, estado_pago='pendiente'):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO usuarios (codigo_barras, nombre, apellido, telefono, email, estado_pago)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (codigo_barras, nombre, apellido, telefono, email, estado_pago))
            
            conn.commit()
            return cursor.lastrowid
        except mysql.connector.IntegrityError:
            return None
        except Error as e:
            print(f"Error agregando usuario: {e}")
            conn.rollback()
            return None
        finally:
            cursor.close()
            conn.close()
    
    def obtener_usuario_por_barcode(self, codigo_barras):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT * FROM usuarios WHERE codigo_barras = %s AND activo = TRUE
            ''', (codigo_barras,))
            
            usuario = cursor.fetchone()
            return usuario
        except Error as e:
            print(f"Error obteniendo usuario: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    
    def actualizar_estado_pago(self, usuario_id, estado_pago):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE usuarios SET estado_pago = %s WHERE id = %s
            ''', (estado_pago, usuario_id))
            
            conn.commit()
        except Error as e:
            print(f"Error actualizando estado de pago: {e}")
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()
    
    def registrar_acceso(self, usuario_id, tipo):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO accesos (usuario_id, tipo) VALUES (%s, %s)
            ''', (usuario_id, tipo))
            
            conn.commit()
        except Error as e:
            print(f"Error registrando acceso: {e}")
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()
    
    def obtener_accesos_hoy(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            hoy = date.today().strftime('%Y-%m-%d')
            
            cursor.execute('''
                SELECT u.nombre, u.apellido, a.tipo, a.fecha_hora 
                FROM accesos a 
                JOIN usuarios u ON a.usuario_id = u.id 
                WHERE DATE(a.fecha_hora) = %s
                ORDER BY a.fecha_hora DESC
            ''', (hoy,))
            
            accesos = cursor.fetchall()
            return accesos
        except Error as e:
            print(f"Error obteniendo accesos de hoy: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    
    def obtener_todos_usuarios(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT id, codigo_barras, nombre, apellido, telefono, email, estado_pago, fecha_registro
                FROM usuarios WHERE activo = TRUE ORDER BY nombre, apellido
            ''')
            
            usuarios = cursor.fetchall()
            return usuarios
        except Error as e:
            print(f"Error obteniendo usuarios: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    
    def obtener_configuracion(self, clave):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT valor FROM configuracion WHERE clave = %s', (clave,))
            resultado = cursor.fetchone()
            
            return resultado[0] if resultado else None
        except Error as e:
            print(f"Error obteniendo configuración: {e}")
            return None
        finally:
            cursor.close()
            conn.close()