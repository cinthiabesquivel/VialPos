import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine
from sklearn.cluster import DBSCAN
import numpy as np

DB_URL = "postgresql://postgres:postgres_password@localhost:5432/vialpos_db"

def detectar_hotspots(eps_metros=150, min_samples=2):
    engine = create_engine(DB_URL)
    
    # 1. Leer siniestros desde PostGIS
    gdf = gpd.read_postgis("SELECT * FROM siniestros", con=engine, geom_col="geometry")
    
    if gdf.empty:
        print("No se encontraron registros en la tabla 'siniestros'.")
        return

    # 2. Reproyectar a UTM Zone 21S (EPSG:32721) para calcular distancias en metros reales
    gdf_utm = gdf.to_crs(epsg=32721)
    
    # Extracción de coordenadas X, Y
    coords = np.column_stack((gdf_utm.geometry.x, gdf_utm.geometry.y))
    
    # 3. Aplicar DBSCAN
    db = DBSCAN(eps=eps_metros, min_samples=min_samples).fit(coords)
    gdf['cluster_id'] = db.labels_
    
    # 4. Reporte por pantalla
    total_clusters = len(set(db.labels_)) - (1 if -1 in db.labels_ else 0)
    puntos_ruido = list(db.labels_).count(-1)
    
    print("=" * 45)
    print("        RESULTADO DEL ANÁLISIS DBSCAN        ")
    print("=" * 45)
    print(f"✓ Total de siniestros analizados: {len(gdf)}")
    print(f"✓ Hotspots (puntos negros) identificados: {total_clusters}")
    print(f"✓ Siniestros aislados: {puntos_ruido}")
    print("-" * 45)
    
    for cluster in sorted(set(db.labels_)):
        if cluster == -1:
            continue
        sub_df = gdf[gdf['cluster_id'] == cluster]
        print(f"  📍 Hotspot #{cluster + 1}: {len(sub_df)} siniestros")
        for _, row in sub_df.iterrows():
            print(f"     - {row['calle_1']} y {row['calle_2']} ({row['tipo_siniestro']})")

if __name__ == "__main__":
    detectar_hotspots()