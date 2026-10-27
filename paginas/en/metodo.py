"""Método por paso y limitaciones."""
import streamlit as st

from nucleo import estilo as E

E.cabecera(
    "Context · Method",
    "How each figure is obtained",
    "A summary of the method used to compare SWOT with the tide gauges, and of its limitations.",
)

tab_metodo, tab_limites = st.tabs(["Per-pass method", "Limitations"])

with tab_metodo:
    pasos = [
        ("1 · Pixels", "All pixels with a valid anomaly within a true circle of radius R around the tide gauge, "
                       "without subsampling; quality 0 only."),
        ("2 · DAC restored", "The atmospheric correction is added to the anomaly, because the tide gauge does "
                             "record the response to pressure and wind."),
        ("3 · Aggregation", "1 km segments along a fixed line per track; outliers by MAD within each segment; "
                            "pass value = median of the medians."),
        ("4 · Actual time", "The pass time is the median of the pixel times; the tide gauge is interpolated "
                            "between the two hours that bracket it."),
        ("5 · Metrics", "Across passes: A (SWOT + DAC), B (DAC alone) and C, on the same passes; offset as a "
                        "descriptor."),
    ]
    cols = st.columns(len(pasos))
    for c, (t, b) in zip(cols, pasos):
        with c:
            E.hallazgo(t, b)
    st.latex(r"\eta_{SWOT} = \mathcal{A}(S + D), \qquad \eta_{TG} = H_{TG}(t_p) - T_{TG}(t_p), \qquad "
             r"d = \eta_{SWOT} - \eta_{TG}")
    st.markdown(
        "It follows the **non-tidal** approach of Han et al. (2026): each system removes the tide with its own "
        "prediction (FES2022 and HRET for SWOT; the harmonic prediction of Puertos del Estado for the tide gauge) "
        "and the atmospheric response is retained on both sides. The vertical reference is not transformed: that "
        "is why the mean offset is a descriptor and the main metric is the RMSE without offset.\n\n"
        "**Design rules.** No filter or definition was chosen for its agreement with the tide gauge; no optimal "
        "radius was sought; the exploratory stations are presented separately with their condition.")

with tab_limites:
    st.markdown(
        "- **Small samples:** 23–25 pairs per main station (7 at Langosteira); wide intervals.\n"
        "- **Dependence:** the stations are not independent of each other, and the intervals assume independent "
        "passes, so they could be somewhat optimistic.\n"
        "- **Vertical reference:** not transformed; the altimeter measures in a geocentric frame and the tide gauge "
        "relative to the crust. Seasonal land motion is not treated.\n"
        "- **Puertos del Estado tide prediction:** its exact composition (long-period constituents) is not "
        "documented; the Sa/Ssa hypothesis remains open.\n"
        "- **Villagarcía:** offset of −47.9 cm on track 197 at 10 km, specific to that station; its cause cannot be "
        "determined with the available data and it is not interpreted.\n"
        "- **Rías:** at Marín and Vigo the valid coverage is scarce; their results are exploratory.")
