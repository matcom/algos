import os
from itertools import combinations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Rectangle

CARPETA = os.path.dirname(os.path.abspath(__file__))

AZUL, VERDE, ROJO = "#1f77b4", "#2ca02c", "#d62728"
NARANJA, GRIS, AMARILLO = "#ff7f0e", "#9a9a9a", "#ffe58a"


def ruta(nombre):
    return os.path.join(CARPETA, nombre)


# ----------------------------------------------------------------------------
# Algoritmos
# ----------------------------------------------------------------------------
def mezcla_original(I, D):
    """Mezcla de la conferencia. Devuelve (salida, comparaciones)."""
    R, i, j, c = [], 0, 0, 0
    while i < len(I) and j < len(D):
        c += 1
        if I[i] <= D[j]:
            R.append(I[i]); i += 1
        else:
            R.append(D[j]); j += 1
    return R + I[i:] + D[j:], c


def mezcla_optimizada(I, D):
    """Se detiene cuando a I le queda 1 elemento y lo pone al final.
    Devuelve (salida, comparaciones como pares de indices, traza)."""
    R, i, j, comps = [], 0, 0, []
    traza = [(0, 0, [], None)]
    while i < len(I) - 1 and j < len(D):
        comps.append((i, j))
        ci, cj = i, j
        if I[i] <= D[j]:
            R.append(I[i]); i += 1
        else:
            R.append(D[j]); j += 1
        traza.append((i, j, list(R), (ci, cj)))
    salida = R + D[j:] + I[i:]
    return salida, comps, traza


# ----------------------------------------------------------------------------
# Entradas (valores 1..2n)
# ----------------------------------------------------------------------------
def intercalada(n):
    """Entrada del adversario: a_k = 2k-1, b_k = 2k."""
    return list(range(1, 2 * n, 2)), list(range(2, 2 * n + 1, 2))


def gemela(n):
    """Intercambia los valores de a_n y b_n en la intercalada."""
    A, B = intercalada(n)
    A[-1], B[-1] = B[-1], A[-1]
    return A, B


def peor_caso(n):
    """a_1..a_{n-2} < b_1..b_n < a_{n-1} < a_n  (n >= 2).
    Alcanza 2n-2 comparaciones y la salida es CORRECTA: el ciclo termina
    porque B se agota (j = n), con i = n-2."""
    A = list(range(1, n - 1)) + [2 * n - 1, 2 * n]
    B = list(range(n - 1, 2 * n - 1))
    return A, B


def nombres(A, B):
    d = {v: f"a{k + 1}" for k, v in enumerate(A)}
    d.update({v: f"b{k + 1}" for k, v in enumerate(B)})
    return d


# ----------------------------------------------------------------------------
# Calculos exhaustivos
# ----------------------------------------------------------------------------
def todas_las_entradas(n):
    """Todas las formas de repartir 1..2n entre dos listas ordenadas."""
    universo = range(1, 2 * n + 1)
    for pos in combinations(universo, n):
        A = list(pos)
        B = [v for v in universo if v not in pos]
        yield A, B


def peor_caso_medido(n):
    return max(len(mezcla_optimizada(A, B)[1]) for A, B in todas_las_entradas(n))


def fraccion_de_fallos(n):
    malas = total = 0
    for A, B in todas_las_entradas(n):
        total += 1
        if mezcla_optimizada(A, B)[0] != sorted(A + B):
            malas += 1
    return malas, total


# ----------------------------------------------------------------------------
# Dibujo de la cadena de comparaciones (usado en fig2, fig3 y fig4)
# ----------------------------------------------------------------------------
def dibujar_cadena(ax, A, B, comps, titulo, marcar_no_comparados=False,
                   destacar=(), pie=None, pie_color="black"):
    todos = sorted(A + B)
    x = {v: t for t, v in enumerate(todos)}
    nom = nombres(A, B)
    hechos = {frozenset((A[i], B[j])) for i, j in comps}

    if marcar_no_comparados:
        for u, v in zip(todos, todos[1:]):
            if (u in A) != (v in A) and frozenset((u, v)) not in hechos:
                ya, yb = (1, 0) if u in A else (0, 1)
                ax.plot([x[u], x[v]], [ya, yb], color=ROJO, lw=2.4,
                        ls=(0, (4, 3)), zorder=1)

    for m, (i, j) in enumerate(comps, 1):
        xa, xb = x[A[i]], x[B[j]]
        ax.plot([xa, xb], [1, 0], color=VERDE, lw=2.2, zorder=2)
        ax.text((xa + xb) / 2, 0.5, str(m), ha="center", va="center",
                fontsize=8, color="white", zorder=3,
                bbox=dict(boxstyle="circle,pad=0.2", fc=VERDE, ec="none"))

    for v in todos:
        es_a = v in A
        y = 1 if es_a else 0
        ec = NARANJA if v in destacar else "#333333"
        lw = 2.8 if v in destacar else 1.2
        ax.text(x[v], y, nom[v], ha="center", va="center", fontsize=10,
                zorder=4, bbox=dict(boxstyle="circle,pad=0.35", fc="#eef3fb",
                                    ec=ec, lw=lw))
        ax.text(x[v], y + (0.3 if es_a else -0.3), str(v), ha="center",
                va="center", fontsize=8, color="#555555")

    ax.text(-1.1, 1, "lista A", ha="right", va="center", fontsize=10)
    ax.text(-1.1, 0, "lista B", ha="right", va="center", fontsize=10)
    if pie:
        ax.text((len(todos) - 1) / 2, -0.78, pie, ha="center", va="center",
                fontsize=10, color=pie_color, fontweight="bold")
    ax.set_xlim(-2.2, len(todos) - 0.2)
    ax.set_ylim(-1.05, 1.6)
    ax.axis("off")
    ax.set_title(titulo, fontsize=11)


def leyenda_cadena(fig, con_rojo=True, con_naranja=False):
    from matplotlib.lines import Line2D
    h = [Line2D([0], [0], color=VERDE, lw=2.2, label="comparación que hizo el algoritmo")]
    if con_rojo:
        h.append(Line2D([0], [0], color=ROJO, lw=2.4, ls=(0, (4, 3)),
                        label="par de vecinos SIN comparar"))
    if con_naranja:
        h.append(Line2D([0], [0], color=NARANJA, lw=2.8,
                        label="valores intercambiados (a_n y b_n)"))
    fig.legend(handles=h, loc="lower center", ncol=len(h), frameon=False,
               fontsize=9)


# ----------------------------------------------------------------------------
# Figuras estaticas
# ----------------------------------------------------------------------------
def figura1():
    ns = list(range(1, 9))
    medido = [peor_caso_medido(n) for n in ns]
    formula = [2 * n - 2 for n in ns]
    original = [2 * n - 1 for n in ns]
    assert medido == formula, "el peor caso medido debe ser 2n-2"

    fig, ax = plt.subplots(figsize=(9, 5))
    w = 0.38
    ax.bar([n - w / 2 for n in ns], original, w, color=GRIS,
           label="mezcla original: 2n − 1 (cota mínima)")
    ax.bar([n + w / 2 for n in ns], medido, w, color=AZUL,
           label="mezcla optimizada: peor caso medido")
    ax.plot(ns, formula, "o--", color=ROJO, label="fórmula 2n − 2")
    for n, o, m in zip(ns, original, medido):
        ax.text(n - w / 2, o + 0.25, str(o), ha="center", fontsize=8)
        ax.text(n + w / 2, m + 0.25, str(m), ha="center", fontsize=8, color=AZUL)
    ax.set_xticks(ns)
    ax.set_xlabel("n (largo de cada lista)")
    ax.set_ylabel("comparaciones en el peor caso")
    ax.set_title("Peor caso medido recorriendo TODAS las C(2n, n) entradas\n"
                 "La optimizada hace 2n − 2 < 2n − 1: viola la cota de la sección 6")
    ax.legend(loc="upper left")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(ruta("fig1_peor_caso_comparaciones.png"), dpi=150)
    plt.close(fig)


def figura2(n=5):
    A, B = peor_caso(n)
    salida, comps, _ = mezcla_optimizada(A, B)
    assert len(comps) == 2 * n - 2
    fig, ax = plt.subplots(figsize=(11, 4.2))
    dibujar_cadena(
        ax, A, B, comps,
        f"Entrada del peor caso (n = {n}):  a₁..a₍ₙ₋₂₎ < b₁ < … < bₙ < a₍ₙ₋₁₎ < aₙ\n"
        f"El algoritmo hace {len(comps)} = 2n − 2 comparaciones (números sobre las líneas)",
        pie=f"salida correcta: {salida == sorted(A + B)}")
    leyenda_cadena(fig, con_rojo=False)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(ruta("fig2_entrada_peor_caso.png"), dpi=150)
    plt.close(fig)


def figura3(n=5):
    A, B = intercalada(n)
    _, comps, _ = mezcla_optimizada(A, B)
    assert len(comps) == 2 * n - 3
    fig, ax = plt.subplots(figsize=(11, 4.2))
    dibujar_cadena(
        ax, A, B, comps,
        f"Entrada del adversario (intercalada perfecta, n = {n}): "
        f"{len(comps)} = 2n − 3 comparaciones\n"
        f"De los 2n − 1 = {2 * n - 1} pares de vecinos quedan 2 sin comparar",
        marcar_no_comparados=True, destacar={A[-1], B[-1]})
    leyenda_cadena(fig, con_rojo=True, con_naranja=False)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(ruta("fig3_cadena_del_adversario.png"), dpi=150)
    plt.close(fig)


def figura4(n=5):
    fig, axes = plt.subplots(2, 1, figsize=(11, 8.2))
    casos = [("X (entrada del adversario)", intercalada(n)),
             ("X' (gemela: se intercambian los valores de aₙ y bₙ)", gemela(n))]
    todos_comps = []
    for ax, (titulo, (A, B)) in zip(axes, casos):
        salida, comps, _ = mezcla_optimizada(A, B)
        todos_comps.append(comps)
        nom = nombres(A, B)
        ok = salida == sorted(A + B)
        texto = " ".join(nom[v] for v in salida)
        dibujar_cadena(
            ax, A, B, comps, titulo, destacar={A[-1], B[-1]},
            pie=f"salida: {texto}   →   {'CORRECTA' if ok else 'INCORRECTA'}",
            pie_color=VERDE if ok else ROJO)
    assert todos_comps[0] == todos_comps[1], "mismas comparaciones en X y X'"
    fig.suptitle("Las mismas comparaciones reciben las mismas respuestas en X y en X':\n"
                 "el algoritmo da la MISMA salida (en posiciones) y no puede acertar las dos",
                 fontsize=12)
    leyenda_cadena(fig, con_rojo=False, con_naranja=True)
    fig.tight_layout(rect=(0, 0.04, 1, 0.94))
    fig.savefig(ruta("fig4_entrada_gemela.png"), dpi=150)
    plt.close(fig)


def figura5():
    ns = list(range(1, 9))
    datos = [fraccion_de_fallos(n) for n in ns]
    pct = [100 * m / t for m, t in datos]
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(ns, pct, color=ROJO, alpha=0.85)
    for n, p, (m, t) in zip(ns, pct, datos):
        ax.text(n, p + 1, f"{m}/{t}", ha="center", fontsize=8)
    ax.set_xticks(ns)
    ax.set_ylim(0, 105)
    ax.set_xlabel("n (largo de cada lista)")
    ax.set_ylabel("% de entradas donde la salida es incorrecta")
    ax.set_title("Fallos de la mezcla optimizada recorriendo TODAS las entradas\n"
                 "(etiqueta: entradas que fallan / entradas totales)")
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(ruta("fig5_fraccion_de_fallos.png"), dpi=150)
    plt.close(fig)


# ----------------------------------------------------------------------------
# GIFs
# ----------------------------------------------------------------------------
def dibujar_estado(ax, A, B, i, j, R, cmp_, msg, final=None, correcta=None):
    ax.clear()
    n = len(A)
    yA, yB, yR = 2.2, 1.2, -0.2

    def caja(x, y, txt, fc, ec="#333333", ls="-"):
        ax.add_patch(Rectangle((x - 0.4, y - 0.4), 0.8, 0.8, fc=fc, ec=ec,
                               lw=1.3, ls=ls, zorder=2))
        if txt is not None:
            ax.text(x, y, str(txt), ha="center", va="center", fontsize=11,
                    zorder=3)

    for k, v in enumerate(A):
        fc = "#dddddd" if k < i else "#eef3fb"
        if cmp_ and k == cmp_[0]:
            fc = AMARILLO
        caja(k, yA, v, fc)
    for k, v in enumerate(B):
        fc = "#dddddd" if k < j else "#eef3fb"
        if cmp_ and k == cmp_[1]:
            fc = AMARILLO
        caja(k, yB, v, fc)

    if final is None:
        ax.text(i, yA + 0.75, "▼ i", ha="center", color=AZUL, fontsize=10)
        if j < len(B):
            ax.text(j, yB - 0.75, "▲ j", ha="center", color=ROJO, fontsize=10)
        elif j == len(B):
            ax.text(len(B) - 0.4, yB - 0.75, "j = n", ha="center", color=ROJO, fontsize=10)

    for t in range(2 * n):
        if final is not None:
            if t < len(final):
                bien = final[t] == correcta[t]
                caja(t, yR, final[t], "#c8efc8" if bien else "#f6c0c0")
            else:
                caja(t, yR, None, "white", ls="--")
        elif t < len(R):
            caja(t, yR, R[t], "#cfe4f7")
        else:
            caja(t, yR, None, "white", ec="#aaaaaa", ls="--")

    ax.text(-0.8, yA, "A", ha="right", va="center", fontsize=12, fontweight="bold")
    ax.text(-0.8, yB, "B", ha="right", va="center", fontsize=12, fontweight="bold")
    ax.text(-0.8, yR, "salida", ha="right", va="center", fontsize=10)
    ax.text((2 * n - 1) / 2, 3.55, msg, ha="center", va="center", fontsize=11,
            fontweight="bold")
    ax.set_xlim(-2.2, 2 * n - 0.4)
    ax.set_ylim(-1.0, 4.0)
    ax.set_aspect("equal")
    ax.axis("off")


def hacer_gif(A, B, archivo, titulo):
    salida, comps, traza = mezcla_optimizada(A, B)
    correcta = sorted(A + B)
    n = len(A)
    estados = []
    for m, (i, j, R, c) in enumerate(traza):
        if c is None:
            estados.append((i, j, R, None, "Inicio: i = 0, j = 0", None))
        else:
            x, y = A[c[0]], B[c[1]]
            estados.append((i, j, R, c,
                            f"Comparación {m}: {x} vs {y}  →  sale {min(x, y)}", None))
    i, j, R, _ = traza[-1]
    motivo = (f"i = n − 1: a_n queda solo, se deja de comparar ({len(comps)} comparaciones)"
              if i == n - 1 else
              f"B se agotó (j = n): {len(comps)} comparaciones")
    estados.append((i, j, R, None, motivo, None))
    ok = salida == correcta
    veredicto = "salida CORRECTA" if ok else "salida INCORRECTA (el orden real termina distinto)"
    estados.append((i, j, R, None, f"Se agrega D[j:] + I[i:]  →  {veredicto}", salida))
    estados.append(estados[-1])

    fig, ax = plt.subplots(figsize=(10, 4.6))
    fig.suptitle(titulo, fontsize=12)

    def actualizar(k):
        i, j, R, c, msg, fin = estados[k]
        dibujar_estado(ax, A, B, i, j, R, c, msg, final=fin, correcta=correcta)
        return []

    anim = FuncAnimation(fig, actualizar, frames=len(estados), blit=False)
    anim.save(ruta(archivo), writer=PillowWriter(fps=0.9))
    plt.close(fig)


# ----------------------------------------------------------------------------
if __name__ == "__main__":
    figura1()
    figura2()
    figura3()
    figura4()
    figura5()
    A, B = intercalada(4)
    hacer_gif(A, B, "anim1_adversario_falla.gif",
              "Mezcla optimizada sobre la entrada del adversario (n = 4)")
    A, B = peor_caso(4)
    hacer_gif(A, B, "anim2_peor_caso_correcto.gif",
              "Mezcla optimizada sobre una entrada de 2n − 2 comparaciones (n = 4)")
    print("Figuras generadas en:", CARPETA)