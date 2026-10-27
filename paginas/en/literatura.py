"""Cómo encajan los resultados con otros estudios de SWOT frente a mareógrafos."""
import pandas as pd
import streamlit as st

from nucleo import datos as D
from nucleo import estilo as E

E.cabecera(
    "Context · Related studies",
    "How it fits with other SWOT validations",
    "SWOT is a recent mission and coastal validations against tide gauges are still few. We compare our design and "
    "our figures with the closest studies, <b>using only works we have read</b>, and distinguish what is comparable "
    "from what is not.",
)

main = [D.fila(s, tr) for s, tr, rol in D.combinaciones() if rol == "principal"]
largas = [f for f in main if f.n >= 20]
r_rango = f"{E.num(min(f.A_r for f in largas))}–{E.num(max(f.A_r for f in largas))}"

tabla = pd.DataFrame([
    {"Study": "This work", "Area": "Galicia (7 REDMAR ports)",
     "What is compared": "Non-tidal sea level, with the DAC restored, and the DAC alone as reference",
     "SWOT phase": "Science, 21 days (20 months)", "Main figures": f"r = {r_rango} (SWOT + DAC)"},
    {"Study": "Han et al. (2026)", "Area": "West coast of Canada (2 tide gauges)",
     "What is compared": "Non-tidal sea level, with the DAC restored", "SWOT phase": "1-day repeat",
     "Main figures": "r = 0.88 and 0.89; RMS 4.9 and 5.1 cm"},
    {"Study": "Lichtman et al. (2025)", "Area": "Bristol Channel and Severn Estuary (hyper-tidal)",
     "What is compared": "Total water level, tide included", "SWOT phase": "—",
     "Main figures": "RMSD 0.137 m, slope 0.99"},
    {"Study": "Rong et al. (2026)", "Area": "Bristol Channel and Severn Estuary",
     "What is compared": "Total water level, tide included", "SWOT phase": "—",
     "Main figures": "RMSE 0.13 m"},
    {"Study": "Gómez-Enri et al. (2025)", "Area": "Puertos del Estado (Huelva, Barcelona, Bilbao)",
     "What is compared": "Agreement depending on the tide model", "SWOT phase": "—",
     "Main figures": "The choice of tide model changes the agreement"},
])
st.dataframe(tabla, hide_index=True, use_container_width=True)

c1, c2 = st.columns(2)
with c1:
    E.hallazgo(
        "Han et al. (2026): the closest study",
        "They compared the same SWOT L3 product, with the DAC restored, with two Canadian tide gauges and obtained "
        "correlations of 0.88 and 0.89, much better than those of conventional altimetry (DUACS nadir: 0.60 and "
        "0.42). <b>Our correlations are of the same order.</b> What our comparison adds is the reference of the "
        "DAC alone, which they did not include and without which the contribution of SWOT cannot be separated "
        "from that of the atmospheric model. They also worked in the 1-day repeat phase, with the filtered anomaly "
        "and a harmonic prediction from the record itself.")
    E.hallazgo(
        "Gómez-Enri et al. (2025): the tide matters",
        "With Puertos del Estado tide gauges at Huelva, Barcelona and Bilbao, they found that the choice of tide "
        "model changes the agreement of SWOT with the tide gauges, in line with the regional pattern we observe "
        "in Galicia.")
with c2:
    E.hallazgo(
        "Lichtman et al. (2025) and Rong et al. (2026): a different question",
        "They validated SWOT in the Severn, one of the estuaries with the largest tidal range in the world, "
        "comparing the <b>total</b> water level. There the tide dominates the variance and their errors of about "
        "13 cm mostly reflect how well the tide is reproduced. <b>They are not comparable</b> with our figures, "
        "which measure what remains once the tide is removed: the two designs answer different questions.")
    E.hallazgo(
        "Ray et al. (2021) and Carrère and Lyard (2003): the pieces of the reasoning",
        "Ray et al. estimated the seasonal cycle at hundreds of tide gauges: the annual and semiannual "
        "constituents (Sa, Ssa) mainly capture meteorological forcing, the basis of our hypothesis for the "
        "regional pattern. Carrère and Lyard describe the model on which the DAC is based and how much it reduces "
        "the variability at tide gauges, which explains why the DAC alone is such a demanding reference.")

st.markdown("### What this validation adds")
st.markdown(
    "1. **A DAC-alone reference**, to separate the contribution of SWOT from that of the atmospheric model.\n"
    "2. **Stations treated as dependent series**, with the regional analysis separate from the metrics by "
    "station.\n"
    "3. **Attention to the two tide predictions**, whose difference enters the non-tidal comparison "
    "directly.\n"
    "4. **Valid coverage as a precondition**, before comparing stations in rías or surrounded by land.")

with st.expander("References"):
    st.markdown(
        "- Carrère, L., & Lyard, F. (2003). Modeling the barotropic response of the global ocean to atmospheric "
        "wind and pressure forcing — comparisons with observations. *Geophysical Research Letters*, 30(6), 1275. "
        "https://doi.org/10.1029/2002GL016473\n"
        "- CLS/CNES (2025). *DUACS Level-3 SWOT KaRIn (L3_LR_SSH) User Handbook*, Issue 2.1. AVISO.\n"
        "- Gómez-Enri, J., Arribas-Rodríguez, B., Tejedor, B., Álvarez, O., González, C. J., & Vignudelli, S. "
        "(2025). *Accuracy assessment of SWOT KaRIn sea level data* [Poster]. SWOT Science Team Meeting 2025.\n"
        "- Han, G., Klymak, J. M., Ross, T., & Chen, N. (2026). Validation of 1-day repeat SWOT measurements "
        "against tide-gauge and glider data off Canada's West Coast. *Geophysical Research Letters*, 53, "
        "e2025GL119491. https://doi.org/10.1029/2025GL119491\n"
        "- Lichtman, I. D., Bell, P. S., Gommenginger, C., Banks, C., Calafat, F. M., Brown, J., & Williams, "
        "S. D. P. (2025). Evaluating water levels from the Surface Water and Ocean Topography (SWOT) mission in a "
        "hyper-tidal coastal and estuarine environment. *Earth and Space Science*, 12, e2024EA004104. "
        "https://doi.org/10.1029/2024EA004104\n"
        "- Puertos del Estado (2024). *Conjunto de datos: REDMAR* [REDMAR dataset]. "
        "https://bancodatos.puertos.es/BD/informes/INT_3.pdf\n"
        "- Ray, R. D., Loomis, B. D., & Zlotnicki, V. (2021). The mean seasonal cycle in relative sea level from "
        "satellite altimetry and gravimetry. *Journal of Geodesy*, 95, 80. "
        "https://doi.org/10.1007/s00190-021-01529-1\n"
        "- Rong, Y., Bates, P., Neal, J., Bell, P., Gommenginger, C., Lichtman, I. D., et al. (2026). Evaluating "
        "SWOT in the coastal zone: Comparisons with tide gauge and airborne LiDAR in the Bristol Channel and "
        "Severn Estuary, UK. *Geophysical Research Letters*, 53, e2025GL116590. "
        "https://doi.org/10.1029/2025GL116590\n"
        "- SWOT L3 LR SSH Unsmoothed, version 2.0.1. DOI 10.24400/527896/A01-2024.003")
