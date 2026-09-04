from django.urls import path
from . import views

urlpatterns = [
    path('', views.ver_mapa, name='mapa_siniestros'),
    path('siniestro/nuevo/', views.registrar_siniestro_manual, name='registrar_siniestro_manual'),
    path('api/siniestros/', views.api_siniestros, name='api_siniestros'),
]