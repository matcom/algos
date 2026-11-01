import os
import random
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT, exist_ok=True)

# ----------------------------------------------------------------- estilo ---
COL = {"A": "#2f6fdb", "B": "#ee8a2c", "C": "#2e9e6b", "D": "#a855c7", "E": "#c79a0a"}
BG, INK, MUTE = "#fbfaf7", "#1f2430", "#8a8f9c"
RED, GOOD, SOFT = "#d6343a", "#1f9d55", "#e9e6df"
RULE_COL = {1: "#2f6fdb", 2: "#2f6fdb", 3: "#2e9e6b", 4: "#2e9e6b", 5: RED}

EJEMPLO = list("ABACABDAB")  # n = 9; A aparece 4 veces (> 3) y B 3 veces (no > 3)


def canvas():
    fig = plt.figure(figsize=(12, 6.667), facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1])
    reset(ax)
    return fig, ax


def reset(ax):
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 10)
    ax.set_facecolor(BG)
    ax.axis("off")


def header(ax, tag, title):
    ax.text(0.6, 9.55, tag.upper(), fontsize=10, color=MUTE, fontweight="bold", va="center")
    ax.text(0.6, 8.95, title, fontsize=17, color=INK, fontweight="bold", va="center")


def block(ax, x, y, ch, w=0.9, alpha=1.0, edge=None, lw=3, fs=14, z=3):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - w / 2), w, w,
                                boxstyle="round,pad=0,rounding_size=0.14",
                                fc=COL.get(ch, "#888"), ec=edge or "none",
                                lw=lw if edge else 0, alpha=alpha, zorder=z))
    ax.text(x, y, ch, ha="center", va="center", color="white", fontsize=fs,
            fontweight="bold", alpha=alpha, zorder=z + 1)


def box(ax, x, y, w, h, fc="white", ec=INK, lw=1.6, ls="-", r=0.25, z=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=fc, ec=ec, lw=lw, ls=ls, zorder=z))


def save_png(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=110, facecolor=BG)
    plt.close(fig)
    print("OK", path)


def save_gif(fig, update, frames, name, fps=1.0):
    path = os.path.join(OUT, name)
    ani = FuncAnimation(fig, update, frames=frames, repeat=True)
    ani.save(path, writer=PillowWriter(fps=fps), dpi=80, savefig_kwargs={"facecolor": BG})
    plt.close(fig)
    print("OK", path)


# ------------------------------------------------------------- algoritmo ---
def simulate(A):
    """Primera pasada. Devuelve la traza completa, incluida la partición explícita
    (ternas + copias de c1 + copias de c2) que construye la demostración del invariante."""
    c1 = c2 = None
    k1 = k2 = 0
    s1, s2, ternas = [], [], []
    tr = [dict(i=0, x=None, rule=None, c1=c1, k1=k1, c2=c2, k2=k2,
               ternas=[], s1=[], s2=[], new=[])]
    for i, x in enumerate(A):
        if k1 > 0 and x == c1:
            rule, k1 = 1, k1 + 1
            s1.append(i)
            new = [i]
        elif k2 > 0 and x == c2:
            rule, k2 = 2, k2 + 1
            s2.append(i)
            new = [i]
        elif k1 == 0:
            rule, c1, k1 = 3, x, 1
            s1.append(i)
            new = [i]
        elif k2 == 0:
            rule, c2, k2 = 4, x, 1
            s2.append(i)
            new = [i]
        else:
            rule, k1, k2 = 5, k1 - 1, k2 - 1
            t = (s1.pop(), s2.pop(), i)
            ternas.append(t)
            new = list(t)
        tr.append(dict(i=i + 1, x=x, rule=rule, c1=c1, k1=k1, c2=c2, k2=k2,
                       ternas=list(ternas), s1=list(s1), s2=list(s2), new=new))
    return tr


def candidatos(A):
    s = simulate(A)[-1]
    return [c for c, k in ((s["c1"], s["k1"]), (s["c2"], s["k2"])) if k > 0]


def correcto(A):
    return {c for c in candidatos(A) if 3 * A.count(c) > len(A)}


def atajo(A):
    return set(candidatos(A))


def invariante_ok(A, s):
    """Comprueba las 3 condiciones del invariante reforzado en el estado s (prefijo A[:s.i])."""
    c1_ = s["k1"] >= 0 and s["k2"] >= 0
    c2_ = not (s["k1"] > 0 and s["k2"] > 0) or s["c1"] != s["c2"]
    idx = sorted([j for t in s["ternas"] for j in t] + s["s1"] + s["s2"])
    c3_ = (idx == list(range(s["i"]))
           and all(len({A[j] for j in t}) == 3 for t in s["ternas"])
           and all(A[j] == s["c1"] for j in s["s1"]) and len(s["s1"]) == s["k1"]
           and all(A[j] == s["c2"] for j in s["s2"]) and len(s["s2"]) == s["k2"]
           and s["i"] == 3 * len(s["ternas"]) + s["k1"] + s["k2"])
    return c1_, c2_, c3_


def autotest(trials=20000, seed=1):
    """Verifica en el propio script el invariante y el teorema (no solo se dibujan)."""
    rng = random.Random(seed)
    for _ in range(trials):
        n = rng.randint(1, 14)
        A = [rng.choice("ABCDE"[: rng.randint(1, 5)]) for _ in range(n)]
        tr = simulate(A)
        for s in tr:
            assert all(invariante_ok(A, s)), (A, s)
        cand = set(candidatos(A))
        for v in set(A):
            if 3 * A.count(v) > n:
                assert v in cand, (A, v)
    print("autotest OK: invariante y teorema verificados en", trials, "arreglos aleatorios")


# =========================================================== 01 PLANTEAMIENTO
def fig_planteamiento():
    A = EJEMPLO
    n = len(A)
    fig, ax = canvas()
    header(ax, "Planteamiento", "Pesado = aparece más de n/3 veces.  ¿Cuántos pesados puede haber?")

    ax.text(0.7, 8.0, "① A lo sumo dos pesados", fontsize=13, fontweight="bold", color=INK)
    sc, x0, y, h = 6.6 / 9, 0.9, 6.3, 0.9
    for k, ch in enumerate("ABC"):
        a = x0 + k * 3.34 * sc
        ax.add_patch(Rectangle((a, y), 3.34 * sc, h, fc=COL[ch], ec="white", lw=2, alpha=0.9, zorder=3))
        ax.text(a + 1.67 * sc, y + h / 2, "> n/3", ha="center", va="center", color="white",
                fontsize=12, fontweight="bold", zorder=4)
    limite = x0 + 9 * sc
    fin = x0 + 3 * 3.34 * sc
    ax.add_patch(Rectangle((limite, y), fin - limite, h, fc="none", ec=RED, lw=0, hatch="////", zorder=5))
    ax.add_patch(Rectangle((x0, y), 9 * sc, h, fc="none", ec=INK, lw=2.4, zorder=6))
    ax.text(x0 + 4.5 * sc, y + h + 0.3, "las n posiciones del arreglo", ha="center", fontsize=10, color=MUTE)
    ax.text((limite + fin) / 2 + 0.2, y - 0.35, "¡se sale!", ha="center", fontsize=11, color=RED, fontweight="bold")
    ax.text(0.9, 5.2, "Tres pesados necesitarían más de 3·(n/3) = n posiciones.", fontsize=11, color=INK)
    ax.text(0.9, 4.7, "Imposible  ⇒  a lo sumo 2 pesados  ⇒  bastan 2 candidatos.", fontsize=11,
            color=INK, fontweight="bold")

    box(ax, 0.7, 0.9, 7.9, 3.0, fc="white", ec=SOFT, lw=2)
    ax.text(0.95, 3.5, "Convenciones", fontsize=12, fontweight="bold", color=INK)
    lin = ["Estado: (c₁, k₁, c₂, k₂) = dos candidatos con su contador.",
           "k = 0  ⇒  casillero vacío (su valor no significa nada).",
           "Solo se compara por igualdad (x = c ?).",
           "Meta: tiempo O(n), memoria extra O(1)."]
    for j, t in enumerate(lin):
        ax.text(1.0, 2.9 - j * 0.5, "• " + t, fontsize=10.5, color=INK)

    ax.text(9.8, 8.0, f"② Ejemplo: n = {n}  →  umbral n/3 = {n // 3}", fontsize=13, fontweight="bold", color=INK)
    for i, ch in enumerate(A):
        block(ax, 10.15 + i * 0.92, 7.0, ch, w=0.74, fs=11)
    base, u = 1.5, 0.85
    for j, ch in enumerate("ABCD"):
        cx, cnt = 11.2 + j * 1.8, A.count(ch)
        ax.add_patch(Rectangle((cx - 0.6, base), 1.2, cnt * u, fc=COL[ch], zorder=3))
        ax.text(cx, base - 0.4, ch, ha="center", fontsize=12, fontweight="bold", color=INK)
        ax.text(cx, base + cnt * u + 0.15, str(cnt), ha="center", fontsize=12, fontweight="bold", color=INK)
    ax.plot([10.3, 17.6], [base + (n // 3) * u] * 2, ls="--", color=INK, lw=1.8, zorder=4)
    ax.text(17.6, base + (n // 3) * u + 0.15, "n/3 = 3", ha="right", fontsize=10, color=INK)
    ax.text(11.2, base + 4 * u + 0.62, "4 > 3  ✓ pesado", ha="center", fontsize=10, color=GOOD, fontweight="bold")
    ax.text(13.0, base + 3 * u + 0.62, "3 > 3  ✗", ha="center", fontsize=10, color=RED, fontweight="bold")
    ax.text(14.6, 6.15, "B está justo en el umbral: no es pesado", ha="center", fontsize=9.5, color=MUTE)
    save_png(fig, "01_planteamiento.png")


# ============================================================ 02 CANCELACIÓN
def fig_cancelacion():
    A = EJEMPLO
    n = len(A)
    tr = simulate(A)
    ternas = tr[-1]["ternas"]
    heavy = [v for v in sorted(set(A)) if 3 * A.count(v) > n]
    frames = [(0, None, False)] * 2
    for j in range(len(ternas)):
        frames += [(j, j, False)] * 2 + [(j + 1, None, False)] * 2
    frames += [(len(ternas), None, True)] * 3

    fig, ax = canvas()

    def update(f):
        struck_n, hl, final = frames[f]
        ax.clear()
        reset(ax)
        header(ax, "Generalización · la idea", "Tachar ternas de elementos distintos entre sí")
        struck = {j for t in ternas[:struck_n] for j in t}
        hot = set(ternas[hl]) if hl is not None else set()
        for i, ch in enumerate(A):
            x, y = 3.4 + 1.4 * i, 7.3
            block(ax, x, y, ch, w=1.0, alpha=0.2 if i in struck else 1.0,
                  edge=RED if i in hot else None, fs=16)
            if i in struck:
                ax.plot([x - 0.5, x + 0.5], [y - 0.5, y + 0.5], color=RED, lw=2.5, zorder=6)
            ax.text(x, y - 0.8, str(i + 1), ha="center", fontsize=8, color=MUTE)

        rem = n - 3 * struck_n
        if hl is not None:
            a, b, c = (A[j] for j in ternas[hl])
            msg = f"Terna {hl + 1}: ({a}, {b}, {c}) — tres valores distintos."
            sub = "Cada valor aparece UNA sola vez en la terna: tacharla le quita a lo sumo 1 copia a cualquier valor."
        elif final:
            msg = "Ya no quedan ternas de distintos."
            sub = "Lo que sobrevive usa a lo sumo 2 valores distintos → los pesados tienen que estar ahí."
        elif struck_n == 0:
            msg = "Plan: ir tachando ternas (x, y, z) con x, y, z distintos."
            sub = "Sin importar el orden: nos quedamos con lo que no se pueda tachar."
        else:
            msg = f"Se tacharon {struck_n} terna(s): quedan {rem} elementos."
            sub = "Siguiente: buscar otra terna de distintos entre los que quedan."
        ax.text(9, 5.55, msg, ha="center", fontsize=13, fontweight="bold", color=INK)
        ax.text(9, 5.05, sub, ha="center", fontsize=10, color=MUTE)

        ax.text(0.7, 4.2, "Lo que sobrevive:", fontsize=11, fontweight="bold", color=INK)
        vivos = [A[j] for j in range(n) if j not in struck]
        for k, ch in enumerate(vivos):
            block(ax, 3.4 + k * 1.1, 3.55, ch, w=0.85, fs=13)

        ax.text(0.7, 2.55, "¿Sigue siendo pesado?", fontsize=11, fontweight="bold", color=INK)
        for v in heavy:
            r = sum(1 for j in range(n) if j not in struck and A[j] == v)
            ok = rem == 0 or 3 * r > rem
            block(ax, 1.0, 1.85, v, w=0.7, fs=11)
            ax.text(1.55, 1.85,
                    f"queda {r} de {rem} elementos  →  {r} > {rem}/3 = {rem / 3:.2f}   " + ("✓" if ok else "✗"),
                    fontsize=12, va="center", color=GOOD if ok else RED, fontweight="bold")
        ax.text(9, 0.6, "#v − t  >  n/3 − t  =  (n − 3t)/3      (t = ternas tachadas)",
                ha="center", fontsize=12, color=INK, style="italic")

    save_gif(fig, update, range(len(frames)), "02_cancelacion.gif", fps=0.9)


# ============================================================ 03 ALGORITMO
def draw_slot(ax, x0, y0, w, h, label, c, k, verdict=None):
    empty = k == 0
    ec = MUTE if empty else COL.get(c, "#888")
    box(ax, x0, y0, w, h, fc="white", ec=ec, lw=2.4, ls="--" if empty else "-")
    ax.text(x0 + 0.3, y0 + h - 0.4, label, fontsize=11, color=MUTE, fontweight="bold", va="center")
    if empty:
        ax.text(x0 + w / 2, y0 + h / 2 - 0.15, "vacío  (k = 0)", ha="center", va="center", fontsize=14, color=MUTE)
    else:
        block(ax, x0 + 1.1, y0 + h / 2 - 0.2, c, w=1.2, fs=20)
        step = min(0.75, 2.9 / max(k, 1))
        for j in range(k):
            ax.add_patch(Circle((x0 + 2.5 + j * step, y0 + h / 2 - 0.2), 0.27, fc=COL[c], ec="white", lw=1.5, zorder=4))
        ax.text(x0 + w - 0.3, y0 + h / 2 - 0.2, f"k = {k}", ha="right", va="center", fontsize=18,
                fontweight="bold", color=INK)
    if verdict:
        ax.text(x0 + w / 2, y0 - 0.35, verdict[0], ha="center", fontsize=11.5, fontweight="bold", color=verdict[1])


def fig_algoritmo():
    A = EJEMPLO
    n = len(A)
    tr = simulate(A)
    nombres = {1: "R1 suma a c₁", 2: "R2 suma a c₂", 3: "R3 ocupa casillero 1", 4: "R4 ocupa casillero 2",
               5: "R5 cancela terna"}
    fig, ax = canvas()
    frames = list(range(len(tr))) + ["fin", "verif"]

    def update(f):
        ax.clear()
        reset(ax)
        header(ax, "Generalización · el mecanismo", "Dos casilleros, cinco reglas (en este orden)")
        step = tr[f] if isinstance(f, int) else tr[-1]
        i = step["i"]
        for j, ch in enumerate(A):
            done = j < i
            block(ax, 3.4 + 1.4 * j, 7.4, ch, w=1.0, alpha=1.0 if (done or not isinstance(f, int)) else 0.3,
                  edge=INK if (isinstance(f, int) and j == i - 1) else None, fs=16)
        if isinstance(f, int) and i > 0:
            ax.text(3.4 + 1.4 * (i - 1), 8.2, "▼", ha="center", fontsize=14, color=INK)

        verdict1 = verdict2 = None
        if f == "verif":
            for k_, (c, slot) in enumerate(((step["c1"], 1), (step["c2"], 2))):
                if (step["k1"], step["k2"])[k_] > 0:
                    cnt = A.count(c)
                    v = (f"2.ª pasada: {c} aparece {cnt} → {cnt} > {n}/3 ?  " + ("✓ pesado" if 3 * cnt > n else "✗ se descarta"),
                         GOOD if 3 * cnt > n else RED)
                    if slot == 1:
                        verdict1 = v
                    else:
                        verdict2 = v
        draw_slot(ax, 1.2, 3.6, 7.0, 2.8, "CASILLERO 1", step["c1"], step["k1"], verdict1)
        draw_slot(ax, 9.8, 3.6, 7.0, 2.8, "CASILLERO 2", step["c2"], step["k2"], verdict2)

        r, x = step["rule"], step["x"]
        prev = tr[f - 1] if isinstance(f, int) and f > 0 else None
        if f == 0:
            msg, sub, col = "Estado inicial: los dos casilleros vacíos.", "Vamos leyendo el arreglo de izquierda a derecha.", MUTE
        elif f == "fin":
            msg = f"Fin de la 1.ª pasada: candidatos con k > 0 = {sorted(candidatos(A))}"
            sub, col = "Por el teorema, todo pesado está entre ellos (pero no todo candidato es pesado).", INK
        elif f == "verif":
            msg, sub, col = "La 2.ª pasada cuenta de verdad y filtra.", "Solo A supera n/3: respuesta = {A}.", GOOD
        else:
            col = RULE_COL[r]
            if r == 1:
                msg, sub = f"Llega {x}  →  R1: {x} = c₁", f"Una copia más de {x}:  k₁ = {step['k1']}"
            elif r == 2:
                msg, sub = f"Llega {x}  →  R2: {x} = c₂", f"Una copia más de {x}:  k₂ = {step['k2']}"
            elif r == 3:
                msg, sub = f"Llega {x}  →  R3: el casillero 1 está vacío", f"{x} lo ocupa:  c₁ = {x}, k₁ = 1"
            elif r == 4:
                msg, sub = f"Llega {x}  →  R4: el casillero 2 está vacío", f"{x} lo ocupa:  c₂ = {x}, k₂ = 1"
            else:
                msg = f"Llega {x}  →  R5: {x} ≠ c₁ y {x} ≠ c₂"
                sub = f"({prev['c1']}, {prev['c2']}, {x}) son distintos: se tacha la terna  →  k₁ y k₂ bajan 1"
                for q, ch in enumerate((prev["c1"], prev["c2"], x)):
                    block(ax, 15.3 + q * 0.9, 2.55, ch, w=0.7, fs=11, alpha=0.5)
                    ax.plot([15.3 + q * 0.9 - 0.35, 15.3 + q * 0.9 + 0.35], [2.2, 2.9], color=RED, lw=2.2, zorder=6)
        ax.text(0.9, 2.8, msg, fontsize=14, fontweight="bold", color=col, va="center")
        ax.text(0.9, 2.2, sub, fontsize=11, color=INK, va="center")

        cur = r if isinstance(f, int) else None
        for q in range(1, 6):
            px = 0.9 + (q - 1) * 3.4
            on = cur == q
            box(ax, px, 0.5, 3.2, 0.7, fc=RULE_COL[q] if on else "white", ec=RULE_COL[q], lw=1.6, r=0.3)
            ax.text(px + 1.6, 0.85, nombres[q], ha="center", va="center", fontsize=9.5,
                    color="white" if on else RULE_COL[q], fontweight="bold")

    save_gif(fig, update, frames, "03_algoritmo.gif", fps=0.8)


# ================================================================ 04 REGLAS
def fig_reglas():
    fig, ax = canvas()
    header(ax, "Generalización · las reglas", "Un árbol de decisión: el ORDEN de las reglas es lo que importa")

    dec = [("¿ x = c₁  (con k₁ > 0) ?", 7.4), ("¿ x = c₂  (con k₂ > 0) ?", 5.8),
           ("¿ casillero 1 vacío  (k₁ = 0) ?", 4.2), ("¿ casillero 2 vacío  (k₂ = 0) ?", 2.6)]
    out = [(1, "R1 · k₁ ← k₁ + 1", "una copia más de c₁"), (2, "R2 · k₂ ← k₂ + 1", "una copia más de c₂"),
           (3, "R3 · c₁ ← x, k₁ ← 1", "x ocupa el casillero 1"), (4, "R4 · c₂ ← x, k₂ ← 1", "x ocupa el casillero 2")]
    for (txt, y), (r, t1, t2) in zip(dec, out):
        box(ax, 1.0, y - 0.45, 5.8, 0.9, fc="white", ec=INK, lw=1.8)
        ax.text(3.9, y, txt, ha="center", va="center", fontsize=11.5, fontweight="bold", color=INK)
        ax.annotate("", xy=(7.6, y), xytext=(6.8, y), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.6))
        ax.text(7.2, y + 0.22, "sí", ha="center", fontsize=9, color=MUTE)
        box(ax, 7.6, y - 0.45, 4.1, 0.9, fc=RULE_COL[r], ec=RULE_COL[r])
        ax.text(9.65, y + 0.12, t1, ha="center", va="center", fontsize=11, fontweight="bold", color="white")
        ax.text(9.65, y - 0.2, t2, ha="center", va="center", fontsize=8.5, color="white")
    for k in range(3):
        y0 = dec[k][1] - 0.45
        ax.annotate("", xy=(3.9, dec[k + 1][1] + 0.45), xytext=(3.9, y0), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.6))
        ax.text(4.2, (y0 + dec[k + 1][1] + 0.45) / 2, "no", fontsize=9, color=MUTE, va="center")
    ax.annotate("", xy=(3.9, 1.5), xytext=(3.9, 2.15), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.6))
    ax.text(4.2, 1.82, "no", fontsize=9, color=MUTE, va="center")
    box(ax, 1.0, 0.75, 10.7, 0.75, fc=RED, ec=RED)
    ax.text(6.35, 1.12, "R5 · k₁ ← k₁ − 1, k₂ ← k₂ − 1   →   (c₁, c₂, x) son 3 distintos: se tacha la terna",
            ha="center", va="center", fontsize=10.5, fontweight="bold", color="white")

    box(ax, 12.2, 0.75, 5.5, 7.75, fc="white", ec=SOFT, lw=2)
    ax.text(14.95, 8.1, "¿Por qué ese orden?", ha="center", fontsize=12.5, fontweight="bold", color=INK)
    ax.text(12.45, 7.4, "Estado: casillero 1 vacío,", fontsize=10, color=INK)
    ax.text(12.45, 6.95, "casillero 2 = A (k₂ = 1).  Llega x = A.", fontsize=10, color=INK)
    ax.text(12.45, 6.1, "Si R3 fuera ANTES que R2:", fontsize=10.5, fontweight="bold", color=RED)
    block(ax, 13.2, 5.35, "A", w=0.7, fs=11)
    block(ax, 14.2, 5.35, "A", w=0.7, fs=11)
    ax.text(14.85, 5.35, "c₁ = c₂ = A", fontsize=10.5, va="center", color=RED, fontweight="bold")
    ax.text(12.45, 4.65, "¡Candidatos iguales con k > 0!", fontsize=10, color=RED)
    ax.text(12.45, 4.2, "Luego R5 tacharía (A, A, x): no son", fontsize=10, color=INK)
    ax.text(12.45, 3.8, "distintos → se rompe el invariante.", fontsize=10, color=INK)
    ax.plot([12.45, 17.45], [3.3, 3.3], color=SOFT, lw=1.5)
    ax.text(12.45, 2.8, "Con el orden correcto (R2 antes):", fontsize=10.5, fontweight="bold", color=GOOD)
    ax.text(12.45, 2.3, "x = A suma al casillero 2 (k₂ = 2) y", fontsize=10, color=INK)
    ax.text(12.45, 1.9, "c₁ ≠ c₂ siempre que ambos sean > 0.", fontsize=10, color=INK)
    ax.text(12.45, 1.25, "(Comprobado por fuerza bruta: sin ese orden", fontsize=8.5, color=MUTE)
    ax.text(12.45, 0.95, "hay violaciones; con él, ninguna.)", fontsize=8.5, color=MUTE)
    save_png(fig, "04_reglas.png")


# ============================================================= 05 INVARIANTE
def fig_invariante():
    A = EJEMPLO
    n = len(A)
    tr = simulate(A)
    fig, ax = canvas()

    def update(f):
        ax.clear()
        reset(ax)
        header(ax, "Invariante reforzado", "Todo prefijo = ternas de distintos  +  k₁ copias de c₁  +  k₂ copias de c₂")
        s = tr[f]
        i = s["i"]
        for j, ch in enumerate(A):
            block(ax, 3.9 + 1.2 * j, 7.55, ch, w=0.85, alpha=1.0 if j < i else 0.25, fs=14)
        ax.text(0.6, 7.55, "Arreglo:", fontsize=10, color=MUTE, va="center")
        if i > 0:
            ax.text(3.9 + 1.2 * (i - 1), 8.2, "▼", ha="center", fontsize=12, color=INK)

        r = s["rule"]
        if f == 0:
            txt, col = "Prefijo vacío: 0 ternas, k₁ = k₂ = 0  (cumple trivialmente).", MUTE
        else:
            col = RULE_COL[r]
            txt = {1: f"R1: llega {s['x']} = c₁  →  una copia más en el grupo c₁.",
                   2: f"R2: llega {s['x']} = c₂  →  una copia más en el grupo c₂.",
                   3: f"R3: {s['x']} abre el grupo c₁ (y no es igual a c₂: si no, habría entrado por R2).",
                   4: f"R4: {s['x']} abre el grupo c₂ (y ≠ c₁: si no, habría entrado por R1).",
                   5: "R5: saco 1 copia de c₁ y 1 de c₂ y, junto con x, formo una terna nueva (distintos por ②)."}[r]
        ax.text(0.6, 6.55, txt, fontsize=11.5, fontweight="bold", color=col, va="center")

        x = 0.8
        ax.text(x, 5.95, "ternas (t = %d)" % len(s["ternas"]), fontsize=9.5, color=MUTE)
        for t in s["ternas"]:
            for q, j in enumerate(t):
                block(ax, x + q * 0.9, 5.0, A[j], w=0.8, fs=12, edge=RED if j in s["new"] and r == 5 else None, lw=3)
            ax.plot([x - 0.4, x - 0.4, x + 2.2, x + 2.2], [4.7, 4.5, 4.5, 4.7], color=INK, lw=1.5)
            x += 3.2
        gx = 10.6
        for lab, c, idxs, gx0 in (("c₁ × k₁", s["c1"], s["s1"], 10.6), ("c₂ × k₂", s["c2"], s["s2"], 14.0)):
            ax.text(gx0, 5.95, lab, fontsize=9.5, color=MUTE)
            for q, j in enumerate(idxs):
                block(ax, gx0 + 0.4 + q * 0.85, 5.0, A[j], w=0.75, fs=12,
                      edge=RED if j in s["new"] and r in (1, 2, 3, 4) else None, lw=3)
            if idxs:
                ax.plot([gx0, gx0, gx0 + 0.85 * len(idxs) - 0.1, gx0 + 0.85 * len(idxs) - 0.1], [4.7, 4.5, 4.5, 4.7],
                        color=INK, lw=1.5)
            else:
                ax.text(gx0, 5.0, "(vacío)", fontsize=10, color=MUTE, va="center")

        t_ = len(s["ternas"])
        ax.text(0.6, 3.5, f"i = 3t + k₁ + k₂   →   {i} = 3·{t_} + {s['k1']} + {s['k2']} = {3 * t_ + s['k1'] + s['k2']}",
                fontsize=14, fontweight="bold", color=INK, va="center")
        ok = invariante_ok(A, s)
        c1v = "—" if s["k1"] == 0 else s["c1"]
        c2v = "—" if s["k2"] == 0 else s["c2"]
        items = [("① k₁ ≥ 0 y k₂ ≥ 0", ok[0]),
                 (f"② si k₁ > 0 y k₂ > 0  ⇒  c₁ ≠ c₂      (c₁ = {c1v}, c₂ = {c2v})", ok[1]),
                 ("③ prefijo = ternas de distintos + k₁·c₁ + k₂·c₂ (partición exacta)", ok[2])]
        for q, (t, good) in enumerate(items):
            ax.text(0.9, 2.55 - q * 0.75, ("✓  " if good else "✗  ") + t, fontsize=11.5, va="center",
                    color=GOOD if good else RED, fontweight="bold")

    save_gif(fig, update, range(len(tr)), "05_invariante.gif", fps=0.8)


# ================================================================ 06 TEOREMA
def fig_teorema():
    fig, ax = canvas()
    header(ax, "Invariante · conclusión", "Si v es pesado, v no puede quedar fuera de los candidatos")
    ax.text(0.6, 8.1, "Supongamos que v = C es pesado pero NO es candidato. Entonces solo puede estar dentro de las ternas:",
            fontsize=10.5, color=INK)
    ternas = [("C", "D", "E"), ("A", "C", "B"), ("B", "D", "C")]
    x = 0.9
    for tr_ in ternas:
        box(ax, x - 0.55, 5.75, 3.1, 1.75, fc="white", ec=SOFT, lw=2)
        for q, ch in enumerate(tr_):
            block(ax, x + q * 1.0, 6.85, ch, w=0.85, fs=14, edge=INK if ch == "C" else None, lw=3.2)
        ax.text(x + 1.0, 6.0, "C aparece ≤ 1 vez", ha="center", fontsize=8.5, color=MUTE)
        x += 3.5
    box(ax, x - 0.55, 5.75, 2.3, 1.75, fc="white", ec=COL["A"], lw=2)
    for q in range(2):
        block(ax, x + 0.05 + q * 0.95, 6.85, "A", w=0.85, fs=14)
    ax.text(x + 0.5, 6.0, "k₁ × c₁", ha="center", fontsize=8.5, color=MUTE)
    ax.text(x + 2.1, 6.85, "+", fontsize=18, ha="center", va="center", color=MUTE)
    box(ax, x + 2.45, 5.75, 1.4, 1.75, fc="white", ec=COL["B"], lw=2)
    block(ax, x + 3.15, 6.85, "B", w=0.85, fs=14)
    ax.text(x + 3.15, 6.0, "k₂ × c₂", ha="center", fontsize=8.5, color=MUTE)

    ax.text(0.9, 5.25, "t = 3 ternas (9 elementos)  +  k₁ = 2  +  k₂ = 1   →   n = 12", fontsize=11, color=INK)

    ax.text(0.9, 4.3, "#v  ≤  t  =  (n − k₁ − k₂)/3  ≤  n/3", fontsize=17, fontweight="bold", color=INK)
    ax.text(0.9, 3.65, "3  ≤  (12 − 2 − 1)/3 = 3  ≤  12/3 = 4", fontsize=13, color=INK)
    ax.text(0.9, 2.95, "Pero ser pesado exige  #v > n/3 = 4.   Contradicción  ■", fontsize=13, color=RED, fontweight="bold")

    base, u = 0.75, 0.42
    ax.text(11.0, 4.5, "Máximo posible de C vs. umbral", fontsize=10, color=MUTE, ha="left")
    for lab, val, col, cx in (("máx. #C\n(una por terna)", 3, COL["C"], 12.0), ("umbral\nn/3", 4, MUTE, 14.2)):
        ax.add_patch(Rectangle((cx - 0.7, base + 0.5), 1.4, val * u, fc=col, alpha=0.9, zorder=3))
        ax.text(cx, base + 0.5 + val * u + 0.15, str(val), ha="center", fontsize=12, fontweight="bold", color=INK)
        ax.text(cx, base - 0.05, lab, ha="center", va="top", fontsize=8.5, color=INK)
    ax.plot([11.1, 15.2], [base + 0.5 + 4 * u] * 2, ls="--", color=RED, lw=1.8, zorder=4)
    ax.text(15.3, base + 0.5 + 4 * u, "hay que\nsuperarlo", fontsize=8.5, color=RED, va="center")
    ax.text(0.9, 1.6, "Por eso la 1.ª pasada nunca pierde un pesado (no hay falsos negativos).", fontsize=11, color=INK)
    ax.text(0.9, 1.1, "La recíproca no vale: un candidato con k > 0 puede no ser pesado (falso positivo).", fontsize=11, color=INK)
    save_png(fig, "06_teorema.png")


# ================================================== 07 ATAJO vs GENERADORES
def gen_bin(n, rng):
    return [rng.choice("AB") for _ in range(n)]


def gen_5(n, rng):
    return [rng.choice("ABCDE") for _ in range(n)]


def gen_un_pesado(n, rng):
    m = n // 3 + 1
    A = [rng.choice("ABCDE")] * m
    A = A + [rng.choice("ABCDE") for _ in range(n - m)]
    rng.shuffle(A)
    return A


def gen_dos_pesados(n, rng):
    a, b = rng.sample("ABCDE", 2)
    m = n // 3 + 1  # n >= 4  =>  2m <= n
    A = [a] * m + [b] * m + [rng.choice("ABCDE") for _ in range(n - 2 * m)]
    rng.shuffle(A)
    return A


def experimento(trials=6000, seed=7):
    rng = random.Random(seed)
    gens = [("Binario uniforme\n(análogo de la conf. 3)", gen_bin),
            ("5 símbolos uniformes", gen_5),
            ("Un pesado plantado", gen_un_pesado),
            ("Dos pesados plantados", gen_dos_pesados)]
    res = []
    for name, g in gens:
        fallos = 0
        for _ in range(trials):
            A = g(rng.randint(4, 30), rng)
            if atajo(A) != correcto(A):
                fallos += 1
        res.append((name, 100.0 * fallos / trials))
        print(f"  {name.splitlines()[0]:28s} atajo falla en {100.0 * fallos / trials:5.1f}% de los arreglos")
    assert res[-1][1] == 0.0, "el generador de dos pesados plantados debía no atrapar el atajo"
    return res


def fmt(S):
    return "{" + ", ".join(sorted(S)) + "}" if S else "∅"


def fig_atajo():
    res = experimento()
    fig, ax = canvas()
    header(ax, "Última sección", "El atajo (sin 2.ª pasada): ¿qué generador de pruebas lo atrapa?")
    ax.text(0.6, 8.1, "% de arreglos (n entre 4 y 30) donde atajo ≠ respuesta correcta", fontsize=11, color=MUTE)
    y = 7.0
    for name, pct in res:
        l1, *l2 = name.split("\n")
        ax.text(0.6, y + (0.12 if l2 else 0), l1, fontsize=11, fontweight="bold", color=INK, va="center")
        if l2:
            ax.text(0.6, y - 0.28, l2[0], fontsize=8.5, color=MUTE, va="center")
        w = 4.6 * pct / 100.0
        ax.add_patch(Rectangle((5.0, y - 0.3), max(w, 0.04), 0.6, fc=GOOD if pct == 0 else RED, zorder=3, alpha=0.9))
        ax.text(5.0 + max(w, 0.04) + 0.15, y, f"{pct:.1f}%  " + ("no lo atrapa" if pct == 0 else "lo atrapa"),
                fontsize=11, va="center", fontweight="bold", color=GOOD if pct == 0 else RED)
        y -= 1.2
    box(ax, 0.6, 0.55, 10.4, 1.7, fc="white", ec=SOFT, lw=2)
    ax.text(0.85, 1.85, "¿Por qué el último no lo atrapa?", fontsize=11, fontweight="bold", color=INK)
    ax.text(0.85, 1.4, "Hay exactamente 2 pesados → por el teorema ambos están en los 2 casilleros.", fontsize=9.5, color=INK)
    ax.text(0.85, 1.0, "Solo hay 2 casilleros ⇒ ya no cabe ningún falso positivo. Atajo ≡ algoritmo completo.",
            fontsize=9.5, color=INK)

    ax.text(11.6, 8.1, "Contraejemplos mínimos", fontsize=12.5, fontweight="bold", color=INK)
    casos = [list("ABCD"), list("AAB")]
    yy = 6.9
    for A in casos:
        n = len(A)
        s = simulate(A)[-1]
        box(ax, 11.4, yy - 1.45, 6.3, 2.2, fc="white", ec=SOFT, lw=2)
        for q, ch in enumerate(A):
            block(ax, 12.0 + q * 0.9, yy + 0.2, ch, w=0.7, fs=12)
        ax.text(12.0 + n * 0.9 + 0.2, yy + 0.2, f"n = {n},  n/3 = {n / 3:.2f}", fontsize=9.5, va="center", color=MUTE)
        st = "  ".join(f"({c if k else '·'}, {k})" for c, k in ((s["c1"], s["k1"]), (s["c2"], s["k2"])))
        ax.text(11.7, yy - 0.45, "estado final:  " + st, fontsize=10, color=INK, va="center")
        ax.text(11.7, yy - 0.9, f"atajo → {fmt(atajo(A))}", fontsize=11, color=RED, fontweight="bold", va="center")
        ax.text(14.9, yy - 0.9, f"correcto → {fmt(correcto(A))}", fontsize=11, color=GOOD,
                fontweight="bold", va="center")
        yy -= 2.5
    ax.text(11.4, 1.35, "Lección: la hipótesis «si hay pesados» marca qué probar:", fontsize=9.5, color=INK)
    ax.text(11.4, 0.95, "hay que generar arreglos con 0 y con 1 pesado,", fontsize=9.5, color=INK)
    ax.text(11.4, 0.6, "y comparar contra un oráculo que cuente todo.", fontsize=9.5, color=INK)
    save_png(fig, "07_atajo_vs_generadores.png")


# ==================================================================== main ===
if __name__ == "__main__":
    autotest()
    fig_planteamiento()
    fig_cancelacion()
    fig_algoritmo()
    fig_reglas()
    fig_invariante()
    fig_teorema()
    fig_atajo()
    print("Listo. Archivos en:", os.path.abspath(OUT))