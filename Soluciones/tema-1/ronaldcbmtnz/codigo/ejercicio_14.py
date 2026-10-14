"""Ejercicio 14 del Tema 1: el ciclo completo sobre un problema nuevo.

Intersección de dos listas ordenadas (A ∩ B), y su versión de decisión
(¿tienen algún elemento en común?). Algoritmo de dos punteros con a lo sumo
2n - 1 comparaciones, y cota mínima de exactamente 2n - 1 por adversario.

Uso:
    python ejercicio_14.py             imprime las tablas del informe
    python ejercicio_14.py --figuras   además regenera las figuras

Las pruebas están en test_ejercicio_14.py.
"""

import math
import random
import sys
from functools import lru_cache
from pathlib import Path


class Comparador:
    """Comparación de tres salidas entre un elemento de A y uno de B, con contador y registro."""

    def __init__(self, clave=None):
        self.clave = clave or (lambda v: v)
        self.total = 0
        self.pares = set()

    def comparar(self, a, b):
        self.total += 1
        self.pares.add((a, b))
        x, y = self.clave(a), self.clave(b)
        return (x > y) - (x < y)


# ---------------------------------------------------------------------------
# 1. Los algoritmos
# ---------------------------------------------------------------------------

def interseccion(A, B, cmp=None, vigilar=False):
    """Dos punteros. Devuelve la lista de elementos comunes, en orden."""
    cmp = cmp or Comparador()
    R, i, j = [], 0, 0
    while i < len(A) and j < len(B):
        if vigilar:
            assert R == sorted(set(A[:i]) & set(B[:j]))
            assert not set(A[:i]) & set(B[j:]) and not set(A[i:]) & set(B[:j])
        c = cmp.comparar(A[i], B[j])
        if c == 0:
            R.append(A[i])
            i += 1
            j += 1
        elif c < 0:
            i += 1                      # A[i] < B[j] <= todo B[j:]: A[i] no está en B
        else:
            j += 1
    return R


def hay_comun(A, B, cmp=None):
    """La versión de decisión: se detiene en el primer elemento común."""
    cmp = cmp or Comparador()
    i, j = 0, 0
    while i < len(A) and j < len(B):
        c = cmp.comparar(A[i], B[j])
        if c == 0:
            return True
        if c < 0:
            i += 1
        else:
            j += 1
    return False


def interseccion_galope(A, B, cmp=None):
    """Para |A| << |B|: por cada a de A, búsqueda exponencial y luego binaria en B."""
    cmp = cmp or Comparador()
    R, j = [], 0
    for a in A:
        if j >= len(B):
            break
        paso, hi = 1, j
        while hi < len(B) and cmp.comparar(a, B[hi]) > 0:   # galope: j, j+1, j+3, j+7, ...
            j = hi + 1
            hi = j + paso
            paso *= 2
        hi = min(hi, len(B))
        lo = j
        while lo < hi:                                        # primer B[k] >= a en [lo, hi)
            m = (lo + hi) // 2
            if cmp.comparar(a, B[m]) > 0:
                lo = m + 1
            else:
                hi = m
        j = lo
        if j < len(B) and cmp.comparar(a, B[j]) == 0:
            R.append(a)
            j += 1
    return R


def oraculo(A, B):
    return sorted(set(A) & set(B))


# ---------------------------------------------------------------------------
# 2. El adversario
# ---------------------------------------------------------------------------

def intercalado_perfecto(n):
    """a1 < b1 < a2 < b2 < ... < an < bn: disjuntas."""
    return list(range(0, 4 * n, 4)), list(range(2, 4 * n, 4))


def entrada_con_par_igual(n, k):
    """El intercalado con el k-ésimo par de vecinos de la cadena (k = 0..2n-2) hecho igual.

    Los pares son (a1,b1), (b1,a2), (a2,b2), ..., (an,bn). Se baja el mayor del par
    al valor del menor: las listas siguen estrictamente crecientes y comparten un elemento.
    """
    A, B = intercalado_perfecto(n)
    i = k // 2
    if k % 2 == 0:              # (a_{i+1}, b_{i+1}): B[i] baja a A[i]
        B[i] = A[i]
    else:                       # (b_{i+1}, a_{i+2}): A[i+1] baja a B[i]
        A[i + 1] = B[i]
    return A, B


def par_de_vecinos(k):
    """Los índices (i en A, j en B) del k-ésimo par de vecinos."""
    i = k // 2
    return (i, i) if k % 2 == 0 else (i + 1, i)


# ---------------------------------------------------------------------------
# 3. El óptimo exacto por fuerza bruta (versión de decisión)
# ---------------------------------------------------------------------------

def patrones(n):
    """Todos los órdenes relativos posibles entre A y B (con empates entre listas).

    Cada patrón es una sucesión de pasos 'a', 'b' o 'e' (un a y un b iguales).
    Devuelve, por patrón, la matriz de signos de A[i] - B[j] y si hay algún 'e'.
    """
    resultado = []

    def extender(seq, na, nb):
        if na == n and nb == n:
            va, vb, v = [], [], 0
            for paso in seq:
                v += 1
                if paso in "ae":
                    va.append(v)
                if paso in "be":
                    vb.append(v)
            signos = tuple((x > y) - (x < y) for x in va for y in vb)
            resultado.append((signos, "e" in seq))
            return
        if na < n:
            extender(seq + "a", na + 1, nb)
        if nb < n:
            extender(seq + "b", na, nb + 1)
        if na < n and nb < n:
            extender(seq + "e", na + 1, nb + 1)

    extender("", 0, 0)
    return resultado


def optimo_exacto(n):
    """Profundidad mínima de un árbol de comparaciones que decide si A ∩ B es no vacía."""
    todos = patrones(n)
    consultas = range(n * n)
    mascaras = {}
    for q in consultas:
        for r in (-1, 0, 1):
            m = 0
            for k, (signos, _) in enumerate(todos):
                if signos[q] == r:
                    m |= 1 << k
            mascaras[(q, r)] = m
    con_comun = sum(1 << k for k, (_, e) in enumerate(todos) if e)

    @lru_cache(maxsize=None)
    def costo(conjunto):
        if conjunto & con_comun == 0 or conjunto & ~con_comun == 0:
            return 0
        mejor = math.inf
        for q in consultas:
            partes = [conjunto & mascaras[(q, r)] for r in (-1, 0, 1)]
            if sum(1 for p in partes if p) <= 1:
                continue
            peor = 0
            for p in partes:
                if p:
                    peor = max(peor, costo(p))
                    if 1 + peor >= mejor:
                        break
            mejor = min(mejor, 1 + peor)
            if mejor == 1:
                break
        return mejor

    return costo((1 << len(todos)) - 1), len(todos)


# ---------------------------------------------------------------------------
# 4. Tablas
# ---------------------------------------------------------------------------

def tabla_optimo():
    print("Tabla 1. Experimento antes de demostrar: el óptimo exacto por fuerza bruta")
    for n in [1, 2, 3, 4]:
        opt, cuantos = optimo_exacto(n)
        print(f"  n = {n}: {cuantos} patrones de orden, óptimo = {opt}, 2n - 1 = {2 * n - 1}")
    print()


def tabla_adversario():
    print("Tabla 2. El adversario: el intercalado perfecto y sus 2n - 1 variantes")
    print(f"{'n':>5} {'comparaciones en el intercalado':>32} {'2n - 1':>7}"
          f" {'variantes ordenadas y con común':>32} {'cada una cambia solo su par':>28}")
    for n in [1, 2, 5, 10, 100]:
        A, B = intercalado_perfecto(n)
        cmp = Comparador()
        assert interseccion(A, B, cmp) == []
        ok_orden, ok_par = True, True
        for k in range(2 * n - 1):
            A2, B2 = entrada_con_par_igual(n, k)
            ok_orden &= A2 == sorted(set(A2)) and B2 == sorted(set(B2)) and bool(oraculo(A2, B2))
            cambios = [(i, j) for i in range(n) for j in range(n)
                       if (A[i] > B[j]) - (A[i] < B[j]) != (A2[i] > B2[j]) - (A2[i] < B2[j])]
            ok_par &= cambios == [par_de_vecinos(k)]
        print(f"{n:>5} {cmp.total:>32} {2 * n - 1:>7} {str(ok_orden):>32} {str(ok_par):>28}")
    print()


def tabla_informacion():
    print("Tabla 3. Lo que da la información contra lo que da el adversario")
    print(f"{'n':>6} {'salidas de la intersección':>27} {'⌈log3 C(2n,n)⌉':>15}"
          f" {'mezcla: ⌈log2 C(2n,n)⌉':>24} {'adversario 2n-1':>16}")
    for n in [2, 5, 10, 100, 1000]:
        salidas = math.comb(2 * n, n)
        info = math.ceil(math.log(salidas) / math.log(3) - 1e-12)
        mezcla = (salidas - 1).bit_length()          # ⌈log2 C(2n,n)⌉ exacto, en enteros
        print(f"{n:>6} {('C(%d,%d)' % (2 * n, n)):>27} {info:>15} {mezcla:>24} {2 * n - 1:>16}")
    print()


def tabla_galope(n=10**4, semilla=14):
    print(f"Tabla 4. |B| = {n}: dos punteros contra galope, según |A| = m (peor de 20 entradas)")
    print(f"{'m':>6} {'dos punteros':>13} {'galope':>8} {'m + n - 1':>10} {'m·log2(n/m)':>12}")
    rng = random.Random(semilla)
    filas = []
    for m in [1, 10, 100, 1000, 10**4]:
        peor_d = peor_g = 0
        for _ in range(20):
            B = sorted(rng.sample(range(10 * n), n))
            A = sorted(rng.sample(range(10 * n), m))
            c1, c2 = Comparador(), Comparador()
            assert interseccion(A, B, c1) == interseccion_galope(A, B, c2) == oraculo(A, B)
            peor_d, peor_g = max(peor_d, c1.total), max(peor_g, c2.total)
        filas.append((m, peor_d, peor_g))
        print(f"{m:>6} {peor_d:>13} {peor_g:>8} {m + n - 1:>10} {m * math.log2(n / m):>12.0f}")
    print()
    return filas


# ---------------------------------------------------------------------------
# 5. Figuras
# ---------------------------------------------------------------------------

AZUL, NARANJA, AQUA, ROJO = "#2a78d6", "#eb6834", "#1baf7a", "#e34948"
TINTA, TINTA_2, TENUE, REJILLA, SUPERFICIE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"


def figura_matriz(destino):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches

    plt.rcParams.update({"font.family": ["Segoe UI", "DejaVu Sans"], "font.size": 10,
                         "axes.titlecolor": TINTA, "axes.titlesize": 11, "axes.titleweight": "bold",
                         "axes.titlelocation": "left", "figure.facecolor": SUPERFICIE,
                         "savefig.dpi": 150, "savefig.bbox": "tight"})
    A = [2, 5, 9, 12, 17, 21, 24]
    B = [3, 6, 9, 14, 17, 20, 28]
    n = len(A)
    cmp = Comparador()
    comunes = interseccion(A, B, cmp)
    orden = {}
    i = j = 0
    paso = 0
    while i < n and j < n:
        paso += 1
        orden[(i, j)] = paso
        if A[i] == B[j]:
            i, j = i + 1, j + 1
        elif A[i] < B[j]:
            i += 1
        else:
            j += 1
    fig, ax = plt.subplots(figsize=(7.2, 6.4))
    ax.set_aspect("equal")
    ax.axis("off")
    for r in range(n):
        for c in range(n):
            d = A[r] - B[c]
            color = "#d6efe5" if d < 0 else ("#fbe0d4" if d > 0 else "#cfe0f6")
            camino = (r, c) in orden
            ax.add_patch(patches.Rectangle((c, -r), 0.95, 0.95, facecolor=color,
                                           edgecolor=AZUL if camino else "#c3c2b7",
                                           linewidth=2.2 if camino else 0.8))
            ax.text(c + 0.47, -r + 0.47, f"{d:+d}" if d else "0", ha="center", va="center",
                    fontsize=9, color=TINTA if camino else TENUE, fontweight="bold" if d == 0 else "normal")
            if camino:
                ax.text(c + 0.84, -r + 0.84, str(orden[(r, c)]), ha="center", va="center", fontsize=7,
                        color=AZUL)
    for r in range(n):
        ax.text(-0.25, -r + 0.47, f"A[{r}]={A[r]}", ha="right", va="center", fontsize=9, color=TINTA_2)
    for c in range(n):
        ax.text(c + 0.47, 1.15, f"B[{c}]\n{B[c]}", ha="center", va="bottom", fontsize=8.5, color=TINTA_2)
    ax.text(0, -n + 0.5, f"A[i] − B[j]: verde < 0, naranja > 0, azul = 0 (común).  Recuadros: las"
            f" {cmp.total} comparaciones\nde los dos punteros, que caminan por la matriz como la escalera"
            f" del ejercicio 6.  A ∩ B = {comunes}", fontsize=8.5, color=TINTA_2, va="top")
    ax.set_xlim(-1.9, n + 0.2)
    ax.set_ylim(-n - 0.4, 2.3)
    ax.set_title("Dos punteros = búsqueda en escalera sobre la matriz A[i] − B[j]")
    destino.mkdir(exist_ok=True)
    fig.savefig(destino / "ejercicio-14-matriz.png")
    plt.close(fig)


def figura_galope(destino, n=10**4, semilla=15):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({
        "font.family": ["Segoe UI", "DejaVu Sans"], "font.size": 10,
        "axes.edgecolor": "#c3c2b7", "axes.labelcolor": TINTA_2, "axes.titlecolor": TINTA,
        "axes.titlesize": 12, "axes.titleweight": "bold", "axes.titlelocation": "left",
        "axes.facecolor": SUPERFICIE, "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.color": REJILLA, "grid.linewidth": 0.6,
        "xtick.color": TENUE, "ytick.color": TENUE, "xtick.labelcolor": TINTA_2,
        "ytick.labelcolor": TINTA_2, "figure.facecolor": SUPERFICIE, "legend.frameon": False,
        "legend.labelcolor": TINTA_2, "lines.linewidth": 2, "savefig.dpi": 150, "savefig.bbox": "tight",
    })
    rng = random.Random(semilla)
    ms = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10**4]
    dos, gal = [], []
    for m in ms:
        B = sorted(rng.sample(range(10 * n), n))
        A = sorted(rng.sample(range(10 * n), m))
        c1, c2 = Comparador(), Comparador()
        interseccion(A, B, c1)
        interseccion_galope(A, B, c2)
        dos.append(c1.total)
        gal.append(c2.total)
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.plot(ms, dos, "o-", color=AZUL, markersize=5, label="dos punteros (≤ m + n − 1)")
    ax.plot(ms, gal, "o-", color=NARANJA, markersize=5, label="galope (O(m log(n/m)))")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("m = |A|  (|B| = 10⁴)")
    ax.set_ylabel("comparaciones")
    ax.set_title("Con largos distintos, la cota de 2n − 1 deja de ser la historia")
    ax.legend(loc="upper left")
    fig.savefig(destino / "ejercicio-14-galope.png")
    plt.close(fig)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    tabla_optimo()
    tabla_adversario()
    tabla_informacion()
    tabla_galope()
    if "--figuras" in sys.argv:
        destino = Path(__file__).resolve().parent.parent / "figuras"
        figura_matriz(destino)
        figura_galope(destino)
        print(f"figuras escritas en {destino}")
