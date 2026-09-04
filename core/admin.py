from django.contrib import admin
from .models import Siniestro

@admin.register(Siniestro)
class SiniestroAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha_hora', 'tipo_siniestro', 'calle_1', 'calle_2', 'latitud', 'longitud')
    search_fields = ('calle_1', 'calle_2', 'tipo_siniestro')