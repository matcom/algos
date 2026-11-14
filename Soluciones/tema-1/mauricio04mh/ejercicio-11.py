"""Ejercicio 11. Mochila entera: costo O(nW) y tamaño de la entrada en bits."""
import math
import random
from itertools import combinations


def mochila(pesos, valores, W):
    n = len(pesos)
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(W + 1):
            dp[i][w] = dp[i - 1][w]
            if pesos[i - 1] <= w:
                dp[i][w] = max(dp[i][w], valores[i - 1] + dp[i - 1][w - pesos[i - 1]])
    return dp[n][W], dp


def fuerza_bruta(pesos, valores, W):
    n = len(pesos)
    mejor = 0
    for r in range(n + 1):
        for sub in combinations(range(n), r):
            if sum(pesos[i] for i in sub) <= W:
                mejor = max(mejor, sum(valores[i] for i in sub))
    return mejor


if __name__ == "__main__":
    pesos, valores, W = [2, 3, 4], [3, 4, 5], 5
    mejor, dp = mochila(pesos, valores, W)
    print("Ejemplo: n = 3, W = 5, respuesta =", mejor)
    for i, fila in enumerate(dp):
        print(f"  i = {i}: {fila}")

    rng = random.Random(11)
    for _ in range(2000):
        n = rng.randint(1, 7)
        p = [rng.randint(1, 8) for _ in range(n)]
        v = [rng.randint(1, 9) for _ in range(n)]
        W = rng.randint(1, 20)
        assert mochila(p, v, W)[0] == fuerza_bruta(p, v, W)
    print("2000 instancias aleatorias: la tabla coincide con la fuerza bruta")

    print("\nTamaño de la entrada y tamaño de la tabla (n = 3 objetos)")
    print(f"{'bits de W':>10} {'W':>22} {'casillas (n+1)(W+1)':>24}")
    for b in [3, 10, 20, 30, 40, 50, 64]:
        W = 2 ** (b - 1)                     # el menor número de b bits
        print(f"{b:>10} {W:>22,} {(3 + 1) * (W + 1):>24,.3g}")

    print("\nPrimalidad por división: divisiones ~ sqrt(N) = 2^(b/2)")
    for b in [32, 64, 128, 256, 1024]:
        print(f"  {b:>5} bits: 2^{b // 2} = {float(2 ** (b // 2)):.3g} divisiones")

    print("\nEscala de la tabla si W se escribiera en unario (tamaño ~ W):")
    for W in [10, 1000, 10**6]:
        print(f"  W = {W:>8,}: binario {W.bit_length():>2} símbolos, unario {W:>8,} símbolos, "
              f"casillas con n = 3: {4 * (W + 1):,}")
