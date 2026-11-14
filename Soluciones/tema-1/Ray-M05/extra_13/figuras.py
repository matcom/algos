import math
import sys
from pathlib import Path

from comun import estilo
from comun.estilo import SERIES, TEXTO, TEXTO_2
from extra_13.splay import buscar, camino, potencial, splay, tamanos

AZUL, NARANJA = SERIES[0], SERIES[1]
CARPETA = Path(__file__).resolve().parent
N = 15


def _forma(raiz):
    prof, padre, pila = {}, {}, [(raiz, 0, None)]
    while pila:
        x, d, p = pila.pop()
        prof[x.clave], padre[x.clave] = d, p
        pila.extend((h, d + 1, x.clave) for h in (x.izq, x.der) if h)
    return prof, padre


def cuadros():
    raiz = camino(N)
    phi0 = potencial(raiz)
    salida = [(*_forma(raiz), None, f"Camino de {N} nodos: 15 en la raíz y 1 al fondo.",
               f"Φ inicial = log₂ {N}! ≈ {phi0:.1f}.")]
    total = 0
    for k in range(1, N + 1):
        x = buscar(raiz, k)
        cota = 3 * (math.log2(N) - math.log2(tamanos(x)[x])) + 1
        antes = potencial(raiz)
        costo = max(splay(x), 1)
        raiz = x
        amortizado = costo + potencial(raiz) - antes
        total += costo
        salida.append((*_forma(raiz), k,
                       f"Acceso a {k}: costo {costo}, amortizado {costo} + ΔΦ = {amortizado:.1f}, "
                       f"y el lema lo acota por {cota:.1f}.",
                       f"Costo acumulado: {total} en {k} acceso{'s' if k > 1 else ''}."))
    salida.append((*_forma(raiz), None,
                   f"Fin de la ronda: {total} rotaciones, {total / N:.1f} por acceso; "
                   f"la cota n(3 log₂ n + 1) da {N * (3 * math.log2(N) + 1):.0f}.",
                   f"El árbol volvió a ser el camino: Φ final = Φ inicial = {potencial(raiz):.1f}."))
    return salida


def animacion():
    lista = cuadros()
    estilo.aplicar()
    fig, ax = estilo.figura(9, 5.4)
    ax.axis("off")
    ax.set_xlim(0.2, N + 0.8)
    ax.set_ylim(-N - 2.6, 0.8)
    ax.set_title("Splay sobre un camino: una ronda de accesos en orden", pad=4)
    aristas = {k: ax.plot([], [], color=TEXTO_2, linewidth=1.2)[0] for k in range(1, N + 1)}
    nodos = {k: ax.plot([], [], "o", markersize=15, markerfacecolor="white",
                        markeredgecolor=TEXTO_2)[0] for k in range(1, N + 1)}
    rotulos = {k: ax.text(0, 0, str(k), ha="center", va="center", fontsize=8)
               for k in range(1, N + 1)}
    linea1 = ax.text(0.4, -N - 1.3, "", ha="left", va="center", fontsize=9.5, color=TEXTO)
    linea2 = ax.text(0.4, -N - 2.2, "", ha="left", va="center", fontsize=9.5, color=TEXTO_2)

    def actualizar(c):
        prof, padre, accedido, l1, l2 = lista[c]
        for k in range(1, N + 1):
            y = -prof[k]
            nodos[k].set_data([k], [y])
            nodos[k].set_markerfacecolor(NARANJA if k == accedido else
                                         ("#d5e4f7" if accedido is not None and k < accedido else "white"))
            rotulos[k].set_position((k, y))
            p = padre[k]
            aristas[k].set_data(([k, p], [y, -prof[p]]) if p is not None else ([], []))
        linea1.set_text(l1)
        linea2.set_text(l2)

    moviles = list(aristas.values()) + list(nodos.values()) + list(rotulos.values()) + [linea1, linea2]
    fig.tight_layout()
    print(estilo.guardar_gif(fig, moviles, actualizar, len(lista),
                             CARPETA / "ronda.gif", "una ronda de accesos en orden",
                             fps=0.8, pausa=5.0))


FIGURAS = {"animacion": animacion}

if __name__ == "__main__":
    FIGURAS[sys.argv[1]]()
