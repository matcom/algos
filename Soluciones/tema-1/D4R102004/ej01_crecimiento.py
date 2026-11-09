"""Ejercicio 1: ¿cuánto crece el n resoluble en una hora si la máquina es k veces más rápida?
Busca el mayor n con costo(n) <= presupuesto (búsqueda binaria)"""

import math


def mayor_n(costo, presupuesto):
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
    "n log n": lambda n: n * math.log2(n),
    "n^2": lambda n: n**2,
}

HORA = 3600 * 10**9  # 10^9 operaciones por segundo durante una hora
for nombre, costo in costos.items():
    n1 = mayor_n(costo, HORA)
    n2 = mayor_n(costo, 1000 * HORA)
    print(f"{nombre:>8}: n1 = {n1:.3e}  n2 = {n2:.3e}  factor = {n2 / n1:.1f}")
