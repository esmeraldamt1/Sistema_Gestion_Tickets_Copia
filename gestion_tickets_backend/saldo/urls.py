from django.urls import path
from . import views

urlpatterns = [
    path('consultar/<str:usuario_id>/', views.ConsultarSaldoView.as_view(), name='consultar_saldo'),
    path('actualizar/<str:usuario_id>/', views.ActualizarSaldoView.as_view(), name='actualizar_saldo'),
    path('movimientos/<str:usuario_id>/', views.ListarMovimientosSaldoView.as_view(), name='listar_movimientos_saldo'),
]
