#!/usr/bin/env python3
"""
Script de prueba simple para el sistema de control de acceso WAKANDA GYM
"""

from database import GymDatabase
from qr_manager import BarcodeManager
from reports import ReportsManager

def test_sistema():
    print("=== PRUEBA DEL SISTEMA WAKANDA GYM ===")
    
    # Inicializar componentes
    db = GymDatabase()
    bm = BarcodeManager()
    reports = ReportsManager()
    
    print("Componentes inicializados OK")
    
    # Registrar usuarios de prueba
    usuarios = [
        ("Juan", "Perez", "123456789", "juan@email.com", "pagado"),
        ("Maria", "Lopez", "987654321", "maria@email.com", "pendiente"),
        ("Carlos", "Garcia", "555123456", "carlos@email.com", "pagado")
    ]
    
    print("\nRegistrando usuarios de prueba...")
    codigos = []
    
    for nombre, apellido, telefono, email, estado in usuarios:
        codigo, archivo = bm.generar_codigo_barras(nombre, apellido)
        user_id = db.agregar_usuario(codigo, nombre, apellido, telefono, email, estado)
        
        if user_id:
            print(f"- {nombre} {apellido}: {codigo} ({estado})")
            codigos.append((codigo, nombre, apellido, estado))
        else:
            print(f"- ERROR: {nombre} {apellido}")
    
    print(f"\nUsuarios registrados: {len(codigos)}")
    
    # Probar validación
    print("\nProbando validacion de codigos...")
    for codigo, nombre, apellido, estado in codigos:
        resultado = bm.validar_codigo_barras(codigo)
        usuario = db.obtener_usuario_por_barcode(codigo)
        
        if resultado['valido'] and usuario:
            print(f"- {codigo} -> {usuario[2]} {usuario[3]} OK")
        else:
            print(f"- {codigo} -> ERROR")
    
    # Simular accesos
    print("\nSimulando accesos...")
    for codigo, nombre, apellido, estado in codigos:
        usuario = db.obtener_usuario_por_barcode(codigo)
        if usuario and estado == "pagado":
            db.registrar_acceso(usuario[0], "entrada")
            print(f"- ENTRADA: {nombre} {apellido}")
        elif usuario:
            print(f"- DENEGADO: {nombre} {apellido} (sin pago)")
    
    # Mostrar accesos
    print("\nAccesos del dia:")
    accesos = db.obtener_accesos_hoy()
    for acceso in accesos:
        nombre, apellido, tipo, fecha_hora = acceso
        print(f"- {nombre} {apellido}: {tipo}")
    
    # Generar reporte
    try:
        archivo = reports.generar_reporte_diario()
        stats = reports.obtener_estadisticas_dia()
        print(f"\nReporte generado: {archivo}")
        print(f"Estadisticas - Entradas: {stats['total_entradas']}, Usuarios: {stats['usuarios_unicos']}")
    except Exception as e:
        print(f"Error en reporte: {e}")
    
    print("\n=== PRUEBA COMPLETADA ===")
    print("\nPara usar el sistema:")
    print("1. python main.py")
    print("2. Ingresar codigo en el campo de texto")
    print("3. Los codigos generados estan en carpeta 'barcodes/'")

if __name__ == "__main__":
    test_sistema()