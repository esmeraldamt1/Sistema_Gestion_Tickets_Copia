# Importamos el módulo de serialización de Django REST Framework
from rest_framework import serializers

# Definimos una clase de serializador personalizada para reportes básicos
class ReporteBasicoSerializer(serializers.Serializer):
    """
    Serializador para reportes generales de tickets.
    Incluye datos relevantes para análisis y métricas.
    """

    # Campo personalizado que convierte el ObjectId a string legible
    id = serializers.SerializerMethodField()

    # Campo del nombre del solicitante (se espera un string)
    solicitante = serializers.CharField()

    # Campo del nombre del departamento (string)
    departamento = serializers.CharField()

    # Fecha en la que fue creado el ticket
    fecha_creacion = serializers.DateTimeField()

    # Fecha en la que se resolvió el ticket (puede ser null)
    fecha_resolucion = serializers.DateTimeField(allow_null=True)

    # Título o asunto del ticket
    asunto = serializers.CharField()

    # Tipo del ticket (ej: problema, incidente, consulta, etc.)
    tipo_ticket = serializers.CharField()

    # Estado actual del ticket (ej: Abierto, Cerrado)
    estado_ticket = serializers.CharField()

    # Nivel de prioridad del ticket (ej: Alta, Media, Baja)
    prioridad = serializers.CharField()

    # Método para obtener el valor del campo `id`
    def get_id(self, obj):
        """
        Convierte el ObjectId de MongoDB a string.
        Esto es necesario porque ObjectId no es serializable por defecto en JSON.
        """
        return str(obj.get('_id'))
