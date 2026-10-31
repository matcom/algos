#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejercicio 7 - Casos de prueba
Mediana de dos arreglos ordenados (eliminar ventanas).

Qué se comprueba:
  1. Exhaustivo con duplicados (n <= 6): mediana(A,B) == sorted(A+B)[n-1]
     y comparaciones <= ceil(log2 n) + 1.
  2. Sobre TODOS los entrelazados (n <= 10): la mediana es n-1, el peor caso
     medido es EXACTAMENTE ceil(log2 n)+1 (la cota de información), y el
     invariante I(a,b,s) vigilado en cada vuelta (n <= 8).
  3. Aleatorio con n hasta 400.
  4. El mutante (s//2 en la rama else): cero fallos cuando n es potencia de
     2, fallos masivos cuando no lo es. Es la trampa de la sección 7.3.

Ejecutar:  python3 prueba_ejercicio_07.py
Solo usa la biblioteca estándar.
"""

import itertools
import random


def mediana(A, B):
    n = len(A)
    a = b = 0
    s = n
    while s > 1:
        k = (s + 1) // 2 - 1                # ceil(s/2) - 1
        l = s // 2 - 1                      # floor(s/2) - 1   (k + l = s - 2)
        if A[a + k] <= B[b + l]:
            a += k + 1
            s = s // 2
        else:
            b += l + 1
            s = (s + 1) // 2
    return min(A[a], B[b])


def mediana_vigilada(A, B):
    """Igual que mediana, pero comprueba I(a,b,s) en cada vuelta."""
    n = len(A)
    objetivo = sorted(A + B)[n - 1]
    a = b = 0
    s = n
    while True:
        assert sorted(A[a:a + s] + B[b:b + s])[s - 1] == objetivo, ("I roto", a, b, s)
        if s == 1:
            return min(A[a], B[b])
        k, l = (s + 1) // 2 - 1, s // 2 - 1
        if A[a + k] <= B[b + l]:
            a += k + 1
            s = s // 2
        else:
            b += l + 1
            s = (s + 1) // 2


def mediana_mutante(A, B):
    """Error plantado: en la rama else se usa s//2 en lugar de ceil(s/2)."""
    n = len(A)
    a = b = 0
    s = n
    while s > 1:
        k, l = (s + 1) // 2 - 1, s // 2 - 1
        if A[a + k] <= B[b + l]:
            a += k + 1
            s = s // 2
        else:
            b += l + 1
            s = s // 2                      # <-- error
    return min(A[a], B[b])


def cuenta(A, B):
    """Comparaciones que hace mediana (copia instrumentada)."""
    n = len(A)
    a = b = 0
    s = n
    c = 0
    while s > 1:
        k, l = (s + 1) // 2 - 1, s // 2 - 1
        c += 1
        if A[a + k] <= B[b + l]:
            a += k + 1
            s = s // 2
        else:
            b += l + 1
            s = (s + 1) // 2
    return c + 1


def ceil_log2(x):
    return (x - 1).bit_length()


def desde_patron(n, posA):
    """Entrada con valores 0..2n-1 donde A ocupa las posiciones posA de la mezcla."""
    posA = set(posA)
    A, B = [], []
    for p in range(2 * n):
        (A if p in posA else B).append(p)
    return A, B


def main():
    # ------------------------------------------------------------------
    # 1) Exhaustivo con duplicados
    # ------------------------------------------------------------------
    total = 0
    for n, V in [(1, 4), (2, 4), (3, 4), (4, 4), (5, 3), (6, 2)]:
        for A in itertools.combinations_with_replacement(range(V + 1), n):
            for B in itertools.combinations_with_replacement(range(V + 1), n):
                assert mediana(list(A), list(B)) == sorted(A + B)[n - 1]
                assert cuenta(list(A), list(B)) <= ceil_log2(n) + 1
                total += 1

    # ------------------------------------------------------------------
    # 2) Todos los entrelazados, n <= 10: peor caso exacto + invariante
    # ------------------------------------------------------------------
    for n in range(1, 11):
        mx, cnt = 0, 0
        for posA in itertools.combinations(range(2 * n), n):
            A, B = desde_patron(n, posA)
            assert mediana(A, B) == n - 1
            if n <= 8:
                assert mediana_vigilada(A, B) == n - 1
            mx, cnt = max(mx, cuenta(A, B)), cnt + 1
        assert mx == ceil_log2(n) + 1, (n, mx)     # coincide con la cota de información

    # el ejemplo del ejercicio: 3 comparaciones = ceil(log2 4)+1
    assert mediana([2, 4, 6, 8], [1, 3, 5, 7]) == 4
    assert cuenta([2, 4, 6, 8], [1, 3, 5, 7]) == 3

    # ------------------------------------------------------------------
    # 3) Aleatorio grande
    # ------------------------------------------------------------------
    random.seed(7)
    for _ in range(3000):
        n = random.randint(1, 400)
        A = sorted(random.randint(0, 500) for _ in range(n))
        B = sorted(random.randint(0, 500) for _ in range(n))
        assert mediana(A, B) == sorted(A + B)[n - 1]
        assert cuenta(A, B) <= ceil_log2(n) + 1

    # ------------------------------------------------------------------
    # 4) El mutante: invisible con n potencia de 2, visible cuando no
    # ------------------------------------------------------------------
    for n in (1, 2, 4, 8):
        f = sum(1 for posA in itertools.combinations(range(2 * n), n)
                if mediana_mutante(*desde_patron(n, posA)) != n - 1)
        assert f == 0, (n, f)                 # con n = 2^k el error no cambia nada
    for n in (3, 5, 6, 7):
        f = sum(1 for posA in itertools.combinations(range(2 * n), n)
                if mediana_mutante(*desde_patron(n, posA)) != n - 1)
        assert f > 0, (n, f)                  # con n != 2^k sí falla

    random.seed(2026)
    for n, esperado_alto in [(8, False), (16, False), (7, True), (9, True)]:
        ens, f = 4000, 0
        for _ in range(ens):
            A = sorted(random.randint(0, 999) for _ in range(n))
            B = sorted(random.randint(0, 999) for _ in range(n))
            f += mediana_mutante(A, B) != sorted(A + B)[n - 1]
        assert (f / ens > 0.5) == esperado_alto, (n, f)

    print("ejercicio 7: todo correcto")
    print(f"  exhaustivo con duplicados: {total} pares, dentro de la cota siempre")
    print("  todos los entrelazados (n <= 10): peor caso medido = ceil(log2 n)+1 exacto")
    print("  invariante I(a,b,s) vigilado en cada vuelta (n <= 8): nunca se rompe")
    print("  mutante s//2: 0 fallos con n = 1,2,4,8; masivo con n = 3,5,6,7,9")


if __name__ == "__main__":
    main()
