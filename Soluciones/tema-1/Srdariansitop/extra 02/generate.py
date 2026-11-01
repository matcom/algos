import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch, Rectangle
from bisect import bisect_left
from PIL import Image
import io

# ===============================================================
# CONSTANTES Y COLORES UNIFICADOS
# ===============================================================
C_INT = "#90caf9"      # Nodo interno / Zona [lo, hi)
C_HOJA = "#ffcc80"     # Hoja / Respuesta / Zona descartada der
C_RUTA = "#d32f2f"     # Camino resaltado / Color de 'm'
C_BORDE = "#455a64"    # Color de bordes genérico
C_GRIS = "#78909c"

# Colores específicos de la Parte 2 (Traza y GIF)
C_IZQ = "#cfd8dc"      # A[i] < x -> descartado
C_CAND = C_INT         # Zona [lo, hi)
C_RESP = "#a5d6a7"     # Índice hi -> A[hi] >= x
C_DER = C_HOJA         # A[i] >= x con i > hi
C_M = C_RUTA


# ===============================================================
# PARTE 1: ÁRBOL DE DECISIÓN Y COTA DE INFORMACIÓN (FIGURAS 3 Y 4)
# ===============================================================

def construir(lo, hi, prof=0):
    if lo == hi:
        return {"leaf": True, "ans": lo, "lo": lo, "hi": hi, "d": prof}
    m = lo + (hi - lo) // 2
    return {
        "leaf": False, "m": m, "lo": lo, "hi": hi, "d": prof,
        "no": construir(lo, m, prof + 1),        # A[m] >= x  -> hi = m
        "si": construir(m + 1, hi, prof + 1),    # A[m] <  x  -> lo = m+1
    }


def posiciones(nodo, cont):
    """Hojas en orden de respuesta 0..n (izquierda->derecha)."""
    if nodo["leaf"]:
        nodo["x"] = cont[0]
        cont[0] += 1
    else:
        posiciones(nodo["no"], cont)
        posiciones(nodo["si"], cont)
        nodo["x"] = (nodo["no"]["x"] + nodo["si"]["x"]) / 2


def altura(nodo):
    return nodo["d"] if nodo["leaf"] else max(altura(nodo["no"]), altura(nodo["si"]))


def en_ruta(nodo, ans):
    return ans is not None and nodo["lo"] <= ans <= nodo["hi"]


def dibujar_arbol(ax, raiz, ans=None, fs=11):
    DY = 1.5

    def rec(nodo):
        if nodo["leaf"]:
            return
        for lado, etiqueta in (("no", "no (A[m] ≥ x)"), ("si", "sí (A[m] < x)")):
            h = nodo[lado]
            ruta = en_ruta(nodo, ans) and en_ruta(h, ans)
            ax.plot([nodo["x"], h["x"]], [-nodo["d"] * DY, -h["d"] * DY],
                    color=C_RUTA if ruta else C_GRIS, lw=3.2 if ruta else 1.4,
                    zorder=1)
            xm = (nodo["x"] + h["x"]) / 2
            ym = (-nodo["d"] * DY - h["d"] * DY) / 2
            ax.text(xm, ym + 0.12, "no" if lado == "no" else "sí", fontsize=fs - 1,
                    ha="center", va="bottom", color=C_RUTA if ruta else C_GRIS,
                    fontweight="bold" if ruta else "normal",
                    bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"), zorder=2)
            rec(h)

    rec(raiz)

    def nodos(nodo):
        ruta = en_ruta(nodo, ans)
        if nodo["leaf"]:
            ax.text(nodo["x"], -nodo["d"] * DY, f"resp.\n{nodo['ans']}", ha="center", va="center",
                    fontsize=fs, fontweight="bold",
                    bbox=dict(boxstyle="round,pad=0.35", fc=C_HOJA,
                              ec=C_RUTA if ruta else C_BORDE, lw=3 if ruta else 1.2), zorder=3)
        else:
            ax.text(nodo["x"], -nodo["d"] * DY, f"A[{nodo['m']}] < x ?", ha="center", va="center",
                    fontsize=fs,
                    bbox=dict(boxstyle="round,pad=0.4", fc=C_INT,
                              ec=C_RUTA if ruta else C_BORDE, lw=3 if ruta else 1.2), zorder=3)
            nodos(nodo["no"])
            nodos(nodo["si"])

    nodos(raiz)


def hojas(nodo):
    return 1 if nodo["leaf"] else hojas(nodo["no"]) + hojas(nodo["si"])


# --- Figura 3: Árboles de decisión ---
fig, axs = plt.subplots(1, 2, figsize=(17, 6.6), gridspec_kw={"width_ratios": [4, 11]})
casos = [(3, None, "n = 3  →  n+1 = 4 hojas, altura h = 2 = ⌈log₂ 4⌉"),
         (10, 5, "n = 10  →  n+1 = 11 hojas, altura h = 4 = ⌈log₂ 11⌉\n(camino de x = 23 resaltado: devuelve 5 con 3 comparaciones)")]

for ax, (n_cas, ans, titulo) in zip(axs, casos):
    raiz = construir(0, n_cas)
    posiciones(raiz, [0])
    h = altura(raiz)
    assert hojas(raiz) == n_cas + 1
    assert h == math.ceil(math.log2(n_cas + 1))
    dibujar_arbol(ax, raiz, ans)
    ax.set_title(titulo, fontsize=13, fontweight="bold")
    ax.set_xlim(-0.8, n_cas + 0.8)
    ax.set_ylim(-h * 1.5 - 0.9, 0.9)
    ax.axis("off")

fig.suptitle("Árbol de decisión de la búsqueda binaria: cada comparación tiene 2 salidas, cada hoja es una respuesta 0..n",
             fontsize=14, fontweight="bold")
fig.legend(handles=[Patch(fc=C_INT, ec=C_BORDE, label="nodo interno = una comparación A[m] vs x"),
                    Patch(fc=C_HOJA, ec=C_BORDE, label="hoja = respuesta (primer índice con A[i] ≥ x)")],
           loc="lower center", ncol=2, frameon=False, fontsize=11)
fig.tight_layout(rect=(0, 0.05, 1, 0.94))
fig.savefig("fig3_arbol_decision.png", dpi=150, facecolor="white")
plt.close(fig)
print("-> Generado: fig3_arbol_decision.png")


# --- Figura 4: La cota de información ---
def peor_caso(n_val):
    A_v = list(range(0, 2 * n_val, 2))
    peor = 0
    for x_v in range(-1, 2 * n_val + 1):
        lo_v, hi_v, it = 0, n_val, 0
        while lo_v < hi_v:
            m_v = lo_v + (hi_v - lo_v) // 2
            if A_v[m_v] < x_v:
                lo_v = m_v + 1
            else:
                hi_v = m_v
            it += 1
        peor = max(peor, it)
    return peor

ns = list(range(1, 65))
medido = [peor_caso(n_v) for n_v in ns]
cota = [math.ceil(math.log2(n_v + 1)) for n_v in ns]
assert medido == cota

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5.6), gridspec_kw={"width_ratios": [5, 6]})

n0 = 10
hs = list(range(0, 6))
cap = [2 ** h for h in hs]
colores = [C_RUTA if c >= n0 + 1 and (h == 0 or 2 ** (h - 1) < n0 + 1) else (C_INT if c >= n0 + 1 else "#cfd8dc")
           for h, c in zip(hs, cap)]
ax1.bar(hs, cap, color=colores, edgecolor=C_BORDE)
for h, c in zip(hs, cap):
    ax1.text(h, c + 0.6, str(c), ha="center", fontsize=11)
ax1.axhline(n0 + 1, color="#1b5e20", ls="--", lw=2)
ax1.text(-0.4, n0 + 1.9, f"n + 1 = {n0 + 1} respuestas posibles", color="#1b5e20", fontsize=11, fontweight="bold")
ax1.set_xlabel("altura h del árbol (nº de comparaciones en el peor caso)", fontsize=11)
ax1.set_ylabel("hojas posibles: 2^h", fontsize=11)
ax1.set_xticks(hs)
ax1.set_title(f"Con h ≤ 3 no caben {n0 + 1} hojas (2³ = 8);\nel menor h con 2^h ≥ {n0 + 1} es h = 4", fontsize=12, fontweight="bold")
ax1.spines[["top", "right"]].set_visible(False)
ax1.set_ylim(0, 38)

xs = [n_v / 10 for n_v in range(10, 650)]
ax2.plot([n_v for n_v in xs], [math.log2(n_v + 1) for n_v in xs], ls="--", color=C_GRIS, lw=1.8,
         label="log₂(n+1)  (bits de información necesarios)")
ax2.step(ns, cota, where="post", color=C_RUTA, lw=2.6, label="cota inferior ⌈log₂(n+1)⌉ (cualquier algoritmo)")
ax2.plot(ns, medido, "o", ms=5.5, color="#1565c0", mfc="white", mew=1.8,
         label="peor caso medido de la búsqueda binaria")
ax2.set_xlabel("n (tamaño del arreglo)", fontsize=11)
ax2.set_ylabel("comparaciones en el peor caso", fontsize=11)
ax2.set_title("La búsqueda binaria toca la cota inferior en todo n (1 ≤ n ≤ 64)", fontsize=12, fontweight="bold")
ax2.legend(loc="lower right", fontsize=10, frameon=False)
ax2.grid(alpha=0.25)
ax2.spines[["top", "right"]].set_visible(False)
ax2.set_xlim(0, 65)
ax2.set_ylim(0, 7.5)

fig.suptitle("Cota de información: n+1 respuestas ⇒ al menos ⌈log₂(n+1)⌉ comparaciones de 1 bit", fontsize=14, fontweight="bold")
fig.tight_layout(rect=(0, 0, 1, 0.93))
fig.savefig("fig4_cota_informacion.png", dpi=150, facecolor="white")
plt.close(fig)
print("-> Generado: fig4_cota_informacion.png")


# ===============================================================
# PARTE 2: TRAZA DE BÚSQUEDA Y GIF (FIGURAS 1 Y 2)
# ===============================================================

A = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
x = 23
n = len(A)
RESP = bisect_left(A, x)


def trace():
    lo, hi = 0, n
    pasos = []
    while lo < hi:
        assert lo <= RESP <= hi
        m = lo + (hi - lo) // 2
        pasos.append((lo, hi, m))
        if A[m] < x:
            lo = m + 1
        else:
            hi = m
    assert lo == hi == RESP
    return pasos, (lo, hi)


def dibujar_traza(ax, lo, hi, m=None, y=0.0):
    for i in range(n + 1):
        if i < lo:
            c = C_IZQ
        elif i < hi:
            c = C_CAND
        elif i == hi:
            c = C_RESP
        else:
            c = C_DER
        centinela = (i == n)
        ax.add_patch(Rectangle((i, y), 1, 1, facecolor=c, edgecolor=C_BORDE, lw=1.2,
                               ls="--" if centinela else "-"))
        ax.text(i + 0.5, y + 0.5, "∞" if centinela else str(A[i]), ha="center", va="center",
                fontsize=15 if centinela else 13, color="#546e7a" if centinela else "black")
        ax.text(i + 0.5, y - 0.22, str(i), ha="center", va="center", fontsize=9, color="#546e7a")
    if m is not None:
        assert lo <= m < hi
        ax.add_patch(Rectangle((m, y), 1, 1, facecolor="none", edgecolor=C_M, lw=3.5))
        ax.annotate("m", xy=(m + 0.5, y + 1), xytext=(m + 0.5, y + 1.55),
                    ha="center", fontsize=13, color=C_M, fontweight="bold",
                    arrowprops=dict(arrowstyle="->", color=C_M, lw=2))
    ax.plot([lo, lo], [y - 0.05, y + 1.05], color="#1565c0", lw=3)
    ax.plot([hi, hi], [y - 0.05, y + 1.05], color="#e65100", lw=3, ls="--")
    if lo == hi:
        ax.text(lo, y + 1.22, "lo = hi", ha="center", color="#37474f", fontsize=12, fontweight="bold")
    else:
        ax.text(lo, y + 1.22, "lo", ha="center", color="#1565c0", fontsize=12, fontweight="bold")
        ax.text(hi, y + 1.22, "hi", ha="center", color="#e65100", fontsize=12, fontweight="bold")


def leyenda_traza(ax, y_pos):
    h = [Patch(facecolor=C_IZQ, edgecolor=C_BORDE, label="A[i] < x  (descartado)"),
         Patch(facecolor=C_CAND, edgecolor=C_BORDE, label="[lo, hi): aquí cae m"),
         Patch(facecolor=C_RESP, edgecolor=C_BORDE, label="índice hi: A[hi] ≥ x, puede ser la respuesta"),
         Patch(facecolor=C_DER, edgecolor=C_BORDE, label="i > hi  (descartado)")]
    ax.legend(handles=h, loc="upper center", bbox_to_anchor=(0.5, y_pos), ncol=4, frameon=False,
              fontsize=9, columnspacing=1.2, handlelength=1.4)


# --- Figura 1: Traza completa ---
pasos, (lo_f, hi_f) = trace()
filas = len(pasos) + 1
fig, ax = plt.subplots(figsize=(12, 2.3 * filas + 1.2))
ax.set_xlim(-2.6, n + 6.2)
ax.set_ylim(-(filas - 1) * 2.3 - 0.8, 2.6)
ax.axis("off")
ax.set_title(f"Búsqueda binaria: A = {A}, x = {x}  →  la respuesta (índice {RESP}) siempre está en [lo, hi]",
             fontsize=13, fontweight="bold")

for k, (lo, hi, m) in enumerate(pasos):
    y_pos = -k * 2.3
    dibujar_traza(ax, lo, hi, m, y_pos)
    accion = "hi ← m" if A[m] >= x else "lo ← m+1"
    cmp_ = "≥" if A[m] >= x else "<"
    ax.text(-0.3, y_pos + 0.5, f"Iter {k}", ha="right", va="center", fontsize=11, fontweight="bold")
    ax.text(n + 1.3, y_pos + 0.88, f"Φ = hi−lo = {hi - lo}", va="center", fontsize=11)
    ax.text(n + 1.3, y_pos + 0.52, f"A[{m}]={A[m]} {cmp_} {x}  →  {accion}", va="center", fontsize=10)
    ax.text(n + 1.3, y_pos + 0.16, f"respuesta ∈ [lo, hi] = [{lo}, {hi}]", va="center", fontsize=10,
            color="#2e7d32", fontweight="bold")

y_pos = -len(pasos) * 2.3
dibujar_traza(ax, lo_f, hi_f, None, y_pos)
ax.text(-0.3, y_pos + 0.5, "Fin", ha="right", va="center", fontsize=11, fontweight="bold")
ax.text(n + 1.3, y_pos + 0.88, "Φ = 0", va="center", fontsize=11)
ax.text(n + 1.3, y_pos + 0.52, f"lo = hi = {lo_f}  →  A[{lo_f}] = {A[lo_f]} = x ✓", va="center", fontsize=10)
ax.text(n + 1.3, y_pos + 0.16, f"respuesta ∈ [lo, hi] = [{lo_f}, {hi_f}]", va="center", fontsize=10,
        color="#2e7d32", fontweight="bold")
leyenda_traza(ax, 0.0)
fig.savefig("fig1_traza_busqueda_binaria.png", dpi=150, bbox_inches="tight", facecolor="white")
plt.close(fig)
print("-> Generado: fig1_traza_busqueda_binaria.png")


# --- Figura 2: GIF animado de las zonas ---
def frame(lo, hi, m, titulo, nota, phi):
    fig_f, ax_f = plt.subplots(figsize=(11, 3.8))
    ax_f.set_xlim(-0.5, n + 1.5)
    ax_f.set_ylim(-1.1, 3.0)
    ax_f.axis("off")
    ax_f.set_title(titulo, fontsize=14, fontweight="bold")
    dibujar_traza(ax_f, lo, hi, m, 0.8)
    ax_f.text((n + 1) / 2, 0.15, nota, ha="center", va="center", fontsize=12)
    ax_f.text((n + 1) / 2, -0.35,
              f"Φ = hi − lo = {phi}     ·     la respuesta está en [lo, hi] = [{lo}, {hi}]",
              ha="center", va="center", fontsize=12, color="#2e7d32", fontweight="bold")
    leyenda_traza(ax_f, 0.02)
    buf = io.BytesIO()
    fig_f.savefig(buf, format="png", dpi=90, facecolor="white")
    plt.close(fig_f)
    buf.seek(0)
    return Image.open(buf).convert("RGB")


frames, dur = [], []
lo, hi = 0, n
frames.append(frame(lo, hi, None, f"Inicio: buscamos x = {x}",
                    "lo = 0, hi = 10  (hi = 10 significaría \"ningún elemento es ≥ x\")", hi - lo))
dur.append(2200)

it = 0
while lo < hi:
    m = lo + (hi - lo) // 2
    frames.append(frame(lo, hi, m, f"Iteración {it}: m cae dentro de [lo, hi)",
                        f"m = lo + ⌊(hi−lo)/2⌋ = {m}   y   lo={lo} ≤ m={m} < hi={hi}  ✓", hi - lo))
    dur.append(1800)
    if A[m] < x:
        txt = f"A[{m}] = {A[m]} < {x}  →  lo ← m+1 = {m + 1}"
        nlo, nhi = m + 1, hi
    else:
        txt = f"A[{m}] = {A[m]} ≥ {x}  →  hi ← m = {m}   (A[{m}] ≥ x: ahora {m} es el candidato verde)"
        nlo, nhi = lo, m
    frames.append(frame(lo, hi, m, f"Iteración {it}: comparamos A[m] con x", txt, hi - lo))
    dur.append(2200)
    lo, hi = nlo, nhi
    it += 1

frames.append(frame(lo, hi, None, "Fin: lo = hi", f"Devuelve {lo}: A[{lo}] = {A[lo]} = x  ✓   (Φ = 0)", 0))
dur.append(3000)

frames[0].save("fig2_zonas_busqueda_binaria.gif", save_all=True, append_images=frames[1:],
               duration=dur, loop=0, optimize=True)
print(f"-> Generado: fig2_zonas_busqueda_binaria.gif ({len(frames)} frames)")

print("\n¡Listo! Se han creado los 4 archivos en la misma carpeta:")
print(" - fig1_traza_busqueda_binaria.png")
print(" - fig2_zonas_busqueda_binaria.gif")
print(" - fig3_arbol_decision.png")
print(" - fig4_cota_informacion.png")