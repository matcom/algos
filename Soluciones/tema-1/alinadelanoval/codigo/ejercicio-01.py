"""Ejercicio 1 del Tema 1: una computadora mil veces más rápida.

Los bloques van en el orden de ejercicio-01.md, y cada uno imprime lo que el .md
muestra debajo de él. Ejecutarlo desde Soluciones/tema-1/alinadelanoval/:

    pip install tesserax        # para la figura
    python codigo/ejercicio-01.py
"""

# == bloque: imports (oculto)
import math
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[3] / "Lectures" / "2026"))   # donde vive figuras.py

# == bloque: biseccion
def biseccion(f, bajo, alto, pasos=200):
    # raíz de una f creciente con f(bajo) < 0 < f(alto)
    for _ in range(pasos):
        medio = (bajo + alto) / 2
        if f(medio) < 0:
            bajo = medio
        else:
            alto = medio
    return bajo

B = 3600 * 10**9                        # una hora a 10^9 operaciones por segundo
n = biseccion(lambda n: n * math.log2(n) - B, 2, B)
cota = 1000 / (1 + math.log(1000) / math.log(n))
k = biseccion(lambda k: k * (math.log(n) + math.log(k)) - 1000 * math.log(n), 1, 1000)
print(f"B = {B:.1e}, n = {n:.3e}, log2 n = {math.log2(n):.1f}")
print(f"{cota:.1f} < k = {k:.1f} < 1000")

# == bloque: mayor_n
def mayor_n(costo, presupuesto):
    # el mayor n con costo(n) <= presupuesto, por búsqueda binaria
    alto = 2
    while costo(alto) <= presupuesto:
        alto *= 2
    bajo = alto // 2
    while bajo + 1 < alto:
        medio = (bajo + alto) // 2
        if costo(medio) <= presupuesto:
            bajo = medio
        else:
            alto = medio
    return bajo

def mayor_n_fuerza_bruta(costo, presupuesto):
    n = 2
    while costo(n + 1) <= presupuesto:
        n += 1
    return n

costos = {"n^2": lambda n: n * n, "n log2 n": lambda n: n * math.log2(n)}

casos = [(c, p) for c in costos.values() for p in range(4, 20_001, 37)]
fallos = sum(mayor_n(c, p) != mayor_n_fuerza_bruta(c, p) for c, p in casos)
print(f"mayor_n contra fuerza bruta: {len(casos)} casos, {fallos} fallos\n")

for nombre, costo in costos.items():
    n0, n1 = mayor_n(costo, B), mayor_n(costo, 1000 * B)
    print(f"{nombre:>9}  {n0:>18,} -> {n1:>22,}   factor {n1 / n0:.1f}")

# == bloque: barrido
print(f"{'op/s':>6} {'n de partida':>13} {'k (n^2)':>8} {'cota inf.':>10} {'k (n log n)':>12}")
filas, peor, n_peor = [], 0.0, None
for e in range(0, 16, 3):
    p = 3600 * 10**e
    n0 = mayor_n(costos["n log2 n"], p)
    k_med = mayor_n(costos["n log2 n"], 1000 * p) / n0
    m0 = mayor_n(costos["n^2"], p)
    k2 = mayor_n(costos["n^2"], 1000 * p) / m0
    cota = 1000 / (1 + math.log(1000) / math.log(n0))
    k_ec = biseccion(lambda k: k * (math.log(n0) + math.log(k)) - 1000 * math.log(n0), 1, 1000)
    assert abs(k2 - math.sqrt(1000)) < 0.01          # sección 3
    assert cota < k_med < 1000                       # sección 4
    dif = abs(k_ec - k_med) / k_med
    assert dif < 1 / n0 + 1e-12      # la ecuación predice lo medido (+ redondeo de float)
    if dif > peor:
        peor, n_peor = dif, n0
    filas.append((n0, k_med, m0, k2))
    print(f"{'10^' + str(e):>6} {n0:>13.2e} {k2:>8.2f} {cota:>10.1f} {k_med:>12.1f}")
assert all(a[1] < b[1] for a, b in zip(filas, filas[1:]))   # k crece con n
print(f"comprobado en {len(filas)} velocidades, sin fallos;"
      f" ecuación contra medida: diferencia máxima {peor:.1e} (n = {n_peor})")

# == bloque: figura (oculto)
try:
    import figuras as F
except ImportError:
    print("sin tesserax no se regenera la figura")
else:
    figura = F.grafica_log_log(
        {"Θ(n log n)": [(n0, k) for n0, k, _, _ in filas],
         "Θ(n²)": [(m0, k2) for _, _, m0, k2 in filas]},
        "n de partida (una hora)", "k = n′/n", ident="ejercicio-01-factor")
    svg = figura[figura.index("<svg"):figura.index("</svg>") + len("</svg>")]
    vb = svg.split('viewBox="')[1].split('"')[0].split()   # fondo blanco para GitHub
    fondo = f'<rect x="{vb[0]}" y="{vb[1]}" width="{vb[2]}" height="{vb[3]}" fill="white"/>'
    (AQUI.parent / "figuras" / "ejercicio-01-factor.svg").write_text(
        svg.replace(">", ">" + fondo, 1), encoding="utf-8")
