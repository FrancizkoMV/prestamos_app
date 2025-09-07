
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_principal, name='dashboard_principal'),
    path('mi-perfil/', views.vista_cliente, name='vista_cliente'),
    path('cliente/<int:cliente_id>/', views.detalle_cliente, name='detalle_cliente'),
]
