"""Ejercicio 1 ★ — Una computadora mil veces más rápida (C1)

Código de validación de ejercicio-01.md.
Ejecutar con: python ejercicio-01.py
"""


# -------------------- Parte 1 --------------------

import math

def mayor_n(costo, presupuesto):
    # el mayor n con costo(n) <= presupuesto, por búsqueda binaria (C1, §7)
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

costos = {
    "n":       lambda n: n,
    "n log n": lambda n: n * math.log2(n),
    "n^2":     lambda n: n ** 2,
    "n^3":     lambda n: n ** 3,
    "2^n":     lambda n: 2 ** n,
}

hora = 3600 * 10**9
print(f"{'costo':>8} {'actual':>12} {'1000x':>12} {'factor':>10}")
factores = {}
for nombre, costo in costos.items():
    a, b = mayor_n(costo, hora), mayor_n(costo, 1000 * hora)
    factores[nombre] = b / a
    print(f"{nombre:>8} {a:>12.3g} {b:>12.3g} {b / a:>10.4g}")

# -------------------- Parte 2 --------------------

# Caso n^2: el factor es sqrt(1000)
assert abs(factores["n^2"] - math.sqrt(1000)) < 1e-3

# Caso n log n: iteración de punto fijo f = 1000 / (1 + log2 f / log2 n)
def factor_nlogn(n, k=1000, iteraciones=50):
    f = k
    for _ in range(iteraciones):
        f = k / (1 + math.log2(f) / math.log2(n))
    return f

n_hoy = mayor_n(costos["n log n"], hora)
f = factor_nlogn(n_hoy)
print(f"n hoy = {n_hoy:.3g}, factor por la fórmula = {f:.1f}, "
      f"factor medido = {factores['n log n']:.1f}")
assert abs(f - factores["n log n"]) < 0.5
assert 1000 / (1 + math.log2(1000) / math.log2(n_hoy)) <= f < 1000

# -------------------- Parte 3 --------------------

print(f"{'op/s':>8} {'n hoy (n log n)':>16} {'factor n log n':>15} {'factor n^2':>11}")
for V in [10**6, 10**9, 10**12, 10**15]:
    P = 3600 * V
    a = mayor_n(costos["n log n"], P)
    fl = mayor_n(costos["n log n"], 1000 * P) / a
    fc = mayor_n(costos["n^2"], 1000 * P) / mayor_n(costos["n^2"], P)
    print(f"{V:>8.0e} {a:>16.3g} {fl:>15.1f} {fc:>11.2f}")
    assert 700 < fl < 1000 and abs(fc - math.sqrt(1000)) < 0.01
