import os
import django
from django.utils import timezone
import spacy

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vialpos_web.settings')
django.setup()

from core.models import Siniestro
from extraer_noticias import buscar_noticias_automaticas

def pipeline_principal():
    print("Iniciando análisis semántico con spaCy...")
    noticias = buscar_noticias_automaticas()
    total_guardados = 0

    # Cargar el modelo de lenguaje en español de spaCy
    try:
        nlp = spacy.load("es_core_news_sm")
    except OSError:
        print("Error: Falta descargar el modelo de spaCy. Ejecuta dentro del contenedor: python -m spacy download es_core_news_sm")
        return

    for item in noticias:
        texto = item["texto"]
        url_fuente = item["url"]
        
        # Procesar el texto de la noticia con NLP
        doc = nlp(texto)
        
        # Extraer entidades identificadas exclusivamente como lugares (LOC)
        ubicaciones_detectadas = set()
        for ent in doc.ents:
            if ent.label_ == "LOC":
                ubicaciones_detectadas.add(ent.text.strip())

        # Detectar el tipo de siniestro
        texto_lower = texto.lower()
        palabras_clave = ["vuelco", "atropello", "motociclista", "moto", "colisión", "choque"]
        tipo_detectado = next((p.capitalize() for p in palabras_clave if p in texto_lower), "Colisión")

        for lugar in ubicaciones_detectadas:
            lugar_limpio = lugar.replace("en", "").replace("el", "").replace("la", "").strip()
            
            # Filtro estricto para descartar instituciones, marcas, medios o frases cortas irrelevantes
            palabras_prohibidas = [
                "misiones", "cuatro", "comisaría", "comando", "policía", "unidad", 
                "regional", "tv", "investigación", "auscia", "argentina", "posadas"
            ]
            
            if any(p in lugar_limpio.lower() for p in palabras_prohibidas) or len(lugar_limpio) < 5:
                continue

            # Coordenadas predeterminadas de referencia en Posadas
            lat, lon = -27.3671, -55.8961 
            
            # Evitar duplicados exactos en la base de datos
            existe = Siniestro.objects.filter(calle_1=lugar_limpio, calle_2=f"Fuente: {url_fuente}").exists()
            
            if not existe:
                Siniestro.objects.create(
                    fecha_hora=timezone.now(),
                    calle_1=lugar_limpio,
                    calle_2=f"Fuente: {url_fuente}",
                    tipo_siniestro=tipo_detectado,
                    latitud=lat,
                    longitud=lon
                )
                total_guardados += 1
                print(f"-> [NLP] Ubicación filtrada y guardada: {lugar_limpio}")

    print(f"\n¡Proceso completado! Se registraron {total_guardados} nuevos siniestros válidos.")

if __name__ == '__main__':
    pipeline_principal()