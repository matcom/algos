#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejercicio 6 - Casos de prueba
Búsqueda en una matriz con filas y columnas ordenadas (la escalera).

Qué se comprueba:
  1. Exhaustivo: TODAS las matrices monótonas n x n (n <= 3) y todos los x:
     correctitud, cota de 2n-1 comparaciones, y que el máximo observado
     es exactamente 2n-1 (la cota se alcanza).
  2. La familia del adversario S, S_0, ..., S_{n-1} para n = 2..40:
     estrictamente crecientes, x solo en D_k, y la escalera hace 2n-1
     comparaciones sobre S.
  3. El mutante con guarda "j > 0": falla EXACTAMENTE cuando x está
     presente solo en la columna 0 (la caracterización de la sección 4),
     en 10000 matrices aleatorias.
  4. Aleatorio grande contra oráculo.

Ejecutar:  python3 prueba_ejercicio_06.py
Solo usa la biblioteca estándar.
"""

import random


def buscar(A, x):
    """Escalera desde la esquina superior derecha. Devuelve (pos | None, comparaciones)."""
    n = len(A)
    i, j, c = 0, n - 1, 0
    while i < n and j >= 0:
        c += 1
        if A[i][j] == x:
            return (i, j), c
        elif A[i][j] < x:
            i += 1
        else:
            j -= 1
    return None, c


def buscar_mutante(A, x):
    """Error plantado: j > 0 en lugar de j >= 0 (nunca mira la columna 0)."""
    n = len(A)
    i, j, c = 0, n - 1, 0
    while i < n and j > 0:
        c += 1
        if A[i][j] == x:
            return (i, j), c
        elif A[i][j] < x:
            i += 1
        else:
            j -= 1
    return None, c


def buscar_rect(A, x):
    """La variante m x n que menciona el ejercicio: j empieza en len(A[0])-1."""
    m, ncol = len(A), len(A[0])
    i, j, c = 0, ncol - 1, 0
    while i < m and j >= 0:
        c += 1
        if A[i][j] == x:
            return (i, j), c
        elif A[i][j] < x:
            i += 1
        else:
            j -= 1
    return None, c


def monotonas(n, V):
    """Todas las matrices n x n con entradas en 0..V, filas y columnas no decrecientes."""
    celdas = [(r, c) for r in range(n) for c in range(n)]

    def rec(k, M):
        if k == len(celdas):
            yield tuple(tuple(f) for f in M)
            return
        r, c = celdas[k]
        lo = max(M[r][c - 1] if c else 0, M[r - 1][c] if r else 0)
        for v in range(lo, V + 1):
            M[r][c] = v
            yield from rec(k + 1, M)
        M[r][c] = 0

    yield from rec(0, [[0] * n for _ in range(n)])


def S(n):
    return [[2 * (r + c) for c in range(n)] for r in range(n)]


def S_k(n, k):
    M = S(n)
    M[k][n - 1 - k] = 2 * n - 3
    return M


def estricta(M):
    n = len(M)
    return (all(M[r][c] < M[r][c + 1] for r in range(n) for c in range(n - 1)) and
            all(M[r][c] < M[r + 1][c] for r in range(n - 1) for c in range(n)))


def main():
    # ------------------------------------------------------------------
    # 1) Exhaustivo: todas las matrices monótonas chicas, todos los x
    # ------------------------------------------------------------------
    instancias = 0
    for n, V in [(1, 3), (2, 4), (3, 4)]:
        maxc = 0
        for M in monotonas(n, V):
            presentes = {v for f in M for v in f}
            for x in range(-1, V + 2):
                pos, c = buscar(M, x)
                assert (pos is not None) == (x in presentes), (M, x)
                if pos is not None:
                    assert M[pos[0]][pos[1]] == x
                assert c <= 2 * n - 1, (M, x, c)
                maxc = max(maxc, c)
                instancias += 1
        assert maxc == 2 * n - 1            # la cota se alcanza de verdad

    # ------------------------------------------------------------------
    # 2) La familia del adversario
    # ------------------------------------------------------------------
    for n in range(2, 41):
        x = 2 * n - 3
        assert estricta(S(n)) and all(v != x for f in S(n) for v in f)
        assert buscar(S(n), x) == (None, 2 * n - 1)          # la escalera llega al máximo
        for k in range(n):
            M = S_k(n, k)
            assert estricta(M)
            assert [(r, c) for r in range(n) for c in range(n) if M[r][c] == x] == [(k, n - 1 - k)]
            assert all(M[r][c] == S(n)[r][c]
                       for r in range(n) for c in range(n) if r + c != n - 1)
            pos, _ = buscar(M, x)
            assert pos == (k, n - 1 - k)

    # ------------------------------------------------------------------
    # 3) El mutante: caracterización exacta del fallo
    # ------------------------------------------------------------------
    random.seed(2026)
    n, ensayos, fallos = 6, 10000, 0
    for _ in range(ensayos):
        B = [[0] * n for _ in range(n)]
        for r in range(n):
            for c in range(n):
                lo = max(B[r][c - 1] if c else 0, B[r - 1][c] if r else 0)
                B[r][c] = lo + random.randint(0, 3)
        if random.random() < 0.5:
            x = random.choice([v for f in B for v in f])
        else:
            x = random.randint(-1, B[-1][-1] + 1)
        esta = any(x in f for f in B)
        fallo = (buscar_mutante(B, x)[0] is not None) != esta
        # el fallo ocurre exactamente cuando x está solo en la columna 0
        solo_col0 = esta and all(B[r][c] != x for r in range(n) for c in range(1, n))
        assert fallo == solo_col0, (B, x)
        fallos += fallo
    assert 0.02 < fallos / ensayos < 0.12

    # ------------------------------------------------------------------
    # 4) Aleatorio grande contra oráculo
    # ------------------------------------------------------------------
    random.seed(7)
    casos = 0
    for _ in range(5000):
        m = random.randint(1, 12)
        ncol = random.randint(1, 12)
        B = [[0] * ncol for _ in range(m)]
        for r in range(m):
            for c in range(ncol):
                lo = max(B[r][c - 1] if c else 0, B[r - 1][c] if r else 0)
                B[r][c] = lo + random.randint(0, 2)
        x = random.randint(-1, B[-1][-1] + 1)
        pos, c = buscar_rect(B, x)
        assert (pos is not None) == any(x in f for f in B)
        if pos is not None:
            assert B[pos[0]][pos[1]] == x
        assert c <= m + ncol - 1            # rectangular: m + n - 1
        casos += 1

    print("ejercicio 6: todo correcto")
    print(f"  exhaustivo: {instancias} instancias (todas las monótonas con n <= 3), max = 2n-1")
    print("  familia del adversario S, S_0..S_{n-1} bien formada para n = 2..40")
    print("  escalera sobre S: exactamente 2n-1 comparaciones (la cota se alcanza)")
    print(f"  mutante j>0: {fallos}/{ensayos} fallos, exactamente cuando x solo está en la columna 0")
    print(f"  aleatorio rectangular: {casos} casos, cota m+n-1")


if __name__ == "__main__":
    main()
