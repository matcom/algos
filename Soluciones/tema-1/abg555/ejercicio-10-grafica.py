import importlib
import math
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

par = importlib.import_module("ejercicio-10-par")
closest_pair_grid, closest_pair_sort = par.closest_pair_grid, par.closest_pair_sort

# Figura 1: la rejilla en una dimension, en el paso donde se inserta 26 (delta = 3)
pts = [10, 30, 22, 27, 5]
p, delta = 26, 3
side = delta / 2
fig, ax = plt.subplots(figsize=(10, 2.6))
c = math.floor(p / side)
for k in range(math.floor(3 / side), math.floor(32 / side) + 1):
    en_bloque = c - 2 <= k <= c + 2
    ax.add_patch(Rectangle((k * side, -0.3), side, 0.6, facecolor="#cfe8f3" if en_bloque else "white",
                           edgecolor="#bbbbbb", lw=0.8))
for q in pts:
    ax.plot(q, 0, "o", color="black", markersize=7)
    ax.text(q, 0.45, str(q), ha="center", fontsize=10)
ax.plot(p, 0, "o", color="tab:red", markersize=9)
ax.text(p, -0.75, "26 (el nuevo)", ha="center", fontsize=10, color="tab:red")
ax.annotate("", xy=(p + delta, -0.45), xytext=(p - delta, -0.45),
            arrowprops=dict(arrowstyle="<->", color="tab:red"))
ax.text(p, -1.15, "lo que esta a menos de delta = 3 cae en el bloque de 5 celdas (azul)", ha="center",
        fontsize=9)
ax.set_xlim(2, 33)
ax.set_ylim(-1.4, 0.9)
ax.set_yticks([])
ax.set_title("Celdas de largo delta/2 = 1.5: cada celda tiene a lo sumo un punto", fontsize=10)
for s in ["left", "right", "top"]:
    ax.spines[s].set_visible(False)
plt.tight_layout()
plt.savefig("ejercicio-10-rejilla.png", dpi=120)

# Figura 2: trabajo por punto (rejilla contra ordenar) y reconstrucciones (barajando o no)
rng = random.Random(5)
ns = [2 ** k for k in range(8, 18)]
rejilla, ordenar = [], []
for n in ns:
    xs = [rng.random() for _ in range(n)]
    stats = {}
    closest_pair_grid(xs, stats=stats)
    rejilla.append((stats["lookups"] + stats["rebuilt_points"]) / n)
    ordenar.append(math.log2(n))               # mergesort hace unas log2 n comparaciones por elemento

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4))
a1.plot(ns, ordenar, "o-", color="tab:orange", label="ordenar: ~log2 n comparaciones por punto")
a1.plot(ns, rejilla, "o-", color="tab:blue", label="rejilla: operaciones por punto (medido)")
a1.set_xscale("log", base=2)
a1.set_xlabel("n")
a1.set_ylabel("trabajo por punto")
a1.set_title("La rejilla hace trabajo constante por punto")
a1.legend(fontsize=9)
a1.grid(alpha=0.3)

ms = list(range(5, 45, 5))
sin, con = [], []
for n in ms:
    xs = [1 - 2 ** -k for k in range(n)]
    s1 = {}
    closest_pair_grid(xs, shuffle=False, stats=s1)
    sin.append(s1["rebuilds"])
    total = 0
    for s in range(50):
        s2 = {}
        closest_pair_grid(xs, seed=s, stats=s2)
        total += s2["rebuilds"]
    con.append(total / 50)
a2.plot(ms, sin, "o-", color="tab:red", label="insertados en orden (sin barajar)")
a2.plot(ms, con, "o-", color="tab:blue", label="barajados (promedio de 50)")
a2.plot(ms, [2 * math.log(n) for n in ms], "--", color="gray", label="2 ln n")
a2.set_xlabel("n  (puntos 1 - 2^-k)")
a2.set_ylabel("reconstrucciones")
a2.set_title("Sin barajar, la peor entrada reconstruye siempre")
a2.legend(fontsize=9)
a2.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("ejercicio-10-costo.png", dpi=120)
