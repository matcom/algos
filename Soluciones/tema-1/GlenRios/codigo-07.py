"""
Mediana (n-ésimo menor) de dos arreglos ordenados de largo n.

Genera figuras:
  - fig_p7_comparaciones.png : comparaciones vs n, con curvas log2(n) y 2*log2(n).
  - fig_p7_boxplot.png       : distribución de comparaciones por n.
  - fig_p7_traza.png         : traza de una ejecución (evolución de [lo, hi]).
  - fig_p7_tipos_entrada.png : comparaciones según el tipo de entrada.
"""
import random
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
RUTA = os.path.join("Soluciones", "tema-1", "GlenRios")
os.makedirs(RUTA, exist_ok=True)  # crea la carpeta si no existe


# ----------------------------------------------------------------------
# Algoritmo
# ----------------------------------------------------------------------

def mediana_dos_arreglos(A, B, traza=None):
    """
    Devuelve (valor_mediana, comparaciones) para arreglos A, B de igual largo n.
    Si traza es una lista, añade (lo, hi, i, j) por iteración.
    """
    n = len(A)
    if n == 0:
        return None, 0
    comparaciones = 0

    def chequear(i):
        nonlocal comparaciones
        j = n - i
        Ai_1 = A[i - 1] if i > 0 else float("-inf")
        Bj = B[j] if j < n else float("inf")
        Bj_1 = B[j - 1] if j > 0 else float("-inf")
        Ai = A[i] if i < n else float("inf")
        comparaciones += 2
        if Ai_1 <= Bj and Bj_1 <= Ai:
            return True
        if Ai_1 > Bj:
            return False
        return None

    lo, hi = 0, n
    while lo <= hi:
        i = (lo + hi) // 2
        if traza is not None:
            traza.append((lo, hi, i))
        r = chequear(i)
        if r is True:
            j = n - i
            izq = max(A[i - 1] if i > 0 else float("-inf"),
                      B[j - 1] if j > 0 else float("-inf"))
            return izq, comparaciones
        elif r is False:
            hi = i - 1
        else:
            lo = i + 1
    return None, comparaciones


def mediana_fuerza_bruta(A, B):
    C = sorted(A + B)
    return C[len(C) // 2 - 1]


# ----------------------------------------------------------------------
# Generadores de entradas
# ----------------------------------------------------------------------

def entrada_uniforme(n, rng):
    A = sorted(rng.randint(0, 10 * n) for _ in range(n))
    B = sorted(rng.randint(0, 10 * n) for _ in range(n))
    return A, B


def entrada_ordenada(n, rng):
    """A tiene los n más pequeños, B los n más grandes. Partición trivial."""
    todos = sorted(rng.randint(0, 10 * n) for _ in range(2 * n))
    return todos[:n], todos[n:]


def entrada_intercalada(n, rng):
    """A y B se alternan en el orden global: a1 < b1 < a2 < b2 < ..."""
    todos = sorted(rng.randint(0, 10 * n) for _ in range(2 * n))
    A = todos[0::2]
    B = todos[1::2]
    return A, B


def entrada_adversaria(n, rng):
    """Los valores de A y B son disjuntos y A va por delante en la primera mitad."""
    A = sorted(rng.sample(range(0, 100 * n), n))
    B = sorted(rng.sample(range(0, 100 * n), n))
    return A, B


# ----------------------------------------------------------------------
# Experimentos
# ----------------------------------------------------------------------

def experimento_comparaciones():
    rng = random.Random(7)
    ns, comps_max, comps_prom = [], [], []
    print(f"{'n':>7} {'máx':>6} {'prom':>8} {'log2(n)':>8} {'2*log2(n)':>10}")
    for n in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]:
        cs = []
        for _ in range(200):
            A, B = entrada_uniforme(n, rng)
            _, c = mediana_dos_arreglos(A, B)
            cs.append(c)
        mx, pr = max(cs), sum(cs) / len(cs)
        ns.append(n); comps_max.append(mx); comps_prom.append(pr)
        lg = math.log2(n) if n > 0 else 0
        print(f"{n:>7} {mx:>6} {pr:>8.1f} {lg:>8.1f} {2*lg:>10.1f}")
    return ns, comps_max, comps_prom


def experimento_boxplot():
    rng = random.Random(13)
    ns = [16, 64, 256, 1024, 4096]
    datos = []
    for n in ns:
        cs = []
        for _ in range(500):
            A, B = entrada_uniforme(n, rng)
            _, c = mediana_dos_arreglos(A, B)
            cs.append(c)
        datos.append(cs)
    return ns, datos


def experimento_traza():
    rng = random.Random(3)
    n = 64
    A, B = entrada_uniforme(n, rng)
    traza = []
    val, comps = mediana_dos_arreglos(A, B, traza=traza)
    return n, traza, comps, val


def experimento_tipos_entrada():
    rng = random.Random(21)
    ns = [32, 128, 512, 2048]
    generadores = {
        "uniforme":    entrada_uniforme,
        "ordenada":    entrada_ordenada,
        "intercalada": entrada_intercalada,
        "adversaria":  entrada_adversaria,
    }
    resultados = {nombre: [] for nombre in generadores}
    for n in ns:
        for nombre, gen in generadores.items():
            cs = []
            for _ in range(100):
                A, B = gen(n, rng)
                _, c = mediana_dos_arreglos(A, B)
                cs.append(c)
            resultados[nombre].append(sum(cs) / len(cs))
    return ns, resultados


# ----------------------------------------------------------------------
# Figuras
# ----------------------------------------------------------------------

def figura_comparaciones():
    ns, comps_max, comps_prom = experimento_comparaciones()
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(ns, comps_max, "o-", label="máximo observado", color="tab:red")
    ax.plot(ns, comps_prom, "s-", label="promedio observado", color="tab:blue")
    ax.plot(ns, [math.log2(n) if n > 0 else 0 for n in ns], "--",
            label="$\\log_2 n$", color="tab:orange")
    ax.plot(ns, [2 * math.log2(n) if n > 0 else 0 for n in ns], ":",
            label="$2\\log_2 n$", color="tab:green")
    ax.set_xscale("log")
    ax.set_xlabel("$n$")
    ax.set_ylabel("comparaciones")
    ax.set_title("Mediana de dos arreglos: comparaciones vs $n$")
    ax.legend(); ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(RUTA,"fig_p7_comparaciones.png"), dpi=150)
    plt.close(fig)
    print("  guardada fig_p7_comparaciones.png")


def figura_boxplot():
    ns, datos = experimento_boxplot()
    fig, ax = plt.subplots(figsize=(8, 5))
    bp = ax.boxplot(datos, label=[str(n) for n in ns], patch_artist=True,
                    medianprops=dict(color="black"))
    for caja in bp["boxes"]:
        caja.set_facecolor("tab:blue")
        caja.set_alpha(0.6)
    ax.set_xlabel("$n$")
    ax.set_ylabel("comparaciones")
    ax.set_title("Distribución de comparaciones (500 instancias por $n$)")
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(RUTA,"fig_p7_boxplot.png"), dpi=150)
    plt.close(fig)
    print("  guardada fig_p7_boxplot.png")


def figura_traza():
    n, traza, comps, val = experimento_traza()
    fig, axes = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

    # Subplot 1: evolución del intervalo [lo, hi]
    iteraciones = list(range(len(traza)))
    los = [t[0] for t in traza]
    his = [t[1] for t in traza]
    is_ = [t[2] for t in traza]
    axes[0].fill_between(iteraciones, los, his, color="tab:blue", alpha=0.3,
                         label="intervalo $[lo, hi]$")
    axes[0].plot(iteraciones, is_, "o-", color="tab:red",
                 label="valor probado $i$")
    axes[0].set_ylabel("índice $i$ en $A$")
    axes[0].set_title(f"Traza de la búsqueda binaria ($n = {n}$, "
                      f"{comps} comparaciones)")
    axes[0].legend(); axes[0].grid(True, alpha=0.3)

    # Subplot 2: tamaño del intervalo
    tamaños = [h - l for (l, h, _) in traza]
    axes[1].plot(iteraciones, tamaños, "s-", color="tab:green")
    axes[1].set_xlabel("iteración")
    axes[1].set_ylabel("tamaño del intervalo")
    axes[1].set_title("El intervalo se reduce a la mitad en cada iteración")
    axes[1].grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(os.path.join(RUTA,"fig_p7_traza.png"), dpi=150)
    plt.close(fig)
    print("  guardada fig_p7_traza.png")


def figura_tipos_entrada():
    ns, resultados = experimento_tipos_entrada()
    fig, ax = plt.subplots(figsize=(8, 5))
    marcadores = {"uniforme": "o-", "ordenada": "s-",
                  "intercalada": "^-", "adversaria": "d-"}
    for nombre, vals in resultados.items():
        ax.plot(ns, vals, marcadores[nombre], label=nombre)
    ax.plot(ns, [math.log2(n) for n in ns], "--", color="gray",
            label="$\\log_2 n$")
    ax.set_xscale("log")
    ax.set_xlabel("$n$")
    ax.set_ylabel("comparaciones (promedio)")
    ax.set_title("Comparaciones según el tipo de entrada")
    ax.legend(); ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(RUTA,"fig_p7_tipos_entrada.png"), dpi=150)
    plt.close(fig)
    print("  guardada fig_p7_tipos_entrada.png")


# ----------------------------------------------------------------------
# Verificación
# ----------------------------------------------------------------------

def verificar():
    rng = random.Random(99)
    fallos = 0
    for _ in range(2000):
        n = rng.randint(1, 30)
        A, B = entrada_uniforme(n, rng)
        v1, _ = mediana_dos_arreglos(A, B)
        v2 = mediana_fuerza_bruta(A, B)
        if v1 != v2:
            fallos += 1
    print(f"Fallos contra fuerza bruta en 2000 instancias: {fallos}")


if __name__ == "__main__":
    verificar()
    print()
    figura_comparaciones()
    figura_boxplot()
    figura_traza()
    figura_tipos_entrada()
    print("\nFiguras generadas.")