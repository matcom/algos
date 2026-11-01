import math
from pathlib import Path
import matplotlib.pyplot as plt


def mayor_n(costo, presupuesto):
    """Devuelve el mayor entero n >= 1 tal que costo(n) <= presupuesto."""
    alto = 2
    while costo(alto) <= presupuesto:
        alto *= 2
    bajo = 1
    while bajo + 1 < alto:
        medio = (bajo + alto) // 2
        if costo(medio) <= presupuesto:
            bajo = medio
        else:
            alto = medio
    return bajo


if __name__ == "__main__":
    ordenes = {
        "n": lambda n: n,
        "n log2 n": lambda n: n * math.log2(n) if n > 1 else 0.0,
        "n^2": lambda n: n ** 2,
        "n^3": lambda n: n ** 3,
        "2^n": lambda n: 2 ** n,
    }

    hora = 3600 * 10**9  # 3.6e12 operaciones en una hora a 10^9 ops/s
    print("=== Comparacion en 1 hora (B = 3.6e12) con maquina 1000x mas rapida ===")
    print(f"{'Orden':>10} | {'n0 (1x)':>14} | {'n1 (1000x)':>14} | {'Factor n1/n0':>14}")
    print("-" * 62)
    resultados_hora = {}
    for nombre, fn in ordenes.items():
        n0 = mayor_n(fn, hora)
        n1 = mayor_n(fn, 1000 * hora)
        resultados_hora[nombre] = (n0, n1)
        print(f"{nombre:>10} | {n0:>14.4g} | {n1:>14.4g} | {n1 / n0:>14.2f}")

    print("\n=== Evolucion del factor para n log2 n segun el presupuesto B ===")
    print(f"{'Presupuesto B':>14} | {'n0':>12} | {'Factor real':>12} | {'Cota inferior':>14} | {'1 iteracion':>12}")
    print("-" * 74)

    exponentes = list(range(4, 19))
    presupuestos = [10 ** e for e in exponentes]
    factores_reales = []
    cotas_inferiores = []
    iteraciones_1 = []

    for e, b in zip(exponentes, presupuestos):
        n0 = mayor_n(ordenes["n log2 n"], b)
        n1 = mayor_n(ordenes["n log2 n"], 1000 * b)
        f_real = n1 / n0
        cota_inf = 1000 * math.log2(n0) / math.log2(1000 * n0)
        f_iter1 = 1000 * math.log2(n0) / (math.log2(n0) + math.log2(cota_inf))
        factores_reales.append(f_real)
        cotas_inferiores.append(cota_inf)
        iteraciones_1.append(f_iter1)
        if e % 2 == 0:
            print(f"{'10^' + str(e):>14} | {n0:>12.4g} | {f_real:>12.2f} | {cota_inf:>14.2f} | {f_iter1:>12.2f}")

    # Generacion de la figura con 2 paneles
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.5))

    # Panel 1: Factor de crecimiento para n log n vs presupuesto B
    ax1.axhline(1000, color="#888888", linestyle=":", lw=1.5, label="Asintota lineal (1000)")
    ax1.plot(presupuestos, factores_reales, "o-", color="#1f77b4", lw=2, markersize=4.5,
             label="Factor exacto n1 / n0")
    ax1.plot(presupuestos, cotas_inferiores, "s--", color="#ff7f0e", lw=1.7, markersize=4,
             label="Cota 1000 log2(n0) / log2(1000 n0)")
    n0_hora, n1_hora = resultados_hora["n log2 n"]
    ax1.scatter([hora], [n1_hora / n0_hora], color="#d62728", zorder=5, s=55,
                label=f"1 hora (B = 3.6e12): {n1_hora / n0_hora:.1f}x")
    ax1.set_xscale("log")
    ax1.set_title("Factor de ganancia en Theta(n log n) vs presupuesto")
    ax1.set_xlabel("Presupuesto de operaciones B (escala log)")
    ax1.set_ylabel("Factor de crecimiento n1 / n0")
    ax1.set_ylim(500, 1030)
    ax1.grid(True, which="both", alpha=0.3)
    ax1.legend(loc="lower right", fontsize=8.5)

    # Panel 2: Comparacion en escala log-log del tamano maximo resoluble antes y despues
    colores = {
        "n": "#2ca02c",
        "n log2 n": "#1f77b4",
        "n^2": "#ff7f0e",
        "n^3": "#9467bd",
        "2^n": "#d62728",
    }
    for nombre, fn in ordenes.items():
        curva_n0 = [mayor_n(fn, b) for b in presupuestos]
        curva_n1 = [mayor_n(fn, 1000 * b) for b in presupuestos]
        c = colores[nombre]
        ax2.plot(presupuestos, curva_n0, "-", color=c, lw=1.8, label=f"{nombre} (1x)")
        ax2.plot(presupuestos, curva_n1, "--", color=c, lw=1.4, alpha=0.85)

    ax2.axvline(hora, color="#444444", linestyle=":", lw=1.2, label="B = 3.6e12 (1 hora)")
    ax2.set_xscale("log")
    ax2.set_yscale("log")
    ax2.set_title("Tamano maximo n resoluble: 1x (solida) vs 1000x (punteada)")
    ax2.set_xlabel("Presupuesto B (escala log)")
    ax2.set_ylabel("Tamano maximo de entrada n (escala log)")
    ax2.grid(True, which="both", alpha=0.3)
    ax2.legend(loc="upper left", fontsize=8, ncol=2)

    plt.tight_layout()
    salida_png = Path(__file__).with_name("ejercicio-01.png")
    plt.savefig(salida_png, dpi=150)
    print(f"\nGrafica guardada en {salida_png.name}")
