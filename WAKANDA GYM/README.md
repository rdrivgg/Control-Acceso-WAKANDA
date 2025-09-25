# WAKANDA GYM - Sistema de Control de Acceso

Sistema de control de acceso para gimnasio usando códigos de barras, desarrollado en Python con Tkinter.

## Características

- 🏃‍♂️ **Control de Acceso**: Escaneo de códigos de barras para entrada y salida
- 👥 **Gestión de Usuarios**: Registro y administración de miembros
- 💳 **Control de Pagos**: Verificación de estado de mensualidad  
- 📊 **Reportes Diarios**: Generación automática de reportes en CSV
- 📱 **Alertas SMS**: Notificaciones cuando usuarios sin pago intentan acceder
- 🎯 **Interfaz Intuitiva**: GUI moderna con Tkinter

## Instalación

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecutar la aplicación:
```bash
python main.py
```

## Uso

### Panel Principal
- **Escanear Cámara**: Activa la cámara para leer códigos de barras
- **Escanear Archivo**: Permite cargar una imagen con código de barras
- **Gestión Usuarios**: Abre el panel de administración
- **Reporte Diario**: Genera reporte CSV de accesos del día

### Panel de Administración
- **Registrar Usuario**: Crear nuevos usuarios y generar sus códigos
- **Gestionar Pagos**: Marcar usuarios como pagados o pendientes
- **Imprimir Códigos**: Regenerar códigos de barras para impresión

### Códigos de Barras
- Se generan automáticamente al registrar usuarios
- Formato: Código único de 10 caracteres alfanuméricos
- Se guardan como imágenes PNG en la carpeta `barcodes/`

## Estructura de Archivos

```
WAKANDA GYM/
├── main.py              # Aplicación principal
├── database.py          # Gestión de base de datos SQLite
├── qr_manager.py        # Generación y validación de códigos
├── sms_manager.py       # Sistema de alertas SMS
├── reports.py           # Generación de reportes
├── requirements.txt     # Dependencias
├── gym_control.db       # Base de datos (se crea automáticamente)
├── barcodes/            # Códigos generados
└── reportes_*.csv       # Reportes generados
```

## Base de Datos

### Tabla `usuarios`
- `id`: ID único
- `codigo_barras`: Código de barras único
- `nombre`: Nombre del usuario  
- `apellido`: Apellido del usuario
- `telefono`: Teléfono (opcional)
- `email`: Email (opcional)
- `estado_pago`: 'pagado' o 'pendiente'
- `fecha_registro`: Fecha de registro
- `activo`: Estado activo/inactivo

### Tabla `accesos`
- `id`: ID único
- `usuario_id`: Referencia al usuario
- `tipo`: 'entrada' o 'salida'
- `fecha_hora`: Timestamp del acceso

## Configuración SMS

Para habilitar alertas SMS, editar la configuración en la base de datos:
- `sms_enabled`: 'true' para habilitar
- `admin_phone`: Número de teléfono del administrador

## Casos de Uso Implementados

1. **Usuario con Código Válido y Pago**: ✅ Acceso autorizado
2. **Usuario sin Pago**: ❌ Acceso denegado + Alerta SMS
3. **Código Inválido**: ❌ Error de validación
4. **Usuario No Registrado**: ❌ Usuario no encontrado
5. **Reporte Diario**: 📊 CSV con todos los accesos
6. **Gestión de Usuarios**: 👥 CRUD completo

## Tecnologías Usadas

- **Python 3.x**: Lenguaje principal
- **Tkinter**: Interfaz gráfica nativa
- **SQLite**: Base de datos local
- **OpenCV**: Procesamiento de cámara
- **python-barcode**: Generación de códigos
- **pyzbar**: Lectura de códigos de barras
- **Pillow**: Procesamiento de imágenes

## Autor

Sistema desarrollado para WAKANDA GYM - Control de Acceso Profesional