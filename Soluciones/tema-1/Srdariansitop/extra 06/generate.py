import argparse
import os

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, FancyBboxPatch, Patch
from matplotlib.animation import FuncAnimation, PillowWriter

OUT = os.path.dirname(os.path.abspath(__file__)) if "__file__" in locals() else "."
DPI = 130
GIF_DPI = 80
MAKE_GIFS = True

C = dict(cell="#f5f7fb", edge="#a9b4c6", cand="#cfe8ff", disc="#e3e3e3",
         cur="#ffd24d", found="#7ddc91", bad="#ff9a94", text="#1b2430",
         dim="#9aa0aa", muted="#6b7585", hi="#ffc48a", lo="#b9d4ff",
         path="#e8833a", x="#d62839", ok="#1f9d55", blue="#2b6cb0",
         ink="#34405a")

# Matriz de ejemplo (la misma del documento)
A4 = np.array([[1, 4, 7, 11],
               [2, 5, 8, 12],
               [3, 6, 9, 16],
               [10, 13, 14, 17]])


def make_matrix(n, rng=None, seed=7, maxinc=3):
    """Matriz n x n con filas y columnas no decrecientes (suma de prefijos)."""
    if rng is None:
        rng = np.random.default_rng(seed)
    r = rng.integers(0, maxinc + 1, size=(n, n))
    return r.cumsum(0).cumsum(1) + 1


def make_B(n):
    """B[i][j] = 2(i+j) con i,j en 1..n (matriz base del adversario)."""
    return np.fromfunction(lambda i, j: 2 * ((i + 1) + (j + 1)), (n, n), dtype=int)


def trace(A, x, buggy=False):
    """
    Ejecuta la escalera y devuelve (estados, operaciones).
    estados[k] = (i, j) (0-based) donde se hace la comparacion k.
    ops[k] in {"eq", "gt", "lt"}  (A[i][j] ==, >, < x).
    Si no se encuentra x, estados tiene un elemento mas (estado final).
    buggy=True intercambia los descartes (algoritmo INCORRECTO, para la sec. 3).
    """
    n = A.shape[0]
    i, j = 0, A.shape[1] - 1
    st, ops = [(i, j)], []
    while i < n and j >= 0:
        v = A[i, j]
        if v == x:
            ops.append("eq")
            break
        if v > x:
            ops.append("gt")
            if buggy:
                i += 1
            else:
                j -= 1
        else:
            ops.append("lt")
            if buggy:
                j -= 1
            else:
                i += 1
        st.append((i, j))
    return st, ops


def savefig(fig, name):
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, name)
    fig.savefig(p, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  ->", p)


def make_gif(name, nframes, draw, figsize, fps=1.0, hold=2):
    if not MAKE_GIFS:
        return
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name)
    fig = plt.figure(figsize=figsize, facecolor="white")

    def upd(f):
        fig.clf()
        draw(fig, min(f, nframes - 1))

    anim = FuncAnimation(fig, upd, frames=nframes + hold)
    anim.save(path, writer=PillowWriter(fps=fps), dpi=GIF_DPI)
    plt.close(fig)
    print("  ->", path)


def patches(items):
    return [Patch(facecolor=c, edgecolor=C["edge"], label=l) for c, l in items]


def draw_grid(ax, A, fill=None, dim=(), edge=None, show=True, fs=None,
              labels=True, texts=None, lw=1.2):
    """Dibuja la matriz A como una cuadricula de celdas coloreadas."""
    n, m = A.shape
    fill = fill or {}
    edge = edge or {}
    texts = texts or {}
    if fs is None:
        fs = min(17, 100 / max(n, m))
    ax.set_xlim(-1.0, m + 0.1)
    ax.set_ylim(n + 0.1, -1.0)
    ax.set_aspect("equal")
    ax.axis("off")
    for i in range(n):
        for j in range(m):
            ec, elw = edge.get((i, j), (C["edge"], lw))
            ax.add_patch(Rectangle((j, i), 1, 1,
                                   facecolor=fill.get((i, j), C["cell"]),
                                   edgecolor=ec, lw=elw,
                                   zorder=3 if (i, j) in edge else 2))
            s = texts.get((i, j), str(A[i, j]) if show else "")
            if s:
                ax.text(j + .5, i + .5, s, ha="center", va="center",
                        fontsize=fs, zorder=6,
                        color=C["dim"] if (i, j) in dim else C["text"])
    if labels:
        for j in range(m):
            ax.text(j + .5, -.28, str(j + 1), ha="center", va="center",
                    fontsize=fs * 0.7, color=C["muted"])
        for i in range(n):
            ax.text(-.28, i + .5, str(i + 1), ha="center", va="center",
                    fontsize=fs * 0.7, color=C["muted"])


def draw_state(fig, A, x, st, ops, k, title, show_inv=False, buggy=False):
    n, m = A.shape
    L = len(ops)
    i, j = st[k]
    final = k >= L
    xcells = [(p, q) for p in range(n) for q in range(m) if A[p, q] == x]
    inR = lambda p, q: (p >= i and q <= j)

    fill = {(p, q): (C["cand"] if inR(p, q) else C["disc"])
            for p in range(n) for q in range(m)}
    dim = {(p, q) for p in range(n) for q in range(m) if not inR(p, q)}
    edge = {c: (C["x"], 3.2) for c in xcells}
    if not final:
        fill[(i, j)] = C["found"] if ops[k] == "eq" else C["cur"]

    ax = fig.add_axes([0.05, 0.25, 0.9, 0.63])
    draw_grid(ax, A, fill=fill, dim=dim, edge=edge)

    pts = [(q + .5, p + .5) for (p, q) in st[:k + 1] if 0 <= p < n and 0 <= q < m]
    if len(pts) > 1:
        ax.plot(*zip(*pts), color=C["path"], lw=2.5, marker="o", ms=5, zorder=5)

    # Texto de la decision
    if final:
        cap = "R quedó vacía (i > n  ó  j < 1)  ⇒  respuesta: FALSO"
    else:
        v, op = A[i, j], ops[k]
        if op == "eq":
            cap = f"A[{i+1}][{j+1}] = {v} = x  ⇒  ¡encontrado!  VERDADERO"
        elif op == "gt":
            cap = (f"A[{i+1}][{j+1}] = {v} > x = {x}  ⇒  " +
                   (f"i ← i+1  (¡BUG: descarta la fila {i+1}!)" if buggy else
                    f"descartar columna {j+1}   (j ← j−1)"))
        else:
            cap = (f"A[{i+1}][{j+1}] = {v} < x = {x}  ⇒  " +
                   (f"j ← j−1  (¡BUG: descarta la columna {j+1}!)" if buggy else
                    f"descartar fila {i+1}   (i ← i+1)"))

    comps = L if final else k + 1
    size = 0 if (i >= n or j < 0) else (n - i) * (j + 1)
    phi = n - i + j + 1

    fig.text(0.5, 0.965, title, ha="center", fontsize=14, weight="bold",
             color=C["text"])
    fig.text(0.5, 0.925, cap, ha="center", fontsize=11.5,
             color=C["x"] if (buggy and not final and ops[k] != "eq") else C["blue"])
    fig.text(0.5, 0.185,
             f"comparaciones: {comps}     |R| = {size} celdas     φ = (n−i+1)+j = {phi}",
             ha="center", fontsize=11, color=C["text"])

    if show_inv:
        if not xcells:
            msg, col = "x ∉ A  ⇒  la implicación del invariante se cumple (vacuamente)", C["ok"]
        elif all(inR(p, q) for p, q in xcells):
            msg, col = "Invariante I(i,j):  x está en A  ⇒  x ∈ R(i,j)   ✓", C["ok"]
        else:
            msg, col = "✗ INVARIANTE VIOLADO: x está en A pero x ∉ R(i,j)", C["x"]
        fig.text(0.5, 0.14, msg, ha="center", fontsize=11.5, weight="bold", color=col)

    fig.legend(handles=patches([(C["cand"], "región candidata R"),
                                (C["disc"], "descartado"),
                                (C["cur"], "celda comparada"),
                                (C["found"], "encontrado")]) +
                              [Patch(facecolor="white", edgecolor=C["x"], lw=2.5,
                                     label="celdas con valor x")],
               loc="lower center", ncol=5, fontsize=8.5, frameon=False,
               bbox_to_anchor=(0.5, 0.0))


def search_gif(name, A, x, title, show_inv=False, buggy=False):
    st, ops = trace(A, x, buggy=buggy)
    make_gif(name, len(st),
             lambda fig, k: draw_state(fig, A, x, st, ops, k, title, show_inv, buggy),
             figsize=(7.2, 7.6), fps=1.0)


def s1_esquina():
    fig, axs = plt.subplots(1, 3, figsize=(16, 6))
    # (a) propiedad de la esquina
    fill = {(0, j): C["lo"] for j in range(3)}
    fill.update({(i, 3): C["hi"] for i in range(1, 4)})
    fill[(0, 3)] = C["cur"]
    draw_grid(axs[0], A4, fill=fill)
    axs[0].set_title("(a) La esquina superior derecha (1,n)\nmáx. de su fila  ·  mín. de su columna",
                     fontsize=12, weight="bold")
    axs[0].legend(handles=patches([(C["lo"], "≤ esquina (su fila)"),
                                   (C["hi"], "≥ esquina (su columna)")]),
                  loc="lower center", bbox_to_anchor=(0.5, -0.12), ncol=2, frameon=False)
    # (b) x = 6 -> 11 > 6
    fill = {(i, j): C["cand"] for i in range(4) for j in range(4)}
    fill.update({(i, 3): C["bad"] for i in range(4)})
    fill[(0, 3)] = C["cur"]
    draw_grid(axs[1], A4, fill=fill, edge={(2, 1): (C["x"], 3.2)})
    axs[1].set_title("(b) x = 6:   11 > 6\n⇒ toda la columna 4 es ≥ 11 > 6: se descarta",
                     fontsize=12, weight="bold")
    # (c) x = 15 -> 11 < 15
    fill = {(i, j): C["cand"] for i in range(4) for j in range(4)}
    fill.update({(0, j): C["bad"] for j in range(4)})
    fill[(0, 3)] = C["cur"]
    draw_grid(axs[2], A4, fill=fill)
    axs[2].set_title("(c) x = 15:   11 < 15\n⇒ toda la fila 1 es ≤ 11 < 15: se descarta",
                     fontsize=12, weight="bold")
    for a in axs[1:]:
        a.legend(handles=patches([(C["bad"], "descartado"), (C["cand"], "sigue candidato")]),
                 loc="lower center", bbox_to_anchor=(0.5, -0.12), ncol=2, frameon=False)
    fig.suptitle("Idea clave: una comparación elimina una fila o una columna entera",
                 fontsize=15, weight="bold", y=1.02)
    savefig(fig, "01_s1_idea_esquina.png")


def s2_flujo():
    fig, ax = plt.subplots(figsize=(12.5, 8.6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 9)
    ax.axis("off")

    def box(x, y, w, h, text, fc, fs=11.5):
        ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                    boxstyle="round,pad=0.02,rounding_size=0.15",
                                    fc=fc, ec=C["ink"], lw=1.6, zorder=3))
        ax.text(x, y, text, ha="center", va="center", fontsize=fs, zorder=4)

    def arrow(p, q, lab=None, lp=None):
        ax.annotate("", xy=q, xytext=p,
                    arrowprops=dict(arrowstyle="-|>", lw=1.9, color=C["ink"]), zorder=2)
        if lab:
            ax.text(*lp, lab, fontsize=11, weight="bold", color=C["blue"],
                    ha="center", va="center", zorder=5,
                    bbox=dict(fc="white", ec="none", pad=1))

    box(6, 8.2, 4, 0.9, "i ← 1 ;  j ← n", "#e8f0ff")
    ax.add_patch(Polygon([(6 - 2.4, 6.5), (6, 6.5 + .9), (6 + 2.4, 6.5), (6, 6.5 - .9)],
                         closed=True, fc="#fff4cc", ec=C["ink"], lw=1.6, zorder=3))
    ax.text(6, 6.5, "¿ i ≤ n  y  j ≥ 1 ?", ha="center", va="center", fontsize=12, zorder=4)
    box(6, 4.6, 4.6, 0.9, "comparar  x  con  A[i][j]", "#e8f0ff")
    box(10.4, 6.5, 2.8, 0.9, "devolver FALSO", "#ffd1cc")
    box(10.4, 4.6, 2.8, 0.9, "devolver VERDADERO", "#c9f2d3")
    box(3.4, 2.7, 4.3, 1.1, "A[i][j] > x\nj ← j − 1\n(descarta la columna j)", "#e0ecff")
    box(8.6, 2.7, 4.3, 1.1, "A[i][j] < x\ni ← i + 1\n(descarta la fila i)", "#e0ecff")

    arrow((6, 7.75), (6, 7.42))
    arrow((6, 5.6), (6, 5.07), "sí", (6.35, 5.35))
    arrow((8.4, 6.5), (9.0, 6.5), "no", (8.7, 6.8))
    arrow((8.3, 4.6), (9.0, 4.6), "=", (8.65, 4.9))
    arrow((5.0, 4.15), (3.6, 3.27), ">", (4.0, 3.85))
    arrow((7.0, 4.15), (8.4, 3.27), "<", (8.0, 3.85))
    # lazo de retorno
    ax.plot([3.4, 3.4], [2.15, 1.3], color=C["ink"], lw=1.9)
    ax.plot([8.6, 8.6], [2.15, 1.3], color=C["ink"], lw=1.9)
    ax.plot([8.6, 0.8], [1.3, 1.3], color=C["ink"], lw=1.9)
    ax.plot([0.8, 0.8], [1.3, 6.5], color=C["ink"], lw=1.9)
    arrow((0.8, 6.5), (3.6, 6.5))

    note = dict(fontsize=10.5, color=C["ok"], weight="bold")
    ax.text(0.1, 8.55, "INICIO", fontsize=10.5, color=C["ok"], weight="bold")
    ax.text(0.1, 8.15, "R(1,n) = toda la matriz\n⇒ I(1,n) se cumple", fontsize=10, color=C["ok"])
    ax.text(10.4, 5.98, "R(i,j) = ∅  ⇒  x ∉ A\n(invariante + guarda falsa)", ha="center",
            va="top", fontsize=10, color=C["ok"])
    ax.text(10.4, 4.08, "se comprobó A[i][j] = x\n⇒ x ∈ A", ha="center", va="top", fontsize=10, color=C["ok"])
    ax.text(0.95, 3.9, "CONSERVACIÓN\nI(i,j) ⇒ I(nuevo estado)\n(Lemas 1 y 2)", fontsize=10, **{
        k: v for k, v in note.items() if k != "fontsize"})
    ax.text(6, 0.55, "Potencial φ = (n − i + 1) + j :  baja exactamente 1 por iteración  ⇒  ≤ 2n − 1 iteraciones",
            ha="center", fontsize=11.5, color=C["blue"], weight="bold")
    ax.set_title("Diagrama del bucle y dónde actúa el invariante I(i,j)",
                 fontsize=14, weight="bold")
    savefig(fig, "03_s2_flujo_e_invariante.png")


def s3_region():
    A = make_matrix(6, seed=5)
    n = 6
    i, j = 2, 3
    fill = {(p, q): (C["cand"] if (p >= i and q <= j) else C["disc"])
            for p in range(n) for q in range(n)}
    fill[(i, j)] = C["cur"]
    dim = {c for c, v in fill.items() if v == C["disc"]}
    fig, ax = plt.subplots(figsize=(8.4, 7.4))
    draw_grid(ax, A, fill=fill, dim=dim)
    ax.text(2.0, 0.95, "filas < i\ndescartadas\n(Lema 2)", ha="center", va="center",
            fontsize=11, color=C["muted"], zorder=7)
    ax.text(5.0, 3.5, "columnas > j\ndescartadas\n(Lema 1)", ha="center", va="center",
            fontsize=11, color=C["muted"], zorder=7)
    ax.text(0.9, 5.45, "R(i,j)", fontsize=14, weight="bold", color=C["blue"], zorder=7)
    ax.set_title("Región candidata  R(i,j) = { (p,q) : i ≤ p ≤ n ,  1 ≤ q ≤ j }\n"
                 "Invariante I:  si x está en la matriz, está dentro de R(i,j)",
                 fontsize=13, weight="bold")
    ax.legend(handles=patches([(C["cur"], "esquina (i,j)"), (C["cand"], "R(i,j): sospechosos"),
                               (C["disc"], "absueltos: aquí no hay x")]),
              loc="lower center", bbox_to_anchor=(0.5, -0.1), ncol=3, frameon=False)
    savefig(fig, "04_s3_region_candidata.png")


def s4_incomparables():
    n = 6
    B = make_B(n)
    D = {(k, n - 1 - k) for k in range(n)}
    ci, cj = 2, 3
    fill = {}
    for p in range(n):
        for q in range(n):
            if p <= ci and q <= cj:
                fill[(p, q)] = C["lo"]
            elif p >= ci and q >= cj:
                fill[(p, q)] = C["hi"]
            else:
                fill[(p, q)] = C["disc"]
    for d in D:
        fill[d] = "#ffa94d"
    fill[(ci, cj)] = C["cur"]
    fig, ax = plt.subplots(figsize=(8.2, 7.4))
    draw_grid(ax, B, fill=fill, edge={d: ("#c0661a", 2.4) for d in D})
    ax.set_title("Las n celdas de la antidiagonal D son incomparables\n"
                 "(ninguna fuerza a otra a ser mayor o menor: Lema 0 no las relaciona)",
                 fontsize=12.5, weight="bold")
    ax.legend(handles=patches([(C["cur"], "una celda c ∈ D"),
                               ("#ffa94d", "resto de D  (NE y SO de c)"),
                               (C["lo"], "≤ c  (Lema 0)"),
                               (C["hi"], "≥ c  (Lema 0)"),
                               (C["disc"], "sin relación con c")]),
              loc="lower center", bbox_to_anchor=(0.5, -0.12), ncol=3, frameon=False)
    savefig(fig, "06_s4_antidiagonal_incomparable.png")


def s4_gif_dos_mundos():
    n = 6
    x = 2 * n + 1
    B = make_B(n)
    c = (2, 3)  # una celda de D que el algoritmo "se salta"
    M = B.copy()
    M[c] = x
    st, ops = trace(B, x)
    qs = [(p, q) for (p, q), o in zip(st[:len(ops)], ops) if (p, q) != c]
    sym = lambda v: ">" if v > x else ("<" if v < x else "=")
    nq = len(qs)

    def draw(fig, k):
        axs = [fig.add_axes([0.03, 0.22, 0.45, 0.6]), fig.add_axes([0.52, 0.22, 0.45, 0.6])]
        reveal = k >= nq + 1
        done = qs[:min(k + 1, nq)]
        for ax, MM, name in zip(axs, (B, M), ("Mundo 1: entrada B  (x ∉ B)", "Mundo 2: entrada M_c  (x ∈ M_c)")):
            fill = {d: C["lo"] for d in done}
            texts = {}
            if not reveal:
                texts[c] = "?"
                fill[c] = C["disc"]
            else:
                fill[c] = C["found"] if MM is M else C["hi"]
            if k < nq:
                fill[qs[k]] = C["cur"]
            draw_grid(ax, MM, fill=fill, texts=texts, fs=12,
                      edge={c: (C["x"], 3.0)} if reveal or True else None)
            ax.set_title(name, fontsize=11.5, weight="bold")
        fig.text(0.5, 0.965, "Si el algoritmo nunca consulta la celda c, no distingue B de M_c",
                 ha="center", fontsize=13.5, weight="bold")
        if k < nq:
            p, q = qs[k]
            fig.text(0.5, 0.915,
                     f"consulta ({p+1},{q+1}):  ambos mundos responden “{sym(B[p, q])}”  (mismo valor en B y M_c)",
                     ha="center", fontsize=11.5, color=C["blue"])
        elif k == nq:
            fig.text(0.5, 0.915, "Historia idéntica en ambos mundos ⇒ el algoritmo da la MISMA respuesta (FALSO)",
                     ha="center", fontsize=11.5, color=C["x"], weight="bold")
        else:
            fig.text(0.5, 0.915, f"Se revela c = ({c[0]+1},{c[1]+1}):  en B vale {B[c]},  en M_c vale {x} = x",
                     ha="center", fontsize=11.5, color=C["blue"], weight="bold")
            fig.text(0.5, 0.15, "Correcto en B: FALSO   ·   Correcto en M_c: VERDADERO   ⇒   se equivoca en uno   ⇒   contradicción",
                     ha="center", fontsize=11.5, color=C["x"], weight="bold")
        fig.text(0.5, 0.2 if k <= nq else 0.2, "", ha="center")
        fig.legend(handles=patches([(C["lo"], "celda consultada"), (C["cur"], "consulta actual"),
                                    (C["disc"], "c: nunca consultada ('?')")]),
                   loc="lower center", ncol=3, frameon=False, fontsize=9.5, bbox_to_anchor=(0.5, 0.0))

    make_gif("07_s4_dos_mundos.gif", nq + 2, draw, figsize=(13, 6.4), fps=1.2, hold=3)


def s1_gif_busqueda():
    search_gif("02_s1_busqueda_x6.gif", A4, 6, "Búsqueda de x = 6  (sí está)")


def s3_gif_invariante():
    A = make_matrix(8, seed=11)
    x = int(A[5, 2])
    search_gif("05_s3_invariante_en_accion.gif", A, x,
               f"El invariante en acción: x = {x} nunca sale de R", show_inv=True)


FIGURAS = [s1_esquina, s1_gif_busqueda, s2_flujo, s3_region,
           s3_gif_invariante, s4_incomparables, s4_gif_dos_mundos]


def main():
    global OUT, MAKE_GIFS
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else ".", help="carpeta de salida")
    ap.add_argument("--no-gif", action="store_true", help="no generar animaciones")
    a = ap.parse_args()
    OUT = a.out
    MAKE_GIFS = not a.no_gif
    for fn in FIGURAS:
        fn()
    print("Listo. Figuras en:", os.path.abspath(OUT))


if __name__ == "__main__":
    main()