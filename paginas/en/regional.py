"""Análisis regional: discrepancia compartida, persistencia entre tracks y asociación con las predicciones de marea."""
import pandas as pd
import streamlit as st

from nucleo import datos as D
from nucleo import estilo as E
from nucleo import graficos as G
from nucleo import textos as T

E.aplicar()
E.aviso(T.t("traduccion_pendiente"))  # retirar al traducir la página
E.cabecera(
    "Resultados · Patrón regional",
    "Una discrepancia que comparten las estaciones",
    "Cuando se mira la diferencia SWOT − mareógrafo paso a paso, aparece algo inesperado: en la costa norte "
    "<b>sube y baja a la vez en todas las estaciones</b>, se repite en las dos pasadas del satélite y sigue de "
    "cerca a la diferencia entre las dos predicciones de marea. Las estaciones, por tanto, no son pruebas "
    "independientes, y este patrón se analiza aparte de los resultados por estación.",
)

E.aviso("<b>Asociación no es causa.</b> Todas las variables analizadas aquí forman parte de la propia diferencia "
        "SWOT − mareógrafo, así que su parecido con ella no es una prueba independiente de qué la provoca.")

# ---------------------------------------------------------------- 1
st.markdown("### 1 · Las estaciones se mueven juntas")
track = st.segmented_control("Track", options=list(D.TRACKS), default=197,
                             format_func=lambda t: f"Track {t}", key="track_d") or 197
st.plotly_chart(G.regional_d(track), use_container_width=True)
cmp = D.estaciones_cmp(track).set_index("station")
ref = D.REFERENCIA_MODO_COMUN[track]
std_cm = D.tracks_json()["cross_track"]["std_common_mode_cm"][f"t{track}"]
st.caption(f"Diferencia por paso de cada estación de referencia, centrada (se le resta su media), y su media: el "
           f"**modo común** del track {track} (desviación típica {E.num(std_cm, 1)} cm).")
filas = [{"Estación": D.nombre(s), "r con el modo común de las demás": cmp.loc[s, "r_common_mode"],
          "Dispersión propia (cm)": cmp.loc[s, "own_part_cm"], "n": int(cmp.loc[s, "n_common_mode"])}
         for s in cmp.index if s in ref or s in ("langosteira_2", "villagarcia")]
a, b = st.columns([3, 2])
a.dataframe(pd.DataFrame(filas), hide_index=True, use_container_width=True,
            column_config={"r con el modo común de las demás": st.column_config.NumberColumn(format="%.2f"),
                           "Dispersión propia (cm)": st.column_config.NumberColumn(format="%.1f")})
b.markdown("La **r** de cada estación se calcula con el modo común de las *demás* (sin ella). La **dispersión "
           "propia** es la desviación típica de su diferencia respecto a ese modo común: mucho menor que la "
           "variabilidad del propio modo común.")

# ---------------------------------------------------------------- 2
st.markdown("### 2 · Se repite en las dos pasadas, separadas 37 horas")
ct = D.tracks_json()["cross_track"]
a, b = st.columns([3, 2])
with a:
    st.plotly_chart(G.entre_tracks(), use_container_width=True, config={"displayModeBar": False})
with b:
    st.markdown(f"El paso del track 197 ocurre **{E.num(ct['hours_t197_minus_t154']['median'], 1)} h** después del "
                f"del track 154 en el mismo ciclo. En los {ct['common_mode_t154_vs_t197']['n']} ciclos válidos en "
                "los dos, los modos comunes casi coinciden.")
    comp = pd.DataFrame([
        {"Señal": "Modo común de la diferencia", "r entre tracks": ct["common_mode_t154_vs_t197"]["r"]},
        {"Señal": "Anomalía de SWOT en A Coruña", "r entre tracks": ct["reference_coruna_swot_l3_t154_vs_t197"]["r"]},
        {"Señal": "DAC − mareógrafo en A Coruña", "r entre tracks": ct["reference_coruna_dac_error_t154_vs_t197"]["r"]},
        {"Señal": "DAC en A Coruña", "r entre tracks": ct["reference_coruna_dac_t154_vs_t197"]["r"]},
        {"Señal": "Residuo del mareógrafo en A Coruña",
         "r entre tracks": ct["reference_coruna_tg_residual_t154_vs_t197"]["r"]},
    ])
    st.dataframe(comp, hide_index=True, use_container_width=True,
                 column_config={"r entre tracks": st.column_config.NumberColumn(format="%.2f")})
    st.caption("La discrepancia compartida persiste entre pasadas más que el propio nivel del mar que mide el "
               "mareógrafo (comparación descriptiva de correlaciones, no contrastada).")

with st.expander("Detalle técnico: robustez de la persistencia entre tracks"):
    rb = D.robustez(10)
    cross = rb[rb.group == "cross_track"].iloc[0]
    pm = D.persistencia_mareografos()
    sets = pm[pm.group == "common_mode_sets_same_cycles"]
    disj = sets[sets.disjoint_tide_gauges.astype(bool)]
    shar = sets[~sets.disjoint_tide_gauges.astype(bool)]
    radios = {r: D.robustez(r, comun=True) for r in D.RADIOS}
    rr = {r: radios[r][radios[r].group == "cross_track"].iloc[0] for r in D.RADIOS}
    st.markdown(
        f"- **Tendencia:** tras retirar una tendencia lineal de cada serie, r = {E.num(cross.r_detrended)}.\n"
        f"- **Ciclos individuales:** dejando fuera un ciclo cada vez, r entre {E.num(cross.loo_min_r)} y "
        f"{E.num(cross.loo_max_r)}.\n"
        f"- **Conjuntos de mareógrafos:** combinaciones de estaciones que no comparten ningún mareógrafo entre "
        f"tracks dan r = {E.num(disj.r.min())}–{E.num(disj.r.max())}; las que comparten alguno, "
        f"{E.num(shar.r.min())}–{E.num(shar.r.max())}. Los mareógrafos no compartidos siguen perteneciendo a la "
        f"misma red y procesado.\n"
        f"- **Radio:** en los ciclos válidos en los tres radios (n = {int(rr[10].n)}), r = "
        f"{', '.join(E.num(rr[r].r) for r in D.RADIOS)} a 6, 8 y 10 km "
        f"({', '.join(E.num(rr[r].r_detrended) for r in D.RADIOS)} sin tendencia).")

# ---------------------------------------------------------------- 3
st.markdown("### 3 · Sigue a la diferencia entre las dos predicciones de marea")
a, b = st.columns([3, 2])
with a:
    st.plotly_chart(G.modo_comun_mareas(), use_container_width=True, config={"displayModeBar": False})
with b:
    st.markdown("Cada sistema retira la marea con su propia predicción: SWOT con un **modelo global** (FES2022 y "
                "marea interna HRET) y el mareógrafo con la **predicción armónica de Puertos del Estado**. Si esas "
                "dos predicciones difieren, la diferencia pasa directamente a la comparación.")
    var = {"tide_prediction_difference_m": "Predicción del mareógrafo − marea de SWOT",
           "agg_ssha_unfiltered": "Anomalía de SWOT", "agg_dac": "DAC", "tg_residual": "Residuo del mareógrafo"}
    filas = [{"Variable (media del track)": etq,
              "r · T197": D.r_guardada(197, v)[0], "r · T154": D.r_guardada(154, v)[0]} for v, etq in var.items()]
    st.dataframe(pd.DataFrame(filas), hide_index=True, use_container_width=True,
                 column_config={c: st.column_config.NumberColumn(format="%.2f") for c in ("r · T197", "r · T154")})
    st.caption("Correlación de cada componente con el modo común. La diferencia de predicciones es la más fuerte "
               "en los dos tracks.")

rob = D.robustez_descomp()
rt = {tr: rob[(rob.track == tr) & (rob.scope == "track_mean_vs_common_mode")
              & (rob.variable == "tide_prediction_difference_m")].iloc[0] for tr in D.TRACKS}
st_ = rob[(rob.scope == "station_vs_own_d") & (rob.variable == "tide_prediction_difference_m")]
st.markdown(
    f"La asociación se mantiene **en cada estación de referencia** (r = {E.num(st_.r.min())}–{E.num(st_.r.max())}), "
    f"tras retirar la tendencia (r = {E.num(rt[197].r_detrended)} en T197 y {E.num(rt[154].r_detrended)} en T154) y "
    f"dejando fuera un ciclo cada vez (r ≥ {E.num(rt[197].loo_min)} y {E.num(rt[154].loo_min)}).")

st.markdown("### Una explicación posible: la marea anual")
E.hallazgo(
    "Hipótesis: las componentes anual y semianual (Sa y Ssa)",
    "En los mareógrafos, las componentes anual y semianual de la marea recogen sobre todo el ciclo estacional "
    "del nivel del mar, dominado por la meteorología más que por la astronomía; en los mareógrafos europeos son "
    "de varios centímetros (Ray et al., 2021). La corrección de marea de SWOT, en cambio, solo incluye la pequeña "
    "parte astronómica. Si la predicción de Puertos del Estado incluye Sa y Ssa ajustadas a cada registro, retira "
    "del mareógrafo un ciclo estacional que SWOT conserva, y esa diferencia aparecería justo como una "
    "discrepancia lenta, común y persistente, contenida en la diferencia de predicciones. <b>Para comprobarlo "
    "hacen falta las constantes exactas de la predicción, que no están publicadas: por ahora es una hipótesis, "
    "no un resultado.</b>")

with st.expander("Detalle técnico: qué más contiene la diferencia de predicciones"):
    st.markdown(
        "- **Marea de carga:** el altímetro mide alturas geocéntricas y su corrección de marea incluye la marea "
        "de carga; el mareógrafo mide respecto a la corteza, que se mueve con ella. Retirar en cada lado su "
        "propia predicción es coherente, pero la *diferencia de predicciones* contiene la marea de carga por "
        "construcción, incluso con modelos perfectos. Esa parte es esperable y no indica un error.\n"
        "- **Ubicación:** una predicción se evalúa en el puerto y la otra en los píxeles, así que la diferencia "
        "incluye también la variación espacial real de la marea y los errores de ambas predicciones cerca de "
        "la costa.\n"
        "- Por todo ello, la asociación **no atribuye** la discrepancia a un modelo concreto.")

with st.expander("Detalle técnico: componentes por paso frente al modo común"):
    tr = st.segmented_control("Track ", options=list(D.TRACKS), default=197,
                              format_func=lambda t: f"Track {t}", key="track_comp") or 197
    st.plotly_chart(G.componentes(tr), use_container_width=True)
    st.caption("Cada componente centrada por estación sobre los ciclos comunes del track; en negro, su media. "
               "Todas están relacionadas algebraicamente con d.")
