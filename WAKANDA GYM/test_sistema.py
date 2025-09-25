#!/usr/bin/env python3
"""
Script de prueba para el sistema de control de acceso WAKANDA GYM
Simula el registro de usuarios y accesos
"""

from database import GymDatabase
from qr_manager import BarcodeManager
from reports import ReportsManager
from sms_manager import SMSManager

def probar_sistema():
    print("INICIANDO PRUEBAS DEL SISTEMA WAKANDA GYM")
    print("=" * 50)
    
    # Inicializar componentes
    db = GymDatabase()
    bm = BarcodeManager()
    reports = ReportsManager()
    sms = SMSManager()
    
    print("\nComponentes inicializados correctamente")
    
    # 1. Probar registro de usuarios
    print("\nREGISTRO DE USUARIOS DE PRUEBA:")
    print("-" * 35)
    
    usuarios_prueba = [
        ("Juan", "Perez", "123456789", "juan@email.com", "pagado"),
        ("Maria", "Lopez", "987654321", "maria@email.com", "pagado"),
        ("Carlos", "Garcia", "555123456", "carlos@email.com", "pendiente"),
        ("Ana", "Martinez", "444987654", "ana@email.com", "pagado"),
        ("Luis", "Rodriguez", "333666999", "luis@email.com", "pendiente")
    ]
    
    codigos_generados = []
    
    for nombre, apellido, telefono, email, estado in usuarios_prueba:
        try:
            # Generar código de barras
            codigo, archivo = bm.generar_codigo_barras(nombre, apellido)
            
            # Registrar en base de datos
            user_id = db.agregar_usuario(codigo, nombre, apellido, telefono, email, estado)
            
            if user_id:
                print(f"✅ {nombre} {apellido} - Código: {codigo} - Estado: {estado}")
                codigos_generados.append((codigo, nombre, apellido, estado))
            else:
                print(f"❌ Error registrando {nombre} {apellido}")
                
        except Exception as e:
            print(f"❌ Error con {nombre} {apellido}: {str(e)}")
    
    print(f"\n📊 Total usuarios registrados: {len(codigos_generados)}")
    
    # 2. Probar validación de códigos
    print("\n🔍 PRUEBA DE VALIDACIÓN DE CÓDIGOS:")
    print("-" * 40)
    
    for codigo, nombre, apellido, estado in codigos_generados[:3]:
        resultado = bm.validar_codigo_barras(codigo)
        if resultado['valido']:
            usuario = db.obtener_usuario_por_barcode(codigo)
            if usuario:
                print(f"✅ {codigo} -> {usuario[2]} {usuario[3]} ({usuario[6]})")
            else:
                print(f"❌ {codigo} -> Usuario no encontrado en BD")
        else:
            print(f"❌ {codigo} -> Código inválido")
    
    # 3. Simular accesos
    print("\n🚪 SIMULACIÓN DE ACCESOS:")
    print("-" * 30)
    
    import time
    
    for i, (codigo, nombre, apellido, estado) in enumerate(codigos_generados[:4]):
        usuario = db.obtener_usuario_por_barcode(codigo)
        if usuario:
            user_id = usuario[0]
            
            if estado == "pagado":
                # Registrar entrada
                db.registrar_acceso(user_id, "entrada")
                print(f"🟢 ENTRADA: {nombre} {apellido}")
                
                # Simular tiempo en el gimnasio
                time.sleep(0.1)
                
                # Algunos usuarios salen
                if i % 2 == 0:
                    db.registrar_acceso(user_id, "salida")
                    print(f"🔴 SALIDA: {nombre} {apellido}")
            else:
                print(f"🚫 ACCESO DENEGADO: {nombre} {apellido} (Sin pago)")
                # Simular alerta SMS
                print(f"📱 SMS enviado por usuario sin pago: {nombre} {apellido}")
    
    # 4. Mostrar accesos del día
    print("\n📋 ACCESOS DEL DÍA:")
    print("-" * 25)
    
    accesos = db.obtener_accesos_hoy()
    for acceso in accesos:
        nombre, apellido, tipo, fecha_hora = acceso
        hora = fecha_hora.split()[1][:5] if ' ' in fecha_hora else fecha_hora
        icono = "🟢" if tipo == "entrada" else "🔴"
        print(f"{icono} {hora} - {nombre} {apellido} ({tipo.upper()})")
    
    # 5. Generar reporte
    print("\n📊 GENERACIÓN DE REPORTE:")
    print("-" * 30)
    
    try:
        archivo_reporte = reports.generar_reporte_diario()
        print(f"✅ Reporte generado: {archivo_reporte}")
        
        # Mostrar estadísticas
        stats = reports.obtener_estadisticas_dia()
        print(f"📈 Estadísticas del día:")
        print(f"   - Entradas: {stats['total_entradas']}")
        print(f"   - Salidas: {stats['total_salidas']}")
        print(f"   - Usuarios únicos: {stats['usuarios_unicos']}")
        print(f"   - Total accesos: {stats['accesos_totales']}")
        
    except Exception as e:
        print(f"❌ Error generando reporte: {str(e)}")
    
    # 6. Mostrar usuarios registrados
    print("\n👥 USUARIOS EN EL SISTEMA:")
    print("-" * 30)
    
    usuarios = db.obtener_todos_usuarios()
    for usuario in usuarios:
        user_id, codigo, nombre, apellido, telefono, email, estado_pago, fecha_registro = usuario
        estado_icon = "💳" if estado_pago == "pagado" else "❌"
        print(f"{estado_icon} {nombre} {apellido} - {codigo} ({estado_pago})")
    
    print(f"\n📊 Total usuarios en sistema: {len(usuarios)}")
    print(f"💳 Usuarios pagados: {len([u for u in usuarios if u[6] == 'pagado'])}")
    print(f"❌ Usuarios pendientes: {len([u for u in usuarios if u[6] == 'pendiente'])}")
    
    print("\n🎉 PRUEBAS COMPLETADAS EXITOSAMENTE")
    print("=" * 50)
    print("\n📋 INSTRUCCIONES DE USO:")
    print("1. Ejecutar: python main.py")
    print("2. En el campo de código, escanear o escribir código de barras")
    print("3. Presionar Enter o click en 'PROCESAR CÓDIGO'")
    print("4. Para administración, click en 'GESTIÓN USUARIOS'")
    print("5. Para reportes, click en 'REPORTE DIARIO'")
    print("\n🔧 Los códigos de barras se encuentran en la carpeta 'barcodes/'")

if __name__ == "__main__":
    probar_sistema()