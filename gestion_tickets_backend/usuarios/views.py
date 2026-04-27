"""
gestion_tickets_backend/usuarios/views.py

"""

# Importaciones estándar de Django
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
import os
import bcrypt
import secrets
from datetime import datetime, timedelta, timezone

# Importaciones de Django REST Framework
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import JSONParser

# Importamos el modelo personalizado de usuario (MongoEngine)
from .models import Usuario


# Vista simple para verificar que el servidor responde correctamente
def index(request):
    # Retorna un JSON con mensaje de bienvenida
    return JsonResponse({"message": "Bienvenido al Sistema de Gestión de Tickets"}, safe=False)


# Enviar enlace de recuperación de contraseña
@api_view(['POST'])  # Permite solo solicitudes POST
@permission_classes([AllowAny])  # No requiere autenticación
def enviar_enlace_recuperacion(request):
    """
    Envía un correo con un enlace único para restablecer la contraseña.
    """
    try:
        # Obtiene el correo desde el cuerpo de la solicitud, acepta "correo" o "email"
        correo = request.data.get("correo") or request.data.get("email")
        if not correo:
            return Response({"error": "Debes proporcionar un correo electrónico."}, status=400)

        # Busca al usuario por correo electrónico
        usuario = Usuario.objects.get(email=correo)

        # Genera un token seguro y calcula tiempo de expiración a 15 minutos en UTC
        token = secrets.token_urlsafe(32)
        expiracion = datetime.now(timezone.utc) + timedelta(minutes=15)

        # Guarda el token y la expiración en el usuario
        usuario.reset_token = token
        usuario.reset_token_expires = expiracion
        usuario.save()

        # Construye el enlace para restablecer la contraseña, con el token
        enlace = f"http://localhost:5173/reset-password/{token}/"

        # Envía el correo con asunto, mensaje y destinatario
        send_mail(
            subject='Recupera tu contraseña',
            message=f'Haz clic en el siguiente enlace para restablecer tu contraseña:\n{enlace}',
            from_email=os.getenv('EMAIL_HOST_USER', settings.DEFAULT_FROM_EMAIL),
            recipient_list=[correo],
            fail_silently=False,
        )

        # Retorna respuesta exitosa
        return Response({'mensaje': 'Correo enviado con éxito'}, status=200)

    except Usuario.DoesNotExist:
        # Si no encuentra el usuario con ese correo
        return Response({'error': 'El correo no está registrado'}, status=404)
    except Exception as e:
        # Para cualquier otro error
        return Response({'error': f'Error interno: {str(e)}'}, status=500)


# Cambiar contraseña con token recibido por correo
@api_view(['POST'])  # Solo POST
@permission_classes([AllowAny])  # Sin autenticación requerida
@parser_classes([JSONParser])  # Parsing JSON explícito
def cambiar_contrasena(request, token):
    """
    Cambia la contraseña si el token es válido y no ha expirado.
    """
    try:
        # Obtiene la nueva contraseña desde el request
        nueva = request.data.get("nueva_contrasena")
        if not nueva:
            return Response({"error": "Debes proporcionar una nueva contraseña"}, status=400)

        # Busca al usuario que tenga el token enviado
        usuario = Usuario.objects.get(reset_token=token)
        token_expira = usuario.reset_token_expires

        # Si no hay fecha de expiración, token inválido o expirado
        if token_expira is None:
            return Response({"error": "El enlace ha expirado"}, status=400)

        # Asegura que token_expira tenga zona horaria (UTC)
        if token_expira.tzinfo is None or token_expira.tzinfo.utcoffset(token_expira) is None:
            token_expira = token_expira.replace(tzinfo=timezone.utc)

        # Verifica si el token expiró comparando con la fecha actual UTC
        if token_expira < datetime.now(timezone.utc):
            return Response({"error": "El enlace ha expirado"}, status=400)

        # Hashea la nueva contraseña con bcrypt
        hashed = bcrypt.hashpw(nueva.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Actualiza la contraseña y limpia los campos del token
        usuario.password = hashed
        usuario.reset_token = None
        usuario.reset_token_expires = None
        usuario.save()

        # Respuesta exitosa
        return Response({"mensaje": "Contraseña actualizada con éxito"}, status=200)

    except Usuario.DoesNotExist:
        # Token inválido porque no se encontró usuario con ese token
        return Response({"error": "Token inválido"}, status=404)
    except Exception as e:
        # Para cualquier otro error
        return Response({'error': f'Error interno: {str(e)}'}, status=500)


# Registrar nuevo usuario
@api_view(['POST'])
@permission_classes([AllowAny])
@parser_classes([JSONParser])
def register(request):
    """
    Crea un nuevo usuario con rol predeterminado 'solicitante'.
    """
    try:
        data = request.data
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        rol = data.get('rol', 'solicitante').lower()  # Por defecto 'solicitante'

        # Verifica que los campos obligatorios estén presentes
        if not username or not email or not password:
            return Response({'error': 'Faltan datos obligatorios'}, status=400)

        # Verifica que el username no exista ya
        if Usuario.objects(username=username).first():
            return Response({'error': 'El nombre de usuario ya existe'}, status=400)

        # Verifica que el email no esté registrado
        if Usuario.objects(email=email).first():
            return Response({'error': 'El correo ya está registrado'}, status=400)

        # Hashea la contraseña antes de guardar
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Crea el usuario con los datos
        usuario = Usuario(username=username, email=email, password=hashed_password, rol=rol)
        usuario.save()

        # Devuelve mensaje de éxito y el ID del nuevo usuario
        return Response({'message': 'Usuario registrado con éxito', 'id': str(usuario.id)}, status=201)

    except Exception as e:
        # Captura errores generales
        return Response({'error': f'Error interno: {str(e)}'}, status=500)


# Login de usuario con JWT (access + refresh)
@api_view(['POST'])
@permission_classes([AllowAny])
@parser_classes([JSONParser])
def login_view(request):
    """
    Autentica al usuario y devuelve JWT tokens junto con datos básicos del usuario.
    """
    try:
        data = request.data
        username = data.get('username')
        password = data.get('password')

        # Busca usuario por username
        usuario = Usuario.objects(username=username).first()

        # Verifica si usuario existe y si la contraseña coincide (bcrypt)
        if not usuario or not bcrypt.checkpw(password.encode('utf-8'), usuario.password.encode('utf-8')):
            return Response({'error': 'Credenciales inválidas'}, status=401)

        # Genera tokens JWT usando Simple JWT
        refresh = RefreshToken.for_user(usuario)

        # Devuelve tokens y datos básicos del usuario
        return Response({
            'message': 'Inicio de sesión exitoso',
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user': {
                'id': str(usuario.id),
                'username': usuario.username,
                'email': usuario.email,
                'rol': usuario.rol
            }
        }, status=200)

    except Exception as e:
        return Response({'error': f'Error interno: {str(e)}'}, status=500)


# ViewSet para CRUD de usuarios
class UsuarioViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]  # Requiere que el usuario esté autenticado

    def list(self, request):
        # Obtiene todos los usuarios, solo con campos seleccionados para optimizar consulta
        usuarios = Usuario.objects.only('id', 'username', 'email', 'rol')
        # Construye lista de diccionarios con datos serializados manualmente
        data = [{'id': str(u.id), 'username': u.username, 'email': u.email, 'rol': u.rol} for u in usuarios]
        return Response(data, status=200)

    def retrieve(self, request, pk=None):
        # Busca usuario por ID
        usuario = Usuario.objects(id=pk).first()
        if not usuario:
            return Response({'error': 'Usuario no encontrado'}, status=404)
        # Devuelve datos del usuario
        return Response({
            'id': str(usuario.id),
            'username': usuario.username,
            'email': usuario.email,
            'rol': usuario.rol
        }, status=200)

    def update(self, request, pk=None):
        # Busca usuario por ID
        usuario = Usuario.objects(id=pk).first()
        if not usuario:
            return Response({'error': 'Usuario no encontrado'}, status=404)

        # Actualiza email y rol si se envían, sino mantiene valores previos
        usuario.email = request.data.get('email', usuario.email)
        usuario.rol = request.data.get('rol', usuario.rol)
        usuario.save()

        return Response({'message': 'Usuario actualizado con éxito', 'id': str(usuario.id)}, status=200)

    def destroy(self, request, pk=None):
        # Busca usuario por ID
        usuario = Usuario.objects(id=pk).first()
        if not usuario:
            return Response({'error': 'Usuario no encontrado'}, status=404)

        # Elimina el usuario
        usuario.delete()
        return Response({'message': 'Usuario eliminado con éxito'}, status=200)


# ViewSet para listar usuarios con rol "agente"
class AgentesViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder

    def list(self, request):
        # Obtiene usuarios con rol "agente", solo campos necesarios
        agentes = Usuario.objects(rol="agente").only('id', 'username')
        # Serializa a lista de diccionarios con id y username
        data = [{'id': str(a.id), 'username': a.username} for a in agentes]
        return Response(data, status=200)


# ViewSet para listar usuarios con rol "solicitante"
class SolicitantesViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder

    def list(self, request):
        # Obtiene usuarios con rol "solicitante", solo campos necesarios
        solicitantes = Usuario.objects(rol="solicitante").only('id', 'username')
        # Serializa a lista de diccionarios con id y username
        data = [{'id': str(s.id), 'username': s.username} for s in solicitantes]
        return Response(data, status=200)
