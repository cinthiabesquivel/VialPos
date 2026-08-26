# Diseño de Arquitectura del Sistema (VialPos)

## 1. Stack Tecnológico Seleccionado
* **Lenguaje Principal:** Python 3.x
* **Base de Datos Relacional y Espacial:** PostgreSQL + Extensión PostGIS
* **Motor de IA / Extracción NLP Local:** Ollama (modelos Llama 3 / Mistral)
* **Procesamiento GIS / Spatial:** GeoPandas, Shapely, PyProj
* **Orquestación y Pipeline:** Scripts Python modulares (`src/`)
* **Visualización / Dashboard:** Streamlit / Power BI / QGIS

## 2. Flujo de Datos Espacial y Relacional (PostGIS)

```text
[ Fuentes Periodísticas ] ──> [ Recolector Raw ] ──> [ Capa RAW (JSON/Text) ]
                                                            │
                                                            ▼
                                                     [ Ollama NLP ]
                                                            │
                                                            ▼
[ IDE Posadas / OSM ] ───────────────────────────> [ PostgreSQL + PostGIS ]
   (Capas GeoJSON/SHP)                                 ├── Tabla: publicaciones_raw
                                                       ├── Tabla: siniestros
                                                       ├── Tabla: ubicaciones (ST_Point)
                                                       └── Tablas: infraestructura_vials