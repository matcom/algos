import math
import sys
from pathlib import Path

import numpy as np

from comun import estilo
from comun.estilo import SERIES, TEXTO_2
from calculos import HORA, K, cotas_n_log_n, factor_n_log_n, tamano_n_log_n

_, NARANJA, AGUA, _, _ = SERIES
CARPETA = Path(__file__).resolve().parent


def factor_tamano():
    fig, ax = estilo.figura()
    exps = np.linspace(2, 40, 300)
    Ls = exps * math.log2(10)
    f = [factor_n_log_n(L) for L in Ls]
    f1 = [cotas_n_log_n(L)[0] for L in Ls]
    n = 10**exps

    ax.plot(n, f, color=NARANJA, label="n log n: factor f")
    ax.plot(n, f1, color=NARANJA, linestyle=(0, (4, 3)), linewidth=1.5,
            label="n log n: cota inferior kL / (L + log₂ k)")
    ax.axhline(K, color=TEXTO_2, linewidth=1, linestyle=":")
    ax.axhline(math.sqrt(K), color=AGUA, label="n²: factor √1000")
    ax.set_xscale("log")
    ax.set_ylim(0, 1060)
    ax.set_xlim(n[0], n[-1])

    L0 = math.log2(tamano_n_log_n(HORA))
    x0, y0 = 2**L0, factor_n_log_n(L0)
    ax.plot([x0], [y0], "o", color=NARANJA, markeredgecolor="white", markeredgewidth=1.5)
    estilo.etiqueta(ax, x0, y0, f"una hora a 10⁹ op/s (C1 §7)\nn ≈ 9.9·10¹⁰, f ≈ {y0:.0f}",
                    dx=8, dy=-26, va="top")
    estilo.etiqueta(ax, n[-1], f[-1], "f", dx=4, dy=6)
    estilo.etiqueta(ax, n[-1], f1[-1], "cota", dx=4, dy=-8)
    estilo.etiqueta(ax, n[0], K, "k = 1000: el factor de un algoritmo lineal", dx=4, dy=-6, va="top")
    estilo.etiqueta(ax, n[0], math.sqrt(K), "n²: √1000 ≈ 31.6, para todo n", dx=4, dy=8, va="bottom")

    ax.set_xlabel("tamaño que resuelve la computadora actual en una hora")
    ax.set_ylabel("factor de crecimiento con k = 1000")
    ax.set_title("El factor de n log n depende del tamaño actual y tiende a 1000 muy despacio")
    ax.legend(loc="lower right")
    print(estilo.guardar(fig, CARPETA / "factor-tamano.png", "factor contra tamaño actual"))


def animacion():
    estilo.aplicar()
    fig, ax = estilo.figura(8, 4.6)
    n = np.logspace(4, 16, 400)
    ax.plot(n, n**2, color=AGUA, label="n²")
    ax.plot(n, n * np.log2(n), color=NARANJA, label="n log₂ n")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1e4, 1e16)
    ax.set_ylim(1e10, 1e17)
    ax.set_xlabel("tamaño de entrada n")
    ax.set_ylabel("operaciones")
    ax.set_title("Lo que compra una computadora mil veces más rápida")
    ax.legend(loc="lower right")

    costos = [(AGUA, lambda x: x * x, lambda B: math.sqrt(B)),
              (NARANJA, lambda x: x * math.log2(x), tamano_n_log_n)]
    for color, costo, inversa in costos:
        x0 = inversa(HORA)
        ax.plot([x0], [HORA], "o", markerfacecolor="none", markeredgecolor=color, markersize=8)

    linea = ax.axhline(HORA, color=TEXTO_2, linewidth=1, linestyle=(0, (4, 3)))
    puntos = [ax.plot([], [], "o", color=c, markeredgecolor="white", markeredgewidth=1.5)[0]
              for c, _, _ in costos]
    guias = [ax.plot([], [], color=c, linewidth=1, alpha=0.6)[0] for c, _, _ in costos]
    texto = ax.text(0.02, 0.96, "", transform=ax.transAxes, va="top", fontsize=10,
                    family="monospace", color=estilo.TEXTO)

    cuadros = 61

    def cuadro(i):
        t = i / (cuadros - 1)
        k = K**t
        B = HORA * k
        linea.set_ydata([B, B])
        lineas = [f"presupuesto × {k:7.1f}"]
        for (color, _, inversa), p, gu, nombre in zip(costos, puntos, guias, ["n^2     ", "n log n "]):
            x = inversa(B)
            p.set_data([x], [B])
            gu.set_data([x, x], [1e10, B])
            lineas.append(f"{nombre}× {x / inversa(HORA):7.1f}")
        texto.set_text("\n".join(lineas))

    fig.tight_layout()
    print(estilo.guardar_gif(fig, [linea, texto, *puntos, *guias], cuadro, cuadros,
                             CARPETA / "presupuesto.gif", "animación del presupuesto"))


FIGURAS = {
    "factor_tamano": factor_tamano,
    "animacion": animacion,
}

if __name__ == "__main__":
    FIGURAS[sys.argv[1]]()
