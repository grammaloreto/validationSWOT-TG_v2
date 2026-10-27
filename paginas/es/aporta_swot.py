"""La comparación de referencia: SWOT + DAC frente al DAC solo, en todas las estaciones."""
import pandas as pd
import streamlit as st

from nucleo import datos as D
from nucleo import estilo as E
from nucleo import graficos as G

E.cabecera(
    "Resultados · Comparación de referencia",
    "¿Aporta SWOT más que el modelo atmosférico?",
    "El mareógrafo registra el efecto de la presión y el viento sobre el mar, y por eso a SWOT se le devuelve la "
    "corrección atmosférica (DAC). Pero entonces el parecido con el mareógrafo puede venir del modelo atmosférico "
    "y no del satélite. La pieza clave del diseño es comparar también <b>el DAC solo</b> con el mareógrafo: si SWOT "
    "aporta información propia, SWOT + DAC debería acercarse al mareógrafo <b>más</b> que el DAC por sí solo.",
)

incluir = st.toggle("Incluir los casos exploratorios", value=False)
filas = []
for s, tr, rol in D.combinaciones():
    if rol == "exploratoria" and not incluir:
        continue
    f = D.fila(s, tr)
    if f is None or pd.isna(f.dRMSE_AB_cm):
        continue
    etiqueta = f"{D.nombre(s)} · T{tr} (n {int(f.n)})" + (" ·expl." if rol == "exploratoria" else "")
    filas.append((etiqueta, f))

st.plotly_chart(G.forest(filas), use_container_width=True, config={"displayModeBar": False})
st.caption("Morado: A, SWOT + DAC. Verde: B, DAC solo. Derecha: ΔRMSE = RMSE(A) − RMSE(B) con su intervalo de "
           "confianza del 95 %; un valor positivo significa que SWOT + DAC se aleja algo más del mareógrafo. "
           "En rojo, intervalos enteramente por encima de cero.")

main = [D.fila(s, tr) for s, tr, rol in D.combinaciones() if rol == "principal"]
largas = [f for f in main if f.n >= 20]
c1, c2, c3 = st.columns(3)
with c1:
    E.hallazgo("SWOT + DAC sí sigue al mareógrafo",
               f"r = {E.num(min(f.A_r for f in largas))}–{E.num(max(f.A_r for f in largas))} en las seis series "
               f"con 23–25 pares (Langosteira, con 7 pares, llega a {E.num(D.fila('langosteira_2', 197).A_r)}).")
with c2:
    E.hallazgo("…pero el DAC solo llega a lo mismo",
               f"r = {E.num(min(f.B_r for f in main))}–{E.num(max(f.B_r for f in main))} y un RMSE sin "
               f"desplazamiento menor en las {len(main)} combinaciones principales.")
with c3:
    E.hallazgo("…y la diferencia no es concluyente",
               f"ΔRMSE de {E.signo(min(f.dRMSE_AB_cm for f in main))} a {E.signo(max(f.dRMSE_AB_cm for f in main))}"
               f" cm, con todos los intervalos incluyendo el cero: ni mejora ni empeoramiento demostrable.")

st.markdown("### Cómo leerlo")
st.markdown(
    "Esto **no significa que SWOT no aporte nada**. Significa que, en estos puertos, la mayor parte de la "
    "variación del nivel del mar no mareal que ve el mareógrafo es la respuesta a la presión y al viento, y el "
    "modelo atmosférico ya la captura. Una correlación alta con el mareógrafo, por sí sola, no demuestra una "
    "aportación del satélite: hay que compararla con la del modelo atmosférico.")

with st.expander("Detalle técnico: lo que queda tras retirar el DAC (comparación C)"):
    filas_c = [{"Estación": D.nombre(s), "Track": tr, "n": int(D.fila(s, tr).n),
                "r A (SWOT + DAC)": D.fila(s, tr).A_r, "r B (DAC solo)": D.fila(s, tr).B_r,
                "r C (SWOT − DAC lado a lado)": D.fila(s, tr).C_r}
               for s, tr, rol in D.combinaciones() if rol == "principal"]
    st.dataframe(pd.DataFrame(filas_c), hide_index=True, use_container_width=True,
                 column_config={c: st.column_config.NumberColumn(format="%.2f")
                                for c in ("r A (SWOT + DAC)", "r B (DAC solo)", "r C (SWOT − DAC lado a lado)")})
    st.markdown(
        "La comparación C enfrenta la anomalía de SWOT (sin DAC) con el residuo del mareógrafo menos el DAC. La "
        f"asociación que queda es moderada (r = {E.num(min(f.C_r for f in largas))}–"
        f"{E.num(max(f.C_r for f in largas))} en las series largas). No prueba por sí sola información "
        "oceánica independiente de SWOT: puede incluir la discrepancia que comparten las estaciones "
        "(ver *Patrón regional*).")

with st.expander("Detalle técnico: por qué el DAC explica tanto"):
    st.markdown(
        "El DAC (*Dynamic Atmospheric Correction*) representa la respuesta del océano al viento y a la presión "
        "atmosférica. El modelo barotrópico en que se basa redujo "
        "de forma importante la variabilidad del nivel del mar en los mareógrafos respecto al barómetro inverso "
        "(Carrère y Lyard, 2003). Cuando la variabilidad no mareal de un puerto está dominada por esa respuesta, "
        "SWOT + DAC hereda del DAC la mayor parte de su concordancia.\n\n"
        "Los intervalos tratan los pasos como independientes. Con una dependencia temporal positiva entre pasos "
        "consecutivos podrían ser algo estrechos, lo que refuerza la lectura prudente: ninguna estación muestra "
        "una diferencia concluyente en ningún sentido.")
