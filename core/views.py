import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .models import Siniestro

def ver_mapa(request):
    siniestros = Siniestro.objects.all()
    return render(request, 'core/mapa.html', {'siniestros': siniestros})

def api_siniestros(request):
    siniestros = Siniestro.objects.all()
    data = list(siniestros.values('id', 'calle_1', 'tipo_siniestro', 'latitud', 'longitud', 'origen'))
    return JsonResponse(data, safe=False)

def registrar_siniestro_manual(request):
    if request.method == 'POST':
        calle_1 = request.POST.get('calle_1')
        tipo_siniestro = request.POST.get('tipo_siniestro', 'Colisión')
        descripcion = request.POST.get('descripcion', '')

        # Armamos la consulta estricta para Posadas, Misiones, Argentina
        query_direccion = f"{calle_1}, Posadas, Misiones, Argentina"
        
        # URL de la API de Nominatim (OpenStreetMap)
        url = "https://nominatim.openstreetmap.org/search"
        
        # IMPORTANTE: Nominatim exige un User-Agent identificable por políticas de uso
        headers = {
            'User-Agent': 'VialPosApp/1.0 (contacto@vialpos.local)'
        }
        params = {
            'q': query_direccion,
            'format': 'json',
            'limit': 1
        }

        try:
            response = requests.get(url, params=params, headers=headers, timeout=5)
            data = response.json()

            if data:
                # Extraemos la latitud y longitud devueltas por OSM
                latitud = float(data[0]['lat'])
                longitud = float(data[0]['lon'])

                # Guardamos en la base de datos PostGIS marcándolo como MANUAL
                Siniestro.objects.create(
                    calle_1=calle_1,
                    calle_2=descripcion,
                    tipo_siniestro=tipo_siniestro,
                    latitud=latitud,
                    longitud=longitud,
                    origen='MANUAL'
                )
                return redirect('mapa_siniestros')
            else:
                # Si la API no encuentra la dirección
                error = "No se pudo encontrar la ubicación en Posadas. Intentá ser más específico (ej: 'Av. Uruguay y Mitre')."
                return render(request, 'core/form_manual.html', {'error': error})

        except requests.exceptions.RequestException:
            error = "Error de conexión con el servicio de geocodificación de OpenStreetMap."
            return render(request, 'core/form_manual.html', {'error': error})

    return render(request, 'core/form_manual.html')