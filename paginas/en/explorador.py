"""Explorador por estación: serie por paso, métricas A/B/C, cobertura y tabla de pasos."""
import numpy as np
import pandas as pd
import streamlit as st

from nucleo import datos as D
from nucleo import estilo as E
from nucleo import graficos as G
from nucleo import textos as T

E.cabecera(
    "Results · Explorer",
    "Pass by pass, station by station",
    "Choose a station, a track and a search circle. Each point is a SWOT pass with its tide gauge value at the "
    "same time. The purple line is SWOT with the atmospheric correction restored; the dashed green one, the "
    "atmospheric model alone. <b>If SWOT measurably improved on the atmospheric model, the purple line would "
    "come closer to the black one than the green one does.</b>",
)

c1, c2, c3 = st.columns([2, 1, 1])
track = c2.segmented_control("Track", options=list(D.TRACKS), default=197,
                             format_func=lambda t: f"Track {t}") or 197
opciones = D.principales(track) + D.exploratorias(track)
station = c1.selectbox("Station", opciones, format_func=lambda s: (
    f"{D.nombre(s)} · {'main' if s in D.principales(track) else 'exploratory'}"))
radio = c3.segmented_control("Radius", options=list(D.RADIOS), default=D.RADIO_REF,
                             format_func=lambda r: f"{r} km") or D.RADIO_REF

f = D.fila(station, track, radio, "propia")
f10 = D.fila(station, track)
df = D.serie(station, track, radio)
ok = D.validos(df)

st.markdown(f"#### {D.nombre(station)} · track {track} · {radio} km &nbsp; {E.papel(f10.role)}",
            unsafe_allow_html=True)
if T.condicion(station, track):
    E.nota(f"<b>Condition:</b> {T.condicion(station, track)}")

if f is None or pd.isna(f.A_r):
    E.aviso(f"With {len(ok)} valid pairs at {radio} km no metrics are computed (minimum 5).")
    st.stop()

E.tarjetas([
    (f"{int(f.n)}", "valid pairs (passes with SWOT and tide gauge)"),
    (f"{E.num(f.A_r)} / {E.num(f.B_r)}", "correlation r of SWOT + DAC / of the DAC alone"),
    (f"{E.num(f.A_rmse_wo_offset_cm, 1)} / {E.num(f.B_rmse_wo_offset_cm, 1)} cm",
     "RMSE without offset of SWOT + DAC / of the DAC alone"),
    (f"{E.signo(f.dRMSE_AB_cm)} cm", f"ΔRMSE A − B, 95 % CI {E.intervalo(f.dRMSE_AB_ci_low, f.dRMSE_AB_ci_high)}"),
    (f"{E.signo(f.A_bias_cm)} cm", "mean offset SWOT + DAC − tide gauge (descriptor)"),
])

if f.dRMSE_AB_ci_low > 0:
    lectura = ("Here SWOT + DAC departs from the tide gauge <b>more</b> than the DAC alone, and the interval does "
               "not include zero.")
elif f.dRMSE_AB_ci_high < 0:
    lectura = "Here SWOT + DAC comes closer to the tide gauge than the DAC alone, and the interval does not include zero."
else:
    lectura = ("The difference between SWOT + DAC and the DAC alone is not conclusive: the interval includes zero.")
E.nota(lectura)

st.plotly_chart(G.serie_estacion(ok, float(f.A_bias_cm)), use_container_width=True)
st.caption("The mean offset of SWOT + DAC is subtracted to compare the shape of the series; the offset includes "
           "the difference between the vertical references of the two systems.")

a, b = st.columns([1, 1])
with a:
    st.markdown("**Satellite and model against the tide gauge**")
    st.plotly_chart(G.dispersion_ab(ok, float(f.A_bias_cm)), use_container_width=True)
with b:
    st.markdown("**SWOT coverage in the circle, by cycle**")
    st.plotly_chart(G.cobertura(df), use_container_width=True)
    st.caption(f"Median of valid pixels in the pairs: {f.sample_median_pixels:.0f} · 1 km segments: "
               f"{f.sample_median_segments:.0f} · spatial dispersion: {f.sample_median_dispersion_cm:.1f} cm.")

with st.expander("Full metrics (comparisons A, B and C)"):
    m = pd.DataFrame([
        {"Comparison": "A · SWOT + DAC against the tide gauge", "r": f.A_r,
         "Minimum leave-one-out r": f.A_r_loo_min, "RMSE without offset (cm)": f.A_rmse_wo_offset_cm,
         "Total RMSE (cm)": f.A_rmse_total_cm, "Offset (cm)": f.A_bias_cm, "Slope": f.A_slope},
        {"Comparison": "B · DAC alone against the tide gauge", "r": f.B_r,
         "RMSE without offset (cm)": f.B_rmse_wo_offset_cm, "Total RMSE (cm)": f.B_rmse_total_cm},
        {"Comparison": "C · SWOT anomaly against tide gauge − DAC", "r": f.C_r},
    ])
    st.dataframe(m, hide_index=True, use_container_width=True,
                 column_config={c: st.column_config.NumberColumn(format="%.2f") for c in m.columns[1:]})
    st.markdown(
        "- **Mean offset:** mean of SWOT + DAC − tide gauge. It is a descriptor, not a SWOT error: it includes "
        "the difference between the mean sea surface and the harbour datum, which is not transformed.\n"
        "- **RMSE without offset:** root mean square error after removing that offset; it measures whether the "
        "two series rise and fall together.\n"
        "- **ΔRMSE A − B:** difference in RMSE between SWOT + DAC and the DAC alone, with a 95 % confidence "
        "interval from a paired bootstrap over the passes (10 000 resamples). It assumes independent passes; with "
        "positive temporal dependence, the intervals could be somewhat narrow.\n"
        "- **C** has the same offset and RMSE as A, but a different r: it measures the association that remains "
        "after removing the DAC from both sides. On its own it does not prove independent oceanic information.")

with st.expander("Table of passes (including the excluded ones and their reason)"):
    tabla = df[["cycle", "status", "exclusion_reason", "pass_time_utc", "pixels_in_circle", "pixels_after_mad",
                "n_segments", "swot_corrected", "dac_median", "tg_residual", "difference"]].copy()
    tabla["status"] = np.where(tabla.status == "ok", "valid", "excluded")
    tabla["exclusion_reason"] = tabla.exclusion_reason.map(T.motivos())
    for c in ("swot_corrected", "dac_median", "tg_residual", "difference"):
        tabla[c] = 100 * tabla[c]
    tabla.columns = ["Cycle", "Status", "Reason", "Pass time (UTC)", "Pixels in the circle",
                     "Pixels used", "1 km segments", "SWOT + DAC (cm)", "DAC (cm)", "Tide gauge (cm)",
                     "d (cm)"]
    st.dataframe(tabla, hide_index=True, use_container_width=True,
                 column_config={c: st.column_config.NumberColumn(format="%.1f")
                                for c in ("SWOT + DAC (cm)", "DAC (cm)", "Tide gauge (cm)", "d (cm)")})
    st.download_button("Download the series (CSV)", df.to_csv(index=False).encode(),
                       file_name=f"{station}_t{track}_r{radio}km.csv", mime="text/csv")
