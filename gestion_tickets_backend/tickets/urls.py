# tickets/urls.py

# Importamos los módulos necesarios de Django y REST Framework
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Importamos el ViewSet que gestiona las operaciones del modelo Ticket
from .views import TicketViewSet

# Creamos una instancia del router
# Este router generará automáticamente las rutas para operaciones CRUD del Ticket
router = DefaultRouter()

# Registramos el ViewSet en la raíz de la ruta /tickets/
# Esto genera rutas como:
#   - GET     /tickets/         → listar tickets
#   - POST    /tickets/         → crear ticket
#   - GET     /tickets/<id>/    → obtener un ticket
#   - PUT     /tickets/<id>/    → actualizar un ticket
#   - DELETE  /tickets/<id>/    → eliminar un ticket
router.register(r'' , TicketViewSet, basename='tickets')

# Definimos las URLs del módulo tickets
urlpatterns = [
    # Incluimos las rutas generadas automáticamente por el router
    path('', include(router.urls)),
]
