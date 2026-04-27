from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId  # Para validar ObjectId de MongoDB
from .models import Saldo, MovimientoSaldo
from usuarios.models import Usuario

class ConsultarSaldoView(APIView):
    def get(self, request, usuario_id):
        # Validar que usuario_id sea un ObjectId válido
        if not ObjectId.is_valid(usuario_id):
            return Response({"error": "ID de usuario inválido"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            usuario = Usuario.objects.get(pk=ObjectId(usuario_id))
        except Usuario.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        saldo = Saldo.objects.filter(usuario=usuario).first()
        if saldo:
            return Response({"usuario": usuario_id, "saldo_actual": saldo.saldo_actual}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Saldo no encontrado"}, status=status.HTTP_404_NOT_FOUND)

class ActualizarSaldoView(APIView):
    def post(self, request, usuario_id):
        # Validar usuario_id
        if not ObjectId.is_valid(usuario_id):
            return Response({"error": "ID de usuario inválido"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            usuario = Usuario.objects.get(pk=ObjectId(usuario_id))
        except Usuario.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data
        if 'cambio_saldo' not in data or not isinstance(data['cambio_saldo'], (int, float)):
            return Response({"error": "Se requiere el campo 'cambio_saldo' como número"}, status=status.HTTP_400_BAD_REQUEST)
        
        cambio_saldo = float(data['cambio_saldo'])
        descripcion = data.get('descripcion', '')

        saldo = Saldo.objects.filter(usuario=usuario).first()
        if not saldo:
            saldo = Saldo(usuario=usuario, saldo_actual=0.0)
        
        saldo.saldo_actual += cambio_saldo
        saldo.save()

        # Crear movimiento de saldo
        movimiento = MovimientoSaldo(
            saldo=saldo,
            cambio=cambio_saldo,
            descripcion=descripcion
        )
        movimiento.save()

        return Response({
            "usuario": usuario_id,
            "nuevo_saldo": saldo.saldo_actual,
            "movimiento": {
                "id": str(movimiento.id),
                "cambio": movimiento.cambio,
                "descripcion": movimiento.descripcion,
                "fecha": movimiento.fecha
            }
        }, status=status.HTTP_200_OK)

class ListarMovimientosSaldoView(APIView):
    def get(self, request, usuario_id):
        # Validar usuario_id
        if not ObjectId.is_valid(usuario_id):
            return Response({"error": "ID de usuario inválido"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            usuario = Usuario.objects.get(pk=ObjectId(usuario_id))
        except Usuario.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        saldo = Saldo.objects.filter(usuario=usuario).first()
        if not saldo:
            return Response({"error": "Saldo no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        movimientos = MovimientoSaldo.objects.filter(saldo=saldo).order_by('-fecha')

        # Serializar movimientos a lista de dicts
        movimientos_list = []
        for mov in movimientos:
            movimientos_list.append({
                "id": str(mov.id),
                "cambio": mov.cambio,
                "descripcion": mov.descripcion,
                "fecha": mov.fecha
            })

        return Response({
            "usuario": usuario_id,
            "movimientos": movimientos_list
        }, status=status.HTTP_200_OK)
