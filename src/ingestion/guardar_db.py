import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from sqlalchemy import create_engine

# Conexión a PostGIS
DB_URL = "postgresql://postgres:postgres_password@localhost:5432/vialpos_db"

def main():
    print("Iniciando carga de datos...")
    
    # 1. Leer CSV
    df = pd.read_csv("data/siniestros_posadas.csv")
    
    # 2. Convertir a GeoDataFrame
    geometrias = [Point(xy) for xy in zip(df['longitud'], df['latitud'])]
    gdf = gpd.GeoDataFrame(df, geometry=geometrias, crs="EPSG:4326")
    
    # 3. Guardar en PostGIS
    engine = create_engine(DB_URL)
    gdf.to_postgis("siniestros", con=engine, if_exists="replace", index=False)
    
    print("✓ Carga completada con éxito en PostGIS.")

if __name__ == "__main__":
    main()