"""
Demo de la validación SWOT–mareógrafo (método por paso `pass_v2.2`), en español.

Aplicación multipágina de Streamlit que presenta las validaciones corregidas: resultados por estación, comparación
con el DAC solo, sensibilidad al radio, patrón regional, contexto bibliográfico y método. Lee solo salidas
versionadas en `datos/` (series de `pass_v2.2` y tabla maestra v2); no recalcula métricas ni llama a ninguna API.

Uso (desde la raíz del repo):
  streamlit run app.py
"""
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent))

st.set_page_config(page_title="Validación SWOT – mareógrafos · Galicia", page_icon=":material/waves:",
                   layout="wide", initial_sidebar_state="expanded")

PAGINAS = Path(__file__).resolve().parent / "paginas"

navegacion = st.navigation({
    "Resumen": [
        st.Page(PAGINAS / "inicio.py", title="Inicio", icon=":material/home:", default=True),
    ],
    "Resultados": [
        st.Page(PAGINAS / "estaciones.py", title="Estaciones y datos", icon=":material/map:"),
        st.Page(PAGINAS / "explorador.py", title="Explorador por estación", icon=":material/query_stats:"),
        st.Page(PAGINAS / "aporta_swot.py", title="¿Aporta SWOT?", icon=":material/compare_arrows:"),
        st.Page(PAGINAS / "radio.py", title="Radio de búsqueda", icon=":material/radar:"),
        st.Page(PAGINAS / "regional.py", title="Patrón regional", icon=":material/hub:"),
    ],
    "Contexto": [
        st.Page(PAGINAS / "literatura.py", title="Otros estudios", icon=":material/menu_book:"),
        st.Page(PAGINAS / "metodo.py", title="Método", icon=":material/fact_check:"),
    ],
})

navegacion.run()
