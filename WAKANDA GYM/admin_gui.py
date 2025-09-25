import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, date
import re
from database import GymDatabase
from qr_manager import BarcodeManager
from reports import ReportsManager
import os

def sanitize_text(text):
    """Remove non-printable characters and excessive whitespace"""
    if text is None:
        return ""
    text = re.sub(r'[^\x20-\x7EñÑáéíóúÁÉÍÓÚüÜ]', '', str(text))
    text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    return ' '.join(text.split()).strip()

class AdminWindow:
    def __init__(self, parent, db, barcode_manager):
        self.db = db
        self.barcode_manager = barcode_manager
        self.reports_manager = ReportsManager()
        
        self.window = tk.Toplevel(parent)
        self.window.title("WAKANDA GYM - Panel de Administración")
        self.window.geometry("1200x800")
        self.window.configure(bg="#000000")
        
        # Variables para filtros y búsqueda
        self.filtro_estado = tk.StringVar(value="todos")
        self.busqueda_texto = tk.StringVar()
        
        self.setup_admin_ui()
        self.cargar_usuarios()
        
        # Auto-refresh cada 30 segundos
        self.auto_refresh()
    
    def setup_admin_ui(self):
        """Configurar la interfaz de administración"""
        # Título principal
        title_frame = tk.Frame(self.window, bg="#000000")
        title_frame.pack(fill='x', pady=10)
        
        title = tk.Label(title_frame, text="🛠️ PANEL DE ADMINISTRACIÓN", 
                        font=('Arial', 18, 'bold'), bg="#000000", fg="#FF8C00")
        title.pack()
        
        subtitle = tk.Label(title_frame, text="Gestión Completa del Sistema WAKANDA GYM", 
                           font=('Arial', 12), bg="#000000", fg="white")
        subtitle.pack()
        
        # Crear notebook (pestañas)
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestaña 1: Gestión de Usuarios
        self.setup_usuarios_tab()
        
        # Pestaña 2: Reportes y Estadísticas
        self.setup_reportes_tab()
        
        # Pestaña 3: Configuración
        self.setup_configuracion_tab()
        
        # Pestaña 4: Respaldos
        self.setup_respaldos_tab()
    
    def setup_usuarios_tab(self):
        """Pestaña de gestión de usuarios"""
        usuarios_frame = ttk.Frame(self.notebook)
        self.notebook.add(usuarios_frame, text="👥 Usuarios")
        
        # Frame para registro de nuevo usuario
        registro_frame = tk.LabelFrame(usuarios_frame, text="📝 Registrar Nuevo Usuario", 
                                     font=('Arial', 12, 'bold'), bg="#FF8C00", fg="#000000")
        registro_frame.pack(fill='x', padx=10, pady=5)
        
        # Campos del formulario
        campos_frame = tk.Frame(registro_frame, bg="#FF8C00")
        campos_frame.pack(pady=10, padx=10)
        
        # Fila 1
        tk.Label(campos_frame, text="Nombre *:", bg="#FF8C00", fg="#000000", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.nombre_entry = tk.Entry(campos_frame, width=20, font=('Arial', 10))\n        self.nombre_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(campos_frame, text="Apellido *:", bg="#FF8C00", fg="#000000", font=('Arial', 10, 'bold')).grid(row=0, column=2, sticky='e', padx=5, pady=5)
        self.apellido_entry = tk.Entry(campos_frame, width=20, font=('Arial', 10))
        self.apellido_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Fila 2
        tk.Label(campos_frame, text="Teléfono:", bg="#FF8C00", fg="#000000", font=('Arial', 10)).grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.telefono_entry = tk.Entry(campos_frame, width=20, font=('Arial', 10))
        self.telefono_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(campos_frame, text="Email:", bg="#FF8C00", fg="#000000", font=('Arial', 10)).grid(row=1, column=2, sticky='e', padx=5, pady=5)
        self.email_entry = tk.Entry(campos_frame, width=20, font=('Arial', 10))
        self.email_entry.grid(row=1, column=3, padx=5, pady=5)
        
        # Fila 3
        tk.Label(campos_frame, text="Estado Pago:", bg="#FF8C00", fg="#000000", font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.estado_pago_combo = ttk.Combobox(campos_frame, values=['pendiente', 'pagado'], 
                                            state='readonly', width=18)
        self.estado_pago_combo.set('pendiente')
        self.estado_pago_combo.grid(row=2, column=1, padx=5, pady=5)
        
        # Botones de acción
        botones_frame = tk.Frame(registro_frame, bg="#FF8C00")
        botones_frame.pack(pady=10)
        
        tk.Button(botones_frame, text="✅ REGISTRAR USUARIO", command=self.registrar_usuario,
                 bg="#000000", fg="#FF8C00", font=('Arial', 11, 'bold'), 
                 relief='raised', bd=2, padx=20).pack(side='left', padx=5)
        
        tk.Button(botones_frame, text="🔄 LIMPIAR CAMPOS", command=self.limpiar_campos,
                 bg="#333333", fg="#FF8C00", font=('Arial', 11), 
                 relief='raised', bd=2, padx=20).pack(side='left', padx=5)
        
        # Frame para búsqueda y filtros
        busqueda_frame = tk.LabelFrame(usuarios_frame, text="🔍 Búsqueda y Filtros", 
                                     font=('Arial', 12, 'bold'), bg="#333333", fg="#FF8C00")
        busqueda_frame.pack(fill='x', padx=10, pady=5)
        
        filtros_frame = tk.Frame(busqueda_frame, bg="#333333")
        filtros_frame.pack(pady=10, padx=10)
        
        tk.Label(filtros_frame, text="Buscar:", bg="#333333", fg="white", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='e', padx=5)
        busqueda_entry = tk.Entry(filtros_frame, textvariable=self.busqueda_texto, width=30, font=('Arial', 10))
        busqueda_entry.grid(row=0, column=1, padx=5)
        busqueda_entry.bind('<KeyRelease>', self.filtrar_usuarios)
        
        tk.Label(filtros_frame, text="Estado:", bg="#333333", fg="white", font=('Arial', 10, 'bold')).grid(row=0, column=2, sticky='e', padx=5)
        filtro_combo = ttk.Combobox(filtros_frame, textvariable=self.filtro_estado,
                                  values=['todos', 'pagado', 'pendiente'], state='readonly', width=15)
        filtro_combo.grid(row=0, column=3, padx=5)
        filtro_combo.bind('<<ComboboxSelected>>', self.filtrar_usuarios)
        
        tk.Button(filtros_frame, text="🔄 ACTUALIZAR", command=self.cargar_usuarios,
                 bg="#FF8C00", fg="#000000", font=('Arial', 10, 'bold')).grid(row=0, column=4, padx=10)
        
        # Frame para lista de usuarios
        lista_frame = tk.LabelFrame(usuarios_frame, text="📋 Lista de Usuarios", 
                                  font=('Arial', 12, 'bold'), bg="#222222", fg="#FF8C00")
        lista_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Treeview mejorado
        tree_frame = tk.Frame(lista_frame, bg="#222222")
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.tree = ttk.Treeview(tree_frame, columns=('ID', 'Código', 'Nombre', 'Apellido', 'Teléfono', 'Email', 'Estado', 'Registro'), 
                               show='headings', height=15)
        
        # Configurar columnas
        self.tree.heading('#1', text='ID')
        self.tree.heading('#2', text='Código de Barras')
        self.tree.heading('#3', text='Nombre')
        self.tree.heading('#4', text='Apellido')
        self.tree.heading('#5', text='Teléfono')
        self.tree.heading('#6', text='Email')
        self.tree.heading('#7', text='Estado Pago')
        self.tree.heading('#8', text='F. Registro')
        
        self.tree.column('#1', width=50, anchor='center')
        self.tree.column('#2', width=120, anchor='center')
        self.tree.column('#3', width=120)
        self.tree.column('#4', width=120)
        self.tree.column('#5', width=100, anchor='center')
        self.tree.column('#6', width=180)
        self.tree.column('#7', width=100, anchor='center')
        self.tree.column('#8', width=100, anchor='center')
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Frame de acciones sobre usuarios
        acciones_frame = tk.Frame(usuarios_frame, bg="#000000")
        acciones_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Button(acciones_frame, text="💳 MARCAR COMO PAGADO", command=self.marcar_pagado,
                 bg="#00AA00", fg="white", font=('Arial', 11, 'bold'), 
                 relief='raised', bd=2, padx=15).pack(side='left', padx=5)
        
        tk.Button(acciones_frame, text="❌ MARCAR SIN PAGO", command=self.marcar_sin_pago,
                 bg="#CC0000", fg="white", font=('Arial', 11, 'bold'), 
                 relief='raised', bd=2, padx=15).pack(side='left', padx=5)
        
        tk.Button(acciones_frame, text="🖨️ IMPRIMIR CÓDIGO", command=self.imprimir_codigo,
                 bg="#FF8C00", fg="#000000", font=('Arial', 11, 'bold'), 
                 relief='raised', bd=2, padx=15).pack(side='left', padx=5)
        
        tk.Button(acciones_frame, text="✏️ EDITAR USUARIO", command=self.editar_usuario,
                 bg="#0066CC", fg="white", font=('Arial', 11, 'bold'), 
                 relief='raised', bd=2, padx=15).pack(side='left', padx=5)
        
        tk.Button(acciones_frame, text="🗑️ ELIMINAR USUARIO", command=self.eliminar_usuario,
                 bg="#660000", fg="white", font=('Arial', 11, 'bold'), 
                 relief='raised', bd=2, padx=15).pack(side='left', padx=5)
    
    def setup_reportes_tab(self):
        """Pestaña de reportes y estadísticas"""
        reportes_frame = ttk.Frame(self.notebook)
        self.notebook.add(reportes_frame, text="📊 Reportes")
        
        # Frame de estadísticas rápidas
        stats_frame = tk.LabelFrame(reportes_frame, text="📈 Estadísticas de Hoy", 
                                  font=('Arial', 12, 'bold'), bg="#FF8C00", fg="#000000")
        stats_frame.pack(fill='x', padx=10, pady=5)
        
        self.stats_frame_content = tk.Frame(stats_frame, bg="#FF8C00")
        self.stats_frame_content.pack(pady=10, padx=10)
        
        self.actualizar_estadisticas()
        
        # Frame de generación de reportes
        gen_reportes_frame = tk.LabelFrame(reportes_frame, text="📋 Generar Reportes", 
                                         font=('Arial', 12, 'bold'), bg="#333333", fg="#FF8C00")
        gen_reportes_frame.pack(fill='x', padx=10, pady=5)
        
        reportes_content = tk.Frame(gen_reportes_frame, bg="#333333")
        reportes_content.pack(pady=10, padx=10)
        
        # Botones de reportes
        tk.Button(reportes_content, text="📅 REPORTE DIARIO", command=self.generar_reporte_diario,
                 bg="#FF8C00", fg="#000000", font=('Arial', 11, 'bold'), 
                 relief='raised', bd=2, padx=20).grid(row=0, column=0, padx=5, pady=5)
        
        tk.Button(reportes_content, text="📆 REPORTE SEMANAL", command=self.generar_reporte_semanal,
                 bg="#FF8C00", fg="#000000", font=('Arial', 11, 'bold'), 
                 relief='raised', bd=2, padx=20).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Button(reportes_content, text="📊 REPORTE MENSUAL", command=self.generar_reporte_mensual,
                 bg="#FF8C00", fg="#000000", font=('Arial', 11, 'bold'), 
                 relief='raised', bd=2, padx=20).grid(row=0, column=2, padx=5, pady=5)
        
        tk.Button(reportes_content, text="👥 USUARIOS SIN PAGO", command=self.generar_reporte_sin_pago,
                 bg="#CC0000", fg="white", font=('Arial', 11, 'bold'), 
                 relief='raised', bd=2, padx=20).grid(row=1, column=0, padx=5, pady=5)
        
        tk.Button(reportes_content, text="💳 USUARIOS PAGADOS", command=self.generar_reporte_pagados,
                 bg="#00AA00", fg="white", font=('Arial', 11, 'bold'), 
                 relief='raised', bd=2, padx=20).grid(row=1, column=1, padx=5, pady=5)
        
        tk.Button(reportes_content, text="📈 ESTADÍSTICAS COMPLETAS", command=self.generar_estadisticas_completas,
                 bg="#0066CC", fg="white", font=('Arial', 11, 'bold'), 
                 relief='raised', bd=2, padx=20).grid(row=1, column=2, padx=5, pady=5)
        
        # Frame de accesos recientes
        accesos_frame = tk.LabelFrame(reportes_frame, text="🚪 Accesos Recientes", 
                                    font=('Arial', 12, 'bold'), bg="#222222", fg="#FF8C00")
        accesos_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.accesos_tree = ttk.Treeview(accesos_frame, columns=('Nombre', 'Tipo', 'Hora'), 
                                       show='headings', height=10)
        
        self.accesos_tree.heading('#1', text='Usuario')
        self.accesos_tree.heading('#2', text='Tipo')
        self.accesos_tree.heading('#3', text='Fecha/Hora')
        
        self.accesos_tree.column('#1', width=200)
        self.accesos_tree.column('#2', width=100, anchor='center')
        self.accesos_tree.column('#3', width=150, anchor='center')
        
        self.accesos_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.cargar_accesos_recientes()
    
    def setup_configuracion_tab(self):
        """Pestaña de configuración del sistema"""
        config_frame = ttk.Frame(self.notebook)
        self.notebook.add(config_frame, text="⚙️ Configuración")
        
        # Frame de configuración de base de datos
        db_frame = tk.LabelFrame(config_frame, text="🗄️ Configuración de Base de Datos", 
                               font=('Arial', 12, 'bold'), bg="#FF8C00", fg="#000000")
        db_frame.pack(fill='x', padx=10, pady=5)
        
        db_content = tk.Frame(db_frame, bg="#FF8C00")
        db_content.pack(pady=10, padx=10)
        
        tk.Button(db_content, text="🔧 VERIFICAR CONEXIÓN", command=self.verificar_conexion_db,
                 bg="#000000", fg="#FF8C00", font=('Arial', 11, 'bold'), 
                 relief='raised', bd=2, padx=20).pack(side='left', padx=5)
        
        tk.Button(db_content, text="🔄 REINICIALIZAR TABLAS", command=self.reinicializar_tablas,
                 bg="#CC4400", fg="white", font=('Arial', 11, 'bold'), 
                 relief='raised', bd=2, padx=20).pack(side='left', padx=5)
        
        # Frame de configuración SMS
        sms_frame = tk.LabelFrame(config_frame, text="📱 Configuración SMS", 
                                font=('Arial', 12, 'bold'), bg="#333333", fg="#FF8C00")
        sms_frame.pack(fill='x', padx=10, pady=5)
        
        sms_content = tk.Frame(sms_frame, bg="#333333")
        sms_content.pack(pady=10, padx=10)
        
        tk.Label(sms_content, text="SMS Habilitado:", bg="#333333", fg="white", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='e', padx=5)
        self.sms_enabled_var = tk.StringVar()
        sms_check = tk.Checkbutton(sms_content, variable=self.sms_enabled_var, bg="#333333")
        sms_check.grid(row=0, column=1, padx=5)
        
        tk.Label(sms_content, text="Teléfono Admin:", bg="#333333", fg="white", font=('Arial', 10, 'bold')).grid(row=0, column=2, sticky='e', padx=5)
        self.admin_phone_entry = tk.Entry(sms_content, width=20, font=('Arial', 10))
        self.admin_phone_entry.grid(row=0, column=3, padx=5)
        
        tk.Button(sms_content, text="💾 GUARDAR CONFIG", command=self.guardar_config_sms,
                 bg="#FF8C00", fg="#000000", font=('Arial', 10, 'bold'), 
                 relief='raised', bd=2).grid(row=0, column=4, padx=10)
        
        self.cargar_configuracion_sms()
    
    def setup_respaldos_tab(self):
        """Pestaña de respaldos y mantenimiento"""
        respaldos_frame = ttk.Frame(self.notebook)
        self.notebook.add(respaldos_frame, text="💾 Respaldos")
        
        # Frame de respaldos
        backup_frame = tk.LabelFrame(respaldos_frame, text="💾 Gestión de Respaldos", 
                                   font=('Arial', 12, 'bold'), bg="#FF8C00", fg="#000000")
        backup_frame.pack(fill='x', padx=10, pady=5)
        
        backup_content = tk.Frame(backup_frame, bg="#FF8C00")
        backup_content.pack(pady=10, padx=10)
        
        tk.Button(backup_content, text="💾 CREAR RESPALDO", command=self.crear_respaldo,
                 bg="#000000", fg="#FF8C00", font=('Arial', 11, 'bold'), 
                 relief='raised', bd=2, padx=20).pack(side='left', padx=5)
        
        tk.Button(backup_content, text="📂 ABRIR CARPETA RESPALDOS", command=self.abrir_carpeta_respaldos,
                 bg="#333333", fg="#FF8C00", font=('Arial', 11, 'bold'), 
                 relief='raised', bd=2, padx=20).pack(side='left', padx=5)
        
        # Frame de mantenimiento
        mant_frame = tk.LabelFrame(respaldos_frame, text="🔧 Mantenimiento del Sistema", 
                                 font=('Arial', 12, 'bold'), bg="#333333", fg="#FF8C00")
        mant_frame.pack(fill='x', padx=10, pady=5)
        
        mant_content = tk.Frame(mant_frame, bg="#333333")
        mant_content.pack(pady=10, padx=10)
        
        tk.Button(mant_content, text="🗑️ LIMPIAR ACCESOS ANTIGUOS", command=self.limpiar_accesos_antiguos,
                 bg="#CC4400", fg="white", font=('Arial', 11, 'bold'), 
                 relief='raised', bd=2, padx=20).pack(side='left', padx=5)
        
        tk.Button(mant_content, text="🔄 OPTIMIZAR BASE DE DATOS", command=self.optimizar_database,
                 bg="#0066CC", fg="white", font=('Arial', 11, 'bold'), 
                 relief='raised', bd=2, padx=20).pack(side='left', padx=5)
    
    def registrar_usuario(self):
        """Registrar nuevo usuario"""
        nombre = sanitize_text(self.nombre_entry.get().strip())
        apellido = sanitize_text(self.apellido_entry.get().strip())
        telefono = sanitize_text(self.telefono_entry.get().strip())
        email = sanitize_text(self.email_entry.get().strip())
        estado_pago = self.estado_pago_combo.get()
        
        if not nombre or not apellido:
            messagebox.showerror("Error", "Nombre y apellido son obligatorios")
            return
        
        # Validar formato de email si se proporciona
        if email and not re.match(r'^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$', email):
            messagebox.showerror("Error", "Formato de email inválido")
            return
        
        # Validar formato de teléfono si se proporciona
        if telefono and not re.match(r'^[\\+]?[\\d\\s\\-\\(\\)]+$', telefono):
            messagebox.showerror("Error", "Formato de teléfono inválido")
            return
        
        try:
            codigo_barras = self.barcode_manager.generar_codigo()
            user_id = self.db.agregar_usuario(codigo_barras, nombre, apellido, telefono, email, estado_pago)
            
            if user_id:
                self.barcode_manager.generar_imagen_codigo(codigo_barras, f"{nombre}_{apellido}")
                messagebox.showinfo("Éxito", f"Usuario registrado exitosamente\\nCódigo: {codigo_barras}")
                self.limpiar_campos()
                self.cargar_usuarios()
                self.actualizar_estadisticas()
            else:
                messagebox.showerror("Error", "Error al registrar usuario. Posible código duplicado.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar usuario: {str(e)}")
    
    def limpiar_campos(self):
        """Limpiar todos los campos del formulario"""
        self.nombre_entry.delete(0, 'end')
        self.apellido_entry.delete(0, 'end')
        self.telefono_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
        self.estado_pago_combo.set('pendiente')
        self.nombre_entry.focus()
    
    def cargar_usuarios(self):
        """Cargar lista de usuarios en el treeview"""
        # Limpiar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            usuarios = self.db.obtener_todos_usuarios()
            for usuario in usuarios:
                user_id, codigo, nombre, apellido, telefono, email, estado_pago, fecha_registro = usuario
                
                # Formatear fecha
                if isinstance(fecha_registro, str):
                    fecha_str = fecha_registro[:10]  # Solo la fecha
                else:
                    fecha_str = fecha_registro.strftime('%Y-%m-%d')
                
                # Sanitizar datos
                nombre = sanitize_text(nombre)
                apellido = sanitize_text(apellido)
                telefono = sanitize_text(telefono) if telefono else ""
                email = sanitize_text(email) if email else ""
                
                self.tree.insert('', 'end', values=(
                    user_id, codigo, nombre, apellido, telefono, email, estado_pago, fecha_str
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar usuarios: {str(e)}")
    
    def filtrar_usuarios(self, event=None):
        """Filtrar usuarios según búsqueda y estado"""
        # Limpiar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            usuarios = self.db.obtener_todos_usuarios()
            busqueda = self.busqueda_texto.get().lower()
            estado_filtro = self.filtro_estado.get()
            
            for usuario in usuarios:
                user_id, codigo, nombre, apellido, telefono, email, estado_pago, fecha_registro = usuario
                
                # Aplicar filtro de estado
                if estado_filtro != "todos" and estado_pago != estado_filtro:
                    continue
                
                # Aplicar filtro de búsqueda
                if busqueda:
                    texto_busqueda = f"{nombre} {apellido} {codigo} {telefono or ''} {email or ''}".lower()
                    if busqueda not in texto_busqueda:
                        continue
                
                # Formatear fecha
                if isinstance(fecha_registro, str):
                    fecha_str = fecha_registro[:10]
                else:
                    fecha_str = fecha_registro.strftime('%Y-%m-%d')
                
                # Sanitizar datos
                nombre = sanitize_text(nombre)
                apellido = sanitize_text(apellido)
                telefono = sanitize_text(telefono) if telefono else ""
                email = sanitize_text(email) if email else ""
                
                self.tree.insert('', 'end', values=(
                    user_id, codigo, nombre, apellido, telefono, email, estado_pago, fecha_str
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Error al filtrar usuarios: {str(e)}")
    
    def obtener_usuario_seleccionado(self):
        """Obtener el usuario seleccionado en el treeview"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Por favor seleccione un usuario")
            return None
        
        item = self.tree.item(selection[0])
        return item['values']
    
    def marcar_pagado(self):
        """Marcar usuario como pagado"""
        usuario = self.obtener_usuario_seleccionado()
        if not usuario:
            return
        
        try:
            self.db.actualizar_estado_pago(usuario[0], 'pagado')
            messagebox.showinfo("Éxito", f"Usuario {usuario[2]} {usuario[3]} marcado como PAGADO")
            self.cargar_usuarios()
            self.actualizar_estadisticas()
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar estado: {str(e)}")
    
    def marcar_sin_pago(self):
        """Marcar usuario sin pago"""
        usuario = self.obtener_usuario_seleccionado()
        if not usuario:
            return
        
        try:
            self.db.actualizar_estado_pago(usuario[0], 'pendiente')
            messagebox.showinfo("Éxito", f"Usuario {usuario[2]} {usuario[3]} marcado como SIN PAGO")
            self.cargar_usuarios()
            self.actualizar_estadisticas()
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar estado: {str(e)}")
    
    def imprimir_codigo(self):
        """Regenerar e imprimir código de barras"""
        usuario = self.obtener_usuario_seleccionado()
        if not usuario:
            return
        
        try:
            codigo = usuario[1]
            nombre = usuario[2]
            apellido = usuario[3]
            
            # Regenerar imagen del código
            self.barcode_manager.generar_imagen_codigo(codigo, f"{nombre}_{apellido}")
            
            # Abrir carpeta de códigos
            carpeta_codigos = os.path.abspath("barcodes")
            if os.path.exists(carpeta_codigos):
                os.startfile(carpeta_codigos)  # Windows
                messagebox.showinfo("Éxito", f"Código regenerado para {nombre} {apellido}\\nCarpeta abierta: barcodes/")
            else:
                messagebox.showerror("Error", "Carpeta de códigos no encontrada")
        except Exception as e:
            messagebox.showerror("Error", f"Error al regenerar código: {str(e)}")
    
    def editar_usuario(self):
        """Editar datos del usuario seleccionado"""
        usuario = self.obtener_usuario_seleccionado()
        if not usuario:
            return
        
        # Crear ventana de edición
        edit_window = tk.Toplevel(self.window)
        edit_window.title(f"Editar Usuario - {usuario[2]} {usuario[3]}")
        edit_window.geometry("400x300")
        edit_window.configure(bg="#000000")
        edit_window.transient(self.window)
        edit_window.grab_set()
        
        # TODO: Implementar formulario de edición completo
        tk.Label(edit_window, text="Función de edición en desarrollo", 
                bg="#000000", fg="#FF8C00", font=('Arial', 14)).pack(pady=50)
        
        tk.Button(edit_window, text="Cerrar", command=edit_window.destroy,
                 bg="#FF8C00", fg="#000000").pack(pady=20)
    
    def eliminar_usuario(self):
        """Eliminar usuario (desactivar)"""
        usuario = self.obtener_usuario_seleccionado()
        if not usuario:
            return
        
        respuesta = messagebox.askyesno("Confirmar", 
                                      f"¿Está seguro de eliminar al usuario {usuario[2]} {usuario[3]}?\\n\\n"
                                      "Esta acción desactivará al usuario pero mantendrá su historial.")
        
        if respuesta:
            try:
                # TODO: Implementar desactivación de usuario
                messagebox.showinfo("Info", "Función de eliminación en desarrollo")
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar usuario: {str(e)}")
    
    def actualizar_estadisticas(self):
        """Actualizar estadísticas en tiempo real"""
        # Limpiar frame de estadísticas
        for widget in self.stats_frame_content.winfo_children():
            widget.destroy()
        
        try:
            # Obtener datos
            usuarios = self.db.obtener_todos_usuarios()
            accesos_hoy = self.db.obtener_accesos_hoy()
            
            total_usuarios = len(usuarios)
            usuarios_pagados = len([u for u in usuarios if u[6] == 'pagado'])
            usuarios_pendientes = len([u for u in usuarios if u[6] == 'pendiente'])
            accesos_hoy_count = len(accesos_hoy)
            
            # Mostrar estadísticas
            stats = [
                ("👥 Total Usuarios", total_usuarios, "#0066CC"),
                ("💳 Usuarios Pagados", usuarios_pagados, "#00AA00"),
                ("❌ Usuarios Pendientes", usuarios_pendientes, "#CC0000"),
                ("🚪 Accesos Hoy", accesos_hoy_count, "#FF8C00")
            ]
            
            for i, (label, valor, color) in enumerate(stats):
                frame = tk.Frame(self.stats_frame_content, bg=color, relief='raised', bd=2)
                frame.grid(row=0, column=i, padx=10, pady=5, ipadx=20, ipady=10)
                
                tk.Label(frame, text=label, bg=color, fg="white", 
                        font=('Arial', 10, 'bold')).pack()
                tk.Label(frame, text=str(valor), bg=color, fg="white", 
                        font=('Arial', 16, 'bold')).pack()
                
        except Exception as e:
            tk.Label(self.stats_frame_content, text=f"Error al cargar estadísticas: {str(e)}", 
                    bg="#FF8C00", fg="#000000").pack()
    
    def cargar_accesos_recientes(self):
        """Cargar accesos recientes"""
        # Limpiar treeview de accesos
        for item in self.accesos_tree.get_children():
            self.accesos_tree.delete(item)
        
        try:
            accesos = self.db.obtener_accesos_hoy()
            for acceso in accesos[-20:]:  # Últimos 20 accesos
                nombre, apellido, tipo, fecha_hora = acceso
                nombre_completo = f"{sanitize_text(nombre)} {sanitize_text(apellido)}"
                
                # Formatear fecha/hora
                if isinstance(fecha_hora, str):
                    fecha_str = fecha_hora
                else:
                    fecha_str = fecha_hora.strftime('%Y-%m-%d %H:%M:%S')
                
                # Color según tipo
                if tipo == 'entrada':
                    self.accesos_tree.insert('', 0, values=(nombre_completo, "🟢 ENTRADA", fecha_str))
                else:
                    self.accesos_tree.insert('', 0, values=(nombre_completo, "🔴 SALIDA", fecha_str))
                    
        except Exception as e:
            print(f"Error al cargar accesos: {e}")
    
    def auto_refresh(self):
        """Auto-actualizar datos cada 30 segundos"""
        self.actualizar_estadisticas()
        self.cargar_accesos_recientes()
        self.window.after(30000, self.auto_refresh)  # 30 segundos
    
    # Métodos de reportes (implementación básica)
    def generar_reporte_diario(self):
        try:
            archivo = self.reports_manager.generar_reporte_diario()
            messagebox.showinfo("Éxito", f"Reporte diario generado: {archivo}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")
    
    def generar_reporte_semanal(self):
        messagebox.showinfo("Info", "Función en desarrollo")
    
    def generar_reporte_mensual(self):
        messagebox.showinfo("Info", "Función en desarrollo")
    
    def generar_reporte_sin_pago(self):
        messagebox.showinfo("Info", "Función en desarrollo")
    
    def generar_reporte_pagados(self):
        messagebox.showinfo("Info", "Función en desarrollo")
    
    def generar_estadisticas_completas(self):
        messagebox.showinfo("Info", "Función en desarrollo")
    
    # Métodos de configuración
    def verificar_conexion_db(self):
        try:
            self.db.get_connection().close()
            messagebox.showinfo("Éxito", "✅ Conexión a MySQL exitosa")
        except Exception as e:
            messagebox.showerror("Error", f"❌ Error de conexión: {str(e)}")
    
    def reinicializar_tablas(self):
        respuesta = messagebox.askyesno("ADVERTENCIA", 
                                      "⚠️ Esto eliminará TODOS los datos.\\n¿Está completamente seguro?")
        if respuesta:
            messagebox.showinfo("Info", "Función de reinicialización en desarrollo")
    
    def cargar_configuracion_sms(self):
        try:
            sms_enabled = self.db.obtener_configuracion('sms_enabled')
            admin_phone = self.db.obtener_configuracion('admin_phone')
            
            self.sms_enabled_var.set("1" if sms_enabled == 'true' else "0")
            if admin_phone:
                self.admin_phone_entry.insert(0, admin_phone)
        except Exception as e:
            print(f"Error cargando configuración SMS: {e}")
    
    def guardar_config_sms(self):
        messagebox.showinfo("Info", "Función de configuración SMS en desarrollo")
    
    # Métodos de respaldo
    def crear_respaldo(self):
        messagebox.showinfo("Info", "Función de respaldo en desarrollo")
    
    def abrir_carpeta_respaldos(self):
        messagebox.showinfo("Info", "Función en desarrollo")
    
    def limpiar_accesos_antiguos(self):
        messagebox.showinfo("Info", "Función en desarrollo")
    
    def optimizar_database(self):
        messagebox.showinfo("Info", "Función en desarrollo")