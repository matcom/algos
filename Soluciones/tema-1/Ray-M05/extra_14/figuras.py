import sys
from pathlib import Path

from matplotlib.patches import Rectangle

from comun import estilo
from comun.estilo import SERIES, TEXTO, TEXTO_2
from extra_14.disjuntos import disjuntos, intercalada

AZUL, NARANJA = SERIES[0], SERIES[1]
CARPETA = Path(__file__).resolve().parent
SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
N = 6


def _claro(hexa, alfa):
    return tuple(1 - alfa * (1 - int(hexa[k:k + 2], 16) / 255) for k in (1, 3, 5))


def animacion():
    A, B = intercalada(N)
    pares = []

    def comparar(x, y):
        pares.append((x, y))
        return (x > y) - (x < y)

    assert disjuntos(A, B, comparar) is None
    nombre = {v: f"a{str(k + 1).translate(SUB)}" for k, v in enumerate(A)}
    nombre |= {v: f"b{str(k + 1).translate(SUB)}" for k, v in enumerate(B)}
    alto = {v: 1.9 for v in A} | {v: 0.9 for v in B}

    estilo.aplicar()
    fig, ax = estilo.figura(9, 3.9)
    ax.axis("off")
    ax.set_xlim(-0.6, 2 * N + 0.8)
    ax.set_ylim(-1.5, 2.7)
    ax.set_title("Dos punteros sobre la entrada del adversario", pad=4)
    ax.text(-0.3, 1.9, "A", ha="center", va="center", fontsize=12, fontweight="bold")
    ax.text(-0.3, 0.9, "B", ha="center", va="center", fontsize=12, fontweight="bold")
    lineas = [ax.plot([x, y], [alto[x], alto[y]], color=AZUL, linewidth=2)[0] for x, y in pares]
    cajas, rotulos = {}, []
    for v in A + B:
        r = Rectangle((v - 0.35, alto[v] - 0.25), 0.7, 0.5, facecolor="white", edgecolor=TEXTO_2)
        ax.add_patch(r)
        cajas[v] = r
        rotulos.append(ax.text(v, alto[v], nombre[v], ha="center", va="center", fontsize=11))
    punteros = [ax.text(0, 0, "", ha="center", va="center", fontsize=9, color=NARANJA,
                        fontweight="bold") for _ in range(2)]
    linea1 = ax.text(-0.5, -0.35, "", ha="left", va="center", fontsize=9.5, color=TEXTO)
    linea2 = ax.text(-0.5, -0.9, "", ha="left", va="center", fontsize=9.5, color=TEXTO_2)


    cuadros = [(0, set(), (A[0], B[0]), "El adversario contesta como si a₁ < b₁ < a₂ < … < a₆ < b₆.",
                f"Φ = elementos sin descartar = {2 * N}.")]
    descartados, i, j = set(), 0, 0
    for c, (x, y) in enumerate(pares, start=1):
        menor = min(x, y)
        descartados.add(menor)
        if menor in A:
            i += 1
        else:
            j += 1
        siguiente = (A[i] if i < N else None, B[j] if j < N else None)
        cuadros.append((c, set(descartados), siguiente,
                        f"Comparación {c}: {nombre[x]} vs {nombre[y]}: {nombre[menor]} es menor, se descarta.",
                        f"Φ = {2 * N - c}.  Pares de vecinos comparados: {c} de {2 * N - 1}."))
    cuadros.append((len(pares), set(descartados), (None, None),
                    f"A se acabó: son disjuntos, después de {len(pares)} = 2n − 1 comparaciones.",
                    "Comparó los 11 pares de vecinos. Si faltara uno, el adversario igualaría ese par."))

    def actualizar(k):
        hechas, desc, (pa, pb), l1, l2 = cuadros[k]
        for m, ln in enumerate(lineas):
            ln.set_visible(m < hechas)
        for v, r in cajas.items():
            r.set_facecolor(_claro(AZUL, 0.25) if v in desc else "white")
            r.set_edgecolor(NARANJA if v in (pa, pb) else TEXTO_2)
            r.set_linewidth(2.5 if v in (pa, pb) else 1)
        for t, v, dy, s in ((punteros[0], pa, 0.45, "i"), (punteros[1], pb, -0.45, "j")):
            if v is None:
                t.set_text("")
            else:
                t.set_position((v, alto[v] + dy))
                t.set_text(s)
        linea1.set_text(l1)
        linea2.set_text(l2)

    moviles = lineas + list(cajas.values()) + rotulos + punteros + [linea1, linea2]
    fig.tight_layout()
    print(estilo.guardar_gif(fig, moviles, actualizar, len(cuadros),
                             CARPETA / "punteros.gif", "los dos punteros sobre la entrada del adversario",
                             fps=0.8, pausa=5.0))


FIGURAS = {"animacion": animacion}

if __name__ == "__main__":
    FIGURAS[sys.argv[1]]()
