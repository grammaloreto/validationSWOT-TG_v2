"""Portada: qué se evalúa, cifras clave y los tres hallazgos, en lenguaje general."""
import streamlit as st

from nucleo import datos as D
from nucleo import estilo as E

E.portada(
    "Digital Twin of the Ocean · Validation",
    "How closely does SWOT match the tide gauges of Galicia?",
    "The <b>SWOT</b> satellite measures sea level at an unprecedented resolution, even very close to the coast. "
    "Before using that information in the digital twin, we compare it with what the "
    "<b>Puertos del Estado tide gauges</b> record in seven Galician ports, pass by pass, over 20 months. "
    "And we ask a more demanding question than “do they look alike?”: <b>how much of that agreement is "
    "really due to SWOT?</b>",
)

main = [D.fila(s, tr) for s, tr, rol in D.combinaciones() if rol == "principal"]
largas = [f for f in main if f.n >= 20]
pares = int(sum(f.n for f in main))
con_cero = sum(f.dRMSE_AB_ci_low <= 0 <= f.dRMSE_AB_ci_high for f in main)

E.tarjetas([
    (f"{len(main)}", "station–track combinations with a main result (10 km radius)", "📍"),
    (f"{pares}", "satellite–tide gauge pairs in those combinations, one per SWOT pass", "🛰️"),
    (f"{E.num(min(f.A_r for f in largas))}–{E.num(max(f.A_r for f in largas))}",
     "correlation of SWOT + DAC with the tide gauge in the long series", "📈"),
    (f"{con_cero} of {len(main)}",
     "stations where SWOT does not demonstrably improve on the atmospheric model alone", "⚖️"),
])

st.markdown("### Three findings")
c1, c2, c3 = st.columns(3)
with c1:
    E.hallazgo(
        "SWOT follows the tide gauges, but not better than the atmospheric model",
        "With the atmospheric correction (DAC) restored, SWOT rises and falls with the tide gauge. But the DAC on "
        "its own reaches similar correlations and a somewhat lower error. Much of the agreement is already "
        "explained by the effect of pressure and wind.", numero=1, acento=E.COLOR_A)
    st.page_link("paginas/en/aporta_swot.py", label="See the comparison", icon=":material/arrow_forward:")
with c2:
    E.hallazgo(
        "Getting closer to the station does not improve the comparison",
        "Reducing the search circle from 10 to 6 km leaves fewer valid pixels and, in general, does not bring SWOT "
        "closer to the tide gauge. The worst cases appear where the circle barely sees water: in the rías, "
        "coverage matters more than proximity.", numero=2, acento="#eb6834")
    st.page_link("paginas/en/radio.py", label="See the sensitivity to the radius", icon=":material/arrow_forward:")
with c3:
    E.hallazgo(
        "The stations share the same discrepancy",
        "The SWOT − tide gauge difference rises and falls at the same time along the north coast, repeats in the "
        "two passes 37 hours apart and closely follows the difference between the two tide predictions. It is an "
        "association, not proof of cause, but it shows where to look.", numero=3, acento="#1b6ca8")
    st.page_link("paginas/en/regional.py", label="See the regional pattern", icon=":material/arrow_forward:")

st.markdown("### What it means for the digital twin")
a, b = st.columns(2)
with a:
    st.markdown(
        "- **SWOT is useful on the Galician coast, but its own contribution has to be demonstrated.** A good "
        "correlation with the tide gauge is not enough: it has to be compared with that of the atmospheric model "
        "alone.\n"
        "- **Nearby stations are not independent tests.** Agreement among several of them does not confirm the "
        "result if they share the same pass and the same discrepancy.")
with b:
    st.markdown(
        "- **The two tide predictions must be consistent.** Before interpreting a difference, one needs to know "
        "which tidal components each system removes.\n"
        "- **Coverage matters more than proximity.** In rías and ports surrounded by land, the number of valid "
        "pixels decides whether the comparison can be interpreted.")

with st.expander("For those who want the detail: what exactly is compared"):
    st.markdown(
        "Each time SWOT flies over a station, **one satellite value and one tide gauge value** are obtained; "
        "the metrics are computed across passes, over the 20 months.")
    st.latex(r"d \;=\; \underbrace{\mathcal{A}(S + D)}_{\text{SWOT + DAC}} \;-\; "
             r"\underbrace{\big[H_{TG}(t_p) - T_{TG}(t_p)\big]}_{\text{tide gauge residual}}")
    st.markdown(
        "- *S*: unfiltered SWOT L3 v2.0.1 sea level anomaly (`ssha_unfiltered`), with the global model tide "
        "already removed.\n"
        "- *D*: dynamic atmospheric correction (DAC), which the product subtracts and is restored here, because "
        "the tide gauge does record the effect of pressure and wind.\n"
        "- 𝒜: median of the medians of 1 km segments within a 10 km circle (6 and 8 km as sensitivity), using "
        "only quality 0 pixels.\n"
        "- *H*, *T*: hourly tide gauge sea level and Puertos del Estado astronomical prediction, interpolated to "
        "the actual pass time.\n\n"
        "Three comparisons are evaluated on the same passes: **A** (SWOT + DAC against the tide gauge), "
        "**B** (DAC alone against the tide gauge, the reference) and **C** (SWOT anomaly against the tide gauge "
        "minus the DAC).")
