# Importa la clase base 'serializers' desde el módulo 'rest_framework' para poder crear serializers personalizados
from rest_framework import serializers

# Define una clase llamada 'ComprarHorasSerializer' que hereda de 'serializers.Serializer'
# Esta clase se utiliza para validar y transformar los datos que se reciben al comprar horas
class ComprarHorasSerializer(serializers.Serializer):
    
    # Campo que representa el ID del usuario que va a comprar horas
    # Se define como un campo de tipo 'CharField' (cadena de texto)
    # 'required=True' indica que este campo es obligatorio
    usuario_id = serializers.CharField(required=True)

    # Campo que representa la cantidad de horas a comprar
    # Se define como un campo de tipo 'IntegerField' (número entero)
    # 'min_value=1' asegura que el valor mínimo permitido sea 1 (no se pueden comprar 0 o menos horas)
    horas = serializers.IntegerField(min_value=1)

    # Campo que representa el precio total de la compra
    # Se define como un campo de tipo 'FloatField' (número decimal)
    # 'min_value=0' asegura que el precio no sea negativo (puede ser 0 o más)
    precio_total = serializers.FloatField(min_value=0)
