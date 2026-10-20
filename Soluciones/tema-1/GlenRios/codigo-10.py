"""
Par más cercano en 1D con el algoritmo aleatorio incremental.

Genera figuras:
  - fig_p10_tiempos.png         : tiempo vs n para fuerza bruta y aleatorio.
  - fig_p10_reconstrucciones.png: reconstrucciones observadas vs 2 ln n.
  - fig_p10_verificacion.png    : fallos contra fuerza bruta.
"""
import random
import math
import time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
RUTA = os.path.join("Soluciones", "tema-1", "GlenRios")
os.makedirs(RUTA, exist_ok=True)  # crea la carpeta si no existe


def fuerza_bruta_1d(P):
    """Par más cercano por fuerza bruta. Devuelve (distancia, comparaciones)."""
    n = len(P)
    mejor = float("inf")
    comps = 0
    for i in range(n):
        for j in range(i + 1, n):
            comps += 1
            d = abs(P[i] - P[j])
            if d < mejor:
                mejor = d
    return mejor, comps


def par_mas_cercano_1d_aleatorio(P, semilla=0):
    """
    Algoritmo aleatorio incremental en 1D.
    Devuelve (distancia, reconstrucciones, accesos_hash).
    """
    rng = random.Random(semilla)
    pts = list(P)
    rng.shuffle(pts)
    if len(pts) < 2:
        return 0.0, 0, 0

    delta = abs(pts[0] - pts[1])
    lado = delta / 2
    def celda(x):
        return int(x // lado)
    rejilla = {celda(pts[0]): pts[0], celda(pts[1]): pts[1]}
    reconstrucciones = 0
    accesos = 0

    for i in range(2, len(pts)):
        p = pts[i]
        c = celda(p)
        delta_antes = delta
        for dc in (-1, 0, 1):
            accesos += 1
            q = rejilla.get(c + dc)
            if q is not None:
                d = abs(p - q)
                if d < delta:
                    delta = d
        if delta < delta_antes:
            # Reconstruir rejilla
            lado = delta / 2
            rejilla = {celda(q): q for q in pts[:i + 1]}
            reconstrucciones += 1
        else:
            rejilla[c] = p
    return delta, reconstrucciones, accesos


def experimento_tiempos():
    rng = random.Random(11)
    ns, t_fb, t_al = [], [], []
    print(f"{'n':>7} {'fuerza bruta':>14} {'aleatorio':>12}")
    for n in [500, 1000, 2000, 4000, 8000, 16000]:
        P = [rng.random() for _ in range(n)]
        inicio = time.perf_counter()
        fuerza_bruta_1d(P)
        t1 = time.perf_counter() - inicio
        inicio = time.perf_counter()
        par_mas_cercano_1d_aleatorio(P)
        t2 = time.perf_counter() - inicio
        ns.append(n); t_fb.append(t1); t_al.append(t2)
        print(f"{n:>7} {t1:>14.4f} {t2:>12.4f}")

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(ns, t_fb, "o-", label="fuerza bruta $O(n^2)$", color="tab:red")
    ax.plot(ns, t_al, "s-", label="aleatorio $O(n)$", color="tab:blue")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("$n$"); ax.set_ylabel("tiempo (s)")
    ax.set_title("Par más cercano en 1D: tiempos")
    ax.legend(); ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(RUTA, "fig_p10_tiempos.png"), dpi=150)
    plt.close(fig)
    print("  guardada fig_p10_tiempos.png")


def experimento_reconstrucciones():
    rng = random.Random(3)
    ns, recon, teor = [], [], []
    print(f"\n{'n':>7} {'recon':>8} {'2 ln n':>8}")
    for n in [100, 500, 1000, 5000, 10000, 50000, 100000]:
        P = [rng.random() for _ in range(n)]
        _, r, _ = par_mas_cercano_1d_aleatorio(P, semilla=0)
        ns.append(n); recon.append(r); teor.append(2 * math.log(n))
        print(f"{n:>7} {r:>8} {2*math.log(n):>8.1f}")

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(ns, recon, "o-", label="reconstrucciones observadas", color="tab:blue")
    ax.plot(ns, teor, "--", label="$2\\ln n$", color="tab:orange")
    ax.set_xscale("log")
    ax.set_xlabel("$n$"); ax.set_ylabel("reconstrucciones")
    ax.set_title("Reconstrucciones vs $2\\ln n$")
    ax.legend(); ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(RUTA, "fig_p10_reconstrucciones.png"), dpi=150)
    plt.close(fig)
    print("  guardada fig_p10_reconstrucciones.png")


def experimento_verificacion():
    rng = random.Random(99)
    fallos = 0
    for _ in range(500):
        n = rng.randint(2, 50)
        P = [rng.random() for _ in range(n)]
        d1, _ = fuerza_bruta_1d(P)
        d2, _, _ = par_mas_cercano_1d_aleatorio(P, semilla=rng.randint(0, 1000))
        if abs(d1 - d2) > 1e-12:
            fallos += 1
    print(f"\nFallos contra fuerza bruta en 500 instancias: {fallos}")

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.bar(["fallos"], [fallos], color="tab:red")
    ax.set_ylabel("número de fallos")
    ax.set_title("Verificación del algoritmo aleatorio contra fuerza bruta")
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(RUTA, "fig_p10_verificacion.png"), dpi=150)
    plt.close(fig)
    print("  guardada fig_p10_verificacion.png")


if __name__ == "__main__":
    experimento_tiempos()
    experimento_reconstrucciones()
    experimento_verificacion()
    print("\nFiguras generadas.")