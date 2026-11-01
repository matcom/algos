import math
import os
import random

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import PillowWriter, FuncAnimation
from matplotlib.patches import FancyBboxPatch, Polygon

CARPETA = os.path.dirname(os.path.abspath(__file__))
AZUL, NARANJA, VERDE, ROJO, GRIS = "#2b6cb0", "#dd7a1f", "#2f855a", "#c53030", "#718096"
plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False})


def guardar(fig, nombre):
    ruta = os.path.join(CARPETA, nombre)
    fig.savefig(ruta, dpi=140, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("generado:", ruta)


def par_minimo(x):
    """Par (i,j) de indices que minimiza |xi-xj| (via ordenacion)."""
    idx = sorted(range(len(x)), key=lambda k: x[k])
    return min(((idx[k], idx[k + 1]) for k in range(len(idx) - 1)),
               key=lambda p: abs(x[p[0]] - x[p[1]]))


# ---------------------------------------------------------------- Fig 1
def fig1_problema():
    rng = random.Random(7)
    x = sorted(rng.uniform(0, 10) for _ in range(9))
    i, j = par_minimo(x)
    fig, ax = plt.subplots(2, 1, figsize=(10, 5.2), gridspec_kw={"height_ratios": [1.2, 1]})
    a = ax[0]
    a.axhline(0, color="black", lw=1)
    a.scatter(x, np.zeros(len(x)), s=90, color=AZUL, zorder=3)
    a.scatter([x[i], x[j]], [0, 0], s=140, color=ROJO, zorder=4)
    for k, v in enumerate(x):
        a.text(v, -0.22, f"x{k + 1}", ha="center", color=GRIS)
    a.annotate("", xy=(x[j], 0.25), xytext=(x[i], 0.25),
               arrowprops=dict(arrowstyle="<->", color=ROJO, lw=2))
    a.text((x[i] + x[j]) / 2, 0.33, f"d = {x[j] - x[i]:.2f}", ha="center", color=ROJO, weight="bold")
    a.set_ylim(-0.5, 0.7); a.set_yticks([]); a.spines["left"].set_visible(False)
    a.set_title("Problema PC1: dada una lista en la recta, hallar el par (i, j), i≠j, con |xi − xj| mínimo")
    b = ax[1]
    gaps = [x[k + 1] - x[k] for k in range(len(x) - 1)]
    cols = [ROJO if k == i else AZUL for k in range(len(gaps))]
    b.bar(range(1, len(gaps) + 1), gaps, color=cols)
    b.set_xlabel("hueco consecutivo tras ordenar (k-ésimo, k+1-ésimo)")
    b.set_ylabel("tamaño del hueco")
    b.set_title("Basta mirar los n−1 huecos consecutivos del orden: el mínimo es la respuesta")
    fig.tight_layout()
    guardar(fig, "fig1_problema.png")


# ---------------------------------------------------------------- Fig 2
def caja(ax, xy, w, h, txt, fc="#ebf4ff", ec=AZUL, fs=10):
    ax.add_patch(FancyBboxPatch((xy[0] - w / 2, xy[1] - h / 2), w, h,
                                boxstyle="round,pad=0.02", fc=fc, ec=ec, lw=1.6))
    ax.text(xy[0], xy[1], txt, ha="center", va="center", fontsize=fs)


def flecha(ax, p, q, color="black"):
    ax.annotate("", xy=q, xytext=p, arrowprops=dict(arrowstyle="->", color=color, lw=1.4))


def fig2_reduccion():
    fig, ax = plt.subplots(figsize=(11, 6.2))
    ax.set_xlim(0, 11); ax.set_ylim(-0.3, 6.2); ax.axis("off")
    caja(ax, (1.1, 5.4), 1.9, 0.7, "Entrada de ED\nx₁,…,xₙ", "#fefcbf", "#b7791f")
    flecha(ax, (2.1, 5.4), (3.1, 5.4))
    ax.text(2.6, 5.7, "identidad\n(0 pruebas)", ha="center", fontsize=8, color=GRIS)
    # arbol T
    ax.add_patch(Polygon([[4.75, 5.3], [3.0, 2.9], [6.5, 2.9]], fc="#ebf4ff", ec=AZUL, lw=1.8))
    ax.text(4.75, 3.7, "Árbol T que resuelve PC1\nprofundidad T(n), grado ≤ d", ha="center", fontsize=10)
    ax.text(4.75, 5.55, "mismas pruebas de signo", ha="center", fontsize=9, color=AZUL)
    ax.text(4.75, 2.6, "hoja de T:  par (i, j)", ha="center", fontsize=10, color=ROJO, weight="bold")
    flecha(ax, (4.75, 2.4), (4.75, 1.95), ROJO)
    caja(ax, (4.75, 1.65), 2.3, 0.6, "¿ sgn( xᵢ − xⱼ ) ?", "#fed7d7", ROJO)
    ax.text(5.95, 2.15, "+1 prueba, grado 1", fontsize=8, color=ROJO)
    for dx, txt, c in [(-3.0, "< 0\ndistintos", VERDE), (0, "= 0\nhay iguales", ROJO), (3.0, "> 0\ndistintos", VERDE)]:
        flecha(ax, (4.75 + dx * 0.35, 1.35), (4.75 + dx, 0.55))
        caja(ax, (4.75 + dx, 0.3), 1.9, 0.6, txt, "#f0fff4" if c == VERDE else "#fff5f5", c, 9)
    ax.text(8.9, 4.6, "Conclusión", fontsize=12, weight="bold")
    ax.text(8.9, 3.0,
            "T′ resuelve ED con\nprofundidad T(n)+1.\n\nBen-Or: ED ≥ c·n log n\n⇒ T(n) ≥ c·n log n − 1\n⇒ PC1 = Ω(n log n)",
            fontsize=10, va="center")
    ax.set_title("Reducción ED ≤ PC1: se reutiliza T y cada hoja (i,j) se cambia por la prueba xᵢ − xⱼ", fontsize=12)
    guardar(fig, "fig2_reduccion.png")


# ---------------------------------------------------------------- Fig 3
def fig3_componentes():
    from itertools import permutations
    fig, ax = plt.subplots(1, 2, figsize=(12, 5.2))
    a = ax[0]
    e1, e2 = np.array([1, -1, 0]) / math.sqrt(2), np.array([1, 1, -2]) / math.sqrt(6)
    g = np.linspace(-2, 2, 500)
    U, V = np.meshgrid(g, g)
    X = [U * e1[k] + V * e2[k] for k in range(3)]
    perms = list(permutations(range(3)))
    code = np.zeros(U.shape)
    for k, p in enumerate(perms):
        m = (X[p[0]] < X[p[1]]) & (X[p[1]] < X[p[2]])
        code[m] = k + 1
    cmap = plt.get_cmap("Set3")
    a.imshow(np.ma.masked_equal(code, 0), extent=[-2, 2, -2, 2], origin="lower", cmap=cmap, vmin=0, vmax=8)
    for k, p in enumerate(perms):
        m = code == k + 1
        cu, cv = U[m].mean(), V[m].mean()
        a.text(cu, cv, "x" + "<x".join(str(q + 1) for q in p).replace("x", "x", 1), ha="center",
               va="center", fontsize=9)
    for ang in (30, 90, 150):
        t = math.radians(ang)
        a.plot([-2 * math.cos(t), 2 * math.cos(t)], [-2 * math.sin(t), 2 * math.sin(t)], color=ROJO, lw=2)
    a.set_title("n = 3: el conjunto «todos distintos» tiene 3! = 6 componentes\n(plano x₁+x₂+x₃=0; rectas rojas: xᵢ = xⱼ)")
    a.set_aspect("equal"); a.set_xticks([]); a.set_yticks([])
    b = ax[1]
    n = np.arange(2, 61)
    lg = np.array([math.lgamma(k + 1) / math.log(3) for k in n])
    b.plot(n, n * np.log2(n), color=NARANJA, lw=2, label="n log₂ n (cota ajustada)")
    b.plot(n, lg, color=ROJO, lw=2, label="log₃(n!)  (profundidad mínima)")
    b.plot(n, n, color=GRIS, lw=2, ls="--", label="n (lineal)")
    b.plot(n, n * (n - 1) / 2, color=AZUL, lw=2, ls=":", label="n(n−1)/2 (fuerza bruta)")
    b.set_ylim(0, 700)
    b.set_xlabel("n"); b.set_ylabel("pruebas de signo")
    b.set_title("Un árbol de profundidad h tiene ≤ 3ʰ hojas\n⇒ con ≥ n! componentes: h ≥ log₃ n! = Ω(n log n)")
    b.legend(frameon=False)
    fig.tight_layout()
    guardar(fig, "fig3_componentes_cota.png")


# ---------------------------------------------------------------- Fig 4
def fig4_modelo():
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.8))
    a = ax[0]
    xs = np.linspace(0, 8, 800)
    a.plot(xs, xs / 2.0, color=GRIS, ls="--", label="y = x/δ  (polinomio: sí es árbol)")
    a.step(xs, np.floor(xs / 2.0), where="post", color=ROJO, lw=2.5, label="⌊x/δ⌋ (δ = 2): NO polinomial")
    a.set_xlabel("x"); a.set_ylabel("índice de celda")
    a.set_title("La parte entera salta: no es continua\nni se obtiene con una prueba de signo")
    a.legend(frameon=False)
    b = ax[1]
    M = np.logspace(0, 6, 200)
    b.semilogx(M, np.log(M + 1) / math.log(3), color=ROJO, lw=2.5,
               label="profundidad mínima del árbol para calcular ⌊x⌋, x∈[0,M]: log₃(M+1)")
    b.axhline(1, color=VERDE, lw=2.5, label="RAM con ⌊·⌋: costo 1")
    b.set_xlabel("magnitud M de la entrada"); b.set_ylabel("operaciones")
    b.set_title("Una sola operación ⌊·⌋ de la RAM\nno cabe en profundidad constante de un árbol")
    b.legend(frameon=False, fontsize=9, loc="center right")
    fig.suptitle("Por qué el algoritmo de la sección 9 se sale del modelo de árboles algebraicos", y=1.03, fontsize=12)
    fig.tight_layout()
    guardar(fig, "fig4_modelo_floor.png")


# ---------------------------------------------------------------- Fig 5
def fig5_rejilla():
    rng = random.Random(11)
    delta = 1.0
    pts = []
    while len(pts) < 8:  # puntos a distancia >= delta entre si
        v = rng.uniform(0, 10)
        if all(abs(v - q) >= delta for q in pts):
            pts.append(v)
    p = 5.35
    pts = [q for q in pts if abs(q - p) >= delta]
    k = math.floor(p / delta)
    fig, ax = plt.subplots(figsize=(11, 3.8))
    for c in range(11):
        ax.axvline(c * delta, color=GRIS, lw=1)
        ax.text(c * delta + delta / 2, -0.55, f"celda {c}", ha="center", fontsize=8, color=GRIS)
    for c in (k - 1, k, k + 1):
        ax.axvspan(c * delta, (c + 1) * delta, color="#fefcbf", alpha=0.8)
    ax.axvspan(k * delta, (k + 1) * delta, color="#fbd38d", alpha=0.8)
    ax.axhline(0, color="black", lw=1)
    ax.scatter(pts, np.zeros(len(pts)), s=90, color=AZUL, zorder=3, label="puntos ya insertados")
    ax.scatter([p], [0], s=170, color=NARANJA, marker="D", zorder=4, label="punto nuevo pᵢ")
    ax.annotate("", xy=(p - delta, 0.55), xytext=(p + delta, 0.55), arrowprops=dict(arrowstyle="<->", color=ROJO, lw=2))
    ax.text(p, 0.68, "solo importan puntos a distancia < δ:\nestán en las celdas k−1, k, k+1", ha="center", color=ROJO)
    ax.text(0.1, 1.35, "Invariante: celdas de longitud δ ⇒ a lo sumo 1 punto por celda\n"
            "(dos puntos de la misma celda estarían a distancia < δ, imposible)", fontsize=10)
    ax.set_xlim(0, 10); ax.set_ylim(-0.8, 1.9); ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.legend(loc="lower right", frameon=False)
    ax.set_title("Rejilla 1D: 3 celdas por consulta (en 2D eran 25)")
    guardar(fig, "fig5_rejilla_1d.png")


# ----------------------------------------------- algoritmo instrumentado
def algoritmo(X, semilla=0, registro=None):
    """Devuelve (d, par, operaciones, reconstrucciones). 'registro' guarda el estado de cada paso."""
    pts = list(X)
    random.Random(semilla).shuffle(pts)
    d, par = abs(pts[0] - pts[1]), (pts[0], pts[1])
    ops, recon = 2, 0
    rej = {math.floor(q / d): q for q in pts[:2]}
    if registro is not None:
        registro.append(dict(i=2, p=None, d=d, par=par, celdas=[], accion="inicio", pts=pts[:2]))
    for i in range(2, len(pts)):
        p, k, antes = pts[i], math.floor(pts[i] / d), d
        for c in (k - 1, k, k + 1):
            ops += 1
            q = rej.get(c)
            if q is not None and abs(p - q) < d:
                d, par = abs(p - q), (p, q)
        if registro is not None:
            registro.append(dict(i=i + 1, p=p, d=antes, par=par, celdas=[k - 1, k, k + 1],
                                 accion="busca", pts=pts[:i], k=k))
        if d < antes:
            recon += 1
            ops += i + 1
            rej = {math.floor(q / d): q for q in pts[:i + 1]}
            if registro is not None:
                registro.append(dict(i=i + 1, p=p, d=d, par=par, celdas=[], accion="reconstruye", pts=pts[:i + 1]))
        else:
            ops += 1
            rej[k] = p
            if registro is not None:
                registro.append(dict(i=i + 1, p=p, d=d, par=par, celdas=[], accion="inserta", pts=pts[:i + 1]))
    return d, par, ops, recon


# ---------------------------------------------------------------- Fig 6 (GIF)
def fig6_gif():
    rng = random.Random(5)
    X = [rng.uniform(0, 1) for _ in range(11)]
    reg = []
    d_fin, par_fin, _, _ = algoritmo(X, semilla=1, registro=reg)
    fig, ax = plt.subplots(figsize=(10, 3.6))

    def dibuja(f):
        ax.clear()
        d = f["d"]
        ax.axhline(0, color="black", lw=1)
        c = 0
        while c * d <= 1.0001:
            ax.axvline(c * d, color="#cbd5e0", lw=0.8)
            c += 1
        for cc in f["celdas"]:
            ax.axvspan(cc * d, (cc + 1) * d, color="#fefcbf", alpha=0.9)
        ax.scatter(f["pts"], np.zeros(len(f["pts"])), s=80, color=AZUL, zorder=3)
        if f["p"] is not None:
            ax.scatter([f["p"]], [0], s=160, marker="D", color=NARANJA, zorder=4)
        a, b = f["par"]
        ax.plot([a, b], [0.15, 0.15], color=ROJO, lw=3)
        ax.scatter([a, b], [0, 0], s=130, color=ROJO, zorder=5, facecolors="none", linewidths=2)
        texto = {"inicio": "Paso 2: δ = |p₁−p₂|, rejilla con 2 puntos",
                 "busca": f"Llega p{f['i']}: se consultan solo 3 celdas (amarillas)",
                 "inserta": "δ no baja → se inserta p en su celda (O(1))",
                 "reconstruye": "¡δ baja! → se reconstruye la rejilla con el nuevo δ (O(i))"}[f["accion"]]
        ax.set_title(f"{texto}\nδ = {d:.3f}   |   puntos en rejilla: {len(f['pts'])}", fontsize=11)
        ax.set_xlim(-0.02, 1.02); ax.set_ylim(-0.45, 0.6); ax.set_yticks([])
        ax.spines["left"].set_visible(False)
        ax.text(0.5, -0.38, "amarillo: celdas consultadas · rojo: par más cercano actual · naranja: punto nuevo",
                ha="center", fontsize=8, color=GRIS)

    final = dict(i=len(X), p=None, d=d_fin, par=par_fin, celdas=[], accion="inserta", pts=list(X))
    frames = reg + [final]

    def actualiza(n):
        dibuja(frames[n])
        if n == len(frames) - 1:
            ax.set_title(f"Resultado: par más cercano a distancia δ = {d_fin:.3f}\n"
                         "(tiempo esperado O(n) en RAM con ⌊·⌋ y hash)", fontsize=11, color=VERDE)

    anim = FuncAnimation(fig, actualiza, frames=len(frames), repeat=False)
    ruta = os.path.join(CARPETA, "fig6_algoritmo_incremental.gif")
    anim.save(ruta, writer=PillowWriter(fps=1.3), dpi=90)
    plt.close(fig)
    print("generado:", ruta)


# ---------------------------------------------------------------- Fig 7
def fig7_costos():
    ns = [100, 200, 400, 800, 1600, 3200, 6400, 12800, 25600]
    ops_prom, rec_prom = [], []
    for n in ns:
        o, r = [], []
        for s in range(15):
            rng = random.Random(1000 * n + s)
            X = [rng.random() for _ in range(n)]
            _, _, ops, rc = algoritmo(X, semilla=s)
            o.append(ops); r.append(rc)
        ops_prom.append(np.mean(o)); rec_prom.append(np.mean(r))
    ns_a = np.array(ns, dtype=float)
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.8))
    a = ax[0]
    a.loglog(ns_a, ops_prom, "o-", color=VERDE, lw=2, label="rejilla aleatorizada (medido)")
    a.loglog(ns_a, ns_a * np.log2(ns_a), "s--", color=NARANJA, label="n log₂ n (ordenar / árboles)")
    a.loglog(ns_a, ns_a * (ns_a - 1) / 2, "^:", color=AZUL, label="n(n−1)/2 (fuerza bruta)")
    a.set_xlabel("n"); a.set_ylabel("operaciones")
    a.set_title("Costo: la rejilla crece linealmente,\nrompiendo Ω(n log n) fuera de los árboles")
    a.legend(frameon=False)
    b = ax[1]
    b.semilogx(ns_a, ops_prom / ns_a, "o-", color=VERDE, lw=2, label="operaciones / n (medido)")
    b.set_ylim(0, 16)
    b.set_xlabel("n"); b.set_ylabel("operaciones por elemento")
    b2 = b.twinx()
    b2.semilogx(ns_a, rec_prom, "d-", color=ROJO, label="reconstrucciones (medido)")
    b2.semilogx(ns_a, 2 * np.log(ns_a), "--", color=GRIS, label="cota 2 ln n")
    b2.set_ylabel("reconstrucciones"); b2.spines["right"].set_visible(True)
    b2.set_ylim(0, 32)
    h1, l1 = b.get_legend_handles_labels(); h2, l2 = b2.get_legend_handles_labels()
    b.legend(h1 + h2, l1 + l2, frameon=False, loc="upper left", fontsize=9)
    b.set_title("Costo por elemento ≈ constante;\nreconstrucciones ≤ 2 ln n (análisis hacia atrás)")
    fig.tight_layout()
    guardar(fig, "fig7_costos_experimentales.png")


if __name__ == "__main__":
    fig1_problema()
    fig2_reduccion()
    fig3_componentes()
    fig4_modelo()
    fig5_rejilla()
    fig6_gif()
    fig7_costos()
    print("Listo: 7 archivos en", CARPETA)