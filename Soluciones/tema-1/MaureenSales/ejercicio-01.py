"""Ejercicio 1 — Una computadora mil veces más rápida

Código extraído de ejercicio-01.md, en el mismo orden en que aparece allí.
Ejecutar con:  python ejercicio-01.py
La salida esperada es la de la sección "Salida" de ejercicio-01.md.
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")   # para que la consola de Windows imprima δ, ≤, ⌈⌉...

# ----------------------------------------------------------------------
# Del md, sección: 7. Casos de prueba
# ----------------------------------------------------------------------

import math

def mayor_n(f, presupuesto):
    """Mayor n >= 1 con f(n) <= presupuesto (f creciente). Búsqueda binaria."""
    lo, hi = 1, 1
    while f(hi) <= presupuesto:      # buscar una cota superior
        hi *= 2
    # invariante: f(lo) <= presupuesto < f(hi)
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if f(mid) <= presupuesto:
            lo = mid
        else:
            hi = mid
    return lo

B = 3600 * 10**9                     # una hora a 10^9 op/s
funciones = {
    "n":        lambda n: n,
    "n log2 n": lambda n: n * math.log2(n) if n > 1 else 1,
    "n^2":      lambda n: n * n,
    "n^3":      lambda n: n ** 3,
    "2^n":      lambda n: 2 ** n,
}

print(f"{'f(n)':10} {'n0':>18} {'n1':>22} {'n1/n0':>9} {'n1-n0':>22}")
res = {}
for nombre, f in funciones.items():
    n0, n1 = mayor_n(f, B), mayor_n(f, 1000 * B)
    res[nombre] = (n0, n1)
    print(f"{nombre:10} {n0:18,} {n1:22,} {n1/n0:9.2f} {n1-n0:22,}")

# --- n^2: factor sqrt(1000), independiente de n0 ---
n0, n1 = res["n^2"]
assert abs(n1 / n0 - math.sqrt(1000)) < 0.01

# --- n log n: entre la cota inferior y 1000, y la estimación de la sección 3 ---
n0, n1 = res["n log2 n"]
inferior = 1000 / (1 + math.log2(1000) / math.log2(n0))
estimacion = 1000 * math.log2(n0) / (math.log2(n0) + math.log2(inferior))
print(f"\nn log n: cota inferior {inferior:.1f} <= factor {n1/n0:.1f} <= 1000;"
      f" estimación iterada {estimacion:.1f}")
assert inferior <= n1 / n0 <= 1000
assert abs(estimacion - n1 / n0) < 1

# --- el factor de n log n depende de n0 y tiende a 1000 ---
for horas in [1e-6, 1, 1e6]:
    a = mayor_n(funciones["n log2 n"], B * horas)
    b = mayor_n(funciones["n log2 n"], 1000 * B * horas)
    print(f"presupuesto {B * horas:9.1e}: n0 = {a:.3g}, factor = {b / a:.1f}")

# --- la constante oculta: no cambia el factor de n^2; en n log n solo entra vía n0 ---
for c in (1, 7, 1000):
    cuad = lambda n: c * n * n
    nlog = lambda n: c * n * math.log2(n) if n > 1 else c
    a2, b2 = mayor_n(cuad, B), mayor_n(cuad, 1000 * B)
    a, b = mayor_n(nlog, B), mayor_n(nlog, 1000 * B)
    cota_c = 1000 / (1 + math.log2(1000) / math.log2(a))   # la cota inferior con ESE n0
    print(f"c = {c:5}:  factor n^2 = {b2/a2:.2f}   n0 = {a:.3g}, factor n log n = {b/a:.2f}"
          f" (cota inferior {cota_c:.1f})")
    assert abs(b2 / a2 - math.sqrt(1000)) < 0.01
    assert cota_c <= b / a <= 1000

# --- datos 1000 veces más grandes en la máquina nueva (sección 5) ---
n0 = res["n log2 n"][0]
print(f"\nn log n con datos x1000 y máquina x1000: tarda "
      f"{funciones['n log2 n'](1000 * n0) / (1000 * funciones['n log2 n'](n0)):.2f} veces lo de hoy")

# --- primalidad por división medida en bits: 2^(b/2) operaciones (sección 6) ---
b0 = mayor_n(lambda b: 2 ** (b / 2), B)
b1 = mayor_n(lambda b: 2 ** (b / 2), 1000 * B)
print(f"primalidad por división: {b0} bits -> {b1} bits (+{b1 - b0})")
assert b1 - b0 in (19, 20)
print("todas las pruebas pasaron")
