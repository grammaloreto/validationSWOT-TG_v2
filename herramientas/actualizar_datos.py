"""
Copia a `datos/` los resultados que lee el demo, desde el repositorio de validación donde se generaron, y escribe
`datos/MANIFIESTO.json` con la procedencia de cada archivo (ruta de origen, último commit que lo modificó y sha256).

Solo lee del repositorio de origen. Se detiene sin copiar nada si alguno de los archivos tiene cambios sin commitear
o no está versionado, para que cada cifra del demo corresponda a una revisión concreta. Después de ejecutarlo hay que
pasar `herramientas/comprobar_demo.py`.

Uso: python herramientas/actualizar_datos.py RUTA_DEL_REPOSITORIO_DE_VALIDACION
"""
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

DATOS = Path(__file__).resolve().parents[1] / "datos"

SERIES = "demo/tests/all_cycles/series/pass_v2.2"
ESTACIONES = {197: ["cibrao", "coruna", "ferrol", "langosteira_2", "villagarcia", "marin", "vigo"],
              154: ["coruna", "ferrol", "langosteira_2", "villagarcia", "marin", "vigo"]}
RADIOS = (6, 8, 10)

# origen (relativo a la raíz del repositorio de validación) → destino (relativo a datos/)
ARCHIVOS = {
    "demo/paper_material/tabla_maestra_val_v2.csv": "tabla_maestra_val_v2.csv",
    "demo/app/validacion_v2/datos/costa_galicia_ne10m.geojson": "costa_galicia_ne10m.geojson",
    **{f"demo/static/reference_tracks/swot_t{t}_reference.json": f"trazas/swot_t{t}_reference.json"
       for t in ESTACIONES},
    **{f"{SERIES}/{s}_t{t}_r{r}km.csv": f"series/{s}_t{t}_r{r}km.csv"
       for t, est in ESTACIONES.items() for s in est for r in RADIOS},
    **{f"{SERIES}/{n}": f"series/{n}" for n in [
        "descomposicion/descomposicion_r10km.csv",
        "descomposicion/descomposicion_correlaciones_r10km.csv",
        "descomposicion/descomposicion_robustez_r10km.csv",
        "comparacion_tracks/comparacion_t154_t197_r10km.json",
        "robustez_modo_comun/robustez_r10km.csv",
        *[f"robustez_modo_comun/robustez_r{r}km_comun6_8_10.csv" for r in RADIOS],
        "robustez_modo_comun/persistencia_mareografos_r10km.csv",
        *[f"comparacion_estaciones/comparacion_t{t}_r10km.csv" for t in ESTACIONES],
    ]},
}


def git(origen, *args):
    return subprocess.run(["git", "-C", str(origen), *args], check=True, capture_output=True,
                          text=True).stdout.strip()


def sha256(ruta):
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def main(origen):
    origen = Path(origen).resolve()
    faltan = [o for o in ARCHIVOS if not (origen / o).is_file()]
    if faltan:
        sys.exit("No existen en el origen:\n  " + "\n  ".join(faltan))
    no_limpios = git(origen, "status", "--porcelain", "--", *ARCHIVOS)
    if no_limpios:
        sys.exit("Archivos con cambios sin commitear o sin versionar en el origen:\n" + no_limpios)

    if DATOS.exists():
        shutil.rmtree(DATOS)
    entradas = []
    for o, d in ARCHIVOS.items():
        destino = DATOS / d
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(origen / o, destino)
        entradas.append({"archivo": d, "origen": o, "commit": git(origen, "log", "-1", "--format=%H", "--", o),
                         "sha256": sha256(destino)})

    manifiesto = {
        "generado_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "revision_origen": git(origen, "rev-parse", "HEAD"),
        "n_archivos": len(entradas),
        "archivos": entradas,
    }
    (DATOS / "MANIFIESTO.json").write_text(json.dumps(manifiesto, ensure_ascii=False, indent=1) + "\n")
    print(f"{len(entradas)} archivos copiados a {DATOS.name}/ (origen en {manifiesto['revision_origen'][:7]})")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
