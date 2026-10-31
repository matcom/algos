import importlib
import math
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

md = importlib.import_module("ejercicio-07-mediana")
median_two = md.median_two

# Figura 1: el corte valido en el ejemplo
A = [1, 3, 8, 9, 15]
B = [7, 11, 18, 19, 21]
n = len(A)
i, j = 4, 1                                    # el corte que encuentra el algoritmo
fig, ax = plt.subplots(figsize=(8, 3.3))
for fila, (nombre, arr, corte, y) in enumerate([("A", A, i, 1.3), ("B", B, j, 0)]):
    ax.text(-0.6, y + 0.4, nombre, ha="center", va="center", fontsize=13)
    for k, v in enumerate(arr):
        color = "#cfe8f3" if k < corte else "white"
        ax.add_patch(Rectangle((k, y), 0.9, 0.8, facecolor=color, edgecolor="black"))
        ax.text(k + 0.45, y + 0.4, str(v), ha="center", va="center", fontsize=12)
    ax.plot([corte - 0.05] * 2, [y - 0.15, y + 0.95], color="tab:red", lw=2.5)
ax.text(5.6, 1.7, "i = 4 de A", fontsize=10, color="tab:red")
ax.text(5.6, 0.4, "j = 1 de B", fontsize=10, color="tab:red")
ax.text(2.5, -0.65, "azul: los n = 5 menores.  A[i-1] = 9 <= B[j] = 11  y  B[j-1] = 7 <= A[i] = 15.  "
        "Mediana = max(9, 7) = 9", ha="center", fontsize=9)
ax.set_xlim(-1, 7.5)
ax.set_ylim(-0.9, 2.3)
ax.axis("off")
plt.tight_layout()
plt.savefig("ejercicio-07-corte.png", dpi=120)

# Figura 2: comparaciones segun n
rng = random.Random(5)
ns = [2 ** k for k in range(0, 18)]
medido = []
for n in ns:
    peor = 0
    for _ in range(40):
        A = sorted(rng.randint(0, 10 * n) for _ in range(n))
        B = sorted(rng.randint(0, 10 * n) for _ in range(n))
        stats = {}
        median_two(A, B, stats=stats)
        peor = max(peor, stats["comparisons"])
    medido.append(peor)
plt.figure(figsize=(7.5, 4.2))
plt.plot(ns, medido, "o-", label="algoritmo, peor caso medido")
plt.plot(ns, [2 * (math.floor(math.log2(n + 1)) + 1) for n in ns], "--", color="tab:blue",
         label="tope del potencial: 2 (floor(log2(n+1)) + 1)")
plt.plot(ns, [math.ceil(math.log2(2 * n)) for n in ns], color="tab:red",
         label="cota de informacion: ceil(log2 2n)")
plt.xscale("log", base=2)
plt.xlabel("n")
plt.ylabel("comparaciones")
plt.title("El algoritmo y la cota crecen los dos como log n")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("ejercicio-07-costo.png", dpi=120)
