"""
Demo de la validación SWOT–mareógrafo (método por paso `pass_v2.2`), en español e inglés.

Aplicación multipágina de Streamlit que presenta las validaciones corregidas: resultados por estación, comparación
con el DAC solo, sensibilidad al radio, patrón regional, contexto bibliográfico y método. Lee solo salidas
versionadas en `datos/` (series de `pass_v2.2` y tabla maestra v2); no recalcula métricas ni llama a ninguna API.

El idioma se elige en la barra lateral y se refleja en la URL (`?lang=es` / `?lang=en`). Cada idioma tiene sus
páginas en `paginas/<idioma>/`, con los mismos nombres de archivo, para que al cambiar de idioma se siga en la
misma página.

Uso (desde la raíz del repo):
  streamlit run app.py
"""
import sys
from pathlib import Path

import streamlit as st

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ))

from nucleo import textos as T  # noqa: E402

# Primera visita: idioma de la URL (?lang=), o español. Después manda el selector.
if "idioma" not in st.session_state:
    lang = st.query_params.get("lang", T.POR_DEFECTO)
    st.session_state.idioma = lang if lang in T.IDIOMAS else T.POR_DEFECTO

st.set_page_config(page_title=T.t("titulo_app"), page_icon=":material/waves:",
                   layout="wide", initial_sidebar_state="expanded")

st.sidebar.radio("Idioma / Language", options=list(T.IDIOMAS), format_func=T.IDIOMAS.get, key="idioma",
                 horizontal=True, label_visibility="collapsed")
st.query_params["lang"] = T.idioma()

CARPETA = RAIZ / "paginas" / T.idioma()
# (sección, [(archivo, título, icono)])
PAGINAS = [
    ("sec_resumen", [("inicio", "pag_inicio", ":material/home:")]),
    ("sec_resultados", [
        ("estaciones", "pag_estaciones", ":material/map:"),
        ("explorador", "pag_explorador", ":material/query_stats:"),
        ("aporta_swot", "pag_aporta", ":material/compare_arrows:"),
        ("radio", "pag_radio", ":material/radar:"),
        ("regional", "pag_regional", ":material/hub:"),
    ]),
    ("sec_contexto", [
        ("literatura", "pag_literatura", ":material/menu_book:"),
        ("metodo", "pag_metodo", ":material/fact_check:"),
    ]),
]

navegacion = st.navigation({
    T.t(seccion): [st.Page(CARPETA / f"{archivo}.py", title=T.t(titulo), icon=icono, default=archivo == "inicio")
                   for archivo, titulo, icono in paginas]
    for seccion, paginas in PAGINAS
})

navegacion.run()
