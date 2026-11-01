import os

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Rectangle

CARPETA = os.path.dirname(os.path.abspath(__file__))


def ruta(nombre):
    return os.path.join(CARPETA, nombre)


AZUL, ROJO, VERDE, NARANJA, GRIS = "#1f77b4", "#d62728", "#2ca02c", "#ff7f0e", "#7f7f7f"

# Instancia pequena que se usa en las figuras 2 y 3
PESOS = [2, 3, 4, 5]
VALORES = [3, 4, 5, 6]
CAP = 8


def construir_tabla(pesos, valores, cap):
    n = len(pesos)
    T = np.zeros((n + 1, cap + 1), dtype=int)
    for i in range(1, n + 1):
        for c in range(cap + 1):
            T[i][c] = T[i - 1][c]
            if pesos[i - 1] <= c:
                T[i][c] = max(T[i][c], T[i - 1][c - pesos[i - 1]] + valores[i - 1])
    return T


def texto_instancia():
    objs = ", ".join(f"({w},{v})" for w, v in zip(PESOS, VALORES))
    return f"Objetos (peso, valor): {objs}   |   capacidad W = {CAP}"


# ---------------------------------------------------------------- Figura 1
def fig1_valor_vs_bits():
    fig, (a, b) = plt.subplots(1, 2, figsize=(12, 4.6))

    W = np.arange(1, 1025)
    bits = np.floor(np.log2(W)) + 1
    a.plot(W, bits, color=AZUL, lw=2)
    a.set_xlabel("valor del número W")
    a.set_ylabel("bits para escribir W en binario")
    a.set_title("Un número ocupa log₂W + 1 bits, no W")
    a.grid(alpha=0.3)
    a.annotate("W = 1024 necesita solo 11 bits", xy=(1024, 11), xytext=(380, 5),
               arrowprops=dict(arrowstyle="->"))

    bs = np.arange(1, 65)
    b.semilogy(bs, 2.0 ** bs, color=ROJO, lw=2, label="W = 2^b (valor máximo con b bits)")
    for k in (8, 16, 32, 64):
        b.plot(k, 2.0 ** k, "o", color="black")
        b.annotate(f"b={k}\nW≈{2.0 ** k:.1e}", xy=(k, 2.0 ** k),
                   xytext=(k - 9, 2.0 ** k * 80), fontsize=9)
    b.set_xlabel("tamaño en bits b")
    b.set_ylabel("valor W (escala log)")
    b.set_title("Cada bit extra duplica el valor: W = 2^Θ(b)")
    b.grid(alpha=0.3, which="both")
    b.legend(loc="lower right")
    b.set_ylim(1, 1e30)

    fig.tight_layout()
    fig.savefig(ruta("01_valor_vs_bits.png"), dpi=140)
    plt.close(fig)


# ---------------------------------------------------------------- Figura 2
def fig2_tabla_dp():
    T = construir_tabla(PESOS, VALORES, CAP)
    n = len(PESOS)
    fig, ax = plt.subplots(figsize=(10, 5.4))
    ax.imshow(T, cmap="Blues", vmin=0, vmax=T.max() * 1.15)
    for i in range(n + 1):
        for c in range(CAP + 1):
            ax.text(c, i, str(T[i][c]), ha="center", va="center", fontsize=12)
    ax.add_patch(Rectangle((CAP - 0.5, n - 0.5), 1, 1, fill=False, ec=ROJO, lw=3))
    ax.set_xticks(range(CAP + 1))
    ax.set_yticks(range(n + 1))
    ax.set_yticklabels(["0 (sin objetos)"] + [f"{i}: w={PESOS[i-1]}, v={VALORES[i-1]}" for i in range(1, n + 1)])
    ax.set_xlabel("capacidad c")
    ax.set_ylabel("primeros i objetos")
    ax.set_title(f"Tabla T[i][c] de la programación dinámica: {(n+1)*(CAP+1)} celdas = (n+1)(W+1)\n"
                 f"Respuesta T[n][W] = {T[n][CAP]} (recuadro rojo)")
    fig.text(0.5, 0.01, texto_instancia(), ha="center", fontsize=9)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(ruta("02_tabla_dp.png"), dpi=140)
    plt.close(fig)


# ---------------------------------------------------------------- Figura 3
def fig3_gif_llenado():
    T = construir_tabla(PESOS, VALORES, CAP)
    n = len(PESOS)
    celdas = [(i, c) for i in range(1, n + 1) for c in range(CAP + 1)]
    pausa = 10
    total = len(celdas) + pausa

    fig, ax = plt.subplots(figsize=(9, 5.6))

    def dibujar(f):
        ax.clear()
        k = min(f, len(celdas) - 1)
        llenas = celdas[: k + 1]
        M = np.full(T.shape, np.nan)
        M[0, :] = 0
        for (i, c) in llenas:
            M[i, c] = T[i, c]
        ax.imshow(np.ma.masked_invalid(M), cmap="Blues", vmin=0, vmax=T.max() * 1.15)
        for i in range(n + 1):
            for c in range(CAP + 1):
                if not np.isnan(M[i, c]):
                    ax.text(c, i, str(int(M[i, c])), ha="center", va="center", fontsize=11)
        i, c = celdas[k]
        w, v = PESOS[i - 1], VALORES[i - 1]
        ax.add_patch(Rectangle((c - 0.5, i - 0.5), 1, 1, fill=False, ec=ROJO, lw=3))
        ax.add_patch(Rectangle((c - 0.5, i - 1.5), 1, 1, fill=False, ec=VERDE, lw=3))
        if w <= c:
            ax.add_patch(Rectangle((c - w - 0.5, i - 1.5), 1, 1, fill=False, ec=NARANJA, lw=3))
            det = (f"T[{i}][{c}] = max(T[{i-1}][{c}], T[{i-1}][{c-w}] + {v}) "
                   f"= max({T[i-1][c]}, {T[i-1][c-w]}+{v}) = {T[i][c]}")
        else:
            det = f"T[{i}][{c}] = T[{i-1}][{c}] = {T[i][c]}   (el objeto pesa {w} > {c})"
        ax.set_xticks(range(CAP + 1))
        ax.set_yticks(range(n + 1))
        ax.set_yticklabels(["0"] + [f"{j} (w={PESOS[j-1]})" for j in range(1, n + 1)])
        ax.set_xlabel("capacidad c")
        ax.set_ylabel("objetos considerados")
        ax.set_title(f"Celda {k + 1} de {len(celdas)}: cada celda cuesta O(1)\n{det}", fontsize=10)
        fig.subplots_adjust(bottom=0.22)
        ax.text(0.0, -0.24, "rojo: celda actual   verde: no usar el objeto   naranja: usar el objeto",
                transform=ax.transAxes, fontsize=9)

    anim = FuncAnimation(fig, dibujar, frames=total, interval=200)
    anim.save(ruta("03_llenado_tabla.gif"), writer=PillowWriter(fps=5), dpi=80)
    plt.close(fig)


# ---------------------------------------------------------------- Figura 4
def fig4_costo_vs_tamano():
    n = 10
    b = np.arange(1, 81)
    N = n * b                      # tamano de la entrada en bits (n pesos de b bits)
    costo = n * 2.0 ** b           # n * W con W = 2^b
    fig, ax = plt.subplots(figsize=(9.5, 5.4))
    ax.semilogy(N, costo, color=ROJO, lw=3, label="mochila: n·W = n·2^b  (exponencial en N)")
    for p, col in ((2, VERDE), (3, NARANJA), (5, AZUL)):
        ax.semilogy(N, N.astype(float) ** p, color=col, lw=1.8, ls="--", label=f"polinomio N^{p}")
    ax.set_ylim(1, 1e30)
    ax.set_xlabel("tamaño de la entrada N (bits), con n = 10 objetos")
    ax.set_ylabel("operaciones (escala log)")
    ax.set_title("El costo nW termina superando a cualquier polinomio en N")
    ax.grid(alpha=0.3, which="both")
    ax.legend(loc="upper left")
    fig.tight_layout()
    fig.savefig(ruta("04_costo_vs_tamano.png"), dpi=140)
    plt.close(fig)


# ---------------------------------------------------------------- Figura 5
def fig5_tiempo_estimado():
    n, vel = 100, 1e9
    bits = [16, 32, 48, 64, 128]
    seg = [n * 2.0 ** b / vel for b in bits]
    fig, ax = plt.subplots(figsize=(10, 5.4))
    barras = ax.bar([f"{b} bits" for b in bits], seg, color=[AZUL, AZUL, NARANJA, ROJO, ROJO])
    ax.set_yscale("log")
    for x, s in zip(barras, seg):
        if s < 60:
            t = f"{s:.2g} s"
        elif s < 3600:
            t = f"{s / 60:.3g} minutos"
        elif s < 86400:
            t = f"{s / 3600:.3g} horas"
        elif s < 3600 * 24 * 365:
            t = f"{s / 86400:.3g} días"
        else:
            t = f"{s / (3600 * 24 * 365):.2g} años".replace("e+", "×10^")
        ax.text(x.get_x() + x.get_width() / 2, s * 4, t, ha="center", fontsize=10)
    refs = [(3600, "1 hora"), (3600 * 24 * 365, "1 año"), (5e9 * 3600 * 24 * 365, "vida restante del Sol (~5×10⁹ años)")]
    for y, txt in refs:
        ax.axhline(y, color=GRIS, ls=":")
        ax.text(-0.45, y * 1.4, txt, fontsize=9, color=GRIS)
    ax.set_ylim(1e-4, 1e36)
    ax.set_ylabel("tiempo estimado (s, escala log)")
    ax.set_xlabel("tamaño en bits de la capacidad W")
    ax.set_title("Tiempo de la DP con n = 100 objetos y 10⁹ celdas por segundo")
    fig.tight_layout()
    fig.savefig(ruta("05_tiempo_estimado.png"), dpi=140)
    plt.close(fig)


# ---------------------------------------------------------------- Figura 6
def fig6_primalidad_vs_mochila():
    n = 100
    b = np.arange(1, 65)
    fig, ax = plt.subplots(figsize=(9.5, 5.4))
    ax.semilogy(b, 2.0 ** (b / 2), color=AZUL, lw=2.5, label="primalidad por división: √x = 2^(b/2)")
    ax.semilogy(b, n * 2.0 ** b, color=ROJO, lw=2.5, label="mochila DP: n·W = n·2^b  (n = 100)")
    ax.semilogy(b, b.astype(float) ** 3, color=VERDE, lw=2.5, ls="--",
                label="algoritmo polinomial en b (por ejemplo b³)")
    ax.set_ylim(1, 1e40)
    ax.set_xlabel("b = número de bits del número de la entrada (x o W)")
    ax.set_ylabel("operaciones (escala log)")
    ax.set_title("Ambos son polinomiales en el valor y exponenciales en los bits")
    ax.grid(alpha=0.3, which="both")
    ax.legend(loc="upper left")
    fig.tight_layout()
    fig.savefig(ruta("06_primalidad_vs_mochila.png"), dpi=140)
    plt.close(fig)


# ---------------------------------------------------------------- Figura 7
def fig7_binario_vs_unario():
    valor = 13
    binario = bin(valor)[2:]
    fig = plt.figure(figsize=(11, 7))
    gs = fig.add_gridspec(2, 1, height_ratios=[1, 1.4])

    a = fig.add_subplot(gs[0])
    a.set_xlim(-0.5, 16)
    a.set_ylim(-1, 2.2)
    a.axis("off")
    a.set_title(f"El mismo número W = {valor}: binario vs unario")
    for j, ch in enumerate(binario):
        a.add_patch(Rectangle((j, 1), 0.9, 0.9, fc="#aec7e8", ec="black"))
        a.text(j + 0.45, 1.45, ch, ha="center", va="center", fontsize=14)
    a.text(len(binario) + 0.3, 1.45, f"binario: {len(binario)} símbolos (≈ log₂W)", va="center")
    for j in range(valor):
        a.add_patch(Rectangle((j * 1.0, 0), 0.9, 0.9, fc="#ff9896", ec="black"))
    a.text(0, -0.5, f"unario: {valor} símbolos (= W). Medida así, nW sí sería polinomial en el tamaño.", fontsize=10)

    b = fig.add_subplot(gs[1])
    W = np.arange(1, 65)
    b.plot(W, W, color=ROJO, lw=2.5, label="unario: W símbolos")
    b.plot(W, np.floor(np.log2(W)) + 1, color=AZUL, lw=2.5, label="binario: ⌊log₂W⌋+1 bits")
    b.set_xlabel("valor W")
    b.set_ylabel("tamaño de la representación")
    b.set_title("La brecha entre ambos tamaños es la que separa 'polinomial en el valor' de 'polinomial en el tamaño'")
    b.grid(alpha=0.3)
    b.legend()

    fig.tight_layout()
    fig.savefig(ruta("07_binario_vs_unario.png"), dpi=140)
    plt.close(fig)


if __name__ == "__main__":
    for f in (fig1_valor_vs_bits, fig2_tabla_dp, fig3_gif_llenado, fig4_costo_vs_tamano,
              fig5_tiempo_estimado, fig6_primalidad_vs_mochila, fig7_binario_vs_unario):
        f()
        print("ok:", f.__name__)
    print("Archivos generados en:", CARPETA)