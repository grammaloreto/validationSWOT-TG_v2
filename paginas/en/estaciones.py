"""Estaciones, trazas y datos: dónde se compara, con qué papel y cuántos pasos quedan."""
import pandas as pd
import streamlit as st

from nucleo import datos as D
from nucleo import estilo as E
from nucleo import graficos as G
from nucleo import textos as T

E.cabecera(
    "Results · Stations and data",
    "Seven ports, two satellite passes",
    "SWOT crosses Galicia in two passes, <b>tracks 197 and 154</b>, once every 21 days. Around each tide gauge a "
    "search circle is taken and the satellite pixels are compared with the port's record. "
    "Not all combinations are equally useful: some are <b>main results</b> and others are analysed as "
    "<b>exploratory cases</b>, with their condition in view.",
)

c1, c2 = st.columns([3, 2])
with c2:
    radio = st.segmented_control("Search circle", options=list(D.RADIOS), default=D.RADIO_REF,
                                 format_func=lambda r: f"{r} km") or D.RADIO_REF
    track_rol = st.segmented_control("Role by track", options=[197, 154], default=197,
                                     format_func=lambda t: f"Track {t}") or 197
    papeles = {s: "principal" for s in D.principales(track_rol)}
    papeles.update({s: "exploratoria" for s in D.exploratorias(track_rol)})
    filas = []
    for s in D.ORDEN:
        fila = {"Station": D.nombre(s)}
        for tr in D.TRACKS:
            f = D.fila(s, tr)
            marca = "● main" if f is not None and f.role == "principal" else "○ explor."
            fila[f"Track {tr}"] = "—" if f is None else f"{marca} · {int(f.n)}"
        filas.append(fila)
    st.dataframe(pd.DataFrame(filas), hide_index=True, use_container_width=True,
                 column_config={"Station": st.column_config.TextColumn(width="small")})
    st.caption("Role at 10 km and number of valid pairs on each track.")
    E.nota("A combination is <b>main</b> if it has sufficient SWOT and tide gauge coverage; "
           "<b>exploratory</b> ones are shown separately and are not included in the synthesis.")
with c1:
    st.plotly_chart(G.mapa(radio, papeles), use_container_width=True, config={"displayModeBar": False})
    st.caption(f"Circles of {radio} km. In colour with a solid line, main stations of track {track_rol}; "
               "in dotted grey, exploratory ones. The tracks are the nadir of the reference pass of each track "
               "(SWOT measures over a wide swath on both sides of that line). Coastline: Natural Earth 10 m. "
               "Hover over a station to see its setting.")

st.markdown("### How many passes make it to the comparison")
st.markdown(
    "Of the 29 cycles, not all give a valid pair: sometimes the tide gauge did not record that day, sometimes SWOT "
    "returned no data over the circle, and sometimes one of the two hours around the pass is missing. "
    "**No pass is excluded because of how well it agrees with the tide gauge**: only for lack of data.")

ex = D.resumen_exclusiones()
ex = ex[ex.radius_km == radio]
resumen = (ex.assign(Reason=ex.exclusion_reason.map(T.motivos()).fillna("Valid pair"))
             .groupby(["track", "Reason"]).size().unstack("track").fillna(0).astype(int))
resumen.columns = [f"Track {c}" for c in resumen.columns]
orden = ["Valid pair"] + [m for m in T.motivos().values() if m in resumen.index]
st.dataframe(resumen.loc[orden], use_container_width=True)
st.caption(f"Count of passes by reason, summing the seven stations, at {radio} km.")

with st.expander("Technical detail: data sources"):
    st.markdown(
        "- **SWOT:** L3 LR SSH *Unsmoothed* product v2.0.1 (CLS/CNES, AVISO), variable `ssha_unfiltered`, "
        "with `dac`, `quality_flag` and `time` per pixel. 21-day science phase, cycles 1–29.\n"
        "- **Tide gauges:** hourly records of the REDMAR network of Puertos del Estado, unmodified. Each record "
        "provides the sea level, the astronomical prediction and their difference (meteorological residual). The "
        "hourly series are filtered averages of the high-frequency record.\n"
        "- **Langosteira** is REDMAR station 3213 (quay A3), the only one in that port with clear instrument "
        "provenance. An alternative record under the same name is excluded from the analysis.\n"
        "- **Names** as in the REDMAR network (San Cibrao, A Coruña, Ferrol, Langosteira, Villagarcía, Marín, "
        "Vigo).")
