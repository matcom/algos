import time
import random

def mochila(n, W, pesos, valores):
    """Programación dinámica O(nW). Devuelve el valor máximo."""
    dp = [0] * (W + 1)
    for i in range(n):
        for w in range(W, pesos[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - pesos[i]] + valores[i])
    return dp[W]

def main():
    random.seed(1)
    print(f"{'n':>6} {'W':>10} {'bits':>8} {'tiempo (s)':>12}")
    for n, W in [(10, 1000), (10, 10000), (10, 100000), (10, 1000000)]:
        pesos = [random.randint(1, W // 2) for _ in range(n)]
        valores = [random.randint(1, 100) for _ in range(n)]
        inicio = time.perf_counter()
        mochila(n, W, pesos, valores)
        seg = time.perf_counter() - inicio
        bits = n * (W.bit_length() + 7)  # aproximación
        print(f"{n:>6} {W:>10} {bits:>8} {seg:>12.4f}")

if __name__ == "__main__":
    main()
