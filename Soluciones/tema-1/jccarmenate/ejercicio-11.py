"""Ejercicio 11 del Tema 1: la mochila en O(nW) y el tamaño de la entrada en bits.

    python ejercicio-11.py

Imprime todas las tablas que cita ejercicio-11.md, corre las pruebas y regenera las
dos figuras (ejercicio-11-bits.svg y ejercicio-11-errores.svg). Cada número que aparece
en la prosa sale de aquí. Solo necesita matplotlib.
"""

import itertools
import random

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt


# --------------------------------------------------------------------------
# 1. Los algoritmos
# --------------------------------------------------------------------------

def knapsack(w, v, W, ascendente=False):
    """Programación dinámica con un arreglo de W + 1 celdas. mejor[c] es el mayor valor
    que cabe en capacidad c usando los objetos vistos. Devuelve (valor, celdas
    actualizadas). ascendente = True es el error plantado de la sección 6."""
    mejor = [0] * (W + 1)
    celdas = 0
    for wi, vi in zip(w, v):
        rango = range(wi, W + 1) if ascendente else range(W, wi - 1, -1)
        for c in rango:
            celdas += 1
            if mejor[c - wi] + vi > mejor[c]:
                mejor[c] = mejor[c - wi] + vi
    return mejor[W], celdas


def mochila_bruta(w, v, W):
    """El oráculo: probar los 2^n subconjuntos."""
    n = len(w)
    mejor = 0
    for S in itertools.product((0, 1), repeat=n):
        peso = sum(wi for wi, s in zip(w, S) if s)
        if peso <= W:
            mejor = max(mejor, sum(vi for vi, s in zip(v, S) if s))
    return mejor


def mochila_con_repeticion(w, v, W):
    """Lo que en realidad calcula la versión ascendente: cada objeto se puede usar
    muchas veces."""
    mejor = [0] * (W + 1)
    for c in range(W + 1):
        for wi, vi in zip(w, v):
            if wi <= c:
                mejor[c] = max(mejor[c], mejor[c - wi] + vi)
    return mejor[W]


def bits(x):
    return max(1, x.bit_length())


def tamano(w, v, W):
    # bits de la entrada: todos los números escritos en binario
    return sum(bits(x) for x in w) + sum(bits(x) for x in v) + bits(W)


def divisiones_primo(b):
    # la división de prueba sobre un primo de b bits hace unas sqrt(2^b) = 2^(b/2)
    return 2 ** (b / 2)


def seccion(titulo):
    print()
    print(titulo)
    print("-" * len(titulo))


def miles(x):
    return f"{x:,}".replace(",", " ")


def cien(x):
    m, e = f"{x:.2e}".split("e")
    return f"{m.replace('.', ',')}·10^{int(e)}"


# --------------------------------------------------------------------------
# 2. Las tablas que cita la prosa
# --------------------------------------------------------------------------

def ejemplo_chico():
    seccion("§2. Ejemplo chico: 4 objetos")
    w, v, W = [3, 4, 5, 9], [4, 5, 6, 11], 12
    valor, celdas = knapsack(w, v, W)
    print(f"pesos {w}, valores {v}, capacidad {W}: mejor valor {valor} "
          f"(el oráculo dice {mochila_bruta(w, v, W)}), {celdas} celdas actualizadas")
    print(f"bits de la entrada: {tamano(w, v, W)}")


def crecimiento():
    seccion("§3. Mismo n, capacidad con cada vez más bits")
    rng = random.Random(3)
    n = 20
    # los mismos objetos en todas las filas: cada peso es una fracción fija de W
    fracciones = [rng.random() for _ in range(n)]
    v = [rng.randint(1, 1000) for _ in range(n)]
    filas = []
    print(f"{'bits de W':>10} {'W':>10} {'bits de la entrada':>19} {'celdas':>12} "
          f"{'celdas / anterior':>18}")
    previo = None
    for k in range(6, 19, 2):
        W = 2 ** k
        w = [max(1, int(f * W)) for f in fracciones]
        _, celdas = knapsack(w, v, W)
        b = tamano(w, v, W)
        filas.append((b, celdas))
        razon = "—" if previo is None else f"{celdas / previo:.2f}"
        print(f"{k + 1:>10} {miles(W):>10} {b:>19} {miles(celdas):>12} {razon:>18}")
        previo = celdas
    return filas


def familia_exponencial():
    seccion("§3. El peor caso: un objeto de peso 1 y valor 1")
    print(f"{'bits de la entrada':>19} {'W':>12} {'celdas':>12}")
    for b in [6, 10, 14, 18, 22]:
        w, v, W = [1], [1], 2 ** (b - 2) - 1     # W se escribe con b - 2 unos
        _, celdas = knapsack(w, v, W)
        print(f"{tamano(w, v, W):>19} {miles(W):>12} {miles(celdas):>12}")


def cruce():
    seccion("§4. La fuerza bruta contra la tabla, con pocos objetos y W enorme")
    n = 20
    for k in [10, 20, 30, 40]:
        W = 2 ** k
        print(f"n = {n}, W = 2^{k}: tabla {cien(n * (W + 1))} celdas, "
              f"fuerza bruta {cien(n * 2 ** n)} pasos")


def primalidad():
    seccion("§5. Primalidad por división contra la mochila, en función de los bits")
    print(f"{'b':>4} {'divisiones (primo de b bits)':>29} {'celdas (n = 20, W de b bits)':>29}")
    for b in [16, 32, 48, 64]:
        print(f"{b:>4} {cien(divisiones_primo(b)):>29} {cien(20 * 2 ** b):>29}")


def errores_plantados():
    seccion("§6. Recorrer las capacidades de menor a mayor")
    rng = random.Random(6)

    def al_azar():
        n = rng.randint(1, 10)
        w = [rng.randint(1, 20) for _ in range(n)]
        return w, [rng.randint(1, 20) for _ in range(n)], rng.randint(1, 60)

    def capacidad_chica():
        # W < 2·(peso mínimo): ningún objeto cabe dos veces
        n = rng.randint(1, 10)
        w = [rng.randint(10, 20) for _ in range(n)]
        return w, [rng.randint(1, 20) for _ in range(n)], rng.randint(1, 2 * min(w) - 1)

    def un_objeto():
        w = [rng.randint(1, 10)]
        return w, [rng.randint(1, 10)], rng.randint(1, 40)

    tabla = {}
    print(f"{'batería':>20} {'casos':>6} {'descendente':>12} {'ascendente':>11}")
    for nombre, g in [("al azar", al_azar), ("W < 2·peso mínimo", capacidad_chica),
                      ("un solo objeto", un_objeto)]:
        casos = [g() for _ in range(3000)]
        f = [100 * sum(knapsack(w, v, W)[0] != mochila_bruta(w, v, W) for w, v, W in casos)
             / len(casos),
             100 * sum(knapsack(w, v, W, True)[0] != mochila_bruta(w, v, W)
                       for w, v, W in casos) / len(casos)]
        tabla[nombre] = f
        print(f"{nombre:>20} {len(casos):>6} {f[0]:>11.1f}% {f[1]:>10.1f}%")
    w, v, W = [3], [5], 9
    print(f"un objeto de peso 3 y valor 5, capacidad 9: descendente "
          f"{knapsack(w, v, W)[0]}, ascendente {knapsack(w, v, W, True)[0]}")
    return tabla


# --------------------------------------------------------------------------
# 3. Pruebas
# --------------------------------------------------------------------------

def pruebas():
    seccion("Pruebas")
    comprobaciones = 0
    rng = random.Random(2026)

    # (a) la tabla contra la fuerza bruta, y la cuenta exacta de celdas
    for _ in range(3000):
        n = rng.randint(0, 11)
        w = [rng.randint(1, 30) for _ in range(n)]
        v = [rng.randint(0, 30) for _ in range(n)]
        W = rng.randint(0, 80)
        valor, celdas = knapsack(w, v, W)
        assert valor == mochila_bruta(w, v, W)
        assert celdas == sum(max(0, W - wi + 1) for wi in w)
        comprobaciones += 2

    # (b) la versión ascendente calcula la mochila con repetición
    for _ in range(3000):
        n = rng.randint(1, 8)
        w = [rng.randint(1, 15) for _ in range(n)]
        v = [rng.randint(0, 20) for _ in range(n)]
        W = rng.randint(0, 50)
        assert knapsack(w, v, W, True)[0] == mochila_con_repeticion(w, v, W)
        comprobaciones += 1

    # (c) con W < 2·(peso mínimo), las dos versiones coinciden
    for _ in range(3000):
        n = rng.randint(1, 8)
        w = [rng.randint(5, 15) for _ in range(n)]
        v = [rng.randint(0, 20) for _ in range(n)]
        W = rng.randint(0, 2 * min(w) - 1)
        assert knapsack(w, v, W)[0] == knapsack(w, v, W, True)[0]
        comprobaciones += 1

    print(f"{miles(comprobaciones)} comprobaciones, 0 fallos")


# --------------------------------------------------------------------------
# 4. Figuras
# --------------------------------------------------------------------------

TINTA, APAGADO, REGLA = "#1a1a1a", "#6b7280", "#d8dce3"
ACENTO, OSCURO, CALIDO, ALARMA = "#0891b2", "#0e7490", "#b45309", "#be123c"


def _estilo():
    plt.rcParams.update({
        "font.size": 9, "axes.edgecolor": APAGADO, "axes.labelcolor": TINTA,
        "xtick.color": APAGADO, "ytick.color": APAGADO,
        "figure.facecolor": "white", "svg.hashsalt": "ejercicio-11",
    })


def _guardar(fig, nombre):
    fig.tight_layout()
    fig.savefig(nombre, metadata={"Date": None})
    plt.close(fig)


def figura_bits():
    bs = list(range(8, 65, 4))
    fig, ax = plt.subplots(figsize=(6.4, 3.0))
    ax.plot(bs, [20 * 2 ** b for b in bs], "o-", color=OSCURO, lw=1.5, ms=3.5,
            label="mochila: celdas con n = 20 y W de b bits")
    ax.plot(bs, [divisiones_primo(b) for b in bs], "o-", color=CALIDO, lw=1.5, ms=3.5,
            label="primalidad: divisiones sobre un primo de b bits")
    ax.axhline(20 * 2 ** 20, color=APAGADO, lw=1, ls="--")
    ax.text(40, 20 * 2 ** 20 / 40, "fuerza bruta con n = 20: n·2ⁿ", color=APAGADO,
            fontsize=8)
    ax.plot(bs, [b ** 3 for b in bs], color=ACENTO, lw=1, ls=":", label="b³, un polinomio")
    ax.set_yscale("log")
    ax.set_xlabel("b, bits del número")
    ax.set_ylabel("operaciones")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(color=REGLA, lw=0.6)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    _guardar(fig, "ejercicio-11-bits.svg")


def figura_errores(tabla):
    fig, ax = plt.subplots(figsize=(6.0, 2.8))
    nombres = list(tabla)
    ancho = 0.36
    for k, (etiqueta, color) in enumerate([("descendente", OSCURO), ("ascendente", ALARMA)]):
        alturas = [tabla[b][k] for b in nombres]
        pos = [i + (k - 0.5) * ancho for i in range(len(nombres))]
        ax.bar(pos, alturas, ancho, color=color, label=etiqueta)
        for xx, h in zip(pos, alturas):
            ax.text(xx, h + 1.5, f"{h:.0f}", ha="center", fontsize=7, color=color)
    ax.set_xticks(range(len(nombres)))
    ax.set_xticklabels(nombres, fontsize=8)
    ax.set_ylabel("% de respuestas mal")
    ax.set_ylim(0, 112)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color=REGLA, lw=0.6)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    _guardar(fig, "ejercicio-11-errores.svg")


if __name__ == "__main__":
    ejemplo_chico()
    crecimiento()
    familia_exponencial()
    cruce()
    primalidad()
    tabla = errores_plantados()
    pruebas()
    _estilo()
    figura_bits()
    figura_errores(tabla)
    print("\nfiguras: ejercicio-11-bits.svg, ejercicio-11-errores.svg")
