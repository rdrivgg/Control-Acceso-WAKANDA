import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import re
from datetime import datetime
from database import GymDatabase
from qr_manager import BarcodeManager
from sms_manager import SMSManager
from reports import ReportsManager
from admin_gui import AdminWindow

def sanitize_text(text):
    """Remove non-printable characters and excessive whitespace"""
    if text is None:
        return ""
    text = re.sub(r'[^\x20-\x7EñÑáéíóúÁÉÍÓÚüÜ]', '', str(text))
    text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    return ' '.join(text.split()).strip()

class GymAccessControl:
    def __init__(self, root):
        self.root = root
        self.root.title("WAKANDA GYM - Control de Acceso")
        self.root.geometry("800x600")
        self.root.configure(bg="#000000")
        
        self.db = GymDatabase()
        self.barcode_manager = BarcodeManager()
        self.sms_manager = SMSManager()
        self.reports_manager = ReportsManager()
        
        self.setup_ui()
        self.ultima_entrada = {}
        
    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Arial', 20, 'bold'), background="#000000", foreground="#FF8C00")
        style.configure('Section.TLabel', font=('Arial', 14, 'bold'), background="#000000", foreground="#FF8C00")
        style.configure('Info.TLabel', font=('Arial', 10), background="#000000", foreground="white")
        
        title_label = ttk.Label(self.root, text="WAKANDA GYM", style='Title.TLabel')
        title_label.pack(pady=20)
        
        subtitle_label = ttk.Label(self.root, text="Sistema de Control de Acceso", style='Section.TLabel')
        subtitle_label.pack(pady=5)
        
        main_frame = tk.Frame(self.root, bg="#000000")
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        left_frame = tk.Frame(main_frame, bg="#FF8C00", relief='raised', bd=2)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        scan_label = ttk.Label(left_frame, text="ESCANEO DE CÓDIGO DE BARRAS", style='Section.TLabel')
        scan_label.pack(pady=10)
        
        input_label = ttk.Label(left_frame, text="Escanee el código o escríbalo manualmente:", style='Info.TLabel')
        input_label.pack(pady=5)
        
        self.codigo_entry = tk.Entry(left_frame, font=('Arial', 14), width=15, justify='center')
        self.codigo_entry.pack(pady=10, padx=20)
        self.codigo_entry.bind('<Return>', self.procesar_codigo_entrada)
        self.codigo_entry.focus()
        
        self.procesar_button = tk.Button(left_frame, text="✅ PROCESAR CÓDIGO", 
                                       command=lambda: self.procesar_codigo_entrada(None), 
                                       bg="#000000", fg="#FF8C00", font=('Arial', 12, 'bold'),
                                       height=1, relief='raised', bd=3)
        self.procesar_button.pack(pady=10, padx=20, fill='x')
        
        self.limpiar_button = tk.Button(left_frame, text="🔄 LIMPIAR", 
                                      command=self.limpiar_entrada, 
                                      bg="#333333", fg="#FF8C00", font=('Arial', 10),
                                      relief='raised', bd=2)
        self.limpiar_button.pack(pady=5, padx=20, fill='x')
        
        self.status_frame = tk.Frame(left_frame, bg="#FF8C00")
        self.status_frame.pack(pady=20, padx=20, fill='x')
        
        self.status_label = ttk.Label(self.status_frame, text="Estado: Esperando escaneo...", 
                                    style='Info.TLabel')
        self.status_label.pack()
        
        self.user_info_text = tk.Text(left_frame, height=8, width=40, bg="#ecf0f1", 
                                    font=('Courier', 10), state='disabled')
        self.user_info_text.pack(pady=10, padx=20, fill='x')
        
        right_frame = tk.Frame(main_frame, bg="#FF8C00", relief='raised', bd=2)
        right_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        control_label = ttk.Label(right_frame, text="PANEL DE CONTROL", style='Section.TLabel')
        control_label.pack(pady=10)
        
        self.admin_button = tk.Button(right_frame, text="👥 GESTIÓN USUARIOS", 
                                    command=self.abrir_admin, 
                                    bg="#000000", fg="#FF8C00", font=('Arial', 10, 'bold'),
                                    relief='raised', bd=2)
        self.admin_button.pack(pady=5, padx=20, fill='x')
        
        self.report_button = tk.Button(right_frame, text="📊 REPORTE DIARIO", 
                                     command=self.generar_reporte, 
                                     bg="#FF8C00", fg="#000000", font=('Arial', 10, 'bold'),
                                     relief='raised', bd=2)
        self.report_button.pack(pady=5, padx=20, fill='x')
        
        self.access_log = tk.Text(right_frame, height=20, width=40, bg="#ecf0f1", 
                                font=('Courier', 9), state='disabled')
        self.access_log.pack(pady=10, padx=20, fill='both', expand=True)
        
        self.cargar_accesos_hoy()
    
    def procesar_codigo_entrada(self, event):
        codigo = sanitize_text(self.codigo_entry.get().strip())
        
        if not codigo:
            self.status_label.config(text="Estado: Por favor ingrese un código")
            messagebox.showwarning("Advertencia", "Por favor ingrese un código de barras")
            return
        
        # Validación adicional de longitud
        if len(codigo) > 20:
            self.status_label.config(text="Estado: Código demasiado largo")
            messagebox.showerror("Error", "El código debe tener máximo 20 caracteres")
            self.codigo_entry.select_range(0, 'end')
            return
        
        resultado = self.barcode_manager.validar_codigo_barras(codigo)
        
        if not resultado.get('valido'):
            error_msg = sanitize_text(resultado.get('error', 'Código de barras inválido'))
            self.status_label.config(text=f"Estado: {error_msg}")
            messagebox.showerror("Error", error_msg)
            self.codigo_entry.select_range(0, 'end')
            return
        
        codigo_validado = resultado['codigo']
        self.procesar_acceso(codigo_validado)
        self.limpiar_entrada()
    
    def limpiar_entrada(self):
        self.codigo_entry.delete(0, 'end')
        self.codigo_entry.focus()
    
    def procesar_acceso(self, codigo_barras):
        usuario = self.db.obtener_usuario_por_barcode(codigo_barras)
        
        if not usuario:
            self.status_label.config(text="Estado: Usuario no encontrado")
            messagebox.showerror("Error", "Usuario no registrado en el sistema")
            return
        
        user_id, codigo, nombre, apellido, telefono, email, estado_pago, fecha_registro, activo = usuario
        
        # Sanitizar datos del usuario
        nombre = sanitize_text(nombre)
        apellido = sanitize_text(apellido)
        telefono = sanitize_text(telefono)
        email = sanitize_text(email)
        estado_pago = sanitize_text(estado_pago)
        
        if estado_pago.lower() != 'pagado':
            self.status_label.config(text=f"Estado: Usuario sin pago - {nombre} {apellido}")
            messagebox.showwarning("Acceso Denegado", f"Usuario {nombre} {apellido} no ha pagado su mensualidad")
            
            self.sms_manager.enviar_alerta_no_pago(nombre, apellido, telefono)
            
            self.mostrar_info_usuario(usuario, "ACCESO DENEGADO - SIN PAGO")
            return
        
        tipo_acceso = self.determinar_tipo_acceso(user_id)
        self.db.registrar_acceso(user_id, tipo_acceso)
        
        self.status_label.config(text=f"Estado: {tipo_acceso.upper()} - {nombre} {apellido}")
        
        mensaje = "ENTRADA AUTORIZADA" if tipo_acceso == "entrada" else "SALIDA REGISTRADA"
        self.mostrar_info_usuario(usuario, mensaje)
        
        messagebox.showinfo("Acceso Autorizado", 
                          f"{tipo_acceso.upper()}: {nombre} {apellido}\nHora: {datetime.now().strftime('%H:%M:%S')}")
        
        self.cargar_accesos_hoy()
    
    def determinar_tipo_acceso(self, user_id):
        if user_id in self.ultima_entrada:
            return "salida"
        else:
            self.ultima_entrada[user_id] = datetime.now()
            return "entrada"
    
    def mostrar_info_usuario(self, usuario, mensaje):
        user_id, codigo, nombre, apellido, telefono, email, estado_pago, fecha_registro, activo = usuario
        
        # Sanitizar todos los campos
        mensaje = sanitize_text(mensaje)
        codigo = sanitize_text(codigo)
        nombre = sanitize_text(nombre)
        apellido = sanitize_text(apellido)
        telefono = sanitize_text(telefono) if telefono else 'N/A'
        email = sanitize_text(email) if email else 'N/A'
        estado_pago = sanitize_text(estado_pago)
        fecha_registro = sanitize_text(fecha_registro)
        
        info = f"{mensaje}\n\n"
        info += f"Código: {codigo}\n"
        info += f"Nombre: {nombre} {apellido}\n"
        info += f"Teléfono: {telefono}\n"
        info += f"Email: {email}\n"
        info += f"Estado: {estado_pago.upper()}\n"
        info += f"Registrado: {fecha_registro}\n"
        info += f"Hora actual: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        
        self.user_info_text.config(state='normal')
        self.user_info_text.delete(1.0, 'end')
        self.user_info_text.insert('end', info)
        self.user_info_text.config(state='disabled')
    
    def cargar_accesos_hoy(self):
        accesos = self.db.obtener_accesos_hoy()
        
        self.access_log.config(state='normal')
        self.access_log.delete(1.0, 'end')
        
        self.access_log.insert('end', f"=== ACCESOS DE HOY ===\n\n")
        
        for acceso in accesos:
            nombre, apellido, tipo, fecha_hora = acceso
            
            # Sanitizar datos antes de mostrar
            nombre = sanitize_text(nombre)
            apellido = sanitize_text(apellido)
            tipo = sanitize_text(tipo)
            fecha_hora = sanitize_text(fecha_hora)
            
            hora = fecha_hora.split()[1][:5] if ' ' in fecha_hora else fecha_hora
            icono = "[E]" if tipo == "entrada" else "[S]"
            
            self.access_log.insert('end', f"{icono} {hora} - {nombre} {apellido} ({tipo.upper()})\n")
        
        self.access_log.config(state='disabled')
        self.access_log.see('end')
    
    def abrir_admin(self):
        AdminWindow(self.root, self.db, self.barcode_manager)
    
    def generar_reporte(self):
        try:
            archivo = self.reports_manager.generar_reporte_diario()
            messagebox.showinfo("Reporte Generado", f"Reporte guardado en: {archivo}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")
    
    def mostrar_error(self, mensaje):
        messagebox.showerror("Error", mensaje)

if __name__ == "__main__":
    root = tk.Tk()
    app = GymAccessControl(root)
    root.mainloop()