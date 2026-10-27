"""Análisis regional: discrepancia compartida, persistencia entre tracks y asociación con las predicciones de marea."""
import pandas as pd
import streamlit as st

from nucleo import datos as D
from nucleo import estilo as E
from nucleo import graficos as G

E.cabecera(
    "Results · Regional pattern",
    "A discrepancy shared by the stations",
    "When the SWOT − tide gauge difference is examined pass by pass, something unexpected appears: on the north "
    "coast it <b>rises and falls at the same time at all the stations</b>, repeats in the two satellite passes and "
    "closely follows the difference between the two tide predictions. The stations are therefore not independent "
    "tests, and this pattern is analysed separately from the results by station.",
)

E.aviso("<b>Association is not causation.</b> All the variables analysed here are part of the SWOT − tide gauge "
        "difference itself, so their resemblance to it is not independent proof of what causes it.")

# ---------------------------------------------------------------- 1
st.markdown("### 1 · The stations move together")
track = st.segmented_control("Track", options=list(D.TRACKS), default=197,
                             format_func=lambda t: f"Track {t}", key="track_d") or 197
st.plotly_chart(G.regional_d(track), use_container_width=True)
cmp = D.estaciones_cmp(track).set_index("station")
ref = D.REFERENCIA_MODO_COMUN[track]
std_cm = D.tracks_json()["cross_track"]["std_common_mode_cm"][f"t{track}"]
st.caption(f"Per-pass difference of each reference station, centred (its mean is subtracted), and their mean: the "
           f"**common mode** of track {track} (standard deviation {E.num(std_cm, 1)} cm).")
filas = [{"Station": D.nombre(s), "r with the common mode of the others": cmp.loc[s, "r_common_mode"],
          "Own dispersion (cm)": cmp.loc[s, "own_part_cm"], "n": int(cmp.loc[s, "n_common_mode"])}
         for s in cmp.index if s in ref or s in ("langosteira_2", "villagarcia")]
a, b = st.columns([3, 2])
a.dataframe(pd.DataFrame(filas), hide_index=True, use_container_width=True,
            column_config={"r with the common mode of the others": st.column_config.NumberColumn(format="%.2f"),
                           "Own dispersion (cm)": st.column_config.NumberColumn(format="%.1f")})
b.markdown("The **r** of each station is computed with the common mode of the *others* (without it). The **own "
           "dispersion** is the standard deviation of its difference with respect to that common mode: much smaller "
           "than the variability of the common mode itself.")

# ---------------------------------------------------------------- 2
st.markdown("### 2 · It repeats in the two passes, 37 hours apart")
ct = D.tracks_json()["cross_track"]
a, b = st.columns([3, 2])
with a:
    st.plotly_chart(G.entre_tracks(), use_container_width=True, config={"displayModeBar": False})
with b:
    st.markdown(f"The track 197 pass occurs **{E.num(ct['hours_t197_minus_t154']['median'], 1)} h** after the "
                f"track 154 pass in the same cycle. In the {ct['common_mode_t154_vs_t197']['n']} cycles valid on "
                "both, the common modes almost coincide.")
    comp = pd.DataFrame([
        {"Signal": "Common mode of the difference", "r between tracks": ct["common_mode_t154_vs_t197"]["r"]},
        {"Signal": "SWOT anomaly at A Coruña", "r between tracks": ct["reference_coruna_swot_l3_t154_vs_t197"]["r"]},
        {"Signal": "DAC − tide gauge at A Coruña", "r between tracks": ct["reference_coruna_dac_error_t154_vs_t197"]["r"]},
        {"Signal": "DAC at A Coruña", "r between tracks": ct["reference_coruna_dac_t154_vs_t197"]["r"]},
        {"Signal": "Tide gauge residual at A Coruña",
         "r between tracks": ct["reference_coruna_tg_residual_t154_vs_t197"]["r"]},
    ])
    st.dataframe(comp, hide_index=True, use_container_width=True,
                 column_config={"r between tracks": st.column_config.NumberColumn(format="%.2f")})
    st.caption("The shared discrepancy persists between passes more than the sea level measured by the tide gauge "
               "itself (descriptive comparison of correlations, not tested).")

with st.expander("Technical detail: robustness of the persistence between tracks"):
    rb = D.robustez(10)
    cross = rb[rb.group == "cross_track"].iloc[0]
    pm = D.persistencia_mareografos()
    sets = pm[pm.group == "common_mode_sets_same_cycles"]
    disj = sets[sets.disjoint_tide_gauges.astype(bool)]
    shar = sets[~sets.disjoint_tide_gauges.astype(bool)]
    radios = {r: D.robustez(r, comun=True) for r in D.RADIOS}
    rr = {r: radios[r][radios[r].group == "cross_track"].iloc[0] for r in D.RADIOS}
    st.markdown(
        f"- **Trend:** after removing a linear trend from each series, r = {E.num(cross.r_detrended)}.\n"
        f"- **Individual cycles:** leaving out one cycle at a time, r between {E.num(cross.loo_min_r)} and "
        f"{E.num(cross.loo_max_r)}.\n"
        f"- **Sets of tide gauges:** combinations of stations that share no tide gauge between tracks give "
        f"r = {E.num(disj.r.min())}–{E.num(disj.r.max())}; those that share some, "
        f"{E.num(shar.r.min())}–{E.num(shar.r.max())}. The non-shared tide gauges still belong to the same "
        f"network and processing.\n"
        f"- **Radius:** on the cycles valid at all three radii (n = {int(rr[10].n)}), r = "
        f"{', '.join(E.num(rr[r].r) for r in D.RADIOS)} at 6, 8 and 10 km "
        f"({', '.join(E.num(rr[r].r_detrended) for r in D.RADIOS)} detrended).")

# ---------------------------------------------------------------- 3
st.markdown("### 3 · It follows the difference between the two tide predictions")
a, b = st.columns([3, 2])
with a:
    st.plotly_chart(G.modo_comun_mareas(), use_container_width=True, config={"displayModeBar": False})
with b:
    st.markdown("Each system removes the tide with its own prediction: SWOT with a **global model** (FES2022 and "
                "the HRET internal tide) and the tide gauge with the **harmonic prediction of Puertos del Estado**. "
                "If those two predictions differ, the difference passes directly into the comparison.")
    var = {"tide_prediction_difference_m": "Tide gauge prediction − SWOT tide",
           "agg_ssha_unfiltered": "SWOT anomaly", "agg_dac": "DAC", "tg_residual": "Tide gauge residual"}
    filas = [{"Variable (track mean)": etq,
              "r · T197": D.r_guardada(197, v)[0], "r · T154": D.r_guardada(154, v)[0]} for v, etq in var.items()]
    st.dataframe(pd.DataFrame(filas), hide_index=True, use_container_width=True,
                 column_config={c: st.column_config.NumberColumn(format="%.2f") for c in ("r · T197", "r · T154")})
    st.caption("Correlation of each component with the common mode. The prediction difference is the strongest "
               "on both tracks.")

rob = D.robustez_descomp()
rt = {tr: rob[(rob.track == tr) & (rob.scope == "track_mean_vs_common_mode")
              & (rob.variable == "tide_prediction_difference_m")].iloc[0] for tr in D.TRACKS}
st_ = rob[(rob.scope == "station_vs_own_d") & (rob.variable == "tide_prediction_difference_m")]
st.markdown(
    f"The association holds **at each reference station** (r = {E.num(st_.r.min())}–{E.num(st_.r.max())}), "
    f"after removing the trend (r = {E.num(rt[197].r_detrended)} on T197 and {E.num(rt[154].r_detrended)} on T154) "
    f"and leaving out one cycle at a time (r ≥ {E.num(rt[197].loo_min)} and {E.num(rt[154].loo_min)}).")

st.markdown("### A possible explanation: the annual tide")
E.hallazgo(
    "Hypothesis: the annual and semiannual constituents (Sa and Ssa)",
    "At tide gauges, the annual and semiannual tidal constituents mainly capture the seasonal cycle of sea level, "
    "dominated by meteorology rather than astronomy; at European tide gauges they amount to several centimetres "
    "(Ray et al., 2021). The SWOT tide correction, by contrast, includes only the small astronomical part. If the "
    "Puertos del Estado prediction includes Sa and Ssa fitted to each record, it removes from the tide gauge a "
    "seasonal cycle that SWOT retains, and that difference would appear precisely as a slow, common and "
    "persistent discrepancy, contained in the prediction difference. <b>Testing it requires the exact constants "
    "of the prediction, which are not published: for now it is a hypothesis, not a result.</b>")

with st.expander("Technical detail: what else the prediction difference contains"):
    st.markdown(
        "- **Load tide:** the altimeter measures geocentric heights and its tide correction includes the load "
        "tide; the tide gauge measures relative to the crust, which moves with it. Removing its own prediction "
        "on each side is consistent, but the *prediction difference* contains the load tide by construction, "
        "even with perfect models. That part is expected and does not indicate an error.\n"
        "- **Location:** one prediction is evaluated at the port and the other at the pixels, so the difference "
        "also includes the real spatial variation of the tide and the errors of both predictions near the "
        "coast.\n"
        "- For all these reasons, the association **does not attribute** the discrepancy to a specific model.")

with st.expander("Technical detail: per-pass components against the common mode"):
    tr = st.segmented_control("Track ", options=list(D.TRACKS), default=197,
                              format_func=lambda t: f"Track {t}", key="track_comp") or 197
    st.plotly_chart(G.componentes(tr), use_container_width=True)
    st.caption("Each component centred by station over the common cycles of the track; in black, their mean. "
               "All of them are algebraically related to d.")
