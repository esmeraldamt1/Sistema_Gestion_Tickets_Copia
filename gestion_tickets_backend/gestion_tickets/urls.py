from django.contrib import admin
from django.urls import path, include
from usuarios.views import index  #  Importamos la vista de inicio del sistema

urlpatterns = [
    # Panel de administración de Django
    path('admin/', admin.site.urls),

    #  Ruta raíz que devuelve mensaje de bienvenida desde usuarios.views.index
    path('', index, name='index'),

    #  Rutas para gestión de usuarios (registro, login, recuperación, agentes, etc.)
    path('usuarios/', include('usuarios.urls')),

    #  Rutas para el módulo de tickets
    path('tickets/', include('tickets.urls')),

    #  Rutas para ayuda y soporte técnico
    path('ayuda_y_soporte/', include('ayuda_y_soporte.urls')),

    #  Rutas para reportes y análisis
    path('reportes/', include('reportes.urls')),

    #  Rutas para manejo de saldo
    path('saldo/', include('saldo.urls')),

    #  Rutas para la compra de horas de servicio
    path('comprar_horas/', include('comprar_horas.urls')),

    #  Rutas para gestión de departamentos
    path('departamentos/', include('departamentos.urls')),
]
