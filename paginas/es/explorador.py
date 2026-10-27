"""Explorador por estación: serie por paso, métricas A/B/C, cobertura y tabla de pasos."""
import numpy as np
import pandas as pd
import streamlit as st

from nucleo import datos as D
from nucleo import estilo as E
from nucleo import graficos as G
from nucleo import textos as T

E.cabecera(
    "Resultados · Explorador",
    "Paso a paso, estación a estación",
    "Elige una estación, una pasada y un círculo de búsqueda. Cada punto es un paso de SWOT con su valor del "
    "mareógrafo a la misma hora. La línea morada es SWOT con la corrección atmosférica devuelta; la verde "
    "discontinua, el modelo atmosférico solo. <b>Si SWOT mejorara de forma medible al modelo atmosférico, la "
    "morada se acercaría a la negra más que la verde.</b>",
)

c1, c2, c3 = st.columns([2, 1, 1])
track = c2.segmented_control("Track", options=list(D.TRACKS), default=197,
                             format_func=lambda t: f"Track {t}") or 197
opciones = D.principales(track) + D.exploratorias(track)
station = c1.selectbox("Estación", opciones, format_func=lambda s: (
    f"{D.nombre(s)} · {'principal' if s in D.principales(track) else 'exploratoria'}"))
radio = c3.segmented_control("Radio", options=list(D.RADIOS), default=D.RADIO_REF,
                             format_func=lambda r: f"{r} km") or D.RADIO_REF

f = D.fila(station, track, radio, "propia")
f10 = D.fila(station, track)
df = D.serie(station, track, radio)
ok = D.validos(df)

st.markdown(f"#### {D.nombre(station)} · track {track} · {radio} km &nbsp; {E.papel(f10.role)}",
            unsafe_allow_html=True)
if T.condicion(station, track):
    E.nota(f"<b>Condición:</b> {T.condicion(station, track)}")

if f is None or pd.isna(f.A_r):
    E.aviso(f"Con {len(ok)} pares válidos a {radio} km no se calculan métricas (mínimo 5).")
    st.stop()

E.tarjetas([
    (f"{int(f.n)}", "pares válidos (pasos con SWOT y mareógrafo)"),
    (f"{E.num(f.A_r)} / {E.num(f.B_r)}", "correlación r de SWOT + DAC / del DAC solo"),
    (f"{E.num(f.A_rmse_wo_offset_cm, 1)} / {E.num(f.B_rmse_wo_offset_cm, 1)} cm",
     "RMSE sin desplazamiento de SWOT + DAC / del DAC solo"),
    (f"{E.signo(f.dRMSE_AB_cm)} cm", f"ΔRMSE A − B, IC 95 % {E.intervalo(f.dRMSE_AB_ci_low, f.dRMSE_AB_ci_high)}"),
    (f"{E.signo(f.A_bias_cm)} cm", "desplazamiento medio SWOT + DAC − mareógrafo (descriptor)"),
])

if f.dRMSE_AB_ci_low > 0:
    lectura = ("Aquí SWOT + DAC se aleja del mareógrafo <b>más</b> que el DAC solo, y el intervalo no incluye el "
               "cero.")
elif f.dRMSE_AB_ci_high < 0:
    lectura = "Aquí SWOT + DAC se acerca al mareógrafo más que el DAC solo, y el intervalo no incluye el cero."
else:
    lectura = ("La diferencia entre SWOT + DAC y el DAC solo no es concluyente: el intervalo incluye el cero.")
E.nota(lectura)

st.plotly_chart(G.serie_estacion(ok, float(f.A_bias_cm)), use_container_width=True)
st.caption("A SWOT + DAC se le resta su desplazamiento medio para comparar la forma de las series; el "
           "desplazamiento incluye la diferencia entre las referencias verticales de los dos sistemas.")

a, b = st.columns([1, 1])
with a:
    st.markdown("**Satélite y modelo frente al mareógrafo**")
    st.plotly_chart(G.dispersion_ab(ok, float(f.A_bias_cm)), use_container_width=True)
with b:
    st.markdown("**Cobertura de SWOT en el círculo, por ciclo**")
    st.plotly_chart(G.cobertura(df), use_container_width=True)
    st.caption(f"Mediana de píxeles válidos en los pares: {f.sample_median_pixels:.0f} · tramos de 1 km: "
               f"{f.sample_median_segments:.0f} · dispersión espacial: {f.sample_median_dispersion_cm:.1f} cm.")

with st.expander("Métricas completas (comparaciones A, B y C)"):
    m = pd.DataFrame([
        {"Comparación": "A · SWOT + DAC frente al mareógrafo", "r": f.A_r,
         "r mínima dejando un paso fuera": f.A_r_loo_min, "RMSE sin desplazamiento (cm)": f.A_rmse_wo_offset_cm,
         "RMSE total (cm)": f.A_rmse_total_cm, "Desplazamiento (cm)": f.A_bias_cm, "Pendiente": f.A_slope},
        {"Comparación": "B · DAC solo frente al mareógrafo", "r": f.B_r,
         "RMSE sin desplazamiento (cm)": f.B_rmse_wo_offset_cm, "RMSE total (cm)": f.B_rmse_total_cm},
        {"Comparación": "C · anomalía SWOT frente a mareógrafo − DAC", "r": f.C_r},
    ])
    st.dataframe(m, hide_index=True, use_container_width=True,
                 column_config={c: st.column_config.NumberColumn(format="%.2f") for c in m.columns[1:]})
    st.markdown(
        "- **Desplazamiento medio:** media de SWOT + DAC − mareógrafo. Es un descriptor, no un error de SWOT: "
        "incluye la diferencia entre la superficie media del mar y el cero del puerto, que no se transforma.\n"
        "- **RMSE sin desplazamiento:** error cuadrático medio tras retirar ese desplazamiento; mide si las dos "
        "series suben y bajan juntas.\n"
        "- **ΔRMSE A − B:** diferencia de RMSE entre SWOT + DAC y el DAC solo, con intervalo de confianza del 95 % "
        "por bootstrap pareado sobre los pasos (10 000 remuestreos). Supone pasos independientes; con dependencia "
        "temporal positiva, los intervalos podrían ser algo estrechos.\n"
        "- **C** tiene el mismo desplazamiento y RMSE que A, pero una r distinta: mide la asociación que queda "
        "tras retirar el DAC de los dos lados. No prueba por sí sola información oceánica independiente.")

with st.expander("Tabla de pasos (incluidos los excluidos y su motivo)"):
    tabla = df[["cycle", "status", "exclusion_reason", "pass_time_utc", "pixels_in_circle", "pixels_after_mad",
                "n_segments", "swot_corrected", "dac_median", "tg_residual", "difference"]].copy()
    tabla["status"] = np.where(tabla.status == "ok", "válido", "excluido")
    tabla["exclusion_reason"] = tabla.exclusion_reason.map(T.motivos())
    for c in ("swot_corrected", "dac_median", "tg_residual", "difference"):
        tabla[c] = 100 * tabla[c]
    tabla.columns = ["Ciclo", "Estado", "Motivo", "Hora del paso (UTC)", "Píxeles en el círculo",
                     "Píxeles usados", "Tramos de 1 km", "SWOT + DAC (cm)", "DAC (cm)", "Mareógrafo (cm)",
                     "d (cm)"]
    st.dataframe(tabla, hide_index=True, use_container_width=True,
                 column_config={c: st.column_config.NumberColumn(format="%.1f")
                                for c in ("SWOT + DAC (cm)", "DAC (cm)", "Mareógrafo (cm)", "d (cm)")})
    st.download_button("Descargar la serie (CSV)", df.to_csv(index=False).encode(),
                       file_name=f"{station}_t{track}_r{radio}km.csv", mime="text/csv")
