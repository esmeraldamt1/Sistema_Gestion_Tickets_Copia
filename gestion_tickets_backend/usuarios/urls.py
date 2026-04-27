"""
gestion_tickets_backend/usuarios/urls.py

"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    index,
    register,
    login_view,
    enviar_enlace_recuperacion,
    cambiar_contrasena,
    UsuarioViewSet,
    AgentesViewSet,
    SolicitantesViewSet
)

# Router para rutas automáticas de los ViewSets
router = DefaultRouter()

# ViewSets con prefijo
router.register(r'agentes', AgentesViewSet, basename='agentes')                # /agentes/
router.register(r'solicitantes', SolicitantesViewSet, basename='solicitantes') # /solicitantes/

# ViewSet sin prefijo → raíz de la API
router.register(r'', UsuarioViewSet, basename='usuarios')                      # /, /<id>/

urlpatterns = [
    path('inicio/', index, name='index'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('enviar-enlace/', enviar_enlace_recuperacion, name='enviar_enlace'),
    path('cambiar-contrasena/<str:token>/', cambiar_contrasena, name='cambiar_contrasena'),

    # Rutas generadas automáticamente por el router
    path('', include(router.urls)),
]
