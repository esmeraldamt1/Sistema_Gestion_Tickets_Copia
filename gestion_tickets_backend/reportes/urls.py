# reportes/urls.py

# Importamos la función path para definir las rutas
from django.urls import path

# Importamos las vistas que se usarán en las rutas
from .views import (
    ReporteTicketsView,            # Vista que retorna el reporte en formato JSON
    ExportarReporteTicketsView,    # Vista que genera y descarga el Excel
    DepartamentosView              # Vista que retorna los departamentos únicos
)

# Lista de rutas disponibles en la app de reportes
urlpatterns = [
    # Ruta para consultar el reporte de tickets (en formato JSON)
    path('tickets/', ReporteTicketsView.as_view(), name='reporte_tickets'),

    # Ruta para exportar el reporte de tickets como archivo Excel
    path('tickets/exportar/', ExportarReporteTicketsView.as_view(), name='exportar_reporte_tickets'),

    # Ruta para obtener los departamentos únicos registrados en los tickets
    path('departamentos/', DepartamentosView.as_view()),  
]
