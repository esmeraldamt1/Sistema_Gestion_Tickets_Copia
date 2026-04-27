from mongoengine import Document, ReferenceField, FloatField, DateTimeField, StringField
from django.utils.timezone import now
from usuarios.models import Usuario  

class Saldo(Document):
    usuario = ReferenceField(Usuario, required=True)
    saldo_actual = FloatField(default=0.0)
    fecha_actualizacion = DateTimeField(default=now)

    meta = {
        'collection': 'saldo',
        'ordering': ['-fecha_actualizacion']
    }

class MovimientoSaldo(Document):
    saldo = ReferenceField(Saldo, required=True)
    cambio = FloatField(required=True)  # Cambio en el saldo, positivo o negativo
    descripcion = StringField(default='')  # Descripción opcional del movimiento
    fecha = DateTimeField(default=now)

    meta = {
        'collection': 'movimientos_saldo',
        'ordering': ['-fecha']
    }
