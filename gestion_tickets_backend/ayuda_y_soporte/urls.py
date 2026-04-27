from django.urls import path
from .views import CrearSolicitudSoporte, ListarSolicitudes, ActualizarSolicitud, BorrarSolicitud

urlpatterns = [
    # Ruta para crear una nueva solicitud de soporte, usando la vista basada en clase 'CrearSolicitudSoporte'
    path('crear/', CrearSolicitudSoporte.as_view(), name='crear_solicitud'),
    
    # Ruta para listar todas las solicitudes de soporte, usando la vista basada en clase 'ListarSolicitudes'
    path('listar/', ListarSolicitudes.as_view(), name='listar_solicitudes'),
    
    # Ruta para actualizar una solicitud específica, identificada por su 'solicitud_id', usando la vista 'ActualizarSolicitud'
    path('actualizar/<str:solicitud_id>/', ActualizarSolicitud.as_view(), name='actualizar_solicitud'),
    
    # Ruta para borrar una solicitud específica, identificada por su 'solicitud_id', usando la vista 'BorrarSolicitud'
    path('borrar/<str:solicitud_id>/', BorrarSolicitud.as_view(), name='borrar_solicitud'),
]

