"""Ejercicio 6. Búsqueda en una matriz con filas y columnas ordenadas."""
import random


def escalera(M, x, vigilar=True):
    """Devuelve (posición o None, comparaciones). Vigila el invariante y el potencial."""
    n = len(M)
    i, j, comps = 0, n - 1, 0
    while i < n and j >= 0:
        if vigilar:
            if any(M[a][b] == x for a in range(n) for b in range(n)):
                assert any(M[a][b] == x for a in range(i, n) for b in range(0, j + 1)), "invariante roto"
        phi = (n - i) + (j + 1)
        comps += 1
        if x == M[i][j]:
            return (i, j), comps
        if x < M[i][j]:
            j -= 1
        else:
            i += 1
        assert (n - i) + (j + 1) == phi - 1
    return None, comps


def matriz_aleatoria(n, rng):
    """Matriz con filas y columnas estrictamente crecientes."""
    base = sorted(rng.sample(range(10 * n * n), n * n))
    # M[i][j] = k-ésimo menor con k = i*n + j no cumple las columnas en general:
    # se construye sumando incrementos positivos por fila y columna.
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            arriba = M[i - 1][j] if i else 0
            izq = M[i][j - 1] if j else 0
            M[i][j] = max(arriba, izq) + rng.randint(1, 5)
    return M


def antidiagonal(n, x):
    """Matrices M1 (sin x) y M2c (con x en la celda c) del adversario."""
    def valor(i, j):
        s = i + j
        if s <= n - 2:
            return x - (n - s)
        if s >= n:
            return x + 1 + (s - n)
        return x + (i + 1) / (n + 1)
    return [[valor(i, j) for j in range(n)] for i in range(n)]


def es_creciente(M):
    n = len(M)
    return all(M[i][j] < M[i][j + 1] for i in range(n) for j in range(n - 1)) and \
           all(M[i][j] < M[i + 1][j] for i in range(n - 1) for j in range(n))


if __name__ == "__main__":
    M = [[1, 4, 7, 11], [2, 5, 8, 12], [3, 6, 9, 16], [10, 13, 14, 17]]
    for x in (9, 15):
        print(f"x = {x}: {escalera(M, x)}")

    rng = random.Random(6)
    print(f"\n{'n':>3} {'pruebas':>8} {'máx. comparaciones':>19} {'2n-1':>5}")
    for n in [2, 3, 4, 5, 8, 12]:
        peor = 0
        for _ in range(300):
            M = matriz_aleatoria(n, rng)
            assert es_creciente(M)
            valores = {v for fila in M for v in fila}
            for x in list(valores) + [v + 0.5 for v in valores] + [-1, 10**9]:
                pos, c = escalera(M, x)
                assert (pos is not None) == (x in valores)
                if pos:
                    assert M[pos[0]][pos[1]] == x
                peor = max(peor, c)
        assert peor <= 2 * n - 1
        print(f"{n:>3} {300:>8} {peor:>19} {2 * n - 1:>5}")

    print("\nAdversario (antidiagonal): M1 no contiene x; M2c lo contiene en la celda c.")
    for n in [2, 3, 4, 6, 8]:
        x = 10
        M1 = antidiagonal(n, x)
        assert es_creciente(M1) and all(v != x for fila in M1 for v in fila)
        for c in range(n):
            M2 = [fila[:] for fila in M1]
            M2[c][n - 1 - c] = x
            assert es_creciente(M2) and sum(v == x for fila in M2 for v in fila) == 1
        print(f"n = {n}: M1 válida sin x, y las {n} matrices M2c válidas con x")
    print("\nM1 para n = 4, x = 10:")
    for fila in antidiagonal(4, 10):
        print("  " + " ".join(f"{v:6.1f}" for v in fila))
