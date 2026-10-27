"""
Idioma del demo y cadenas cortas compartidas (etiquetas de gráficos, navegación, zonas, condiciones y motivos de
exclusión). La prosa de cada página vive en `paginas/es/` y `paginas/en/`; aquí solo lo que usan varias páginas o
`graficos.py`.

El idioma se elige en la barra lateral (`app.py`), se guarda en `st.session_state["idioma"]` y se refleja en la URL
(`?lang=en`). La terminología inglesa es la del borrador del artículo.
"""
import streamlit as st

IDIOMAS = {"es": "Español", "en": "English"}
POR_DEFECTO = "es"


def idioma():
    return st.session_state.get("idioma", POR_DEFECTO)


def t(clave, **kw):
    texto = TEXTOS[idioma()][clave]
    return texto.format(**kw) if kw else texto


def zona(station):
    return ZONAS[idioma()][station]


def condicion(station, track):
    return CONDICIONES[idioma()].get((station, track))


def motivos():
    return MOTIVOS[idioma()]


def componentes():
    return COMPONENTES[idioma()]


TEXTOS = {
    "es": {
        # navegación
        "selector": "Idioma",
        "sec_resumen": "Resumen", "sec_resultados": "Resultados", "sec_contexto": "Contexto",
        "pag_inicio": "Inicio", "pag_estaciones": "Estaciones y datos", "pag_explorador": "Explorador por estación",
        "pag_aporta": "¿Aporta SWOT?", "pag_radio": "Radio de búsqueda", "pag_regional": "Patrón regional",
        "pag_literatura": "Otros estudios", "pag_metodo": "Método",
        "titulo_app": "Validación SWOT – mareógrafos · Galicia",
        "traduccion_pendiente": "",
        # comparaciones
        "etiqueta_a": "SWOT + DAC",
        "etiqueta_b": "DAC solo (modelo atmosférico)",
        "etiqueta_b_corta": "DAC solo",
        "etiqueta_tg": "Mareógrafo (nivel − marea)",
        "menos_desplazamiento": "{a} − desplazamiento medio",
        "principal": "principal", "exploratoria": "exploratoria",
        # comunes en gráficos
        "ciclo": "Ciclo", "ciclo_min": "ciclo", "ciclos": "ciclos", "pixeles": "píxeles", "Pixeles": "Píxeles",
        "papel": "Papel", "oeste": "O", "ic95": "IC 95 %", "ic": "IC", "media": "media",
        # mapa y explorador
        "eje_tg": "Mareógrafo (cm)", "eje_satelite": "Satélite / modelo (cm)",
        "cob_circulo": "En el círculo", "cob_calidad": "Calidad = 0", "cob_atipicos": "Tras valores atípicos",
        # ¿aporta SWOT? y radio
        "forest_r": "Correlación r", "forest_rmse": "RMSE sin desplazamiento (cm)",
        "drmse_ic": "ΔRMSE A − B (cm) e IC 95 %", "pixeles_mediana": "Píxeles válidos por paso (mediana)",
        "eje_radio": "Radio de búsqueda (km)",
        # análisis regional
        "modo_comun": "Modo común", "modo_comun_track": "Modo común (T{track})", "d_centrada": "d centrada (cm)",
        "eje_modo_comun_track": "Modo común, track {track} (cm)", "eje_modo_comun": "Modo común (cm)",
        "delta_predicciones": "Δ predicciones",
        "eje_predicciones": "Predicción del mareógrafo − marea de SWOT (cm)",
        "r_con_modo_comun": "r con el modo común", "media_track": "Media del track",
    },
    "en": {
        "selector": "Language",
        "sec_resumen": "Summary", "sec_resultados": "Results", "sec_contexto": "Context",
        "pag_inicio": "Home", "pag_estaciones": "Stations and data", "pag_explorador": "Station explorer",
        "pag_aporta": "Does SWOT add value?", "pag_radio": "Search radius", "pag_regional": "Regional pattern",
        "pag_literatura": "Related studies", "pag_metodo": "Method",
        "titulo_app": "SWOT – tide gauge validation · Galicia",
        "traduccion_pendiente": "Translation in progress: the text of this page is still in Spanish. "
                                "Figures and chart labels are already in English.",
        "etiqueta_a": "SWOT + DAC",
        "etiqueta_b": "DAC alone (atmospheric model)",
        "etiqueta_b_corta": "DAC alone",
        "etiqueta_tg": "Tide gauge (sea level − tide)",
        "menos_desplazamiento": "{a} − mean offset",
        "principal": "main", "exploratoria": "exploratory",
        "ciclo": "Cycle", "ciclo_min": "cycle", "ciclos": "cycles", "pixeles": "pixels", "Pixeles": "Pixels",
        "papel": "Role", "oeste": "W", "ic95": "95 % CI", "ic": "CI", "media": "mean",
        "eje_tg": "Tide gauge (cm)", "eje_satelite": "Satellite / model (cm)",
        "cob_circulo": "In the circle", "cob_calidad": "Quality flag = 0", "cob_atipicos": "After outlier removal",
        "forest_r": "Correlation r", "forest_rmse": "RMSE without offset (cm)",
        "drmse_ic": "ΔRMSE A − B (cm) and 95 % CI", "pixeles_mediana": "Valid pixels per pass (median)",
        "eje_radio": "Search radius (km)",
        "modo_comun": "Common mode", "modo_comun_track": "Common mode (T{track})", "d_centrada": "Centred d (cm)",
        "eje_modo_comun_track": "Common mode, track {track} (cm)", "eje_modo_comun": "Common mode (cm)",
        "delta_predicciones": "Δ predictions",
        "eje_predicciones": "Tide gauge prediction − SWOT tide (cm)",
        "r_con_modo_comun": "r with the common mode", "media_track": "Track mean",
    },
}

ZONAS = {
    "es": {
        "cibrao": "Costa norte (A Mariña)", "coruna": "Golfo Ártabro", "ferrol": "Ría de Ferrol",
        "langosteira_2": "Puerto exterior de A Coruña (REDMAR 3213)", "villagarcia": "Ría de Arousa (interior)",
        "marin": "Ría de Pontevedra", "vigo": "Ría de Vigo",
    },
    "en": {
        "cibrao": "North coast (A Mariña)", "coruna": "Ártabro Gulf", "ferrol": "Ría de Ferrol",
        "langosteira_2": "Outer port of A Coruña (REDMAR 3213)", "villagarcia": "Ría de Arousa (inner part)",
        "marin": "Ría de Pontevedra", "vigo": "Ría de Vigo",
    },
}

# Condición que define cada caso exploratorio (equivale a la Tabla 2 de resultados; en inglés, su redacción)
CONDICIONES = {
    "es": {
        ("marin", 197): "Cobertura válida escasa (mediana de 130 píxeles por paso) y pasos de calidad o "
                        "representatividad incierta.",
        ("vigo", 197): "Pocas fechas con datos del mareógrafo y un paso de calidad o representatividad incierta.",
        ("langosteira_2", 154): "Pocas fechas con datos del mareógrafo (5 pares).",
        ("villagarcia", 154): "SWOT solo cubre la estación en los ciclos 23–29 (5 pares).",
        ("marin", 154): "Mediana de 36 píxeles válidos por paso: el círculo apenas ve agua.",
        ("vigo", 154): "Pocas fechas con datos del mareógrafo (7 pares).",
        ("langosteira_2", 197): "Serie principal con pocos pares (7): pesa mucho menos que las de 23–25.",
    },
    "en": {
        ("marin", 197): "Scarce valid coverage (median of 130 valid pixels per pass); passes of uncertain quality "
                        "or representativeness.",
        ("vigo", 197): "Few tide gauge dates; one pass of uncertain quality or representativeness.",
        ("langosteira_2", 154): "Few tide gauge dates (5 pairs).",
        ("villagarcia", 154): "SWOT covers the station only in cycles 23–29 (5 pairs).",
        ("marin", 154): "Median of 36 valid pixels per pass: the circle barely sees water.",
        ("vigo", 154): "Few tide gauge dates (7 pairs).",
        ("langosteira_2", 197): "Main series with few pairs (7): it weighs much less than those with 23–25.",
    },
}

MOTIVOS = {
    "es": {
        "no_tide_gauge_data": "Sin registro del mareógrafo ese día",
        "api_returned_no_swot_data": "SWOT no devolvió datos (sin archivo o sin píxeles en el círculo)",
        "no_swot_pixels_in_circle": "Sin píxeles válidos de SWOT en el círculo",
        "tg_after_pass_not_in_daily_file": "Falta la hora posterior al paso en el archivo diario del mareógrafo",
        "pass_not_on_tg_file_date": "La fecha del paso no coincide con la del archivo del mareógrafo",
        "tg_bracketing_observations_missing": "Falta alguna de las dos horas que rodean el paso",
    },
    "en": {
        "no_tide_gauge_data": "No tide gauge record that day",
        "api_returned_no_swot_data": "SWOT returned no data (no file or no pixels in the circle)",
        "no_swot_pixels_in_circle": "No valid SWOT pixels in the circle",
        "tg_after_pass_not_in_daily_file": "The hour after the pass is missing from the daily tide gauge file",
        "pass_not_on_tg_file_date": "The pass date does not match the tide gauge file date",
        "tg_bracketing_observations_missing": "One of the two hours around the pass is missing",
    },
}

COMPONENTES = {
    "es": {
        "difference": "d = SWOT + DAC − mareógrafo",
        "tide_prediction_difference_m": "Predicción del mareógrafo − marea oceánica e interna de SWOT",
        "agg_ssha_unfiltered": "Anomalía de SWOT (SSHA)",
        "agg_dac": "DAC",
        "tg_residual": "Residuo del mareógrafo",
    },
    "en": {
        "difference": "d = SWOT + DAC − tide gauge",
        "tide_prediction_difference_m": "Tide gauge prediction − SWOT ocean and internal tide",
        "agg_ssha_unfiltered": "SWOT anomaly (SSHA)",
        "agg_dac": "DAC",
        "tg_residual": "Tide gauge residual",
    },
}
