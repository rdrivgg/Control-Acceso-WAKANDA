import requests
from database import GymDatabase

class SMSManager:
    def __init__(self):
        self.db = GymDatabase()
        
    def enviar_alerta_no_pago(self, nombre, apellido, telefono_usuario=None):
        """Envía SMS de alerta cuando un usuario sin pago intenta acceder"""
        try:
            sms_enabled = self.db.obtener_configuracion('sms_enabled')
            if sms_enabled and sms_enabled.lower() == 'true':
                admin_phone = self.db.obtener_configuracion('admin_phone')
                
                if admin_phone:
                    mensaje = f"ALERTA WAKANDA GYM: Usuario {nombre} {apellido} intentó acceder sin pago. Tel: {telefono_usuario or 'N/A'}"
                    return self.enviar_sms(admin_phone, mensaje)
            
            print(f"ALERTA: {nombre} {apellido} intentó acceder sin pago")
            return True
            
        except Exception as e:
            print(f"Error al enviar SMS: {str(e)}")
            return False
    
    def enviar_sms(self, telefono, mensaje):
        """Función para enviar SMS usando un servicio (requiere configuración)"""
        try:
            # Aquí se integraría con un servicio de SMS como Twilio, Nexmo, etc.
            # Ejemplo con Twilio (requiere credenciales):
            # from twilio.rest import Client
            # client = Client(account_sid, auth_token)
            # message = client.messages.create(
            #     body=mensaje,
            #     from_='+1234567890',  # Número Twilio
            #     to=telefono
            # )
            
            # Por ahora, solo simula el envío
            print(f"SMS enviado a {telefono}: {mensaje}")
            return True
            
        except Exception as e:
            print(f"Error enviando SMS: {str(e)}")
            return False
    
    def configurar_sms(self, enabled=True, admin_phone=None):
        """Configura las opciones de SMS"""
        try:
            if admin_phone:
                # Actualizar teléfono del administrador
                pass
                
            # Habilitar/deshabilitar SMS
            self.db.configurar('sms_enabled', 'true' if enabled else 'false')
            return True
            
        except Exception as e:
            print(f"Error configurando SMS: {str(e)}")
            return False