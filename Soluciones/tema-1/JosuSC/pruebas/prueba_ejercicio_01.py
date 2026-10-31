#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejercicio 1 - Casos de prueba
Una computadora mil veces más rápida: ¿cuánto crece el tamaño de entrada
que se resuelve en una hora con un algoritmo Θ(n²)? ¿Y con uno Θ(n log n)?

Qué se comprueba:
  1. Que n_max(P) = piso(sqrt(P)) cuando el costo es n², para varios P.
  2. Que el factor de crecimiento del caso n² es exactamente sqrt(1000),
     sin importar el presupuesto (la sección 3 del ejercicio).
  3. La comprobación numérica de la sección 3 con la máquina de 1e9 op/s:
     P = 3.6e12 -> n = 1 897 366 y P' = 3.6e15 -> n = 60 000 000.
  4. Que el factor r del caso n log n resuelve de verdad la ecuación
     r * (1 + log2(r)/log2(n1)) = 1000, que r < 1000 siempre y que se
     acerca a 1000 cuando n1 crece (la sección 4 del ejercicio).

Ejecutar:  python3 prueba_ejercicio_01.py
Solo usa la biblioteca estándar.
"""

import math


def n_max(costo, P):
    """Mayor n tal que costo(n) <= P, para costo no decreciente (búsqueda binaria)."""
    if costo(1) > P:
        return 0
    n, salto = 1, 1
    while costo(n + salto) <= P:        # crecer por bloques...
        n += salto
        salto *= 2
    lo, hi = n, n + salto               # ...y afinar: costo(lo) <= P < costo(hi)
    while hi - lo > 1:
        m = (lo + hi) // 2
        if costo(m) <= P:
            lo = m
        else:
            hi = m
    return lo


def c_cuad(n):
    return n * n


def c_nlogn(n):
    return n * math.log2(n) if n > 1 else 0


def factor_nlogn(n1):
    """Factor r = n2/n1 tal que n2*log2(n2) = 1000 * (n1*log2(n1)).

    Es la iteración de punto fijo del ejercicio: r <- 1000 / (1 + log2(r)/log2(n1)).
    """
    L = math.log2(n1)
    r = 1000.0
    for _ in range(500):
        r_nuevo = 1000.0 / (1.0 + math.log2(r) / L)
        if abs(r_nuevo - r) < 1e-12:
            return r_nuevo
        r = r_nuevo
    return r


def main():
    # ------------------------------------------------------------------
    # 1) Caso n²: n_max(P) = piso(sqrt(P)) y el factor es sqrt(1000)
    # ------------------------------------------------------------------
    for P in [3600, 10**6, 3_600_000_000_000, 10**15]:
        assert n_max(c_cuad, P) == math.isqrt(P), P

    for P in [3600, 10**6, 10**9, 3_600_000_000_000]:
        F = n_max(c_cuad, 1000 * P) / n_max(c_cuad, P)
        # el piso de los sqrt mete un ruido relativo ~1/sqrt(P): no se puede
        # pedir igualdad exacta con P chico, pero si acercarse
        assert abs(F - math.sqrt(1000)) < 0.02, (P, F)

    # ------------------------------------------------------------------
    # 2) La comprobación de la sección 3: máquina de 1e9 operaciones/segundo
    # ------------------------------------------------------------------
    P = 10**9 * 3600                     # presupuesto de una hora: 3.6e12
    n_lenta = n_max(c_cuad, P)
    n_rapida = n_max(c_cuad, 1000 * P)
    assert (n_lenta, n_rapida) == (1_897_366, 60_000_000), (n_lenta, n_rapida)
    assert abs(n_rapida / n_lenta - math.sqrt(1000)) < 1e-3   # el piso del sqrt mete ruido ~1e-5

    # ------------------------------------------------------------------
    # 3) Caso n log n: el factor r y su dependencia con n1
    # ------------------------------------------------------------------
    for n1 in (10**4, 10**6, 10**9, 10**12):
        r = factor_nlogn(n1)
        n2 = r * n1
        # la ecuación que define a r se cumple de verdad:
        assert abs(n2 * math.log2(n2) - 1000 * n1 * math.log2(n1)) < 1e-3 * n1 * math.log2(n1)
        assert r < 1000                   # siempre un poco menos de 1000

    r6 = factor_nlogn(10**6)
    r9 = factor_nlogn(10**9)
    r12 = factor_nlogn(10**12)
    assert 670 < r6 < 690                 # el ejercicio: "alrededor de 680-690"
    assert r9 > r6 and r12 > r9           # crece con n1...
    assert r12 < 1000                     # ...pero sin llegar a 1000

    print("ejercicio 1: todo correcto")
    print(f"  costo n^2     : factor = sqrt(1000) = {math.sqrt(1000):.4f} (igual para todo P)")
    print(f"  costo n log n : factor = {r6:.1f} con n1 = 1e6")
    print(f"                  factor = {r9:.1f} con n1 = 1e9")
    print(f"                  factor = {r12:.1f} con n1 = 1e12  (tiende a 1000)")
    print(f"  máquina 1e9 op/s, n^2: n = {n_lenta:,} -> {n_rapida:,} en una hora")


if __name__ == "__main__":
    main()
