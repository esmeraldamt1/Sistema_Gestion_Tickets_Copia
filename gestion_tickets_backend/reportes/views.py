# Importamos utilidades necesarias
from django.http import HttpResponse                            # Para generar respuesta de descarga (Excel)
from rest_framework.views import APIView                        # Clase base para vistas basadas en clase (APIView)
from rest_framework.response import Response                   # Para estructurar las respuestas
from rest_framework import status                               # Para usar códigos HTTP estándar
from rest_framework.permissions import IsAuthenticated          # Para proteger las vistas con autenticación

# Importamos el modelo de tickets
from tickets.models import Ticket                               # Modelo principal para obtener datos de tickets

# Importamos funciones del servicio que generan los reportes
from .services import (
    generar_reporte_tickets,                                    # Función para generar reporte JSON
    generar_reporte_tickets_excel,                              # Función para generar archivo Excel
)

# Vista para obtener los departamentos únicos usados en los tickets
class DepartamentosView(APIView):
    """
    Vista para listar los departamentos únicos que tienen al menos un ticket registrado.
    """
    def get(self, request):
        try:
            # Extrae los departamentos únicos desde los tickets
            departamentos = Ticket.objects.distinct('departamento')
            # Filtra posibles valores vacíos o nulos
            departamentos_filtrados = [d for d in departamentos if d]
            # Devuelve los departamentos válidos
            return Response({"departamentos": departamentos_filtrados}, status=status.HTTP_200_OK)
        except Exception as e:
            # Captura errores generales
            return Response(
                {"error": f"Error al obtener departamentos: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# Función auxiliar para extraer filtros desde el request
def extraer_filtros(request):
    """
    Extrae los filtros aplicados desde los parámetros de consulta del request.
    Devuelve un diccionario con claves reconocidas por las funciones de servicio.
    """
    filtros = {}  # Diccionario de filtros

    # Filtros directos desde query params
    estado = request.query_params.get('estado')
    asignado = request.query_params.get('asignado')
    solicitante = request.query_params.get('solicitante')
    tipo_ticket = request.query_params.get('tipo_ticket')
    prioridad = request.query_params.get('prioridad')
    departamento = request.query_params.get('departamento')

    # Filtros por fechas
    fecha_inicio = request.query_params.get('fecha_inicio')  # Formato: YYYY-MM-DD
    fecha_fin = request.query_params.get('fecha_fin')        # Formato: YYYY-MM-DD

    # Asignamos al diccionario solo si están presentes
    if estado:
        filtros['estado_ticket'] = estado
    if asignado:
        filtros['asignado'] = asignado
    if solicitante:
        filtros['solicitante'] = solicitante
    if tipo_ticket:
        filtros['tipo_ticket'] = tipo_ticket
    if prioridad:
        filtros['prioridad'] = prioridad
    if departamento:
        filtros['departamento'] = departamento
    if fecha_inicio:
        filtros['fecha_inicio'] = fecha_inicio
    if fecha_fin:
        filtros['fecha_fin'] = fecha_fin

    return filtros  # Devuelve los filtros listos para aplicar

# Vista para retornar el reporte de tickets en formato JSON
class ReporteTicketsView(APIView):
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder

    """
    Vista para generar un listado de tickets filtrado (formato JSON).
    """
    def get(self, request):
        try:
            filtros = extraer_filtros(request)                     # Extrae filtros de la URL
            reporte = generar_reporte_tickets(filtros)            # Llama al servicio con esos filtros

            if not reporte:
                # Si no se encontraron tickets, se retorna mensaje 404
                return Response(
                    {"mensaje": "No se encontraron tickets con los filtros aplicados."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Si hay datos, se retorna el reporte en formato JSON
            return Response({"tickets": reporte}, status=status.HTTP_200_OK)
        except ValueError as e:
            # Si hay error de validación (formato de fechas, por ejemplo)
            return Response(
                {"error": f"Error de validación: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            # Si ocurre cualquier otro error inesperado
            return Response(
                {"error": f"Error inesperado: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# Vista para exportar los tickets filtrados como un archivo Excel
class ExportarReporteTicketsView(APIView):
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden acceder

    """
    Vista para exportar el reporte de tickets como archivo Excel.
    """
    def get(self, request):
        try:
            filtros = extraer_filtros(request)                          # Extrae los filtros de la URL
            archivo_memoria = generar_reporte_tickets_excel(filtros)   # Genera el archivo en memoria

            if not archivo_memoria:
                # Si no hay resultados, se retorna un Excel vacío
                response = HttpResponse(
                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
                response['Content-Disposition'] = 'attachment; filename="reporte_vacio.xlsx"'
                return response

            # Si hay resultados, se retorna el archivo con contenido
            response = HttpResponse(
                archivo_memoria,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename="reporte_tickets.xlsx"'
            return response
        except ValueError as e:
            # Error por datos mal formateados
            return Response(
                {"error": f"Error de validación: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            # Cualquier otro error
            return Response(
                {"error": f"Error inesperado: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
