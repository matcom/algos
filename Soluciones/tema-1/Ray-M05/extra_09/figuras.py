import sys
from pathlib import Path

from matplotlib.patches import Rectangle

from comun import estilo
from comun.estilo import SERIES, TEXTO, TEXTO_2
from extra_09.mezcla import contar, intercalada

AZUL, NARANJA = SERIES[0], SERIES[1]
CARPETA = Path(__file__).resolve().parent
SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
N = 5


def _rgb(hexa, alfa):
    return tuple(1 - alfa * (1 - int(hexa[k:k + 2], 16) / 255) for k in (1, 3, 5))


def animacion():
    A, B = intercalada(N)
    salida, pares = contar(A, B)
    nombre = {v: f"a{str(k + 1).translate(SUB)}" for k, v in enumerate(A)}
    nombre |= {v: f"b{str(k + 1).translate(SUB)}" for k, v in enumerate(B)}
    alto = {v: 1.9 for v in A} | {v: 0.9 for v in B}

    estilo.aplicar()
    fig, ax = estilo.figura(9, 4.4)
    ax.axis("off")
    ax.set_xlim(-0.6, 2 * N + 0.8)
    ax.set_ylim(-2.75, 2.6)
    ax.set_title("La mezcla optimizada contra la entrada intercalada", pad=4)
    ax.text(-0.3, 1.9, "A", ha="center", va="center", fontsize=12, fontweight="bold")
    ax.text(-0.3, 0.9, "B", ha="center", va="center", fontsize=12, fontweight="bold")
    nodos, rotulos = {}, []
    for v in A + B:
        r = Rectangle((v - 0.35, alto[v] - 0.25), 0.7, 0.5, facecolor="white",
                      edgecolor=TEXTO_2, zorder=2)
        ax.add_patch(r)
        nodos[v] = r
        rotulos.append(ax.text(v, alto[v], nombre[v], ha="center", va="center", fontsize=11))


    lineas = [ax.plot([x, y], [alto[x], alto[y]], color=AZUL, linewidth=2, zorder=1)[0]
              for x, y in pares]
    vistos = {frozenset(p) for p in pares}
    sin_comparar = [(v, v + 1) for v in range(1, 2 * N) if frozenset((v, v + 1)) not in vistos]
    punteadas = [ax.plot([x, y], [alto[x], alto[y]], color=NARANJA, linewidth=2.5,
                         linestyle=(0, (3, 2)), zorder=1)[0] for x, y in sin_comparar]

    ax.text(-0.3, -0.75, "salida", ha="center", va="center", fontsize=9, color=TEXTO_2)
    cajas, textos = [], []
    for k in range(2 * N):
        r = Rectangle((k + 0.65, -1.0), 0.7, 0.5, facecolor="white", edgecolor=TEXTO_2)
        ax.add_patch(r)
        cajas.append(r)
        textos.append(ax.text(k + 1, -0.75, "", ha="center", va="center", fontsize=11))
    linea1 = ax.text(-0.5, -1.55, "", ha="left", va="center", fontsize=9.5, color=TEXTO)
    linea2 = ax.text(-0.5, -2.05, "", ha="left", va="center", fontsize=9.5, color=TEXTO_2)

    cuadros = [(0, 0, False, "El adversario contesta como si a₁ < b₁ < a₂ < b₂ < … < a₅ < b₅.",
                "Esa cadena tiene 9 pares de vecinos: un algoritmo correcto tiene que comparar los 9.")]
    for c, (x, y) in enumerate(pares, start=1):
        menor = min(x, y)
        cuadros.append((c, c, False, f"Comparación {c}: ¿{nombre[x]} ≤ {nombre[y]}?  "
                        f"Sale {nombre[menor]}.",
                        f"Pares de vecinos comparados: {c} de 9."))
    falta = ", ".join(f"({nombre[x]}, {nombre[y]})" for x, y in sin_comparar)
    cuadros.append((len(pares), 2 * N, True,
                    f"A A le queda solo a₅: deja de comparar, copia lo que queda de B y pone a₅ al final.",
                    f"{len(pares)} comparaciones. Sin comparar: {falta}."))
    cuadros.append((len(pares), 2 * N, True,
                    "La salida pone b₅ antes que a₅, pero a₅ < b₅: falla en la propia entrada intercalada.",
                    "Es el par (a₅, b₅), que nunca comparó, el que el argumento de C5, §6 señala."))

    def actualizar(c):
        hechas, salieron, final, l1, l2 = cuadros[c]
        for k, ln in enumerate(lineas):
            ln.set_visible(k < hechas)
        for ln in punteadas:
            ln.set_visible(final)
        usados = set(salida[:salieron])
        for v, r in nodos.items():
            r.set_facecolor(_rgb(AZUL, 0.25) if v in usados else "white")
        for k in range(2 * N):
            v = salida[k] if k < salieron else None
            textos[k].set_text(nombre[v] if v is not None else "")
            mal = final and v is not None and v != k + 1
            cajas[k].set_facecolor(_rgb(NARANJA, 0.35) if mal else
                                   (_rgb(AZUL, 0.25) if v is not None else "white"))
        linea1.set_text(l1)
        linea2.set_text(l2)


    moviles = lineas + punteadas + list(nodos.values()) + rotulos + cajas + textos + [linea1, linea2]
    fig.tight_layout()
    print(estilo.guardar_gif(fig, moviles, actualizar, len(cuadros),
                             CARPETA / "adversario.gif", "la mezcla optimizada contra el adversario",
                             fps=0.8, pausa=5.0))


FIGURAS = {"animacion": animacion}

if __name__ == "__main__":
    FIGURAS[sys.argv[1]]()
