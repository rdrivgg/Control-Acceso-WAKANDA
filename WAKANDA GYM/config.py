import os
from typing import Dict, Any
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class DatabaseConfig:
    """
    Configuración de base de datos para WAKANDA GYM
    Soporta tanto desarrollo local como producción con MySQL
    """
    
    def __init__(self):
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Carga configuración desde variables de entorno o valores por defecto"""
        return {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 3306)),
            'database': os.getenv('DB_NAME', 'wakanda_gym'),
            'user': os.getenv('DB_USER', 'gym_admin'),
            'password': os.getenv('DB_PASSWORD', 'gym123456'),
            'charset': 'utf8mb4',
            'autocommit': True,
            'pool_size': 10,
            'pool_reset_session': True
        }
    
    def get_connection_params(self) -> Dict[str, Any]:
        """Retorna parámetros de conexión para MySQL"""
        return {
            'host': self.config['host'],
            'port': self.config['port'],
            'database': self.config['database'],
            'user': self.config['user'],
            'password': self.config['password'],
            'charset': self.config['charset'],
            'autocommit': self.config['autocommit']
        }
    
    def get_pool_params(self) -> Dict[str, Any]:
        """Retorna parámetros para pool de conexiones"""
        params = self.get_connection_params()
        params.update({
            'pool_size': self.config['pool_size'],
            'pool_reset_session': self.config['pool_reset_session']
        })
        return params

# Configuración global
db_config = DatabaseConfig()