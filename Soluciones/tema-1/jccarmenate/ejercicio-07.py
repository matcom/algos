"""Ejercicio 7 del Tema 1: la mediana de dos arreglos ordenados de largo n.

    python ejercicio-07.py

Imprime todas las tablas que cita ejercicio-07.md, corre las pruebas y regenera las
tres figuras (ejercicio-07-corte.svg, ejercicio-07-comparaciones.svg y
ejercicio-07-errores.svg). Cada número que aparece en la prosa sale de aquí. Solo
necesita matplotlib.
"""

import itertools
import math
import random
from functools import lru_cache

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt


# --------------------------------------------------------------------------
# 1. El algoritmo
# --------------------------------------------------------------------------

class Comparador:
    """a <= b, contando. Con valores iguales, el de A va primero: así el orden de los
    2n elementos queda bien definido aunque haya repetidos."""

    def __init__(self):
        self.veces = 0

    def __call__(self, a, b):
        self.veces += 1
        return a <= b


def split_point(A, B, less_equal):
    """i* = cuántos elementos de A hay entre los n menores. Es la cantidad de k con
    A[k] <= B[n-1-k], y esa condición es verdadera para k < i* y falsa después."""
    n = len(A)
    lo, hi = 0, n                       # invariante: c_k vale para k < lo, no vale para k >= hi
    while lo < hi:
        m = (lo + hi) // 2
        if less_equal(A[m], B[n - 1 - m]):
            lo = m + 1
        else:
            hi = m
    return lo


def median(A, B, less_equal, centinela_python=False):
    """El n-ésimo menor de los 2n elementos. `centinela_python = True` es el error
    plantado de la sección 7: confiar en que A[-1] y B[-1] se portan como -infinito."""
    n = len(A)
    i = split_point(A, B, less_equal)
    j = n - i                           # elementos de B entre los n menores
    if not centinela_python:
        if i == 0:
            return B[n - 1]
        if j == 0:
            return A[n - 1]
    a, b = A[i - 1], B[j - 1]           # con i = 0, A[-1] es el ÚLTIMO de A, no -infinito
    return b if less_equal(a, b) else a


def median_alternating(A, B, less_equal):
    """La búsqueda de la sección 5 sobre la fila c_0, d_0, c_1, ..., d_{n-2}, c_{n-1}:
    la posición t = 2k es c_k (A[k] <= B[n-1-k]) y t = 2k + 1 es d_k (A[k] <= B[n-2-k])."""
    n = len(A)
    lo, hi = 0, 2 * n - 1               # invariante: vale para t < lo, no vale para t >= hi
    while lo < hi:
        t = (lo + hi) // 2
        k = t // 2
        if less_equal(A[k], B[n - 1 - k - t % 2]):
            lo = t + 1
        else:
            hi = t
    return A[lo // 2] if lo % 2 == 1 else B[n - 1 - lo // 2]


def oraculo(A, B):
    return sorted(A + B)[len(A) - 1]


def seccion(titulo):
    print()
    print(titulo)
    print("-" * len(titulo))


def miles(x):
    return f"{x:,}".replace(",", " ")


def techo_log2(m):
    return (m - 1).bit_length()


# --------------------------------------------------------------------------
# 2. Las tablas que cita la prosa
# --------------------------------------------------------------------------

EJ_A = [3, 8, 11, 20, 24, 31, 40, 52]
EJ_B = [1, 5, 9, 14, 17, 26, 33, 45]


def ejemplo_chico():
    seccion("§2. Ejemplo chico: n = 8")
    A, B, n = EJ_A, EJ_B, len(EJ_A)
    print("A =", " ".join(map(str, A)))
    print("B =", " ".join(map(str, B)))
    print("ordenados juntos:", " ".join(map(str, sorted(A + B))))
    print(f"{'k':>2} {'A[k]':>5} {'B[n-1-k]':>9}  A[k] <= B[n-1-k]")
    for k in range(n):
        print(f"{k:>2} {A[k]:>5} {B[n - 1 - k]:>9}  {'sí' if A[k] <= B[n - 1 - k] else 'no'}")
    c = Comparador()
    i = split_point(A, B, c)
    print(f"i* = {i}: los n menores son A[0..{i - 1}] y B[0..{n - i - 1}]; "
          f"la búsqueda binaria usó {c.veces} comparaciones")
    c = Comparador()
    m = median(A, B, c)
    print(f"mediana = max(A[{i - 1}], B[{n - i - 1}]) = max({A[i - 1]}, {B[n - i - 1]}) "
          f"= {m}, con {c.veces} comparaciones en total; el oráculo dice {oraculo(A, B)}")


def invariante_vigilado():
    seccion("§3. El corte, vigilado con assert")
    rng = random.Random(3)
    casos = 0
    for _ in range(20_000):
        n = rng.randint(1, 30)
        A = sorted(rng.randrange(40) for _ in range(n))
        B = sorted(rng.randrange(40) for _ in range(n))
        c = [A[k] <= B[n - 1 - k] for k in range(n)]
        assert all(c[k] >= c[k + 1] for k in range(n - 1))      # verdaderos y después falsos
        i = split_point(A, B, Comparador())
        assert i == sum(c)
        # los n menores, con el desempate "A primero", son A[:i] y B[:n-i]
        orden = sorted([(v, 0, k) for k, v in enumerate(A)] + [(v, 1, k) for k, v in enumerate(B)])
        menores = orden[:n]
        assert sum(1 for _, lista, _ in menores if lista == 0) == i
        assert median(A, B, Comparador()) == oraculo(A, B)
        casos += 1
    print(f"{miles(casos)} pares de arreglos con repetidos: la condición es monótona, el "
          f"corte cuenta los elementos de A entre los n menores, y la mediana es correcta")


def interleavings(n):
    """Todas las maneras de intercalar n elementos de A con n de B, sin repetidos."""
    for posA in itertools.combinations(range(2 * n), n):
        s = set(posA)
        A = [p for p in range(2 * n) if p in s]
        B = [p for p in range(2 * n) if p not in s]
        yield A, B


def peor_del_algoritmo(n):
    peor = 0
    for A, B in interleavings(n):
        c = Comparador()
        assert median(A, B, c) == oraculo(A, B)
        peor = max(peor, c.veces)
    return peor


def peor_alternado(n):
    peor = 0
    for A, B in interleavings(n):
        c = Comparador()
        assert median_alternating(A, B, c) == oraculo(A, B)
        peor = max(peor, c.veces)
    return peor


def optimo(n):
    """El menor peor caso de CUALQUIER algoritmo que compare elementos de A con
    elementos de B (las comparaciones dentro de un mismo arreglo ya se saben)."""
    casos = list(interleavings(n))
    respuesta = []
    for A, B in casos:
        med = sorted(A + B)[n - 1]
        respuesta.append(("A", A.index(med)) if med in A else ("B", B.index(med)))
    preguntas = [(i, j) for i in range(n) for j in range(n)]

    @lru_cache(maxsize=None)
    def f(S):
        respuestas = {respuesta[k] for k in S}
        if len(respuestas) == 1:
            return 0
        cota = techo_log2(len(respuestas))
        mejor = math.inf
        for i, j in preguntas:
            si = frozenset(k for k in S if casos[k][0][i] < casos[k][1][j])
            if not si or si == S:
                continue
            no = S - si
            valor = 1 + max(f(si), f(no))
            if valor < mejor:
                mejor = valor
                if mejor == cota:
                    break
        return mejor

    return f(frozenset(range(len(casos))))


def comparaciones():
    seccion("§4 y §5. Comparaciones en el peor caso")
    filas = []
    print(f"{'n':>3} {'algoritmo':>10} {'ceil(log2(n+1)) + 1':>20} {'información':>12} "
          f"{'óptimo':>7} {'alternada':>10}")
    for n in range(1, 9):
        alg = peor_del_algoritmo(n)
        info = techo_log2(2 * n)
        opt = optimo(n) if n <= 5 else None
        alt = peor_alternado(n)
        filas.append((n, alg, info, opt, alt))
        print(f"{n:>3} {alg:>10} {techo_log2(n + 1) + 1:>20} {info:>12} "
              f"{'—' if opt is None else opt:>7} {alt:>10}")
    for n in [100, 1000, 10**6]:
        rng = random.Random(n)
        peor = 0
        repeticiones = 300 if n <= 1000 else 10
        # cortes al azar, más los dos extremos
        for i in [0, n] + [rng.randint(0, n) for _ in range(repeticiones)]:
            AA = [v * 4 for v in range(n)]
            BB = sorted([-4 * k - 1 for k in range(n - i)] + [4 * n + 4 * k for k in range(i)])
            c = Comparador()
            assert median(AA, BB, c) == oraculo(AA, BB)
            peor = max(peor, c.veces)
        print(f"{miles(n):>9}: peor medido {peor}, ceil(log2(n+1)) + 1 = "
              f"{techo_log2(n + 1) + 1}, información {techo_log2(2 * n)}")
    return filas


# --------------------------------------------------------------------------
# 3. El error plantado
# --------------------------------------------------------------------------

def errores_plantados():
    seccion("§7. El centinela que Python no tiene")
    rng = random.Random(7)

    def al_azar(nmin, nmax):
        n = rng.randint(nmin, nmax)
        return (sorted(rng.randrange(10**6) for _ in range(n)),
                sorted(rng.randrange(10**6) for _ in range(n)))

    def disjuntos():
        n = rng.randint(1, 50)
        bajos = sorted(rng.randrange(1000) for _ in range(n))
        altos = sorted(1000 + rng.randrange(1000) for _ in range(n))
        return (bajos, altos) if rng.random() < 0.5 else (altos, bajos)

    baterias = {
        "n de 10 a 50, al azar": [al_azar(10, 50) for _ in range(4000)],
        "n de 1 a 3, al azar": [al_azar(1, 3) for _ in range(4000)],
        "exhaustivo, n <= 4": [(A, B) for n in range(1, 5) for A, B in interleavings(n)],
        "rangos disjuntos": [disjuntos() for _ in range(4000)],
    }
    fallos = {}
    print(f"{'batería':>22} {'casos':>6} {'correcta':>9} {'con A[-1]':>10}")
    for nombre, casos in baterias.items():
        fila = []
        for bug in (False, True):
            malos = sum(median(A, B, Comparador(), bug) != oraculo(A, B) for A, B in casos)
            fila.append(100 * malos / len(casos))
        fallos[nombre] = fila
        print(f"{nombre:>22} {miles(len(casos)):>6} {fila[0]:>8.1f}% {fila[1]:>9.1f}%")
    extremos = sum(split_point(A, B, Comparador()) in (0, len(A))
                   for A, B in baterias["exhaustivo, n <= 4"])
    malos = sum(median(A, B, Comparador(), True) != oraculo(A, B)
                for A, B in baterias["exhaustivo, n <= 4"])
    print(f"en el exhaustivo, el corte cae en un extremo (i* = 0 o i* = n) en {extremos} "
          f"casos, y la versión con A[-1] falla en {malos}")
    for n in [5, 10, 20]:
        print(f"con n = {n}, al azar, el corte cae en un extremo con probabilidad "
              f"2 / C(2n, n) = {2 / math.comb(2 * n, n):.2e}")
    return fallos


# --------------------------------------------------------------------------
# 4. Pruebas
# --------------------------------------------------------------------------

def pruebas():
    seccion("Pruebas")
    comprobaciones = 0
    rng = random.Random(2026)

    # (a) contra el oráculo, con repetidos y valores de varios rangos
    for _ in range(30_000):
        n = rng.randint(1, 40)
        r = rng.choice([3, 30, 10**6])
        A = sorted(rng.randrange(r) for _ in range(n))
        B = sorted(rng.randrange(r) for _ in range(n))
        c = Comparador()
        assert median(A, B, c) == oraculo(A, B)
        assert c.veces <= techo_log2(n + 1) + 1
        c = Comparador()
        assert median_alternating(A, B, c) == oraculo(A, B)
        assert c.veces <= techo_log2(2 * n)
        comprobaciones += 1

    # (b) todos los intercalados para n <= 9
    for n in range(1, 10):
        for A, B in interleavings(n):
            assert median(A, B, Comparador()) == oraculo(A, B)
            comprobaciones += 1

    # (c) cada una de las 2n respuestas posibles aparece en algún intercalado
    for n in range(1, 9):
        vistas = set()
        for A, B in interleavings(n):
            med = sorted(A + B)[n - 1]
            vistas.add(("A", A.index(med)) if med in A else ("B", B.index(med)))
        assert len(vistas) == 2 * n
        comprobaciones += 1

    print(f"{miles(comprobaciones)} comprobaciones, 0 fallos")


# --------------------------------------------------------------------------
# 5. Figuras
# --------------------------------------------------------------------------

TINTA, APAGADO, REGLA = "#1a1a1a", "#6b7280", "#d8dce3"
ACENTO, OSCURO, CALIDO, ALARMA = "#0891b2", "#0e7490", "#b45309", "#be123c"


def _estilo():
    plt.rcParams.update({
        "font.size": 9, "axes.edgecolor": APAGADO, "axes.labelcolor": TINTA,
        "xtick.color": APAGADO, "ytick.color": APAGADO,
        "figure.facecolor": "white", "svg.hashsalt": "ejercicio-07",
    })


def _guardar(fig, nombre):
    fig.tight_layout()
    fig.savefig(nombre, metadata={"Date": None})
    plt.close(fig)


def figura_corte():
    A, B, n = EJ_A, EJ_B, len(EJ_A)
    i = split_point(A, B, Comparador())
    j = n - i
    med = oraculo(A, B)
    fig, ax = plt.subplots(figsize=(6.6, 2.4))
    for fila, (nombre, X, k, y) in enumerate([("A", A, i, 1.2), ("B", B, j, 0)]):
        ax.text(-0.7, y + 0.4, nombre, ha="center", va="center", fontsize=10, color=TINTA)
        for p, v in enumerate(X):
            dentro = p < k
            color = ALARMA if v == med else (OSCURO if dentro else APAGADO)
            ax.add_patch(plt.Rectangle((p, y), 0.9, 0.8,
                                       facecolor="#ecfeff" if dentro else "white",
                                       edgecolor=color, lw=1.6 if v == med else 0.9))
            ax.text(p + 0.45, y + 0.4, str(v), ha="center", va="center", fontsize=9,
                    color=color)
        ax.plot([k - 0.05, k - 0.05], [y - 0.1, y + 0.9], color=CALIDO, lw=2)
    ax.annotate("", (j + 0.45, 0.8), (i - 1 + 0.45, 1.2),
                arrowprops={"arrowstyle": "->", "color": CALIDO, "lw": 1})
    ax.text(n + 0.2, 1.6, f"i* = {i}: A[{i - 1}] = {A[i - 1]} ≤ B[{j}] = {B[j]}",
            fontsize=8, color=CALIDO)
    ax.text(n + 0.2, 0.4, f"n - i* = {j}: B[{j - 1}] = {B[j - 1]} < A[{i}] = {A[i]}",
            fontsize=8, color=CALIDO)
    ax.set_xlim(-1.1, n + 5.2)
    ax.set_ylim(-0.3, 2.2)
    ax.set_aspect("equal")
    ax.axis("off")
    _guardar(fig, "ejercicio-07-corte.svg")


def figura_comparaciones(filas):
    fig, ax = plt.subplots(figsize=(6.4, 2.9))
    ns = [f[0] for f in filas]
    ax.plot(ns, [f[1] for f in filas], "o-", color=OSCURO, lw=1.6, label="este algoritmo")
    ax.plot(ns, [f[2] for f in filas], "s--", color=CALIDO, lw=1.2,
            label="cota de información ⌈log₂ 2n⌉")
    opt = [(f[0], f[3]) for f in filas if f[3] is not None]
    ax.plot([a for a, _ in opt], [b for _, b in opt], "x", color=ALARMA, ms=9, mew=2,
            label="óptimo por fuerza bruta")
    ax.set_xlabel("n")
    ax.set_ylabel("comparaciones en el peor caso")
    ax.set_yticks(range(1, 6))
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(color=REGLA, lw=0.6)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    _guardar(fig, "ejercicio-07-comparaciones.svg")


def figura_errores(fallos):
    fig, ax = plt.subplots(figsize=(6.6, 2.9))
    nombres = list(fallos)
    ancho = 0.36
    for k, (etiqueta, color) in enumerate([("correcta", OSCURO), ("con A[-1]", ALARMA)]):
        alturas = [fallos[b][k] for b in nombres]
        pos = [i + (k - 0.5) * ancho for i in range(len(nombres))]
        ax.bar(pos, alturas, ancho, color=color, label=etiqueta)
        for xx, h in zip(pos, alturas):
            ax.text(xx, h + 1.5, f"{h:.1f}", ha="center", fontsize=7, color=color)
    ax.set_xticks(range(len(nombres)))
    ax.set_xticklabels(nombres, fontsize=8)
    ax.set_ylabel("% de medianas mal")
    ax.set_ylim(0, 112)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color=REGLA, lw=0.6)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    _guardar(fig, "ejercicio-07-errores.svg")


if __name__ == "__main__":
    ejemplo_chico()
    invariante_vigilado()
    filas = comparaciones()
    fallos = errores_plantados()
    pruebas()
    _estilo()
    figura_corte()
    figura_comparaciones(filas)
    figura_errores(fallos)
    print("\nfiguras: ejercicio-07-corte.svg, ejercicio-07-comparaciones.svg, "
          "ejercicio-07-errores.svg")
