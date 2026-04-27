# Importamos las clases necesarias para construir serializers
from rest_framework import serializers

# Importamos datetime para convertir fechas en formato string
from datetime import datetime

# Importamos los modelos utilizados en este serializer
from tickets.models import Ticket
from usuarios.models import Usuario
from departamentos.models import Departamento

# Serializer personalizado para el modelo Ticket
class TicketSerializer(serializers.Serializer):
    # ID del ticket (solo lectura)
    id = serializers.CharField(read_only=True)

    # Campos de texto obligatorios
    asunto = serializers.CharField()
    descripcion = serializers.CharField()
    tipo_ticket = serializers.CharField()
    estado_ticket = serializers.CharField()
    prioridad = serializers.CharField()

    # Fechas (algunas son opcionales o pueden ser nulas)
    fecha_creacion = serializers.DateTimeField(required=False)
    fecha_actualizacion = serializers.DateTimeField(required=False)
    fecha_resolucion = serializers.DateTimeField(required=False, allow_null=True)

    # Campo para archivos (puede ser nulo u opcional)
    archivo = serializers.FileField(required=False, allow_null=True)

    # Relaciones: se reciben como strings (ID)
    solicitante = serializers.CharField()                             # ID del solicitante
    asignado = serializers.CharField(allow_null=True, required=False) # ID del asignado (puede ser nulo)
    departamento = serializers.CharField()                            # ID del departamento

    # Método para crear un nuevo Ticket
    def create(self, validated_data):
        # Buscar instancia del solicitante
        solicitante = Usuario.objects.get(id=validated_data['solicitante'])

        # Buscar asignado si fue proporcionado
        asignado = None
        if validated_data.get('asignado'):
            asignado = Usuario.objects.get(id=validated_data['asignado'])

        # Buscar departamento
        departamento = Departamento.objects.get(id=validated_data['departamento'])

        # Crear la instancia del ticket
        ticket = Ticket(
            asunto=validated_data['asunto'],
            descripcion=validated_data['descripcion'],
            tipo_ticket=validated_data['tipo_ticket'],
            estado_ticket=validated_data['estado_ticket'],
            prioridad=validated_data['prioridad'],
            solicitante=solicitante,
            asignado=asignado,
            departamento=departamento,
            archivo=validated_data.get('archivo'),
            fecha_resolucion=validated_data.get('fecha_resolucion')
        )

        ticket.save()  # Guardar en la base de datos
        return ticket  # Retornar el nuevo ticket creado

    # Método para actualizar un ticket existente
    def update(self, instance, validated_data):
        # Obtener el request desde el contexto para acceder a los archivos
        request = self.context.get('request')

        # Actualizar campos simples si se proporcionaron
        instance.asunto = validated_data.get('asunto', instance.asunto)
        instance.descripcion = validated_data.get('descripcion', instance.descripcion)
        instance.tipo_ticket = validated_data.get('tipo_ticket', instance.tipo_ticket)
        instance.estado_ticket = validated_data.get('estado_ticket', instance.estado_ticket)
        instance.prioridad = validated_data.get('prioridad', instance.prioridad)

        # Revisar si se recibió un archivo en el request y asignarlo
        if request and request.FILES.get('archivo'):
            print(">> Archivos recibidos:", self.context['request'].FILES)
            instance.archivo = request.FILES['archivo']

        # Intentar convertir la fecha de resolución a datetime si viene como string
        fecha_str = validated_data.get("fecha_resolucion")
        if fecha_str:
            try:
                if isinstance(fecha_str, str):
                    instance.fecha_resolucion = datetime.strptime(fecha_str, "%Y-%m-%d")
                else:
                    instance.fecha_resolucion = fecha_str
            except Exception:
                pass  # Ignora errores de formato

        # Actualizar relaciones externas

        # Solicitante
        if 'solicitante' in validated_data:
            instance.solicitante = Usuario.objects.get(id=validated_data['solicitante'])

        # Asignado (puede ser nulo o vacío)
        if 'asignado' in validated_data:
            asignado_id = validated_data.get('asignado')
            if asignado_id:
                instance.asignado = Usuario.objects.get(id=asignado_id)
            else:
                instance.asignado = None

        # Departamento
        if 'departamento' in validated_data:
            instance.departamento = Departamento.objects.get(id=validated_data['departamento'])

        instance.save()  # Guardar cambios en base de datos
        return instance  # Retornar el ticket actualizado

    # Método para definir cómo se representa un Ticket al devolverlo al frontend
    def to_representation(self, instance):
        return {
            "id": str(instance.id),  # ID en formato string
            "asunto": instance.asunto,
            "descripcion": instance.descripcion,
            "tipo_ticket": instance.tipo_ticket,
            "estado_ticket": instance.estado_ticket,
            "prioridad": instance.prioridad,
            "fecha_creacion": instance.fecha_creacion,
            "fecha_actualizacion": instance.fecha_actualizacion,
            "fecha_resolucion": instance.fecha_resolucion,

            # Verificamos si el archivo tiene una URL (usando hasattr para evitar errores)
            "archivo": instance.archivo.url if instance.archivo and hasattr(instance.archivo, "url") else None,

            # Representación del solicitante como diccionario
            "solicitante": {
                "id": str(instance.solicitante.id),
                "nombre": instance.solicitante.username
            },

            # Representación del asignado si existe
            "asignado": {
                "id": str(instance.asignado.id),
                "nombre": instance.asignado.username
            } if instance.asignado else None,

            # Representación del departamento como diccionario
            "departamento": {
                "id": str(instance.departamento.id),
                "nombre": instance.departamento.nombre
            },
        }
