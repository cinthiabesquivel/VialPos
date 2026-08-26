import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# 1. Crear datos sintéticos de siniestros en Posadas
datos_siniestros = [
    {"id": 1, "fecha_hora": "2026-08-10 08:30:00", "calle_1": "Av. Uruguay", "calle_2": "Av. Quaranta", "latitud": -27.3985, "longitud": -55.9012, "gravedad": "Moderado"},
    {"id": 2, "fecha_hora": "2026-08-12 19:15:00", "calle_1": "Av. Corrientes", "calle_2": "Av. Centenario", "latitud": -27.3681, "longitud": -55.8964, "gravedad": "Grave"},
    {"id": 3, "fecha_hora": "2026-08-15 14:00:00", "calle_1": "Av. San Martín", "calle_2": "Av. Urquiza", "latitud": -27.3750, "longitud": -55.9120, "gravedad": "Leve"}
]

# 2. Convertir a DataFrame de Pandas
df = pd.DataFrame(datos_siniestros)

# 3. Transformar a GeoDataFrame espacial (EPSG:4326)
geometry = [Point(xy) for xy in zip(df['longitud'], df['latitud'])]
gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

print("--- Dataframe Geoespacial Creado con Éxito ---")
print(gdf[['id', 'calle_1', 'calle_2', 'gravedad', 'geometry']])