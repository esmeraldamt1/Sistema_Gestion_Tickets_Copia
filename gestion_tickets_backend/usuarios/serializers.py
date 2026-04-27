"""
Serializadores para el modelo Usuario en MongoDB.
"""

import re  #  Validaciones de contraseña con expresiones regulares
from rest_framework import serializers  #  Serializadores de Django REST Framework
import bcrypt  #  Para cifrar contraseñas de forma segura
from .models import Usuario  #  Modelo de Usuario en MongoEngine

class UsuarioSerializer(serializers.Serializer):
    """
    Serializador para manejar usuarios (lectura y escritura).
    """

    #  Campo especial para mostrar el ID como string (MongoDB usa ObjectId)
    id = serializers.CharField()

    #  Campos obligatorios
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    #  Campo para distinguir entre agentes y solicitantes
    rol = serializers.ChoiceField(choices=["agente", "solicitante"], default="solicitante")

    def get_id(self, obj):
        """
        Convierte el ObjectId de MongoDB a string.
        """
        return str(obj.id)

    def validate_password(self, value):
        """
        Valida la contraseña cumpliendo requisitos de seguridad.
        """
        if len(value) < 8:
            raise serializers.ValidationError("La contraseña debe tener al menos 8 caracteres.")

        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError("Debe incluir al menos una letra mayúscula.")

        if not re.search(r"[0-9]", value):
            raise serializers.ValidationError("Debe incluir al menos un número.")

        return value

    def create(self, validated_data):
        """
        Crea un nuevo usuario con contraseña cifrada.
        """
        validated_data["password"] = bcrypt.hashpw(
            validated_data["password"].encode('utf-8'), bcrypt.gensalt()
        ).decode('utf-8')

        validated_data["rol"] = validated_data["rol"].lower()  # Normalizamos el rol
        usuario = Usuario(**validated_data)
        usuario.save()
        return usuario

    def update(self, instance, validated_data):
        """
        Actualiza los campos del usuario, incluyendo cifrado si se cambia la contraseña.
        """
        if "password" in validated_data:
            validated_data["password"] = bcrypt.hashpw(
                validated_data["password"].encode('utf-8'), bcrypt.gensalt()
            ).decode('utf-8')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
