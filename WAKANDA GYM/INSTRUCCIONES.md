# WAKANDA GYM - Sistema de Control de Acceso

## ✅ INSTALACIÓN Y EJECUCIÓN

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Ejecutar aplicación
```bash
python main.py
```

### 3. Probar el sistema
```bash
python test_simple.py
```

## 📋 CÓDIGOS DE PRUEBA GENERADOS

Los siguientes códigos están listos para probar:

- **456BEF6725** - Juan Perez (PAGADO) ✅
- **21722384C4** - Maria Lopez (SIN PAGO) ❌  
- **FAA584E644** - Carlos Garcia (PAGADO) ✅

## 🎯 CÓMO USAR

### Panel Principal
1. **Campo de código**: Escanear código de barras o escribir manualmente
2. **Presionar ENTER** o click en "PROCESAR CÓDIGO"
3. El sistema validará automáticamente:
   - ✅ Usuario pagado → Acceso autorizado
   - ❌ Usuario sin pago → Acceso denegado + Alerta
   - ❓ Código inválido → Error

### Panel de Administración
1. Click en **"GESTIÓN USUARIOS"**
2. **Registrar nuevos usuarios**: Llenar formulario + click "REGISTRAR"
3. **Cambiar estado de pago**: Seleccionar usuario + click "MARCAR COMO PAGADO"
4. **Imprimir código**: Seleccionar usuario + click "IMPRIMIR CÓDIGO"

### Reportes
1. Click en **"REPORTE DIARIO"**
2. Se genera archivo CSV automáticamente
3. Incluye estadísticas de entrada/salida

## 🏃‍♂️ FLUJO DE USO TÍPICO

### Entrada de Usuario
1. Usuario escanea su código de barras
2. Sistema verifica estado de pago
3. Si pagó → "✅ ENTRADA AUTORIZADA"
4. Si no pagó → "❌ ACCESO DENEGADO" + SMS al admin

### Salida de Usuario  
1. Mismo código escaneado nuevamente
2. Sistema detecta que ya entró
3. Registra como "🔴 SALIDA"

### Gestión Diaria
1. Al final del día → "REPORTE DIARIO"
2. Archivo CSV con todos los movimientos
3. Estadísticas de usuarios únicos, entradas, salidas

## 🛠️ CONFIGURACIÓN

### SMS (Opcional)
Para habilitar SMS reales, editar `sms_manager.py`:
- Configurar servicio (Twilio, etc.)
- Agregar credenciales
- Cambiar en BD: `sms_enabled` = 'true'

### Base de Datos
- **Archivo**: `gym_control.db` (SQLite)
- **Ubicación**: Carpeta del proyecto
- **Backup**: Copiar archivo para respaldo

## 📁 ESTRUCTURA DE ARCHIVOS

```
WAKANDA GYM/
├── main.py                    # Aplicación principal
├── database.py                # Base de datos SQLite
├── qr_manager.py             # Códigos de barras
├── sms_manager.py            # Alertas SMS
├── reports.py                # Reportes CSV
├── gym_control.db            # Base de datos
├── barcodes/                 # Códigos generados
│   ├── 456BEF6725_Juan_Perez.png
│   └── ...
└── reporte_accesos_*.csv     # Reportes diarios
```

## 🚨 CASOS DE USO IMPLEMENTADOS

✅ **Usuario con código válido y pago** → Acceso autorizado
✅ **Usuario sin pago** → Acceso denegado + SMS
✅ **Código inválido** → Error de validación  
✅ **Usuario no registrado** → Usuario no encontrado
✅ **Reporte diario** → CSV con estadísticas
✅ **Gestión de usuarios** → CRUD completo

## 🔧 INTEGRACIÓN CON LECTOR FÍSICO

El sistema está diseñado para lectores USB de códigos de barras:

1. **Conectar lector** USB al equipo
2. **Configurar como HID** (actúa como teclado)
3. **Enfocar campo de código** en la aplicación
4. **Escanear código** → Se escribe automáticamente + ENTER

**Lectores recomendados:**
- Cualquier lector USB HID compatible
- Configuración automática (plug & play)
- Soporte para CODE128 (usado por el sistema)

## 📞 SOPORTE

- El sistema registra errores en consola
- Base de datos se crea automáticamente
- Códigos se regeneran si se pierden
- Backup manual copiando `gym_control.db`