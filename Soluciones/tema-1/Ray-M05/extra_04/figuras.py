import sys
from pathlib import Path

from matplotlib.patches import Rectangle

from comun import estilo
from comun.estilo import SERIES, TEXTO, TEXTO_2
from maquina import BLANCO, incrementar, unos

AZUL, NARANJA, AGUA = SERIES[0], SERIES[1], SERIES[2]
CARPETA = Path(__file__).resolve().parent


def costos():
    m = 64
    cinta = {0: "0"}
    reales, amortizados, potencial = [], [], []
    for _ in range(m):
        antes = 2 * unos(cinta)
        c = incrementar(cinta)
        despues = 2 * unos(cinta)
        reales.append(c)
        amortizados.append(c + despues - antes)
        potencial.append(despues)
    xs = range(1, m + 1)

    fig, ax = estilo.figura(9, 4.4)
    ax.bar(xs, reales, width=0.75, color=AZUL, alpha=0.55, label="costo real (pasos)")
    ax.step(xs, potencial, where="mid", color=AGUA, linewidth=2, label="potencial Φ = 2·unos")
    ax.plot(xs, amortizados, color=NARANJA, linewidth=2.5, label="costo amortizado")
    estilo.etiqueta(ax, m, amortizados[-1], "amortizado = 4", dy=6)
    for i in (8, 16, 32, 64):
        estilo.etiqueta(ax, i, reales[i - 1], f"{reales[i - 1]}", dx=0, dy=8, ha="center",
                        va="bottom")
    ax.set_xlim(0, m + 6)
    ax.set_ylim(0, max(reales) + 3)
    ax.set_xlabel("número de incremento")
    ax.set_ylabel("pasos")
    ax.set_title("El potencial paga los acarreos: cada pico de costo es una caída de Φ")
    ax.legend(loc="upper left")
    print(estilo.guardar(fig, CARPETA / "costos.png", "costo real, amortizado y potencial"))


def animacion():
    cinta = {p: b for p, b in zip(range(-2, 1), "110")}
    posiciones = list(range(-4, 2))
    cuadros = [(dict(cinta), 0, "acarreo", "La cinta tiene 6 = 110. Cabezal en el bit menos significativo.")]
    total = 0
    for v in (6, 7, 8):
        traza = []
        pasos = incrementar(cinta, traza)
        total += pasos
        for k, (c, cab, est) in enumerate(traza, start=1):
            if est == "fin":
                texto = (f"{v} → {v + 1}: {pasos} pasos. Volvió al bit menos significativo. "
                         f"Φ = 2·unos = {2 * unos(c)}")
            else:
                texto = f"{v} → {v + 1}: paso {k}, estado «{est}»"
            cuadros.append((c, cab, est, texto))
        cuadros.append(cuadros[-1])

    estilo.aplicar()
    fig, ax = estilo.figura(8, 3.2)
    ax.axis("off")
    ax.set_xlim(-4.7, 2.7)
    ax.set_ylim(-1.2, 2.3)
    ax.set_title("El contador binario en una máquina de Turing de una cinta", pad=4)
    for p in posiciones:
        ax.text(p + 0.45, -0.35, "bit menos significativo" if p == 0 else "",
                ha="center", va="top", fontsize=8, color=TEXTO_2)

    celdas, simbolos = [], []
    for p in posiciones:
        r = Rectangle((p, 0), 0.9, 0.9, facecolor="white", edgecolor=TEXTO_2)
        ax.add_patch(r)
        celdas.append(r)
        simbolos.append(ax.text(p + 0.45, 0.45, "", ha="center", va="center", fontsize=14))
    cabezal = ax.plot([], [], marker="v", markersize=14, color=TEXTO, linestyle="none")[0]
    estado = ax.text(-4.6, 1.85, "", ha="left", va="center", fontsize=10, color=TEXTO)

    def actualizar(i):
        c, cab, est, texto = cuadros[i]
        for p, r, s in zip(posiciones, celdas, simbolos):
            simbolo = c.get(p, BLANCO)
            s.set_text("" if simbolo == BLANCO else simbolo)
            uno = simbolo == "1"
            r.set_facecolor((*_rgb(AZUL), 0.3) if uno else "white")
        cabezal.set_data([cab + 0.45], [1.15])
        estado.set_text(texto)

    moviles = celdas + simbolos + [cabezal, estado]
    fig.tight_layout()
    print(estilo.guardar_gif(fig, moviles, actualizar, len(cuadros),
                             CARPETA / "maquina.gif", "la máquina de Turing incrementando",
                             fps=1.4, pausa=3.0))


def _rgb(hexa):
    return tuple(int(hexa[k:k + 2], 16) / 255 for k in (1, 3, 5))


FIGURAS = {"costos": costos, "animacion": animacion}

if __name__ == "__main__":
    FIGURAS[sys.argv[1]]()
