"""
Comprobaciones internas de coherencia del demo (no se muestran en la app): que lo que dibuja reproduce las n y las
r guardadas en los resultados de pass_v2.2 y en la tabla maestra v2 de `datos/`. Sale con código 1 si algo falla.

Uso: python herramientas/comprobar_demo.py
"""
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
logging.disable(logging.WARNING)  # avisos de Streamlit fuera de la app (caché sin servidor)

from nucleo import datos as D  # noqa: E402


def main():
    resultados = D.comprobaciones()
    for que, ok, detalle in resultados:
        print(f"{'OK ' if ok else 'ERR'} {que} — {detalle}")
    fallos = sum(not ok for _, ok, _ in resultados)
    print("\nTODO OK" if not fallos else f"\n{fallos} comprobaciones fallidas")
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
