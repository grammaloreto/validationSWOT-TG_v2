"""La comparación de referencia: SWOT + DAC frente al DAC solo, en todas las estaciones."""
import pandas as pd
import streamlit as st

from nucleo import datos as D
from nucleo import estilo as E
from nucleo import graficos as G

E.cabecera(
    "Results · Reference comparison",
    "Does SWOT add more than the atmospheric model?",
    "The tide gauge records the effect of pressure and wind on the sea, and that is why the atmospheric "
    "correction (DAC) is restored to SWOT. But then the agreement with the tide gauge may come from the atmospheric "
    "model rather than from the satellite. The key piece of the design is to also compare <b>the DAC alone</b> with "
    "the tide gauge: if SWOT adds information of its own, SWOT + DAC should come closer to the tide gauge <b>than</b> "
    "the DAC does on its own.",
)

incluir = st.toggle("Include the exploratory cases", value=False)
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
st.caption("Purple: A, SWOT + DAC. Green: B, DAC alone. Right: ΔRMSE = RMSE(A) − RMSE(B) with its 95 % "
           "confidence interval; a positive value means that SWOT + DAC departs somewhat more from the tide gauge. "
           "In red, intervals lying entirely above zero.")

main = [D.fila(s, tr) for s, tr, rol in D.combinaciones() if rol == "principal"]
largas = [f for f in main if f.n >= 20]
c1, c2, c3 = st.columns(3)
with c1:
    E.hallazgo("SWOT + DAC does follow the tide gauge",
               f"r = {E.num(min(f.A_r for f in largas))}–{E.num(max(f.A_r for f in largas))} in the six series "
               f"with 23–25 pairs (Langosteira, with 7 pairs, reaches {E.num(D.fila('langosteira_2', 197).A_r)}).")
with c2:
    E.hallazgo("…but the DAC alone gets just as far",
               f"r = {E.num(min(f.B_r for f in main))}–{E.num(max(f.B_r for f in main))} and a lower RMSE "
               f"without offset in the {len(main)} main combinations.")
with c3:
    E.hallazgo("…and the difference is not conclusive",
               f"ΔRMSE from {E.signo(min(f.dRMSE_AB_cm for f in main))} to {E.signo(max(f.dRMSE_AB_cm for f in main))}"
               f" cm, with every interval including zero: no demonstrable improvement or degradation.")

st.markdown("### How to read it")
st.markdown(
    "This **does not mean that SWOT adds nothing**. It means that, in these ports, most of the non-tidal sea "
    "level variation seen by the tide gauge is the response to pressure and wind, and the atmospheric model "
    "already captures it. A high correlation with the tide gauge does not, by itself, demonstrate a contribution "
    "from the satellite: it has to be compared with that of the atmospheric model.")

with st.expander("Technical detail: what remains after removing the DAC (comparison C)"):
    filas_c = [{"Station": D.nombre(s), "Track": tr, "n": int(D.fila(s, tr).n),
                "r A (SWOT + DAC)": D.fila(s, tr).A_r, "r B (DAC alone)": D.fila(s, tr).B_r,
                "r C (SWOT − DAC on both sides)": D.fila(s, tr).C_r}
               for s, tr, rol in D.combinaciones() if rol == "principal"]
    st.dataframe(pd.DataFrame(filas_c), hide_index=True, use_container_width=True,
                 column_config={c: st.column_config.NumberColumn(format="%.2f")
                                for c in ("r A (SWOT + DAC)", "r B (DAC alone)", "r C (SWOT − DAC on both sides)")})
    st.markdown(
        "Comparison C sets the SWOT anomaly (without DAC) against the tide gauge residual minus the DAC. The "
        f"association that remains is moderate (r = {E.num(min(f.C_r for f in largas))}–"
        f"{E.num(max(f.C_r for f in largas))} in the long series). On its own it does not prove independent "
        "oceanic information from SWOT: it may include the discrepancy shared by the stations "
        "(see *Regional pattern*).")

with st.expander("Technical detail: why the DAC explains so much"):
    st.markdown(
        "The DAC (*Dynamic Atmospheric Correction*) represents the response of the ocean to wind and atmospheric "
        "pressure. The barotropic model on which it is based substantially reduced the sea level variability at "
        "tide gauges with respect to the inverted barometer "
        "(Carrère and Lyard, 2003). When the non-tidal variability at a port is dominated by that response, "
        "SWOT + DAC inherits most of its agreement from the DAC.\n\n"
        "The intervals treat the passes as independent. With a positive temporal dependence between consecutive "
        "passes they could be somewhat narrow, which reinforces the cautious reading: no station shows a "
        "conclusive difference in either direction.")
