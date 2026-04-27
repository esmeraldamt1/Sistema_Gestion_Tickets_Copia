from django.db import models
from mongoengine import Document, StringField, DateTimeField, ReferenceField
from django.utils.timezone import now
from usuarios.models import Usuario 

class SolicitudSoporte(Document):
    # Campo que hace referencia al usuario que crea la solicitud (relación con el modelo Usuario)
    usuario = ReferenceField(Usuario, required=True)  
    
    # Asunto de la solicitud de soporte (campo obligatorio)
    asunto = StringField(max_length=255, required=True)
    
    # Mensaje que describe el problema o solicitud (campo obligatorio)
    mensaje = StringField(required=True)
    
    # Fecha de creación de la solicitud (valor predeterminado es la fecha y hora actuales)
    fecha_creacion = DateTimeField(default=now)
    
    # Estado de la solicitud, puede ser "pendiente", "en progreso" o "resuelto" (por defecto es "pendiente")
    estado = StringField(choices=["pendiente", "en progreso", "resuelto"], default="pendiente")

    # Metadatos del modelo: colección de MongoDB y orden por fecha de creación descendente
    meta = {
        'collection': 'solicitudes_soporte',  # Nombre de la colección en MongoDB
        'ordering': ['-fecha_creacion']  # Ordenar las solicitudes de soporte por fecha de creación, de más reciente a más antigua
    }

