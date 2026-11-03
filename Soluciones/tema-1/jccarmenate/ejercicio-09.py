"""Ejercicio 9 del Tema 1: un merge "optimizado" que la cota mínima delata.

    python ejercicio-09.py

Imprime todas las tablas que cita ejercicio-09.md, corre las pruebas y regenera las
dos figuras (ejercicio-09-adversario.svg y ejercicio-09-baterias.svg). Cada número que
aparece en la prosa sale de aquí. Solo necesita matplotlib.
"""

import itertools
import math
import random

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt


# --------------------------------------------------------------------------
# 1. Los dos merges
# --------------------------------------------------------------------------

class Comparador:
    def __init__(self):
        self.veces, self.pares = 0, []

    def __call__(self, a, b):
        self.veces += 1
        self.pares.append((a, b))
        return a <= b


def merge(I, D, less_equal):
    R, i, j = [], 0, 0
    while i < len(I) and j < len(D):
        if less_equal(I[i], D[j]):
            R.append(I[i])
            i += 1
        else:
            R.append(D[j])
            j += 1
    return R + I[i:] + D[j:]


def optimized_merge(I, D, less_equal):
    """Deja de comparar cuando a I le queda un solo elemento y lo pone al final."""
    R, i, j = [], 0, 0
    while len(I) - i > 1 and j < len(D):
        if less_equal(I[i], D[j]):
            R.append(I[i])
            i += 1
        else:
            R.append(D[j])
            j += 1
    if j == len(D):                          # D se acabó: lo que queda de I va en orden
        return R + I[i:]
    return R + D[j:] + I[i:]                 # el "ahorro": el último de I, al final


def intercalados(n):
    """Todas las entradas de largo n sin repetidos, salvo renombrar valores: cada
    manera de intercalar I con D."""
    for pos in itertools.combinations(range(2 * n), n):
        s = set(pos)
        yield [p for p in range(2 * n) if p in s], [p for p in range(2 * n) if p not in s]


def seccion(titulo):
    print()
    print(titulo)
    print("-" * len(titulo))


def miles(x):
    return f"{x:,}".replace(",", " ")


# --------------------------------------------------------------------------
# 2. Las tablas que cita la prosa
# --------------------------------------------------------------------------

def ejemplo_chico():
    seccion("§2. Ejemplo chico: n = 4")
    for I, D in [([1, 4, 6, 9], [2, 3, 7, 8]), ([2, 4, 6, 8], [1, 3, 5, 7])]:
        c = Comparador()
        R = optimized_merge(I, D, c)
        print(f"I = {I}, D = {D}: optimizado {R} con {c.veces} comparaciones; "
              f"{'correcta' if R == sorted(I + D) else 'MAL'}")


def peor_caso():
    seccion("§3. Comparaciones en el peor caso, sobre todas las entradas")
    print(f"{'n':>3} {'entradas':>9} {'optimizado':>11} {'2n - 2':>7} {'merge':>7} "
          f"{'2n - 1':>7} {'optimizado bien':>16}")
    for n in range(1, 11):
        peor_o = peor_m = bien = total = 0
        for I, D in intercalados(n):
            c1, c2 = Comparador(), Comparador()
            R = optimized_merge(I, D, c1)
            merge(I, D, c2)
            peor_o, peor_m = max(peor_o, c1.veces), max(peor_m, c2.veces)
            bien += R == sorted(I + D)
            total += 1
        print(f"{n:>3} {miles(total):>9} {peor_o:>11} {max(0, 2 * n - 2):>7} {peor_m:>7} "
              f"{2 * n - 1:>7} {100 * bien / total:>15.1f}%")


def adversario(n=5):
    seccion("§5. La entrada del adversario: a1 < b1 < a2 < b2 < ... < an < bn")
    I = list(range(0, 2 * n, 2))             # a_k = 2k
    D = list(range(1, 2 * n, 2))             # b_k = 2k + 1
    nombre = lambda v: f"a{v // 2 + 1}" if v % 2 == 0 else f"b{v // 2 + 1}"
    c = Comparador()
    R = optimized_merge(I, D, c)
    vecinos = [(v, v + 1) for v in range(2 * n - 1)]
    comparados = {tuple(sorted(p)) for p in c.pares}
    sin_comparar = [p for p in vecinos if p not in comparados]
    print("salida del optimizado:", " ".join(nombre(v) for v in R))
    print("salida correcta:      ", " ".join(nombre(v) for v in sorted(I + D)))
    print(f"comparaciones: {c.veces}; pares de vecinos: {len(vecinos)}; sin comparar: "
          + ", ".join(f"({nombre(a)}, {nombre(b)})" for a, b in sin_comparar))
    # intercambiar el último par sin comparar: el optimizado no distingue las dos entradas
    a, b = sin_comparar[-1]
    I2 = [b if v == a else v for v in I]
    D2 = [a if v == b else v for v in D]
    c2 = Comparador()
    R2 = optimized_merge(I2, D2, c2)
    respuestas = [x <= y for x, y in c.pares] == [x <= y for x, y in c2.pares]
    print(f"con {nombre(a)} y {nombre(b)} intercambiados: mismas respuestas a las "
          f"comparaciones: {respuestas}; el optimizado acierta: {R2 == sorted(I2 + D2)}")
    return I, D, c.pares, sin_comparar


def cuando_falla():
    seccion("§5. Cuándo falla exactamente")
    total = coinciden = 0
    for n in range(1, 11):
        for I, D in intercalados(n):
            R = optimized_merge(I, D, Comparador())
            coinciden += (R == sorted(I + D)) == (I[-1] > D[-1])
            total += 1
    print(f"en las {miles(total)} entradas con n de 1 a 10, el optimizado acierta si y "
          f"solo si el máximo está en I: se cumple en {miles(coinciden)}")


# --------------------------------------------------------------------------
# 3. Las baterías de pruebas
# --------------------------------------------------------------------------

def baterias():
    seccion("§6. Qué baterías de pruebas ven el error")
    rng = random.Random(9)

    def al_azar():
        n = rng.randint(1, 30)
        return sorted(rng.randrange(1000) for _ in range(n)), sorted(rng.randrange(1000)
                                                                     for _ in range(n))

    def alternando():
        # repartir una lista ordenada empezando por D: el máximo queda en I
        n = rng.randint(1, 30)
        L = sorted(rng.sample(range(1000), 2 * n))
        return L[1::2], L[0::2]

    def I_arriba():
        n = rng.randint(1, 30)
        return sorted(rng.sample(range(500, 1000), n)), sorted(rng.sample(range(500), n))

    def I_abajo():
        n = rng.randint(1, 30)
        return sorted(rng.sample(range(500), n)), sorted(rng.sample(range(500, 1000), n))

    tabla = {}
    print(f"{'batería':>20} {'casos':>6} {'merge':>7} {'optimizado':>11}")
    for nombre, g in [("al azar", al_azar), ("repartir alternando", alternando),
                      ("I con los grandes", I_arriba), ("I con los chicos", I_abajo)]:
        casos = [g() for _ in range(4000)]
        f = [100 * sum(merge(I, D, Comparador()) != sorted(I + D) for I, D in casos) / 4000,
             100 * sum(optimized_merge(I, D, Comparador()) != sorted(I + D)
                       for I, D in casos) / 4000]
        tabla[nombre] = f
        print(f"{nombre:>20} {len(casos):>6} {f[0]:>6.1f}% {f[1]:>10.1f}%")
    return tabla


# --------------------------------------------------------------------------
# 4. Pruebas
# --------------------------------------------------------------------------

def pruebas():
    seccion("Pruebas")
    comprobaciones = 0
    rng = random.Random(2026)

    # (a) el merge correcto, contra sorted, con repetidos y largos distintos
    for _ in range(20_000):
        I = sorted(rng.randrange(20) for _ in range(rng.randint(0, 30)))
        D = sorted(rng.randrange(20) for _ in range(rng.randint(0, 30)))
        c = Comparador()
        assert merge(I, D, c) == sorted(I + D)
        assert c.veces <= max(0, len(I) + len(D) - 1)
        comprobaciones += 1

    # (b) en todas las entradas sin repetidos con n <= 10: el merge compara todos los
    #     pares de vecinos de la intercalada, y el optimizado nunca pasa de 2n - 2
    for n in range(1, 11):
        for I, D in intercalados(n):
            c = Comparador()
            optimized_merge(I, D, c)
            assert c.veces <= max(0, 2 * n - 2)
            comprobaciones += 1
        I, D = list(range(0, 2 * n, 2)), list(range(1, 2 * n, 2))
        c = Comparador()
        merge(I, D, c)
        assert {tuple(sorted(p)) for p in c.pares} == {(v, v + 1) for v in range(2 * n - 1)}
        comprobaciones += 1

    # (c) el optimizado acierta si y solo si el máximo está en I, también con repetidos
    for _ in range(20_000):
        n = rng.randint(1, 20)
        I = sorted(rng.randrange(15) for _ in range(n))
        D = sorted(rng.randrange(15) for _ in range(n))
        bien = optimized_merge(I, D, Comparador()) == sorted(I + D)
        assert bien == (I[-1] >= D[-1])
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
        "figure.facecolor": "white", "svg.hashsalt": "ejercicio-09",
    })


def _guardar(fig, nombre):
    fig.tight_layout()
    fig.savefig(nombre, metadata={"Date": None})
    plt.close(fig)


def figura_adversario(I, D, pares, sin_comparar):
    fig, ax = plt.subplots(figsize=(6.8, 2.2))
    n = len(I)
    y = {"a": 1.0, "b": 0.0}
    pos = {}
    for v in range(2 * n):
        fila = "a" if v % 2 == 0 else "b"
        pos[v] = (v, y[fila])
        ax.add_patch(plt.Circle(pos[v], 0.28, facecolor="white",
                                edgecolor=OSCURO if fila == "a" else CALIDO, lw=1.5))
        ax.text(*pos[v], f"{fila}{v // 2 + 1}", ha="center", va="center", fontsize=8,
                color=OSCURO if fila == "a" else CALIDO)
    comparados = {tuple(sorted(p)) for p in pares}
    for v in range(2 * n - 1):
        (x0, y0), (x1, y1) = pos[v], pos[v + 1]
        if (v, v + 1) in comparados:
            ax.plot([x0, x1], [y0, y1], color=APAGADO, lw=1.2, zorder=0)
        else:
            ax.plot([x0, x1], [y0, y1], color=ALARMA, lw=1.6, ls="--", zorder=0)
    ax.text(2 * n - 0.2, 0.5, "sin comparar", color=ALARMA, fontsize=8, va="center")
    ax.text(-0.9, 1.0, "I", fontsize=10, va="center", color=OSCURO)
    ax.text(-0.9, 0.0, "D", fontsize=10, va="center", color=CALIDO)
    ax.set_xlim(-1.2, 2 * n + 1.6)
    ax.set_ylim(-0.5, 1.5)
    ax.set_aspect("equal")
    ax.axis("off")
    _guardar(fig, "ejercicio-09-adversario.svg")


def figura_baterias(tabla):
    fig, ax = plt.subplots(figsize=(6.4, 2.9))
    nombres = list(tabla)
    ancho = 0.36
    for k, (etiqueta, color) in enumerate([("merge", OSCURO), ("optimizado", ALARMA)]):
        alturas = [tabla[b][k] for b in nombres]
        pos = [i + (k - 0.5) * ancho for i in range(len(nombres))]
        ax.bar(pos, alturas, ancho, color=color, label=etiqueta)
        for xx, h in zip(pos, alturas):
            ax.text(xx, h + 1.5, f"{h:.0f}", ha="center", fontsize=7, color=color)
    ax.set_xticks(range(len(nombres)))
    ax.set_xticklabels(nombres, fontsize=8)
    ax.set_ylabel("% de merges mal")
    ax.set_ylim(0, 112)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color=REGLA, lw=0.6)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    _guardar(fig, "ejercicio-09-baterias.svg")


if __name__ == "__main__":
    ejemplo_chico()
    peor_caso()
    I, D, pares, sin_comparar = adversario()
    cuando_falla()
    tabla = baterias()
    pruebas()
    _estilo()
    figura_adversario(I, D, pares, sin_comparar)
    figura_baterias(tabla)
    print("\nfiguras: ejercicio-09-adversario.svg, ejercicio-09-baterias.svg")
