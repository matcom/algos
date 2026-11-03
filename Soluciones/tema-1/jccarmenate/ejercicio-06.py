"""Ejercicio 6 del Tema 1: buscar un valor en una matriz con filas y columnas ordenadas.

    python ejercicio-06.py

Imprime todas las tablas que cita ejercicio-06.md, corre las pruebas y regenera las
tres figuras (ejercicio-06-escalera.svg, ejercicio-06-adversario.svg y
ejercicio-06-errores.svg). Cada número que aparece en la prosa sale de aquí. Solo
necesita matplotlib.
"""

import math
import random

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt


# --------------------------------------------------------------------------
# 1. Matrices y algoritmos
# --------------------------------------------------------------------------

class Comparador:
    """Compara x con una celda: -1, 0 o 1. Cuenta las comparaciones y recuerda las
    celdas que miró."""

    def __init__(self, M):
        self.M, self.veces, self.miradas = M, 0, []

    def __call__(self, x, i, j):
        self.veces += 1
        self.miradas.append((i, j))
        v = self.M[i][j]
        return (x > v) - (x < v)


def matriz_al_azar(n, rng, paso=3):
    """Filas y columnas estrictamente crecientes: cada celda supera a la de arriba y a
    la de la izquierda en entre 1 y `paso`."""
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            base = max(M[i - 1][j] if i else 0, M[i][j - 1] if j else 0)
            M[i][j] = base + rng.randint(1, paso)
    return M


def saddleback_search(M, x, compare, columna_minima=0):
    """Empieza en la esquina superior derecha. Si la celda es mayor que x, descarta su
    columna; si es menor, descarta su fila. `columna_minima = 1` es el error plantado
    de la sección 7: el ciclo nunca mira la columna 0."""
    n = len(M)
    i, j = 0, n - 1
    while i < n and j >= columna_minima:
        r = compare(x, i, j)
        if r == 0:
            return ("está", (i, j))
        if r < 0:
            j -= 1                      # M[i][j] > x: la columna j, de i para abajo, también
        else:
            i += 1                      # M[i][j] < x: la fila i, de j para la izquierda, también
    return ("no está", None)


def binaria_por_filas(M, x, compare):
    """La alternativa obvia: una búsqueda binaria en cada fila."""
    for i in range(len(M)):
        lo, hi = 0, len(M)
        while lo < hi:
            m = (lo + hi) // 2
            r = compare(x, i, m)
            if r == 0:
                return ("está", (i, m))
            if r < 0:
                hi = m
            else:
                lo = m + 1
    return ("no está", None)


def correcta(M, x, resultado):
    tipo, celda = resultado
    if tipo == "está":
        i, j = celda
        return M[i][j] == x
    return all(x != v for fila in M for v in fila)


def adversario(n):
    """La matriz del adversario: M[i][j] = i + j fuera de las dos antidiagonales
    i + j = n - 1 e i + j = n, que valen n - 0,75 y n - 0,25. Se busca x = n - 0,5.
    Cualquiera de las 2n - 1 celdas de las antidiagonales puede valer x sin desordenar
    la matriz."""
    M = [[float(i + j) for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            if i + j == n - 1:
                M[i][j] = n - 0.75
            elif i + j == n:
                M[i][j] = n - 0.25
    return M, n - 0.5


def diagonales(n):
    return {(i, j) for i in range(n) for j in range(n) if i + j in (n - 1, n)}


def ordenada(M):
    n = len(M)
    return (all(M[i][j] < M[i][j + 1] for i in range(n) for j in range(n - 1))
            and all(M[i][j] < M[i + 1][j] for i in range(n - 1) for j in range(n)))


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
    seccion("§2. Ejemplo chico: una matriz de 5 x 5")
    rng = random.Random(6)
    M = matriz_al_azar(5, rng)
    for fila in M:
        print(" ".join(f"{v:>3}" for v in fila))
    for x in [21, 14]:
        c = Comparador(M)
        resultado = saddleback_search(M, x, c)
        pasos = " -> ".join(f"M[{i}][{j}]={M[i][j]}" for i, j in c.miradas)
        print(f"x = {x}: {pasos}")
        print(f"   {resultado[0]}, con {c.veces} comparaciones")
    return M


def invariante_vigilado():
    seccion("§3. El invariante y el potencial, vigilados con assert")
    rng = random.Random(3)
    busquedas = vueltas = 0
    for _ in range(4000):
        n = rng.randint(1, 12)
        M = matriz_al_azar(n, rng)
        x = rng.randint(0, M[-1][-1] + 2)
        i, j = 0, n - 1
        while True:
            # invariante: x no está en ninguna celda (r, c) con r < i o c > j
            assert all(M[r][c] != x for r in range(n) for c in range(n) if r < i or c > j)
            potencial = (n - i) + (j + 1)
            if not (i < n and j >= 0):
                break
            vueltas += 1
            if M[i][j] == x:
                break
            if M[i][j] > x:
                j -= 1
            else:
                i += 1
            assert (n - i) + (j + 1) == potencial - 1
        busquedas += 1
    print(f"{miles(busquedas)} búsquedas, {miles(vueltas)} vueltas vigiladas, 0 fallos")


def costos():
    seccion("§4. Comparaciones en el peor caso")
    print(f"{'n':>6} {'escalera (adversario)':>22} {'2n - 1':>7} "
          f"{'binaria por filas':>18} {'n·ceil(log2(n+1))':>18} {'fuerza bruta':>13}")
    for n in [2, 5, 10, 100, 1000]:
        M, x = adversario(n)
        c = Comparador(M)
        assert saddleback_search(M, x, c)[0] == "no está"
        c2 = Comparador(M)
        binaria_por_filas(M, M[0][0] - 1, c2)    # su peor caso: x menor que todo
        print(f"{n:>6} {c.veces:>22} {2 * n - 1:>7} {c2.veces:>18} "
              f"{n * (n).bit_length():>18} {n * n:>13}")
    rng = random.Random(4)
    peor = {}
    for n in [5, 10, 20]:
        p = 0
        for _ in range(2000):
            M = matriz_al_azar(n, rng)
            x = rng.randint(0, M[-1][-1] + 1)
            c = Comparador(M)
            saddleback_search(M, x, c)
            p = max(p, c.veces)
        peor[n] = p
    print("en matrices al azar, el peor de 2000 búsquedas: "
          + ", ".join(f"n = {n}: {p} de {2 * n - 1}" for n, p in peor.items()))


def adversario_en_accion():
    seccion("§5. El adversario: las 2n - 1 celdas de las dos antidiagonales")
    for n in [6, 50]:
        M, x = adversario(n)
        assert ordenada(M)
        D = diagonales(n)
        libres = 0
        for celda in D:
            i, j = celda
            M2 = [fila[:] for fila in M]
            M2[i][j] = x
            libres += ordenada(M2)
        c = Comparador(M)
        saddleback_search(M, x, c)
        print(f"n = {n}: {len(D)} celdas en las antidiagonales; en {libres} de ellas se "
              f"puede poner x sin desordenar la matriz; la escalera mira "
              f"{len(set(c.miradas) & D)} de ellas con {c.veces} comparaciones")


# --------------------------------------------------------------------------
# 3. El error plantado
# --------------------------------------------------------------------------

def errores_plantados():
    seccion("§7. La escalera que nunca mira la columna 0")
    rng = random.Random(7)
    baterias = {}

    def caso_presente():
        n = rng.randint(1, 10)
        M = matriz_al_azar(n, rng)
        return M, M[rng.randrange(n)][rng.randrange(n)]

    def caso_ausente():
        n = rng.randint(1, 10)
        M = matriz_al_azar(n, rng)
        valores = {v for fila in M for v in fila}
        x = rng.choice([v for v in range(M[-1][-1] + 2) if v not in valores])
        return M, x

    def caso_columna_0():
        n = rng.randint(1, 10)
        M = matriz_al_azar(n, rng)
        return M, M[rng.randrange(n)][0]

    baterias["x presente"] = [caso_presente() for _ in range(4000)]
    baterias["x ausente"] = [caso_ausente() for _ in range(4000)]
    baterias["x en la columna 0"] = [caso_columna_0() for _ in range(4000)]
    baterias["el adversario"] = []
    for n in range(1, 31):
        M, x = adversario(n)
        c = Comparador(M)
        saddleback_search(M, x, c, columna_minima=1)
        no_miradas = sorted(diagonales(n) - set(c.miradas))
        M2 = [fila[:] for fila in M]
        if no_miradas:
            i, j = no_miradas[0]
            M2[i][j] = x                 # el adversario pone x donde no miró
        baterias["el adversario"].append((M2, x))

    fallos = {}
    print(f"{'batería':>18} {'casos':>6} {'correcta':>9} {'sin columna 0':>14}")
    for nombre, casos in baterias.items():
        fila = []
        for minima in (0, 1):
            malos = sum(not correcta(M, x, saddleback_search(M, x, Comparador(M), minima))
                        for M, x in casos)
            fila.append(100 * malos / len(casos))
        fallos[nombre] = fila
        print(f"{nombre:>18} {len(casos):>6} {fila[0]:>8.1f}% {fila[1]:>13.1f}%")
    M, x = adversario(6)
    c = Comparador(M)
    saddleback_search(M, x, c, columna_minima=1)
    print(f"con n = 6, la versión mala mira {c.veces} celdas y deja sin mirar "
          f"{sorted(diagonales(6) - set(c.miradas))}")
    return fallos


# --------------------------------------------------------------------------
# 4. Pruebas
# --------------------------------------------------------------------------

def pruebas():
    seccion("Pruebas")
    comprobaciones = 0
    rng = random.Random(2026)

    # (a) escalera y binaria por filas contra el oráculo, con x presente y ausente
    for _ in range(5000):
        n = rng.randint(1, 15)
        M = matriz_al_azar(n, rng, paso=rng.choice([1, 2, 5]))
        x = rng.randint(-1, M[-1][-1] + 2)
        c = Comparador(M)
        r = saddleback_search(M, x, c)
        assert correcta(M, x, r) and c.veces <= 2 * n - 1
        assert correcta(M, x, binaria_por_filas(M, x, Comparador(M)))
        comprobaciones += 2

    # (b) todos los valores de una matriz se encuentran
    for _ in range(300):
        n = rng.randint(1, 12)
        M = matriz_al_azar(n, rng)
        for fila in M:
            for v in fila:
                assert saddleback_search(M, v, Comparador(M))[0] == "está"
                comprobaciones += 1

    # (c) el adversario: la matriz está ordenada, las 2n - 1 celdas son libres, y la
    #     escalera usa exactamente 2n - 1 comparaciones
    for n in range(1, 41):
        M, x = adversario(n)
        assert ordenada(M) and len(diagonales(n)) == 2 * n - 1
        for i, j in diagonales(n):
            M2 = [fila[:] for fila in M]
            M2[i][j] = x
            assert ordenada(M2)
        c = Comparador(M)
        assert saddleback_search(M, x, c)[0] == "no está" and c.veces == 2 * n - 1
        assert diagonales(n) <= set(c.miradas)
        comprobaciones += 3

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
        "figure.facecolor": "white", "svg.hashsalt": "ejercicio-06",
    })


def _guardar(fig, nombre):
    fig.tight_layout()
    fig.savefig(nombre, metadata={"Date": None})
    plt.close(fig)


def _grilla(ax, M, colores, textos=None):
    n = len(M)
    for i in range(n):
        for j in range(n):
            fondo = colores.get((i, j), "white")
            ax.add_patch(plt.Rectangle((j, -i - 1), 1, 1, facecolor=fondo,
                         edgecolor=REGLA, lw=0.8, zorder=1))
            t = textos(M[i][j]) if textos else str(M[i][j])
            ax.text(j + 0.5, -i - 0.5, t, ha="center", va="center", fontsize=8,
                    color=TINTA, zorder=5,
                    bbox={"facecolor": fondo, "edgecolor": "none", "pad": 0.4})
    ax.set_xlim(-0.2, n + 0.2)
    ax.set_ylim(-n - 0.2, 0.2)
    ax.set_aspect("equal")
    ax.axis("off")


def figura_escalera():
    rng = random.Random(6)
    M = matriz_al_azar(8, rng)
    # el valor que aparece una sola vez y que la escalera tarda más en encontrar
    valores = [v for fila in M for v in fila]
    unicos = [v for v in valores if valores.count(v) == 1]

    def pasos(v):
        c = Comparador(M)
        saddleback_search(M, v, c)
        return c.veces

    x = max(unicos, key=lambda v: (pasos(v), -v))
    c = Comparador(M)
    saddleback_search(M, x, c)
    fig, ax = plt.subplots(figsize=(4.4, 4.4))
    colores = {celda: "#ecfeff" for celda in c.miradas}
    colores[c.miradas[-1]] = "#fde2e7"
    _grilla(ax, M, colores)
    xs = [j + 0.5 for _, j in c.miradas]
    ys = [-i - 0.5 for i, _ in c.miradas]
    ax.plot(xs, ys, color=ACENTO, lw=1.4, zorder=2)
    ax.set_title(f"x = {x}: {c.veces} comparaciones", fontsize=9, color=TINTA)
    _guardar(fig, "ejercicio-06-escalera.svg")


def figura_adversario():
    n = 6
    M, x = adversario(n)
    c = Comparador(M)
    saddleback_search(M, x, c)
    fig, ax = plt.subplots(figsize=(4.4, 4.4))
    colores = {}
    for i, j in diagonales(n):
        colores[(i, j)] = "#fef3c7" if i + j == n - 1 else "#fde2e7"
    _grilla(ax, M, colores, textos=lambda v: f"{v:g}".replace(".", ","))
    xs = [j + 0.5 for _, j in c.miradas]
    ys = [-i - 0.5 for i, _ in c.miradas]
    ax.plot(xs, ys, color=ACENTO, lw=1.4, zorder=2)
    ax.set_title(f"x = {x:g}: las {2 * n - 1} celdas de color pueden valer x".replace(
        ".", ","), fontsize=9, color=TINTA)
    _guardar(fig, "ejercicio-06-adversario.svg")


def figura_errores(fallos):
    fig, ax = plt.subplots(figsize=(6.4, 2.9))
    nombres = list(fallos)
    ancho = 0.36
    for k, (etiqueta, color) in enumerate([("correcta", OSCURO), ("sin columna 0", ALARMA)]):
        alturas = [fallos[b][k] for b in nombres]
        pos = [i + (k - 0.5) * ancho for i in range(len(nombres))]
        ax.bar(pos, alturas, ancho, color=color, label=etiqueta)
        for xx, h in zip(pos, alturas):
            ax.text(xx, h + 1.5, f"{h:.0f}", ha="center", fontsize=7, color=color)
    ax.set_xticks(range(len(nombres)))
    ax.set_xticklabels(nombres)
    ax.set_ylabel("% de búsquedas mal")
    ax.set_ylim(0, 110)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color=REGLA, lw=0.6)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    _guardar(fig, "ejercicio-06-errores.svg")


if __name__ == "__main__":
    ejemplo_chico()
    invariante_vigilado()
    costos()
    adversario_en_accion()
    fallos = errores_plantados()
    pruebas()
    _estilo()
    figura_escalera()
    figura_adversario()
    figura_errores(fallos)
    print("\nfiguras: ejercicio-06-escalera.svg, ejercicio-06-adversario.svg, "
          "ejercicio-06-errores.svg")
