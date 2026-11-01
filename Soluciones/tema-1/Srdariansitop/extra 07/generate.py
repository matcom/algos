#!/usr/bin/env python3
"""
Genera 7 figuras (4 PNG + 3 GIF) que ilustran las 3 secciones del problema
"Mediana de dos arreglos ordenados de largo n  (O(log n))".

  Sección 1 (algoritmo)       : s1_corte.png, s1_busqueda.gif, s1_monotonia.png
  Sección 2 (correctitud)     : s2_cuatro_casos.png, s2_invariante.gif
  Sección 3 (cota información): s3_arbol_decision.png, s3_cota_informacion.gif

Requisitos:  pip install matplotlib pillow
Uso:         python generar_visuales.py        ->  guarda los 7 archivos en la carpeta actual
"""
import math
import os
import random

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Rectangle, FancyArrowPatch, Circle, FancyBboxPatch

OUT = os.getcwd()   # las imágenes se guardan en la carpeta desde donde ejecutas el script

# ------------------------------------------------------------------ estilo
BLUE, LBLUE = "#2F6FDE", "#DCE8FB"
ORANGE, LORANGE = "#F28C28", "#FDE9D2"
GREEN, LGREEN = "#2E9E5B", "#D5F0E0"
RED, LRED = "#D64545", "#F9D9D9"
GOLD, YELLOW = "#C99700", "#FFE680"
GRAY, DARK = "#B8BEC6", "#1F2937"
DPI = 90
plt.rcParams["font.family"] = "DejaVu Sans"


# ------------------------------------------------------------------ lógica
def trace(A, B):
    """Ejecuta el algoritmo y devuelve (pasos, i*). A y B son listas 0-indexadas."""
    n = len(A)
    lo, hi = 0, n
    pasos = []
    while lo < hi:
        i = (lo + hi) // 2
        cond = A[i] > B[n - i - 1]          # g(i):  A[i+1] > B[n-i]  (1-indexado)
        nlo, nhi = (lo, i) if cond else (i + 1, hi)
        pasos.append(dict(lo=lo, hi=hi, i=i, cond=cond, nlo=nlo, nhi=nhi))
        lo, hi = nlo, nhi
    return pasos, lo


def g_values(A, B):
    n = len(A)
    return [A[i] > B[n - i - 1] for i in range(n)] + [True]   # g(n) = verdadero


# ------------------------------------------------------------------ dibujo
def row(ax, arr, y, cut, name, rings=(), ring_col=GOLD, h=0.8, fs=13):
    """Dibuja un arreglo: prefijo (<=cut) azul, sufijo naranja, y la línea de corte."""
    ax.text(-0.3, y + h / 2, name, ha="right", va="center",
            fontsize=16, fontweight="bold", color=DARK)
    for k, v in enumerate(arr, start=1):
        ax.add_patch(Rectangle((k - 1, y), 1, h,
                               facecolor=LBLUE if k <= cut else LORANGE,
                               edgecolor=DARK, lw=1.2))
        ax.text(k - 0.5, y + h / 2, str(v), ha="center", va="center", fontsize=fs, color=DARK)
        ax.text(k - 0.5, y - 0.12, str(k), ha="center", va="top", fontsize=8, color="#6B7280")
    for k in rings:
        ax.add_patch(Rectangle((k - 1, y), 1, h, fill=False, edgecolor=ring_col, lw=3.8))
    ax.plot([cut, cut], [y - 0.12, y + h + 0.12], color=DARK, lw=3.4, solid_capstyle="round")


def strip(ax, n, lo, hi, y, i=None, istar=None):
    """Franja con los candidatos {0..n} para i; los vivos están en amarillo."""
    ax.text(-0.9, y + 0.3, "candidatos\npara i", ha="right", va="center", fontsize=10, color=DARK)
    for t in range(n + 1):
        vivo = lo <= t <= hi
        ax.add_patch(Rectangle((t - 0.4, y), 0.8, 0.6,
                               facecolor=YELLOW if vivo else "#E5E7EB",
                               edgecolor=DARK if vivo else GRAY, lw=1.2))
        ax.text(t, y + 0.3, str(t), ha="center", va="center", fontsize=11,
                color=DARK if vivo else "#9CA3AF")
    if i is not None:
        ax.add_patch(Rectangle((i - 0.4, y), 0.8, 0.6, fill=False, edgecolor=RED, lw=3.6))
        ax.text(i, y + 0.72, "i", ha="center", va="bottom", color=RED, fontsize=13, fontweight="bold")
    if istar is not None:
        ax.text(istar, y - 0.1, "★ i*", ha="center", va="top", color=GREEN, fontsize=12, fontweight="bold")


def save_gif(fig, update, n_frames, name, interval_ms=1300):
    anim = FuncAnimation(fig, update, frames=n_frames, interval=interval_ms)
    anim.save(os.path.join(OUT, name), writer=PillowWriter(fps=1000 / interval_ms), dpi=DPI)
    plt.close(fig)
    print("OK", name)


def save_png(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=130, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("OK", name)


# =========================================================================
# SECCIÓN 1 -- Figura 1: la mediana es un "corte"
# =========================================================================
def s1_corte():
    A, B = [1, 2, 3, 4, 10, 12], [5, 6, 7, 8, 9, 11]
    n = len(A)
    i = 4
    j = n - i
    fig, ax = plt.subplots(figsize=(11, 6.4))
    ax.set_xlim(-1.4, n + 0.8)
    ax.set_ylim(-1.9, 6.0)
    ax.axis("off")
    ax.set_title("La mediana es un CORTE: L = prefijo de A  +  prefijo de B",
                 fontsize=16, fontweight="bold", color=DARK, pad=10)

    row(ax, A, 4.3, i, "A", rings=[i], ring_col=GOLD)
    row(ax, B, 2.5, j, "B", rings=[j], ring_col=GOLD)
    ax.text(i, 5.3, f"i = {i}", ha="center", color=BLUE, fontsize=13, fontweight="bold")
    ax.text(j, 3.5, f"j = n − i = {j}", ha="center", color=BLUE, fontsize=13, fontweight="bold")
    ax.text(n / 2, 1.85, "Total en L:  i + j = n   (los n menores de los 2n)",
            ha="center", fontsize=12, color=DARK)

    # arreglo mezclado
    M = sorted(A + B)
    w = n / (2 * n)
    ax.text(-0.3, 0.6, "Mezcla", ha="right", va="center", fontsize=14, fontweight="bold", color=DARK)
    for k, v in enumerate(M):
        ax.add_patch(Rectangle((k * w, 0.2), w, 0.8,
                               facecolor=LBLUE if k < n else LORANGE, edgecolor=DARK, lw=1.0))
        ax.text(k * w + w / 2, 0.6, str(v), ha="center", va="center", fontsize=10.5, color=DARK)
    ax.add_patch(Rectangle(((n - 1) * w, 0.2), w, 0.8, fill=False, edgecolor=GOLD, lw=3.8))
    ax.annotate("mediana = n-ésimo menor\n= max(A[i], B[j]) = %d" % max(A[i - 1], B[j - 1]),
                xy=((n - 1) * w + w / 2, 0.2), xytext=((n - 1) * w + w / 2, -1.2),
                ha="center", fontsize=12, color=GOLD, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=GOLD, lw=2))
    ax.text(n * w / 2 / 2 * 1.0, 1.1, "L  (azul)", ha="center", color=BLUE, fontsize=11, fontweight="bold")
    ax.text(n * w * 0.75 + 0.0, 1.1, "R  (naranja)", ha="center", color=ORANGE, fontsize=11, fontweight="bold")
    save_png(fig, "s1_corte.png")


# =========================================================================
# SECCIÓN 1 -- GIF 1: búsqueda binaria sobre el corte i
# =========================================================================
def s1_busqueda():
    A = [2, 5, 8, 11, 14, 17, 20, 23]
    B = [1, 3, 6, 9, 12, 15, 18, 21]
    n = len(A)
    pasos, istar = trace(A, B)
    frames = []
    for s, p in enumerate(pasos, start=1):
        frames.append(("probe", s, p))
        frames.append(("decide", s, p))
    frames += [("final", 0, None)] * 3

    fig, ax = plt.subplots(figsize=(11, 6.4))

    def update(k):
        ax.clear()
        ax.set_xlim(-1.6, n + 0.8)
        ax.set_ylim(-0.9, 6.9)
        ax.axis("off")
        ax.set_title("Búsqueda binaria sobre el corte i   (A y B con n = 8)",
                     fontsize=15, fontweight="bold", color=DARK)
        kind, s, p = frames[k]
        if kind == "final":
            i = istar
            strip(ax, n, istar, istar, 5.4, istar=istar)
            row(ax, A, 3.4, i, "A", rings=[i], ring_col=GOLD)
            row(ax, B, 1.7, n - i, "B", rings=[n - i], ring_col=GOLD)
            med = max(A[i - 1], B[n - i - 1])
            ax.text(n / 2, 0.55, f"lo = hi = i* = {i}   ⇒   mediana = max(A[{i}], B[{n - i}]) "
                                 f"= max({A[i - 1]}, {B[n - i - 1]}) = {med}",
                    ha="center", fontsize=13, color=GREEN, fontweight="bold")
            ax.text(n / 2, -0.25, "Total: 3 comparaciones  ≈  ⌈log₂(n+1)⌉",
                    ha="center", fontsize=12, color=DARK)
            return
        i = p["i"]
        lo, hi = (p["lo"], p["hi"]) if kind == "probe" else (p["nlo"], p["nhi"])
        strip(ax, n, lo, hi, 5.4, i=i if kind == "probe" else None)
        row(ax, A, 3.4, i, "A", rings=[i + 1], ring_col=GOLD)
        row(ax, B, 1.7, n - i, "B", rings=[n - i], ring_col=GOLD)
        ax.text(i, 4.4, f"i = {i}", ha="center", color=BLUE, fontsize=12, fontweight="bold")
        ax.text(n - i, 2.7, f"j = n − i = {n - i}", ha="center", color=BLUE, fontsize=12, fontweight="bold")
        if kind == "probe":
            ax.text(n / 2, 0.75,
                    f"Paso {s}:  lo = {p['lo']},  hi = {p['hi']}   →   i = ⌊({p['lo']}+{p['hi']})/2⌋ = {i}",
                    ha="center", fontsize=13, color=DARK, fontweight="bold")
            ax.text(n / 2, 0.05, f"Probamos el corte i = {i}: comparamos los dos elementos resaltados",
                    ha="center", fontsize=11.5, color="#4B5563")
        else:
            col = GREEN if p["cond"] else RED
            ax.text(n / 2, 0.75,
                    f"¿ A[{i + 1}] = {A[i]}  >  B[{n - i}] = {B[n - i - 1]} ?    "
                    f"{'SÍ' if p['cond'] else 'NO'}",
                    ha="center", fontsize=13.5, color=col, fontweight="bold")
            if p["cond"]:
                msg = f"A[{i + 1}] ya es demasiado grande para L  ⇒  i* ≤ i  ⇒  hi = {i}"
            else:
                msg = f"A[{i + 1}] sí cabe en L (es menor que B[{n - i}])  ⇒  i* ≥ i+1  ⇒  lo = {i + 1}"
            ax.text(n / 2, 0.05, msg, ha="center", fontsize=11.5, color=col)

    save_gif(fig, update, len(frames), "s1_busqueda.gif", 1500)


# =========================================================================
# SECCIÓN 1 -- Figura 2: monotonía de g(i)
# =========================================================================
def s1_monotonia():
    A = [2, 5, 8, 11, 14, 17, 20, 23]
    B = [1, 3, 6, 9, 12, 15, 18, 21]
    n = len(A)
    _, istar = trace(A, B)
    gs = g_values(A, B)
    xs = list(range(n))
    ya = [A[i] for i in xs]                 # A[i+1] (sube)
    yb = [B[n - i - 1] for i in xs]         # B[n-i] (baja)

    fig, (ax, ax2) = plt.subplots(2, 1, figsize=(10, 7), gridspec_kw=dict(height_ratios=[4, 1]))
    ax.plot(xs, ya, "-o", color=BLUE, lw=3, ms=8, label="A[i+1]   (sube con i)")
    ax.plot(xs, yb, "-o", color=ORANGE, lw=3, ms=8, label="B[n−i]   (baja con i)")
    ax.axvspan(istar - 0.5, n + 0.5, color=LGREEN, alpha=0.6, zorder=0)
    ax.axvspan(-0.5, istar - 0.5, color=LRED, alpha=0.5, zorder=0)
    ax.axvline(istar - 0.5, color=GREEN, ls="--", lw=2)
    ax.plot([n], [33], marker="^", color=GREEN, ms=11)
    ax.annotate("i = n:  A[n+1] = +∞ > B[0] = −∞\n(g(n) siempre es verdadero)",
                xy=(n, 33), xytext=(n - 2.2, 33), ha="right", va="center",
                fontsize=10.5, color=GREEN, arrowprops=dict(arrowstyle="->", color=GREEN))
    ax.text(istar / 2 - 0.5, 28, "g(i) = FALSO\nA[i+1] < B[n−i]", ha="center", fontsize=12,
            color=RED, fontweight="bold")
    ax.text((istar + n - 2.2) / 2 + 0.3, 27, "g(i) = VERDADERO\nA[i+1] > B[n−i]", ha="center", fontsize=12,
            color=GREEN, fontweight="bold")
    ax.set_xlim(-0.5, n + 0.5)
    ax.set_ylim(0, 36)
    ax.set_xticks(range(n + 1))
    ax.set_xlabel("i  (cuántos elementos de A van en L)", fontsize=12)
    ax.set_title("g(i) ≡ A[i+1] > B[n−i]  es MONÓTONA:  F…F V…V   ⇒   búsqueda binaria",
                 fontsize=14, fontweight="bold", color=DARK, pad=34)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, fontsize=11, frameon=False)
    ax.grid(alpha=0.25)

    ax2.set_xlim(-0.5, n + 0.5)
    ax2.set_ylim(0, 1)
    ax2.axis("off")
    for t, v in enumerate(gs):
        ax2.add_patch(Rectangle((t - 0.42, 0.1), 0.84, 0.8,
                                facecolor=LGREEN if v else LRED,
                                edgecolor=GREEN if v else RED, lw=2))
        ax2.text(t, 0.5, "V" if v else "F", ha="center", va="center", fontsize=14,
                 fontweight="bold", color=GREEN if v else RED)
    ax2.text(istar, -0.05, f"★ i* = {istar} (primer V)", ha="center", va="top",
             fontsize=12, color=GREEN, fontweight="bold")
    save_png(fig, "s1_monotonia.png")


# =========================================================================
# SECCIÓN 2 -- Figura 3: las 4 desigualdades que prueban L < R
# =========================================================================
def s2_cuatro_casos():
    A, B = [1, 2, 3, 4, 10, 12], [5, 6, 7, 8, 9, 11]
    n, i = len(A), 4
    j = n - i
    ya, yb, h = 3.4, 0.9, 0.8
    fig, ax = plt.subplots(figsize=(11.5, 7.2))
    ax.set_xlim(-1.4, n + 5.0)
    ax.set_ylim(-1.6, 6.2)
    ax.axis("off")
    ax.set_title("Lema 3:  C1 y C2  ⇒  todo elemento de L es menor que todo elemento de R",
                 fontsize=15, fontweight="bold", color=DARK)
    row(ax, A, ya, i, "A")
    row(ax, B, yb, j, "B")

    def arr(p, q, color, rad, lw=3):
        ax.add_patch(FancyArrowPatch(p, q, connectionstyle=f"arc3,rad={rad}",
                                     arrowstyle="-|>", mutation_scale=22, color=color, lw=lw))

    cA, cB = lambda k: k - 0.5, lambda k: k - 0.5
    # 1) A[i] < A[i+1]
    arr((cA(i), ya + h + 0.05), (cA(i + 1), ya + h + 0.05), GREEN, -0.9)
    # 2) B[j] < B[j+1]
    arr((cB(j), yb - 0.35), (cB(j + 1), yb - 0.35), BLUE, 0.9)
    # 3) C1: A[i] < B[j+1]
    arr((cA(i), ya), (cB(j + 1), yb + h), RED, 0.0, 3.4)
    # 4) C2: B[j] < A[i+1]
    arr((cB(j), yb + h), (cA(i + 1), ya), "#8E44AD", 0.0, 3.4)

    x0, y0 = n + 0.9, 5.2
    items = [(GREEN, "① x ∈ A[1..i], y ∈ A[i+1..n]", "x ≤ A[i] < A[i+1] ≤ y   (A ordenado)"),
             (BLUE, "② x ∈ B[1..j], y ∈ B[j+1..n]", "x ≤ B[j] < B[j+1] ≤ y   (B ordenado)"),
             (RED, "③ x ∈ A[1..i], y ∈ B[j+1..n]", "x ≤ A[i] < B[j+1] ≤ y   (condición C1)"),
             ("#8E44AD", "④ x ∈ B[1..j], y ∈ A[i+1..n]", "x ≤ B[j] < A[i+1] ≤ y   (condición C2)")]
    for t, (c, a, b) in enumerate(items):
        yy = y0 - t * 1.45
        ax.add_patch(FancyBboxPatch((x0, yy - 0.5), 3.3, 1.2, boxstyle="round,pad=0.05",
                                    facecolor="white", edgecolor=c, lw=2.5))
        ax.text(x0 + 0.12, yy + 0.38, a, fontsize=9.6, fontweight="bold", color=c, va="center")
        ax.text(x0 + 0.12, yy - 0.12, b, fontsize=9.4, color=DARK, va="center")
    ax.text(n / 2 + 0.2, -0.55, "Los 4 casos cubren todos los pares (x ∈ L, y ∈ R)",
            ha="center", fontsize=12.5, color=DARK, fontweight="bold")
    ax.text(n / 2 + 0.2, -1.15, "⇒ L son exactamente los n menores  ⇒  mediana = max(A[i], B[j]) = 6",
            ha="center", fontsize=12, color=GREEN, fontweight="bold")
    ax.text(i, ya + h + 0.95, "corte", ha="center", fontsize=10, color=DARK)
    save_png(fig, "s2_cuatro_casos.png")


# =========================================================================
# SECCIÓN 2 -- GIF 2: invariante  lo <= i* <= hi  (y por qué se mantiene)
# =========================================================================
def s2_invariante():
    rng = random.Random(11)
    pool = rng.sample(range(1, 100), 32)
    rng.shuffle(pool)
    A, B = sorted(pool[:16]), sorted(pool[16:])
    n = len(A)
    pasos, istar = trace(A, B)
    assert max(A[istar - 1] if istar else -1e9, B[n - istar - 1] if n - istar else -1e9) == sorted(A + B)[n - 1]
    gs = g_values(A, B)

    # estados: (kind, paso, lo, hi, known)
    known = {}
    frames = [("init", 0, 0, n, dict(known), None)]
    for s, p in enumerate(pasos, start=1):
        k_probe = dict(known)
        k_probe[p["i"]] = p["cond"]
        frames.append(("probe", s, p["lo"], p["hi"], k_probe, p))
        if p["cond"]:
            for t in range(p["i"], n + 1):
                known[t] = True
        else:
            for t in range(0, p["i"] + 1):
                known[t] = False
        frames.append(("decide", s, p["nlo"], p["nhi"], dict(known), p))
    frames += [("final", 0, istar, istar, dict(known), None)] * 3

    fig, ax = plt.subplots(figsize=(12.5, 5.6))

    def update(k):
        ax.clear()
        ax.set_xlim(-1.3, n + 0.9)
        ax.set_ylim(-1.7, 4.3)
        ax.axis("off")
        kind, s, lo, hi, kn, p = frames[k]
        ax.set_title("Invariante del bucle:   lo ≤ i* ≤ hi   (n = 16, i* es el primer V de g)",
                     fontsize=15, fontweight="bold", color=DARK)
        for t in range(n + 1):
            v = kn.get(t)
            if v is None:
                fc, ec, tx, tc = "#F3F4F6", GRAY, "?", "#6B7280"
            elif v:
                fc, ec, tx, tc = LGREEN, GREEN, "V", GREEN
            else:
                fc, ec, tx, tc = LRED, RED, "F", RED
            ax.add_patch(Rectangle((t - 0.42, 1.5), 0.84, 0.9, facecolor=fc, edgecolor=ec, lw=2))
            ax.text(t, 1.95, tx, ha="center", va="center", fontsize=14, fontweight="bold", color=tc)
            ax.text(t, 1.35, str(t), ha="center", va="top", fontsize=9, color="#6B7280")
        ax.text(-0.7, 1.95, "g(i)", ha="right", va="center", fontsize=14, fontweight="bold", color=DARK)
        ax.add_patch(Rectangle((lo - 0.5, 1.4), hi - lo + 1, 1.1, fill=False, edgecolor=BLUE, lw=4))
        ax.text((lo + hi) / 2, 2.65, "ventana [lo, hi]", ha="center", color=BLUE, fontsize=11, fontweight="bold")
        if kind in ("probe",):
            i = p["i"]
            ax.add_patch(Rectangle((i - 0.42, 1.5), 0.84, 0.9, fill=False, edgecolor=GOLD, lw=4))
            ax.text(i, 3.15, f"i = {i}", ha="center", color=GOLD, fontsize=13, fontweight="bold")
        ok = lo <= istar <= hi
        ax.text(n / 2, 0.55, f"lo = {lo}   ≤   i* = {istar}   ≤   hi = {hi}      {'✔ invariante se cumple' if ok else '✘'}",
                ha="center", fontsize=14, color=GREEN, fontweight="bold")
        if kind == "init":
            msg = "Inicio: lo = 0, hi = n. Como i* ∈ {0..n}, el invariante vale. (los '?' son valores aún desconocidos)"
        elif kind == "probe":
            msg = f"Paso {s}: probamos i = {p['i']}  ⇒  g({p['i']}) = {'V' if p['cond'] else 'F'}"
        elif kind == "decide":
            if p["cond"]:
                msg = (f"g({p['i']}) = V  ⇒  i* ≤ {p['i']} (minimalidad)  ⇒  hi ← {p['i']}.   "
                       "Monotonía: g(k)=V para todo k ≥ i")
            else:
                msg = (f"g({p['i']}) = F  ⇒  g(k)=F para todo k ≤ {p['i']} (monotonía)  ⇒  i* ≥ {p['i'] + 1}  ⇒  lo ← {p['i'] + 1}")
        else:
            msg = f"lo = hi = i* = {istar}.  Terminó: el corte correcto es i* = {istar}."
        ax.text(n / 2, -0.3, msg, ha="center", fontsize=11.5, color=DARK)
        if kind == "final":
            ax.text(istar, 3.15, "★ i*", ha="center", color=GREEN, fontsize=15, fontweight="bold")

    save_gif(fig, update, len(frames), "s2_invariante.gif", 1700)


# =========================================================================
# SECCIÓN 3 -- Figura 4: árbol de decisión con 2n hojas
# =========================================================================
def s3_arbol():
    n = 4
    leaves = [f"A{k}" for k in range(1, n + 1)] + [f"B{k}" for k in range(1, n + 1)]
    fig, ax = plt.subplots(figsize=(12, 6.8))
    ax.set_xlim(-1.6, 8.6)
    ax.set_ylim(-2.4, 4.0)
    ax.axis("off")
    ax.set_title("Árbol de decisión: cada hoja = una respuesta posible  (hay 2n = 8)",
                 fontsize=15, fontweight="bold", color=DARK)

    pos = {}
    for k in range(8):
        pos[(0, k)] = (k, 0.0)
    for lvl in (1, 2, 3):
        for k in range(8 // 2 ** lvl):
            a, b = pos[(lvl - 1, 2 * k)], pos[(lvl - 1, 2 * k + 1)]
            pos[(lvl, k)] = ((a[0] + b[0]) / 2, lvl * 1.15)
    path = {(3, 0), (2, 1), (1, 3), (0, 6)}          # camino hacia la hoja B3

    for lvl in (1, 2, 3):
        for k in range(8 // 2 ** lvl):
            x, y = pos[(lvl, k)]
            for c, lab in ((2 * k, "sí"), (2 * k + 1, "no")):
                cx, cy = pos[(lvl - 1, c)]
                on = (lvl, k) in path and (lvl - 1, c) in path
                ax.plot([x, cx], [y - 0.2, cy + (0.35 if lvl == 1 else 0.2)],
                        color=RED if on else GRAY, lw=3.4 if on else 1.8, zorder=1)
                ax.text((x + cx) / 2 + (-0.14 if lab == "sí" else 0.14), (y + cy) / 2 + 0.1, lab,
                        fontsize=8.5, ha="center", color=RED if on else "#6B7280")
    for (lvl, k), (x, y) in pos.items():
        if lvl == 0:
            on = (0, k) in path
            ax.add_patch(FancyBboxPatch((x - 0.38, -0.3), 0.76, 0.6, boxstyle="round,pad=0.03",
                                        facecolor=LRED if on else LBLUE, edgecolor=RED if on else BLUE, lw=2.2, zorder=3))
            ax.text(x, 0, leaves[k], ha="center", va="center", fontsize=12, fontweight="bold",
                    color=RED if on else BLUE, zorder=4)
        else:
            on = (lvl, k) in path
            ax.add_patch(Circle((x, y), 0.25, facecolor=LRED if on else "white",
                                edgecolor=RED if on else DARK, lw=2.2, zorder=3))
            ax.text(x, y, "x<y?", ha="center", va="center", fontsize=7.5, color=DARK, zorder=4)

    ax.annotate("", xy=(-1.0, 0.2), xytext=(-1.0, 3.45),
                arrowprops=dict(arrowstyle="<->", color=GREEN, lw=2.5))
    ax.text(-1.15, 1.8, "h = 3\ncomparaciones", rotation=90, ha="right", va="center",
            fontsize=12, color=GREEN, fontweight="bold")
    ax.text(3.5, -0.85, "Un árbol binario de altura h tiene a lo sumo 2ʰ hojas", ha="center",
            fontsize=12.5, color=DARK)
    ax.text(3.5, -1.45, "Se necesitan ≥ 2n hojas  ⇒  2ʰ ≥ 2n  ⇒  h ≥ log₂(2n) = 1 + log₂ n = Ω(log n)",
            ha="center", fontsize=13, color=GREEN, fontweight="bold")
    ax.text(3.5, -2.05, "(camino rojo: las 3 respuestas sí/no que identifican a B3 como mediana)",
            ha="center", fontsize=10.5, color=RED)
    save_png(fig, "s3_arbol_decision.png")


# =========================================================================
# SECCIÓN 3 -- GIF 3: cada comparación (1 bit) divide los candidatos por 2
# =========================================================================
def s3_cota():
    n = 8
    labels = [f"A{k}" for k in range(1, n + 1)] + [f"B{k}" for k in range(1, n + 1)]
    target = 10                                      # "B3" es la mediana real
    intervals = [(0, 16)]
    lo, hi = 0, 16
    while hi - lo > 1:
        mid = (lo + hi) // 2
        lo, hi = (mid, hi) if target >= mid else (lo, mid)
        intervals.append((lo, hi))
    frames = intervals + [intervals[-1]] * 3

    fig, ax = plt.subplots(figsize=(11.5, 6))

    def update(k):
        ax.clear()
        ax.set_xlim(-1.5, n + 0.7)
        ax.set_ylim(-1.8, 5.0)
        ax.axis("off")
        lo, hi = frames[k]
        ncomp = min(k, len(intervals) - 1)
        alive = hi - lo
        ax.set_title("Cota de información: cada comparación da 1 bit  ⇒  divide los candidatos a lo más por 2",
                     fontsize=13.5, fontweight="bold", color=DARK)
        for idx in range(2 * n):
            r, c = divmod(idx, n)
            y = 3.3 - r * 1.5
            vivo = lo <= idx < hi
            ax.add_patch(Rectangle((c, y), 0.92, 0.95, facecolor=YELLOW if vivo else "#EEF0F3",
                                   edgecolor=DARK if vivo else GRAY, lw=1.5))
            ax.text(c + 0.46, y + 0.47, labels[idx], ha="center", va="center", fontsize=12,
                    fontweight="bold", color=DARK if vivo else "#B0B6BF")
        if alive == 1:
            r, c = divmod(lo, n)
            ax.add_patch(Rectangle((c, 3.3 - r * 1.5), 0.92, 0.95, fill=False, edgecolor=GREEN, lw=4.5))
        ax.text(n / 2, 1.4, f"Comparaciones realizadas: {ncomp}", ha="center", fontsize=14,
                fontweight="bold", color=BLUE)
        ax.text(n / 2, 0.8, f"Candidatos a mediana que siguen vivos: {alive}   "
                            f"(bits que faltan = log₂({alive}) = {math.log2(alive):.0f})",
                ha="center", fontsize=12.5, color=DARK)
        if alive == 1:
            msg = "Quedó 1 solo candidato tras log₂(2n) = log₂(16) = 4 comparaciones  ⇒  no se puede en menos"
            col = GREEN
        else:
            msg = "Un algoritmo debe distinguir los 2n candidatos: 2ʰ ≥ 2n  ⇒  h ≥ log₂(2n)"
            col = DARK
        ax.text(n / 2, 0.05, msg, ha="center", fontsize=12, color=col, fontweight="bold" if alive == 1 else None)
        ax.text(n / 2, -0.7, "Búsqueda binaria sobre i hace ⌈log₂(n+1)⌉ + 1 ≈ log₂ n: ÓPTIMO (diferencia ≤ 1)",
                ha="center", fontsize=11, color="#4B5563")

    save_gif(fig, update, len(frames), "s3_cota_informacion.gif", 1400)


if __name__ == "__main__":
    s1_corte()
    s1_busqueda()
    s1_monotonia()
    s2_cuatro_casos()
    s2_invariante()
    s3_arbol()
    s3_cota()
    print("\nListo. Archivos en:", OUT)