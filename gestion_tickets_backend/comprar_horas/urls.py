# Importa la función 'path' desde 'django.urls' para definir rutas de URL
from django.urls import path

# Importa la vista 'ComprarHorasView' desde el archivo 'views.py' del mismo módulo
from .views import ComprarHorasView, ListarComprasView 

# Lista de patrones de URL para esta aplicación
urlpatterns = [
    # Define una ruta que espera un string como 'usuario_id' en la URL
    # Esta ruta está asociada a la vista 'ComprarHorasView'
    # El nombre 'comprar_horas' permite referenciar esta URL fácilmente desde otras partes del proyecto
    path('<str:usuario_id>/', ComprarHorasView.as_view(), name='comprar_horas'),
    
    path('historial/<str:usuario_id>/', ListarComprasView.as_view(), name='historial_compras'),
    # Define una nueva ruta para consultar el historial de compras de un usuario específico
    # 'historial/<str:usuario_id>/' indica que la URL incluirá el ID del usuario como string
    # Esta ruta está asociada a la vista 'ListarComprasView', que se encargará de procesar la solicitud GET
    # El nombre 'historial_compras' permite referenciar esta URL fácilmente desde otras partes del sistema

]
