import sys
from pathlib import Path

from matplotlib.patches import Rectangle

from comun import estilo
from comun.estilo import SERIES, TEXTO, TEXTO_2
from matriz import escalera, familia, primera_columna_y_fila

AZUL, NARANJA = SERIES[0], SERIES[1]
CARPETA = Path(__file__).resolve().parent


def _rgb(hexa, alfa):
    return (*[int(hexa[k:k + 2], 16) / 255 for k in (1, 3, 5)], alfa)


def animacion():
    n = 6
    M = [[2 * (i + j) for j in range(1, n + 1)] for i in range(1, n + 1)]
    x = 2 * n + 1

    def comparar(i, j):
        return (x > M[i][j]) - (x < M[i][j])

    _, camino = escalera(n, comparar)

    cuadros = [(0, n - 1, None, f"x = {x}. Al principio puede estar en cualquier casilla.\n"
                                f"Φ = {n} filas + {n} columnas = {2 * n}")]
    fila, columna = 0, n - 1
    for k, (i, j) in enumerate(camino, start=1):
        cuadros.append((fila, columna, (i, j),
                        f"Comparación {k}: x = {x} contra la casilla ({i + 1}, {j + 1}), que vale {M[i][j]}."))
        if x < M[i][j]:
            columna -= 1
            texto = (f"x < {M[i][j]}: lo que queda de la columna {j + 1} es aún mayor y se descarta.\n"
                     f"Φ = {n - fila} filas + {columna + 1} columnas = {n - fila + columna + 1}")
        else:
            fila += 1
            texto = (f"x > {M[i][j]}: lo que queda de la fila {i + 1} es aún menor y se descarta.\n"
                     f"Φ = {n - fila} filas + {columna + 1} columnas = {n - fila + columna + 1}")
        cuadros.append((fila, columna, None, texto))
    cuadros.append((fila, columna, None,
                    f"No quedan casillas: x no está.\n{len(camino)} comparaciones = 2n − 1, "
                    f"el peor caso."))

    estilo.aplicar()
    fig, ax = estilo.figura(6.2, 6.2)
    ax.axis("off")
    ax.set_aspect("equal")
    ax.set_xlim(-0.6, n + 0.2)
    ax.set_ylim(-1.9, n + 0.9)
    ax.set_title("La escalera: cada comparación descarta una fila o una columna", pad=4)
    celdas = {}
    for i in range(n):
        for j in range(n):
            r = Rectangle((j, n - 1 - i), 0.95, 0.95, facecolor="white", edgecolor=TEXTO_2)
            ax.add_patch(r)
            celdas[i, j] = r
    valores = [ax.text(j + 0.475, n - 1 - i + 0.475, str(M[i][j]), ha="center", va="center",
                       fontsize=11) for i in range(n) for j in range(n)]
    for k in range(n):
        ax.text(-0.3, n - 1 - k + 0.475, str(k + 1), ha="center", va="center", fontsize=8,
                color=TEXTO_2)
        ax.text(k + 0.475, n + 0.2, str(k + 1), ha="center", va="center", fontsize=8,
                color=TEXTO_2)
    texto = ax.text(-0.5, -0.4, "", ha="left", va="top", fontsize=9.5, color=TEXTO, linespacing=1.5)

    def actualizar(c):
        fila, columna, actual, mensaje = cuadros[c]
        for (i, j), r in celdas.items():
            if i < fila:
                r.set_facecolor(_rgb(AZUL, 0.3))
            elif j > columna:
                r.set_facecolor(_rgb(NARANJA, 0.3))
            else:
                r.set_facecolor("white")
            r.set_linewidth(3 if (i, j) == actual else 1)
            r.set_edgecolor(TEXTO if (i, j) == actual else TEXTO_2)
        texto.set_text(mensaje)

    moviles = list(celdas.values()) + valores + [texto]
    fig.tight_layout()
    print(estilo.guardar_gif(fig, moviles, actualizar, len(cuadros),
                             CARPETA / "escalera.gif", "la escalera sobre la matriz",
                             fps=1.5, pausa=3.5))


def adversario():
    n = 8
    M, x = familia(n)
    estilo.aplicar()
    fig, ejes = estilo.figura(11, 5.4)
    fig.clf()
    ejes = fig.subplots(1, 2)

    def comparar(i, j):
        return (x > M[i][j]) - (x < M[i][j])

    paneles = [("escalera", escalera), ("primera columna y una fila", primera_columna_y_fila)]
    for ax, (nombre, algoritmo) in zip(ejes, paneles):
        _, camino = algoritmo(n, comparar)
        vistas = set(camino)
        faltan = [i for i in range(n) if (i, n - 1 - i) not in vistas]
        ax.axis("off")
        ax.set_aspect("equal")
        ax.set_xlim(-0.1, n + 0.1)
        ax.set_ylim(-0.9, n + 0.6)
        for i in range(n):
            for j in range(n):
                diagonal = i + j == n - 1
                trampa = diagonal and faltan and i == faltan[0]
                ax.add_patch(Rectangle((j, n - 1 - i), 0.95, 0.95,
                                       facecolor=_rgb(AZUL, 0.3) if diagonal else "white",
                                       edgecolor=TEXTO if (i, j) in vistas else REJILLA_SUAVE,
                                       linewidth=2.6 if (i, j) in vistas else 0.8))
                valor = x if trampa else M[i][j]
                ax.text(j + 0.475, n - 1 - i + 0.475, str(valor), ha="center", va="center",
                        fontsize=9, color=TEXTO, fontweight="bold" if trampa else "normal")
        ax.set_title(f"{nombre}: {len(camino)} comparaciones", fontsize=11)
        if faltan:
            i = faltan[0]
            ax.text(n / 2, -0.45, f"Nunca miró la casilla ({i + 1}, {n - i}): el adversario "
                    f"pone ahí x = {x}", ha="center", va="center", fontsize=9, color=TEXTO)
        else:
            ax.text(n / 2, -0.45, f"Compara las {n} casillas de la antidiagonal", ha="center",
                    va="center", fontsize=9, color=TEXTO)
    fig.suptitle(f"La matriz del adversario: fuera de la antidiagonal 2(i + j), "
                 f"en ella x − 1 = {x - 1}", x=0.02, ha="left", fontsize=12, fontweight="bold")
    print(estilo.guardar(fig, CARPETA / "adversario.png", "las casillas que mira cada algoritmo"))


REJILLA_SUAVE = "#c9c8c3"

FIGURAS = {"animacion": animacion, "adversario": adversario}

if __name__ == "__main__":
    FIGURAS[sys.argv[1]]()
