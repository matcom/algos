"""
Problema 11: Mochila entera y tiempo pseudopolinomial.

Experimentos:
  - Verificación de la DP contra fuerza bruta.
  - Comparación del tiempo de la mochila DP y la primalidad por división.
    * Contra el valor de la entrada (escala lineal).
    * Contra el número de bits (escala logarítmica).

Genera (en Soluciones/tema-1/GlenRios/):
  fig_p11_verificacion.png  : confirmación de 0 fallos.
  fig_p11_tiempo_valor.png  : tiempo vs valor (escala lineal).
  fig_p11_tiempo_bits.png   : tiempo vs bits (escala logarítmica).
"""
import os
import time
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RUTA = os.path.join("Soluciones", "tema-1", "GlenRios")
os.makedirs(RUTA, exist_ok=True)


# ----------------------------------------------------------------------
# Algoritmos
# ----------------------------------------------------------------------

def mochila_dp(pesos, valores, W):
    """Mochila entera con DP. Tiempo O(nW), memoria O(W)."""
    n = len(pesos)
    dp = [0] * (W + 1)
    for i in range(n):
        for w in range(W, pesos[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - pesos[i]] + valores[i])
    return dp[W]


def mochila_fuerza_bruta(pesos, valores, W):
    """Mochila por fuerza bruta (oráculo). O(2^n)."""
    n = len(pesos)
    mejor = 0
    for mask in range(1 << n):
        peso_actual = 0
        valor_actual = 0
        for i in range(n):
            if mask & (1 << i):
                peso_actual += pesos[i]
                valor_actual += valores[i]
        if peso_actual <= W:
            mejor = max(mejor, valor_actual)
    return mejor


def es_primo_division(n):
    """Primalidad por división por tentativa. O(sqrt(n))."""
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


# ----------------------------------------------------------------------
# Experimentos
# ----------------------------------------------------------------------

def experimento_verificacion():
    rng = random.Random(42)
    fallos = 0
    total = 200
    for _ in range(total):
        n = rng.randint(1, 10)
        pesos = [rng.randint(1, 20) for _ in range(n)]
        valores = [rng.randint(1, 50) for _ in range(n)]
        W = rng.randint(1, 30)
        v_dp = mochila_dp(pesos, valores, W)
        v_fb = mochila_fuerza_bruta(pesos, valores, W)
        if v_dp != v_fb:
            fallos += 1

    print(f"Verificación: {fallos} fallos en {total} instancias.")

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(["Fallos"], [fallos], color="tab:red" if fallos else "tab:green")
    ax.set_ylabel("número de fallos")
    ax.set_title(f"Verificación DP vs Fuerza Bruta ({total} instancias)")
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(RUTA, "fig_p11_verificacion.png"), dpi=150)
    plt.close(fig)
    print("  guardada fig_p11_verificacion.png")


def experimento_pseudo():
    rng = random.Random(7)
    n = 50  # fijo número de ítems
    bits = [10, 12, 14, 16, 18, 20]
    valores = [2**b for b in bits]

    tiempos_mochila = []
    tiempos_primo = []

    # Primos cercanos a 2^b para forzar el peor caso en la división
    primos = {
        10: 1021, 12: 4093, 14: 16381,
        16: 65521, 18: 262139, 20: 1048573
    }

    for b in bits:
        W = 2**b
        pesos = [rng.randint(1, 100) for _ in range(n)]
        valores_m = [rng.randint(1, 100) for _ in range(n)]

        # Mochila DP
        inicio = time.perf_counter()
        mochila_dp(pesos, valores_m, W)
        tiempos_mochila.append(time.perf_counter() - inicio)

        # Primalidad por división
        inicio = time.perf_counter()
        es_primo_division(primos[b])
        tiempos_primo.append(time.perf_counter() - inicio)

    print(f"\n{'Bits':>6} {'Valor':>10} {'T_Mochila (s)':>16} {'T_Primo (s)':>14}")
    for b, v, tm, tp in zip(bits, valores, tiempos_mochila, tiempos_primo):
        print(f"{b:>6} {v:>10} {tm:>16.6f} {tp:>14.6f}")

    # ---------- Figura 1: Tiempo vs Valor (escala lineal) ----------
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(valores, tiempos_mochila, "o-", label="Mochila DP $O(nW)$", color="tab:blue")
    ax.plot(valores, tiempos_primo, "s-", label="Primo División $O(\\sqrt{n})$", color="tab:orange")
    ax.set_xlabel("Valor de la entrada ($W$ o $n$)")
    ax.set_ylabel("Tiempo (s)")
    ax.set_title("Tiempo vs Valor (escala lineal)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(RUTA, "fig_p11_tiempo_valor.png"), dpi=150)
    plt.close(fig)

    # ---------- Figura 2: Tiempo vs Bits (escala logarítmica) ----------
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(bits, tiempos_mochila, "o-", label="Mochila DP $O(n 2^b)$", color="tab:blue")
    ax.plot(bits, tiempos_primo, "s-", label="Primo División $O(2^{b/2})$", color="tab:orange")
    ax.set_yscale("log")
    ax.set_xlabel("Bits de la entrada $b$")
    ax.set_ylabel("Tiempo (s) — escala log")
    ax.set_title("Tiempo vs Bits (escala logarítmica)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(RUTA, "fig_p11_tiempo_bits.png"), dpi=150)
    plt.close(fig)

    print("\n  guardadas fig_p11_tiempo_valor.png y fig_p11_tiempo_bits.png")


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Verificación de la DP")
    print("=" * 60)
    experimento_verificacion()

    print("\n" + "=" * 60)
    print("Experimento pseudopolinomial")
    print("=" * 60)
    experimento_pseudo()

    print("\nFiguras generadas en Soluciones/tema-1/GlenRios/")