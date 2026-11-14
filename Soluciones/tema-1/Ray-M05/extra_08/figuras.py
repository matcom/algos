import sys
from collections import Counter
from pathlib import Path

from matplotlib.patches import Rectangle

from comun import estilo
from comun.estilo import SERIES, TEXTO, TEXTO_2

AZUL, NARANJA, VERDE = SERIES[0], SERIES[1], SERIES[2]
CARPETA = Path(__file__).resolve().parent

FILA = "BDADCBDDCDCA"


def _rgb(hexa, alfa):
    return (*[int(hexa[k:k + 2], 16) / 255 for k in (1, 3, 5)], alfa)


def _copias(k, c):
    return f"{k} copia{'s' if k != 1 else ''} de {c}"


def estados():
    n = len(FILA)
    papel = [None] * n
    lugares = [[None, []], [None, []]]
    trios = 0
    cuadros = [(list(papel), [(None, 0), (None, 0)], None,
                "Dos lugares para candidatos, cada uno con su contador.",
                "Todavía no se procesó nada.")]
    for i, x in enumerate(FILA):
        vivos = [(c, len(p)) for c, p in lugares]
        activo = [len(p) > 0 for _, p in lugares]
        if activo[0] and x == lugares[0][0]:
            lugares[0][1].append(i)
            papel[i] = 1
            linea = f"{x} es el candidato 1: una copia más."
        elif activo[1] and x == lugares[1][0]:
            lugares[1][1].append(i)
            papel[i] = 2
            linea = f"{x} es el candidato 2: una copia más."
        elif not activo[0] or not activo[1]:
            j = 0 if not activo[0] else 1
            lugares[j] = [x, [i]]
            papel[i] = j + 1
            linea = f"{x} no es candidato y el lugar {j + 1} está libre: {x} pasa a ocuparlo."
        else:
            trios += 1
            p1, p2 = lugares[0][1].pop(), lugares[1][1].pop()
            for p in (p1, p2, i):
                papel[p] = ("t", trios)
            linea = (f"{x} es distinto de {vivos[0][0]} y de {vivos[1][0]}: "
                     f"los tres forman el trío {trios} y los dos contadores bajan.")
        partes = [f"{trios} trío{'s' if trios != 1 else ''}"]
        partes += [_copias(len(p), c) for c, p in lugares if p]
        resumen = f"Prefijo de largo {i + 1} = " + " + ".join(partes) + \
                  f"   ({3 * trios} + {sum(len(p) for _, p in lugares)} = {i + 1})"
        cuadros.append((list(papel), [(c, len(p)) for c, p in lugares], i, linea, resumen))

    cuenta = Counter(FILA)
    tercio = n / 3
    juicios = []
    for c, p in lugares:
        if p:
            mas = cuenta[c] > tercio
            juicios.append(f"{c} aparece {cuenta[c]} veces, {'más' if mas else 'no más'} de n/3 = {tercio:g}")
    cuadros.append((list(papel), [(c, len(p)) for c, p in lugares], None,
                    "Segunda pasada: " + "; ".join(juicios) + ".",
                    "El atajo devolvería los dos candidatos; la respuesta correcta es solo "
                    + ", ".join(c for c, p in lugares if p and cuenta[c] > tercio) + "."))
    return cuadros


def animacion():
    n = len(FILA)
    cuadros = estados()
    estilo.aplicar()
    fig, ax = estilo.figura(9, 4.2)
    ax.axis("off")
    ax.set_xlim(-0.3, n + 0.1)
    ax.set_ylim(-3.6, 1.9)
    ax.set_title("Más de n/3: dos candidatos y tríos de distintos", pad=4)

    cajas, letras, marcas = [], [], []
    for k, x in enumerate(FILA):
        r = Rectangle((k, 0), 0.85, 0.85, facecolor="white", edgecolor=TEXTO_2)
        ax.add_patch(r)
        cajas.append(r)
        letras.append(ax.text(k + 0.425, 0.425, x, ha="center", va="center", fontsize=12))
        ax.text(k + 0.425, 1.1, str(k + 1), ha="center", va="center", fontsize=7, color=TEXTO_2)
        marcas.append(ax.text(k + 0.425, -0.3, "", ha="center", va="center",
                              fontsize=8, color=TEXTO))

    lugares, rotulos = [], []
    for j, color in enumerate((AZUL, NARANJA)):
        x0 = 1.0 + 5.5 * j
        r = Rectangle((x0, -1.75), 4.0, 0.8, facecolor=_rgb(color, 0.25), edgecolor=color,
                      linewidth=2)
        ax.add_patch(r)
        lugares.append(r)
        rotulos.append(ax.text(x0 + 2.0, -1.35, "", ha="center", va="center", fontsize=11))

    linea1 = ax.text(-0.2, -2.4, "", ha="left", va="center", fontsize=9.5, color=TEXTO)
    linea2 = ax.text(-0.2, -2.95, "", ha="left", va="center", fontsize=9.5, color=TEXTO_2)

    def actualizar(c):
        papel, candidatos, actual, l1, l2 = cuadros[c]
        for k, r in enumerate(cajas):
            p = papel[k]
            if p == 1:
                r.set_facecolor(_rgb(AZUL, 0.35))
            elif p == 2:
                r.set_facecolor(_rgb(NARANJA, 0.35))
            elif isinstance(p, tuple):
                r.set_facecolor(_rgb(VERDE, 0.30))
            else:
                r.set_facecolor("white")
            marcas[k].set_text(f"t{p[1]}" if isinstance(p, tuple) else "")
            grueso = k == actual
            r.set_linewidth(3 if grueso else 1)
            r.set_edgecolor(TEXTO if grueso else TEXTO_2)
            letras[k].set_color(TEXTO if actual is None or k <= actual or c == len(cuadros) - 1
                                else TEXTO_2)
        for j, (cand, cont) in enumerate(candidatos):
            rotulos[j].set_text(f"candidato {j + 1}: {cand if cont else '—'}    contador {cont}")
        linea1.set_text(l1)
        linea2.set_text(l2)

    moviles = cajas + letras + marcas + [linea1, linea2] + rotulos
    fig.tight_layout()
    print(estilo.guardar_gif(fig, moviles, actualizar, len(cuadros),
                             CARPETA / "trios.gif", "la primera pasada con dos candidatos",
                             fps=0.8, pausa=5.0))


FIGURAS = {"animacion": animacion}

if __name__ == "__main__":
    FIGURAS[sys.argv[1]]()
