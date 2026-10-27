"""
Gráficos interactivos (Plotly) del demo. Cada función recibe datos ya leídos por `datos.py` y no calcula métricas:
las r, RMSE e intervalos que aparecen en títulos y etiquetas vienen de la tabla maestra o de las salidas guardadas.
"""
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from . import datos as D
from .estilo import (COLOR_A, COLOR_B, COLOR_TG, COLOR_TRACK, ETIQUETA_A, ETIQUETA_B, ETIQUETA_TG, GRIS, REJILLA,
                     SUPERFICIE, TINTA, signo)

FUENTE = dict(family="Inter, -apple-system, Segoe UI, Helvetica, Arial, sans-serif", size=13, color=TINTA)


def _base(fig, alto=420, leyenda=True, subtitulos=False):
    """Estilo común. Con subtitulos=True (figuras con subgráficos titulados), la leyenda va arriba del todo, anclada
    al contenedor, y el margen superior deja sitio para que no se solape con los títulos."""
    if subtitulos:
        margen_sup = 90 if leyenda else 45
        posicion = dict(yref="container", y=0.99, yanchor="top")
    else:
        margen_sup = 40
        posicion = dict(y=1.02, yanchor="bottom")
    fig.update_layout(
        height=alto + (margen_sup - 40), font=FUENTE, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor=SUPERFICIE,
        margin=dict(l=10, r=10, t=margen_sup, b=10), hoverlabel=dict(bgcolor="white", font_size=12),
        showlegend=leyenda,
        legend=dict(orientation="h", xanchor="left", x=0, bgcolor="rgba(0,0,0,0)", **posicion),
    )
    if subtitulos:
        fig.update_annotations(font=dict(size=13, color=TINTA), yshift=6)
    fig.update_xaxes(gridcolor=REJILLA, zerolinecolor=REJILLA, linecolor=REJILLA, tickfont=dict(color=GRIS))
    fig.update_yaxes(gridcolor=REJILLA, zerolinecolor=REJILLA, linecolor=REJILLA, tickfont=dict(color=GRIS))
    return fig


# ---------------------------------------------------------------- mapa


MAR, TIERRA, COSTA = "#eef4f8", "#efeee9", "#b9b7ae"
EXTENSION = (-9.75, -7.05, 41.88, 44.12)  # lon_min, lon_max, lat_min, lat_max (como la figura 1 del artículo)
# Desplazamiento de la etiqueta (grados) y lado; por defecto, a la izquierda
ETIQUETA = {"cibrao": (0.13, 0.0), "ferrol": (0.13, 0.04), "coruna": (0.13, -0.07),
            "langosteira_2": (-0.13, -0.04)}


def _circulo(lon, lat, km, n=90):
    th = np.linspace(0, 2 * np.pi, n)
    return (lon + km / (111.32 * np.cos(np.radians(lat))) * np.cos(th), lat + km / 111.32 * np.sin(th))


def _tierra():
    """Anillos exteriores de la tierra (Natural Earth 10 m) separados por None, para un único relleno."""
    lon, lat = [], []
    for f in D.costa()["features"]:
        g = f["geometry"]
        poligonos = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        for p in poligonos:
            anillo = np.array(p[0])
            lon += list(anillo[:, 0]) + [None]
            lat += list(anillo[:, 1]) + [None]
    return lon, lat


def mapa(radio=10, papeles=None, alto=600, destacar=None):
    """Estaciones, nadir de las trazas de referencia y círculos de búsqueda sobre la costa de Natural Earth 10 m,
    sin servicios de teselas. papeles: {station: 'principal' | 'exploratoria'}."""
    papeles = papeles or {}
    fig = go.Figure()
    lon, lat = _tierra()
    fig.add_trace(go.Scatter(x=lon, y=lat, mode="lines", fill="toself", fillcolor=TIERRA,
                             line=dict(color=COSTA, width=0.8), hoverinfo="skip", showlegend=False))
    for track in D.TRACKS:
        v = np.array(D.referencia(track)["vertices"])
        fig.add_trace(go.Scatter(x=v[:, 0], y=v[:, 1], mode="lines", name=f"Track {track} (nadir)",
                                 line=dict(color=COLOR_TRACK[track], width=2.5, dash="dash" if track == 154 else None),
                                 hovertemplate=f"Track {track}<extra></extra>"))
    coords = D.coordenadas()
    for s, (x0, y0) in coords.items():
        principal = papeles.get(s) == "principal"
        x, y = _circulo(x0, y0, radio)
        fig.add_trace(go.Scatter(
            x=x, y=y, mode="lines", showlegend=False, hoverinfo="skip",
            line=dict(color=D.ESTACIONES[s]["color"] if principal else GRIS, width=2.4 if principal else 1.2,
                      dash=None if principal else "dot")))
    for s, (x0, y0) in coords.items():
        e = D.ESTACIONES[s]
        dx, dy = ETIQUETA.get(s, (-0.13, 0.0))
        fig.add_trace(go.Scatter(
            x=[x0], y=[y0], mode="markers", showlegend=False,
            marker=dict(size=12 if s == destacar else 10, color=e["color"], symbol=e["marcador"],
                        line=dict(color="white", width=1)),
            hovertemplate=f"<b>{e['nombre']}</b><br>{e['zona']}<br>{y0:.2f}° N, {abs(x0):.2f}° O"
                          f"<br>Papel: {papeles.get(s, '—')}<extra></extra>"))
        fig.add_annotation(x=x0 + dx, y=y0 + dy, text=e["nombre"], showarrow=False,
                           xanchor="left" if dx > 0 else "right", font=dict(size=12, color=TINTA))
    lon_min, lon_max, lat_min, lat_max = EXTENSION
    fig.update_xaxes(range=[lon_min, lon_max], showgrid=False, zeroline=False, ticksuffix="°", title=None)
    fig.update_yaxes(range=[lat_min, lat_max], showgrid=False, zeroline=False, ticksuffix="°", title=None,
                     scaleanchor="x", scaleratio=1 / np.cos(np.radians((lat_min + lat_max) / 2)))
    _base(fig, alto)
    fig.update_layout(plot_bgcolor=MAR, margin=dict(l=0, r=0, t=30, b=0),
                      legend=dict(orientation="h", yanchor="bottom", y=1.0, xanchor="left", x=0))
    return fig


# ---------------------------------------------------------------- explorador


def serie_estacion(ok, desplazamiento_cm, alto=420):
    """Residuo del mareógrafo, SWOT+DAC menos su desplazamiento medio y DAC solo, por paso (cm)."""
    t = ok.pass_time_utc
    hover = "Ciclo %{customdata}<br>%{x|%Y-%m-%d %H:%M} UTC<br>%{y:.1f} cm<extra>%{fullData.name}</extra>"
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=100 * ok.tg_residual, name=ETIQUETA_TG, mode="lines+markers",
                             line=dict(color=COLOR_TG, width=2), marker=dict(size=7), customdata=ok.cycle,
                             hovertemplate=hover))
    fig.add_trace(go.Scatter(x=t, y=100 * ok.swot_corrected - desplazamiento_cm,
                             name=f"{ETIQUETA_A} − desplazamiento medio", mode="lines+markers",
                             line=dict(color=COLOR_A, width=2), marker=dict(size=7, symbol="square"),
                             customdata=ok.cycle, hovertemplate=hover))
    fig.add_trace(go.Scatter(x=t, y=100 * ok.dac_median, name=ETIQUETA_B, mode="lines+markers",
                             line=dict(color=COLOR_B, width=1.6, dash="dash"),
                             marker=dict(size=6, symbol="triangle-up"), customdata=ok.cycle, hovertemplate=hover))
    fig.add_hline(y=0, line_color=REJILLA)
    fig.update_yaxes(title="cm")
    return _base(fig, alto)


def dispersion_ab(ok, desplazamiento_cm, alto=380):
    """SWOT+DAC (sin desplazamiento) y DAC solo frente al mareógrafo, con la recta 1:1."""
    tg = 100 * ok.tg_residual
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=tg, y=100 * ok.swot_corrected - desplazamiento_cm, mode="markers", name=ETIQUETA_A,
                             marker=dict(color=COLOR_A, size=8, symbol="square"), customdata=ok.cycle,
                             hovertemplate="Ciclo %{customdata}<br>TG %{x:.1f} cm · SWOT+DAC %{y:.1f} cm"
                                           "<extra></extra>"))
    fig.add_trace(go.Scatter(x=tg, y=100 * ok.dac_median, mode="markers", name=ETIQUETA_B,
                             marker=dict(color=COLOR_B, size=7, symbol="triangle-up"), customdata=ok.cycle,
                             hovertemplate="Ciclo %{customdata}<br>TG %{x:.1f} cm · DAC %{y:.1f} cm<extra></extra>"))
    lim = float(np.nanmax(np.abs(np.r_[tg, 100 * ok.swot_corrected - desplazamiento_cm, 100 * ok.dac_median]))) * 1.1
    fig.add_trace(go.Scatter(x=[-lim, lim], y=[-lim, lim], mode="lines", line=dict(color=GRIS, dash="dot", width=1),
                             name="1:1", hoverinfo="skip"))
    fig.update_xaxes(title="Mareógrafo (cm)", range=[-lim, lim])
    fig.update_yaxes(title="Satélite / modelo (cm)", range=[-lim, lim], scaleanchor="x", scaleratio=1)
    return _base(fig, alto)


def cobertura(df, alto=300):
    """Píxeles en el círculo y tras cada filtro, por ciclo (incluidos los excluidos, en blanco)."""
    fig = go.Figure()
    for col, etq, color in (("pixels_in_circle", "En el círculo", REJILLA),
                            ("pixels_after_quality_flag", "Calidad = 0", "#9db8d9"),
                            ("pixels_after_mad", "Tras valores atípicos", "#0f4c75")):
        fig.add_trace(go.Bar(x=df.cycle, y=df[col], name=etq, marker_color=color,
                             hovertemplate="Ciclo %{x}: %{y:.0f} píxeles<extra>" + etq + "</extra>"))
    fig.update_layout(barmode="overlay")
    fig.update_xaxes(title="Ciclo", dtick=2)
    fig.update_yaxes(title="Píxeles")
    return _base(fig, alto)


# ---------------------------------------------------------------- ¿aporta SWOT?


def forest(filas, alto=None):
    """filas: [(etiqueta, fila de la tabla maestra)]. r A/B, RMSE A/B y ΔRMSE A − B con IC 95 %."""
    y = [e for e, _ in filas]
    alto = alto or 120 + 42 * len(filas)
    fig = make_subplots(rows=1, cols=3, shared_yaxes=True, horizontal_spacing=0.04, column_widths=[0.3, 0.3, 0.4],
                        subplot_titles=("Correlación r", "RMSE sin desplazamiento (cm)",
                                        "ΔRMSE A − B (cm) e IC 95 %"))
    for col, (ca, cb) in enumerate((("A_r", "B_r"), ("A_rmse_wo_offset_cm", "B_rmse_wo_offset_cm")), start=1):
        for e, f in filas:
            fig.add_trace(go.Scatter(x=[f[ca], f[cb]], y=[e, e], mode="lines", line=dict(color=REJILLA, width=3),
                                     showlegend=False, hoverinfo="skip"), row=1, col=col)
        fig.add_trace(go.Scatter(x=[f[ca] for _, f in filas], y=y, mode="markers", name=f"A: {ETIQUETA_A}",
                                 marker=dict(color=COLOR_A, size=11), showlegend=col == 1,
                                 hovertemplate="%{y}<br>A: %{x:.2f}<extra></extra>"), row=1, col=col)
        fig.add_trace(go.Scatter(x=[f[cb] for _, f in filas], y=y, mode="markers", name="B: DAC solo",
                                 marker=dict(color=COLOR_B, size=10, symbol="square"), showlegend=col == 1,
                                 hovertemplate="%{y}<br>B: %{x:.2f}<extra></extra>"), row=1, col=col)
    d = np.array([f.dRMSE_AB_cm for _, f in filas])
    lo = np.array([f.dRMSE_AB_ci_low for _, f in filas])
    hi = np.array([f.dRMSE_AB_ci_high for _, f in filas])
    concluyente = lo > 0
    fig.add_trace(go.Scatter(
        x=d, y=y, mode="markers", showlegend=False,
        marker=dict(color=[("#b3261e" if c else TINTA) for c in concluyente], size=10),
        error_x=dict(type="data", symmetric=False, array=hi - d, arrayminus=d - lo, color=GRIS, thickness=2, width=0),
        customdata=np.c_[lo, hi],
        hovertemplate="%{y}<br>ΔRMSE %{x:+.1f} cm<br>IC 95 % [%{customdata[0]:+.1f}, %{customdata[1]:+.1f}]"
                      "<extra></extra>"), row=1, col=3)
    fig.add_vline(x=0, line_dash="dash", line_color=GRIS, row=1, col=3)
    fig.update_yaxes(autorange="reversed")
    return _base(fig, alto, subtitulos=True)


# ---------------------------------------------------------------- radio


def radio_track(track, estaciones, alto=420):
    """ΔRMSE A − B (IC 95 %) y píxeles válidos a 6/8/10 km, muestra común a los tres radios."""
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1,
                        subplot_titles=("ΔRMSE A − B (cm) e IC 95 %", "Píxeles válidos por paso (mediana)"))
    salto = np.linspace(-0.3, 0.3, max(len(estaciones), 2))
    for j, s in zip(salto, estaciones):
        e = D.ESTACIONES[s]
        ff = [D.fila(s, track, r, "común") for r in D.RADIOS]
        if any(f is None or np.isnan(f.dRMSE_AB_cm) for f in ff):
            continue
        d = np.array([f.dRMSE_AB_cm for f in ff])
        lo = np.array([f.dRMSE_AB_ci_low for f in ff])
        hi = np.array([f.dRMSE_AB_ci_high for f in ff])
        nom = f"{e['nombre']} (n {int(ff[0].n)})"
        fig.add_trace(go.Scatter(
            x=np.array(D.RADIOS) + j, y=d, mode="lines+markers", name=nom, legendgroup=s,
            line=dict(color=e["color"], width=2), marker=dict(symbol=e["marcador"], size=10, color=e["color"]),
            error_y=dict(type="data", symmetric=False, array=hi - d, arrayminus=d - lo, color=e["color"],
                         thickness=1.4, width=0),
            customdata=np.c_[D.RADIOS, lo, hi],
            hovertemplate=(e["nombre"] + " · %{customdata[0]:.0f} km<br>ΔRMSE %{y:+.1f} cm"
                           "<br>IC [%{customdata[1]:+.1f}, %{customdata[2]:+.1f}]<extra></extra>")), row=1, col=1)
        fig.add_trace(go.Scatter(
            x=list(D.RADIOS), y=[f.sample_median_pixels for f in ff], mode="lines+markers", name=nom,
            legendgroup=s, showlegend=False, line=dict(color=e["color"], width=2),
            marker=dict(symbol=e["marcador"], size=10, color=e["color"]),
            hovertemplate=e["nombre"] + " · %{x} km<br>%{y:.0f} píxeles<extra></extra>"), row=1, col=2)
    fig.add_hline(y=0, line_dash="dash", line_color=GRIS, row=1, col=1)
    fig.update_xaxes(tickvals=list(D.RADIOS), title="Radio de búsqueda (km)")
    fig.update_yaxes(title="cm", row=1, col=1)
    # Log con marcas fijas: sin etiquetas en las divisiones menores (2, 3… 9)
    fig.update_yaxes(type="log", tickvals=[10, 20, 50, 100, 200, 500, 1000, 2000, 5000],
                     ticktext=["10", "20", "50", "100", "200", "500", "1000", "2000", "5000"],
                     title="píxeles", row=1, col=2)
    return _base(fig, alto, subtitulos=True)


# ---------------------------------------------------------------- análisis regional


def regional_d(track, alto=400):
    d, tiempos = D.d_centrada(track)
    cm = d.mean(axis=1)
    fig = go.Figure()
    for s in d.columns:
        e = D.ESTACIONES[s]
        fig.add_trace(go.Scatter(x=tiempos, y=d[s], name=e["nombre"], mode="lines+markers",
                                 line=dict(color=e["color"], width=1.3), marker=dict(symbol=e["marcador"], size=7),
                                 customdata=d.index,
                                 hovertemplate="Ciclo %{customdata}: %{y:+.1f} cm<extra>" + e["nombre"] + "</extra>"))
    fig.add_trace(go.Scatter(x=tiempos, y=cm, name=f"Modo común (T{track})", mode="lines",
                             line=dict(color=TINTA, width=4), customdata=d.index,
                             hovertemplate="Ciclo %{customdata}: %{y:+.1f} cm<extra>Modo común</extra>"))
    fig.add_hline(y=0, line_color=REJILLA)
    fig.update_yaxes(title="d centrada (cm)")
    return _base(fig, alto)


def entre_tracks(alto=420):
    cm154, t154 = D.modo_comun(154)
    cm197, _ = D.modo_comun(197)
    both = cm154.index.intersection(cm197.index)
    g = D.tracks_json()["cross_track"]["common_mode_t154_vs_t197"]
    lim = float(np.nanmax(np.abs(np.r_[cm154.loc[both], cm197.loc[both]]))) * 1.15
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[-lim, lim], y=[-lim, lim], mode="lines", line=dict(color=REJILLA, width=1),
                             hoverinfo="skip", showlegend=False))
    fig.add_trace(go.Scatter(x=cm197.loc[both], y=cm154.loc[both], mode="markers", showlegend=False,
                             marker=dict(color=TINTA, size=10, line=dict(color="white", width=1)),
                             customdata=np.c_[both, t154.loc[both].dt.strftime("%Y-%m-%d")],
                             hovertemplate="Ciclo %{customdata[0]} (%{customdata[1]})<br>T197 %{x:+.1f} cm"
                                           "<br>T154 %{y:+.1f} cm<extra></extra>"))
    fig.add_annotation(x=0.03, y=0.97, xref="paper", yref="paper", showarrow=False, align="left",
                       text=f"r = {g['r']:.2f} (n = {g['n']} ciclos)", font=dict(size=14))
    fig.update_xaxes(title="Modo común, track 197 (cm)", range=[-lim, lim])
    fig.update_yaxes(title="Modo común, track 154 (cm)", range=[-lim, lim], scaleanchor="x", scaleratio=1)
    return _base(fig, alto, leyenda=False)


def modo_comun_mareas(alto=420):
    fig = go.Figure()
    lim = 0.0
    for track, simbolo, relleno in ((197, "circle", TINTA), (154, "square", "white")):
        _, ciclos, medias, tiempos = D.descomp_centrada(track)
        x = 100 * medias.loc[ciclos, "tide_prediction_difference_m_c"]
        y = 100 * medias.loc[ciclos, "difference_c"]
        r, n = D.r_guardada(track, "tide_prediction_difference_m")
        fig.add_trace(go.Scatter(
            x=x, y=y, mode="markers", name=f"Track {track}: r = {r:.2f} (n = {n})",
            marker=dict(symbol=simbolo, size=10, color=relleno, line=dict(color=TINTA, width=1.5)),
            customdata=np.c_[ciclos, tiempos.loc[ciclos].dt.strftime("%Y-%m-%d")],
            hovertemplate="T" + str(track) + " · ciclo %{customdata[0]} (%{customdata[1]})"
                                             "<br>Δ predicciones %{x:+.1f} cm<br>Modo común %{y:+.1f} cm"
                                             "<extra></extra>"))
        lim = max(lim, float(np.nanmax(np.abs(np.r_[x, y]))) * 1.15)
    fig.add_trace(go.Scatter(x=[-lim, lim], y=[-lim, lim], mode="lines", line=dict(color=REJILLA, width=1),
                             hoverinfo="skip", showlegend=False))
    fig.update_xaxes(title="Predicción del mareógrafo − marea de SWOT (cm)", range=[-lim, lim])
    fig.update_yaxes(title="Modo común (cm)", range=[-lim, lim], scaleanchor="x", scaleratio=1)
    return _base(fig, alto)


COMPONENTES = {
    "difference": "d = SWOT + DAC − mareógrafo",
    "tide_prediction_difference_m": "Predicción del mareógrafo − marea oceánica e interna de SWOT",
    "agg_ssha_unfiltered": "Anomalía de SWOT (SSHA)",
    "agg_dac": "DAC",
    "tg_residual": "Residuo del mareógrafo",
}


def componentes(track, alto=None):
    sub, ciclos, medias, tiempos = D.descomp_centrada(track)
    est = D.REFERENCIA_MODO_COMUN[track]
    cols = list(COMPONENTES)
    titulos = []
    for c in cols:
        if c == "difference":
            titulos.append(COMPONENTES[c])
        else:
            r, n = D.r_guardada(track, c)
            titulos.append(f"{COMPONENTES[c]} · r con el modo común {signo(r, 2)} (n {n})")
    fig = make_subplots(rows=len(cols), cols=1, shared_xaxes=True, vertical_spacing=0.05, subplot_titles=titulos)
    for i, c in enumerate(cols, start=1):
        for s in est:
            e = D.ESTACIONES[s]
            st_ = sub[sub.station == s].sort_values("cycle")
            fig.add_trace(go.Scatter(x=st_.cycle.map(tiempos), y=100 * st_[c + "_c"], mode="lines+markers",
                                     name=e["nombre"], legendgroup=s, showlegend=i == 1,
                                     line=dict(color=e["color"], width=1.1), marker=dict(symbol=e["marcador"], size=6),
                                     hovertemplate="%{y:+.1f} cm<extra>" + e["nombre"] + "</extra>"), row=i, col=1)
        fig.add_trace(go.Scatter(x=tiempos.loc[ciclos], y=100 * medias.loc[ciclos, c + "_c"], mode="lines",
                                 name="Media del track", legendgroup="media", showlegend=i == 1,
                                 line=dict(color=TINTA, width=3), hovertemplate="%{y:+.1f} cm<extra>media</extra>"),
                      row=i, col=1)
        fig.update_yaxes(title_text="cm", row=i, col=1)
    _base(fig, alto or 190 * len(cols), subtitulos=True)
    fig.update_annotations(font=dict(size=12, color=TINTA), xanchor="left", x=0)
    return fig
