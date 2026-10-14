"""Ejercicio 2 del Tema 1: invariante, potencial y cota de información de la búsqueda binaria.

Uso:
    python ejercicio_02.py             imprime las tablas del informe
    python ejercicio_02.py --figuras   además regenera las figuras

Las pruebas están en test_ejercicio_02.py.
"""

import math
import random
import sys
from pathlib import Path


class SinTerminar(Exception):
    """La búsqueda superó el límite de vueltas: el potencial dejó de bajar."""


def comparar(x, y):
    return (x > y) - (x < y)


def busqueda_binaria(A, x, camino=None, vigilar=False, variante="correcta", limite=None):
    """Busca x en el arreglo ordenado A con comparaciones de tres salidas.

    Devuelve ("está", m) con A[m] == x, o ("hueco", lo): x no está y va entre
    A[lo - 1] y A[lo]. Si se pasa una lista `camino`, anota cada respuesta
    (-1, 0 o 1), que es el camino en el árbol de decisión.

    `variante` planta los dos errores del informe:
      "lo = m"     rompe el potencial (puede no terminar);
      "hi = m - 1" rompe el invariante (puede perder a x).
    """
    lo, hi = 0, len(A)
    vueltas = 0
    while lo < hi:
        if vigilar:
            assert 0 <= lo <= hi <= len(A)
            assert all(A[k] < x for k in range(lo)), "falla la mitad izquierda del invariante"
            assert all(A[k] > x for k in range(hi, len(A))), "falla la mitad derecha"
        vueltas += 1
        if limite is not None and vueltas > limite:
            raise SinTerminar((lo, hi))
        m = (lo + hi) // 2
        r = comparar(x, A[m])
        if camino is not None:
            camino.append(r)
        if r == 0:
            return ("está", m)
        if r < 0:
            hi = m - 1 if variante == "hi = m - 1" else m
        else:
            lo = m if variante == "lo = m" else m + 1
    return ("hueco", lo)


def bits(k):
    return k.bit_length()


def potenciales(A, x):
    """Los valores de Φ = hi - lo y Ψ = bits(hi - lo) al empezar cada vuelta."""
    lo, hi = 0, len(A)
    fi, psi = [], []
    while lo < hi:
        fi.append(hi - lo)
        psi.append(bits(hi - lo))
        m = (lo + hi) // 2
        r = comparar(x, A[m])
        if r == 0:
            break
        if r < 0:
            hi = m
        else:
            lo = m + 1
    return fi, psi


def cota_informacion(n):
    """⌈log2(n + 1)⌉: hojas para los n + 1 huecos en un árbol binario."""
    return bits(n)  # ⌈log2(n+1)⌉ = ⌊log2 n⌋ + 1 = bits(n)


def peor_caso(n):
    """Máximo de comparaciones sobre todo x: los n elementos y un valor en cada hueco."""
    A = list(range(2, 2 * n + 1, 2))
    peor = 0
    for x in range(1, 2 * n + 2):
        camino = []
        busqueda_binaria(A, x, camino)
        peor = max(peor, len(camino))
    return peor


def caminos_de_los_huecos(n):
    """El camino de un valor en cada uno de los n + 1 huecos."""
    A = list(range(2, 2 * n + 1, 2))
    caminos = []
    for x in range(1, 2 * n + 2, 2):
        camino = []
        busqueda_binaria(A, x, camino)
        caminos.append(tuple(camino))
    return caminos


# ---------------------------------------------------------------------------
# Pruebas al azar contra los errores plantados
# ---------------------------------------------------------------------------

def generar(nombre, rng):
    n = rng.randint(1, 30)
    if nombre == "distintos, x presente":
        A = sorted(rng.sample(range(1000), n))
        return A, rng.choice(A)
    if nombre == "distintos, x ausente":
        A = sorted(rng.sample(range(0, 2000, 2), n))
        return A, rng.randrange(1, 2001, 2)
    if nombre == "distintos, x cualquiera":
        A = sorted(rng.sample(range(1000), n))
        return A, rng.randrange(-5, 1005)
    if nombre == "con repetidos, x cualquiera":
        A = sorted(rng.randrange(10) for _ in range(n))
        return A, rng.randrange(-1, 11)
    raise ValueError(nombre)


GENERADORES = ["distintos, x presente", "distintos, x ausente", "distintos, x cualquiera",
               "con repetidos, x cualquiera"]


def respuesta_correcta(A, x):
    return x in A


def falla(A, x, variante, mirar_hueco):
    """True si la variante se equivoca (o no termina) en (A, x)."""
    try:
        res = busqueda_binaria(A, x, variante=variante, limite=4 * len(A) + 4)
    except SinTerminar:
        return True
    if res[0] == "está":
        return A[res[1]] != x
    if x in A:
        return True
    if mirar_hueco:
        lo = res[1]
        return not ((lo == 0 or A[lo - 1] < x) and (lo == len(A) or A[lo] > x))
    return False


def tasas_de_fallo(casos=4000, semilla=2):
    rng = random.Random(semilla)
    filas = []
    for nombre in GENERADORES:
        entradas = [generar(nombre, rng) for _ in range(casos)]
        fila = [nombre]
        for variante, mirar_hueco in [("lo = m", False), ("hi = m - 1", False), ("hi = m - 1", True)]:
            fila.append(100 * sum(falla(A, x, variante, mirar_hueco) for A, x in entradas) / casos)
        filas.append(fila)
    return filas


# ---------------------------------------------------------------------------
# Tablas
# ---------------------------------------------------------------------------

def tabla_peor_caso():
    print("Tabla 1. Peor caso medido contra la cota de información ⌈log2(n+1)⌉")
    distintos = [n for n in range(1, 1025) if peor_caso(n) != cota_informacion(n)]
    print(f"n = 1..1024: casos donde difieren: {len(distintos)}")
    for n in [1, 2, 3, 7, 8, 100, 1000, 1023, 1024]:
        print(f"  n = {n:>5}  peor caso {peor_caso(n):>3}  cota {cota_informacion(n):>3}")
    print()


def tabla_caminos():
    print("Tabla 2. Los n + 1 huecos van a hojas distintas y sin respuestas '='")
    for n in [1, 3, 7, 10, 100]:
        caminos = caminos_de_los_huecos(n)
        print(f"  n = {n:>3}: {len(caminos)} huecos, {len(set(caminos))} caminos distintos,"
              f" con '=': {sum(0 in c for c in caminos)}, profundidad máx {max(map(len, caminos))}")
    print()


def tabla_traza():
    A = [3, 8, 12, 15, 21, 24, 30, 33, 37, 41, 46, 52, 58, 63, 70]
    x = 40
    print(f"Tabla 3. Traza con A = {A}, x = {x}")
    lo, hi = 0, len(A)
    vuelta = 0
    while lo < hi:
        m = (lo + hi) // 2
        r = comparar(x, A[m])
        print(f"  vuelta {vuelta}: lo={lo:>2} hi={hi:>2} Φ={hi - lo:>2} Ψ={bits(hi - lo)}"
              f"  m={m:>2} A[m]={A[m]:>2}  x {'<' if r < 0 else '>' if r > 0 else '='} A[m]")
        if r == 0:
            break
        if r < 0:
            hi = m
        else:
            lo = m + 1
        vuelta += 1
    print(f"  final: lo={lo} hi={hi}, resultado {busqueda_binaria(A, x)}")
    print()


def tabla_fallos(filas):
    print("Tabla 4. Porcentaje de fallos de los errores plantados, 4000 casos por generador")
    print(f"{'generador':>28} {'lo = m':>8} {'hi = m-1':>9} {'hi = m-1 (+hueco)':>18}")
    for nombre, a, b, c in filas:
        print(f"{nombre:>28} {a:>7.1f}% {b:>8.1f}% {c:>17.1f}%")
    print()


# ---------------------------------------------------------------------------
# Figuras
# ---------------------------------------------------------------------------

AZUL, NARANJA, AQUA, AMARILLO = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
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


def figura_invariante(plt, destino):
    import matplotlib.patches as patches

    A = [3, 8, 12, 15, 21, 24, 30, 33, 37, 41, 46, 52, 58, 63, 70]
    x = 40
    estados = []
    lo, hi = 0, len(A)
    while True:
        m = (lo + hi) // 2 if lo < hi else None
        estados.append((lo, hi, m))
        if lo >= hi:
            break
        r = comparar(x, A[m])
        if r < 0:
            hi = m
        else:
            lo = m + 1
    fig, ax = plt.subplots(figsize=(8.6, 0.75 * len(estados) + 1.0))
    ax.axis("off")
    for fila, (lo, hi, m) in enumerate(estados):
        y = -fila
        for k, v in enumerate(A):
            if k < lo:
                color, texto = "#d6efe5", TINTA_2
            elif k >= hi:
                color, texto = "#fbe0d4", TINTA_2
            else:
                color, texto = SUPERFICIE, TINTA
            borde = AZUL if k == m else "#c3c2b7"
            ax.add_patch(patches.Rectangle((k, y - 0.32), 0.92, 0.64, facecolor=color,
                                           edgecolor=borde, linewidth=2 if k == m else 0.8))
            ax.text(k + 0.46, y, str(v), ha="center", va="center", fontsize=9, color=texto)
        etiqueta = f"lo={lo}, hi={hi}" + (f", m={m}" if m is not None else ": lo = hi, x va aquí")
        ax.text(len(A) + 0.3, y, etiqueta, va="center", fontsize=9, color=TINTA_2)
    ax.text(0, 0.75, f"buscar x = {x}", fontsize=10, color=TINTA, fontweight="bold")
    ax.text(4.0, 0.75, "verde: A[k] < x (k < lo)", fontsize=9, color="#1a7a55")
    ax.text(9.0, 0.75, "naranja: A[k] > x (k ≥ hi)", fontsize=9, color="#b4471b")
    ax.set_xlim(-0.2, len(A) + 5.2)
    ax.set_ylim(-len(estados) + 0.4, 1.1)
    ax.set_title("El invariante: todo lo de la izquierda es menor que x y todo lo de la derecha, mayor")
    fig.savefig(destino / "ejercicio-02-invariante.png")
    plt.close(fig)


def figura_peor_caso(plt, destino):
    ns = list(range(1, 130))
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.step(ns, [cota_informacion(n) for n in ns], where="post", color=TENUE, linewidth=5,
            alpha=0.45, label="cota de información ⌈log₂(n+1)⌉")
    ax.plot(ns, [peor_caso(n) for n in ns], "o", color=AZUL, markersize=3.5,
            label="peor caso medido de la búsqueda binaria")
    ax.set_xlabel("n")
    ax.set_ylabel("comparaciones")
    ax.set_title("El peor caso coincide con la cota para cada n, no solo asintóticamente")
    ax.legend(loc="lower right")
    fig.savefig(destino / "ejercicio-02-peor-caso.png")
    plt.close(fig)


def figura_fallos(plt, destino, filas):
    import numpy as np

    fig, ax = plt.subplots(figsize=(8.4, 4.2))
    etiquetas = [f[0] for f in filas]
    x = np.arange(len(filas))
    ancho = 0.26
    series = [("lo = m (potencial)", AZUL, 1), ("hi = m − 1, solo está/no está", NARANJA, 2),
              ("hi = m − 1, mirando el hueco", AQUA, 3)]
    for i, (nombre, color, col) in enumerate(series):
        vals = [f[col] for f in filas]
        barras = ax.bar(x + (i - 1) * ancho, vals, ancho - 0.03, color=color, label=nombre)
        for b, v in zip(barras, vals):
            ax.text(b.get_x() + b.get_width() / 2, v + 1, f"{v:.0f}", ha="center", fontsize=8,
                    color=TINTA_2)
    ax.set_xticks(x)
    ax.set_xticklabels(etiquetas, fontsize=9)
    ax.set_ylabel("% de casos donde la variante falla")
    ax.set_ylim(0, 100)
    ax.set_title("Los dos ceros son teoremas, y la demostración dice dónde caen")
    ax.legend(loc="upper right")
    fig.savefig(destino / "ejercicio-02-fallos.png")
    plt.close(fig)


def figuras(filas):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    _estilo(plt)
    destino = Path(__file__).resolve().parent.parent / "figuras"
    destino.mkdir(exist_ok=True)
    figura_invariante(plt, destino)
    figura_peor_caso(plt, destino)
    figura_fallos(plt, destino, filas)
    print(f"figuras escritas en {destino}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    tabla_traza()
    tabla_peor_caso()
    tabla_caminos()
    filas = tasas_de_fallo()
    tabla_fallos(filas)
    if "--figuras" in sys.argv:
        figuras(filas)
