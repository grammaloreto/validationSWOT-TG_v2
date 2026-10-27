"""
Capa de datos del demo de validación v2: solo lee los resultados de `pass_v2.2` y la tabla maestra v2 copiados en
`datos/` (procedencia de cada archivo en `datos/MANIFIESTO.json`, generado por `herramientas/actualizar_datos.py`).

No recalcula métricas, intervalos ni correlaciones: todas las cifras que muestra el demo salen de esos archivos.
Las únicas transformaciones son de presentación (centrar una serie restando su media, promediar series centradas
para dibujar el modo común), con las mismas definiciones que los scripts que generaron los resultados
(`comparacion_tracks.py`, `descomposicion_figuras.py`). `comprobaciones()` verifica que lo dibujado reproduce las
n y las r guardadas.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

DATOS = Path(__file__).resolve().parents[1] / "datos"
SERIES = DATOS / "series"
TABLA = DATOS / "tabla_maestra_val_v2.csv"
REFERENCIA = DATOS / "trazas/swot_t{track}_reference.json"
DESCOMP = SERIES / "descomposicion/descomposicion_r10km.csv"
DESCOMP_CORR = SERIES / "descomposicion/descomposicion_correlaciones_r10km.csv"
DESCOMP_ROB = SERIES / "descomposicion/descomposicion_robustez_r10km.csv"
TRACKS_JSON = SERIES / "comparacion_tracks/comparacion_t154_t197_r10km.json"
ROBUSTEZ = SERIES / "robustez_modo_comun/robustez_r{r}km{sufijo}.csv"
PERSISTENCIA = SERIES / "robustez_modo_comun/persistencia_mareografos_r10km.csv"
ESTACIONES_CMP = SERIES / "comparacion_estaciones/comparacion_t{track}_r10km.csv"
COSTA = DATOS / "costa_galicia_ne10m.geojson"

TRACKS = (197, 154)
RADIOS = (6, 8, 10)
RADIO_REF = 10
# Estaciones de referencia del modo común (las mismas que en comparacion_tracks.py y descomposicion_figuras.py)
REFERENCIA_MODO_COMUN = {197: ["cibrao", "coruna", "ferrol"], 154: ["coruna", "ferrol"]}

# id interno → nombre en la red REDMAR, color y marcador (paleta categórica de las figuras del paper).
# `langosteira` (registro alternativo de T154, procedencia instrumental no establecida) queda fuera del demo,
# como del paper; Langosteira es siempre la estación REDMAR 3213 (`langosteira_2`).
# Zonas, condiciones de los casos exploratorios y motivos de exclusión, por idioma, en `textos.py`.
ESTACIONES = {
    "cibrao": {"nombre": "San Cibrao", "color": "#1baf7a", "marcador": "triangle-up"},
    "coruna": {"nombre": "A Coruña", "color": "#2a78d6", "marcador": "circle"},
    "ferrol": {"nombre": "Ferrol", "color": "#eb6834", "marcador": "square"},
    "langosteira_2": {"nombre": "Langosteira", "color": "#eda100", "marcador": "diamond"},
    "villagarcia": {"nombre": "Villagarcía", "color": "#e87ba4", "marcador": "triangle-down"},
    "marin": {"nombre": "Marín", "color": "#8a8983", "marcador": "cross"},
    "vigo": {"nombre": "Vigo", "color": "#5c5b56", "marcador": "x"},
}
ORDEN = list(ESTACIONES)

COLUMNAS_VALIDAS = ["swot_corrected", "swot_l3", "dac_median", "tg_residual"]


def nombre(station):
    return ESTACIONES[station]["nombre"]


# ---------------------------------------------------------------- tabla maestra


@st.cache_data
def tabla():
    t = pd.read_csv(TABLA)
    t = t[t.station.isin(ESTACIONES)].copy()
    t["nombre"] = t.station.map(nombre)
    return t


def fila(station, track, radio=RADIO_REF, muestra="propia"):
    t = tabla()
    r = t[(t.station == station) & (t.track == track) & (t.radius_km == radio) & (t["sample"] == muestra)]
    return r.iloc[0] if len(r) == 1 else None


def principales(track):
    t = tabla()
    r = t[(t.track == track) & (t.radius_km == RADIO_REF) & (t["sample"] == "propia") & (t.role == "principal")]
    return [s for s in ORDEN if s in set(r.station)]


def exploratorias(track):
    t = tabla()
    r = t[(t.track == track) & (t.radius_km == RADIO_REF) & (t["sample"] == "propia") & (t.role == "exploratoria")]
    return [s for s in ORDEN if s in set(r.station)]


def combinaciones():
    """(estación, track, papel) a 10 km, principales primero."""
    out = [(s, tr, "principal") for tr in TRACKS for s in principales(tr)]
    return out + [(s, tr, "exploratoria") for tr in TRACKS for s in exploratorias(tr)]


# ---------------------------------------------------------------- series por paso


@st.cache_data
def serie(station, track, radio=RADIO_REF):
    df = pd.read_csv(SERIES / f"{station}_t{track}_r{radio}km.csv")
    df["pass_time_utc"] = pd.to_datetime(df.pass_time_utc, utc=True, format="ISO8601")
    return df


def validos(df):
    """Pasos válidos para las tres comparaciones (mismo criterio que los scripts de métricas)."""
    return df[df.status == "ok"].dropna(subset=COLUMNAS_VALIDAS)


@st.cache_data
def referencia(track):
    return json.loads(Path(str(REFERENCIA).format(track=track)).read_text())


@st.cache_data
def coordenadas():
    """Coordenadas de cada estación según las trazas de referencia."""
    out = {}
    for track in TRACKS:
        for s, info in referencia(track)["stations"].items():
            if s in ESTACIONES:
                out[s] = (info["station_lon"], info["station_lat"])
    return out


@st.cache_data
def costa():
    """Tierra de Natural Earth 10 m recortada a Galicia."""
    return json.loads(COSTA.read_text())


@st.cache_data
def resumen_exclusiones():
    filas = []
    for s in ESTACIONES:
        for track in TRACKS:
            for radio in RADIOS:
                p = SERIES / f"{s}_t{track}_r{radio}km.csv"
                if p.exists():
                    df = pd.read_csv(p, usecols=["cycle", "status", "exclusion_reason"])
                    filas.append(df.assign(station=s, track=track, radius_km=radio))
    return pd.concat(filas, ignore_index=True)


# ---------------------------------------------------------------- análisis regional


def _validos_indexados(station, track):
    return validos(serie(station, track)).set_index("cycle")


@st.cache_data
def d_centrada(track):
    """d = SWOT+DAC − mareógrafo (cm) de las estaciones de referencia, centrada por estación sobre sus propios
    pasos válidos y limitada a los ciclos comunes (definición de comparacion_tracks.common_mode)."""
    est = REFERENCIA_MODO_COMUN[track]
    d = pd.DataFrame({s: 100 * (_validos_indexados(s, track).swot_corrected
                                - _validos_indexados(s, track).tg_residual) for s in est})
    d = (d - d.mean()).dropna()
    tiempos = _validos_indexados(est[0], track).loc[d.index, "pass_time_utc"]
    return d, tiempos


def modo_comun(track):
    d, tiempos = d_centrada(track)
    return d.mean(axis=1), tiempos


@st.cache_data
def descomposicion():
    return pd.read_csv(DESCOMP)


@st.cache_data
def descomp_centrada(track):
    """Componentes por paso centradas por estación sobre los ciclos comunes del track
    (definición de descomposicion_figuras.centered_track)."""
    df = descomposicion()
    est = REFERENCIA_MODO_COMUN[track]
    sub = df[(df.track == track) & df.station.isin(est) & df.closed.astype(bool)]
    ciclos = sorted(set.intersection(*[set(sub[sub.station == s].cycle) for s in est]))
    sub = sub[sub.cycle.isin(ciclos)].copy()
    cols = ["difference", "agg_ssha_unfiltered", "agg_dac", "tg_residual", "tide_prediction_difference_m",
            "agg_calibration"]
    for c in cols:
        sub[c + "_c"] = sub[c] - sub.groupby("station")[c].transform("mean")
    medias = sub.groupby("cycle")[[c + "_c" for c in cols]].mean()
    tiempos = sub.groupby("cycle").pass_time_utc.first().map(pd.Timestamp)
    return sub, ciclos, medias, tiempos


@st.cache_data
def correlaciones_descomp():
    return pd.read_csv(DESCOMP_CORR)


@st.cache_data
def robustez_descomp():
    return pd.read_csv(DESCOMP_ROB)


@st.cache_data
def tracks_json():
    return json.loads(TRACKS_JSON.read_text())


@st.cache_data
def robustez(radio=10, comun=False):
    return pd.read_csv(Path(str(ROBUSTEZ).format(r=radio, sufijo="_comun6_8_10" if comun else "")))


@st.cache_data
def persistencia_mareografos():
    return pd.read_csv(PERSISTENCIA)


@st.cache_data
def estaciones_cmp(track):
    df = pd.read_csv(Path(str(ESTACIONES_CMP).format(track=track)))
    return df[(df["sample"] == "raw") & df.station.isin(ESTACIONES)]


def r_guardada(track, variable, scope="track_mean_vs_common_mode", station=None):
    c = correlaciones_descomp()
    c = c[(c.scope == scope) & (c.track.astype(str) == str(track)) & (c.variable == variable)]
    if station:
        c = c[c.station == station]
    row = c.iloc[0]
    return float(row.r), int(row.n)


# ---------------------------------------------------------------- comprobaciones de coherencia


@st.cache_data
def comprobaciones():
    """Comprueba que lo que dibuja el demo reproduce lo guardado. Devuelve [(qué, ok, detalle)]."""
    out = []
    t = tabla()
    # 1) n de la tabla maestra = pasos válidos de la serie (10 km, muestra propia)
    malos = []
    for s, tr, _ in combinaciones():
        f = fila(s, tr)
        if f is not None and int(f.n) != len(validos(serie(s, tr))):
            malos.append(f"{nombre(s)} T{tr}")
    out.append(("n de la tabla maestra = pasos válidos de cada serie a 10 km", not malos,
                ", ".join(malos) or f"{len(combinaciones())} combinaciones"))
    # 2) desplazamiento de la tabla = media de d en la serie
    malos = []
    for s, tr, _ in combinaciones():
        f, ok = fila(s, tr), validos(serie(s, tr))
        if f is not None and not np.isnan(f.A_bias_cm):
            if abs(round(100 * float((ok.swot_corrected - ok.tg_residual).mean()), 2) - f.A_bias_cm) > 0.011:
                malos.append(f"{nombre(s)} T{tr}")
    out.append(("Desplazamiento medio de la tabla = media de SWOT+DAC − mareógrafo en la serie", not malos,
                ", ".join(malos) or "todas coinciden (±0.01 cm)"))
    # 3) modo común entre tracks
    cm154, _ = modo_comun(154)
    cm197, _ = modo_comun(197)
    both = cm154.index.intersection(cm197.index)
    g = tracks_json()["cross_track"]["common_mode_t154_vs_t197"]
    r = float(np.corrcoef(cm154.loc[both], cm197.loc[both])[0, 1])
    out.append(("Modo común T154 frente a T197 (r y n guardados)", len(both) == g["n"] and abs(r - g["r"]) < 5e-4,
                f"dibujado r = {r:.3f}, n = {len(both)} · guardado r = {g['r']}, n = {g['n']}"))
    # 4) modo común frente a la diferencia de predicciones de marea
    for track in TRACKS:
        _, ciclos, medias, _ = descomp_centrada(track)
        x = medias.loc[ciclos, "tide_prediction_difference_m_c"]
        y = medias.loc[ciclos, "difference_c"]
        r = float(np.corrcoef(x, y)[0, 1])
        rg, ng = r_guardada(track, "tide_prediction_difference_m")
        out.append((f"T{track}: modo común frente a la diferencia de predicciones de marea",
                    len(ciclos) == ng and abs(r - rg) < 5e-4,
                    f"dibujado r = {r:.3f}, n = {len(ciclos)} · guardado r = {rg:.3f}, n = {ng}"))
    # 5) todos los pasos de la descomposición se reproducen
    df = descomposicion()
    out.append(("Pasos de la descomposición que reproducen el método", bool(df.closed.astype(bool).all()),
                f"{int(df.closed.astype(bool).sum())}/{len(df)}"))
    # 6) series y tabla: revisión de git de cada serie registrada
    sin_rev = t[t.series_git_revision.isna() & t.n.gt(0)]
    out.append(("Cada fila con métricas lleva serie e identificador de revisión", sin_rev.empty,
                f"{t.series_id.nunique()} series distintas en la tabla"))
    return out
