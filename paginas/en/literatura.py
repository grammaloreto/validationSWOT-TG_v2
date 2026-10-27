"""Cómo encajan los resultados con otros estudios de SWOT frente a mareógrafos."""
import pandas as pd
import streamlit as st

from nucleo import datos as D
from nucleo import estilo as E
from nucleo import textos as T

E.aplicar()
E.aviso(T.t("traduccion_pendiente"))  # retirar al traducir la página
E.cabecera(
    "Contexto · Otros estudios",
    "Cómo encaja con otras validaciones de SWOT",
    "SWOT es una misión reciente y las validaciones costeras frente a mareógrafos son todavía pocas. Comparamos "
    "nuestro diseño y nuestras cifras con los estudios más cercanos, <b>solo con trabajos leídos</b>, y "
    "distinguimos qué es comparable y qué no.",
)

main = [D.fila(s, tr) for s, tr, rol in D.combinaciones() if rol == "principal"]
largas = [f for f in main if f.n >= 20]
r_rango = f"{E.num(min(f.A_r for f in largas))}–{E.num(max(f.A_r for f in largas))}"

tabla = pd.DataFrame([
    {"Estudio": "Este trabajo", "Zona": "Galicia (7 puertos REDMAR)",
     "Qué se compara": "Nivel sin marea, con el DAC devuelto, y el DAC solo como referencia",
     "Fase de SWOT": "Científica, 21 días (20 meses)", "Cifras principales": f"r = {r_rango} (SWOT + DAC)"},
    {"Estudio": "Han et al. (2026)", "Zona": "Costa oeste de Canadá (2 mareógrafos)",
     "Qué se compara": "Nivel sin marea, con el DAC devuelto", "Fase de SWOT": "Repetición de 1 día",
     "Cifras principales": "r = 0.88 y 0.89; RMS 4.9 y 5.1 cm"},
    {"Estudio": "Lichtman et al. (2025)", "Zona": "Bristol Channel y estuario del Severn (hipermareal)",
     "Qué se compara": "Nivel total del agua, marea incluida", "Fase de SWOT": "—",
     "Cifras principales": "RMSD 0.137 m, pendiente 0.99"},
    {"Estudio": "Rong et al. (2026)", "Zona": "Bristol Channel y estuario del Severn",
     "Qué se compara": "Nivel total del agua, marea incluida", "Fase de SWOT": "—",
     "Cifras principales": "RMSE 0.13 m"},
    {"Estudio": "Gómez-Enri et al. (2025)", "Zona": "Puertos del Estado (Huelva, Barcelona, Bilbao)",
     "Qué se compara": "Concordancia según el modelo de marea", "Fase de SWOT": "—",
     "Cifras principales": "La elección del modelo de marea cambia la concordancia"},
])
st.dataframe(tabla, hide_index=True, use_container_width=True)

c1, c2 = st.columns(2)
with c1:
    E.hallazgo(
        "Han et al. (2026): el estudio más cercano",
        "Compararon el mismo producto SWOT L3, con el DAC devuelto, con dos mareógrafos canadienses y obtuvieron "
        "correlaciones de 0.88 y 0.89, mucho mejores que las de la altimetría convencional (DUACS nadir: 0.60 y "
        "0.42). <b>Nuestras correlaciones son del mismo orden.</b> Lo que añade nuestra comparación es la "
        "referencia del DAC solo, que ellos no incluyeron y sin la cual la aportación de SWOT no puede separarse "
        "de la del modelo atmosférico. Trabajaron además en la fase de repetición diaria, con la anomalía filtrada "
        "y una predicción armónica del propio registro.")
    E.hallazgo(
        "Gómez-Enri et al. (2025): la marea importa",
        "Con mareógrafos de Puertos del Estado en Huelva, Barcelona y Bilbao, encontraron que la elección del "
        "modelo de marea cambia la concordancia de SWOT con los mareógrafos, en línea con el patrón regional que "
        "observamos en Galicia.")
with c2:
    E.hallazgo(
        "Lichtman et al. (2025) y Rong et al. (2026): otra pregunta",
        "Validaron SWOT en el Severn, uno de los estuarios con mayor rango de marea del mundo, comparando el "
        "<b>nivel total</b> del agua. Allí la marea domina la varianza y sus errores de unos 13 cm reflejan sobre "
        "todo cómo se reproduce la marea. <b>No son comparables</b> con nuestras cifras, que miden lo que queda "
        "una vez retirada la marea: los dos diseños responden a preguntas distintas.")
    E.hallazgo(
        "Ray et al. (2021) y Carrère y Lyard (2003): las piezas del razonamiento",
        "Ray et al. estimaron el ciclo estacional en cientos de mareógrafos: las componentes anual y semianual "
        "(Sa, Ssa) recogen sobre todo forzamiento meteorológico, la base de nuestra hipótesis para el patrón "
        "regional. Carrère y Lyard describen el modelo en que se basa el DAC y cuánto reduce la variabilidad en "
        "los mareógrafos, lo que explica que el DAC solo sea una referencia tan exigente.")

st.markdown("### Qué aporta esta validación")
st.markdown(
    "1. **Una referencia del DAC solo**, para separar la aportación de SWOT de la del modelo atmosférico.\n"
    "2. **Estaciones tratadas como series dependientes**, con el análisis regional aparte de las métricas por "
    "estación.\n"
    "3. **Atención a las dos predicciones de marea**, cuya diferencia entra directamente en la comparación sin "
    "marea.\n"
    "4. **La cobertura válida como condición previa**, antes de comparar estaciones de ría o rodeadas de tierra.")

with st.expander("Referencias"):
    st.markdown(
        "- Carrère, L., & Lyard, F. (2003). Modeling the barotropic response of the global ocean to atmospheric "
        "wind and pressure forcing — comparisons with observations. *Geophysical Research Letters*, 30(6), 1275. "
        "https://doi.org/10.1029/2002GL016473\n"
        "- CLS/CNES (2025). *DUACS Level-3 SWOT KaRIn (L3_LR_SSH) User Handbook*, Issue 2.1. AVISO.\n"
        "- Gómez-Enri, J., Arribas-Rodríguez, B., Tejedor, B., Álvarez, O., González, C. J., & Vignudelli, S. "
        "(2025). *Accuracy assessment of SWOT KaRIn sea level data* [Póster]. SWOT Science Team Meeting 2025.\n"
        "- Han, G., Klymak, J. M., Ross, T., & Chen, N. (2026). Validation of 1-day repeat SWOT measurements "
        "against tide-gauge and glider data off Canada's West Coast. *Geophysical Research Letters*, 53, "
        "e2025GL119491. https://doi.org/10.1029/2025GL119491\n"
        "- Lichtman, I. D., Bell, P. S., Gommenginger, C., Banks, C., Calafat, F. M., Brown, J., & Williams, "
        "S. D. P. (2025). Evaluating water levels from the Surface Water and Ocean Topography (SWOT) mission in a "
        "hyper-tidal coastal and estuarine environment. *Earth and Space Science*, 12, e2024EA004104. "
        "https://doi.org/10.1029/2024EA004104\n"
        "- Puertos del Estado (2024). *Conjunto de datos: REDMAR*. "
        "https://bancodatos.puertos.es/BD/informes/INT_3.pdf\n"
        "- Ray, R. D., Loomis, B. D., & Zlotnicki, V. (2021). The mean seasonal cycle in relative sea level from "
        "satellite altimetry and gravimetry. *Journal of Geodesy*, 95, 80. "
        "https://doi.org/10.1007/s00190-021-01529-1\n"
        "- Rong, Y., Bates, P., Neal, J., Bell, P., Gommenginger, C., Lichtman, I. D., et al. (2026). Evaluating "
        "SWOT in the coastal zone: Comparisons with tide gauge and airborne LiDAR in the Bristol Channel and "
        "Severn Estuary, UK. *Geophysical Research Letters*, 53, e2025GL116590. "
        "https://doi.org/10.1029/2025GL116590\n"
        "- SWOT L3 LR SSH Unsmoothed, versión 2.0.1. DOI 10.24400/527896/A01-2024.003")
