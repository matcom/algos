import importlib
import math
import matplotlib.pyplot as plt

bs = importlib.import_module("ejercicio-02-busqueda")
binary_search, comparisons = bs.binary_search, bs.comparisons

# Figura 1: el potencial hi - lo en una busqueda sobre 100 elementos
A = list(range(0, 200, 2))
trace = []
binary_search(A, 77, trace)                    # 77 no esta: el peor caso
pot = [hi - lo for lo, hi in trace]
plt.figure(figsize=(7, 3.8))
barras = plt.bar(range(len(pot)), pot, color="tab:blue")
for b, p in zip(barras, pot):
    plt.text(b.get_x() + b.get_width() / 2, p + 1.5, str(p), ha="center")
plt.xlabel("vuelta")
plt.ylabel("potencial  hi - lo")
plt.title("n = 100, x = 77 (no esta): el potencial baja a la mitad en cada vuelta")
plt.tight_layout()
plt.savefig("ejercicio-02-potencial.png", dpi=120)

# Figura 2: el arbol de decision para n = 7, corriendo la busqueda con un valor
# de cada hueco (como la figura 7 de la conferencia 5)
A = [10, 20, 30, 40, 50, 60, 70]
fig, ax = plt.subplots(figsize=(10, 4.2))
pos = {}


def dibujar(lo, hi, x, y, ancho):
    # cada nodo es una vuelta con rango [lo, hi); una hoja es un hueco
    if lo >= hi:
        ax.add_patch(plt.Rectangle((x - 0.45, y - 0.3), 0.9, 0.6, facecolor="#cfe8f3",
                                   edgecolor="black"))
        ax.text(x, y, f"h{lo}", ha="center", va="center", fontsize=10)
        return
    m = (lo + hi) // 2
    ax.add_patch(plt.Rectangle((x - 0.7, y - 0.3), 1.4, 0.6, facecolor="white",
                               edgecolor="black"))
    ax.text(x, y, f"x vs a{m + 1}", ha="center", va="center", fontsize=9)
    for hijo_lo, hijo_hi, dx, txt in [(lo, m, -ancho, "<"), (m + 1, hi, ancho, ">")]:
        ax.plot([x, x + dx], [y - 0.3, y - 1.2], color="gray", lw=0.8)
        ax.text(x + dx / 2 + (-0.25 if dx < 0 else 0.25), y - 0.75, txt, fontsize=9,
                color="gray", ha="center")
        dibujar(hijo_lo, hijo_hi, x + dx, y - 1.5, ancho / 2)


dibujar(0, 7, 0, 0, 4)
ax.text(0, -6.3, "8 huecos = 8 hojas en las ramas < y >, altura 3 = ceil(log2 8)",
        ha="center", fontsize=10)
ax.set_xlim(-8.5, 8.5)
ax.set_ylim(-6.7, 0.6)
ax.axis("off")
plt.tight_layout()
plt.savefig("ejercicio-02-arbol.png", dpi=120)

# Figura 3: peor caso medido contra la cota de informacion y la busqueda lineal
ns = list(range(1, 130))
peor, cota = [], []
for n in ns:
    A = list(range(0, 2 * n, 2))
    peor.append(max(comparisons(A, x) for x in range(-1, 2 * n + 1)))
    cota.append(math.ceil(math.log2(n + 1)))
plt.figure(figsize=(7.5, 4))
plt.plot(ns, peor, "o", markersize=4, label="busqueda binaria, peor caso medido")
plt.step(ns, cota, where="mid", color="tab:red", label="cota de informacion  ceil(log2(n+1))")
plt.xlabel("n")
plt.ylabel("comparaciones")
plt.title("El peor caso coincide con la cota en todos los n")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("ejercicio-02-peor_caso.png", dpi=120)
