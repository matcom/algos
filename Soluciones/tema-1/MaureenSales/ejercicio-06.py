"""Ejercicio 6 — Buscar en una matriz con filas y columnas ordenadas

Código extraído de ejercicio-06.md, en el mismo orden en que aparece allí.
Ejecutar con:  python ejercicio-06.py
La salida esperada es la de la sección "Salida" de ejercicio-06.md.
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")   # para que la consola de Windows imprima δ, ≤, ⌈⌉...

# ----------------------------------------------------------------------
# Del md, sección: 2. Algoritmo: búsqueda en escalera
# ----------------------------------------------------------------------

def escalera(A, x, contador=None):
    """Devuelve (i, j) con A[i][j] == x, o None. A es n x m con filas y columnas crecientes."""
    n = len(A)
    if n == 0: return None
    m = len(A[0])
    i, j = 0, m - 1                   # esquina superior derecha
    while i < n and j >= 0:
        if contador is not None: contador[0] += 1
        v = A[i][j]
        if v == x:
            return (i, j)
        elif v > x:
            j -= 1                    # toda la columna j desde la fila i hacia abajo es >= v > x
        else:
            i += 1                    # toda la fila i desde la columna j hacia la izquierda es <= v < x
    return None


# ----------------------------------------------------------------------
# Del md, sección: 5. Casos de prueba
# ----------------------------------------------------------------------

import random

def matriz_ordenada(n, m, max_salto=3):
    """Matriz n x m con filas y columnas crecientes (no estrictas)."""
    A = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            base = max(A[i-1][j] if i else 0, A[i][j-1] if j else 0)
            A[i][j] = base + random.randint(0, max_salto)
    return A

def bruta(A, x):
    return any(x in fila for fila in A)

def escalera_vigilada(A, x):
    n, m = len(A), len(A[0])
    i, j = 0, m - 1
    while i < n and j >= 0:
        # invariante: x no está fuera de R(i, j)
        for a in range(n):
            for b in range(m):
                if not (a >= i and b <= j):
                    assert A[a][b] != x
        v = A[i][j]
        if v == x: return (i, j)
        if v > x: j -= 1
        else: i += 1
    return None

random.seed(6)
# 1) y 2) correctitud
for _ in range(1500):
    n, m = random.randint(1, 7), random.randint(1, 7)
    A = matriz_ordenada(n, m)
    x = random.randint(-1, A[-1][-1] + 1)
    r = escalera(A, x)
    assert (r is not None) == bruta(A, x)
    if r: assert A[r[0]][r[1]] == x
    assert (escalera_vigilada(A, x) is not None) == bruta(A, x)
print("1500 matrices aleatorias (con repetidos y rectangulares): OK")

# Ejemplo de la ilustración
A = [[1, 4, 7, 11, 15], [2, 5, 8, 12, 19], [3, 6, 9, 16, 22],
     [10, 13, 14, 17, 24], [18, 21, 23, 26, 30]]
c = [0]
assert escalera(A, 14, c) == (3, 2) and c[0] == 6
print(f"ejemplo de la ilustración: x=14 en (3,2) con {c[0]} comparaciones")

# 3) peor caso 2n-1: A[i][j] = 2(i+j), x impar entre 2(n-1) y 2n
print(f"\n{'n':>5} {'comparaciones':>14} {'2n-1':>6}")
for n in [1, 2, 5, 10, 100, 500]:
    A = [[2 * (i + j) for j in range(n)] for i in range(n)]
    c = [0]
    assert escalera(A, 2 * (n - 1) + 1, c) is None
    print(f"{n:5} {c[0]:14} {2*n-1:6}")
    assert c[0] == 2 * n - 1
