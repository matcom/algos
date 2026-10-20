"""
Problema 14: MEX de un arreglo.

Experimentos:
  - Verificación del algoritmo contra fuerza bruta (set-based).
  - Conteo de swaps en función de n (con cota teórica n).
  - Comparación de tiempos: in-place O(n) vs set O(n) memoria vs sort O(n log n).
  - Histograma de swaps sobre entradas aleatorias.
  - Ejemplo adversario que maximiza swaps.

Genera:
  fig_p14_tiempos.png     : tiempos vs n de los tres enfoques.
  fig_p14_swaps.png       : swaps observados vs cota n.
  fig_p14_histograma.png  : distribución de swaps para n fijo.
  fig_p14_verificacion.png: fallos contra fuerza bruta.
"""
import random
import time
from collections import Counter
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
RUTA = os.path.join("Soluciones", "tema-1", "GlenRios")
os.makedirs(RUTA, exist_ok=True)  # crea la carpeta si no existe


# ----------------------------------------------------------------------
# Algoritmos
# ----------------------------------------------------------------------

def mex_inplace(A):
    """
    MEX con O(n) tiempo y O(1) memoria extra.
    Modifica A. Devuelve (mex, swaps).
    """
    n = len(A)
    i = 0
    swaps = 0
    while i < n:
        v = A[i]
        if 0 <= v < n and A[v] != v:
            A[i], A[v] = A[v], A[i]
            swaps += 1
        else:
            i += 1
    for i in range(n):
        if A[i] != i:
            return i, swaps
    return n, swaps


def mex_set(A):
    """MEX con set: O(n) tiempo, O(n) memoria."""
    s = set(A)
    i = 0
    while i in s:
        i += 1
    return i


def mex_sort(A):
    """MEX ordenando: O(n log n) tiempo, O(n) memoria."""
    B = sorted(set(A))
    i = 0
    for v in B:
        if v == i:
            i += 1
        elif v > i:
            break
    return i


def mex_fuerza_bruta(A):
    """Oráculo: recorre desde 0 y pregunta si está."""
    s = set(A)
    i = 0
    while i in s:
        i += 1
    return i


# ----------------------------------------------------------------------
# Verificación
# ----------------------------------------------------------------------

def verificar(n_sims=20000):
    rng = random.Random(2026)
    fallos = 0
    for _ in range(n_sims):
        n = rng.randint(0, 30)
        # Mezcla de valores: algunos dentro del rango, otros fuera
        A = [rng.randint(0, n + 3) for _ in range(n)]
        esperado = mex_fuerza_bruta(A)
        A_copia = A[:]
        obtenido, _ = mex_inplace(A_copia)
        if obtenido != esperado:
            fallos += 1
    print(f"Fallos contra fuerza bruta en {n_sims} instancias: {fallos}")

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(["fallos"], [fallos], color="tab:red" if fallos else "tab:green")
    ax.set_ylabel("número de fallos")
    ax.set_title(f"Verificación contra fuerza bruta ({n_sims} instancias)")
    ax.grid(True, axis="y", alpha=0.3)
    for i, v in enumerate([fallos]):
        ax.text(i, v + 0.05, str(v), ha="center", va="bottom")
    fig.tight_layout()
    fig.savefig(os.path.join(RUTA, "fig_p14_verificacion.png"), dpi=150)
    plt.close(fig)
    print("  guardada fig_p14_verificacion.png")


# ----------------------------------------------------------------------
# Conteo de swaps
# ----------------------------------------------------------------------

def swaps_aleatorio(n, rng):
    A = [rng.randint(0, n + 3) for _ in range(n)]
    _, s = mex_inplace(A)
    return s


def swaps_rotacion(n):
    """A = [1, 2, ..., n-1, 0]: maximiza swaps."""
    A = list(range(1, n)) + [0]
    _, s = mex_inplace(A)
    return s


def swaps_adversario(n):
    """Permutación aleatoria de 0..n-1 (sin MEX n si es permutación)."""
    rng = random.Random(0)
    A = list(range(n))
    rng.shuffle(A)
    _, s = mex_inplace(A)
    return s


def experimento_swaps():
    rng = random.Random(7)
    ns = [10, 25, 50, 100, 200, 400, 800, 1600, 3200]
    swaps_aleat, swaps_rot, swaps_perm = [], [], []

    print(f"\n{'n':>6} {'aleatorio':>10} {'rotación':>10} {'permutación':>12} {'n':>6}")
    for n in ns:
        s1 = sum(swaps_aleatorio(n, rng) for _ in range(50)) / 50
        s2 = swaps_rotacion(n)
        s3 = swaps_adversario(n)
        swaps_aleat.append(s1)
        swaps_rot.append(s2)
        swaps_perm.append(s3)
        print(f"{n:>6} {s1:>10.1f} {s2:>10} {s3:>12} {n:>6}")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(ns, swaps_aleat, "o-", label="aleatorio", color="tab:blue")
    ax.plot(ns, swaps_rot, "s-", label="rotación $[1,2,\\ldots,n-1,0]$", color="tab:red")
    ax.plot(ns, swaps_perm, "^-", label="permutación aleatoria", color="tab:green")
    ax.plot(ns, ns, "--", label="$n$ (cota)", color="black")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("$n$")
    ax.set_ylabel("swaps")
    ax.set_title("Swaps del algoritmo in-place vs cota $n$")
    ax.legend(); ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(RUTA, "fig_p14_swaps.png"), dpi=150)
    plt.close(fig)
    print("  guardada fig_p14_swaps.png")


def experimento_histograma():
    rng = random.Random(11)
    n = 200
    datos = [swaps_aleatorio(n, rng) for _ in range(3000)]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(datos, bins=range(0, max(datos) + 2), color="tab:purple",
            edgecolor="black", alpha=0.8)
    ax.axvline(n, color="red", linestyle="--", label=f"$n = {n}$")
    ax.set_xlabel("swaps")
    ax.set_ylabel("frecuencia")
    ax.set_title(f"Distribución de swaps para $n={n}$ (3000 instancias aleatorias)")
    ax.legend(); ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(RUTA, "fig_p14_histograma.png"), dpi=150)
    plt.close(fig)
    print("  guardada fig_p14_histograma.png")


# ----------------------------------------------------------------------
# Tiempos
# ----------------------------------------------------------------------

def experimento_tiempos():
    rng = random.Random(3)
    ns = [1000, 5000, 10000, 50000, 100000, 500000, 1000000]
    t_inplace, t_set, t_sort = [], [], []

    print(f"\n{'n':>8} {'in-place':>12} {'set':>12} {'sort':>12}")
    for n in ns:
        A = [rng.randint(0, n + 5) for _ in range(n)]

        A1 = A[:]
        inicio = time.perf_counter()
        mex_inplace(A1)
        t1 = time.perf_counter() - inicio

        A2 = A[:]
        inicio = time.perf_counter()
        mex_set(A2)
        t2 = time.perf_counter() - inicio

        A3 = A[:]
        inicio = time.perf_counter()
        mex_sort(A3)
        t3 = time.perf_counter() - inicio

        t_inplace.append(t1)
        t_set.append(t2)
        t_sort.append(t3)
        print(f"{n:>8} {t1:>12.5f} {t2:>12.5f} {t3:>12.5f}")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(ns, t_inplace, "o-", label="in-place $O(n)$, $O(1)$ memoria", color="tab:blue")
    ax.plot(ns, t_set, "s-", label="set $O(n)$, $O(n)$ memoria", color="tab:green")
    ax.plot(ns, t_sort, "^-", label="sort $O(n \\log n)$", color="tab:red")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("$n$")
    ax.set_ylabel("tiempo (s)")
    ax.set_title("MEX: comparación de tiempos")
    ax.legend(); ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(RUTA, "fig_p14_tiempos.png"), dpi=150)
    plt.close(fig)
    print("  guardada fig_p14_tiempos.png")


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Verificación")
    print("=" * 60)
    verificar(n_sims=20000)

    print("\n" + "=" * 60)
    print("Conteo de swaps")
    print("=" * 60)
    experimento_swaps()

    print("\n" + "=" * 60)
    print("Histograma de swaps")
    print("=" * 60)
    experimento_histograma()

    print("\n" + "=" * 60)
    print("Tiempos")
    print("=" * 60)
    experimento_tiempos()

    print("\nFiguras generadas: fig_p14_verificacion.png, fig_p14_swaps.png, "
          "fig_p14_histograma.png, fig_p14_tiempos.png")