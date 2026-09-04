import os
import django
import pandas as pd

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vialpos_web.settings')
django.setup()

from core.models import Siniestro

def importar():
    ruta = 'data/siniestros_posadas.csv'
    print(f"Leyendo archivo desde {ruta}...")
    
    try:
        # sep=None y engine='python' detectan automáticamente si usa comas o punto y coma
        df = pd.read_csv(ruta, sep=None, engine='python')
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")
        return

    print(f"Columnas encontradas en el CSV: {list(df.columns)}")
    
    contador = 0
    errores = 0
    
    for _, row in df.iterrows():
        try:
            # Limpieza y conversión segura de coordenadas y datos
            lat = row.get('latitud')
            lon = row.get('longitud')
            
            if pd.isna(lat) or pd.isna(lon):
                continue

            Siniestro.objects.create(
                fecha_hora=row.get('fecha_hora'),
                calle_1=str(row.get('calle_1', 'Desconocida')),
                calle_2=str(row.get('calle_2', '')),
                tipo_siniestro=str(row.get('tipo_siniestro', 'Colisión')),
                latitud=float(str(lat).replace(',', '.')),
                longitud=float(str(lon).replace(',', '.'))
            )
            contador += 1
        except Exception as err:
            errores += 1
            print(f"Error en la fila {contador + errores}: {err}")
        
    print(f"¡Listo! Se importaron {contador} siniestros correctamente (Omitidos/Errores: {errores}).")

if __name__ == '__main__':
    importar()