"""Ejercicio 4 del Tema 1: el contador binario en una máquina de Turing de una cinta.

    python ejercicio-04.py

Imprime todas las tablas que cita ejercicio-04.md, corre las pruebas y regenera las
tres figuras (ejercicio-04-espacio-tiempo.svg, ejercicio-04-potencial.svg y
ejercicio-04-cabezal.svg). Cada número que aparece en la prosa sale de aquí. Solo
necesita matplotlib.
"""

import math

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt


# --------------------------------------------------------------------------
# 1. La máquina
# --------------------------------------------------------------------------
# La cinta es un diccionario posición -> símbolo; lo que no está es blanco. El número
# se escribe con el bit más significativo a la izquierda y el menos significativo en
# la posición 0. La celda 1, a la derecha del bit menos significativo, queda en blanco
# y le sirve a la máquina para encontrar el camino de vuelta.

BLANCO = "□"

# delta[(estado, símbolo leído)] = (símbolo que escribe, movimiento, estado nuevo)
INCREMENTAR = {
    ("carry", "1"): ("0", -1, "carry"),      # 1 + acarreo = 0, el acarreo sigue
    ("carry", "0"): ("1", +1, "back"),       # 0 + acarreo = 1, se acabó
    ("carry", BLANCO): ("1", +1, "back"),    # el número crece un bit
    ("back", "0"): ("0", +1, "back"),        # la vuelta solo pisa los ceros que
    ("back", BLANCO): (BLANCO, -1, "halt"),     # dejó el acarreo; el blanco de la
}                                                # derecha marca el final

# La variante con el cabezal en el bit MÁS significativo: tiene que ir hasta el final
# del número, sumar, y volver al principio.
INCREMENTAR_DESDE_MSB = {
    ("go", "0"): ("0", +1, "go"),
    ("go", "1"): ("1", +1, "go"),
    ("go", BLANCO): (BLANCO, -1, "carry"),
    ("carry", "1"): ("0", -1, "carry"),
    ("carry", "0"): ("1", -1, "back"),
    ("carry", BLANCO): ("1", -1, "back"),
    ("back", "0"): ("0", -1, "back"),
    ("back", "1"): ("1", -1, "back"),
    ("back", BLANCO): (BLANCO, +1, "halt"),
}


def correr(delta, cinta, cabezal, estado, traza=None):
    """Aplica la función de transición hasta llegar al estado 'halt'. Modifica la cinta
    y devuelve (posición final del cabezal, cantidad de pasos)."""
    pasos = 0
    while estado != "halt":
        leido = cinta.get(cabezal, BLANCO)
        if traza is not None:
            traza.append((estado, cabezal, dict(cinta)))
        escribe, mueve, estado = delta[(estado, leido)]
        if escribe == BLANCO:
            cinta.pop(cabezal, None)
        else:
            cinta[cabezal] = escribe
        cabezal += mueve
        pasos += 1
    if traza is not None:
        traza.append((estado, cabezal, dict(cinta)))
    return cabezal, pasos


def leer(cinta):
    return "".join(cinta[p] for p in sorted(cinta))


def unos_finales(v):
    # cuántos unos tiene v al final de su escritura en binario
    t = 0
    while v & 1:
        v, t = v >> 1, t + 1
    return t


def unos(v):
    return bin(v).count("1")


class Contador:
    """La máquina con el cabezal en el bit menos significativo, empezando en 0."""

    def __init__(self):
        self.cinta, self.cabezal, self.valor = {0: "0"}, 0, 0

    def incrementar(self, traza=None):
        self.cabezal, pasos = correr(INCREMENTAR, self.cinta, self.cabezal, "carry",
                                     traza)
        self.valor += 1
        return pasos

    def potencial(self):
        return 2 * sum(1 for s in self.cinta.values() if s == "1")


class ContadorDesdeMSB:
    """La variante con el cabezal en el bit más significativo."""

    def __init__(self):
        self.cinta, self.cabezal, self.valor = {0: "0"}, 0, 0

    def incrementar(self):
        self.cabezal, pasos = correr(INCREMENTAR_DESDE_MSB, self.cinta, self.cabezal, "go")
        self.valor += 1
        return pasos


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
    seccion("§2. Los primeros diez incrementos, con dos potenciales")
    c = Contador()
    print(f"{'de':>5} {'a':>5} {'t':>2} {'pasos':>6} {'unos antes':>11} "
          f"{'unos después':>13} {'amort. con unos':>16} {'amort. con 2·unos':>18}")
    for _ in range(10):
        antes_bits, antes_unos = leer(c.cinta), c.potencial() // 2
        t = unos_finales(c.valor)
        pasos = c.incrementar()
        despues_unos = c.potencial() // 2
        print(f"{antes_bits:>5} {leer(c.cinta):>5} {t:>2} {pasos:>6} {antes_unos:>11} "
              f"{despues_unos:>13} {pasos + despues_unos - antes_unos:>16} "
              f"{pasos + 2 * (despues_unos - antes_unos):>18}")


def traza_de_un_incremento():
    seccion("§3. Un incremento caro, paso a paso: 10111 + 1")
    c = Contador()
    while c.valor < 23:
        c.incrementar()
    traza = []
    pasos = c.incrementar(traza)
    for k, (estado, cabezal, cinta) in enumerate(traza):
        celdas = range(-5, 2)
        fila = " ".join(f"[{cinta.get(p, BLANCO)}]" if p == cabezal else
                        f" {cinta.get(p, BLANCO)} " for p in celdas)
        print(f"{k:>2} {estado:>8}  {fila}")
    print(f"{pasos} pasos = 2·3 + 2, y el cabezal termina en la posición {c.cabezal}")
    return traza


def costo_por_incremento():
    seccion("§3. Costo de cada incremento: 2t + 2")
    c = Contador()
    bien = 0
    for v in range(1 << 16):
        assert c.incrementar() == 2 * unos_finales(v) + 2
        bien += 1
    print(f"en los {miles(bien)} incrementos de 0 a {miles(1 << 16)}, cada uno costó "
          f"exactamente 2t + 2 pasos")


def totales():
    seccion("§5. Costo total de m incrementos desde 0")
    print(f"{'m':>8} {'total medido':>13} {'4m - 2·unos(m)':>15} {'total / m':>10} "
          f"{'incremento más caro':>20} {'2·floor(log2 m) + 2':>20}")
    c, total, mas_caro = Contador(), 0, 0
    marcas = {10, 100, 1000, 10**4, 65_536, 10**5}
    for m in range(1, 10**5 + 1):
        p = c.incrementar()
        total += p
        mas_caro = max(mas_caro, p)
        assert total == 4 * m - 2 * unos(m)
        if m in marcas:
            print(f"{miles(m):>8} {miles(total):>13} {miles(4 * m - 2 * unos(m)):>15} "
                  f"{total / m:>10.4f} {mas_caro:>20} "
                  f"{2 * int(math.log2(m)) + 2:>20}")
    print("la fórmula 4m - 2·unos(m) se cumple para todo m de 1 a 100 000")


def potencial_vigilado():
    seccion("§5. El potencial 2·(unos en la cinta), vigilado con assert")
    c = Contador()
    assert c.potencial() == 0
    for _ in range(1 << 16):
        antes = c.potencial()
        pasos = c.incrementar()
        assert pasos + c.potencial() - antes == 4
        assert c.potencial() >= 0
    print(f"costo amortizado = 4 en los {miles(1 << 16)} incrementos; "
          f"el potencial empieza en 0 y nunca es negativo")


def desde_msb():
    seccion("§6. Si el cabezal empieza en el bit más significativo")
    print(f"{'m':>8} {'total, desde el menos signif.':>30} {'total, desde el más signif.':>28} "
          f"{'por incremento':>15} {'2·log2 m':>9}")
    medidas = []
    c1, c2 = Contador(), ContadorDesdeMSB()
    t1 = t2 = 0
    marcas = {2**k for k in range(4, 17, 2)}
    for m in range(1, (1 << 16) + 1):
        t1 += c1.incrementar()
        bits = len(leer(c2.cinta))
        p2 = c2.incrementar()
        assert p2 == 2 * bits + 2 + (m - 1 == (1 << bits) - 1)
        t2 += p2
        assert leer(c2.cinta) == bin(m)[2:] and c2.cabezal == min(c2.cinta)
        if m in marcas:
            medidas.append((m, t1 / m, t2 / m))
            print(f"{miles(m):>8} {miles(t1):>30} {miles(t2):>28} {t2 / m:>15.2f} "
                  f"{2 * math.log2(m):>9.1f}")
    print(f"cada uno de los {miles(1 << 16)} incrementos costó 2b + 2 pasos, o 2b + 3 "
          f"si sus b bits eran unos")
    return medidas


# --------------------------------------------------------------------------
# 3. Pruebas
# --------------------------------------------------------------------------

def pruebas():
    seccion("Pruebas")
    comprobaciones = 0

    # (a) la cinta dice el número en binario y el cabezal vuelve a la posición 0
    c = Contador()
    for k in range(1, (1 << 16) + 1):
        c.incrementar()
        assert leer(c.cinta) == bin(k)[2:] and c.cabezal == 0
        assert sorted(c.cinta) == list(range(1 - len(c.cinta), 1))
        assert c.cinta.get(1, BLANCO) == BLANCO
        comprobaciones += 1

    # (b) cada par (estado, símbolo) que aparece en una ejecución tiene transición, y
    #     en 1024 incrementos se usan las cinco
    usados = set()
    c = Contador()
    for _ in range(1 << 10):
        traza = []
        c.incrementar(traza)
        for estado, cabezal, cinta in traza[:-1]:
            usados.add((estado, cinta.get(cabezal, BLANCO)))
    assert usados == set(INCREMENTAR)
    comprobaciones += 1

    # (c) costo por incremento, total exacto y costo amortizado
    c, total = Contador(), 0
    for v in range(1 << 16):
        antes = c.potencial()
        p = c.incrementar()
        total += p
        assert p == 2 * unos_finales(v) + 2
        assert p + c.potencial() - antes == 4
        assert total == 4 * (v + 1) - 2 * unos(v + 1)
        comprobaciones += 3

    # (d) la variante desde el bit más significativo: correcta, y cada incremento
    #     cuesta al menos la cantidad de bits del número
    c = ContadorDesdeMSB()
    for v in range(1 << 14):
        bits = len(leer(c.cinta))
        p = c.incrementar()
        assert leer(c.cinta) == bin(v + 1)[2:] and c.cabezal == min(c.cinta)
        assert sorted(c.cinta) == list(range(1 - len(c.cinta), 1))
        assert p >= bits
        comprobaciones += 2

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
        "figure.facecolor": "white", "svg.hashsalt": "ejercicio-04",
    })


def _guardar(fig, nombre):
    fig.tight_layout()
    fig.savefig(nombre, metadata={"Date": None})
    plt.close(fig)


def figura_espacio_tiempo(traza):
    celdas = list(range(-5, 2))
    fig, ax = plt.subplots(figsize=(5.6, 4.0))
    colores = {"carry": CALIDO, "back": OSCURO, "halt": APAGADO}
    for k, (estado, cabezal, cinta) in enumerate(traza):
        y = -k
        for p in celdas:
            s = cinta.get(p, BLANCO)
            es_cabezal = p == cabezal
            ax.add_patch(plt.Rectangle((p - 0.45, y - 0.4), 0.9, 0.8,
                                       facecolor=colores[estado] if es_cabezal else "white",
                                       edgecolor=REGLA if not es_cabezal else colores[estado],
                                       lw=0.8))
            ax.text(p, y, s, ha="center", va="center", fontsize=9,
                    color="white" if es_cabezal else (TINTA if s != BLANCO else REGLA))
        ax.text(-6.0, y, f"{k}", ha="right", va="center", fontsize=8, color=APAGADO)
        ax.text(2.0, y, estado, ha="left", va="center", fontsize=8, color=colores[estado])
    ax.text(-6.0, 0.9, "paso", ha="right", fontsize=8, color=APAGADO)
    ax.text(0, 0.9, "bit menos\nsignificativo", ha="center", fontsize=7, color=APAGADO)
    ax.set_xlim(-6.6, 3.6)
    ax.set_ylim(-len(traza) + 0.3, 1.7)
    ax.set_aspect("equal")
    ax.axis("off")
    _guardar(fig, "ejercicio-04-espacio-tiempo.svg")


def figura_potencial():
    m = 64
    c, reales, pot = Contador(), [], []
    for _ in range(m):
        reales.append(c.incrementar())
        pot.append(c.potencial())
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.6, 3.8), sharex=True,
                                   gridspec_kw={"height_ratios": [3, 2]})
    xs = range(1, m + 1)
    ax1.bar(xs, reales, color=ACENTO, width=0.8, label="pasos reales")
    ax1.axhline(4, color=ALARMA, lw=1.4, label="costo amortizado = 4")
    ax1.set_ylabel("pasos")
    ax1.legend(frameon=False, fontsize=8, loc="upper left")
    ax2.plot(xs, pot, color=OSCURO, lw=1.4, drawstyle="steps-mid")
    ax2.set_ylabel("potencial\n2·(unos)")
    ax2.set_xlabel("incremento")
    for ax in (ax1, ax2):
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", color=REGLA, lw=0.6)
        ax.set_axisbelow(True)
    _guardar(fig, "ejercicio-04-potencial.svg")


def figura_cabezal(medidas):
    fig, ax = plt.subplots(figsize=(6.4, 3.0))
    ms = [m for m, _, _ in medidas]
    ax.plot(ms, [b for _, _, b in medidas], "o-", color=ALARMA, lw=1.4, ms=4,
            label="cabezal en el bit más significativo")
    ax.plot(ms, [a for _, a, _ in medidas], "o-", color=OSCURO, lw=1.4, ms=4,
            label="cabezal en el bit menos significativo")
    ax.axhline(4, color=OSCURO, lw=0.8, ls=":")
    ax.set_xscale("log", base=2)
    ax.set_xlabel("m, cantidad de incrementos")
    ax.set_ylabel("pasos por incremento")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(color=REGLA, lw=0.6)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    _guardar(fig, "ejercicio-04-cabezal.svg")


if __name__ == "__main__":
    ejemplo_chico()
    traza = traza_de_un_incremento()
    costo_por_incremento()
    totales()
    potencial_vigilado()
    medidas = desde_msb()
    pruebas()
    _estilo()
    figura_espacio_tiempo(traza)
    figura_potencial()
    figura_cabezal(medidas)
    print("\nfiguras: ejercicio-04-espacio-tiempo.svg, ejercicio-04-potencial.svg, "
          "ejercicio-04-cabezal.svg")
