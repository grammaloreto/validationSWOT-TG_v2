"""
Estilo común del demo: tokens de color, CSS, cabecera de página, tarjetas de cifras y avisos.

La paleta de estaciones y de comparaciones (A: SWOT+DAC, B: DAC solo) es la de las figuras del paper, para que el
demo y el paper se lean igual.
"""
import html

import streamlit as st

TINTA = "#1a1a19"
GRIS = "#6b6a64"
REJILLA = "#e4e3de"
SUPERFICIE = "#fcfcfb"
OCEANO = "#0f4c75"
COLOR_A = "#6250d6"   # A: SWOT + DAC
COLOR_B = "#008300"   # B: DAC solo
COLOR_TG = TINTA      # mareógrafo
COLOR_TRACK = {197: "#2a78d6", 154: "#eb6834"}

ETIQUETA_A = "SWOT + DAC"
ETIQUETA_B = "DAC solo (modelo atmosférico)"
ETIQUETA_TG = "Mareógrafo (nivel − marea)"

_CSS = f"""
<style>
.block-container {{ padding-top: 2.2rem; max-width: 1180px; }}
h1, h2, h3 {{ color: {TINTA}; letter-spacing: -0.01em; }}
.dvv-eyebrow {{ color: {OCEANO}; font-size: .78rem; font-weight: 600; letter-spacing: .08em;
  text-transform: uppercase; margin-bottom: .2rem; }}
.dvv-lead {{ color: #3b3a36; font-size: 1.08rem; line-height: 1.55; max-width: 62rem; margin-bottom: .6rem; }}
.dvv-card {{ background: #ffffff; border: 1px solid {REJILLA}; border-top: 4px solid var(--acento, {OCEANO});
  border-radius: 12px; padding: 16px 18px 14px; height: 100%; box-shadow: 0 1px 2px rgba(15,76,117,.06);
  transition: box-shadow .15s ease, transform .15s ease; }}
.dvv-card:hover {{ box-shadow: 0 6px 18px rgba(15,76,117,.12); transform: translateY(-1px); }}
.dvv-card .i {{ font-size: 1.15rem; line-height: 1; margin-bottom: 8px; }}
.dvv-card .v {{ font-size: 1.9rem; font-weight: 700; color: var(--acento, {OCEANO}); line-height: 1.1;
  letter-spacing: -0.02em; }}
.dvv-card .k {{ font-size: .84rem; color: {GRIS}; margin-top: 6px; line-height: 1.4; }}
.dvv-hero {{ position: relative; overflow: hidden; border-radius: 18px; padding: 34px 36px 58px;
  margin: 0 0 22px; color: #ffffff;
  background: radial-gradient(circle at 85% 15%, rgba(120,190,235,.35) 0, rgba(120,190,235,0) 45%),
              linear-gradient(135deg, #0a2e47 0%, #0f4c75 55%, #1b6ca8 100%); }}
.dvv-hero .e {{ font-size: .78rem; font-weight: 600; letter-spacing: .12em; text-transform: uppercase;
  color: #9fd3f5; margin-bottom: 10px; }}
.dvv-hero h1 {{ color: #ffffff; font-size: 2.5rem; line-height: 1.12; margin: 0 0 14px; padding: 0;
  max-width: 46rem; letter-spacing: -0.02em; }}
.dvv-hero .l {{ color: #dceaf5; font-size: 1.08rem; line-height: 1.6; max-width: 58rem; }}
.dvv-hero .l b {{ color: #ffffff; }}
.dvv-hero svg {{ position: absolute; left: 0; bottom: 0; width: 100%; height: 46px; }}
.dvv-num {{ display: inline-flex; align-items: center; justify-content: center; width: 28px; height: 28px;
  border-radius: 50%; background: var(--acento, {OCEANO}); color: #fff; font-weight: 700; font-size: .9rem;
  margin-right: 8px; flex: none; }}
.dvv-finding .t {{ display: flex; align-items: center; }}
.dvv-finding {{ background: {SUPERFICIE}; border: 1px solid {REJILLA}; border-left: 4px solid {OCEANO};
  border-radius: 8px; padding: 14px 16px; margin: 6px 0 10px; height: 100%; }}
.dvv-finding .t {{ font-weight: 650; color: {TINTA}; margin-bottom: 6px; font-size: 1.0rem; }}
.dvv-finding .b {{ color: #3b3a36; font-size: .93rem; line-height: 1.5; }}
.dvv-note {{ background: #f1f4f8; border-radius: 8px; padding: 10px 14px; color: #2c3e50; font-size: .9rem;
  line-height: 1.5; margin: 6px 0 12px; }}
.dvv-warn {{ background: #fdf6e7; border-radius: 8px; padding: 10px 14px; color: #5a4300; font-size: .9rem;
  line-height: 1.5; margin: 6px 0 12px; }}
.dvv-pill {{ display: inline-block; border-radius: 999px; padding: 1px 9px; font-size: .75rem; font-weight: 600;
  margin-right: 4px; }}
.dvv-main {{ background: #e3eefb; color: #1d4f8f; }}
.dvv-expl {{ background: #efeee9; color: #55544f; }}
</style>
"""


def aplicar():
    st.markdown(_CSS, unsafe_allow_html=True)


def cabecera(antetitulo, titulo, entradilla=None):
    aplicar()
    st.markdown(f'<div class="dvv-eyebrow">{html.escape(antetitulo)}</div>', unsafe_allow_html=True)
    st.title(titulo)
    if entradilla:
        st.markdown(f'<div class="dvv-lead">{entradilla}</div>', unsafe_allow_html=True)


_OLA = ('<svg viewBox="0 0 1200 46" preserveAspectRatio="none" aria-hidden="true">'
        '<path d="M0,26 C150,46 300,6 450,22 C600,38 750,10 900,22 C1020,32 1110,18 1200,24 L1200,46 L0,46 Z" '
        'fill="rgba(255,255,255,.10)"/>'
        '<path d="M0,34 C180,20 320,46 520,32 C700,20 860,44 1040,32 C1110,28 1160,34 1200,36 L1200,46 L0,46 Z" '
        'fill="#ffffff"/></svg>')

# Acentos de las tarjetas (tonos de la paleta del demo)
ACENTOS = ["#0f4c75", "#1b6ca8", COLOR_A, COLOR_B, "#eb6834"]


def portada(antetitulo, titulo, entradilla):
    """Cabecera destacada de la portada: degradado océano, texto en blanco y una ola decorativa."""
    aplicar()
    st.markdown(f'<div class="dvv-hero"><div class="e">{html.escape(antetitulo)}</div><h1>{titulo}</h1>'
                f'<div class="l">{entradilla}</div>{_OLA}</div>', unsafe_allow_html=True)


def tarjetas(items):
    """items: [(valor, texto)] o [(valor, texto, icono)]; una fila de tarjetas de cifras con acento de color."""
    cols = st.columns(len(items))
    for i, (col, item) in enumerate(zip(cols, items)):
        valor, texto, icono = (item + ("",))[:3]
        col.markdown(f'<div class="dvv-card" style="--acento:{ACENTOS[i % len(ACENTOS)]}">'
                     + (f'<div class="i">{icono}</div>' if icono else "")
                     + f'<div class="v">{valor}</div><div class="k">{texto}</div></div>', unsafe_allow_html=True)


def hallazgo(titulo, cuerpo, numero=None, acento=OCEANO):
    marca = f'<span class="dvv-num" style="--acento:{acento}">{numero}</span>' if numero else ""
    st.markdown(f'<div class="dvv-finding" style="border-left-color:{acento}"><div class="t">{marca}'
                f'<span>{titulo}</span></div><div class="b">{cuerpo}</div></div>', unsafe_allow_html=True)


def nota(texto):
    st.markdown(f'<div class="dvv-note">{texto}</div>', unsafe_allow_html=True)


def aviso(texto):
    st.markdown(f'<div class="dvv-warn">{texto}</div>', unsafe_allow_html=True)


def papel(rol):
    clase, texto = ("dvv-main", "principal") if rol == "principal" else ("dvv-expl", "exploratoria")
    return f'<span class="dvv-pill {clase}">{texto}</span>'


def signo(x, dec=1):
    """Número con signo y menos tipográfico."""
    return f"{x:+.{dec}f}".replace("-", "−")


def num(x, dec=2):
    return f"{x:.{dec}f}".replace("-", "−")


def intervalo(lo, hi, dec=1):
    return f"[{signo(lo, dec)}, {signo(hi, dec)}]"
