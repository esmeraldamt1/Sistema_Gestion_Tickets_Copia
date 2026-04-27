""" 
gestion_tickets_backend/usuarios/authentication

Autenticación personalizada con JWT para MongoDB.
"""

from rest_framework.authentication import BaseAuthentication  #  Clase base para autenticación personalizada en DRF
from rest_framework.exceptions import AuthenticationFailed  #  Excepción para errores en autenticación
from rest_framework_simplejwt.tokens import AccessToken  #  Manejo de tokens JWT para validación y decodificación
from rest_framework_simplejwt.exceptions import TokenError  #  Excepción específica para errores en JWT
from .models import Usuario  #  Modelo Usuario para consulta en MongoDB
from bson import ObjectId  #  Para manejar IDs de MongoDB (aunque en este caso no es estrictamente necesario)


class MongoDBJWTAuthentication(BaseAuthentication):
    """
    Clase de autenticación personalizada que valida tokens JWT y autentica usuarios en MongoDB.
    """

    def authenticate(self, request):
        """
        Método principal que obtiene y valida el token JWT desde la cabecera Authorization.
        Si el token es válido, devuelve el usuario autenticado; si no, lanza AuthenticationFailed.
        """
        #  Obtenemos el valor de la cabecera Authorization
        auth_header = request.headers.get("Authorization")

        #  Validamos que la cabecera Authorization exista y tenga formato 'Bearer <token>'
        if not auth_header or not auth_header.startswith("Bearer "):
            return None  # No se encontró token, DRF continuará con otras autenticaciones si las hay

        #  Extraemos solo el token JWT quitando la palabra 'Bearer '
        token_str = auth_header.split(" ")[1]

        try:
            #  Decodificamos y validamos el token JWT
            access_token = AccessToken(token_str)

            #  Obtenemos el ID del usuario desde el payload del token
            user_id = access_token["user_id"]

            #  Buscamos el usuario en la base de datos MongoDB usando MongoEngine
            usuario = Usuario.objects(id=user_id).first()

            #  Si no existe el usuario con ese ID, lanzamos error de autenticación
            if not usuario:
                raise AuthenticationFailed("Usuario no encontrado")

            #  Retornamos el usuario autenticado y None para el token (DRF espera esta tupla)
            return usuario, None

        except (TokenError, KeyError):
            #  Si el token es inválido, ha expirado o falta el campo user_id, lanzamos error
            raise AuthenticationFailed("Token inválido o expirado")
        except Exception:
            #  Captura cualquier otro error inesperado y lanza error genérico de autenticación
            raise AuthenticationFailed("Error en autenticación con token JWT")
