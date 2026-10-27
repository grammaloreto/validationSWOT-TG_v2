# Validación SWOT – mareógrafos en Galicia

Demo interactivo (Streamlit, en español) de la validación de la altimetría del satélite SWOT frente a los
mareógrafos de la red REDMAR de Puertos del Estado en la costa de Galicia, para los tracks 197 y 154.

Muestra los resultados por estación, la comparación con el DAC solo, la sensibilidad al radio de búsqueda, el
patrón regional compartido por las estaciones de la costa norte, el contexto de otros estudios y el método.

## Ejecutar en local

```bash
pip install -r requirements.txt
streamlit run app.py
```

El idioma (español o inglés) se elige en la barra lateral; también se puede abrir directamente con `?lang=en`
al final de la URL.

## Datos

El demo solo lee los archivos de `datos/`: la tabla de resultados, las series por paso de cada estación y radio
(6, 8 y 10 km), los análisis regionales, las trazas de referencia de los tracks y la línea de costa. No recalcula
métricas ni se conecta a ningún servicio.

`datos/MANIFIESTO.json` registra la procedencia de cada archivo (origen, revisión y sha256). Para actualizarlos y
comprobar que lo que dibuja el demo reproduce las cifras guardadas:

```bash
python herramientas/actualizar_datos.py RUTA_DEL_REPOSITORIO_DE_VALIDACION
python herramientas/comprobar_demo.py
```

## Fuentes

- SWOT L3 LR SSH Unsmoothed v2.0.1 (AVISO/CNES).
- Mareógrafos REDMAR, Puertos del Estado.
- Línea de costa: Natural Earth 10 m (dominio público).
