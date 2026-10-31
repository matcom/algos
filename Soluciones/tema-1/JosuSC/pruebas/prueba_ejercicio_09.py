#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejercicio 9 - Casos de prueba
La mezcla "optimizada" que ahorra una comparación (y por eso está mal).

Qué se comprueba:
  1. Sobre TODOS los entrelazados de valores distintos (n <= 8):
       - la estándar hace 2n-1 en el peor caso y es siempre correcta;
       - la "optimizada" hace 2n-2 en el peor caso;
       - falla en exactamente C(2n-1, n) entradas (la mitad);
       - correcta si y solo si a_n >= b_n (el teorema de la sección 4.3).
  2. Con duplicados (3141 pares chicos): la caracterización sigue valiendo.
  3. El adversario de la sección 3: sobre I la "optimizada" se salta
     exactamente los dos pares adyacentes {b_{n-1}, a_n} y {a_n, b_n},
     y la entrada gemela I' produce la MISMA traza (pero correcta).
  4. Los ejemplos concretos n = 3 y n = 4, y el aleatorio (~48% de fallos).

Ejecutar:  python3 prueba_ejercicio_09.py
Solo usa la biblioteca estándar.
"""

import itertools
import random
from math import comb


def mezcla(A, B):
    """Mezcla estándar. Devuelve (salida como celdas, comparaciones hechas)."""
    n = len(A)
    i = j = 0
    out, cmps = [], []
    while i < n and j < n:
        cmps.append((("A", i), ("B", j)))
        if A[i] <= B[j]:
            out.append(("A", i))
            i += 1
        else:
            out.append(("B", j))
            j += 1
    out += [("A", k) for k in range(i, n)] + [("B", k) for k in range(j, n)]
    return out, cmps


def mezcla_opt(A, B):
    """La 'optimizada': deja de comparar cuando a A le queda un elemento."""
    n = len(A)
    i = j = 0
    out, cmps = [], []
    while i < n - 1 and j < n:
        cmps.append((("A", i), ("B", j)))
        if A[i] <= B[j]:
            out.append(("A", i))
            i += 1
        else:
            out.append(("B", j))
            j += 1
    if j == n:
        out += [("A", k) for k in range(i, n)]
    else:
        out += [("B", k) for k in range(j, n)] + [("A", n - 1)]
    return out, cmps


def valores(A, B, out):
    return [A[k] if t == "A" else B[k] for t, k in out]


def desde_patron(n, posA):
    """Entrada con valores 0..2n-1 donde A ocupa las posiciones posA de la mezcla."""
    posA = set(posA)
    A, B = [], []
    for p in range(2 * n):
        (A if p in posA else B).append(p)
    return A, B


def main():
    # ------------------------------------------------------------------
    # 1) Todos los entrelazados, n = 1..8
    # ------------------------------------------------------------------
    for n in range(1, 9):
        mx_s = mx_o = fallos = tot = 0
        for posA in itertools.combinations(range(2 * n), n):
            A, B = desde_patron(n, posA)
            tot += 1
            os_, cs = mezcla(A, B)
            oo, co = mezcla_opt(A, B)
            assert valores(A, B, os_) == sorted(A + B)          # la estándar nunca falla
            mx_s, mx_o = max(mx_s, len(cs)), max(mx_o, len(co))
            correcta = valores(A, B, oo) == sorted(A + B)
            assert correcta == (A[-1] >= B[-1]), (A, B)         # el teorema de 4.3
            fallos += not correcta
        assert mx_s == 2 * n - 1 and mx_o == 2 * n - 2, (n, mx_s, mx_o)
        assert fallos == comb(2 * n - 1, n), (n, fallos)        # exactamente la mitad

    # ------------------------------------------------------------------
    # 2) Con duplicados: la caracterización sigue valiendo
    # ------------------------------------------------------------------
    cnt = 0
    for n, V in [(1, 4), (2, 4), (3, 4), (4, 3), (5, 2)]:
        for A in itertools.combinations_with_replacement(range(V + 1), n):
            for B in itertools.combinations_with_replacement(range(V + 1), n):
                A_, B_ = list(A), list(B)
                oo, co = mezcla_opt(A_, B_)
                assert (valores(A_, B_, oo) == sorted(A + B)) == (A[-1] >= B[-1])
                assert len(co) <= 2 * n - 2
                cnt += 1

    # ------------------------------------------------------------------
    # 3) El adversario: los dos pares que se salta, y la gemela I'
    # ------------------------------------------------------------------
    for n in range(2, 9):
        A = [2 * k + 1 for k in range(n)]                # I: a1 < b1 < ... < an < bn
        B = [2 * k + 2 for k in range(n)]
        orden = []
        for k in range(n):
            orden += [("A", k), ("B", k)]
        pares = {frozenset((orden[t], orden[t + 1])) for t in range(2 * n - 1)}
        _, cs = mezcla(A, B)
        assert {frozenset(c) for c in cs} == pares and len(cs) == 2 * n - 1
        oo, co = mezcla_opt(A, B)
        faltan = pares - {frozenset(c) for c in co}
        assert len(co) == 2 * n - 3
        assert faltan == {frozenset((("B", n - 2), ("A", n - 1))),
                          frozenset((("A", n - 1), ("B", n - 1)))}
        # la gemela: mismos valores salvo el par intercambiado
        A2 = A[:-1] + [B[-1]]
        B2 = B[:-1] + [A[-1]]
        oo2, co2 = mezcla_opt(A2, B2)
        assert co2 == co and oo2 == oo                     # misma traza...
        assert valores(A2, B2, oo2) == sorted(A2 + B2)     # ...correcta en I'
        assert valores(A, B, oo) != sorted(A + B)          # ...incorrecta en I

    # los ejemplos impresos del ejercicio
    oo, co = mezcla_opt([1, 3, 5], [2, 4, 6])
    assert valores([1, 3, 5], [2, 4, 6], oo) == [1, 2, 3, 4, 6, 5] and len(co) == 3
    for nombre, A, B, salida in [("I  ", [1, 3, 5, 7], [2, 4, 6, 8], [1, 2, 3, 4, 5, 6, 8, 7]),
                                 ("I' ", [1, 3, 5, 8], [2, 4, 6, 7], [1, 2, 3, 4, 5, 6, 7, 8]),
                                 ("I''", [1, 3, 5, 6], [2, 4, 7, 8], [1, 2, 3, 4, 5, 7, 8, 6])]:
        oo, co = mezcla_opt(A, B)
        assert valores(A, B, oo) == salida and len(co) == 5, nombre

    # la entrada donde la "optimizada" alcanza 2n-2 y es correcta
    for n in (2, 3, 4, 5):
        B = [2 * k + 1 for k in range(n - 1)] + [2 * n - 1]
        A = [2 * k + 2 for k in range(n - 1)] + [2 * n]
        oo, co = mezcla_opt(A, B)
        assert len(co) == 2 * n - 2 and valores(A, B, oo) == sorted(A + B)

    # ------------------------------------------------------------------
    # 4) Aleatorio: falla cerca de la mitad de las veces
    # ------------------------------------------------------------------
    random.seed(2026)
    n, ens, f = 8, 10000, 0
    for _ in range(ens):
        A = sorted(random.randint(0, 99) for _ in range(n))
        B = sorted(random.randint(0, 99) for _ in range(n))
        oo, _ = mezcla_opt(A, B)
        f += valores(A, B, oo) != sorted(A + B)
    assert 0.35 < f / ens < 0.60

    print("ejercicio 9: todo correcto")
    print("  todos los entrelazados (n <= 8): estándar 2n-1, 'optimizada' 2n-2,")
    print(f"  fallos = C(2n-1, n) exactos; correcta <=> a_n >= b_n en los {cnt} pares con duplicados")
    print("  adversario: sobre I se salta exactamente {b_{n-1},a_n} y {a_n,b_n}; I' da la misma traza")
    print("  ejemplos n=3 y n=4 reproducidos; aleatorio: "
          f"{f}/{ens} fallos ({100 * f / ens:.1f}%)")


if __name__ == "__main__":
    main()
