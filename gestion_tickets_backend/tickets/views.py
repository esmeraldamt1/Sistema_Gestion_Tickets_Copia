# Importaciones necesarias desde DRF
from rest_framework import status                             # Códigos de estado HTTP
from rest_framework.response import Response                 # Para construir respuestas HTTP
from rest_framework.permissions import IsAuthenticated       # Para restringir acceso a usuarios autenticados
from rest_framework.decorators import action                 # Para crear endpoints personalizados en el ViewSet
from rest_framework.viewsets import ModelViewSet             # ViewSet que implementa CRUD completo

# Importación de modelos y lógica de negocio del proyecto
from tickets.models import Ticket                            # Modelo de Ticket
from tickets.serializers import TicketSerializer             # Serializer para el modelo Ticket
from usuarios.models import Usuario                          # Modelo de Usuario
from departamentos.models import Departamento                # Modelo de Departamento
from tickets.services import asignar_usuarios_a_tickets      # Servicio de asignación automática de tickets

# ViewSet principal que gestiona todas las operaciones sobre tickets
class TicketViewSet(ModelViewSet):
    """
    ViewSet que permite:
    - Listar, crear, actualizar y eliminar tickets
    - Asignación automática o manual de usuarios
    """
    queryset = Ticket.objects.all().order_by('-fecha_actualizacion')  # Tickets ordenados por última actualización
    serializer_class = TicketSerializer                               # Serializer que define la representación de los datos
    permission_classes = [IsAuthenticated]                            # Solo usuarios autenticados pueden acceder

    # POST /tickets/ → Crear un nuevo ticket
    def create(self, request):
        data = request.data.copy()  # Copiamos el request data para poder modificarlo

        # Validar el solicitante
        try:
            solicitante = Usuario.objects.get(pk=data['solicitante'])
        except Usuario.DoesNotExist:
            return Response({"error": "Solicitante no válido"}, status=status.HTTP_400_BAD_REQUEST)

        # Validar el asignado si fue proporcionado
        asignado = None
        if 'asignado' in data and data['asignado']:
            try:
                asignado = Usuario.objects.get(pk=data['asignado'])
            except Usuario.DoesNotExist:
                return Response({"error": "Asignado no válido"}, status=status.HTTP_400_BAD_REQUEST)

        # Validar el departamento
        try:
            departamento = Departamento.objects.get(pk=data['departamento'])
        except Departamento.DoesNotExist:
            return Response({"error": "Departamento no válido"}, status=status.HTTP_400_BAD_REQUEST)

        # Crear el ticket con los datos validados
        ticket = Ticket(
            asunto=data['asunto'],
            descripcion=data['descripcion'],
            tipo_ticket=data['tipo_ticket'],
            estado_ticket=data.get('estado_ticket', 'Abierto'),
            prioridad=data['prioridad'],
            solicitante=solicitante,
            asignado=asignado,
            departamento=departamento,
            archivo=data.get('archivo', None),
        )
        ticket.save()  # Guardar en base de datos

        # Serializar y devolver el ticket creado
        serializer = TicketSerializer(ticket)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # DELETE /tickets/<id>/ → Eliminar un ticket y devolver confirmación
    def destroy(self, request, pk=None):
        try:
            ticket = Ticket.objects.get(pk=pk)  # Buscar el ticket por ID
        except Ticket.DoesNotExist:
            return Response({"error": "Ticket no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        ticket.delete()  # Eliminar el ticket
        return Response({"mensaje": "Ticket eliminado con éxito"}, status=status.HTTP_200_OK)

    # POST /tickets/<id>/asignar_usuario/ → Asignar un usuario manualmente
    @action(detail=True, methods=['post'])
    def asignar_usuario(self, request, pk=None):
        try:
            ticket = Ticket.objects.get(pk=pk)  # Buscar ticket por ID
        except Ticket.DoesNotExist:
            return Response({'error': 'Ticket no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        asignado_id = request.data.get('asignado')  # Obtener ID del usuario a asignar
        if not asignado_id:
            return Response({'error': 'Debe proporcionar el ID del usuario a asignar.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            usuario = Usuario.objects.get(pk=asignado_id)  # Buscar usuario
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        ticket.asignado = usuario  # Asignar el usuario al ticket
        ticket.save()              # Guardar cambios

        return Response({'message': f'Usuario {usuario.nombre} asignado correctamente al ticket.'}, status=status.HTTP_200_OK)

    # POST /tickets/asignacion_automatica/ → Asignar automáticamente a los tickets sin asignar
    @action(detail=False, methods=['post'])
    def asignacion_automatica(self, request):
        resultado = asignar_usuarios_a_tickets()  # Ejecuta lógica de asignación round-robin
        return Response({"mensaje": resultado})   # Devuelve mensaje de resultado
