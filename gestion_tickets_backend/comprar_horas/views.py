from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId
from usuarios.models import Usuario
from .models import CompraHoras
from saldo.models import Saldo  # Para actualizar el saldo si se desea

class ComprarHorasView(APIView):
    def post(self, request, usuario_id):
        # Validar el ObjectId del usuario
        if not ObjectId.is_valid(usuario_id):
            return Response({"error": "ID de usuario inválido"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            usuario = Usuario.objects.get(pk=ObjectId(usuario_id))
        except Usuario.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        cantidad_horas = data.get('cantidad_horas')
        valor_por_hora = data.get('valor_por_hora')

        # Validar datos requeridos
        if cantidad_horas is None or valor_por_hora is None:
            return Response({"error": "Se requieren 'cantidad_horas' y 'valor_por_hora'"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cantidad_horas = float(cantidad_horas)
            valor_por_hora = float(valor_por_hora)
        except ValueError:
            return Response({"error": "Los valores deben ser numéricos"}, status=status.HTTP_400_BAD_REQUEST)

        total_pagado = cantidad_horas * valor_por_hora

        # Crear la compra
        compra = CompraHoras(
            usuario=usuario,
            cantidad_horas=cantidad_horas,
            valor_por_hora=valor_por_hora,
            total_pagado=total_pagado
        )
        compra.save()

        # Opcional: agregar las horas al saldo (si así se maneja tu lógica)
        saldo = Saldo.objects(usuario=usuario).first()
        if saldo:
            saldo.saldo_actual += cantidad_horas
            saldo.save()
        else:
            saldo = Saldo(usuario=usuario, saldo_actual=cantidad_horas)
            saldo.save()

        return Response({
            "mensaje": "Horas compradas exitosamente",
            "usuario": str(usuario.id),
            "cantidad_horas": cantidad_horas,
            "valor_por_hora": valor_por_hora,
            "total_pagado": total_pagado
        }, status=status.HTTP_201_CREATED)
        
class ListarComprasView(APIView):
    def get(self, request, usuario_id):
        if not ObjectId.is_valid(usuario_id):
            return Response({"error": "ID de usuario inválido"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            usuario = Usuario.objects.get(pk=ObjectId(usuario_id))
        except Usuario.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        compras = CompraHoras.objects(usuario=usuario).order_by('-fecha_compra')

        data = []
        for compra in compras:
            data.append({
                "cantidad_horas": compra.cantidad_horas,
                "valor_por_hora": compra.valor_por_hora,
                "total_pagado": compra.total_pagado,
                "fecha_compra": compra.fecha_compra.strftime('%Y-%m-%d %H:%M:%S'),
            })

        return Response(data, status=status.HTTP_200_OK) 
