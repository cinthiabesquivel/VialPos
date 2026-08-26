# Documento de Inventario y Diagnóstico de Fuentes de Datos

## 1. Medios Periodísticos (Siniestros Viales)
| Fuente | Método de Acceso (RSS/API/Scraping) | Cobertura Histórica Estimada | Variables Observables | Limitaciones Identificadas |
| :--- | :--- | :--- | :--- | :--- |
| **Primera Edición** | *A evaluar (RSS/Sitemap/Scraping)* | *Por determinar* | Título, Texto, Fecha, Ubicación | Sesgo hacia siniestros graves/noticiosos. |
| **El Territorio** | *A evaluar (RSS/Sitemap/Scraping)* | *Por determinar* | Título, Texto, Fecha, Ubicación | Posible duplicación con Primera Edición. |

## 2. Infraestructura y Geografía (IDE Posadas / Complementarios)
| Capa / Fuente | Formato (SHP/KML/GeoJSON/WFS/API) | Descripción | Atributos Clave | Estado de Disponibilidad |
| :--- | :--- | :--- | :--- | :--- |
| **IDE Posadas - Calles** | *A evaluar* | Red de vialidad urbana | Nombre, Sentido, Jerarquía | *Pendiente de descarga/consultar WFS* |
| **IDE Posadas - Semáforos** | *A evaluar* | Puntos de intersección semaforizada | Ubicación | *Pendiente de descarga* |
| **OpenStreetMap (OSM)** | API / Overpass / Shapefile | Capa vial complementaria | Geometry, highway, maxspeed | Disponible vía `osmnx` o Geofabrik |

## 3. Fuentes Complementarias (Clima / Demografía)
| Fuente | Variables | Resolución Temporal/Espacial | Prioridad de Integración |
| :--- | :--- | :--- | :--- |
| **SMN** | Precipitación, Visibilidad | Horaria / Estación Posadas | Secundaria (Etapa posterior) |
| **INDEC / IPEC** | Población por radio censal | Censal / Posadas | Secundaria (Normalización) |