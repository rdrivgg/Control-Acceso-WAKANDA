import csv
from datetime import date, datetime
from database import GymDatabase

class ReportsManager:
    def __init__(self):
        self.db = GymDatabase()
        
    def generar_reporte_diario(self, fecha=None):
        """Genera un reporte CSV con los accesos del día"""
        if fecha is None:
            fecha = date.today()
        
        fecha_str = fecha.strftime('%Y-%m-%d')
        filename = f"reporte_accesos_{fecha_str}.csv"
        
        accesos = self.db.obtener_accesos_hoy()
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Encabezados
            writer.writerow(['Fecha Reporte', 'Nombre', 'Apellido', 'Tipo Acceso', 'Hora', 'Fecha Completa'])
            writer.writerow([fecha_str, '', '', '', '', ''])
            writer.writerow(['', '', '', '', '', ''])
            
            total_entradas = 0
            total_salidas = 0
            
            for acceso in accesos:
                nombre, apellido, tipo, fecha_hora = acceso
                if tipo == 'entrada':
                    total_entradas += 1
                else:
                    total_salidas += 1
                    
                # Extraer solo la hora
                try:
                    hora = datetime.strptime(fecha_hora, '%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S')
                except:
                    hora = fecha_hora
                
                writer.writerow([fecha_str, nombre, apellido, tipo.upper(), hora, fecha_hora])
            
            # Resumen
            writer.writerow(['', '', '', '', '', ''])
            writer.writerow(['RESUMEN DEL DÍA:', '', '', '', '', ''])
            writer.writerow(['Total Entradas:', total_entradas, '', '', '', ''])
            writer.writerow(['Total Salidas:', total_salidas, '', '', '', ''])
            writer.writerow(['Usuarios únicos:', len(set(f"{acceso[0]} {acceso[1]}" for acceso in accesos)), '', '', '', ''])
            writer.writerow(['Hora generación:', datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '', '', '', ''])
        
        return filename
    
    def generar_reporte_usuarios(self):
        """Genera un reporte CSV con todos los usuarios registrados"""
        filename = f"reporte_usuarios_{date.today().strftime('%Y-%m-%d')}.csv"
        
        usuarios = self.db.obtener_todos_usuarios()
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            writer.writerow(['ID', 'Código Barras', 'Nombre', 'Apellido', 'Teléfono', 'Email', 'Estado Pago', 'Fecha Registro'])
            
            for usuario in usuarios:
                writer.writerow(usuario)
            
            writer.writerow(['', '', '', '', '', '', '', ''])
            writer.writerow(['Total usuarios:', len(usuarios), '', '', '', '', '', ''])
            writer.writerow(['Usuarios pagados:', len([u for u in usuarios if u[6] == 'pagado']), '', '', '', '', '', ''])
            writer.writerow(['Usuarios pendientes:', len([u for u in usuarios if u[6] == 'pendiente']), '', '', '', '', '', ''])
            
        return filename
    
    def obtener_estadisticas_dia(self, fecha=None):
        """Obtiene estadísticas del día especificado"""
        if fecha is None:
            fecha = date.today()
            
        accesos = self.db.obtener_accesos_hoy()
        
        estadisticas = {
            'fecha': fecha.strftime('%Y-%m-%d'),
            'total_entradas': len([a for a in accesos if a[2] == 'entrada']),
            'total_salidas': len([a for a in accesos if a[2] == 'salida']),
            'usuarios_unicos': len(set(f"{acceso[0]} {acceso[1]}" for acceso in accesos)),
            'accesos_totales': len(accesos)
        }
        
        return estadisticas