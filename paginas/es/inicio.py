"""Portada: qué se evalúa, cifras clave y los tres hallazgos, en lenguaje general."""
import streamlit as st

from nucleo import datos as D
from nucleo import estilo as E

E.portada(
    "Gemelo Digital del Océano · Validación",
    "¿Cuánto se parece SWOT a los mareógrafos de Galicia?",
    "El satélite <b>SWOT</b> mide el nivel del mar con una resolución inédita, incluso muy cerca de la costa. "
    "Antes de usar esa información en el gemelo digital, la comparamos con lo que registran los "
    "<b>mareógrafos de Puertos del Estado</b> en siete puertos gallegos, paso a paso, durante 20 meses. "
    "Y nos hacemos una pregunta más exigente que «¿se parecen?»: <b>¿cuánto de ese parecido se debe "
    "realmente a SWOT?</b>",
)

main = [D.fila(s, tr) for s, tr, rol in D.combinaciones() if rol == "principal"]
largas = [f for f in main if f.n >= 20]
pares = int(sum(f.n for f in main))
con_cero = sum(f.dRMSE_AB_ci_low <= 0 <= f.dRMSE_AB_ci_high for f in main)

E.tarjetas([
    (f"{len(main)}", "combinaciones estación–track con resultado principal (radio de 10 km)", "📍"),
    (f"{pares}", "pares satélite–mareógrafo en esas combinaciones, uno por paso de SWOT", "🛰️"),
    (f"{E.num(min(f.A_r for f in largas))}–{E.num(max(f.A_r for f in largas))}",
     "correlación de SWOT + DAC con el mareógrafo en las series largas", "📈"),
    (f"{con_cero} de {len(main)}",
     "combinaciones sin mejora demostrada al añadir SWOT al modelo atmosférico (DAC)", "⚖️"),
])

st.markdown("### Tres hallazgos")
c1, c2, c3 = st.columns(3)
with c1:
    E.hallazgo(
        "SWOT sigue a los mareógrafos, pero no mejor que el modelo atmosférico",
        "Con la corrección atmosférica (DAC) devuelta, SWOT sube y baja con el mareógrafo. Pero el DAC por sí "
        "solo consigue correlaciones parecidas y un error algo menor. Gran parte del parecido lo explica ya el "
        "efecto de la presión y el viento.", numero=1, acento=E.COLOR_A)
    st.page_link("paginas/es/aporta_swot.py", label="Ver la comparación", icon=":material/arrow_forward:")
with c2:
    E.hallazgo(
        "Acercarse más a la estación no mejora la comparación",
        "Reducir el círculo de búsqueda de 10 a 6 km deja menos píxeles válidos y, en general, no acerca SWOT al "
        "mareógrafo. En algunos casos limita mucho la cobertura válida; además, importa qué zona del mar "
        "representan los píxeles respecto al puerto.", numero=2, acento="#eb6834")
    st.page_link("paginas/es/radio.py", label="Ver la sensibilidad al radio", icon=":material/arrow_forward:")
with c3:
    E.hallazgo(
        "Las estaciones comparten una misma discrepancia",
        "La diferencia SWOT − mareógrafo sube y baja a la vez en la costa norte, se repite en las dos pasadas "
        "separadas 37 horas y sigue de cerca a la diferencia entre las dos predicciones de marea. Es una "
        "asociación, no una prueba de causa, pero señala dónde mirar.", numero=3, acento="#1b6ca8")
    st.page_link("paginas/es/regional.py", label="Ver el patrón regional", icon=":material/arrow_forward:")

st.markdown("### Qué significa para el gemelo digital")
a, b = st.columns(2)
with a:
    st.markdown(
        "- **Una buena correlación no basta para demostrar la aportación de SWOT.** Hay que comprobar si añadir "
        "SWOT reduce el error frente al DAC solo; en estos puertos no lo hace de forma demostrable, lo que no "
        "equivale a que no aporte nada.\n"
        "- **Las estaciones cercanas no son pruebas independientes.** Que varias concuerden no confirma el "
        "resultado si comparten la misma pasada y la misma discrepancia.")
with b:
    st.markdown(
        "- **Las dos predicciones de marea deben ser coherentes.** Antes de interpretar una diferencia, hay que "
        "saber qué componentes de marea retira cada sistema.\n"
        "- **La cobertura válida importa más que la cercanía.** En rías y puertos rodeados de tierra, antes de "
        "interpretar la comparación conviene comprobar cuántos píxeles válidos quedan y qué zona del mar "
        "representan respecto al puerto.")

with st.expander("Para quien quiera el detalle: qué se compara exactamente"):
    st.markdown(
        "Cada vez que SWOT sobrevuela una estación se obtiene **un valor del satélite y uno del mareógrafo**; "
        "las métricas se calculan entre pasos, a lo largo de los 20 meses.")
    st.latex(r"d \;=\; \underbrace{\mathcal{A}(S + D)}_{\text{SWOT + DAC}} \;-\; "
             r"\underbrace{\big[H_{TG}(t_p) - T_{TG}(t_p)\big]}_{\text{residuo del mareógrafo}}")
    st.markdown(
        "- *S*: anomalía del nivel del mar de SWOT L3 v2.0.1 sin filtrar (`ssha_unfiltered`), con la marea del "
        "modelo global ya retirada.\n"
        "- *D*: corrección atmosférica dinámica (DAC), que el producto resta y aquí se devuelve, porque el "
        "mareógrafo sí registra el efecto de la presión y el viento.\n"
        "- 𝒜: mediana de las medianas de tramos de 1 km dentro de un círculo de 10 km (6 y 8 km como "
        "sensibilidad), solo con píxeles de calidad 0.\n"
        "- *H*, *T*: nivel horario del mareógrafo y predicción astronómica de Puertos del Estado, interpolados a "
        "la hora real del paso.\n\n"
        "Se evalúan tres comparaciones sobre los mismos pasos: **A** (SWOT + DAC frente al mareógrafo), "
        "**B** (DAC solo frente al mareógrafo, la referencia) y **C** (anomalía de SWOT frente al mareógrafo "
        "menos el DAC).")
