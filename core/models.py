from django.db import models
from django.utils import timezone

class Siniestro(models.Model):
    TIPO_ORIGEN = [
        ('AUTOMATICO', 'Automático (IA - Scraping)'),
        ('MANUAL', 'Carga Manual (Web)'),
    ]

    fecha_hora = models.DateTimeField(default=timezone.now)
    calle_1 = models.CharField(max_length=255, help_text="Ubicación o intersección")
    calle_2 = models.CharField(max_length=255, blank=True, null=True, help_text="Fuente o detalles adicionales")
    tipo_siniestro = models.CharField(max_length=100, default="Colisión")
    
    # Coordenadas geográficas para PostGIS / Leaflet
    latitud = models.FloatField()
    longitud = models.FloatField()
    
    # Nuevo campo para diferenciar el origen del dato
    origen = models.CharField(max_length=20, choices=TIPO_ORIGEN, default='AUTOMATICO')
    
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo_siniestro} en {self.calle_1} ({self.origen})"