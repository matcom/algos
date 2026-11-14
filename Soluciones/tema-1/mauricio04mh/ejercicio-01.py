"""Ejercicio 1. Una computadora mil veces más rápida.

Comprueba numéricamente los factores de crecimiento del tamaño de entrada
para algoritmos de costo c*n^2 y c*n*log2(n).
"""
import math


def mayor_n(costo, presupuesto):
    """Mayor n con costo(n) <= presupuesto (búsqueda binaria)."""
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


def factor_nlogn(n0, veces=1000):
    """Resuelve k * (1 + log2(k) / log2(n0)) = veces por bisección."""
    f = lambda k: k * (1 + math.log2(k) / math.log2(n0)) - veces
    lo, hi = 1.0, float(veces)
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    return lo


if __name__ == "__main__":
    print("Algoritmo c*n^2 (c = 1)")
    print(f"{'n0':>10} {'n1 directo':>14} {'n1/n0':>8} {'sqrt(1000)':>11}")
    for n0 in [10**3, 10**6, 10**9]:
        T = n0 ** 2
        n1 = mayor_n(lambda n: n ** 2, 1000 * T)
        print(f"{n0:>10.0e} {n1:>14,} {n1 / n0:>8.2f} {math.sqrt(1000):>11.2f}")

    print("\nAlgoritmo c*n*log2(n) (c = 1)")
    print(f"{'n0':>8} {'k directo':>10} {'k (ecuación)':>13} {'cota inf.':>10}")
    for n0 in [10**3, 10**6, 10**9, 10**12]:
        T = n0 * math.log2(n0)
        n1 = mayor_n(lambda n: n * math.log2(n), 1000 * T)
        k = factor_nlogn(n0)
        cota = 1000 / (1 + math.log2(1000) / math.log2(n0))
        print(f"{n0:>8.0e} {n1 / n0:>10.1f} {k:>13.1f} {cota:>10.1f}")
