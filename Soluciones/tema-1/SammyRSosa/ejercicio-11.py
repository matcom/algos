import random
from pathlib import Path
import matplotlib.pyplot as plt


def mochila(pesos, valores, W):
    """
    Programacion dinamica 0/1 en O(nW): mejor[c] guarda el valor optimo con capacidad c.
    Devuelve (valor_optimo, celdas_actualizadas).
    """
    mejor = [0] * (W + 1)
    celdas = 0
    for w, v in zip(pesos, valores):
        for c in range(W, w - 1, -1):
            celdas += 1
            nuevo = mejor[c - w] + v
            if nuevo > mejor[c]:
                mejor[c] = nuevo
    return mejor[W], celdas


def bits_de_la_entrada(pesos, valores, W):
    return sum(x.bit_length() for x in pesos + valores) + W.bit_length()


if __name__ == "__main__":
    # 1. Ejemplo pequeno a mano (3 objetos) escalando los pesos y W por potencias de 2
    pesos_base = [2, 3, 4]
    valores_base = [3, 4, 5]
    W_base = 5
    print("=== Ejemplo pequeno (n = 3) escalando pesos y capacidad por 2^k ===")
    print(f"{'Factor 2^k':>12} {'W':>8} {'Bits entrada (N)':>18} {'Celdas evaluadas':>18} {'Valor optimo':>14}")
    for k in [0, 3, 6, 9, 12]:
        factor = 2 ** k
        pesos_k = [w * factor for w in pesos_base]
        W_k = W_base * factor
        opt, celdas = mochila(pesos_k, valores_base, W_k)
        bits_k = bits_de_la_entrada(pesos_k, valores_base, W_k)
        print(f"{factor:>12,} {W_k:>8,} {bits_k:>18} {celdas:>18,} {opt:>14}")
    print()

    # 2. Experimento con n = 10 fijo y capacidad W = 2^b
    rng = random.Random(314)
    n_fijo = 10
    bs = list(range(4, 21, 2))
    bits_lista = []
    celdas_exp_lista = []

    print(f"{'b':>4} {'W = 2^b':>10} {'bits de la entrada (N)':>24} {'celdas actualizadas':>21}")
    for b in bs:
        W = 2 ** b
        pesos = [rng.randint(W // 4, W // 2) for _ in range(n_fijo)]
        valores = [rng.randint(1, W) for _ in range(n_fijo)]
        _, celdas = mochila(pesos, valores, W)
        nbits = bits_de_la_entrada(pesos, valores, W)
        bits_lista.append(nbits)
        celdas_exp_lista.append(celdas)
        print(f"{b:>4} {W:>10,} {nbits:>24} {celdas:>21,}")

    # 3. Extrapolacion para n = 100 objetos a 10^9 operaciones por segundo
    print("\n=== Extrapolacion para n = 100 objetos (a 10^9 ops/s) ===")
    segundos_anio = 3600 * 24 * 365
    for b in [32, 64, 128]:
        ops = 100 * (2 ** b)
        anios = ops / 1e9 / segundos_anio
        bits_aprox = 2 * 100 * b + b
        print(f"n = 100, W = 2^{b:<3} | entrada ~ {bits_aprox:>6} bits | {float(ops):.2e} ops | {anios:.2e} anios")

    # 4. Comparacion de dos regimenes variando n (n = 2..16):
    # Regimen A (pesos pequenos): W = 10 * n -> polinomial en N
    # Regimen B (pesos de n bits): W = 2^n -> exponencial en N
    ns_reg = list(range(2, 17))
    celdas_reg_poli = []
    celdas_reg_expo = []
    for n_val in ns_reg:
        # Regimen A: W = 10n, pesos entre 1 y 5n
        W_a = 10 * n_val
        pesos_a = [max(1, (i * 3) % (5 * n_val) + 1) for i in range(1, n_val + 1)]
        valores_a = [1] * n_val
        _, c_a = mochila(pesos_a, valores_a, W_a)
        celdas_reg_poli.append(c_a)

        # Regimen B: W = 2^n, pesos alrededor de 2^(n-2)
        W_b = 2 ** n_val
        pesos_b = [max(1, W_b // 4 + i) for i in range(n_val)]
        valores_b = [1] * n_val
        _, c_b = mochila(pesos_b, valores_b, W_b)
        celdas_reg_expo.append(c_b)

    # 5. Generacion de la grafica con 2 paneles
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.4))

    polinomio_ref = [nb ** 2 for nb in bits_lista]
    ax1.plot(bits_lista, celdas_exp_lista, "o-", color="#d62728", lw=2, markersize=5,
             label="Celdas DP reales (n=10, W=2^b)")
    ax1.plot(bits_lista, polinomio_ref, "s--", color="#1f77b4", lw=1.8, markersize=4,
             label="Referencia cuadratica en bits (N^2)")
    ax1.set_yscale("log")
    ax1.set_title("Explosion exponencial frente a los bits N (escala log)")
    ax1.set_xlabel("Tamano de la entrada N (en bits)")
    ax1.set_ylabel("Celdas evaluadas (escala log)")
    ax1.grid(True, which="both", alpha=0.3)
    ax1.legend(fontsize=8.5)

    ax2.plot(ns_reg, celdas_reg_expo, "o-", color="#d62728", lw=2, markersize=5,
             label="Regimen de numeros grandes: W = 2^n (exponencial)")
    ax2.plot(ns_reg, celdas_reg_poli, "s-", color="#2ca02c", lw=2, markersize=5,
             label="Regimen de pesos acotados: W = 10n (polinomial)")
    ax2.set_yscale("log")
    ax2.set_title("El mismo algoritmo O(nW) en dos regimenes (n = 2..16)")
    ax2.set_xlabel("Numero de objetos (n)")
    ax2.set_ylabel("Celdas evaluadas (escala log)")
    ax2.set_xticks(ns_reg)
    ax2.grid(True, which="both", alpha=0.3)
    ax2.legend(fontsize=8.5)

    plt.tight_layout()
    salida_png = Path(__file__).with_name("ejercicio-11.png")
    plt.savefig(salida_png, dpi=150)
    print(f"\nGrafica guardada en {salida_png.name}")
