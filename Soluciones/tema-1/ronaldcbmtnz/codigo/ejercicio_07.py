"""Ejercicio 7 del Tema 1: la mediana de dos arreglos ordenados de largo n.

El n-ésimo menor de los 2n elementos, con dos algoritmos O(log n):
  - el clásico: búsqueda binaria sobre cuántos elementos se toman de A, más un max final;
  - el de la escalera: búsqueda binaria sobre una sucesión monótona de 2n - 1 comparaciones,
    que alcanza exactamente la cota de información ⌈log2(2n)⌉.

Uso:
    python ejercicio_07.py             imprime las tablas del informe
    python ejercicio_07.py --figuras   además regenera las figuras

Las pruebas están en test_ejercicio_07.py.
"""

import itertools
import math
import random
import sys
from pathlib import Path


class Contador:
    """Cuenta las comparaciones entre un elemento de A y uno de B."""

    def __init__(self):
        self.total = 0
        self.pares = []

    def menor(self, a, b, par=None):
        self.total += 1
        if par is not None:
            self.pares.append(par)
        return a < b


def oraculo(A, B):
    return sorted(A + B)[len(A) - 1]


# ---------------------------------------------------------------------------
# 1. El algoritmo clásico
# ---------------------------------------------------------------------------

def mediana_clasica(A, B, cont=None):
    """Busca i* = el menor i con A[i] >= B[n-1-i]; la mediana es max(A[i*-1], B[n-i*-1])."""
    cont = cont or Contador()
    n = len(A)
    lo, hi = 0, n                        # invariante: i* está en [lo, hi]
    while lo < hi:
        i = (lo + hi) // 2               # i <= n - 1, así que A[i] y B[n-1-i] existen
        if cont.menor(A[i], B[n - 1 - i], ("A", i, "B", n - 1 - i)):
            lo = i + 1                   # A[i] < B[n-1-i]: i* > i
        else:
            hi = i                       # A[i] >= B[n-1-i]: i* <= i
    i = lo
    j = n - i
    if i == 0:
        return B[n - 1]
    if j == 0:
        return A[n - 1]
    return B[j - 1] if cont.menor(A[i - 1], B[j - 1], ("A", i - 1, "B", j - 1)) else A[i - 1]


# ---------------------------------------------------------------------------
# 2. El algoritmo de la escalera
# ---------------------------------------------------------------------------

def par_de_la_escalera(k, n):
    """El k-ésimo par (i, j) de la escalera: (0,n-1), (0,n-2), (1,n-2), (1,n-3), ..., (n-1,0)."""
    i = k // 2
    j = n - 1 - i - (k % 2)
    return i, j


def mediana_escalera(A, B, cont=None):
    """Búsqueda binaria del primer falso de q(k) = [A[i] < B[j]] sobre los 2n - 1 pares de la escalera.

    Si el primer falso es s: s impar -> la mediana es A[(s-1)/2]; s par -> B[n-1-s/2].
    """
    cont = cont or Contador()
    n = len(A)
    lo, hi = 0, 2 * n - 1                # el primer falso s está en [lo, hi] (hi = 2n-1: no hay falsos)
    while lo < hi:
        k = (lo + hi) // 2
        i, j = par_de_la_escalera(k, n)
        if cont.menor(A[i], B[j], ("A", i, "B", j)):
            lo = k + 1
        else:
            hi = k
    s = lo
    return A[(s - 1) // 2] if s % 2 else B[n - 1 - s // 2]


def predicado_en_la_escalera(A, B):
    """La lista q(0), ..., q(2n-2): debe ser True...True False...False."""
    n = len(A)
    return [A[i] < B[j] for i, j in (par_de_la_escalera(k, n) for k in range(2 * n - 1))]


# ---------------------------------------------------------------------------
# 3. Entradas: todos los intercalados
# ---------------------------------------------------------------------------

def intercalados(n):
    """Todas las formas de intercalar A y B con 2n valores distintos: C(2n, n) entradas."""
    for posiciones in itertools.combinations(range(2 * n), n):
        enA = set(posiciones)
        A = [v for v in range(2 * n) if v in enA]
        B = [v for v in range(2 * n) if v not in enA]
        yield A, B


def peor_caso(funcion, n):
    peor = 0
    for A, B in intercalados(n):
        cont = Contador()
        assert funcion(A, B, cont) == oraculo(A, B)
        peor = max(peor, cont.total)
    return peor


def cota_informacion(n):
    """⌈log2(2n)⌉: hay 2n salidas posibles (cualquier elemento puede ser la mediana)."""
    return math.ceil(math.log2(2 * n))


def salidas_posibles(n):
    """Qué elementos ("A", i) o ("B", j) son la mediana de algún intercalado."""
    salidas = set()
    for A, B in intercalados(n):
        m = oraculo(A, B)
        salidas.add(("A", A.index(m)) if m in A else ("B", B.index(m)))
    return salidas


# ---------------------------------------------------------------------------
# 4. Tablas
# ---------------------------------------------------------------------------

def tabla_peor_caso():
    print("Tabla 1. Peor caso exacto sobre todos los intercalados contra la cota de información")
    print(f"{'n':>3} {'intercalados':>13} {'salidas posibles':>17} {'cota ⌈log2 2n⌉':>15}"
          f" {'escalera':>9} {'clásico':>8}")
    for n in range(1, 11):
        print(f"{n:>3} {math.comb(2 * n, n):>13} {len(salidas_posibles(n)):>17} {cota_informacion(n):>15}"
              f" {peor_caso(mediana_escalera, n):>9} {peor_caso(mediana_clasica, n):>8}")
    print()


def tabla_grandes():
    print("Tabla 2. Arreglos grandes al azar (peor caso sobre 300 entradas)")
    print(f"{'n':>9} {'cota':>5} {'escalera':>9} {'clásico':>8}")
    rng = random.Random(7)
    for n in [10**3, 2**10, 10**5, 2**17, 10**6]:
        peor_e = peor_c = 0
        for _ in range(300):
            valores = rng.sample(range(10 * n), 2 * n) if n <= 2**17 else None
            if valores is None:
                A = sorted(rng.randrange(10**9) for _ in range(n))
                B = sorted(rng.randrange(10**9) for _ in range(n))
            else:
                A, B = sorted(valores[:n]), sorted(valores[n:])
            c1, c2 = Contador(), Contador()
            assert mediana_escalera(A, B, c1) == mediana_clasica(A, B, c2) == oraculo(A, B)
            peor_e, peor_c = max(peor_e, c1.total), max(peor_c, c2.total)
            if n >= 10**5:
                break
        print(f"{n:>9} {cota_informacion(n):>5} {peor_e:>9} {peor_c:>8}")
    print()


def tabla_traza():
    A = [1, 4, 6, 9, 13, 15, 20, 22]
    B = [2, 3, 8, 10, 11, 17, 19, 25]
    print(f"Tabla 3. Traza con A = {A}, B = {B}")
    print(f"  q en la escalera: {''.join('V' if v else 'F' for v in predicado_en_la_escalera(A, B))}")
    cont = Contador()
    m = mediana_escalera(A, B, cont)
    print(f"  comparaciones: {cont.pares}")
    print(f"  mediana: {m} (oráculo {oraculo(A, B)}), {cont.total} comparaciones, cota {cota_informacion(len(A))}")
    print()


# ---------------------------------------------------------------------------
# 5. Figuras
# ---------------------------------------------------------------------------

AZUL, NARANJA, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
TINTA, TINTA_2, TENUE, REJILLA, SUPERFICIE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"


def _estilo(plt):
    plt.rcParams.update({
        "font.family": ["Segoe UI", "DejaVu Sans"], "font.size": 10,
        "axes.edgecolor": "#c3c2b7", "axes.labelcolor": TINTA_2, "axes.titlecolor": TINTA,
        "axes.titlesize": 12, "axes.titleweight": "bold", "axes.titlelocation": "left",
        "axes.facecolor": SUPERFICIE, "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.color": REJILLA, "grid.linewidth": 0.6,
        "xtick.color": TENUE, "ytick.color": TENUE, "xtick.labelcolor": TINTA_2,
        "ytick.labelcolor": TINTA_2, "figure.facecolor": SUPERFICIE, "legend.frameon": False,
        "legend.labelcolor": TINTA_2, "lines.linewidth": 2, "savefig.dpi": 150,
        "savefig.bbox": "tight",
    })


def figura_matriz(plt, destino):
    import matplotlib.patches as patches

    A = [1, 4, 6, 9, 13, 15, 20, 22]
    B = [2, 3, 8, 10, 11, 17, 19, 25]
    n = len(A)
    cont = Contador()
    mediana_escalera(A, B, cont)
    consultadas = {(p[1], p[3]): k + 1 for k, p in enumerate(cont.pares)}
    escalera = [par_de_la_escalera(k, n) for k in range(2 * n - 1)]
    fig, ax = plt.subplots(figsize=(7.4, 7))
    ax.set_aspect("equal")
    ax.axis("off")
    # Filas: i (A), columnas: j (B) de derecha a izquierda, para que la escalera baje como en el ejercicio 6.
    for i in range(n):
        for j in range(n):
            col = n - 1 - j
            menor = A[i] < B[j]
            color = "#d6efe5" if menor else "#fbe0d4"
            en_escalera = (i, j) in escalera
            ax.add_patch(patches.Rectangle((col, -i), 0.95, 0.95, facecolor=color,
                                           edgecolor=AZUL if en_escalera else "#c3c2b7",
                                           linewidth=2.0 if en_escalera else 0.8))
            ax.text(col + 0.47, -i + 0.47, "<" if menor else "≥", ha="center", va="center",
                    fontsize=11, color=TINTA if en_escalera else TENUE)
            if (i, j) in consultadas:
                ax.text(col + 0.82, -i + 0.82, str(consultadas[(i, j)]), ha="center", va="center",
                        fontsize=8, color=AZUL, fontweight="bold")
    for i in range(n):
        ax.text(-0.35, -i + 0.47, f"A[{i}]={A[i]}", ha="right", va="center", fontsize=9, color=TINTA_2)
    for j in range(n):
        ax.text(n - 1 - j + 0.47, 1.2, f"B[{j}]\n{B[j]}", ha="center", va="bottom", fontsize=8.5,
                color=TINTA_2)
    m = mediana_escalera(A, B)
    ax.text(0, -n + 0.45,
            f"verde: A[i] < B[j]   naranja: A[i] ≥ B[j]   contorno azul: la escalera de 2n − 1 = {2 * n - 1}"
            f" pares\nnúmeros azules: las {cont.total} comparaciones de la búsqueda binaria."
            f" Mediana = {m}", fontsize=8.5, color=TINTA_2, va="top")
    ax.set_xlim(-2.2, n + 0.2)
    ax.set_ylim(-n - 0.2, 2.4)
    ax.set_title("La matriz de comparaciones A[i] vs B[j] está ordenada: la mediana vive en su escalera")
    fig.savefig(destino / "ejercicio-07-escalera.png")
    plt.close(fig)


def figura_peor_caso(plt, destino):
    ns = list(range(1, 11))
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.step(ns, [cota_informacion(n) for n in ns], where="mid", color=TENUE, linewidth=6, alpha=0.4,
            label="cota de información ⌈log₂ 2n⌉")
    ax.plot(ns, [peor_caso(mediana_clasica, n) for n in ns], "s", color=NARANJA, markersize=8,
            label="clásico (búsqueda en i + max final)")
    ax.plot(ns, [peor_caso(mediana_escalera, n) for n in ns], "o", color=AZUL, markersize=6,
            label="escalera")
    ax.set_xlabel("n")
    ax.set_ylabel("comparaciones, peor caso exacto")
    ax.set_xticks(ns)
    ax.set_title("Peor caso sobre todos los intercalados: la escalera alcanza la cota")
    ax.legend(loc="upper left")
    fig.savefig(destino / "ejercicio-07-peor-caso.png")
    plt.close(fig)


def figuras():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    _estilo(plt)
    destino = Path(__file__).resolve().parent.parent / "figuras"
    destino.mkdir(exist_ok=True)
    figura_matriz(plt, destino)
    figura_peor_caso(plt, destino)
    print(f"figuras escritas en {destino}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    tabla_traza()
    tabla_peor_caso()
    tabla_grandes()
    if "--figuras" in sys.argv:
        figuras()
