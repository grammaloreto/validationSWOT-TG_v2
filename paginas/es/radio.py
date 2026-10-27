"""Sensibilidad al radio de búsqueda (6, 8 y 10 km) sobre la muestra común de cada estación y track."""
import pandas as pd
import streamlit as st

from nucleo import datos as D
from nucleo import estilo as E
from nucleo import graficos as G

E.cabecera(
    "Resultados · Radio de búsqueda",
    "¿Mejora la comparación al acercarse al puerto?",
    "Parece intuitivo que, cuanto más cerca del mareógrafo se tomen los píxeles, más se parecerá SWOT a lo que "
    "mide el puerto. Repetimos la comparación con círculos de <b>6, 8 y 10 km</b> sobre los mismos pasos. "
    "Resultado: reducir el círculo deja menos píxeles válidos y, en general, <b>no</b> acerca SWOT al mareógrafo.",
)

track = st.segmented_control("Track", options=list(D.TRACKS), default=197,
                             format_func=lambda t: f"Track {t}") or 197
st.plotly_chart(G.radio_track(track, D.principales(track)), use_container_width=True)
st.caption("Estaciones principales; mismos pasos en los tres radios (muestra común). Izquierda: ΔRMSE A − B "
           "(SWOT + DAC menos DAC solo) con su IC 95 %. Derecha: mediana de píxeles válidos por paso, en escala "
           "logarítmica.")

ferrol6 = D.fila("ferrol", 197, 6, "común")
ferrol10 = D.fila("ferrol", 197, 10, "común")
coruna6 = D.fila("coruna", 197, 6, "común")
coruna10 = D.fila("coruna", 197, 10, "común")
c1, c2, c3 = st.columns(3)
with c1:
    E.hallazgo("Menos círculo, muchos menos píxeles válidos",
               f"En A Coruña (T197) los píxeles válidos caen de {coruna10.sample_median_pixels:.0f}"
               f" a {coruna6.sample_median_pixels:.0f}, y en Ferrol de "
               f"{ferrol10.sample_median_pixels:.0f} a {ferrol6.sample_median_pixels:.0f} por paso.")
with c2:
    E.hallazgo("Con muy poca cobertura válida, la comparación puede empeorar",
               f"Ferrol a 6 km: el RMSE de SWOT + DAC sube de {E.num(ferrol10.A_rmse_wo_offset_cm, 1)} a "
               f"{E.num(ferrol6.A_rmse_wo_offset_cm, 1)} cm y el ΔRMSE es {E.signo(ferrol6.dRMSE_AB_cm)} cm "
               f"{E.intervalo(ferrol6.dRMSE_AB_ci_low, ferrol6.dRMSE_AB_ci_high)}, por encima de cero.")
with c3:
    var_b = max(max(D.fila(s, tr, r, "común").B_rmse_wo_offset_cm for r in D.RADIOS)
                - min(D.fila(s, tr, r, "común").B_rmse_wo_offset_cm for r in D.RADIOS)
                for tr in D.TRACKS for s in D.principales(tr))
    E.hallazgo("El modelo atmosférico no cambia",
               f"El RMSE del DAC solo varía como mucho {E.num(var_b, 2)} cm entre radios. Lo que cambia con el "
               "radio es lo que ve SWOT en cada círculo.")

E.nota("<b>No se buscó un radio «óptimo».</b> Elegir el radio que mejor concuerda con el mareógrafo sesgaría la "
       "validación hacia el propio mareógrafo. Los 10 km son la referencia, y 6 y 8 km, un análisis de "
       "sensibilidad.")

with st.expander("Detalle técnico: tabla por radio (muestra común)"):
    filas = []
    for s in D.principales(track):
        for r in D.RADIOS:
            f = D.fila(s, track, r, "común")
            filas.append({"Estación": D.nombre(s), "Radio (km)": r, "n": int(f.n),
                          "Píxeles (mediana)": f.sample_median_pixels, "Desplazamiento (cm)": f.A_bias_cm,
                          "r A": f.A_r, "RMSE A (cm)": f.A_rmse_wo_offset_cm, "RMSE B (cm)": f.B_rmse_wo_offset_cm,
                          "ΔRMSE A − B (cm)": f.dRMSE_AB_cm, "IC inf.": f.dRMSE_AB_ci_low,
                          "IC sup.": f.dRMSE_AB_ci_high})
    tabla = pd.DataFrame(filas)
    st.dataframe(tabla, hide_index=True, use_container_width=True,
                 column_config={c: st.column_config.NumberColumn(format="%.2f" if c == "r A" else "%.1f")
                                for c in tabla.columns[3:]})
    st.markdown(
        "- **Muestra común:** solo los ciclos válidos en los tres radios, para que las diferencias entre radios no "
        "vengan de un cambio de muestra. Por eso los valores a 10 km pueden diferir ligeramente de los del "
        "explorador (Ferrol en T197 tiene 23 pares comunes en lugar de 24).\n"
        "- **Los intervalos comparan A con B en cada radio**; las diferencias entre radios se describen, no se "
        "contrastan.\n"
        "- **El desplazamiento depende del radio donde cambia la cobertura** (Ferrol T197: de "
        f"{E.signo(ferrol10.A_bias_cm)} cm a 10 km a {E.signo(ferrol6.A_bias_cm)} cm a 6 km): no es una propiedad "
        "de la estación independiente del área de búsqueda.")

with st.expander("Detalle técnico: los casos exploratorios en las rías"):
    st.markdown(
        "En Marín y Vigo en el track 197, la correlación de SWOT + DAC con el mareógrafo es **negativa** "
        f"(r = {E.num(D.fila('marin', 197).A_r)} y {E.num(D.fila('vigo', 197).A_r)} a 10 km), mientras que la del "
        f"DAC solo es positiva ({E.num(D.fila('marin', 197).B_r)} y {E.num(D.fila('vigo', 197).B_r)}). La "
        "cobertura escasa y algunos pasos de calidad o representatividad incierta impiden atribuir ese desacuerdo "
        "a la precisión de SWOT. En Marín, en el track 154, el círculo solo ve una mediana de 36 píxeles válidos "
        "por paso.")
