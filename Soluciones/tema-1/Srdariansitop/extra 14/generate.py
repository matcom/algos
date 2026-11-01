import math
import os
import random
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter

CARPETA = os.path.dirname(os.path.abspath(__file__))
AZUL, NARANJA, VERDE, ROJO, GRIS = "#1f77b4", "#e07b00", "#2ca02c", "#d62728", "#b5b5b5"


def ruta(nombre):
    return os.path.join(CARPETA, nombre)


# --------------------------------------------------------------------------
# Nucleo: predicado de orientacion y los algoritmos de la seccion 3 y 4
# --------------------------------------------------------------------------
def orient(a, b, c):
    """o(a,b,c) > 0 si a->b->c gira a la izquierda; 0 colineales; < 0 derecha."""
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def ordenar(P, st):
    """Ordenamiento por mezcla lexicografico que cuenta pruebas de signo."""
    def menor(i, j):
        st["pruebas"] += 1
        if P[i][0] != P[j][0]:
            return P[i][0] < P[j][0]
        st["pruebas"] += 1
        return P[i][1] < P[j][1]

    def ms(a):
        if len(a) <= 1:
            return a
        m = len(a) // 2
        izq, der = ms(a[:m]), ms(a[m:])
        out, i, j = [], 0, 0
        while i < len(izq) and j < len(der):
            if menor(der[j], izq[i]):
                out.append(der[j]); j += 1
            else:
                out.append(izq[i]); i += 1
        return out + izq[i:] + der[j:]

    return ms(list(range(len(P))))


def andrew(P, st=None):
    """Cadena monotona. Devuelve (envolvente, cadena inferior, cadena superior)."""
    st = st if st is not None else {"pruebas": 0}
    n = len(P)
    idx = ordenar(P, st)
    if n == 1:
        return idx, idx, idx

    def cadena(orden):
        S = []
        for i in orden:
            while len(S) >= 2:
                st["pruebas"] += 1
                if orient(P[S[-2]], P[S[-1]], P[i]) <= 0:
                    S.pop()
                else:
                    break
            S.append(i)
        return S

    L, U = cadena(idx), cadena(idx[::-1])
    return L[:-1] + U[:-1], L, U


def jarvis(P):
    n = len(P)
    ini = min(range(n), key=lambda i: P[i])
    H, cur = [], ini
    while True:
        H.append(cur)
        cand = (cur + 1) % n
        for j in range(n):
            if orient(P[cur], P[cand], P[j]) < 0:
                cand = j
        cur = cand
        if cur == ini:
            return H


def fuerza_bruta(P):
    """(i,j) es arista si todos los demas quedan a la izquierda. Sin cortocircuito: n^3."""
    n = len(P)
    aristas = []
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            bien = 0
            for k in range(n):
                if k != i and k != j and orient(P[i], P[j], P[k]) > 0:
                    bien += 1
            if bien == n - 2:
                aristas.append((i, j))
    return aristas


def verificar():
    """Prueba contra el oraculo de fuerza bruta (como en la conferencia)."""
    rng = random.Random(2026)
    for _ in range(60):
        P = [(rng.random(), rng.random()) for _ in range(30)]
        a = set(andrew(P)[0])
        assert a == set(jarvis(P)) == {i for e in fuerza_bruta(P) for i in e}
    print("verificacion OK: Andrew = Jarvis = fuerza bruta en 60 instancias")


# --------------------------------------------------------------------------
# Figura 1: el problema y la respuesta
# --------------------------------------------------------------------------
def fig1():
    P = [(-2, 4), (0, 0), (10, 0), (12, 5), (8, 11), (2, 9),
         (5, 0),                                   # colineal sobre una arista: NO es vertice
         (4, 4), (6, 6), (8, 3), (3, 6), (5, 8), (9, 7), (7, 2)]
    H, L, U = andrew(P)
    assert len(H) == 6 and 6 not in H
    fig, ax = plt.subplots(1, 2, figsize=(11, 5))
    xs, ys = zip(*P)
    ax[0].scatter(xs, ys, c="#555", s=45)
    ax[0].set_title("Entrada: n puntos del plano")
    ax[1].scatter(xs, ys, c=GRIS, s=40, zorder=2)
    for cad, col, nom in ((L, AZUL, "cadena inferior L"), (U, NARANJA, "cadena superior U")):
        ax[1].plot([P[i][0] for i in cad], [P[i][1] for i in cad], color=col, lw=2.2,
                   label=nom, zorder=3)
    for orden, i in enumerate(H, 1):
        ax[1].scatter(*P[i], c=ROJO, s=90, zorder=4)
        ax[1].annotate(str(orden), P[i], textcoords="offset points", xytext=(7, 7),
                       fontweight="bold", color=ROJO)
    ax[1].annotate("colineal sobre la arista:\nno es vértice", P[6], xytext=(2.2, -3.3),
                   arrowprops=dict(arrowstyle="->"), fontsize=9)
    ax[1].set_title("Salida: vértices en orden antihorario (1 = menor lexicográfico)")
    ax[1].legend(loc="upper right", fontsize=8)
    for a in ax:
        a.set_aspect("equal"); a.set_xlim(-4, 14); a.set_ylim(-5, 15)
    fig.suptitle("Figura 1. Envolvente convexa con salida ordenada", fontweight="bold")
    fig.tight_layout()
    fig.savefig(ruta("fig1_problema.png"), dpi=130)
    plt.close(fig)


# --------------------------------------------------------------------------
# Figura 2: predicado de orientacion
# --------------------------------------------------------------------------
def fig2():
    a, b = (0, 0), (2, 0.5)
    casos = [("giro a la izquierda: o > 0", (4, 2)),
             ("colineales: o = 0", (4, 1)),
             ("giro a la derecha: o < 0", (4, -1))]
    fig, ax = plt.subplots(1, 3, figsize=(12, 4.6))
    for axi, (tit, c) in zip(ax, casos):
        v = orient(a, b, c)
        col = VERDE if v > 0 else (NARANJA if v == 0 else ROJO)
        axi.annotate("", b, a, arrowprops=dict(arrowstyle="->", lw=2, color=col))
        axi.annotate("", c, b, arrowprops=dict(arrowstyle="->", lw=2, color=col))
        for nombre, p in (("a", a), ("b", b), ("c", c)):
            axi.scatter(*p, c="k", zorder=3)
            axi.annotate(nombre, p, textcoords="offset points", xytext=(6, 6), fontsize=12)
        axi.set_title(f"{tit}\no(a,b,c) = {v:g}")
        axi.set_xlim(-0.5, 4.8); axi.set_ylim(-1.8, 2.8); axi.set_aspect("equal")
    fig.suptitle("Figura 2. El único predicado del algoritmo: o(a,b,c) = (bx−ax)(cy−ay) − (by−ay)(cx−ax)",
                 fontweight="bold", fontsize=10)
    fig.tight_layout(rect=[0, 0, 1, 0.9])
    fig.savefig(ruta("fig2_orientacion.png"), dpi=130)
    plt.close(fig)


# --------------------------------------------------------------------------
# Figura 3: GIF de la cadena monotona
# --------------------------------------------------------------------------
def traza_andrew(P):
    idx = sorted(range(len(P)), key=lambda i: P[i])
    frames, cadenas = [], {}
    for fase, orden in (("inferior", idx), ("superior", idx[::-1])):
        S = []
        frames.append(dict(fase=fase, S=[], cur=None, quitado=None,
                           msg=f"Cadena {fase}: se procesan los puntos en orden"))
        for i in orden:
            while len(S) >= 2:
                o = orient(P[S[-2]], P[S[-1]], P[i])
                if o <= 0:
                    q = S.pop()
                    frames.append(dict(fase=fase, S=list(S), cur=i, quitado=q,
                                       msg=f"o(s[-2], s[-1], p) = {o:.3f} ≤ 0  →  sacar de la pila"))
                else:
                    break
            S.append(i)
            frames.append(dict(fase=fase, S=list(S), cur=i, quitado=None,
                               msg=f"giro a la izquierda  →  meter p (pila de {len(S)})"))
        cadenas[fase] = list(S)
    L, U = cadenas["inferior"], cadenas["superior"]
    frames += [dict(fase="fin", S=L[:-1] + U[:-1], cur=None, quitado=None,
                    msg="Envolvente = L ++ U (sin repetir extremos)")] * 3
    return frames, cadenas


def fig3():
    rng = random.Random(11)
    P = [(rng.random(), rng.random()) for _ in range(14)]
    frames, cadenas = traza_andrew(P)
    xs, ys = zip(*P)
    fig, ax = plt.subplots(figsize=(6, 5.2))

    def dibujar(k):
        f = frames[k]
        ax.clear()
        ax.scatter(xs, ys, c=GRIS, s=45, zorder=2)
        if f["fase"] == "superior":
            Lc = cadenas["inferior"]
            ax.plot([P[i][0] for i in Lc], [P[i][1] for i in Lc], color=AZUL, lw=1.5, alpha=.5)
        if f["fase"] == "fin":
            H = f["S"] + [f["S"][0]]
            ax.fill([P[i][0] for i in H], [P[i][1] for i in H], color=VERDE, alpha=.15)
            ax.plot([P[i][0] for i in H], [P[i][1] for i in H], color=VERDE, lw=2.5)
            ax.scatter([P[i][0] for i in f["S"]], [P[i][1] for i in f["S"]], c=ROJO, s=70, zorder=4)
        else:
            col = AZUL if f["fase"] == "inferior" else NARANJA
            S = f["S"]
            ax.plot([P[i][0] for i in S], [P[i][1] for i in S], color=col, lw=2.5, zorder=3)
            ax.scatter([P[i][0] for i in S], [P[i][1] for i in S], c=col, s=70, zorder=4)
            if f["quitado"] is not None:
                ax.scatter(*P[f["quitado"]], marker="x", c=ROJO, s=170, lw=3, zorder=5)
            if f["cur"] is not None:
                ax.scatter(*P[f["cur"]], marker="*", c=VERDE, s=320, zorder=6)
        ax.set_title(f["msg"], fontsize=9)
        ax.set_xlim(-.05, 1.05); ax.set_ylim(-.05, 1.05); ax.set_aspect("equal")
        ax.set_xticks([]); ax.set_yticks([])

    ani = FuncAnimation(fig, dibujar, frames=len(frames), interval=700)
    ani.save(ruta("fig3_andrew.gif"), writer=PillowWriter(fps=1.6), dpi=90)
    plt.close(fig)


# --------------------------------------------------------------------------
# Figura 4: el invariante de la pila (Lema 2)
# --------------------------------------------------------------------------
def fig4():
    s = [(0, 2), (1, 0.8), (2, 0.5), (3, 0.6)]
    p = (4, -1)
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.4))
    # antes
    ax[0].plot(*zip(*s), color=AZUL, lw=2.5, marker="o")
    ax[0].scatter(*p, marker="*", c=VERDE, s=250, zorder=5)
    ax[0].plot([s[-1][0], p[0]], [s[-1][1], p[1]], ls="--", color=GRIS)
    ax[0].set_title("Antes: pila (s1..s4) convexa y llega p")
    # despues
    ax[1].plot(*zip(s[0], s[1], p), color=AZUL, lw=2.5, marker="o")
    xx = np.array([1, 4]); yy = s[1][1] + (p[1] - s[1][1]) / 3 * (xx - 1)
    ax[1].plot(xx, yy, ls="--", color=ROJO, label="recta s_r p")
    for q, nom, off in ((s[2], "s3", (6, 40)), (s[3], "s4", (14, 16))):
        ax[1].scatter(*q, marker="x", c=ROJO, s=150, lw=3)
        ax[1].annotate(nom + " sacado\n(encima de la recta)", q, textcoords="offset points", xytext=off,
                       fontsize=8, color=ROJO, ha="center")
    ax[1].scatter(*p, marker="*", c=VERDE, s=250, zorder=5)
    ax[1].set_title("Después: se sacó s4 y s3 hasta o(s1,s2,p) > 0")
    ax[1].legend(loc="lower left", fontsize=8)
    for i, (a, nom) in enumerate(zip(s, ["s1", "s2", "s3", "s4"])):
        ax[0].annotate(nom, a, textcoords="offset points", xytext=(6, 6))
    ax[0].annotate("p", p, textcoords="offset points", xytext=(6, 6))
    ax[1].annotate("s1", s[0], textcoords="offset points", xytext=(6, 6))
    ax[1].annotate("s2", s[1], textcoords="offset points", xytext=(6, 6))
    ax[1].annotate("p", p, textcoords="offset points", xytext=(6, 6))
    for a in ax:
        a.set_xlim(-.4, 4.6); a.set_ylim(-1.6, 2.8)
    fig.suptitle("Figura 4. Invariante (Lema 2): lo que se saca queda sobre o encima de la recta s_r–p, "
                 "y todo sigue por encima de la nueva cadena", fontweight="bold", fontsize=10)
    fig.tight_layout()
    fig.savefig(ruta("fig4_invariante.png"), dpi=130)
    plt.close(fig)


# --------------------------------------------------------------------------
# Figura 5: costo medido contra la cota de la seccion 4 y la cota minima
# --------------------------------------------------------------------------
def fig5():
    rng = np.random.default_rng(2026)
    ns = [2 ** k for k in range(4, 16)]
    medido, sup, inf = [], [], []
    for n in ns:
        P = [tuple(r) for r in rng.random((n, 2))]
        st = {"pruebas": 0}
        andrew(P, st)
        cota = 2 * n * math.ceil(math.log2(n)) + 4 * n
        assert st["pruebas"] <= cota
        norm = n * math.log2(n)
        medido.append(st["pruebas"] / norm)
        sup.append(cota / norm)
        inf.append(math.lgamma(n + 1) / math.log(3) / norm)
    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.plot(ns, sup, color=ROJO, marker="s", label="cota superior demostrada: 2n⌈log₂n⌉ + 4n")
    ax.plot(ns, medido, color=AZUL, marker="o", label="pruebas de signo medidas (Andrew)")
    ax.plot(ns, inf, color=VERDE, marker="^", label="cota mínima: log₃(n!)")
    ax.axhline(math.log(2) / math.log(3), color=VERDE, ls=":", lw=1,
               label="límite de la cota mínima: ln 2 / ln 3 ≈ 0,63")
    ax.set_xscale("log", base=2)
    ax.set_xlabel("n"); ax.set_ylabel("pruebas de signo / (n log₂ n)")
    ax.set_title("Figura 5. Entre las dos cotas, el cociente es acotado: Θ(n log n)", fontweight="bold",
                 fontsize=10)
    ax.legend(fontsize=8); ax.grid(alpha=.3)
    fig.tight_layout()
    fig.savefig(ruta("fig5_costo.png"), dpi=130)
    plt.close(fig)


# --------------------------------------------------------------------------
# Figura 6: tiempos de los tres algoritmos (puntos en un circulo: h = n)
# --------------------------------------------------------------------------
def circulo(n, rng):
    t = rng.uniform(0, 2 * math.pi, n)
    return [(math.cos(a), math.sin(a)) for a in t]


def medir(f, P):
    t0 = time.perf_counter()
    f(P)
    return time.perf_counter() - t0


def fig6():
    rng = np.random.default_rng(5)
    series = {
        "Fuerza bruta O(n³)": (fuerza_bruta, [10, 20, 40, 80, 120]),
        "Jarvis O(nh), aquí h = n": (jarvis, [100, 200, 400, 800, 1600]),
        "Cadena monótona Θ(n log n)": (lambda P: andrew(P), [100, 400, 1600, 6400, 25600]),
    }
    colores = [ROJO, NARANJA, AZUL]
    fig, ax = plt.subplots(figsize=(8, 5))
    for (nom, (f, ns)), col in zip(series.items(), colores):
        ts = [medir(f, circulo(n, rng)) for n in ns]
        pend = np.polyfit(np.log(ns), np.log(ts), 1)[0]
        ax.loglog(ns, ts, marker="o", color=col, label=f"{nom}  (pendiente ≈ {pend:.2f})")
    ax.set_xlabel("n"); ax.set_ylabel("segundos")
    ax.set_title("Figura 6. Misma entrada (n puntos en convexo), tres algoritmos", fontweight="bold",
                 fontsize=10)
    ax.legend(fontsize=8); ax.grid(alpha=.3, which="both")
    fig.tight_layout()
    fig.savefig(ruta("fig6_tiempos.png"), dpi=130)
    plt.close(fig)


# --------------------------------------------------------------------------
# Figura 7: la cota minima (reduccion desde ordenamiento + conteo de hojas)
# --------------------------------------------------------------------------
def fig7():
    sigma = [3, 6, 1, 7, 4, 2, 5]
    n = len(sigma)
    salida = [int(j) + 1 for j in np.argsort(sigma)]
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.8))
    t = np.linspace(0.5, n + .5, 100)
    ax[0].plot(t, t ** 2, color=GRIS, lw=1)
    P = [(s, s * s) for s in sigma]
    for j, (x, y) in enumerate(P, 1):
        ax[0].scatter(x, y, c=ROJO, s=70, zorder=3)
        ax[0].annotate(f"p{j}", (x, y), textcoords="offset points", xytext=(-14, 6), fontsize=10)
    H = [P[j - 1] for j in salida] + [P[salida[0] - 1]]
    ax[0].plot(*zip(*H), color=AZUL, lw=2)
    ax[0].set_title(f"p_j = (σ(j), σ(j)²),  σ = {sigma}\n"
                    f"salida = {salida}  →  determina σ", fontsize=9)
    ax[0].set_xlabel("x = σ(j)"); ax[0].set_ylabel("y = σ(j)²")
    ns = list(range(1, 13))
    h = [math.ceil(math.log(math.factorial(m), 3)) if m > 1 else 0 for m in ns]
    ax[1].bar(ns, h, color=VERDE, alpha=.7, label="profundidad mínima ⌈log₃ n!⌉")
    ax[1].plot(ns, [max(0, m * math.log(m, 3) - m * math.log(math.e, 3)) for m in ns], color=ROJO,
               marker="o", label="n log₃ n − n log₃ e")
    ax[1].set_xlabel("n"); ax[1].set_ylabel("pruebas de signo en el peor caso")
    ax[1].set_title("n! hojas distintas y cada nodo ramifica ≤ 3 → 3^h ≥ n!", fontsize=9)
    ax[1].legend(fontsize=8); ax[1].grid(alpha=.3)
    fig.suptitle("Figura 7. Cota mínima Ω(n log n): ordenar se reduce a la envolvente convexa",
                 fontweight="bold", fontsize=10)
    fig.tight_layout()
    fig.savefig(ruta("fig7_cota_minima.png"), dpi=130)
    plt.close(fig)


if __name__ == "__main__":
    verificar()
    for f in (fig1, fig2, fig3, fig4, fig5, fig6, fig7):
        f()
        print("generada:", f.__name__)
    print("Listo. Archivos en:", CARPETA)