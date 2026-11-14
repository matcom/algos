import random
import sys
from pathlib import Path

from matplotlib.patches import Rectangle

from comun import estilo
from comun.estilo import SERIES, TEXTO, TEXTO_2
from extra_10.cercano import par_cercano_rejilla

AZUL, NARANJA = SERIES[0], SERIES[1]
CARPETA = Path(__file__).resolve().parent

PUNTOS = [4, 12, 19, 30, 40, 60, 81, 85, 89, 93]
SEMILLA = 1059
ANCHO = 110


def _claro(hexa, alfa):
    return tuple(1 - alfa * (1 - int(hexa[k:k + 2], 16) / 255) for k in (1, 3, 5))


def cuadros():
    traza = []
    d, _, _ = par_cercano_rejilla(PUNTOS, random.Random(SEMILLA), traza)
    p, pasos = traza[0], traza[1:]
    delta = abs(p[1] - p[0])
    salida = [(2, delta, None, None, None,
               f"Orden al azar: {', '.join(map(str, p))}.",
               f"Con los dos primeros, δ = |{p[1]} − {p[0]}| = {delta}: celdas de largo {delta}, "
               f"una por punto.")]
    for i, delta, c, mejor in pasos:
        x = p[i]
        salida.append((i, delta, x, c, None,
                       f"Punto {i + 1}: x = {x}, su celda es ⌊{x}/{delta}⌋ = {c}.",
                       f"Todo punto a menos de δ = {delta} está en las celdas {c - 1}, {c} o {c + 1}: "
                       f"3 accesos a la tabla."))
        if mejor is not None and abs(x - p[mejor]) < delta:
            nuevo = abs(x - p[mejor])
            salida.append((i + 1, nuevo, x, None, (p[mejor], x),
                           f"{p[mejor]} está a {nuevo} < {delta}: δ baja a {nuevo}.",
                           f"Se reconstruye la rejilla con celdas de largo {nuevo}: costo O({i + 1})."))
        else:
            cerca = f"el más cercano, {p[mejor]}, está a {abs(x - p[mejor])}" if mejor is not None \
                else "las tres están vacías"
            salida.append((i + 1, delta, x, None, None,
                           f"No hay nada a menos de {delta} ({cerca}).",
                           f"δ no cambia: {x} entra en su celda, costo O(1)."))
    r = sum(1 for _, delta, _, _, _, l1, _ in salida if "baja a" in l1)
    salida.append((len(p), d, None, None, None,
                   f"Resultado: δ = {d}, con {r} reconstrucciones.",
                   "Cada celda tuvo siempre a lo sumo un punto."))
    return p, salida


def animacion():
    p, lista = cuadros()
    estilo.aplicar()
    fig, ax = estilo.figura(9, 3.4)
    ax.axis("off")
    ax.set_xlim(-3, ANCHO + 1)
    ax.set_ylim(-2.3, 1.2)
    ax.set_title("Par más cercano en una dimensión: la rejilla de C2, §9", pad=4)
    ax.plot([0, ANCHO], [0, 0], color=TEXTO_2, linewidth=1)

    bloque = Rectangle((0, -0.35), 0, 0.7, facecolor=_claro(NARANJA, 0.18), edgecolor="none")
    centro = Rectangle((0, -0.35), 0, 0.7, facecolor=_claro(NARANJA, 0.4), edgecolor="none")
    ax.add_patch(bloque)
    ax.add_patch(centro)
    marcas = [ax.plot([], [], color=TEXTO_2, linewidth=0.8)[0] for _ in range(ANCHO + 2)]
    par = ax.plot([], [], color=NARANJA, linewidth=3)[0]
    puntos = {x: ax.plot([x], [0], "o", markersize=8, color=AZUL)[0] for x in p}
    rotulos = {x: ax.text(x, -0.6, str(x), ha="center", va="center", fontsize=8, color=TEXTO)
               for x in p}
    linea1 = ax.text(-1, -1.2, "", ha="left", va="center", fontsize=9.5, color=TEXTO)
    linea2 = ax.text(-1, -1.7, "", ha="left", va="center", fontsize=9.5, color=TEXTO_2)

    def actualizar(k):
        insertados, delta, nuevo, celda, marcado, l1, l2 = lista[k]
        hechos = set(p[:insertados])
        for x, pt in puntos.items():
            visible = x in hechos or x == nuevo
            pt.set_visible(visible)
            rotulos[x].set_visible(visible)
            pt.set_color(NARANJA if x == nuevo else AZUL)
        for m, ln in enumerate(marcas):
            if m * delta <= ANCHO:
                ln.set_data([m * delta, m * delta], [-0.3, 0.3])
            else:
                ln.set_data([], [])
        if celda is None:
            bloque.set_width(0)
            centro.set_width(0)
        else:
            bloque.set_x((celda - 1) * delta)
            bloque.set_width(3 * delta)
            centro.set_x(celda * delta)
            centro.set_width(delta)
        par.set_data(marcado if marcado else [], [0.5, 0.5] if marcado else [])
        linea1.set_text(l1)
        linea2.set_text(l2)

    moviles = [bloque, centro] + marcas + [par] + list(puntos.values()) + list(rotulos.values()) \
        + [linea1, linea2]
    fig.tight_layout()
    print(estilo.guardar_gif(fig, moviles, actualizar, len(lista),
                             CARPETA / "rejilla.gif", "la rejilla en una dimensión",
                             fps=0.8, pausa=5.0))


FIGURAS = {"animacion": animacion}

if __name__ == "__main__":
    FIGURAS[sys.argv[1]]()
