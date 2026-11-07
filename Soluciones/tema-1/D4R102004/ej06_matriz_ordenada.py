"""Ejercicio 6: búsqueda en una matriz n×n con filas y columnas crecientes.
Algoritmo de la esquina superior derecha, con invariante y potencial vigilados,
y la matriz trampa del adversario."""
import random


def buscar(A, x):
    """Devuelve (está?, comparaciones)."""
    n = len(A)
    f, c = 0, n - 1
    comparaciones = 0
    while f < n and c >= 0:
        # invariante: si x está en A, está en las filas f..n-1 y columnas 0..c
        assert not any(x in fila for fila in A) or any(x in A[i][:c + 1] for i in range(f, n))
        potencial = (n - f) + (c + 1)
        comparaciones += 1
        if A[f][c] == x:
            return True, comparaciones
        if x < A[f][c]:
            c -= 1          # la columna c tiene solo valores >= A[f][c] > x
        else:
            f += 1          # la fila f tiene a la izquierda solo valores <= A[f][c] < x
        assert 0 <= (n - f) + (c + 1) < potencial
    return False, comparaciones


def matriz_aleatoria(n, rng):
    """Filas y columnas crecientes: cada casilla es al menos el máximo de arriba y de la izquierda."""
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            base = max(A[i - 1][j] if i else 0, A[i][j - 1] if j else 0)
            A[i][j] = base + rng.randint(0, 3)
    return A


def trampa(n):
    """A[i][j] = i + j, salvo la antidiagonal (i + j = n - 1), que vale n - 1.5. x = n - 1 no está."""
    return [[(n - 1.5) if i + j == n - 1 else i + j for j in range(n)] for i in range(n)]


def ordenada(A):
    n = len(A)
    return all(A[i][j] <= A[i][j + 1] for i in range(n) for j in range(n - 1)) and \
           all(A[i][j] <= A[i + 1][j] for i in range(n - 1) for j in range(n))


# 1. Correctitud contra la búsqueda exhaustiva, y cota 2n - 1
rng = random.Random(6)
for _ in range(3000):
    n = rng.randint(1, 12)
    A = matriz_aleatoria(n, rng)
    x = rng.randint(-1, A[-1][-1] + 1)
    esta, comps = buscar(A, x)
    assert esta == any(x in fila for fila in A)
    assert comps <= 2 * n - 1
print("3000 búsquedas al azar: correctas, invariante y potencial cumplidos, <= 2n-1 comparaciones\n")

# 2. El adversario: en la matriz trampa, cambiar cualquier casilla de la antidiagonal por x
#    la deja ordenada y hace que x sí esté.
for n in [2, 4, 8, 50]:
    T, x = trampa(n), n - 1
    assert ordenada(T) and not any(x in fila for fila in T)
    for i in range(n):
        T2 = [fila[:] for fila in T]
        T2[i][n - 1 - i] = x
        assert ordenada(T2) and buscar(T2, x)[0]
print("matriz trampa: cada una de las n casillas de la antidiagonal se puede cambiar por x")
print("sin desordenar la matriz, así que un algoritmo correcto tiene que mirar las n\n")

print(f"{'n':>5} {'comparaciones en la trampa':>27} {'cota mínima n':>14} {'2n - 1':>7}")
for n in [4, 16, 64, 256]:
    print(f"{n:>5} {buscar(trampa(n), n - 1)[1]:>27} {n:>14} {2 * n - 1:>7}")
