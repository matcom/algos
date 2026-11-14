import math
import sys
from pathlib import Path

from matplotlib.patches import Circle, FancyArrowPatch

from comun import estilo
from comun.estilo import SERIES, TEXTO, TEXTO_2
from floyd import vueltas_formula

AZUL, NARANJA = SERIES[0], SERIES[1]
CARPETA = Path(__file__).resolve().parent
COLA, CICLO = 3, 7


def _coordenadas():
    radio = CICLO / (2 * math.pi) * 1.15
    centro = (COLA + radio, 0.0)
    puntos = [(float(i), 0.0) for i in range(COLA)]
    for k in range(CICLO):
        angulo = math.pi - 2 * math.pi * k / CICLO
        puntos.append((centro[0] + radio * math.cos(angulo), radio * math.sin(angulo)))
    return puntos


def _nodo(k):
    return k if k < COLA else COLA + (k - COLA) % CICLO


def animacion():
    puntos = _coordenadas()
    estilo.aplicar()
    fig, ax = estilo.figura(8, 4.2)
    ax.axis("off")
    ax.set_aspect("equal")
    ax.set_xlim(-0.8, 9.6)
    ax.set_ylim(-2.0, 2.2)
    ax.set_title("Floyd: a₁ avanza un nodo por vuelta, a₂ avanza dos", pad=4)

    siguientes = list(range(1, COLA + CICLO)) + [COLA]
    for i, (x, y) in enumerate(puntos):
        ax.add_patch(Circle((x, y), 0.22, facecolor="white", edgecolor=TEXTO_2, zorder=2))
        ax.text(x, y, str(i), ha="center", va="center", fontsize=8, color=TEXTO_2, zorder=3)
        destino = puntos[siguientes[i]]
        ax.add_patch(FancyArrowPatch((x, y), destino, arrowstyle="-|>", mutation_scale=9,
                                     shrinkA=9, shrinkB=9, color=TEXTO_2, linewidth=1))
    ax.text(1.0, -0.65, f"cola: μ = {COLA}", ha="center", fontsize=9, color=TEXTO_2)
    ax.text(puntos[COLA][0] + CICLO / (2 * math.pi) * 1.15, -0.1, f"ciclo\nλ = {CICLO}",
            ha="center", va="center", fontsize=9, color=TEXTO_2)

    p1 = ax.plot([], [], "o", color=AZUL, markersize=13, alpha=0.85, zorder=4)[0]
    p2 = ax.plot([], [], "o", color=NARANJA, markersize=13, alpha=0.85, zorder=4)[0]
    texto = ax.text(-0.6, -1.6, "", ha="left", va="top", fontsize=10, color=TEXTO,
                    linespacing=1.4)
    ax.plot([], [], "o", color=AZUL, label="a₁: pos(j)")
    ax.plot([], [], "o", color=NARANJA, label="a₂: pos(2j)")
    ax.legend(loc="upper left", bbox_to_anchor=(0.0, 1.0))

    j_final = vueltas_formula(COLA, CICLO)
    cuadros = [(0, 0, 0)]
    for j in range(1, j_final + 1):
        cuadros.append((j, j, 2 * j - 1))
        cuadros.append((j, j, 2 * j))

    def potencial(j):
        return COLA - j + CICLO if j < COLA else CICLO - j % CICLO

    def actualizar(i):
        j, pt, pl = cuadros[i]
        xt, yt = puntos[_nodo(pt)]
        xl, yl = puntos[_nodo(pl)]
        p1.set_data([xt - 0.08], [yt + 0.08])
        p2.set_data([xl + 0.08], [yl - 0.08])
        if j == 0:
            linea = "Las dos salen de la cabeza."
        elif j == j_final and pl == 2 * j:
            linea = (f"Vuelta {j}: se encuentran en el nodo {_nodo(j)}: "
                     f"j = {j} es múltiplo de λ = {CICLO} y es ≥ μ = {COLA}.")
        elif pt < COLA:
            linea = f"Vuelta {j}: a₁ todavía está en la cola.  Φ = μ − j + λ = {potencial(j)}"
        else:
            linea = (f"Vuelta {j}: los dos en el ciclo; a₂ está {(-j) % CICLO} nodos detrás de a₁.  "
                     f"Φ = λ − (j mod λ) = {potencial(j)}")
        texto.set_text(linea)

    fig.tight_layout()
    print(estilo.guardar_gif(fig, [p1, p2, texto], actualizar, len(cuadros),
                             CARPETA / "floyd.gif", "los dos punteros sobre la lista",
                             fps=1.6, pausa=3.5))


FIGURAS = {"animacion": animacion}

if __name__ == "__main__":
    FIGURAS[sys.argv[1]]()
