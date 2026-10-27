"""Método por paso y limitaciones."""
import streamlit as st

from nucleo import estilo as E

E.cabecera(
    "Contexto · Método",
    "Cómo se obtiene cada cifra",
    "Un resumen del método de comparación entre SWOT y los mareógrafos y de sus limitaciones.",
)

tab_metodo, tab_limites = st.tabs(["Método por paso", "Limitaciones"])

with tab_metodo:
    pasos = [
        ("1 · Píxeles", "Todos los píxeles con anomalía válida dentro de un círculo real de radio R alrededor del "
                        "mareógrafo, sin submuestreo; solo calidad 0."),
        ("2 · DAC devuelto", "Se suma la corrección atmosférica a la anomalía, porque el mareógrafo sí registra la "
                             "respuesta a la presión y el viento."),
        ("3 · Agregación", "Tramos de 1 km sobre una línea fija por track; valores atípicos por MAD dentro de cada "
                           "tramo; valor del paso = mediana de las medianas."),
        ("4 · Hora real", "La hora del paso es la mediana del tiempo de los píxeles; el mareógrafo se interpola "
                          "entre las dos horas que la rodean."),
        ("5 · Métricas", "Entre pasos: A (SWOT + DAC), B (DAC solo) y C, sobre los mismos pasos; desplazamiento "
                         "como descriptor."),
    ]
    cols = st.columns(len(pasos))
    for c, (t, b) in zip(cols, pasos):
        with c:
            E.hallazgo(t, b)
    st.latex(r"\eta_{SWOT} = \mathcal{A}(S + D), \qquad \eta_{TG} = H_{TG}(t_p) - T_{TG}(t_p), \qquad "
             r"d = \eta_{SWOT} - \eta_{TG}")
    st.markdown(
        "Es la comparación **sin marea** de Han et al. (2026): cada sistema retira la marea con su propia "
        "predicción (FES2022 y HRET en SWOT; la predicción armónica de Puertos del Estado en el mareógrafo) y la "
        "respuesta atmosférica se conserva en los dos lados. No se transforma la referencia vertical: por eso el "
        "desplazamiento medio es un descriptor y la métrica principal es el RMSE sin desplazamiento.\n\n"
        "**Reglas de diseño.** Ningún filtro ni definición se eligió por su concordancia con el mareógrafo; no se "
        "buscó un radio óptimo; las estaciones exploratorias se presentan aparte con su condición.")

with tab_limites:
    st.markdown(
        "- **Muestras pequeñas:** 23–25 pares por estación principal (7 en Langosteira); intervalos anchos.\n"
        "- **Dependencia:** las estaciones no son independientes entre sí, y los intervalos suponen pasos "
        "independientes, por lo que podrían ser algo optimistas.\n"
        "- **Referencia vertical:** no se transforma; el altímetro mide en un marco geocéntrico y el mareógrafo "
        "respecto a la corteza. El movimiento estacional del terreno no se trata.\n"
        "- **Predicción de marea de Puertos del Estado:** su composición exacta (constituyentes de largo periodo) "
        "no está documentada; la hipótesis de Sa/Ssa sigue abierta.\n"
        "- **Villagarcía:** desplazamiento de −47.9 cm en el track 197 a 10 km, propio de esa estación; su causa "
        "no puede determinarse con los datos disponibles y no se interpreta.\n"
        "- **Rías:** en Marín y Vigo la cobertura válida es escasa; sus resultados son exploratorios.")
