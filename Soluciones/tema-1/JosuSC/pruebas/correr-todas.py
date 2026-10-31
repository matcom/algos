#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Corre las 14 baterías de pruebas y imprime un resumen.

Uso:  python3 pruebas/correr-todas.py
"""

import os
import subprocess
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))

def main():
    pruebas = sorted(f for f in os.listdir(AQUI) if f.startswith("prueba_ejercicio_"))
    print(f"Corriendo {len(pruebas)} baterías...\n")
    ok, mal = [], []
    for nombre in pruebas:
        t0 = time.time()
        r = subprocess.run([sys.executable, os.path.join(AQUI, nombre)],
                           capture_output=True, text=True, timeout=600)
        dt = time.time() - t0
        if r.returncode == 0:
            ok.append(nombre)
            print(f"  [OK]     {nombre:<28s} {dt:5.1f} s")
        else:
            mal.append(nombre)
            print(f"  [FALLA]  {nombre:<28s} {dt:5.1f} s")
            for linea in (r.stdout + r.stderr).strip().splitlines()[-4:]:
                print(f"           {linea}")
    print(f"\n{len(ok)} de {len(pruebas)} en verde."
          + ("" if not mal else "  Fallaron: " + ", ".join(mal)))
    return 0 if not mal else 1


if __name__ == "__main__":
    sys.exit(main())
