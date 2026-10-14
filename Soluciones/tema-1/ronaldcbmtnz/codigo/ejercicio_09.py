"""Ejercicio 9 del Tema 1: la mezcla "optimizada".

Deja de comparar cuando a la primera lista le queda un solo elemento, y lo pone
al final. Contamos sus comparaciones, decidimos con la cota de la conferencia 5,
§6 que no puede ser correcta, y construimos con el adversario la entrada en la
que falla. Incluye un detector genérico: dado cualquier algoritmo de mezcla,
el adversario fabrica la entrada que lo hace fallar.

Uso:
    python ejercicio_09.py             imprime las tablas del informe
    python ejercicio_09.py --figuras   además regenera la figura

Las pruebas están en test_ejercicio_09.py.
"""

import itertools
import math
import random
import sys
from pathlib import Path


class Comparador:
    """menor(x, y) con contador y registro de los pares comparados."""

    def __init__(self, clave=None):
        self.clave = clave or (lambda v: v)
        self.total = 0
        self.pares = set()

    def menor(self, x, y):
        self.total += 1
        self.pares.add(frozenset((x, y)))
        return self.clave(x) < self.clave(y)


# ---------------------------------------------------------------------------
# 1. Las mezclas (reciben los elementos y un comparador)
# ---------------------------------------------------------------------------

def mezcla(A, B, cmp):
    """La mezcla de siempre: compara las cabezas hasta que una lista se acaba."""
    R, i, j = [], 0, 0
    while i < len(A) and j < len(B):
        if cmp.menor(B[j], A[i]):
            R.append(B[j])
            j += 1
        else:
            R.append(A[i])
            i += 1
    return R + A[i:] + B[j:]


def mezcla_optimizada(A, B, cmp):
    """La del enunciado: cuando a A le queda un elemento, deja de comparar y lo pone al final."""
    R, i, j = [], 0, 0
    while len(A) - i > 1 and j < len(B):
        if cmp.menor(B[j], A[i]):
            R.append(B[j])
            j += 1
        else:
            R.append(A[i])
            i += 1
    if j == len(B):
        return R + A[i:]
    return R + B[j:] + A[i:]              # A[i:] es un solo elemento: va al final


def mezcla_sin_la_ultima(A, B, cmp):
    """Otra "optimización": cuando queda un elemento en cada lista, pone primero el de A."""
    R, i, j = [], 0, 0
    while i < len(A) and j < len(B):
        if len(A) - i == 1 and len(B) - j == 1:
            return R + [A[i], B[j]]
        if cmp.menor(B[j], A[i]):
            R.append(B[j])
            j += 1
        else:
            R.append(A[i])
            i += 1
    return R + A[i:] + B[j:]


def mezcla_con_atajo(A, B, cmp):
    """Correcta: si A[-1] <= B[0] concatena sin más; si no, mezcla normal."""
    if A and B and not cmp.menor(B[0], A[-1]):
        return A + B
    return mezcla(A, B, cmp)


MEZCLAS = {
    "mezcla": mezcla,
    "optimizada (enunciado)": mezcla_optimizada,
    "sin la última": mezcla_sin_la_ultima,
    "con atajo (correcta)": mezcla_con_atajo,
}


def correr(algoritmo, A, B):
    """Ejecuta con valores numéricos; devuelve (resultado, comparaciones)."""
    cmp = Comparador()
    return algoritmo(list(A), list(B), cmp), cmp.total


def es_correcta_en(algoritmo, A, B):
    return correr(algoritmo, A, B)[0] == sorted(A + B)


# ---------------------------------------------------------------------------
# 2. Entradas: los intercalados
# ---------------------------------------------------------------------------

def intercalados(n):
    """Todas las formas de intercalar dos listas de n valores distintos."""
    for posiciones in itertools.combinations(range(2 * n), n):
        enA = set(posiciones)
        yield [v for v in range(2 * n) if v in enA], [v for v in range(2 * n) if v not in enA]


def intercalado_perfecto(n):
    """a1 < b1 < a2 < b2 < ... < an < bn (C5, §6)."""
    return list(range(0, 2 * n, 2)), list(range(1, 2 * n, 2))


# ---------------------------------------------------------------------------
# 3. El adversario de la C5, §6, como detector
# ---------------------------------------------------------------------------

def adversario(algoritmo, n):
    """Construye la entrada donde falla un algoritmo de mezcla, o None si compara todo.

    1. Corre el algoritmo contestando como si la entrada fuera el intercalado perfecto
       (los elementos son etiquetas; el comparador usa sus valores en esa cadena).
    2. Busca un par de vecinos de la cadena que nunca comparó.
    3. Intercambia sus valores: las dos entradas reciben las mismas respuestas en todas
       las comparaciones hechas, pero su orden correcto es distinto.
    4. Devuelve la de las dos en la que el algoritmo se equivoca.
    """
    A, B = intercalado_perfecto(n)
    etiquetas_A = [("A", i) for i in range(n)]
    etiquetas_B = [("B", j) for j in range(n)]
    valor = {("A", i): A[i] for i in range(n)}
    valor.update({("B", j): B[j] for j in range(n)})
    cmp = Comparador(clave=valor.get)
    algoritmo(etiquetas_A, etiquetas_B, cmp)
    cadena = sorted(valor, key=valor.get)
    for u, v in zip(cadena, cadena[1:]):
        if frozenset((u, v)) not in cmp.pares:
            otro = dict(valor)
            otro[u], otro[v] = valor[v], valor[u]
            for vals in (valor, otro):
                A2 = [vals[("A", i)] for i in range(n)]
                B2 = [vals[("B", j)] for j in range(n)]
                if not es_correcta_en(algoritmo, A2, B2):
                    return dict(A=A2, B=B2, par=(u, v), comparaciones=cmp.total)
            raise AssertionError("el teorema dice que alguna de las dos falla")
    return None


# ---------------------------------------------------------------------------
# 4. Tablas
# ---------------------------------------------------------------------------

def tabla_conteo():
    print("Tabla 1. Comparaciones sobre todos los intercalados (valores distintos)")
    print(f"{'n':>3} {'intercalados':>13} {'mezcla: peor':>13} {'2n-1':>5} {'promedio':>9}"
          f" {'2n-2n/(n+1)':>12} {'optimizada: peor':>17} {'2n-2':>5} {'falla en':>9}"
          f" {'con a_n < b_n':>14}")
    for n in range(1, 10):
        total = 0
        peor_m = peor_o = 0
        suma = 0
        fallos = 0
        a_menor = 0
        for A, B in intercalados(n):
            total += 1
            _, cm = correr(mezcla, A, B)
            r, co = correr(mezcla_optimizada, A, B)
            peor_m, peor_o = max(peor_m, cm), max(peor_o, co)
            suma += cm
            fallos += r != sorted(A + B)
            a_menor += A[-1] < B[-1]
        print(f"{n:>3} {total:>13} {peor_m:>13} {2 * n - 1:>5} {suma / total:>9.4f}"
              f" {2 * n - 2 * n / (n + 1):>12.4f} {peor_o:>17} {max(2 * n - 2, 0):>5}"
              f" {fallos:>9} {a_menor:>14}")
    print()


def tabla_adversario():
    print("Tabla 2. El adversario como detector (n = 6)")
    for nombre, algoritmo in MEZCLAS.items():
        res = adversario(algoritmo, 6)
        if res is None:
            _, total = correr(algoritmo, *intercalado_perfecto(6))
            print(f"  {nombre:>24}: {total} comparaciones; compara los 11 pares de la cadena;"
                  f" no hay entrada que lo haga fallar")
        else:
            print(f"  {nombre:>24}: {res['comparaciones']} comparaciones; par sin comparar {res['par']};"
                  f" falla en A = {res['A']}, B = {res['B']}")
    print()


def tabla_traza(n=5):
    A, B = intercalado_perfecto(n)
    print(f"Tabla 3. La optimizada sobre el intercalado perfecto A = {A}, B = {B}")
    r, c = correr(mezcla_optimizada, A, B)
    print(f"  resultado {r}")
    print(f"  correcto  {sorted(A + B)}  ({c} comparaciones)")
    print()


def tabla_pruebas_al_azar(casos=4000, semilla=9):
    print("Tabla 4. Qué tan seguido la atrapan pruebas al azar")
    rng = random.Random(semilla)
    for nombre, generar in [
        ("valores al azar", lambda n: (sorted(rng.sample(range(1000), n)), sorted(rng.sample(range(1000), n)))),
        ("A al principio (A todo menor)", lambda n: (list(range(n)), list(range(n, 2 * n)))),
        ("B al principio (B todo menor)", lambda n: (list(range(n, 2 * n)), list(range(n)))),
    ]:
        fallos = 0
        for _ in range(casos):
            A, B = generar(rng.randint(1, 20))
            fallos += not es_correcta_en(mezcla_optimizada, A, B)
        print(f"  {nombre:>30}: {100 * fallos / casos:5.1f}% de fallos")
    print()


# ---------------------------------------------------------------------------
# 5. Figura
# ---------------------------------------------------------------------------

AZUL, NARANJA, ROJO = "#2a78d6", "#eb6834", "#e34948"
TINTA, TINTA_2, TENUE, SUPERFICIE = "#0b0b0b", "#52514e", "#898781", "#fcfcfb"


def figura(destino, n=5):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({"font.family": ["Segoe UI", "DejaVu Sans"], "font.size": 10,
                         "axes.titlecolor": TINTA, "axes.titlesize": 11, "axes.titleweight": "bold",
                         "axes.titlelocation": "left", "figure.facecolor": SUPERFICIE,
                         "savefig.dpi": 150, "savefig.bbox": "tight"})
    fig, ejes = plt.subplots(2, 1, figsize=(9, 5.2))
    for ax, (nombre, algoritmo) in zip(ejes, [("mezcla", mezcla), ("optimizada (enunciado)", mezcla_optimizada)]):
        A, B = intercalado_perfecto(n)
        etiquetas = {("A", i): (2 * i, 1.0) for i in range(n)}
        etiquetas.update({("B", j): (2 * j + 1, 0.0) for j in range(n)})
        valor = {("A", i): A[i] for i in range(n)}
        valor.update({("B", j): B[j] for j in range(n)})
        cmp = Comparador(clave=valor.get)
        algoritmo([("A", i) for i in range(n)], [("B", j) for j in range(n)], cmp)
        cadena = sorted(valor, key=valor.get)
        faltan = 0
        for u, v in zip(cadena, cadena[1:]):
            (x1, y1), (x2, y2) = etiquetas[u], etiquetas[v]
            comparado = frozenset((u, v)) in cmp.pares
            faltan += not comparado
            ax.plot([x1, x2], [y1, y2], color=NARANJA if comparado else ROJO,
                    linestyle="-" if comparado else (0, (3, 3)), linewidth=1.8 if comparado else 1.5)
        for (lista, k), (x, y) in etiquetas.items():
            ax.plot(x, y, "o", color=SUPERFICIE, markersize=22, markeredgecolor=AZUL if lista == "A" else TINTA_2,
                    markeredgewidth=1.5)
            ax.text(x, y, f"{lista.lower()}{k + 1}", ha="center", va="center", fontsize=9, color=TINTA)
        ax.set_xlim(-1, 2 * n + 3.2)
        ax.set_ylim(-0.5, 1.5)
        ax.axis("off")
        extra = "" if not faltan else f"; {faltan} pares de vecinos sin comparar (rojo)"
        ax.set_title(f"{nombre}: {cmp.total} comparaciones sobre a₁ < b₁ < … < a₅ < b₅{extra}")
    ejes[1].text(2 * n + 0.2, 0.5, "salida: … b₄, b₅, a₅\ncorrecto: … b₄, a₅, b₅", fontsize=9,
                 color=ROJO, ha="left", va="center")
    destino.mkdir(exist_ok=True)
    fig.savefig(destino / "ejercicio-09-cadena.png")
    plt.close(fig)
    print(f"figura escrita en {destino}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    tabla_traza()
    tabla_conteo()
    tabla_adversario()
    tabla_pruebas_al_azar()
    if "--figuras" in sys.argv:
        figura(Path(__file__).resolve().parent.parent / "figuras")
