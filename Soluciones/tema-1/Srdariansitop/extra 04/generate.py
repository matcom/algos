"""
Contador binario en una máquina de Turing: visualización del análisis amortizado.
Genera 4 imágenes PNG:
  fig1_traza_maquina.png      -> un incremento caro (3 -> 4) paso a paso
  fig2_contador_0_a_8.png     -> 8 incrementos con bits que cambian, coste y potencial
  fig3_coste_por_incremento.png -> coste real vs coste amortizado (=3)
  fig4_potencial_y_suma.png   -> potencial Phi y suma telescópica
Requisitos: pip install matplotlib numpy
Convención: el bit menos significativo (LSB) va a la IZQUIERDA de la cinta.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ROJO, VERDE, AZUL, GRIS = "#d9534f", "#3c9d5d", "#3b7dd8", "#e8e8e8"
OSCURO = "#2b2b2b"


# ---------------------------------------------------------------- simulación
def incrementar(cinta):
    """Suma 1. Devuelve (nueva_cinta, t, coste_real). Coste = 2t+1 pasos de la MT."""
    c = cinta[:]
    t = 0
    while c[t] == 1:
        c[t] = 0
        t += 1
    c[t] = 1
    return c, t, 2 * t + 1


def historial(m, k):
    cinta = [0] * k
    datos = [(cinta[:], None, None)]
    for _ in range(m):
        cinta, t, c = incrementar(cinta)
        datos.append((cinta[:], t, c))
    return datos


def phi(cinta):
    return 2 * sum(cinta)  # potencial = 2 * (número de unos)


def dibuja_celda(ax, x, y, valor, color_fondo="white", borde=OSCURO, grosor=1.2, tam=0.9):
    ax.add_patch(Rectangle((x, y), tam, tam, facecolor=color_fondo,
                           edgecolor=borde, linewidth=grosor))
    ax.text(x + tam / 2, y + tam / 2, str(valor), ha="center", va="center",
            fontsize=15, fontweight="bold", color=OSCURO)


# ---------------------------------------------------------------- figura 1
def fig1():
    # Incremento 3 -> 4 con t = 2.  (cinta, posición del cabezal, fase, texto)
    pasos = [
        ([1, 1, 0], 0, "inicio", "estado inicial: el número 3 = 1 1 0 (LSB a la izquierda)"),
        ([0, 1, 0], 1, "ida",    "paso 1: lee 1 → escribe 0, mueve →   (acarreo se propaga)"),
        ([0, 0, 0], 2, "ida",    "paso 2: lee 1 → escribe 0, mueve →"),
        ([0, 0, 1], 1, "escribe","paso 3: lee 0 → escribe 1, mueve ←   (acarreo absorbido)"),
        ([0, 0, 1], 0, "vuelta", "paso 4: rebobina ←"),
        ([0, 0, 1], 0, "fin",    "paso 5: ve la marca del borde → se detiene.  Total = 5 = 2t+1"),
    ]
    colores = {"inicio": GRIS, "ida": "#f4c7c3", "escribe": "#c8e6c9",
               "vuelta": "#c5d9f5", "fin": "#fff3b0"}
    fig, ax = plt.subplots(figsize=(11, 6))
    for r, (cinta, cab, fase, texto) in enumerate(pasos):
        y = -r * 1.15
        for j, b in enumerate(cinta):
            dibuja_celda(ax, j * 1.0, y, b, colores[fase])
        # cabezal
        ax.annotate("", xy=(cab + 0.45, y + 0.95), xytext=(cab + 0.45, y + 1.12),
                    arrowprops=dict(arrowstyle="-|>", color=ROJO, lw=2.2))
        ax.text(3.4, y + 0.45, texto, va="center", fontsize=10.5)
        ax.text(-0.35, y + 0.45, f"paso {r}", ha="right", va="center",
                fontsize=9, color="gray")
    ax.text(0.45, 1.45, "LSB", ha="center", fontsize=9, color="gray")
    ax.text(2.45, 1.45, "MSB", ha="center", fontsize=9, color="gray")
    ax.set_xlim(-1.6, 11.5)
    ax.set_ylim(-6.5, 1.8)
    ax.axis("off")
    ax.set_title("Figura 1 · Un incremento caro: 3 → 4  (t = 2 unos seguidos, coste 2t+1 = 5)",
                 fontsize=13, fontweight="bold")
    fig.text(0.5, 0.02,
             "Rojo = ida destruyendo unos · Verde = escribe el nuevo 1 · Azul = vuelta · Flecha roja = cabezal",
             ha="center", fontsize=9.5, color="gray")
    fig.savefig("fig1_traza_maquina.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------- figura 2
def fig2():
    m, k = 8, 4
    datos = historial(m, k)
    fig, ax = plt.subplots(figsize=(11, 8))
    cabeceras = ["i", "cinta\n(b0 b1 b2 b3)", "t", "coste\nreal", "Φ = 2·\n(#unos)", "ΔΦ", "coste\namortizado"]
    xs_text = [-1.2, None, 4.7, 5.9, 7.4, 9.1, 10.4]
    for x, h in zip(xs_text, cabeceras):
        if x is not None:
            ax.text(x, 1.05, h, ha="center", va="bottom", fontsize=9.5, fontweight="bold")
    ax.text(2.0, 1.05, cabeceras[1], ha="center", va="bottom", fontsize=9.5, fontweight="bold")
    total_real = 0
    for i, (cinta, t, c) in enumerate(datos):
        y = -i * 1.05
        anterior = datos[i - 1][0] if i else None
        for j, b in enumerate(cinta):
            fondo = "white"
            if anterior is not None and anterior[j] != b:
                fondo = "#f4c7c3" if anterior[j] == 1 else "#c8e6c9"  # 1→0 rojo, 0→1 verde
            elif b == 1:
                fondo = "#dcdcdc"
            dibuja_celda(ax, j, y, b, fondo, tam=0.9)
        ax.text(-1.2, y + 0.45, str(i), ha="center", va="center", fontsize=11)
        if i:
            total_real += c
            d = phi(cinta) - phi(anterior)
            ax.text(4.7, y + 0.45, str(t), ha="center", va="center", fontsize=11)
            col = ROJO if c >= 5 else OSCURO
            ax.text(5.9, y + 0.45, str(c), ha="center", va="center", fontsize=12,
                    fontweight="bold" if c >= 5 else None, color=col)
            ax.text(9.1, y + 0.45, f"{d:+d}", ha="center", va="center", fontsize=11,
                    color=VERDE if d > 0 else (ROJO if d < 0 else "gray"))
            ax.text(10.4, y + 0.45, str(c + d), ha="center", va="center", fontsize=12,
                    fontweight="bold", color=AZUL)
        ax.text(7.4, y + 0.45, str(phi(cinta)), ha="center", va="center", fontsize=11)
    yfin = -(m + 1) * 1.05
    ax.plot([-1.7, 11], [yfin + 0.95, yfin + 0.95], color="gray", lw=0.8)
    ax.text(5.9, yfin + 0.4, f"Σ = {total_real}", ha="center", fontsize=12, fontweight="bold")
    ax.text(10.4, yfin + 0.4, f"Σ = {3*m}", ha="center", fontsize=12, fontweight="bold", color=AZUL)
    ax.text(0, yfin - 0.35,
            f"Comprobación: Σ real = 3m − Φ(D_m) + Φ(D_0) = {3*m} − {phi(datos[-1][0])} + 0 = {total_real}  ✓",
            fontsize=11.5, fontweight="bold")
    ax.text(0, yfin - 0.95,
            "Verde = bit que pasa 0→1 (se «ahorra» 2 monedas) · Rojo = bits que pasan 1→0 (se «gastan» sus monedas)",
            fontsize=9.5, color="gray")
    ax.set_xlim(-2, 11.6)
    ax.set_ylim(yfin - 1.4, 2.0)
    ax.axis("off")
    ax.set_title("Figura 2 · Contando de 0 a 8: cada incremento paga 3 amortizado, aunque el coste real oscile",
                 fontsize=12.5, fontweight="bold")
    fig.savefig("fig2_contador_0_a_8.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------- figura 3
def fig3():
    m, k = 32, 6
    datos = historial(m, k)
    idx = list(range(1, m + 1))
    reales = [datos[i][2] for i in idx]
    fig, ax = plt.subplots(figsize=(11, 5.5))
    colores = [ROJO if c >= 7 else (AZUL if c >= 3 else "#9ec5f4") for c in reales]
    ax.bar(idx, reales, color=colores, edgecolor="white")
    ax.axhline(3, color=VERDE, lw=2.5, ls="--", label="coste amortizado = 3 (constante)")
    media = sum(reales) / m
    ax.axhline(media, color="gray", lw=1.2, ls=":", label=f"media real ≈ {media:.2f}")
    ax.axhline(2 * k + 1, color=ROJO, lw=1, ls="-.", alpha=0.6,
               label=f"peor caso de UNA operación = 2k+1 = {2*k+1}")
    for i, c in zip(idx, reales):
        if c >= 7:
            ax.text(i, c + 0.25, f"i={i}\n{c}", ha="center", fontsize=8.5, color=ROJO)
    ax.set_xlabel("incremento número i")
    ax.set_ylabel("pasos de la máquina de Turing")
    ax.set_title("Figura 3 · Los incrementos caros son raros: el de coste 2t+1 ocurre cada 2^t pasos",
                 fontsize=13, fontweight="bold")
    ax.legend(loc="upper left", fontsize=9.5)
    ax.set_ylim(0, 2 * k + 3)
    ax.grid(axis="y", alpha=0.3)
    fig.savefig("fig3_coste_por_incremento.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------- figura 4
def fig4():
    m, k = 40, 7
    datos = historial(m, k)
    pot = [phi(d[0]) for d in datos]
    acum, s = [0], 0
    for d in datos[1:]:
        s += d[2]
        acum.append(s)
    xs = list(range(m + 1))
    cota = [3 * i for i in xs]

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 5.2))

    a1.step(xs, pot, where="post", color=AZUL, lw=2)
    a1.fill_between(xs, pot, step="post", color=AZUL, alpha=0.15)
    a1.axhline(0, color=OSCURO, lw=1)
    a1.set_title("Φ(D_i) = 2·(número de unos):  nunca baja de 0", fontsize=11.5, fontweight="bold")
    a1.set_xlabel("incremento i")
    a1.set_ylabel("monedas guardadas (deuda)")
    a1.annotate("Φ(D_0)=0", (0, 0), (2.5, 0.9), arrowprops=dict(arrowstyle="->"), fontsize=9.5,
                bbox=dict(fc="white", ec="none", pad=1))
    a1.annotate("i=32: incremento caro,\nse pagan las deudas", (32, 2), (33.5, 10.6),
                arrowprops=dict(arrowstyle="->", color=ROJO), fontsize=9.5, color=ROJO,
                ha="center")
    a1.set_ylim(0, 12.5)
    a1.grid(alpha=0.3)

    a2.plot(xs, cota, color=VERDE, lw=2, ls="--", label="3m  (suma de costes amortizados)")
    a2.plot(xs, acum, color=ROJO, lw=2.2, label="coste real acumulado Σ cᵢ")
    a2.fill_between(xs, acum, cota, color=VERDE, alpha=0.15,
                    label="hueco = Φ(D_m) ≥ 0")
    a2.set_title("Suma telescópica:  Σ cᵢ = 3m − Φ(D_m) ≤ 3m", fontsize=11.5, fontweight="bold")
    a2.set_xlabel("m = número de incrementos")
    a2.set_ylabel("pasos acumulados")
    a2.legend(loc="upper left", fontsize=9.5)
    a2.grid(alpha=0.3)

    fig.suptitle("Figura 4 · El potencial es la deuda; como termina ≥ donde empezó, la cota 3m es válida",
                 fontsize=13, fontweight="bold", y=1.02)
    fig.savefig("fig4_potencial_y_suma.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    fig1(); fig2(); fig3(); fig4()
    print("Listo: 4 imágenes generadas.")