# Importamos los campos y tipos de documentos de mongoengine
from mongoengine import Document, StringField, DateTimeField, ReferenceField, FileField

# Importamos datetime para manejar fechas y horas
from datetime import datetime

# Importamos los modelos relacionados
from usuarios.models import Usuario
from departamentos.models import Departamento

# Definimos el modelo Ticket que representa un ticket de soporte o solicitud
class Ticket(Document):
    # Título o asunto del ticket
    asunto = StringField(required=True)
    
    # Descripción del problema o solicitud
    descripcion = StringField(required=True)

    # Tipo de ticket (por ejemplo: problema, consulta, incidente, etc.)
    tipo_ticket = StringField(required=True)

    # Estado actual del ticket (por ejemplo: abierto, cerrado, en proceso)
    estado_ticket = StringField(required=True)

    # Nivel de prioridad del ticket (por ejemplo: alta, media, baja)
    prioridad = StringField(required=True)

    # Fecha y hora en que se creó el ticket (por defecto es la fecha y hora actual)
    fecha_creacion = DateTimeField(default=datetime.utcnow)

    # Fecha y hora en que se resolvió el ticket (puede estar vacía inicialmente)
    fecha_resolucion = DateTimeField(null=True)

    # Fecha y hora de la última actualización del ticket (para ordenamiento y seguimiento)
    fecha_actualizacion = DateTimeField(default=datetime.utcnow)

    # Archivo adjunto (por ejemplo, una imagen o PDF relacionado con el ticket)
    archivo = FileField(null=True)

    # Referencia al usuario que creó o reportó el ticket (obligatorio)
    solicitante = ReferenceField(Usuario, required=True)

    # Referencia al usuario asignado para resolver el ticket (puede ser null al inicio)
    asignado = ReferenceField(Usuario, null=True)

    # Referencia al departamento responsable del ticket (obligatorio)
    departamento = ReferenceField(Departamento, required=True)

    # Sobrescribimos el método save para actualizar automáticamente la fecha_actualizacion
    def save(self, *args, **kwargs):
        self.fecha_actualizacion = datetime.utcnow()  # Actualiza a la hora actual
        return super(Ticket, self).save(*args, **kwargs)  # Llama al método original de guardado

    # Representación legible del ticket como cadena (útil para logs y paneles de administración)
    def __str__(self):
        return f"[{self.tipo_ticket}] {self.asunto}"
