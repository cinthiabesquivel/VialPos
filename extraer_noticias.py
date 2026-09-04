import requests
from bs4 import BeautifulSoup
from datetime import datetime

def buscar_noticias_automaticas():
    # Ampliamos las fuentes recorriendo páginas de resultados (simulando paginación o listados más amplios)
    fuentes_urls = [
        "https://www.elterritorio.com.ar/tag/70/siniestro-vial",
        "https://www.noticiasdelacalle.com.ar/buscador/?s=siniestro",
        "https://misionesonline.net/?s=siniestro+vial",
        "https://misionescuatro.com/policiales/"
    ]
    
    noticias_extraidas = []
    links_encontrados = set()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    for url_fuente in fuentes_urls:
        print(f"Escaneando fuente: {url_fuente}...")
        try:
            response = requests.get(url_fuente, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                for a in soup.find_all('a', href=True):
                    link = a['href']
                    if link.startswith("http") and any(dominio in link for dominio in ["elterritorio.com.ar", "noticiasdelacalle.com.ar", "misionesonline.net", "misionescuatro.com"]):
                        if "/tag/" not in link and "/buscador/" not in link and "/category/" not in link:
                            links_encontrados.add(link)
        except Exception as e:
            print(f"Error al escanear {url_fuente}: {e}")

    print(f"Se detectaron {len(links_encontrados)} enlaces únicos en total. Procesando contenido completo...")

    # Quitamos el límite de [:20] para evaluar todos los enlaces recolectados de las fuentes
    for url in list(links_encontrados):
        try:
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 200:
                soup_nota = BeautifulSoup(res.text, 'html.parser')
                parrafos = [p.get_text() for p in soup_nota.find_all('p')]
                texto_completo = " ".join(parrafos)
                
                palabras_viales = ["choque", "siniestro", "colisión", "moto", "auto", "atropello", "vuelco", "avenida"]
                if any(p in texto_completo.lower() for p in palabras_viales) and len(texto_completo) > 200:
                    noticias_extraidas.append({
                        "url": url,
                        "texto": texto_completo
                    })
        except Exception:
            continue

    print(f"¡Extracción automática finalizada! Se obtuvieron {len(noticias_extraidas)} notas viales listas para procesar.")
    return noticias_extraidas

if __name__ == '__main__':
    buscar_noticias_automaticas()