"""Sensibilidad al radio de búsqueda (6, 8 y 10 km) sobre la muestra común de cada estación y track."""
import pandas as pd
import streamlit as st

from nucleo import datos as D
from nucleo import estilo as E
from nucleo import graficos as G

E.cabecera(
    "Results · Search radius",
    "Does the comparison improve closer to the port?",
    "It seems intuitive that the closer to the tide gauge the pixels are taken, the more SWOT will resemble what "
    "the port measures. We repeat the comparison with circles of <b>6, 8 and 10 km</b> on the same passes. "
    "Result: reducing the circle leaves fewer valid pixels and, in general, does <b>not</b> bring SWOT closer to "
    "the tide gauge.",
)

track = st.segmented_control("Track", options=list(D.TRACKS), default=197,
                             format_func=lambda t: f"Track {t}") or 197
st.plotly_chart(G.radio_track(track, D.principales(track)), use_container_width=True)
st.caption("Main stations; same passes at the three radii (common sample). Left: ΔRMSE A − B "
           "(SWOT + DAC minus DAC alone) with its 95 % CI. Right: median of valid pixels per pass, on a "
           "logarithmic scale.")

ferrol6 = D.fila("ferrol", 197, 6, "común")
ferrol10 = D.fila("ferrol", 197, 10, "común")
coruna6 = D.fila("coruna", 197, 6, "común")
coruna10 = D.fila("coruna", 197, 10, "común")
c1, c2, c3 = st.columns(3)
with c1:
    E.hallazgo("Smaller circle, much less water",
               f"At A Coruña (T197) the valid pixels fall from {coruna10.sample_median_pixels:.0f}"
               f" to {coruna6.sample_median_pixels:.0f}, and at Ferrol from "
               f"{ferrol10.sample_median_pixels:.0f} to {ferrol6.sample_median_pixels:.0f} per pass.")
with c2:
    E.hallazgo("Where water is lacking, the comparison gets worse",
               f"Ferrol at 6 km: the RMSE of SWOT + DAC rises from {E.num(ferrol10.A_rmse_wo_offset_cm, 1)} to "
               f"{E.num(ferrol6.A_rmse_wo_offset_cm, 1)} cm and ΔRMSE is {E.signo(ferrol6.dRMSE_AB_cm)} cm "
               f"{E.intervalo(ferrol6.dRMSE_AB_ci_low, ferrol6.dRMSE_AB_ci_high)}, above zero.")
with c3:
    var_b = max(max(D.fila(s, tr, r, "común").B_rmse_wo_offset_cm for r in D.RADIOS)
                - min(D.fila(s, tr, r, "común").B_rmse_wo_offset_cm for r in D.RADIOS)
                for tr in D.TRACKS for s in D.principales(tr))
    E.hallazgo("The atmospheric model does not change",
               f"The RMSE of the DAC alone varies by at most {E.num(var_b, 2)} cm between radii. What changes with "
               "the radius is what SWOT sees in each circle.")

E.nota("<b>No “optimal” radius was sought.</b> Choosing the radius that best agrees with the tide gauge would "
       "bias the validation towards the tide gauge itself. 10 km is the reference, and 6 and 8 km are a "
       "sensitivity analysis.")

with st.expander("Technical detail: table by radius (common sample)"):
    filas = []
    for s in D.principales(track):
        for r in D.RADIOS:
            f = D.fila(s, track, r, "común")
            filas.append({"Station": D.nombre(s), "Radius (km)": r, "n": int(f.n),
                          "Pixels (median)": f.sample_median_pixels, "Offset (cm)": f.A_bias_cm,
                          "r A": f.A_r, "RMSE A (cm)": f.A_rmse_wo_offset_cm, "RMSE B (cm)": f.B_rmse_wo_offset_cm,
                          "ΔRMSE A − B (cm)": f.dRMSE_AB_cm, "CI low": f.dRMSE_AB_ci_low,
                          "CI high": f.dRMSE_AB_ci_high})
    tabla = pd.DataFrame(filas)
    st.dataframe(tabla, hide_index=True, use_container_width=True,
                 column_config={c: st.column_config.NumberColumn(format="%.2f" if c == "r A" else "%.1f")
                                for c in tabla.columns[3:]})
    st.markdown(
        "- **Common sample:** only the cycles valid at all three radii, so that the differences between radii do "
        "not come from a change of sample. That is why the values at 10 km may differ slightly from those in the "
        "explorer (Ferrol on T197 has 23 common pairs instead of 24).\n"
        "- **The intervals compare A with B at each radius**; the differences between radii are described, not "
        "tested.\n"
        "- **The offset depends on the radius where the coverage changes** (Ferrol T197: from "
        f"{E.signo(ferrol10.A_bias_cm)} cm at 10 km to {E.signo(ferrol6.A_bias_cm)} cm at 6 km): it is not a "
        "property of the station independent of the search area.")

with st.expander("Technical detail: the exploratory cases in the rías"):
    st.markdown(
        "At Marín and Vigo on track 197, the correlation of SWOT + DAC with the tide gauge is **negative** "
        f"(r = {E.num(D.fila('marin', 197).A_r)} and {E.num(D.fila('vigo', 197).A_r)} at 10 km), whereas that of "
        f"the DAC alone is positive ({E.num(D.fila('marin', 197).B_r)} and {E.num(D.fila('vigo', 197).B_r)}). The "
        "scarce coverage and some passes of uncertain quality or representativeness prevent attributing that "
        "disagreement to the accuracy of SWOT. At Marín, on track 154, the circle sees a median of only 36 valid "
        "pixels per pass.")
