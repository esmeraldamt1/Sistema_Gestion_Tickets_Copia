"""
gestion_tickets_backend/usuarios/models.py

Definición del modelo de Usuario utilizando MongoDB y MongoEngine.
"""

import mongoengine as me  # MongoEngine se usa como ODM para trabajar con MongoDB en Django
from datetime import datetime, timezone  # datetime y timezone permiten manejar fechas con zona horaria

# Definición del modelo de Usuario heredando de mongoengine.Document
class Usuario(me.Document):
    """
    Modelo de Usuario para autenticación y gestión usando MongoDB.
    """

    # Nombre de usuario único, obligatorio y con máximo 150 caracteres
    username = me.StringField(
        required=True,       # Campo obligatorio
        unique=True,         # Debe ser único en la colección
        max_length=150       # Longitud máxima permitida
    )

    # Correo electrónico único y obligatorio con validación automática de formato
    email = me.EmailField(
        required=True,       # Campo obligatorio
        unique=True          # No se permite repetir correos
    )

    # Contraseña del usuario, debe estar encriptada (hash) antes de almacenarse
    password = me.StringField(
        required=True        # Campo obligatorio
    )

    # Rol del usuario: puede ser "agente" o "solicitante", por defecto es "solicitante"
    rol = me.StringField(
        choices=["agente", "solicitante"],  # Valores válidos
        default="solicitante"               # Valor por defecto
    )

    # Fecha de creación del usuario (timezone-aware UTC)
    created_at = me.DateTimeField(
        default=lambda: datetime.now(timezone.utc)  # Fecha actual con zona horaria UTC
    )

    # Fecha de última modificación (timezone-aware UTC)
    updated_at = me.DateTimeField(
        default=lambda: datetime.now(timezone.utc)  # Fecha actual con zona horaria UTC
    )

    # Token usado para restablecimiento de contraseña (puede ser None)
    reset_token = me.StringField()

    # Fecha de expiración del token de recuperación de contraseña (timezone-aware)
    reset_token_expires = me.DateTimeField()

    # Metaopciones del documento (nombre de la colección en MongoDB)
    meta = {
        'collection': 'usuarios'  # Define el nombre de la colección en MongoDB
    }

    # Campo utilizado como identificador de usuario en autenticación (si se usa con Django)
    USERNAME_FIELD = "username"

    def is_authenticated(self):
        """
        Método para indicar si el usuario está autenticado.
        En esta implementación siempre devuelve True, útil si se desea integrar con middlewares.
        """
        return True

    def __str__(self):
        """
        Representación en forma de cadena del objeto Usuario.
        Retorna el nombre de usuario.
        """
        return self.username
