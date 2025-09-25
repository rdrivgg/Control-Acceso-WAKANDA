# Configuración MySQL para WAKANDA GYM

## Instalación de MySQL

### Windows
1. Descargar MySQL Server desde: https://dev.mysql.com/downloads/mysql/
2. Instalar MySQL Server con configuración por defecto
3. Durante la instalación, crear usuario root con contraseña segura

### Ubuntu/Debian
```bash
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
```

### CentOS/RHEL
```bash
sudo yum install mysql-server
sudo systemctl start mysqld
sudo mysql_secure_installation
```

## Configuración de Base de Datos

### 1. Conectar a MySQL como root
```bash
mysql -u root -p
```

### 2. Crear base de datos y usuario
```sql
-- Crear base de datos
CREATE DATABASE wakanda_gym CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Crear usuario dedicado
CREATE USER 'gym_admin'@'%' IDENTIFIED BY 'gym123456';

-- Otorgar permisos
GRANT ALL PRIVILEGES ON wakanda_gym.* TO 'gym_admin'@'%';
FLUSH PRIVILEGES;

-- Verificar usuario
SELECT User, Host FROM mysql.user WHERE User = 'gym_admin';
```

### 3. Configurar acceso remoto (para múltiples equipos)

#### Editar archivo de configuración MySQL:
**Windows**: `C:\ProgramData\MySQL\MySQL Server 8.0\my.ini`
**Linux**: `/etc/mysql/mysql.conf.d/mysqld.cnf` o `/etc/my.cnf`

Agregar o modificar:
```ini
[mysqld]
bind-address = 0.0.0.0
port = 3306
max_connections = 100
```

#### Reiniciar servicio MySQL:
**Windows**:
```cmd
net stop mysql80
net start mysql80
```

**Linux**:
```bash
sudo systemctl restart mysql
```

### 4. Configurar Firewall (si es necesario)
**Windows Firewall**:
- Abrir puerto 3306 TCP

**Linux (UFW)**:
```bash
sudo ufw allow 3306/tcp
```

## Variables de Entorno

Crear archivo `.env` en cada equipo con las configuraciones:

### Equipo Servidor (donde está MySQL):
```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=wakanda_gym
DB_USER=gym_admin
DB_PASSWORD=gym123456
```

### Equipos Cliente (Control de Acceso):
```env
DB_HOST=192.168.1.100  # IP del servidor MySQL
DB_PORT=3306
DB_NAME=wakanda_gym
DB_USER=gym_admin
DB_PASSWORD=gym123456
```

## Instalación de Dependencias Python

```bash
pip install -r requirements.txt
```

## Configuración de Red

### Obtener IP del servidor MySQL:
**Windows**:
```cmd
ipconfig
```

**Linux**:
```bash
ip addr show
# o
hostname -I
```

### Verificar conectividad desde cliente:
```bash
# Ping básico
ping 192.168.1.100

# Verificar puerto MySQL
telnet 192.168.1.100 3306
```

## Estructura de Equipos Recomendada

```
┌─────────────────────┐    ┌─────────────────────┐
│   EQUIPO SERVIDOR   │    │  EQUIPO CONTROL     │
│                     │    │     ACCESO          │
│ - MySQL Server      │◄───┤                     │
│ - Aplicación Admin  │    │ - Solo Control      │
│ - IP: 192.168.1.100 │    │ - IP: 192.168.1.101 │
└─────────────────────┘    └─────────────────────┘
```

## Separación de Aplicaciones

### Para el Servidor (Administración):
Ejecutar `main.py` completo con ventana de administración.

### Para Control de Acceso:
Crear `control_acceso.py` con solo la funcionalidad de escaneo:
```python
# Solo mantener la clase GymAccessControl
# Eliminar AdminWindow del código
```

## Solución de Problemas Comunes

### Error de Conexión:
1. Verificar que MySQL esté ejecutándose
2. Comprobar configuración de firewall
3. Verificar usuario y permisos
4. Confirmar IP y puerto correctos

### Error de Permisos:
```sql
GRANT ALL PRIVILEGES ON wakanda_gym.* TO 'gym_admin'@'%';
FLUSH PRIVILEGES;
```

### Error de Charset:
```sql
ALTER DATABASE wakanda_gym CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## Comandos Útiles

### Verificar conexiones activas:
```sql
SHOW PROCESSLIST;
```

### Verificar estado de la base de datos:
```sql
USE wakanda_gym;
SHOW TABLES;
SELECT COUNT(*) FROM usuarios;
```

### Backup de base de datos:
```bash
mysqldump -u gym_admin -p wakanda_gym > backup_wakanda_gym.sql
```

### Restaurar backup:
```bash
mysql -u gym_admin -p wakanda_gym < backup_wakanda_gym.sql
```