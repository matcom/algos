import importlib
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

mz = importlib.import_module("ejercicio-06-matriz")
search_matrix, Adversary = mz.search_matrix, mz.Adversary

# Figura 1: el camino de la escalera en el ejemplo de 4 x 4, buscando 6 y 15
M = [[1, 4, 7, 11],
     [2, 5, 8, 12],
     [3, 6, 9, 16],
     [10, 13, 14, 17]]
fig, axes = plt.subplots(1, 2, figsize=(9, 4.3))
for ax, x in zip(axes, [6, 15]):
    trace = []
    r = search_matrix(M, x, trace)
    vistos = set(trace)
    for i in range(4):
        for j in range(4):
            color = "white"
            if (i, j) in vistos:
                color = "#cfe8f3"
            if r == (i, j):
                color = "#b8e0b8"
            ax.add_patch(Rectangle((j, -i), 1, 1, facecolor=color, edgecolor="black"))
            ax.text(j + 0.5, -i + 0.5, str(M[i][j]), ha="center", va="center", fontsize=12)
    for (i1, j1), (i2, j2) in zip(trace, trace[1:]):
        ax.annotate("", xy=(j2 + 0.5, -i2 + 0.5), xytext=(j1 + 0.5, -i1 + 0.5),
                    arrowprops=dict(arrowstyle="->", color="tab:red", lw=1.5))
    resultado = "esta" if r else "no esta"
    ax.set_title(f"x = {x}: {len(trace)} comparaciones, {resultado}")
    ax.set_xlim(-0.1, 4.1)
    ax.set_ylim(-3.1, 1.1)
    ax.set_aspect("equal")
    ax.axis("off")
plt.suptitle("La escalera empieza arriba a la derecha y en cada paso descarta una fila o una columna")
plt.tight_layout()
plt.savefig("ejercicio-06-escalera.png", dpi=120)

# Figura 2: la matriz del adversario para n = 6
n = 6
A = Adversary(n)
Madv = A.matrix()
fig, ax = plt.subplots(figsize=(5, 5))
for i in range(n):
    for j in range(n):
        if i + j < n - 1:
            color, txt = "#e8e8e8", "-1"
        elif i + j > n - 1:
            color, txt = "#f6d7a7", "+1"
        else:
            color, txt = "#f6c9c9", "?"
        ax.add_patch(Rectangle((j, -i), 1, 1, facecolor=color, edgecolor="black"))
        ax.text(j + 0.5, -i + 0.5, txt, ha="center", va="center", fontsize=13)
ax.set_title("x = 0. Gris: menor que x. Naranja: mayor.\nRojo: la antidiagonal, cada celda puede ser -1 o 0",
             fontsize=10)
ax.set_xlim(-0.1, n + 0.1)
ax.set_ylim(-n + 0.9, 1.1)
ax.set_aspect("equal")
ax.axis("off")
plt.tight_layout()
plt.savefig("ejercicio-06-adversario.png", dpi=120)

# Figura 3: comparaciones segun n
ns = [2 ** k for k in range(1, 12)]
plt.figure(figsize=(7.5, 4.2))
plt.plot(ns, [n * n for n in ns], "o-", color="gray", label="mirar todas las celdas: n²")
plt.plot(ns, [n * math.ceil(math.log2(n + 1)) for n in ns], "o-", color="tab:orange",
         label="busqueda binaria en cada fila: n log n")
plt.plot(ns, [2 * n - 1 for n in ns], "o-", color="tab:blue", label="escalera, peor caso: 2n - 1")
plt.plot(ns, ns, "--", color="tab:red", label="cota minima del adversario: n")
plt.xscale("log", base=2)
plt.yscale("log")
plt.xlabel("n")
plt.ylabel("comparaciones")
plt.title("La escalera y la cota minima son las dos lineales")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("ejercicio-06-costo.png", dpi=120)
