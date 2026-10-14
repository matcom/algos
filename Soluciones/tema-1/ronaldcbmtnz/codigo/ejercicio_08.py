"""Ejercicio 8 del Tema 1: los elementos que aparecen más de n/3 veces.

Boyer-Moore con dos candidatos (el caso k = 3 de Misra-Gries), la versión que
no verifica y los generadores de pruebas que la atrapan o no.

Uso:
    python ejercicio_08.py             imprime las tablas del informe
    python ejercicio_08.py --figuras   además regenera las figuras

Las pruebas están en test_ejercicio_08.py.
"""

import itertools
import random
import sys
from collections import Counter
from pathlib import Path


# ---------------------------------------------------------------------------
# 1. Primera pasada: dos candidatos con contador
# ---------------------------------------------------------------------------

def primera_pasada(A, orden_malo=False, vigilar=False):
    """Devuelve [(c1, k1), (c2, k2)]. Solo compara elementos por igualdad.

    Reglas, en este orden:
      1. si x es uno de los candidatos, su contador sube;
      2. si no, y algún contador está en 0, x pasa a ser ese candidato con contador 1;
      3. si no, los dos contadores bajan (x se cancela con una copia de cada uno).
    Con orden_malo=True se mira primero la regla 2: es el error del informe.
    """
    cand = [None, None]
    cont = [0, 0]
    for i, x in enumerate(A):
        if orden_malo:
            if cont[0] == 0:
                cand[0], cont[0] = x, 1
            elif cont[1] == 0:
                cand[1], cont[1] = x, 1
            elif x == cand[0]:
                cont[0] += 1
            elif x == cand[1]:
                cont[1] += 1
            else:
                cont[0] -= 1
                cont[1] -= 1
        else:
            if x == cand[0]:
                cont[0] += 1
            elif x == cand[1]:
                cont[1] += 1
            elif cont[0] == 0:
                cand[0], cont[0] = x, 1
            elif cont[1] == 0:
                cand[1], cont[1] = x, 1
            else:
                cont[0] -= 1
                cont[1] -= 1
        if vigilar:
            assert invariante(A[:i + 1], cand, cont), (A[:i + 1], cand, cont)
    return list(zip(cand, cont))


def se_parte_en_ternas(multiconjunto):
    """Lema 1: tamaño múltiplo de 3 y ningún elemento más de un tercio de las veces."""
    total = sum(multiconjunto.values())
    return total % 3 == 0 and all(3 * k <= total for k in multiconjunto.values())


def invariante(prefijo, cand, cont):
    """El prefijo = ternas de distintos + cont[0] copias de cand[0] + cont[1] copias de cand[1]."""
    if cont[0] > 0 and cont[1] > 0 and cand[0] == cand[1]:
        return False
    resto = Counter(prefijo)
    for c, k in zip(cand, cont):
        if k > 0:
            resto[c] -= k
            if resto[c] < 0:
                return False
    return se_parte_en_ternas(+resto)


def mas_de_un_tercio(A, orden_malo=False):
    """Las dos pasadas: candidatos y verificación. Devuelve la lista ordenada de respuestas."""
    candidatos = {c for c, k in primera_pasada(A, orden_malo) if k > 0}
    return sorted(c for c in candidatos if 3 * A.count(c) > len(A))


def sin_verificar(A):
    """La versión del enunciado: devuelve los candidatos con contador positivo, sin contarlos."""
    return sorted({c for c, k in primera_pasada(A) if k > 0})


def oraculo(A):
    return sorted(x for x, k in Counter(A).items() if 3 * k > len(A))


# ---------------------------------------------------------------------------
# 2. Generadores de pruebas
# ---------------------------------------------------------------------------

def _plantar(rng, n, pesados, alfabeto):
    """n elementos con `pesados` símbolos que aparecen ⌊n/3⌋ + 1 veces cada uno."""
    simbolos = rng.sample(alfabeto, len(alfabeto))
    A = []
    for s in simbolos[:pesados]:
        A += [s] * (n // 3 + 1)
    resto = simbolos[pesados:]
    while len(A) < n:
        A.append(rng.choice(resto))
    rng.shuffle(A)
    return A[:n]


GENERADORES = {
    "mayoría plantada (> n/2)": lambda rng, n: _plantar_mayoria(rng, n),
    "un pesado plantado": lambda rng, n: _plantar(rng, n, 1, list("ABCDE")),
    "dos pesados plantados": lambda rng, n: _plantar(rng, max(n, 4), 2, list("ABCDE")),
    "binario": lambda rng, n: [rng.choice("AB") for _ in range(n)],
    "3 símbolos": lambda rng, n: [rng.choice("ABC") for _ in range(n)],
    "5 símbolos": lambda rng, n: [rng.choice("ABCDE") for _ in range(n)],
}


def _plantar_mayoria(rng, n):
    m = rng.choice("ABCDE")
    A = [m] * (n // 2 + 1) + [rng.choice("ABCDE") for _ in range(n - n // 2 - 1)]
    rng.shuffle(A)
    return A


def tasas_de_fallo(casos=4000, semilla=8):
    rng = random.Random(semilla)
    filas = []
    for nombre, generar in GENERADORES.items():
        entradas = [generar(rng, rng.randint(1, 15)) for _ in range(casos)]
        f_sin = sum(sin_verificar(A) != oraculo(A) for A in entradas)
        f_orden = sum(mas_de_un_tercio(A, orden_malo=True) != oraculo(A) for A in entradas)
        f_bien = sum(mas_de_un_tercio(A) != oraculo(A) for A in entradas)
        filas.append((nombre, 100 * f_sin / casos, 100 * f_orden / casos, 100 * f_bien / casos))
    return filas


def contraejemplo(funcion, alfabeto="ABC", largo_max=8):
    """La entrada más corta (y primera en orden) donde `funcion` difiere del oráculo."""
    for largo in range(1, largo_max + 1):
        for A in itertools.product(alfabeto, repeat=largo):
            A = list(A)
            if funcion(A) != oraculo(A):
                return "".join(A)
    return None


# ---------------------------------------------------------------------------
# 3. Tablas
# ---------------------------------------------------------------------------

def tabla_traza(A="ABCAACBAAB"):
    print(f"Tabla 1. Traza sobre {A}")
    cand, cont = [None, None], [0, 0]
    for i, x in enumerate(A):
        if x == cand[0]:
            cont[0] += 1
            accion = "sube 1"
        elif x == cand[1]:
            cont[1] += 1
            accion = "sube 2"
        elif cont[0] == 0:
            cand[0], cont[0] = x, 1
            accion = "nuevo 1"
        elif cont[1] == 0:
            cand[1], cont[1] = x, 1
            accion = "nuevo 2"
        else:
            cont[0] -= 1
            cont[1] -= 1
            accion = "terna"
        print(f"  {i + 1:>2} {x}  {accion:>8}   ({cand[0]},{cont[0]}) ({cand[1]},{cont[1]})")
    print(f"  respuesta: {mas_de_un_tercio(list(A))}, sin verificar: {sin_verificar(list(A))},"
          f" oráculo: {oraculo(list(A))}")
    print()


def tabla_tres_simbolos(casos=5000, semilla=9):
    print("Tabla 2. Con tres símbolos, los contadores finales son f - f_min (lema 4)")
    rng = random.Random(semilla)
    bien = 0
    for _ in range(casos):
        A = [rng.choice("ABC") for _ in range(rng.randint(0, 30))]
        f = Counter({s: 0 for s in "ABC"})
        f.update(A)
        fmin = min(f.values())
        finales = {c: k for c, k in primera_pasada(A) if k > 0}
        esperado = {s: f[s] - fmin for s in "ABC" if f[s] > fmin}
        bien += finales == esperado
    print(f"  {bien} de {casos} arreglos cumplen el lema")
    print()


def tabla_fallos(filas):
    print("Tabla 3. Porcentaje de fallos, 4000 arreglos de largo 1 a 15 por generador")
    print(f"{'generador':>26} {'sin verificar':>14} {'orden malo':>11} {'dos pasadas':>12}")
    for nombre, a, b, c in filas:
        print(f"{nombre:>26} {a:>13.1f}% {b:>10.1f}% {c:>11.1f}%")
    print()


def tabla_contraejemplos():
    print("Tabla 4. Contraejemplos mínimos (búsqueda exhaustiva)")
    print(f"  sin verificar, alfabeto AB:  {contraejemplo(sin_verificar, 'AB')}")
    print(f"  sin verificar, alfabeto ABC: {contraejemplo(sin_verificar, 'ABC')}")
    print(f"  orden malo, alfabeto ABC:    {contraejemplo(lambda A: mas_de_un_tercio(A, True), 'ABC')}")
    print(f"  orden malo, alfabeto ABCD:   {contraejemplo(lambda A: mas_de_un_tercio(A, True), 'ABCD')}")
    print()


# ---------------------------------------------------------------------------
# 4. Figura
# ---------------------------------------------------------------------------

AZUL, NARANJA, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
TINTA, TINTA_2, TENUE, REJILLA, SUPERFICIE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"


def figura_fallos(destino, filas):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    plt.rcParams.update({
        "font.family": ["Segoe UI", "DejaVu Sans"], "font.size": 10,
        "axes.edgecolor": "#c3c2b7", "axes.labelcolor": TINTA_2, "axes.titlecolor": TINTA,
        "axes.titlesize": 12, "axes.titleweight": "bold", "axes.titlelocation": "left",
        "axes.facecolor": SUPERFICIE, "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.color": REJILLA, "grid.linewidth": 0.6,
        "xtick.color": TENUE, "ytick.color": TENUE, "xtick.labelcolor": TINTA_2,
        "ytick.labelcolor": TINTA_2, "figure.facecolor": SUPERFICIE, "legend.frameon": False,
        "legend.labelcolor": TINTA_2, "savefig.dpi": 150, "savefig.bbox": "tight",
    })
    fig, ax = plt.subplots(figsize=(9, 4.2))
    x = np.arange(len(filas))
    ancho = 0.38
    for i, (nombre, color, col) in enumerate([("sin verificar", AZUL, 1),
                                               ("orden malo de los if (con verificación)", NARANJA, 2)]):
        vals = [f[col] for f in filas]
        barras = ax.bar(x + (i - 0.5) * ancho, vals, ancho - 0.04, color=color, label=nombre)
        for b, v in zip(barras, vals):
            ax.text(b.get_x() + b.get_width() / 2, v + 1, f"{v:.1f}", ha="center", fontsize=8,
                    color=TINTA_2)
    ax.set_xticks(x)
    ax.set_xticklabels([f[0].replace(" (", "\n(").replace(" plantad", "\nplantad") for f in filas],
                       fontsize=9)
    ax.set_ylim(0, 100)
    ax.set_ylabel("% de arreglos donde falla")
    ax.set_title("Dos pesados plantados: de estos seis generadores, el único ciego al atajo")
    ax.legend(loc="upper left")
    fig.savefig(destino / "ejercicio-08-fallos.png")
    plt.close(fig)
    print(f"figura escrita en {destino}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    tabla_traza()
    tabla_tres_simbolos()
    filas = tasas_de_fallo()
    tabla_fallos(filas)
    tabla_contraejemplos()
    if "--figuras" in sys.argv:
        figura_fallos(Path(__file__).resolve().parent.parent / "figuras", filas)
