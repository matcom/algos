import os
import random

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon

OUT = os.path.dirname(os.path.abspath(__file__))

# Paleta (azul = proponentes, rosa = receptores, verde = pareja, rojo = rechazo/bloqueo)
AZUL, ROSA, VERDE = "#2f6fdd", "#c2417a", "#2e9e5b"
ROJO, NARANJA, GRIS = "#d64545", "#e08a1e", "#9aa5b1"

# ----------------------------------------------------------------------------
# Instancia de ejemplo: listas incompletas de los proponentes.
# Las receptoras ordenan a todos los proponentes.
# ----------------------------------------------------------------------------
MEN = ["m1", "m2", "m3", "m4"]
WOM = ["w1", "w2", "w3", "w4"]
L = {"m1": ["w1", "w2"], "m2": ["w1", "w3"], "m3": ["w1", "w2"], "m4": ["w1"]}
PW = {
    "w1": ["m3", "m1", "m2", "m4"],
    "w2": ["m1", "m3", "m2", "m4"],
    "w3": ["m2", "m4", "m1", "m3"],
    "w4": ["m3", "m4", "m1", "m2"],
}
YM = {m: 3 - i for i, m in enumerate(MEN)}
YW = {w: 3 - i for i, w in enumerate(WOM)}


# ----------------------------------------------------------------------------
# Algoritmo Gale-Shapley adaptado a listas incompletas
# ----------------------------------------------------------------------------
def gale_shapley(L, PW):
    """Devuelve (mu_m, iteraciones, phi0, traza). mu_m: dict proponente -> receptora."""
    men = sorted(L)
    rank_w = {w: {m: i for i, m in enumerate(p)} for w, p in PW.items()}
    p = {m: 0 for m in men}          # puntero a la siguiente propuesta de cada m
    mu_m, mu_w = {}, {}
    phi0 = sum(len(L[m]) for m in men)
    trace = []

    def snap(desc, m=None, w=None, kind=None):
        trace.append(dict(desc=desc, m=m, w=w, kind=kind, mu=dict(mu_m),
                          k=dict(p), phi=sum(len(L[x]) - p[x] for x in men)))

    snap("Estado inicial: todos libres")
    it = 0
    while True:
        libres = [m for m in men if m not in mu_m and p[m] < len(L[m])]
        if not libres:
            break
        m = libres[0]
        w = L[m][p[m]]
        p[m] += 1
        it += 1
        if w not in mu_w:
            mu_m[m], mu_w[w] = w, m
            snap(f"{m} propone a {w} (libre)  ->  {w} acepta", m, w, "accept")
        else:
            cur = mu_w[w]
            if rank_w[w][m] < rank_w[w][cur]:
                del mu_m[cur]
                mu_m[m], mu_w[w] = w, m
                snap(f"{m} propone a {w}: {w} prefiere {m} a {cur}  ->  {cur} queda libre",
                     m, w, "displace")
            else:
                snap(f"{m} propone a {w}: {w} prefiere a {cur}  ->  {m} es rechazado",
                     m, w, "reject")
    return mu_m, it, phi0, trace


def pares_bloqueantes(L, PW, mu_m):
    """Pares (m,w) bloqueantes segun la definicion adaptada (3 condiciones)."""
    mu_w = {w: m for m, w in mu_m.items()}
    rank_w = {w: {m: i for i, m in enumerate(p)} for w, p in PW.items()}
    res = []
    for m in L:
        for w in L[m]:                                   # cond. 1: w es aceptable para m
            if mu_m.get(m) == w:
                continue
            m_prefiere = (m not in mu_m) or L[m].index(w) < L[m].index(mu_m[m])      # cond. 2
            w_prefiere = (w not in mu_w) or rank_w[w][m] < rank_w[w][mu_w[w]]        # cond. 3
            if m_prefiere and w_prefiere:
                res.append((m, w))
    return res


MU, ITER, PHI0, TRACE = gale_shapley(L, PW)
assert not pares_bloqueantes(L, PW, MU), "el resultado deberia ser estable"


# ----------------------------------------------------------------------------
# Utilidades de dibujo
# ----------------------------------------------------------------------------
def draw_graph(ax, mu=None, prop=None, kind=None, unlisted=None, final=False, caption=""):
    ax.clear()
    ax.set_xlim(-1.6, 2.5)
    ax.set_ylim(-1.2, 3.9)
    ax.axis("off")
    mu = mu or {}

    # aristas listadas con su posicion en la lista del proponente
    for m in MEN:
        for r, w in enumerate(L[m], start=1):
            ax.plot([0, 1], [YM[m], YW[w]], color=GRIS, lw=1.3, zorder=1)
            ax.text(0.2, YM[m] + 0.2 * (YW[w] - YM[m]), str(r), fontsize=8, ha="center",
                    va="center", color="#444", zorder=2,
                    bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    # aristas NO listadas (el proponente prefiere quedarse solo)
    for m, w in (unlisted or []):
        ax.plot([0, 1], [YM[m], YW[w]], color=ROJO, lw=1.4, ls=(0, (4, 3)), alpha=.8, zorder=1)
        ax.text(0.5, (YM[m] + YW[w]) / 2, "×", fontsize=15, color=ROJO, ha="center",
                va="center", zorder=2, bbox=dict(boxstyle="circle,pad=0.05", fc="white", ec="none"))
    # emparejamiento actual
    for m, w in mu.items():
        ax.plot([0, 1], [YM[m], YW[w]], color=VERDE, lw=4, zorder=3, solid_capstyle="round")
    # propuesta actual
    if prop:
        m, w = prop
        col = {"accept": AZUL, "reject": ROJO, "displace": NARANJA}.get(kind, AZUL)
        ax.annotate("", xy=(0.92, YW[w]), xytext=(0.08, YM[m]), zorder=4,
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=3, shrinkA=0, shrinkB=0,
                                    mutation_scale=18))

    solos_m = [m for m in MEN if m not in mu]
    solos_w = [w for w in WOM if w not in mu.values()]
    for m in MEN:
        ax.scatter([0], [YM[m]], s=950, fc="#cfe3ff", ec=AZUL, lw=2, zorder=5)
        ax.text(0, YM[m], m, ha="center", va="center", fontsize=11, weight="bold", zorder=6)
        ax.text(-0.2, YM[m], "L(%s) = (%s)" % (m, ", ".join(L[m])), ha="right", va="center",
                fontsize=9)
        if final and m in solos_m:
            ax.text(0, YM[m] - 0.36, "solo", ha="center", fontsize=8, color=ROJO, weight="bold")
    for w in WOM:
        ax.scatter([1], [YW[w]], s=950, fc="#ffe0ec", ec=ROSA, lw=2, zorder=5)
        ax.text(1, YW[w], w, ha="center", va="center", fontsize=11, weight="bold", zorder=6)
        ax.text(1.2, YW[w], "%s: %s" % (w, " ≻ ".join(PW[w])), ha="left", va="center", fontsize=9)
        if final and w in solos_w:
            ax.text(1, YW[w] - 0.36, "sola", ha="center", fontsize=8, color=ROJO, weight="bold")
    ax.text(0, 3.65, "Proponentes M", ha="center", fontsize=10, color=AZUL, weight="bold")
    ax.text(1, 3.65, "Receptores W", ha="center", fontsize=10, color=ROSA, weight="bold")
    if caption:
        ax.text(0.5, -0.85, caption, ha="center", va="center", fontsize=10.5)


def box(ax, x, y, w, h, text, fc="#eef3fb", ec=AZUL, fs=10):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle="round,pad=0.02,rounding_size=0.15", fc=fc, ec=ec, lw=1.6))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs)


def diamond(ax, x, y, w, h, text, fc="#fff6e0", ec=NARANJA, fs=10):
    ax.add_patch(Polygon([(x, y + h / 2), (x + w / 2, y), (x, y - h / 2), (x - w / 2, y)],
                         closed=True, fc=fc, ec=ec, lw=1.6))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs)


def arrow(ax, p, q, text=None, off=(0.15, 0.0), color="#444"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=14, lw=1.5, color=color))
    if text:
        ax.text((p[0] + q[0]) / 2 + off[0], (p[1] + q[1]) / 2 + off[1], text, fontsize=9.5,
                weight="bold", color=color, ha="left" if off[0] > 0 else "center", va="center")


# ----------------------------------------------------------------------------
# FIGURA 1 - El problema: modelo con listas incompletas
# ----------------------------------------------------------------------------
def fig1():
    fig, ax = plt.subplots(figsize=(9.5, 6))
    draw_graph(ax, unlisted=[("m1", "w3"), ("m4", "w4")],
               caption="línea gris + número = w ∈ L(m) y su posición en la lista de m\n"
                       "línea roja punteada × = w ∉ L(m): m prefiere quedarse solo antes que con w")
    ax.set_title("Pregunta 12 · Modelo de Gale–Shapley con listas incompletas",
                 fontsize=13, weight="bold")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig1_modelo_listas_incompletas.png"), dpi=140)
    plt.close(fig)


# ----------------------------------------------------------------------------
# FIGURA 2 - Diagrama de flujo del algoritmo adaptado
# ----------------------------------------------------------------------------
def fig2():
    fig, ax = plt.subplots(figsize=(9, 10.5))
    ax.set_xlim(0, 13.2)
    ax.set_ylim(0, 14.4)
    ax.axis("off")
    ax.set_title("Algoritmo de Gale–Shapley adaptado a listas incompletas", fontsize=13, weight="bold")

    box(ax, 5, 13.1, 5.0, 1.0, "Inicio:  μ = ∅ ,  p(m) = 1  ∀ m", fs=10)
    diamond(ax, 5, 10.8, 4.8, 2.2, "¿∃ m libre con\np(m) ≤ |L(m)| ?", fs=10)
    box(ax, 1.1, 10.8, 2.0, 1.2, "Devolver μ\n(fin)", fc="#e6f5ec", ec=VERDE, fs=9.5)
    box(ax, 5, 8.2, 5.0, 1.3, "w ← L(m)[p(m)] ;  p(m) ← p(m) + 1\n(solo se propone a listadas)", fs=9.5)
    diamond(ax, 5, 6.0, 4.0, 1.8, "¿w está libre?", fs=10)
    box(ax, 10.2, 6.0, 3.6, 1.1, "μ ← μ ∪ {(m, w)}", fc="#e6f5ec", ec=VERDE)
    diamond(ax, 5, 3.6, 4.4, 1.9, "¿w prefiere m\na μ(w) ?", fs=10)
    box(ax, 10.2, 3.6, 3.6, 1.2, "μ(w) ← m\nm' queda libre", fc="#fdeede", ec=NARANJA)
    box(ax, 5, 1.2, 3.8, 1.1, "m es rechazado\n(sigue libre)", fc="#fbe7e7", ec=ROJO)

    arrow(ax, (5, 12.6), (5, 11.9))
    arrow(ax, (2.6, 10.8), (2.1, 10.8), "No", off=(0, 0.35))
    arrow(ax, (5, 9.7), (5, 8.85), "Sí")
    arrow(ax, (5, 7.55), (5, 6.9))
    arrow(ax, (7.0, 6.0), (8.4, 6.0), "Sí", off=(0, 0.35))
    arrow(ax, (5, 5.1), (5, 4.55), "No")
    arrow(ax, (7.2, 3.6), (8.4, 3.6), "Sí", off=(0, 0.35))
    arrow(ax, (5, 2.65), (5, 1.75), "No")

    # lazo de retorno
    ax.plot([12.0, 12.6], [6.0, 6.0], color="#444", lw=1.5)
    ax.plot([12.0, 12.6], [3.6, 3.6], color="#444", lw=1.5)
    ax.plot([6.9, 12.6], [1.2, 1.2], color="#444", lw=1.5)
    ax.plot([12.6, 12.6], [1.2, 10.8], color="#444", lw=1.5)
    arrow(ax, (12.6, 10.8), (7.4, 10.8))

    ax.text(0.1, 8.4, "Cambio clave:\nsolo se propone a\nreceptoras listadas;\nal agotar su lista,\nm termina soltero.",
            fontsize=8.5, style="italic", color=ROJO, va="center")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig2_algoritmo_flujo.png"), dpi=140)
    plt.close(fig)


# ----------------------------------------------------------------------------
# FIGURA 3 - GIF con la traza del algoritmo
# ----------------------------------------------------------------------------
def fig3():
    fig, ax = plt.subplots(figsize=(9.5, 6.2))
    n = len(TRACE)

    def update(i):
        s = TRACE[i] if i < n else None
        if s is not None:
            prop = (s["m"], s["w"]) if s["m"] else None
            cap = "Paso %d/%d   ·   %s\nΦ = %d  (propuestas pendientes)" % (
                i, n - 1, s["desc"], s["phi"])
            draw_graph(ax, s["mu"], prop, s["kind"], caption=cap)
        else:                                            # fotograma final
            f = TRACE[-1]
            solos = [m for m in MEN if m not in f["mu"]]
            cap = ("FIN: μ = {%s}\n%s agotó su lista y queda solo; no hay pareja bloqueante  ⇒  μ es estable"
                   % (", ".join("(%s,%s)" % (m, w) for m, w in sorted(f["mu"].items())),
                      ", ".join(solos) if solos else "nadie"))
            draw_graph(ax, f["mu"], final=True, caption=cap)
        ax.set_title("Traza del algoritmo  (azul: acepta · naranja: desplaza · rojo: rechaza · verde: pareja)",
                     fontsize=10.5, weight="bold")

    anim = FuncAnimation(fig, update, frames=n + 2, interval=1400)
    anim.save(os.path.join(OUT, "fig3_traza_algoritmo.gif"), writer=PillowWriter(fps=0.75))
    plt.close(fig)


# ----------------------------------------------------------------------------
# FIGURA 4 - El potencial Phi
# ----------------------------------------------------------------------------
def fig4():
    ts = list(range(len(TRACE)))
    phis = [s["phi"] for s in TRACE]
    fig, (a, b) = plt.subplots(1, 2, figsize=(12, 5), gridspec_kw={"width_ratios": [1, 1.1]})

    a.plot(ts, phis, "-o", color=AZUL, lw=2.5, ms=8, zorder=3)
    a.axhline(0, color=ROJO, ls="--", lw=1.4)
    a.text(len(ts) - 1, 0.18, "Φ ≥ 0", color=ROJO, ha="right", fontsize=10)
    a.axhline(phis[0], color=GRIS, ls=":", lw=1.4)
    a.text(len(ts) - 1, phis[0] + 0.18, "$\\Phi_0$ = Σ|L(m)| = %d  (cota de iteraciones)" % phis[0],
           ha="right", fontsize=10, color="#555")
    for i in range(1, len(ts)):
        a.annotate("−1", ((ts[i - 1] + ts[i]) / 2, (phis[i - 1] + phis[i]) / 2 + 0.25),
                   ha="center", fontsize=9, color=AZUL, weight="bold")
    a.set_xlabel("iteración t")
    a.set_ylabel("Φ(t) = Σ (|L(m)| − k_m)")
    a.set_title("Φ baja exactamente 1 en cada iteración", fontsize=11.5, weight="bold")
    a.set_ylim(-0.6, phis[0] + 1.3)
    a.set_xticks(ts)
    a.grid(alpha=.25)

    cols = ["#4e79a7", "#f28e2b", "#59a14f", "#b07aa1"]
    bottom = [0] * len(ts)
    for c, m in zip(cols, MEN):
        vals = [len(L[m]) - s["k"][m] for s in TRACE]
        b.bar(ts, vals, bottom=bottom, color=c, label=m, edgecolor="white", width=0.7)
        bottom = [x + y for x, y in zip(bottom, vals)]
    b.set_xlabel("iteración t")
    b.set_ylabel("propuestas restantes por proponente")
    b.set_title("Φ(t) = altura total de la pila  (|L(m)| − k_m por proponente)",
                fontsize=11.5, weight="bold")
    b.set_xticks(ts)
    b.legend(title="proponente", ncol=4, loc="upper right", fontsize=9)
    b.set_ylim(0, phis[0] + 1.6)
    fig.suptitle("Potencial del algoritmo adaptado:  termina en ≤ $\\Phi_0$ iteraciones", fontsize=13, weight="bold")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig4_potencial.png"), dpi=140)
    plt.close(fig)


# ----------------------------------------------------------------------------
# FIGURA 5 - Pareja bloqueante (definicion adaptada)
# ----------------------------------------------------------------------------
def fig5():
    fig, (ax, tx) = plt.subplots(1, 2, figsize=(13, 5.6), gridspec_kw={"width_ratios": [1.15, 1]})
    ax.set_xlim(-1.9, 3.2)
    ax.set_ylim(-1.3, 2.6)
    ax.axis("off")
    ym = {"m1": 1.6, "m2": 0.2}
    yw = {"w1": 1.6, "w2": 0.2}
    # emparejamiento mu = {(m1,w1)}
    ax.plot([0, 1], [ym["m1"], yw["w1"]], color=VERDE, lw=5, zorder=2)
    ax.text(0.5, 1.82, "μ", color=VERDE, ha="center", fontsize=12, weight="bold")
    # par bloqueante (m2,w1)
    ax.plot([0, 1], [ym["m2"], yw["w1"]], color=ROJO, lw=3.2, zorder=2)
    ax.text(0.28, 0.62, "BLOQUEANTE\n(m2, w1)", color=ROJO, fontsize=10, weight="bold",
            ha="center", va="center", bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=ROJO))
    # par NO bloqueante (m1,w2): w2 no esta en L(m1)
    ax.plot([0, 1], [ym["m1"], yw["w2"]], color=GRIS, lw=2, ls=(0, (4, 3)), zorder=1)
    ax.text(0.78, 0.62, "×", color=GRIS, fontsize=18, ha="center", va="center",
            bbox=dict(boxstyle="circle,pad=0.05", fc="white", ec="none"))
    ax.text(1.45, 0.62, "(m1, w2) no bloquea:\nw2 ∉ L(m1)", color="#555", fontsize=9.5, va="center")

    for m in ym:
        ax.scatter([0], [ym[m]], s=1100, fc="#cfe3ff", ec=AZUL, lw=2, zorder=5)
        ax.text(0, ym[m], m, ha="center", va="center", fontsize=11, weight="bold", zorder=6)
    for w in yw:
        ax.scatter([1], [yw[w]], s=1100, fc="#ffe0ec", ec=ROSA, lw=2, zorder=5)
        ax.text(1, yw[w], w, ha="center", va="center", fontsize=11, weight="bold", zorder=6)
    ax.text(-0.22, ym["m1"], "L(m1) = (w1)", ha="right", va="center", fontsize=9.5)
    ax.text(-0.22, ym["m2"], "L(m2) = (w1, w2)", ha="right", va="center", fontsize=9.5)
    ax.text(1.2, 1.6, "w1:  m2 ≻ m1", va="center", fontsize=9.5)
    ax.text(0.5, -0.35, "m2 está solo en μ", ha="center", fontsize=10, color=ROJO)
    ax.set_title("Ejemplo", fontsize=12, weight="bold")

    tx.axis("off")
    tx.set_xlim(0, 1)
    tx.set_ylim(0, 1)
    tx.text(0.0, 0.97, "(m, w) es bloqueante para μ  ⇔  se cumplen las 3 condiciones",
            fontsize=11.5, weight="bold", va="top")
    items = [
        ("1", AZUL, "w es aceptable para m:  w ∈ L(m)",
         "(condición nueva: m nunca bloquea con quien no listó)"),
        ("2", AZUL, "m prefiere w a su situación actual",
         "μ(m) = ∅  ó  w está por encima de μ(m) en L(m)"),
        ("3", ROSA, "w prefiere m a su situación actual",
         "μ(w) = ∅  ó  w ordena m por encima de μ(w)"),
    ]
    y = 0.80
    for num, col, t1, t2 in items:
        tx.add_patch(FancyBboxPatch((0.0, y - 0.16), 0.97, 0.19, boxstyle="round,pad=0.01,rounding_size=0.02",
                                    fc="#f7f9fc", ec=col, lw=1.6))
        tx.text(0.03, y - 0.065, num, fontsize=16, weight="bold", color=col, va="center")
        tx.text(0.09, y - 0.02, t1, fontsize=10.5, weight="bold", va="center")
        tx.text(0.09, y - 0.11, t2, fontsize=9.5, va="center", color="#444")
        y -= 0.25
    tx.text(0.0, 0.0, "μ es estable  ⇔  es individualmente racional (nadie con una pareja\n"
                      "inaceptable) y no tiene ninguna pareja bloqueante.",
            fontsize=10.5, va="bottom", color="#222",
            bbox=dict(boxstyle="round,pad=0.4", fc="#e6f5ec", ec=VERDE))
    fig.suptitle("Definición de pareja bloqueante con listas incompletas", fontsize=13, weight="bold")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig5_pareja_bloqueante.png"), dpi=140)
    plt.close(fig)


# ----------------------------------------------------------------------------
# FIGURA 6 - Esquema de la demostracion de estabilidad
# ----------------------------------------------------------------------------
def fig6():
    fig, ax = plt.subplots(figsize=(11, 8.6))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10.2)
    ax.axis("off")
    ax.set_title("Demostración: el resultado μ es estable (por contradicción)", fontsize=13, weight="bold")

    box(ax, 7, 9.3, 8.6, 1.0, "Supongamos que (m, w) es bloqueante para μ\n"
        "cond. 1: w ∈ L(m)   ·   cond. 2: m prefiere w a μ(m)   ·   cond. 3: w prefiere m a μ(w)", fs=10)
    box(ax, 7, 7.4, 9.6, 1.3,
        "Lema 2 ⇒ m le propuso a w antes de terminar\n"
        "(si m acaba libre propuso a toda L(m); si acaba con μ(m) por debajo de w, propuso a w antes)",
        fc="#eef3fb", fs=10)
    box(ax, 3.4, 5.3, 6.0, 1.4, "Caso A: w rechazó a m\nw tenía una pareja m* con  $m^{*} \\succ_w m$",
        fc="#fbe7e7", ec=ROJO, fs=10)
    box(ax, 10.6, 5.3, 6.0, 1.4, "Caso B: w aceptó a m y luego lo dejó\npor un m* con  $m^{*} \\succ_w m$",
        fc="#fdeede", ec=NARANJA, fs=10)
    box(ax, 7, 3.2, 9.4, 1.3,
        "Lema 1: la pareja de w solo mejora con el tiempo\n"
        "μ(w) = m*  ó  mejor para w que m*   ⇒   μ(w) $\\succ_w$ m", fc="#eef3fb", fs=10.5)
    box(ax, 7, 1.1, 10.4, 1.4,
        "Entonces w NO prefiere m a μ(w): se contradice la condición 3\n"
        "⇒ no existe pareja bloqueante  ⇒  μ es estable   ∎", fc="#e6f5ec", ec=VERDE, fs=11)

    arrow(ax, (7, 8.8), (7, 8.05))
    arrow(ax, (5.6, 6.75), (3.8, 6.0), "")
    arrow(ax, (8.4, 6.75), (10.2, 6.0), "")
    ax.text(7, 6.15, "w respondió así\n(solo hay 2 casos)", fontsize=9, ha="center", color="#555")
    arrow(ax, (3.4, 4.6), (5.4, 3.85))
    arrow(ax, (10.6, 4.6), (8.6, 3.85))
    arrow(ax, (7, 2.55), (7, 1.8))
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig6_demostracion_estabilidad.png"), dpi=140)
    plt.close(fig)


# ----------------------------------------------------------------------------
# FIGURA 7 - Comprobacion experimental
# ----------------------------------------------------------------------------
def random_instance(n, rng):
    men = ["m%d" % i for i in range(1, n + 1)]
    wom = ["w%d" % i for i in range(1, n + 1)]
    Lr = {m: rng.sample(wom, rng.randint(1, n)) for m in men}
    PWr = {w: rng.sample(men, n) for w in wom}
    return Lr, PWr


def random_matching(Lr, rng):
    mu, used = {}, set()
    order = list(Lr)
    rng.shuffle(order)
    for m in order:
        opts = [w for w in Lr[m] if w not in used]
        if opts and rng.random() < 0.8:
            w = rng.choice(opts)
            mu[m] = w
            used.add(w)
    return mu


def fig7(trials=500, n=8):
    rng = random.Random(7)
    iters, phis, gs_bad, rnd_bad = [], [], 0, 0
    for _ in range(trials):
        Lr, PWr = random_instance(n, rng)
        mu, it, phi0, _t = gale_shapley(Lr, PWr)
        assert it <= phi0                                  # teorema del potencial
        assert all(w in Lr[m] for m, w in mu.items())      # racionalidad individual
        iters.append(it)
        phis.append(phi0)
        gs_bad += bool(pares_bloqueantes(Lr, PWr, mu))
        rnd_bad += bool(pares_bloqueantes(Lr, PWr, random_matching(Lr, rng)))

    fig, (a, b) = plt.subplots(1, 2, figsize=(12, 5))
    a.scatter(phis, iters, s=22, alpha=.55, color=AZUL, edgecolor="none")
    mx = max(phis) + 1
    a.plot([0, mx], [0, mx], "--", color=ROJO, lw=1.6, label="iteraciones = $\\Phi_0$ (cota)")
    a.set_xlim(0, mx)
    a.set_ylim(0, mx)
    a.set_xlabel("$\\Phi_0$ = Σ|L(m)|")
    a.set_ylabel("iteraciones realizadas")
    a.set_title("Terminación: todas bajo la cota $\\Phi_0$", fontsize=11.5, weight="bold")
    a.legend(loc="upper left")
    a.grid(alpha=.25)

    vals = [100 * gs_bad / trials, 100 * rnd_bad / trials]
    bars = b.bar(["Gale–Shapley\nadaptado", "emparejamiento\naleatorio válido"], vals,
                 color=[VERDE, ROJO], width=0.55)
    for bar, v, c in zip(bars, vals, [gs_bad, rnd_bad]):
        b.text(bar.get_x() + bar.get_width() / 2, v + 2, "%d de %d\n(%.1f %%)" % (c, trials, v),
               ha="center", fontsize=10.5, weight="bold")
    b.set_ylim(0, 112)
    b.set_ylabel("% de instancias con ≥ 1 pareja bloqueante")
    b.set_title("Estabilidad: GS nunca produce pares bloqueantes", fontsize=11.5, weight="bold")
    b.grid(axis="y", alpha=.25)
    fig.suptitle("Verificación experimental (%d instancias aleatorias, n = %d, listas incompletas)"
                 % (trials, n), fontsize=13, weight="bold")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig7_verificacion_experimental.png"), dpi=140)
    plt.close(fig)
    return gs_bad, rnd_bad, trials


if __name__ == "__main__":
    fig1()
    fig2()
    fig3()
    fig4()
    fig5()
    fig6()
    gs_bad, rnd_bad, tr = fig7()
    print("Resultado del ejemplo:", dict(sorted(MU.items())), "| iteraciones:", ITER, "| Phi0:", PHI0)
    print("Experimento: GS con pares bloqueantes = %d/%d ; aleatorio = %d/%d" % (gs_bad, tr, rnd_bad, tr))
    print("Figuras guardadas en:", OUT)