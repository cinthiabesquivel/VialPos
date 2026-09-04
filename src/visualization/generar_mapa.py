import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import HeatMap
from sklearn.cluster import DBSCAN
from sqlalchemy import create_engine

DB_URL = "postgresql://postgres:postgres_password@localhost:5432/vialpos_db"

def main():
    print("Cargando datos desde PostGIS...")
    engine = create_engine(DB_URL)
    
    # 1. Leer datos desde PostGIS
    query = "SELECT id, calle_1, calle_2, tipo_siniestro, geometry FROM siniestros;"
    gdf = gpd.read_postgis(query, con=engine, geom_col="geometry")
    
    # 2. Ejecutar DBSCAN proyectando a metros (EPSG:32721 - UTM zone 21S)
    gdf_proyectado = gdf.to_crs(epsg=32721)
    coords = list(zip(gdf_proyectado.geometry.x, gdf_proyectado.geometry.y))
    
    # eps = 100 metros, min_samples = 2 siniestros
    db = DBSCAN(eps=100, min_samples=2).fit(coords)
    gdf['cluster'] = db.labels_

    # 3. Inicializar mapa en Posadas
    mapa = folium.Map(location=[-27.38, -55.90], zoom_start=13, tiles="OpenStreetMap")
    
    # Paleta de colores para los clusters
    colores_clusters = ['red', 'blue', 'green', 'purple', 'orange', 'darkred']
    
    # 4. Capa de Marcadores por Cluster
    for idx, row in gdf.iterrows():
        lat = row.geometry.y
        lon = row.geometry.x
        cluster_id = row['cluster']
        
        if cluster_id == -1:
            color = 'gray'
            etiqueta_cluster = "Siniestro Aislado (Ruido)"
        else:
            color = colores_clusters[cluster_id % len(colores_clusters)]
            etiqueta_cluster = f"<b>Hotspot #{cluster_id + 1}</b>"
        
        popup_text = f"""
        {etiqueta_cluster}<br>
        <b>ID:</b> #{row['id']}<br>
        <b>Ubicación:</b> {row['calle_1']} y {row['calle_2']}<br>
        <b>Tipo:</b> {row['tipo_siniestro']}
        """
        
        folium.Marker(
            location=[lat, lon],
            popup=popup_text,
            icon=folium.Icon(color=color, icon="info-sign" if cluster_id != -1 else "minus")
        ).add_to(mapa)
        
    # 5. Capa adicional: Mapa de Calor (HeatMap)
    heat_data = [[point.xy[1][0], point.xy[0][0]] for point in gdf.geometry]
    HeatMap(heat_data, radius=15, blur=10).add_to(mapa)
    
    # 6. Guardar mapa interactivo final
    output_path = "mapa_hotspots.html"
    mapa.save(output_path)
    print(f"✓ Mapa enriquecido generado con éxito: {output_path}")

if __name__ == "__main__":
    main()