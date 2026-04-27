# Importamos librerías necesarias
import io  # Para manejar archivos en memoria
from datetime import datetime  # Para manejar fechas
from mongoengine.queryset.visitor import Q  # Para construir filtros de consultas dinámicas
from openpyxl import Workbook  # Para generar archivos Excel

# Usamos importaciones relativas para evitar errores de importación si se usa como módulo
from tickets.models import Ticket   # Modelo principal de Tickets
from usuarios.models import Usuario  # Modelo de Usuario
from departamentos.models import Departamento  # Modelo de Departamento

def generar_reporte_tickets(filtros):
    """
    Genera una lista de tickets filtrados según los parámetros recibidos.
    Retorna una lista de diccionarios con datos listos para el frontend (nombres legibles).
    """
    query = Q()  # Creamos una consulta vacía

    # Aplicamos filtros según los parámetros proporcionados
    if 'estado_ticket' in filtros:
        query &= Q(estado_ticket=filtros['estado_ticket'])
    if 'asignado' in filtros:
        query &= Q(asignado=filtros['asignado'])
    if 'solicitante' in filtros:
        query &= Q(solicitante=filtros['solicitante'])
    if 'tipo_ticket' in filtros:
        query &= Q(tipo_ticket=filtros['tipo_ticket'])
    if 'prioridad' in filtros:
        query &= Q(prioridad=filtros['prioridad'])
    if 'departamento' in filtros:
        query &= Q(departamento=filtros['departamento'])

    # Filtro por rango de fechas (inicio y fin)
    if 'fecha_inicio' in filtros:
        fecha_inicio = datetime.strptime(filtros['fecha_inicio'], "%Y-%m-%d")
        query &= Q(fecha_creacion__gte=fecha_inicio)
    if 'fecha_fin' in filtros:
        fecha_fin = datetime.strptime(filtros['fecha_fin'], "%Y-%m-%d")
        query &= Q(fecha_creacion__lte=fecha_fin)

    # Ejecutamos la consulta y obtenemos tickets
    tickets = Ticket.objects(query)

    # Convertimos a formato legible para JSON (con nombres)
    reporte = []
    for ticket in tickets:
        reporte.append({
            "id": str(ticket.id),
            "titulo": ticket.asunto,
            "descripcion": ticket.descripcion,
            "estado": ticket.estado_ticket,
            "tipo": ticket.tipo_ticket,
            "prioridad": ticket.prioridad,
            "solicitante": ticket.solicitante.username if ticket.solicitante else None,
            "asignado": ticket.asignado.username if ticket.asignado else None,
            "departamento": ticket.departamento.nombre if ticket.departamento else None,
            "fecha_creacion": ticket.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S") if ticket.fecha_creacion else ""
        })

    return reporte

def generar_reporte_tickets_excel(filtros):
    """
    Genera un archivo Excel a partir de los tickets filtrados, usando nombres legibles.
    Retorna un objeto BytesIO que contiene el archivo Excel.
    """
    # Obtenemos los tickets ya formateados como lista de diccionarios
    tickets = generar_reporte_tickets(filtros)

    # Si no hay tickets, no generamos archivo
    if not tickets:
        return None

    # Creamos un nuevo libro de Excel y activamos una hoja
    wb = Workbook()
    ws = wb.active
    ws.title = "Reporte de Tickets"

    # Definimos los encabezados de las columnas
    encabezados = [
        "ID", "Título", "Descripción", "Estado", "Tipo", "Prioridad",
        "Solicitante", "Asignado", "Departamento", "Fecha de Creación"
    ]
    ws.append(encabezados)  # Escribimos encabezados en la hoja

    # Agregamos las filas de tickets
    for ticket in tickets:
        fila = [
            ticket["id"],
            ticket["titulo"],
            ticket["descripcion"],
            ticket["estado"],
            ticket["tipo"],
            ticket["prioridad"],
            ticket["solicitante"] or "",
            ticket["asignado"] or "",
            ticket["departamento"] or "",
            ticket["fecha_creacion"]
        ]
        ws.append(fila)  # Añadimos fila a la hoja

    # Guardamos el archivo en memoria (BytesIO)
    archivo_memoria = io.BytesIO()
    wb.save(archivo_memoria)
    archivo_memoria.seek(0)  # Volvemos al inicio del stream para poder descargarlo
    return archivo_memoria
