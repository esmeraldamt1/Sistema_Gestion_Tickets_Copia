# 📦 Importamos la función path para definir rutas URL en Django
from django.urls import path

# 📦 Importamos las vistas definidas en el archivo views.py del mismo módulo
from . import views


# 🛣️ Lista de rutas (endpoints) disponibles en la app departamentos
urlpatterns = [

    # 🔹 GET /departamentos/
    # Muestra la lista de departamentos disponibles
    path(
        '',                                # Ruta vacía → raíz del módulo
        views.ListaDepartamentos.as_view(),  # Vista basada en clase (hereda de APIView o similar)
        name='departamentos_list'          # Nombre interno para usar en templates o reversas
    ),

    # 🔹 POST /departamentos/crear/
    # Permite crear un solo departamento nuevo
    path(
        'crear/',                          # Ruta relativa para crear uno
        views.departamento_create,         # Vista basada en función
        name='departamento_create'         # Nombre interno de la URL
    ),

    # 🔹 POST /departamentos/crear-multiples/
    # Permite crear múltiples departamentos de una vez
    path(
        'crear-multiples/',                # Ruta para creación masiva
        views.departamentos_create_bulk,   # Vista basada en función
        name='departamentos_create_bulk'   # Nombre interno de la URL
    ),
]
