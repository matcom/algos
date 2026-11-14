import sys
from pathlib import Path

from matplotlib.patches import Patch, Rectangle

from comun import estilo
from comun.estilo import SERIES, TEXTO, TEXTO_2
from busqueda import comparar

AZUL, NARANJA = SERIES[0], SERIES[1]
CARPETA = Path(__file__).resolve().parent

A = [3 * i + 2 for i in range(15)]
X = 30


def estados():
    n = len(A)
    lo, hi = 0, n
    cuadros = [(lo, hi, None, f"x = {X}. Al principio no se sabe nada: Φ = hi − lo = {n}")]
    paso = 0
    while lo < hi:
        m = (lo + hi) // 2
        paso += 1
        cuadros.append((lo, hi, m, f"comparación {paso}: x = {X} contra A[{m}] = {A[m]}"))
        r = comparar(X, A[m])
        if r < 0:
            hi = m
            texto = f"x < A[{m}]: todo desde {m} es mayor que x.  hi ← {m}"
        else:
            lo = m + 1
            texto = f"x > A[{m}]: todo hasta {m} es menor que x.  lo ← {m + 1}"
        cuadros.append((lo, hi, None, texto + f".  Φ = {hi - lo}"))
    cuadros.append((lo, hi, None,
                    f"lo = hi = {lo}: x no está, y cae en el hueco {lo} "
                    f"(entre A[{lo - 1}] y A[{lo}]). {paso} comparaciones = ⌈log₂ 16⌉"))
    return cuadros


def animacion():
    estilo.aplicar()
    fig, ax = estilo.figura(10, 3.6)
    ax.axis("off")
    ax.set_xlim(-0.8, len(A) + 0.2)
    ax.set_ylim(-1.75, 2.0)
    ax.set_title("La búsqueda binaria, con su invariante y su potencial", pad=4)

    cajas, valores = [], []
    for i, a in enumerate(A):
        caja = Rectangle((i, 0), 0.9, 0.9, facecolor="white", edgecolor=TEXTO_2, linewidth=1)
        ax.add_patch(caja)
        cajas.append(caja)
        valores.append(ax.text(i + 0.45, 0.45, str(a), ha="center", va="center", fontsize=10))
        ax.text(i + 0.45, -0.25, str(i), ha="center", va="center", fontsize=8, color=TEXTO_2)

    barra = ax.plot([], [], color=TEXTO, linewidth=3, solid_capstyle="butt")[0]
    rotulo_barra = ax.text(0, -0.95, "", ha="center", va="top", fontsize=9, color=TEXTO)
    estado = ax.text(-0.6, 1.65, "", ha="left", va="center", fontsize=10, color=TEXTO)
    invariante = ax.text(-0.6, 1.2, "", ha="left", va="center", fontsize=10,
                         family="monospace", color=TEXTO_2)
    hueco = ax.plot([], [], marker="v", color=TEXTO, markersize=11, linestyle="none")[0]

    ax.legend(handles=[Patch(facecolor=AZUL, alpha=0.3, label="ya se sabe: menor que x"),
                       Patch(facecolor=NARANJA, alpha=0.3, label="ya se sabe: mayor que x"),
                       Patch(facecolor="white", edgecolor=TEXTO_2, label="todavía puede ser x")],
              loc="lower center", ncol=3, bbox_to_anchor=(0.5, -0.06))

    cuadros = estados()

    def actualizar(i):
        lo, hi, m, texto = cuadros[i]
        for j, caja in enumerate(cajas):
            if j < lo:
                caja.set_facecolor((*_rgb(AZUL), 0.3))
            elif j >= hi:
                caja.set_facecolor((*_rgb(NARANJA), 0.3))
            else:
                caja.set_facecolor("white")
            caja.set_edgecolor(TEXTO if j == m else TEXTO_2)
            caja.set_linewidth(3 if j == m else 1)
        if hi > lo:
            barra.set_data([lo + 0.02, hi - 0.12], [-0.6, -0.6])
            rotulo_barra.set_position(((lo + hi - 0.1) / 2, -0.75))
            rotulo_barra.set_text(f"[lo, hi) = [{lo}, {hi}):  Φ = {hi - lo}")
        else:
            barra.set_data([], [])
            rotulo_barra.set_position((lo - 0.05, -0.75))
            rotulo_barra.set_text("Φ = 0")
        hueco.set_data(([lo - 0.05], [1.0]) if lo == hi else ([], []))
        estado.set_text(texto)
        invariante.set_text(f"invariante:  A[0:{lo}] < x < A[{hi}:{len(A)}]")

    moviles = cajas + valores + [barra, rotulo_barra, estado, invariante, hueco]
    fig.tight_layout()
    print(estilo.guardar_gif(fig, moviles, actualizar, len(cuadros),
                             CARPETA / "invariante.gif", "búsqueda binaria animada",
                             fps=0.6, pausa=4.0))


def _rgb(hexa):
    return tuple(int(hexa[k:k + 2], 16) / 255 for k in (1, 3, 5))


FIGURAS = {"animacion": animacion}

if __name__ == "__main__":
    FIGURAS[sys.argv[1]]()
