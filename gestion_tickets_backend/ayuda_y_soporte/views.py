from django.http import JsonResponse
from django.views import View
from .models import SolicitudSoporte
from usuarios.models import Usuario
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from django.utils.timezone import now

@method_decorator(csrf_exempt, name='dispatch')
class CrearSolicitudSoporte(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))

            usuario_id = data.get('usuario')
            asunto = data.get('asunto')
            mensaje = data.get('mensaje')

            if not usuario_id or not asunto or not mensaje:
                return JsonResponse({'message': 'Todos los campos son obligatorios'}, status=400)

            usuario = Usuario.objects(id=usuario_id).first()
            if not usuario:
                return JsonResponse({'message': 'Usuario no encontrado'}, status=404)

            solicitud = SolicitudSoporte(
                usuario=usuario,
                asunto=asunto,
                mensaje=mensaje,
                estado='pendiente',
                fecha_creacion=now()
            )
            solicitud.save()

            return JsonResponse({'message': 'Solicitud creada exitosamente', 'solicitud_id': str(solicitud.id)}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'message': 'El cuerpo debe estar en formato JSON válido'}, status=400)

        except Exception as e:
            return JsonResponse({'message': 'Error al procesar la solicitud', 'error': str(e)}, status=500)


class ListarSolicitudes(View):
    def get(self, request, *args, **kwargs):
        solicitudes = SolicitudSoporte.objects.all()
        solicitudes_data = [
            {
                'id': str(solicitud.id),
                'usuario': str(solicitud.usuario.id),
                'asunto': solicitud.asunto,
                'mensaje': solicitud.mensaje,
                'estado': solicitud.estado,
                'fecha_creacion': solicitud.fecha_creacion.isoformat()
            } for solicitud in solicitudes
        ]
        return JsonResponse({'solicitudes': solicitudes_data}, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class ActualizarSolicitud(View):
    def patch(self, request, solicitud_id, *args, **kwargs):
        try:
            solicitud = SolicitudSoporte.objects(id=solicitud_id).first()
            if not solicitud:
                return JsonResponse({'message': 'Solicitud no encontrada'}, status=404)

            data = json.loads(request.body.decode('utf-8'))

            solicitud.asunto = data.get('asunto', solicitud.asunto)
            solicitud.mensaje = data.get('mensaje', solicitud.mensaje)
            solicitud.estado = data.get('estado', solicitud.estado)
            solicitud.save()

            return JsonResponse({'message': 'Solicitud actualizada exitosamente'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'message': 'El cuerpo debe estar en formato JSON válido'}, status=400)

        except Exception as e:
            return JsonResponse({'message': 'Error al actualizar la solicitud', 'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class BorrarSolicitud(View):
    def delete(self, request, solicitud_id, *args, **kwargs):
        try:
            solicitud = SolicitudSoporte.objects(id=solicitud_id).first()
            if not solicitud:
                return JsonResponse({'message': 'Solicitud no encontrada'}, status=404)

            solicitud.delete()
            return JsonResponse({'message': 'Solicitud eliminada exitosamente'}, status=200)

        except Exception as e:
            return JsonResponse({'message': 'Error al eliminar la solicitud', 'error': str(e)}, status=500)
