import importlib
import math
import matplotlib.pyplot as plt

pk = importlib.import_module("ejercicio-14-pico")
peak_binary, unimodal = pk.peak_binary, pk.unimodal

# Figura 1: el arreglo del ejemplo y el rango [lo, hi] en cada vuelta
A = [1, 4, 9, 12, 15, 11, 7, 2]
trace = []
peak_binary(A, trace)
fig, axes = plt.subplots(1, len(trace), figsize=(12, 3.2), sharey=True)
for t, (ax, (lo, hi)) in enumerate(zip(axes, trace)):
    colores = ["tab:blue" if lo <= i <= hi else "#dddddd" for i in range(len(A))]
    ax.bar(range(len(A)), A, color=colores)
    if lo < hi:
        m = (lo + hi) // 2
        ax.bar([m, m + 1], [A[m], A[m + 1]], color="none", edgecolor="tab:red", lw=2)
        ax.set_title(f"vuelta {t}: [{lo}, {hi}], compara {m} y {m + 1}", fontsize=9)
    else:
        ax.set_title(f"termina: el pico es {lo}", fontsize=9)
    ax.set_xticks(range(len(A)))
axes[0].set_ylabel("valor")
plt.suptitle("Azul: donde todavia puede estar el pico.  Rojo: los dos vecinos que se comparan", fontsize=10)
plt.tight_layout()
plt.savefig("ejercicio-14-traza.png", dpi=120)

# Figura 2: el arbol de decision para n = 8 y el peor caso segun n
fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 4.2), gridspec_kw={"width_ratios": [1.3, 1]})


def dibujar(lo, hi, x, y, ancho):
    if lo == hi:
        a1.add_patch(plt.Rectangle((x - 0.45, y - 0.3), 0.9, 0.6, facecolor="#cfe8f3", edgecolor="black"))
        a1.text(x, y, f"p = {lo}", ha="center", va="center", fontsize=9)
        return
    m = (lo + hi) // 2
    a1.add_patch(plt.Rectangle((x - 0.8, y - 0.3), 1.6, 0.6, facecolor="white", edgecolor="black"))
    a1.text(x, y, f"A[{m}] < A[{m + 1}]?", ha="center", va="center", fontsize=8)
    for hlo, hhi, dx, txt in [(lo, m, -ancho, "no"), (m + 1, hi, ancho, "si")]:
        a1.plot([x, x + dx], [y - 0.3, y - 1.2], color="gray", lw=0.8)
        a1.text(x + dx / 2 + (-0.3 if dx < 0 else 0.3), y - 0.75, txt, fontsize=8, color="gray", ha="center")
        dibujar(hlo, hhi, x + dx, y - 1.5, ancho / 2)


dibujar(0, 7, 0, 0, 4)
a1.set_xlim(-8.5, 8.5)
a1.set_ylim(-5.2, 0.6)
a1.axis("off")
a1.set_title("n = 8: 8 posiciones posibles = 8 hojas, altura 3", fontsize=10)

ns = list(range(1, 130))
peor = []
for n in ns:
    w = 0
    for p in range(n):
        stats = {}
        peak_binary(unimodal(n, p), stats=stats)
        w = max(w, stats.get("comparisons", 0))
    peor.append(w)
a2.plot(ns, peor, "o", markersize=4, label="busqueda binaria, peor caso medido")
a2.step(ns, [math.ceil(math.log2(n)) for n in ns], where="mid", color="tab:red",
        label="cota de informacion  ceil(log2 n)")
a2.set_xlabel("n")
a2.set_ylabel("comparaciones")
a2.set_title("El algoritmo alcanza la cota en todos los n", fontsize=10)
a2.legend(fontsize=9)
a2.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("ejercicio-14-arbol.png", dpi=120)
