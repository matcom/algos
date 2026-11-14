import sys
from pathlib import Path

from matplotlib.patches import FancyBboxPatch

from comun import estilo
from comun.estilo import SERIES, TEXTO, TEXTO_2
from extra_12.gale_shapley import gale_shapley_incompleto

AZUL, NARANJA = SERIES[0], SERIES[1]
GRIS = "#b9b8b3"
CARPETA = Path(__file__).resolve().parent
SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")

PREF_A = [[0, 1], [0], [0, 2], [1]]
PREF_B = [[2, 1, 0, 3], [0, 3, 1, 2], [0, 1, 2, 3], [0, 1, 2, 3]]


def _a(k):
    return f"a{str(k + 1).translate(SUB)}"


def _b(k):
    return f"b{str(k + 1).translate(SUB)}"


def _claro(hexa, alfa):
    return tuple(1 - alfa * (1 - int(hexa[k:k + 2], 16) / 255) for k in (1, 3, 5))


def cuadros():
    traza = []
    gale_shapley_incompleto(PREF_A, PREF_B, traza)
    n = len(PREF_A)
    pareja_de_b = [None] * len(PREF_B)
    hechas = [0] * n
    solos = {a for a in range(n) if not PREF_A[a]}
    fi = sum(len(lista) for lista in PREF_A)
    salida = [(list(pareja_de_b), list(hechas), set(solos), None, fi,
               "Cada proponente lista solo a algunos receptores; los receptores ordenan a todos.",
               f"Φ = pares (a, b) con b en la lista de a a los que a todavía no propuso = {fi}.")]
    for a, b, rechazado in traza:
        hechas[a] += 1
        fi -= 1
        salida.append((list(pareja_de_b), list(hechas), set(solos), (a, b), fi,
                       f"{_a(a)} le propone a {_b(b)}, el siguiente de su lista.",
                       f"Φ baja a {fi}."))
        pareja_de_b[b] = a if rechazado != a else pareja_de_b[b]
        if rechazado is None:
            l1 = f"{_b(b)} estaba sola: acepta a {_a(a)}."
        elif rechazado == a:
            l1 = f"{_b(b)} prefiere a {_a(pareja_de_b[b])}: rechaza a {_a(a)}."
        else:
            l1 = f"{_b(b)} prefiere a {_a(a)} antes que a {_a(rechazado)}: lo cambia."
        if rechazado is not None and hechas[rechazado] == len(PREF_A[rechazado]):
            solos.add(rechazado)
            l2 = f"{_a(rechazado)} agotó su lista: queda solo, antes que con alguien que no listó."
        elif rechazado is not None:
            l2 = f"{_a(rechazado)} queda libre y sigue con su lista."
        else:
            l2 = f"Φ = {fi}."
        salida.append((list(pareja_de_b), list(hechas), set(solos), None, fi, l1, l2))
    salida.append((list(pareja_de_b), list(hechas), set(solos), None, fi,
                   f"Fin: {len(traza)} propuestas, Φ terminó en {fi} (a₃ nunca tuvo que proponerle a b₃).",
                   "a₂ y a₄ quedan solos, b₃ y b₄ quedan solas, y no hay ningún par bloqueante."))
    return salida


def animacion():
    lista = cuadros()
    n_a, n_b = len(PREF_A), len(PREF_B)
    estilo.aplicar()
    fig, ax = estilo.figura(9, 4.8)
    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(-1.9, 4.0)
    ax.set_title("Gale-Shapley con listas incompletas", pad=4)
    xa, xb = 3.2, 6.6
    y = lambda k: 3 - k

    nodos_a, nodos_b, nombres, entradas, solos_txt = [], [], [], [], []
    for k in range(n_a):
        r = FancyBboxPatch((xa - 0.3, y(k) - 0.22), 0.6, 0.44, boxstyle="round,pad=0.02",
                           facecolor="white", edgecolor=TEXTO_2)
        ax.add_patch(r)
        nodos_a.append(r)
        nombres.append(ax.text(xa, y(k), _a(k), ha="center", va="center", fontsize=11))
        fila = []
        for j, b in enumerate(PREF_A[k]):
            fila.append(ax.text(xa - 0.75 - 0.5 * (len(PREF_A[k]) - 1 - j), y(k), _b(b),
                                ha="center", va="center", fontsize=10, color=TEXTO))
        entradas.append(fila)
        solos_txt.append(ax.text(xa + 0.45, y(k) + 0.32, "", ha="left", va="center",
                                 fontsize=8, color=TEXTO_2))
    for k in range(n_b):
        r = FancyBboxPatch((xb - 0.3, y(k) - 0.22), 0.6, 0.44, boxstyle="round,pad=0.02",
                           facecolor="white", edgecolor=TEXTO_2)
        ax.add_patch(r)
        nodos_b.append(r)
        nombres.append(ax.text(xb, y(k), _b(k), ha="center", va="center", fontsize=11))
        ax.text(xb + 0.55, y(k), " ".join(_a(a) for a in PREF_B[k]), ha="left", va="center",
                fontsize=10, color=TEXTO_2)
    ax.text(xa - 1.3, 3.65, "lista de cada proponente", ha="center", fontsize=8, color=TEXTO_2)
    ax.text(xb + 1.45, 3.65, "lista de cada receptor", ha="center", fontsize=8, color=TEXTO_2)

    parejas = [ax.plot([], [], color=AZUL, linewidth=2.5)[0] for _ in range(n_b)]
    propuesta = ax.plot([], [], color=NARANJA, linewidth=2.5, linestyle=(0, (4, 2)))[0]
    fi_txt = ax.text(9.9, -0.75, "", ha="right", va="center", fontsize=11, fontweight="bold")
    linea1 = ax.text(0.1, -0.75, "", ha="left", va="center", fontsize=9.5, color=TEXTO)
    linea2 = ax.text(0.1, -1.3, "", ha="left", va="center", fontsize=9.5, color=TEXTO_2)

    def actualizar(c):
        pareja_de_b, hechas, solos, curso, fi, l1, l2 = lista[c]
        for b, ln in enumerate(parejas):
            a = pareja_de_b[b]
            if a is None:
                ln.set_data([], [])
            else:
                ln.set_data([xa + 0.3, xb - 0.3], [y(a), y(b)])
        if curso is None:
            propuesta.set_data([], [])
        else:
            a, b = curso
            propuesta.set_data([xa + 0.3, xb - 0.3], [y(a) + 0.08, y(b) + 0.08])
        con_pareja = {a for a in pareja_de_b if a is not None}
        for a in range(n_a):
            for j, t in enumerate(entradas[a]):
                t.set_color(GRIS if j < hechas[a] else TEXTO)
            nodos_a[a].set_facecolor(_claro(AZUL, 0.25) if a in con_pareja else
                                     (_claro(GRIS, 0.6) if a in solos else "white"))
            solos_txt[a].set_text("solo" if a in solos else "")
        for b in range(n_b):
            nodos_b[b].set_facecolor(_claro(AZUL, 0.25) if pareja_de_b[b] is not None else "white")
        fi_txt.set_text(f"Φ = {fi}")
        linea1.set_text(l1)
        linea2.set_text(l2)

    moviles = parejas + [propuesta] + nodos_a + nodos_b + nombres + \
        [t for fila in entradas for t in fila] + solos_txt + [fi_txt, linea1, linea2]
    fig.tight_layout()
    print(estilo.guardar_gif(fig, moviles, actualizar, len(lista),
                             CARPETA / "gale_shapley.gif", "Gale-Shapley con listas incompletas",
                             fps=0.7, pausa=5.0))


FIGURAS = {"animacion": animacion}

if __name__ == "__main__":
    FIGURAS[sys.argv[1]]()
