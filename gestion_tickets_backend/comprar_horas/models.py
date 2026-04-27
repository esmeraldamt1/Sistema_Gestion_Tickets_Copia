from mongoengine import Document, ReferenceField, IntField, FloatField, DateTimeField
from mongoengine import Document, ReferenceField, FloatField, DateTimeField
from django.utils.timezone import now
from usuarios.models import Usuario

class CompraHoras(Document):
    usuario = ReferenceField(Usuario, required=True)
    cantidad_horas = FloatField(required=True)
    valor_por_hora = FloatField(required=True)
    total_pagado = FloatField()
    fecha_compra = DateTimeField(default=now)

    meta = {
        'collection': 'compras_horas',
        'ordering': ['-fecha_compra']
    }
