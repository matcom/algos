"""Ejercicio 10 del Tema 1: par más cercano en una dimensión.

Tres algoritmos (fuerza bruta, ordenar y recorrer, rejilla aleatoria), la
verificación experimental del argumento de la cota mínima y las mediciones de
la rejilla.

Uso:
    python ejercicio_10.py             imprime las tablas rápidas del informe
    python ejercicio_10.py --figuras   además corre los experimentos largos y regenera las figuras

Las pruebas están en test_ejercicio_10.py.

Las coordenadas son enteros (o fracciones exactas), como en la word RAM: así la
celda x // δ se calcula sin error de redondeo.
"""

import itertools
import math
import random
import sys
import time
from pathlib import Path


# ---------------------------------------------------------------------------
# 1. Fuerza bruta: el oráculo
# ---------------------------------------------------------------------------

def fuerza_bruta(xs):
    """Mira los n(n-1)/2 pares. Devuelve (δ, (i, j)) con i < j índices de la entrada."""
    mejor = None
    for i, j in itertools.combinations(range(len(xs)), 2):
        d = abs(xs[i] - xs[j])
        if mejor is None or d < mejor[0]:
            mejor = (d, (i, j))
    return mejor


# ---------------------------------------------------------------------------
# 2. Ordenar y recorrer (conferencia 2, §3)
# ---------------------------------------------------------------------------

class Pruebas:
    """Registra las pruebas de signo que hace un algoritmo: es su camino en el árbol."""

    def __init__(self):
        self.camino = []

    def signo(self, valor):
        s = (valor > 0) - (valor < 0)
        self.camino.append(s)
        return s


def _ordenar_por_mezcla(indices, xs, pruebas):
    if len(indices) <= 1:
        return list(indices)
    medio = len(indices) // 2
    izq = _ordenar_por_mezcla(indices[:medio], xs, pruebas)
    der = _ordenar_por_mezcla(indices[medio:], xs, pruebas)
    res = []
    i = j = 0
    while i < len(izq) and j < len(der):
        if pruebas.signo(xs[izq[i]] - xs[der[j]]) <= 0:   # prueba lineal: x_a - x_b
            res.append(izq[i])
            i += 1
        else:
            res.append(der[j])
            j += 1
    return res + izq[i:] + der[j:]


def ordenar_y_recorrer(xs, pruebas=None):
    """Ordena por mezcla y mira los n-1 huecos consecutivos.

    Todas las pruebas son signos de funciones lineales de la entrada, así que el
    algoritmo es un árbol de decisión lineal. Devuelve (δ, (i, j)) con i < j.
    """
    if pruebas is None:
        pruebas = Pruebas()
    orden = _ordenar_por_mezcla(list(range(len(xs))), xs, pruebas)
    mejor = (xs[orden[1]] - xs[orden[0]], 0)
    for k in range(1, len(orden) - 1):
        hueco = xs[orden[k + 1]] - xs[orden[k]]
        # prueba lineal: (x_c - x_d) - (x_a - x_b)
        if pruebas.signo(hueco - mejor[0]) < 0:
            mejor = (hueco, k)
    k = mejor[1]
    i, j = sorted((orden[k], orden[k + 1]))
    return mejor[0], (i, j)


def distintos_por_reduccion(xs, pruebas=None):
    """Distinción de elementos con el par más cercano y una prueba más (la reducción)."""
    if pruebas is None:
        pruebas = Pruebas()
    _, (i, j) = ordenar_y_recorrer(xs, pruebas)
    return pruebas.signo(xs[i] - xs[j]) != 0


def ordenar_y_recorrer_rapido(xs):
    """El mismo algoritmo con el sorted de Python (en C), para medir tiempos."""
    orden = sorted(range(len(xs)), key=xs.__getitem__)
    k = min(range(len(xs) - 1), key=lambda k: xs[orden[k + 1]] - xs[orden[k]])
    return xs[orden[k + 1]] - xs[orden[k]], tuple(sorted((orden[k], orden[k + 1])))


# ---------------------------------------------------------------------------
# 3. La rejilla aleatoria, adaptada a una dimensión
# ---------------------------------------------------------------------------

def rejilla_1d(xs, semilla=0, barajar=True, vigilar=False, orden=None):
    """Inserción incremental en una rejilla de celdas de largo δ (conferencia 2, §9, en 1D).

    La celda del punto x es x // δ. Cada celda guarda a lo sumo un índice, y para
    un punto nuevo basta mirar su celda y las dos vecinas. Devuelve
    (δ, (i, j), estadísticas) con i < j índices de la entrada.

    El orden de inserción es una permutación al azar (o la identidad si
    barajar=False, o el que se pase en `orden`). Con vigilar=True comprueba los
    dos invariantes después de cada inserción (cuesta O(n²); solo para las pruebas).
    """
    n = len(xs)
    if orden is None:
        orden = list(range(n))
        if barajar:
            random.Random(semilla).shuffle(orden)
    est = {"reconstrucciones": 0, "reinserciones": 0, "consultas": 0, "inserciones": 2}

    a, b = orden[0], orden[1]
    delta, par = abs(xs[a] - xs[b]), (a, b)
    if delta == 0:
        return 0, tuple(sorted(par)), est
    rejilla = {xs[a] // delta: a, xs[b] // delta: b}

    for t in range(2, n):
        i = orden[t]
        c = xs[i] // delta
        antes = delta
        for d in (-1, 0, 1):                       # las tres celdas
            est["consultas"] += 1
            j = rejilla.get(c + d)
            if j is not None and abs(xs[i] - xs[j]) < delta:
                delta, par = abs(xs[i] - xs[j]), (j, i)
        if delta == 0:                             # hay repetidos: no se puede bajar más
            return 0, tuple(sorted(par)), est
        if delta < antes:                          # δ bajó: la rejilla vieja no sirve
            est["reconstrucciones"] += 1
            est["reinserciones"] += t + 1
            rejilla = {}
            for k in orden[:t + 1]:
                assert xs[k] // delta not in rejilla  # lema: un punto por celda
                rejilla[xs[k] // delta] = k
        else:
            assert c not in rejilla                   # lema: la celda de x estaba vacía
            rejilla[c] = i
            est["inserciones"] += 1
        if vigilar:
            insertados = orden[:t + 1]
            assert delta == fuerza_bruta([xs[k] for k in insertados])[0]
            assert sorted(rejilla.values()) == sorted(insertados)
            assert all(xs[k] // delta == celda for celda, k in rejilla.items())
    return delta, tuple(sorted(par)), est


# ---------------------------------------------------------------------------
# 4. Entradas
# ---------------------------------------------------------------------------

def al_azar(n, semilla, rango=10**12):
    """n enteros distintos al azar en [0, rango)."""
    return random.Random(semilla).sample(range(rango), n)


def huecos_decrecientes(n):
    """Insertados en orden, cada punto nuevo crea un hueco menor que todos los anteriores."""
    xs = [0]
    for k in range(1, n):
        xs.append(xs[-1] + (n - k))
    return xs


def armonico(n):
    return sum(1 / k for k in range(1, n + 1))


def reconstrucciones_esperadas(n):
    """2·H_n - 3: la esperanza exacta cuando el par más cercano es único."""
    return 2 * armonico(n) - 3


def log3_factorial(n):
    return math.lgamma(n + 1) / math.log(3)


# ---------------------------------------------------------------------------
# 5. Tablas del informe
# ---------------------------------------------------------------------------

def tabla_caminos(n_max=7):
    print("Tabla 1. Los n! órdenes llegan a hojas distintas (distinción por la reducción)")
    print(f"{'n':>3} {'n!':>6} {'caminos distintos':>18} {'todos dicen no':>15}"
          f" {'profundidad':>12} {'⌈log3 n!⌉':>10}")
    for n in range(2, n_max + 1):
        caminos = set()
        todos_no = True
        profundidad = 0
        for perm in itertools.permutations(range(1, n + 1)):
            pruebas = Pruebas()
            todos_no &= distintos_por_reduccion(list(perm), pruebas)
            caminos.add(tuple(pruebas.camino))
            profundidad = max(profundidad, len(pruebas.camino))
        print(f"{n:>3} {math.factorial(n):>6} {len(caminos):>18} {str(todos_no):>15}"
              f" {profundidad:>12} {math.ceil(log3_factorial(n) - 1e-9):>10}")
    print()


def tabla_cotas():
    print("Tabla 2. Pruebas del algoritmo de ordenar contra la cota del árbol lineal")
    print(f"{'n':>8} {'⌈log3 n!⌉ - 1':>14} {'⌈log2 n!⌉':>10} {'pruebas (al azar)':>18} {'cociente':>9}")
    for n in [8, 64, 512, 4096, 32768]:
        cota = math.ceil(log3_factorial(n)) - 1
        pruebas = Pruebas()
        ordenar_y_recorrer(al_azar(n, n), pruebas)
        print(f"{n:>8} {cota:>14,} {math.ceil(math.lgamma(n + 1) / math.log(2)):>10,}"
              f" {len(pruebas.camino):>18,} {len(pruebas.camino) / cota:>9.3f}")
    print()


def tabla_adversaria():
    print("Tabla 3. La entrada de huecos decrecientes, con y sin barajar")
    print(f"{'n':>6} {'sin barajar':>12} {'n - 2':>7} {'reinserciones':>14}"
          f" {'barajada (media de 200)':>24} {'2H_n - 3':>9}")
    for n in [100, 1000, 3000]:
        xs = huecos_decrecientes(n)
        _, _, est = rejilla_1d(xs, barajar=False)
        medias = [rejilla_1d(xs, semilla=s)[2]["reconstrucciones"] for s in range(200)]
        print(f"{n:>6} {est['reconstrucciones']:>12} {n - 2:>7} {est['reinserciones']:>14,}"
              f" {sum(medias) / len(medias):>24.2f} {reconstrucciones_esperadas(n):>9.2f}")
    print()


def experimento_reconstrucciones():
    """Media de reconstrucciones y reinserciones con entradas al azar."""
    filas = []
    for n, semillas in [(10, 4000), (100, 2000), (1000, 1000), (10**4, 200), (10**5, 40)]:
        rec, rein = [], []
        for s in range(semillas):
            _, _, est = rejilla_1d(al_azar(n, 10**6 + s), semilla=s)
            rec.append(est["reconstrucciones"])
            rein.append(est["reinserciones"])
        media = sum(rec) / semillas
        error = (sum((r - media) ** 2 for r in rec) / (semillas - 1)) ** 0.5 / semillas**0.5
        filas.append((n, semillas, media, error, sum(rein) / semillas))
    return filas


def tabla_reconstrucciones(filas):
    print("Tabla 4. Reconstrucciones con entradas al azar (barajadas)")
    print(f"{'n':>7} {'corridas':>9} {'media':>8} {'± error':>8} {'2H_n - 3':>9} {'2 ln n':>7}"
          f" {'reinserciones/(n-2)':>20}")
    for n, semillas, media, error, rein in filas:
        print(f"{n:>7} {semillas:>9} {media:>8.3f} {error:>8.3f} {reconstrucciones_esperadas(n):>9.3f}"
              f" {2 * math.log(n):>7.2f} {rein / (n - 2):>20.3f}")
    print()


def experimento_operaciones():
    """Operaciones por punto: pruebas del ordenamiento contra accesos a la rejilla.

    Los accesos de la rejilla son la media de 5 barajados: una corrida suelta
    depende de cuándo cayeron las reconstrucciones.
    """
    filas = []
    for e in range(8, 18):
        n = 2**e
        xs = al_azar(n, e)
        pruebas = Pruebas()
        ordenar_y_recorrer(xs, pruebas)
        accesos = 0
        for s in range(5):
            _, _, est = rejilla_1d(xs, semilla=s)
            accesos += est["consultas"] + est["inserciones"] + est["reinserciones"]
        filas.append((n, len(pruebas.camino) / n, accesos / 5 / n))
    return filas


def tabla_operaciones(filas):
    print("Tabla 5. Operaciones por punto")
    print(f"{'n':>8} {'ordenar: pruebas/n':>19} {'rejilla: accesos/n':>19}")
    for n, ordenar, rejilla in filas:
        print(f"{n:>8} {ordenar:>19.2f} {rejilla:>19.2f}")
    print()


def tabla_tiempos():
    print("Tabla 6. Tiempos en Python (sorted está en C; la rejilla, en Python puro)")
    print(f"{'n':>9} {'sorted + recorrer':>18} {'rejilla':>9}")
    for n in [10**4, 10**5, 10**6]:
        xs = al_azar(n, 7)
        inicio = time.perf_counter()
        ordenar_y_recorrer_rapido(xs)
        t1 = time.perf_counter() - inicio
        inicio = time.perf_counter()
        rejilla_1d(xs, semilla=7)
        t2 = time.perf_counter() - inicio
        print(f"{n:>9,} {t1:>17.3f}s {t2:>8.3f}s")
    print()


# ---------------------------------------------------------------------------
# 6. Figuras
# ---------------------------------------------------------------------------

AZUL, NARANJA, AQUA, AMARILLO = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
ROJO = "#e34948"
TINTA, TINTA_2, TENUE, REJILLA, SUPERFICIE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"


def _estilo(plt):
    plt.rcParams.update({
        "font.family": ["Segoe UI", "DejaVu Sans"],
        "font.size": 10,
        "axes.edgecolor": "#c3c2b7",
        "axes.labelcolor": TINTA_2,
        "axes.titlecolor": TINTA,
        "axes.titlesize": 12,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.facecolor": SUPERFICIE,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": REJILLA,
        "grid.linewidth": 0.6,
        "xtick.color": TENUE,
        "ytick.color": TENUE,
        "xtick.labelcolor": TINTA_2,
        "ytick.labelcolor": TINTA_2,
        "figure.facecolor": SUPERFICIE,
        "legend.frameon": False,
        "legend.labelcolor": TINTA_2,
        "lines.linewidth": 2,
        "savefig.dpi": 150,
        "savefig.bbox": "tight",
    })


def _proyectar(x):
    """Proyección de R³ al plano x1 + x2 + x3 = 0, en una base ortonormal."""
    u = (1 / math.sqrt(2), -1 / math.sqrt(2), 0)
    v = (1 / math.sqrt(6), 1 / math.sqrt(6), -2 / math.sqrt(6))
    return sum(a * b for a, b in zip(x, u)), sum(a * b for a, b in zip(x, v))


def _desproyectar(px, py):
    u = (1 / math.sqrt(2), -1 / math.sqrt(2), 0)
    v = (1 / math.sqrt(6), 1 / math.sqrt(6), -2 / math.sqrt(6))
    return tuple(px * a + py * b for a, b in zip(u, v))


def figura_camaras(plt, destino):
    fig, ax = plt.subplots(figsize=(6.4, 6.4))
    ax.set_aspect("equal")
    ax.axis("off")
    r = 1.0
    # Las tres rectas x_i = x_j (planos de repetidos cortados con x1 + x2 + x3 = 0).
    for i, j, nombre in [(0, 1, "x₁ = x₂"), (0, 2, "x₁ = x₃"), (1, 2, "x₂ = x₃")]:
        d = [0, 0, 0]
        k = 3 - i - j
        d[i] = d[j] = 1
        d[k] = -2
        px, py = _proyectar(d)
        norma = math.hypot(px, py)
        px, py = px / norma, py / norma
        ax.plot([-r * px, r * px], [-r * py, r * py], color=TINTA_2, linewidth=1.4)
        ax.text(1.08 * r * px, 1.08 * r * py, nombre, color=TINTA_2, fontsize=10,
                ha="center", va="center")
    # Etiquetas de las seis cámaras.
    for s in range(6):
        ang = math.radians(60 * s)
        x = _desproyectar(math.cos(ang), math.sin(ang))
        orden = sorted(range(3), key=lambda k: x[k])
        etiqueta = " < ".join(f"x{'₁₂₃'[k]}" for k in orden)
        ax.text(0.78 * r * math.cos(ang), 0.78 * r * math.sin(ang), etiqueta, color=TINTA,
                fontsize=10, ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.25", fc=SUPERFICIE, ec="none"))
    # El segmento entre dos entradas con órdenes distintos, en el centro de sus cámaras.
    p = (0.45 * math.cos(math.radians(0)), 0.45 * math.sin(math.radians(0)))
    q = (0.45 * math.cos(math.radians(120)), 0.45 * math.sin(math.radians(120)))
    ax.plot([p[0], q[0]], [p[1], q[1]], color=AZUL, linewidth=2.2)
    for punto, nombre, (dx, dy) in [(p, "p", (0.04, -0.07)), (q, "q", (-0.1, 0.03))]:
        ax.plot(*punto, "o", color=AZUL, markersize=9, markeredgecolor=SUPERFICIE,
                markeredgewidth=2)
        ax.text(punto[0] + dx, punto[1] + dy, nombre, color=AZUL, fontsize=12,
                fontweight="bold")
    # Dónde cruza: el primer t con z_i = z_j.
    P, Q = _desproyectar(*p), _desproyectar(*q)
    cruces = []
    for i, j in [(0, 1), (0, 2), (1, 2)]:
        a, b = P[i] - P[j], Q[i] - Q[j]
        if a * b < 0:
            t = a / (a - b)
            cruces.append((t, i, j))
    for t, i, j in cruces:
        z = (p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1]))
        ax.plot(*z, "o", color=ROJO, markersize=8, markeredgecolor=SUPERFICIE,
                markeredgewidth=2)
    t, i, j = min(cruces)
    z = (p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1]))
    ax.text(z[0] + 0.04, z[1] + 0.05, "z", color=ROJO, fontsize=12, fontweight="bold")
    ax.text(0, -1.22, f"En z vale z{'₁₂₃'[i]} = z{'₁₂₃'[j]}: la respuesta correcta es \"hay repetidos\".\n"
            "Pero z está en el segmento entre p y q, y si p y q llegan a la misma hoja,\n"
            "la región de esa hoja es convexa y contiene a z: el árbol diría \"no hay\".",
            color=TINTA, fontsize=9, ha="center", va="center")
    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-1.45, 1.25)
    ax.set_title("Los 3! órdenes son regiones separadas por los planos xᵢ = xⱼ")
    fig.savefig(destino / "ejercicio-10-camaras.png")
    plt.close(fig)


def figura_rejilla(plt, destino):
    delta = 1.0
    puntos = [0.35, 1.8, 3.1, 4.55, 6.3, 7.9]
    nuevo = 2.45
    fig, ax = plt.subplots(figsize=(8.4, 2.6))
    ax.axis("off")
    for k in range(0, 9):
        ax.plot([k * delta, k * delta], [-0.18, 0.18], color=TENUE, linewidth=1)
    ax.plot([0, 9 * delta], [0, 0], color="#c3c2b7", linewidth=1.2)
    c = int(nuevo // delta)
    ax.axvspan((c - 1) * delta, (c + 2) * delta, ymin=0.32, ymax=0.68, color=AZUL, alpha=0.10,
               linewidth=0)
    for k in range(0, 9):
        ax.text(k * delta + delta / 2, -0.36, f"celda {k}", color=TINTA_2, fontsize=8,
                ha="center")
    for x in puntos:
        ax.plot(x, 0, "o", color=TINTA_2, markersize=8, markeredgecolor=SUPERFICIE,
                markeredgewidth=1.5)
    ax.plot(nuevo, 0, "o", color=AZUL, markersize=10, markeredgecolor=SUPERFICIE,
            markeredgewidth=2)
    ax.text(nuevo, 0.26, "x nuevo", color=AZUL, fontsize=10, ha="center", fontweight="bold")
    ax.annotate("", xy=(nuevo - delta, 0.5), xytext=(nuevo + delta, 0.5),
                arrowprops=dict(arrowstyle="<->", color=NARANJA, linewidth=1.6))
    ax.text(nuevo, 0.6, "(x − δ, x + δ): lo que puede mejorar a δ", color=NARANJA, fontsize=9,
            ha="center")
    ax.text((c + 0.5) * delta, -0.62, "las tres celdas que se miran", color=AZUL, fontsize=9,
            ha="center")
    ax.annotate("", xy=(0, -0.8), xytext=(delta, -0.8),
                arrowprops=dict(arrowstyle="<->", color=TINTA_2, linewidth=1))
    ax.text(delta / 2, -0.95, "δ", color=TINTA_2, fontsize=10, ha="center")
    ax.set_xlim(-0.2, 9.2)
    ax.set_ylim(-1.05, 0.8)
    ax.set_title("Rejilla en una dimensión: celdas de largo δ, a lo sumo un punto por celda")
    fig.savefig(destino / "ejercicio-10-rejilla.png")
    plt.close(fig)


def figura_reconstrucciones(plt, destino, filas):
    fig, ax = plt.subplots(figsize=(8, 4.4))
    ns = [10 ** (e / 10) for e in range(10, 51)]
    ax.plot(ns, [reconstrucciones_esperadas(round(n)) for n in ns], color=AZUL,
            label="2Hₙ − 3 (esperanza exacta, demostrada)")
    ax.plot(ns, [2 * math.log(n) for n in ns], color=TENUE, linestyle=(0, (4, 3)), linewidth=1.4,
            label="2 ln n (la aproximación de la conferencia)")
    xs = [n for n, *_ in filas]
    ys = [media for _, _, media, _, _ in filas]
    errores = [error for _, _, _, error, _ in filas]
    ax.errorbar(xs, ys, yerr=errores, fmt="o", color=NARANJA, markersize=7,
                markeredgecolor=SUPERFICIE, markeredgewidth=1.5, capsize=3,
                label="medido (media sobre muchas semillas)")
    ax.set_xscale("log")
    ax.set_xlabel("n")
    ax.set_ylabel("reconstrucciones de la rejilla")
    ax.set_title("Reconstrucciones esperadas: la cuenta exacta contra lo medido")
    ax.legend(loc="upper left")
    fig.savefig(destino / "ejercicio-10-reconstrucciones.png")
    plt.close(fig)


def figura_operaciones(plt, destino, filas):
    fig, ax = plt.subplots(figsize=(8, 4.4))
    ns = [n for n, *_ in filas]
    ax.plot(ns, [o for _, o, _ in filas], "o-", color=NARANJA, markersize=6,
            markeredgecolor=SUPERFICIE, markeredgewidth=1.5,
            label="ordenar y recorrer: pruebas de signo por punto")
    ax.plot(ns, [r for _, _, r in filas], "o-", color=AZUL, markersize=6,
            markeredgecolor=SUPERFICIE, markeredgewidth=1.5,
            label="rejilla: accesos a la tabla hash por punto")
    ax.plot(ns, [log3_factorial(n) / n for n in ns], color=TENUE, linestyle=(0, (4, 3)),
            linewidth=1.4, label="cota del árbol lineal: log₃(n!)/n")
    ax.set_xscale("log", base=2)
    ax.set_ylim(0, 20)
    ax.set_xlabel("n")
    ax.set_ylabel("operaciones por punto")
    ax.set_title("Por punto: el árbol de decisión crece como log n; la rejilla, no")
    ax.legend(loc="upper left")
    fig.savefig(destino / "ejercicio-10-operaciones.png")
    plt.close(fig)


def figuras(filas_reconstrucciones, filas_operaciones):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    _estilo(plt)
    destino = Path(__file__).resolve().parent.parent / "figuras"
    destino.mkdir(exist_ok=True)
    figura_camaras(plt, destino)
    figura_rejilla(plt, destino)
    figura_reconstrucciones(plt, destino, filas_reconstrucciones)
    figura_operaciones(plt, destino, filas_operaciones)
    print(f"figuras escritas en {destino}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # la consola de Windows no es UTF-8
    tabla_caminos()
    tabla_cotas()
    tabla_adversaria()
    if "--figuras" in sys.argv:
        filas_r = experimento_reconstrucciones()
        tabla_reconstrucciones(filas_r)
        filas_o = experimento_operaciones()
        tabla_operaciones(filas_o)
        tabla_tiempos()
        figuras(filas_r, filas_o)
