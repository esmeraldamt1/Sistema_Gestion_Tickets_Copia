# Importamos el modelo Usuario desde la app usuarios
from usuarios.models import Usuario

# Importamos el modelo Ticket desde la app tickets
from tickets.models import Ticket


# Función para asignar tickets automáticamente usando estrategia "round-robin"
def asignar_usuarios_a_tickets():
    """
    Esta función busca todos los tickets que no tienen asignado ningún agente
    y los distribuye equitativamente entre los agentes disponibles usando round-robin.

    Retorna:
        str: Mensaje que indica cuántos tickets fueron asignados y a cuántos agentes.
    """

    # Buscamos todos los tickets donde el campo 'asignado' es None (no tienen agente)
    tickets_no_asignados = Ticket.objects(asignado=None)

    # Obtenemos todos los usuarios cuyo rol es "agente"
    agentes = list(Usuario.objects(rol="agente"))

    # Si no hay agentes disponibles, retornamos mensaje de advertencia
    if not agentes:
        return " No hay usuarios con rol 'agente' para realizar asignaciones."

    # Si no hay tickets sin asignar, no hay nada que hacer
    if not tickets_no_asignados:
        return "No hay tickets pendientes por asignar."

    # Contamos el total de tickets sin asignar y el total de agentes disponibles
    total_tickets = len(tickets_no_asignados)
    total_agentes = len(agentes)
    asignados = 0  # Contador de tickets que vamos a asignar

    # Recorremos todos los tickets sin asignar
    for i, ticket in enumerate(tickets_no_asignados):
        #  Elegimos un agente de forma rotativa usando el operador módulo (%)
        agente = agentes[i % total_agentes]

        #  Asignamos el agente al ticket
        ticket.asignado = agente

        #  Guardamos el ticket actualizado en la base de datos
        ticket.save()

        #  Aumentamos el contador de tickets asignados
        asignados += 1

    #  Devolvemos un mensaje con el resumen de la operación
    return f" {asignados} tickets fueron asignados entre {total_agentes} agentes."
