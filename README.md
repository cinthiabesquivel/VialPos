# 🚦 VialPos — Sistema de Inteligencia Espacial y Análisis de Siniestralidad Vial

**VialPos** es una plataforma de análisis espacial desarrollada para la gestión de la seguridad vial en la ciudad de Posadas, Misiones. Permite la ingesta de siniestros viales, la detección automática de puntos negros (hotspots) mediante Inteligencia Artificial y la generación de mapas interactivos para la toma de decisiones municipales.

---

## 🎯 1. Objetivos del Proyecto

* **Objetivo General:** Automatizar la detección y visualización de puntos negros de siniestralidad urbana en la ciudad de Posadas mediante aprendizaje no supervisado y tecnologías geoespaciales.
* **Objetivos Específicos:**
  * Desplegar una base de datos geoespacial (PostgreSQL + PostGIS) containerizada con Docker Compose.
  * Ingestar y almacenar geometrías de siniestros viales en sistema de referencia espacial `EPSG:4326`.
  * Aplicar el algoritmo **DBSCAN** sobre coordenadas proyectadas en metros (`EPSG:32721`) para agrupar accidentes sin imponer un número fijo de clusters.
  * Implementar trazabilidad y auditoría automática de cambios mediante *triggers* PL/pgSQL.
  * Renderizar mapas interactivos en HTML (Folium) con capas de marcadores y mapas de calor (HeatMap).

---

## 📍 2. Alcance del Proyecto

* **Dentro del Alcance (In Scope):**
  * Infraestructura containerizada vía `docker-compose.yml`.
  * Scripts de ingesta de archivos CSV hacia la base de datos PostGIS.
  * Algoritmo de clustering DBSCAN con detección de concentraciones y filtrado de ruido (outliers).
  * Sistema de auditoría automática (INSERT/UPDATE/DELETE) guardando estados en formato `JSONB`.
  * Exportación de mapas interactivos HTML.
* **Fuera del Alcance (Out of Scope):**
  * Sincronización e integración directa con redes semafóricas en tiempo real.
  * Procesamiento en vivo de transmisiones de cámaras de fotomulta.

---

## 📐 3. Arquitectura y Diagramas del Sistema

### Diagrama Entidad-Relación (DER) + Auditoría