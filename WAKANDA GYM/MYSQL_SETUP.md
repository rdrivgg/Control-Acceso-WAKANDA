# 🐬 Configuración MySQL para WAKANDA GYM

## 📋 Pasos de Instalación

### 1. Instalar MySQL Server

**Windows:**
```bash
# Descargar desde: https://dev.mysql.com/downloads/mysql/
# O usando chocolatey:
choco install mysql
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
```

**macOS:**
```bash
brew install mysql
brew services start mysql
```

### 2. Configurar Base de Datos

```sql
-- Conectar como root
mysql -u root -p

-- Crear base de datos
CREATE DATABASE wakanda_gym CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Crear usuario dedicado
CREATE USER 'gym_admin'@'%' IDENTIFIED BY 'gym123456';

-- Otorgar permisos
GRANT ALL PRIVILEGES ON wakanda_gym.* TO 'gym_admin'@'%';
FLUSH PRIVILEGES;

-- Verificar
SHOW DATABASES;
SELECT User, Host FROM mysql.user WHERE User = 'gym_admin';
```

### 3. Configuración para Acceso Remoto

#### Editar configuración MySQL
**Linux:** `/etc/mysql/mysql.conf.d/mysqld.cnf`
**Windows:** `C:\ProgramData\MySQL\MySQL Server 8.0\my.ini`

```ini
[mysqld]
# Permitir conexiones remotas
bind-address = 0.0.0.0

# Puerto por defecto
port = 3306

# Configuración de seguridad
ssl-ca = ca.pem
ssl-cert = server-cert.pem
ssl-key = server-key.pem
```

#### Abrir puerto en firewall
```bash
# Linux (ufw)
sudo ufw allow 3306

# Windows
# Ir a: Panel de Control > Sistema y Seguridad > Firewall de Windows
# Crear regla de entrada para puerto 3306
```

#### Reiniciar servicio
```bash
# Linux
sudo systemctl restart mysql

# Windows
net stop mysql80
net start mysql80

# macOS
brew services restart mysql
```

### 4. Configurar Variables de Entorno

Copiar `.env.example` a `.env` y editar:

```bash
# Copiar archivo de configuración
cp .env.example .env

# Editar con tus datos
# Para conexión local:
DB_HOST=localhost
DB_PORT=3306
DB_NAME=wakanda_gym
DB_USER=gym_admin
DB_PASSWORD=gym123456

# Para conexión remota:
DB_HOST=192.168.1.100  # IP del servidor MySQL
DB_PORT=3306
DB_NAME=wakanda_gym
DB_USER=gym_admin
DB_PASSWORD=gym123456
```

### 5. Instalar Dependencias Python

```bash
pip install -r requirements.txt
```

### 6. Migrar Datos desde SQLite (Opcional)

Si tienes datos en `gym_control.db`:

```bash
python migrate_sqlite_to_mysql.py
```

### 7. Probar Conexión

```bash
python -c "from database import GymDatabase; db = GymDatabase(); print('✅ Conexión MySQL exitosa')"
```

## 🌐 Configuración Multi-Instancia

### Servidor Central (MySQL)
- Instalar MySQL Server
- Configurar para acceso remoto
- IP estática recomendada
- Backup automático configurado

### Clientes (Aplicaciones)
- Solo necesitan las dependencias Python
- Configurar `.env` con IP del servidor
- No necesitan MySQL Server local

### Ejemplo de Red:
```
Servidor MySQL: 192.168.1.100:3306
├── Cliente 1:  192.168.1.101 (Recepción)
├── Cliente 2:  192.168.1.102 (Entrada principal)
└── Cliente 3:  192.168.1.103 (Salida)
```

## 🔒 Seguridad

### Recomendaciones:
1. **Cambiar contraseñas por defecto**
2. **Usar SSL/TLS para conexiones remotas**
3. **Firewall configurado correctamente**
4. **Backup regular de la base de datos**
5. **Actualizar MySQL regularmente**

### Backup automatizado:
```bash
# Crear script de backup diario
#!/bin/bash
mysqldump -u gym_admin -pgym123456 wakanda_gym > backup_$(date +%Y%m%d).sql
```

## 🚨 Troubleshooting

### Error: "Can't connect to MySQL server"
1. Verificar que MySQL esté ejecutándose
2. Verificar configuración de firewall
3. Verificar bind-address en configuración
4. Verificar credenciales en .env

### Error: "Access denied for user"
1. Verificar usuario y contraseña
2. Verificar permisos del usuario
3. Verificar host permitido (% vs localhost)

### Error: "Unknown database"
1. Verificar que la base de datos existe
2. Ejecutar scripts de creación de BD

### Performance lenta:
1. Verificar índices en tablas
2. Optimizar consultas
3. Configurar pool de conexiones
4. Monitorear recursos del servidor

## 📊 Monitoreo

### Consultas útiles:
```sql
-- Ver conexiones activas
SHOW PROCESSLIST;

-- Ver estado del servidor
SHOW STATUS LIKE 'Threads_connected';

-- Ver tablas y tamaños
SELECT table_name, table_rows, data_length, index_length 
FROM information_schema.tables 
WHERE table_schema = 'wakanda_gym';
```

¡Listo! Tu sistema WAKANDA GYM ahora puede funcionar con MySQL local o remoto. 🎉