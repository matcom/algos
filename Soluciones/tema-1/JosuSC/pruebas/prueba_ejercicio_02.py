#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejercicio 2 - Casos de prueba
Búsqueda binaria: invariante, potencial y cota de información.

Qué se comprueba:
  1. El contrato (posición si x está, hueco si no), exhaustivo en chico
     (con y sin duplicados) y en aleatorio grande.
  2. Que el peor caso medido, contando comparaciones una por una, es
     EXACTAMENTE ceil(log2(n+1)) = piso(log2 n) + 1 para n = 1..60,
     sobre todos los presentes y todos los huecos.
  3. La identidad del teorema para n = 1..10^6.
  4. El ejemplo delicado de n = 8 (n+1 = 9 no es potencia de 2): el hueco
     entre A[0] y A[1] cuesta 4 comparaciones y recorre A[4],A[2],A[1],A[0].

Ejecutar:  python3 prueba_ejercicio_02.py
Solo usa la biblioteca estándar.
"""

import itertools
import math
import random


def busqueda_binaria(A, x):
    lo, hi = 0, len(A)
    while lo < hi:
        m = (lo + hi) // 2
        if A[m] == x:
            return ("está", m)
        elif A[m] < x:
            lo = m + 1
        else:
            hi = m
    return ("hueco", lo)


def busqueda_binaria_cuenta(A, x):
    """Copia instrumentada: devuelve (respuesta, comparaciones, camino de índices m)."""
    lo, hi, c, camino = 0, len(A), 0, []
    while lo < hi:
        m = (lo + hi) // 2
        c += 1
        camino.append(m)
        if A[m] == x:
            return ("está", m), c, camino
        elif A[m] < x:
            lo = m + 1
        else:
            hi = m
    return ("hueco", lo), c, camino


def techo_log2(x):
    return (x - 1).bit_length()          # ceil(log2 x) para x >= 1


def piso_log2(x):
    return x.bit_length() - 1


def revisa_contrato(A, x, res, c):
    """El contrato de la sección 1, más la cota de comparaciones."""
    n = len(A)
    if x in A:
        assert res[0] == "está" and A[res[1]] == x, (A, x, res)
    else:
        assert res[0] == "hueco"
        h = res[1]
        izq = A[h - 1] if h > 0 else -math.inf
        der = A[h] if h < n else math.inf
        assert izq < x < der, (A, x, res)      # A[h-1] < x < A[h]: el hueco exacto
    assert c <= techo_log2(n + 1), (A, x, c)


def main():
    # ------------------------------------------------------------------
    # 1) Exhaustivo chico, con duplicados incluidos
    # ------------------------------------------------------------------
    total = 0
    for n, V in [(1, 3), (2, 4), (3, 3), (4, 3), (5, 2)]:
        for A in itertools.combinations_with_replacement(range(V + 1), n):
            A = list(A)
            for x in range(-1, V + 2):
                res, c, _ = busqueda_binaria_cuenta(A, x)
                revisa_contrato(A, x, res, c)
                total += 1

    # ------------------------------------------------------------------
    # 2) Peor caso exacto para n = 1..60 (todos los x, presentes y huecos)
    # ------------------------------------------------------------------
    for n in range(1, 61):
        A = list(range(1, n + 1))
        peor = 0
        for x in range(0, n + 2):        # cubre los n presentes y los n+1 huecos
            _, c, _ = busqueda_binaria_cuenta(A, x)
            peor = max(peor, c)
        assert peor == techo_log2(n + 1), (n, peor, techo_log2(n + 1))
        assert peor == piso_log2(n) + 1, (n, peor)      # la identidad del teorema

    # ------------------------------------------------------------------
    # 3) La identidad ceil(log2(n+1)) = piso(log2 n) + 1, n = 1..10^6
    # ------------------------------------------------------------------
    for n in range(1, 10**6 + 1):
        assert techo_log2(n + 1) == piso_log2(n) + 1
        if 2**piso_log2(n) != n:         # cuando n+1 no es potencia de 2...
            pass                         # ...el techo y el piso "se ven distintos"

    # ------------------------------------------------------------------
    # 4) El ejemplo donde el techo se nota: n = 8 (9 huecos, 4 comparaciones)
    # ------------------------------------------------------------------
    A = [2, 4, 6, 8, 10, 12, 14, 16]
    x = 3                                # hueco 1: A[0] = 2 < 3 < 4 = A[1]
    (res, h), c, camino = busqueda_binaria_cuenta(A, x)
    assert (res, h) == ("hueco", 1)
    assert c == 4 and camino == [4, 2, 1, 0]
    assert c == techo_log2(9)            # 9 huecos: un árbol binario de altura 3 tiene 8 hojas y no alcanza

    # y el arreglo donde sí está, en el peor lugar posible, no cuesta más:
    (_, m), c2, _ = busqueda_binaria_cuenta(A, 16)
    assert m == 7 and c2 <= 4

    # ------------------------------------------------------------------
    # 5) Aleatorio grande, con duplicados
    # ------------------------------------------------------------------
    random.seed(7)
    casos = 0
    for _ in range(20000):
        n = random.randint(0, 40)
        A = sorted(random.randint(0, 30) for _ in range(n))
        x = random.randint(-1, 31)
        res, c, _ = busqueda_binaria_cuenta(A, x)
        revisa_contrato(A, x, res, c)
        casos += 1

    print("ejercicio 2: todo correcto")
    print(f"  contrato (posición/hueco): {total} casos exhaustivos + {casos} aleatorios")
    print("  peor caso medido = ceil(log2(n+1)) = piso(log2 n)+1 para n = 1..60")
    print("  identidad del teorema verificada para n = 1..10^6")
    print("  n = 8, x = 3 (hueco 1): 4 comparaciones, camino A[4],A[2],A[1],A[0]")


if __name__ == "__main__":
    main()
