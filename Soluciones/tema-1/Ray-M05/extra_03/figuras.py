import sys
from pathlib import Path

from matplotlib.patches import Rectangle

from comun import estilo
from comun.estilo import SERIES, TEXTO, TEXTO_2
from pila import PilaConMinimo

AZUL = SERIES[0]
CARPETA = Path(__file__).resolve().parent

OPERACIONES = [("+", 5), ("+", 3), ("+", 7), ("+", 3), ("+", 1),
               ("-",), ("-",), ("-",), ("+", 4), ("-",), ("-",)]
ALTO, SEP = 0.62, 0.78


def estados():
    pila = PilaConMinimo()

    def nodos():
        lista, nodo = [], pila.cima
        while nodo is not None:
            lista.append((nodo[0], nodo[1]))
            nodo = nodo[2]
        return lista[::-1]

    cuadros = [([], "La pila empieza vacía.")]
    for op in OPERACIONES:
        if op[0] == "+":
            x = op[1]
            debajo = None if pila.vacia() else pila.minimo()
            pila.apilar(x)
            if debajo is None:
                texto = f"apilar({x}): es el único nodo,\nsu mínimo es {x}."
            else:
                texto = (f"apilar({x}): el mínimo del nodo nuevo\n"
                         f"es min({x}, {debajo}) = {pila.minimo()},\n"
                         f"con una sola comparación.")
        else:
            x = pila.desapilar()
            texto = f"desapilar() → {x}: el nodo se va\ny el de abajo ya tenía su mínimo."
            if pila.vacia():
                texto = f"desapilar() → {x}: la pila queda vacía."
        if not pila.vacia():
            texto += f"\n\nminimo() = {pila.minimo()}: se lee en el tope,\nsin recorrer nada."
        cuadros.append((nodos(), texto))
    return cuadros


def animacion():
    estilo.aplicar()
    fig, ax = estilo.figura(8, 4.4)
    ax.axis("off")
    ax.set_xlim(-0.3, 8.4)
    ax.set_ylim(-0.75, 4.45)
    ax.set_title("Pila con mínimo: cada nodo guarda el mínimo de lo que tiene debajo", pad=4)
    ax.text(0.8, -0.45, "valor", ha="center", va="center", fontsize=9, color=TEXTO_2)
    ax.text(2.5, -0.45, "mínimo hasta el fondo", ha="center", va="center", fontsize=9,
            color=TEXTO_2)
    ax.plot([-0.1, 3.4], [-0.15, -0.15], color=TEXTO_2, linewidth=2)

    cuadros = estados()
    filas_max = max(len(n) for n, _ in cuadros)
    celdas = []
    for i in range(filas_max):
        y = i * SEP
        valor = Rectangle((0, y), 1.6, ALTO, facecolor="white", edgecolor=TEXTO_2)
        minimo = Rectangle((1.7, y), 1.6, ALTO, facecolor="white", edgecolor=TEXTO_2)
        for r in (valor, minimo):
            ax.add_patch(r)
        tv = ax.text(0.8, y + ALTO / 2, "", ha="center", va="center", fontsize=11)
        tm = ax.text(2.5, y + ALTO / 2, "", ha="center", va="center", fontsize=11)
        celdas.append((valor, minimo, tv, tm))
    estado = ax.text(3.9, 4.1, "", ha="left", va="top", fontsize=10, color=TEXTO,
                     linespacing=1.4)

    def actualizar(k):
        nodos, texto = cuadros[k]
        for i, (valor, minimo, tv, tm) in enumerate(celdas):
            visible = i < len(nodos)
            for a in (valor, minimo, tv, tm):
                a.set_visible(visible)
            if visible:
                tv.set_text(str(nodos[i][0]))
                tm.set_text(str(nodos[i][1]))
                arriba = i == len(nodos) - 1
                minimo.set_facecolor((*_rgb(AZUL), 0.3) if arriba else "white")
                for r in (valor, minimo):
                    r.set_linewidth(2.5 if arriba else 1)
                    r.set_edgecolor(TEXTO if arriba else TEXTO_2)
        estado.set_text(texto)

    moviles = [a for fila in celdas for a in fila] + [estado]
    fig.tight_layout()
    print(estilo.guardar_gif(fig, moviles, actualizar, len(cuadros),
                             CARPETA / "pila.gif", "pila con mínimo animada",
                             fps=0.6, pausa=3.0))


def _rgb(hexa):
    return tuple(int(hexa[k:k + 2], 16) / 255 for k in (1, 3, 5))


FIGURAS = {"animacion": animacion}

if __name__ == "__main__":
    FIGURAS[sys.argv[1]]()
