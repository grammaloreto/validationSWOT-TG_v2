"""Estaciones, trazas y datos: dónde se compara, con qué papel y cuántos pasos quedan."""
import pandas as pd
import streamlit as st

from nucleo import datos as D
from nucleo import estilo as E
from nucleo import graficos as G
from nucleo import textos as T

E.cabecera(
    "Resultados · Estaciones y datos",
    "Siete puertos, dos pasadas del satélite",
    "SWOT cruza Galicia en dos pasadas, los <b>tracks 197 y 154</b>, una vez cada 21 días. Alrededor de cada "
    "mareógrafo se toma un círculo de búsqueda y se comparan los píxeles del satélite con el registro del puerto. "
    "No todas las combinaciones sirven igual: unas son <b>resultados principales</b> y otras se analizan como "
    "<b>casos exploratorios</b>, con su condición a la vista.",
)

c1, c2 = st.columns([3, 2])
with c2:
    radio = st.segmented_control("Círculo de búsqueda", options=list(D.RADIOS), default=D.RADIO_REF,
                                 format_func=lambda r: f"{r} km") or D.RADIO_REF
    track_rol = st.segmented_control("Papel según el track", options=[197, 154], default=197,
                                     format_func=lambda t: f"Track {t}") or 197
    papeles = {s: "principal" for s in D.principales(track_rol)}
    papeles.update({s: "exploratoria" for s in D.exploratorias(track_rol)})
    filas = []
    for s in D.ORDEN:
        fila = {"Estación": D.nombre(s)}
        for tr in D.TRACKS:
            f = D.fila(s, tr)
            marca = "● principal" if f is not None and f.role == "principal" else "○ explor."
            fila[f"Track {tr}"] = "—" if f is None else f"{marca} · {int(f.n)}"
        filas.append(fila)
    st.dataframe(pd.DataFrame(filas), hide_index=True, use_container_width=True,
                 column_config={"Estación": st.column_config.TextColumn(width="small")})
    st.caption("Papel a 10 km y número de pares válidos en cada track.")
    E.nota("Una combinación es <b>principal</b> si tiene cobertura suficiente de SWOT y del mareógrafo; "
           "las <b>exploratorias</b> se muestran aparte y no entran en la síntesis.")
with c1:
    st.plotly_chart(G.mapa(radio, papeles), use_container_width=True, config={"displayModeBar": False})
    st.caption(f"Círculos de {radio} km. En color y trazo continuo, estaciones principales del track {track_rol}; "
               "en gris punteado, exploratorias. Las trazas son el nadir de la pasada de referencia de cada track "
               "(SWOT mide en una franja ancha a ambos lados de esa línea). Costa: Natural Earth 10 m. "
               "Pasa el ratón por una estación para ver su entorno.")

st.markdown("### Cuántos pasos llegan a compararse")
st.markdown(
    "De los 29 ciclos, no todos dan un par válido: a veces el mareógrafo no registró ese día, a veces SWOT no "
    "devolvió datos sobre el círculo, y a veces falta alguna de las dos horas que rodean el paso. "
    "**Ningún paso se excluye por cómo concuerda con el mareógrafo**: solo por falta de datos.")

ex = D.resumen_exclusiones()
ex = ex[ex.radius_km == radio]
resumen = (ex.assign(Motivo=ex.exclusion_reason.map(T.motivos()).fillna("Par válido"))
             .groupby(["track", "Motivo"]).size().unstack("track").fillna(0).astype(int))
resumen.columns = [f"Track {c}" for c in resumen.columns]
orden = ["Par válido"] + [m for m in T.motivos().values() if m in resumen.index]
st.dataframe(resumen.loc[orden], use_container_width=True)
st.caption(f"Recuento de pasos por motivo, sumando las siete estaciones, a {radio} km.")

with st.expander("Detalle técnico: fuentes de datos"):
    st.markdown(
        "- **SWOT:** producto L3 LR SSH *Unsmoothed* v2.0.1 (CLS/CNES, AVISO), variable `ssha_unfiltered`, "
        "con `dac`, `quality_flag` y `time` por píxel. Fase científica de 21 días, ciclos 1–29.\n"
        "- **Mareógrafos:** registros horarios de la red REDMAR de Puertos del Estado, sin modificar. Cada registro "
        "trae el nivel, la predicción astronómica y su diferencia (residuo meteorológico). Las series horarias "
        "son promedios filtrados del registro de alta frecuencia.\n"
        "- **Langosteira** es la estación REDMAR 3213 (muelle A3), la única de ese puerto con procedencia "
        "instrumental clara. Un registro alternativo con el mismo nombre queda fuera del análisis.\n"
        "- **Nombres** según la red REDMAR (San Cibrao, A Coruña, Ferrol, Langosteira, Villagarcía, Marín, Vigo).")
