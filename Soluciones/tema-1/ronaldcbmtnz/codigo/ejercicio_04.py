"""Ejercicio 4 del Tema 1: el contador binario en una máquina de Turing.

Una máquina de Turing de una cinta suma 1 a un número binario. El bit menos
significativo está en la celda 0, los más significativos a su izquierda, y el
cabezal empieza y termina sobre la celda 0 (ejercicio 7 de la conferencia 1).

Uso:
    python ejercicio_04.py             imprime las tablas del informe
    python ejercicio_04.py --figuras   además regenera las figuras

Las pruebas están en test_ejercicio_04.py.
"""

import sys
from pathlib import Path

BLANCO = "_"

# (estado, símbolo leído) -> (símbolo a escribir, movimiento, estado siguiente)
TRANSICIONES = {
    ("sumar", "1"): ("0", -1, "sumar"),      # acarreo: 1 -> 0, seguir a la izquierda
    ("sumar", "0"): ("1", +1, "volver"),     # se absorbe el acarreo
    ("sumar", BLANCO): ("1", +1, "volver"),  # el número crece un bit
    ("volver", "0"): ("0", +1, "volver"),    # volver sobre los ceros que dejó el acarreo
    ("volver", BLANCO): (BLANCO, -1, "fin"),  # se pasó del bit menos significativo: un paso atrás
}

# Variante del informe: el cabezal vive en el bit MÁS significativo (la celda más a la izquierda).
TRANSICIONES_MSB = {
    ("ir", "0"): ("0", +1, "ir"),            # caminar hasta el bit menos significativo
    ("ir", "1"): ("1", +1, "ir"),
    ("ir", BLANCO): (BLANCO, -1, "sumar"),
    ("sumar", "1"): ("0", -1, "sumar"),
    ("sumar", "0"): ("1", -1, "volver"),
    ("sumar", BLANCO): ("1", -1, "volver"),
    ("volver", "0"): ("0", -1, "volver"),
    ("volver", "1"): ("1", -1, "volver"),
    ("volver", BLANCO): (BLANCO, +1, "fin"),
}


class Cinta:
    def __init__(self):
        self.celdas = {0: "0"}               # el número 0
        self.cabezal = 0

    def leer(self):
        return self.celdas.get(self.cabezal, BLANCO)

    def escribir(self, s):
        if s == BLANCO:
            self.celdas.pop(self.cabezal, None)
        else:
            self.celdas[self.cabezal] = s

    def valor(self):
        return int("".join(self.celdas[k] for k in sorted(self.celdas)), 2)

    def unos(self):
        return sum(s == "1" for s in self.celdas.values())

    def bits(self):
        return len(self.celdas)


def incrementar(cinta, transiciones=TRANSICIONES, inicial="sumar", traza=None):
    """Ejecuta la máquina hasta el estado final. Devuelve el número de pasos."""
    estado, pasos = inicial, 0
    while estado != "fin":
        leido = cinta.leer()
        escribir, mover, estado_nuevo = transiciones[(estado, leido)]
        if traza is not None:
            traza.append((pasos, estado, cinta.cabezal, leido, escribir, mover, estado_nuevo))
        cinta.escribir(escribir)
        cinta.cabezal += mover
        estado = estado_nuevo
        pasos += 1
    return pasos


def unos_finales(k):
    """t(k): la cantidad de unos al final de k en binario."""
    t = 0
    while k & 1:
        k >>= 1
        t += 1
    return t


def costo_teorico(k):
    """Pasos para incrementar k: 2 t(k) + 2."""
    return 2 * unos_finales(k) + 2


def total_teorico(m):
    """Pasos de m incrementos desde 0: 4m - 2·popcount(m)."""
    return 4 * m - 2 * bin(m).count("1")


def potencial(cinta):
    """Φ = 2 · (unos en la cinta)."""
    return 2 * cinta.unos()


def correr(m):
    """m incrementos desde 0. Devuelve las listas de costo real, Φ y costo amortizado."""
    cinta = Cinta()
    reales, potenciales, amortizados = [], [potencial(cinta)], []
    for _ in range(m):
        antes = potencial(cinta)
        c = incrementar(cinta)
        reales.append(c)
        potenciales.append(potencial(cinta))
        amortizados.append(c + potencial(cinta) - antes)
    return reales, potenciales, amortizados


def total_msb(m):
    """Pasos de m incrementos con el cabezal en el bit más significativo."""
    cinta = Cinta()
    cinta.cabezal = 0
    total = 0
    for _ in range(m):
        cinta.cabezal = min(cinta.celdas)            # el cabezal está en el bit más significativo
        total += incrementar(cinta, TRANSICIONES_MSB, inicial="ir")
        assert cinta.cabezal == min(cinta.celdas)
    return total


# ---------------------------------------------------------------------------
# Tablas
# ---------------------------------------------------------------------------

def tabla_traza():
    print("Tabla 1. Traza de un incremento: 0111 (7) -> 1000 (8)")
    cinta = Cinta()
    for _ in range(7):
        incrementar(cinta)
    traza = []
    incrementar(cinta, traza=traza)
    for paso, estado, pos, leido, escribe, mueve, nuevo in traza:
        print(f"  paso {paso + 1}: {estado:>6} en la celda {pos:>2} lee {leido}, escribe {escribe},"
              f" va a la {'izquierda' if mueve < 0 else 'derecha'}, pasa a {nuevo}")
    print(f"  pasos: {len(traza)} = 2·t(7) + 2 = 2·3 + 2; valor final {cinta.valor()},"
          f" cabezal en la celda {cinta.cabezal}")
    print()


def tabla_totales():
    print("Tabla 2. Pasos de m incrementos desde 0")
    print(f"{'m':>9} {'total medido':>13} {'4m - 2·popcount(m)':>19} {'4m':>9} {'total / m':>10}"
          f" {'peor incremento':>16} {'2⌊log2 m⌋ + 2':>14} {'cabezal en el MSB':>18}")
    for m in [1, 2, 3, 8, 15, 16, 100, 1000, 10**4, 10**5]:
        reales, _, _ = correr(m)
        msb = total_msb(m) if m <= 10**4 else None
        print(f"{m:>9} {sum(reales):>13} {total_teorico(m):>19} {4 * m:>9} {sum(reales) / m:>10.4f}"
              f" {max(reales):>16} {2 * (m.bit_length() - 1) + 2:>14}"
              f" {'' if msb is None else msb:>18}")
    print()


# ---------------------------------------------------------------------------
# Figuras
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


def figura_costos(plt, destino, m=64):
    reales, potenciales, amortizados = correr(m)
    fig, (arriba, abajo) = plt.subplots(2, 1, figsize=(9, 5.4), sharex=True,
                                        gridspec_kw={"height_ratios": [3, 2]})
    xs = list(range(1, m + 1))
    arriba.bar(xs, reales, 0.75, color=NARANJA, label="pasos reales del incremento")
    arriba.plot(xs, amortizados, color=AZUL, label="costo amortizado = real + ΔΦ = 4")
    arriba.set_ylabel("pasos")
    arriba.set_title(f"{m} incrementos desde 0: picos de 2⌊log₂ m⌋ + 2, amortizado plano")
    arriba.legend(loc="upper left")
    abajo.step([0] + xs, potenciales, where="post", color=AQUA)
    abajo.set_ylabel("Φ = 2·unos")
    abajo.set_xlabel("incremento número")
    for k in [16, 32, 64]:
        if k <= m:
            arriba.text(k, reales[k - 1] + 0.4, f"{k - 1} → {k}", ha="center", fontsize=8,
                        color=TINTA_2)
    arriba.set_ylim(0, 19)
    fig.savefig(destino / "ejercicio-04-costos.png")
    plt.close(fig)


def figura_totales(plt, destino):
    ms = list(range(1, 1025))
    reales, _, _ = correr(1024)
    acumulado = []
    s = 0
    for c in reales:
        s += c
        acumulado.append(s)
    msb = []
    cinta = Cinta()
    s = 0
    for _ in ms:
        cinta.cabezal = min(cinta.celdas)
        s += incrementar(cinta, TRANSICIONES_MSB, inicial="ir")
        msb.append(s)
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.plot(ms, [a / m for a, m in zip(msb, ms)], color=NARANJA,
            label="cabezal en el bit más significativo: Θ(log m) por incremento")
    ax.plot(ms, [a / m for a, m in zip(acumulado, ms)], color=AZUL,
            label="cabezal en el bit menos significativo: total/m = 4 − 2·popcount(m)/m")
    ax.axhline(4, color=TENUE, linewidth=1, linestyle=(0, (4, 3)))
    ax.text(1100 * 0.62, 4.25, "4", color=TINTA_2)
    ax.set_xscale("log", base=2)
    ax.set_xlabel("m (incrementos)")
    ax.set_ylabel("pasos por incremento, en promedio sobre m")
    ax.set_title("Dónde vive el cabezal decide si el total es Θ(m) o Θ(m log m)")
    ax.legend(loc="upper left")
    fig.savefig(destino / "ejercicio-04-cabezal.png")
    plt.close(fig)


def figuras():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    _estilo(plt)
    destino = Path(__file__).resolve().parent.parent / "figuras"
    destino.mkdir(exist_ok=True)
    figura_costos(plt, destino)
    figura_totales(plt, destino)
    print(f"figuras escritas en {destino}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    tabla_traza()
    tabla_totales()
    if "--figuras" in sys.argv:
        figuras()
