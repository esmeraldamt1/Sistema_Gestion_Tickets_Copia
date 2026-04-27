# 📦 Importamos la clase base Document y los tipos de campos desde mongoengine
from mongoengine import Document, StringField, DateTimeField

# 📦 Importamos datetime para asignar la fecha de creación
from datetime import datetime


# 🏢 Definimos el modelo Departamento, que representa un área dentro del sistema
class Departamento(Document):
    """
    Modelo que representa un departamento (área funcional) en la organización.
    Por ejemplo: Tecnología, Recursos Humanos, Soporte, etc.
    """

    # 🏷️ Nombre del departamento
    # Campo obligatorio, único y con un máximo de 100 caracteres
    nombre = StringField(
        required=True,        # El nombre es obligatorio
        unique=True,          # No puede repetirse con otro departamento
        max_length=100        # Longitud máxima permitida
    )

    # 📝 Descripción del departamento (opcional)
    descripcion = StringField()  # Puede usarse para detalles adicionales

    # 📅 Fecha de creación del registro
    # Se asigna automáticamente al momento de guardar el objeto
    creado_en = DateTimeField(default=datetime.utcnow)  # UTC para consistencia en MongoDB

    # 📌 Método que define cómo se muestra el objeto cuando se convierte en string
    def __str__(self):
        # Devolvemos el nombre del departamento como representación del objeto
        return self.nombre
