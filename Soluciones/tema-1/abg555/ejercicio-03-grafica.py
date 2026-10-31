import importlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

pila = importlib.import_module("ejercicio-03-pila")
MinStack, NormalStack = pila.MinStack, pila.NormalStack

# Figura 1: la traza del ejemplo. Cada columna es la pila despues de una
traza = [("push 5", 5), ("push 3", 3), ("push 7", 7), ("push 1", 1),
         ("pop", None), ("pop", None), ("pop", None),
         ("push 6", 6)]

fig, ax = plt.subplots(figsize=(11, 4.2))
p = MinStack()
for col, (nombre, x) in enumerate(traza):
    p.push(x) if x is not None else p.pop()
    nodos = list(p.nodes())[::-1]              # de abajo hacia arriba
    for fila, node in enumerate(nodos):
        cima = fila == len(nodos) - 1
        ax.add_patch(Rectangle((col * 1.4, fila), 1.1, 0.9,
                               facecolor="#cfe8f3" if cima else "white",
                               edgecolor="black"))
        ax.text(col * 1.4 + 0.3, fila + 0.45, str(node.value), ha="center", va="center",
                fontsize=12)
        ax.text(col * 1.4 + 0.8, fila + 0.45, str(node.min), ha="center", va="center",
                fontsize=12, color="tab:red")
        ax.plot([col * 1.4 + 0.55] * 2, [fila, fila + 0.9], color="gray", lw=0.8)
    ax.text(col * 1.4 + 0.55, -0.45, nombre, ha="center", fontsize=10)
    ax.text(col * 1.4 + 0.55, 4.35, f"min = {p.minimo()}", ha="center",
            fontsize=10, color="tab:red")
ax.set_xlim(-0.3, len(traza) * 1.4)
ax.set_ylim(-0.8, 4.8)
ax.axis("off")
ax.set_title("Cada caja: valor (negro) | minimo de ahi para abajo (rojo). "
             "La cima esta en azul.", fontsize=10)
plt.tight_layout()
plt.savefig("ejercicio-03-traza.png", dpi=120)

# Figura 2: comparaciones totales para hacer n veces "push y pedir el minimo"
ns = [10, 30, 100, 300, 1000, 3000]
con_min, normal = [], []
for n in ns:
    p, q = MinStack(), NormalStack()
    for x in range(n):
        p.push(x)
        p.minimo()
        q.push(x)
        q.minimo()
    con_min.append(max(p.comparisons, 1))     # max(.., 1) para el eje log
    normal.append(q.comparisons)

plt.figure(figsize=(7, 4.2))
plt.plot(ns, normal, "o-", color="tab:red", label="pila normal (recorre todo)")
plt.plot(ns, con_min, "o-", color="tab:blue", label="pila con minimo guardado")
plt.xscale("log")
plt.yscale("log")
plt.xlabel("n (operaciones de push + minimo)")
plt.ylabel("comparaciones en total")
plt.title("La pila normal crece como n²/2, la del mínimo guardado como n")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("ejercicio-03-costo.png", dpi=120)

# Figura 3: cuanto falla la version con < segun las pruebas (de la prueba 6)
nombres = ["reales\ndistintos", "enteros\n0..1000", "enteros\n0..9", "solo\n0 y 1"]
con_menor_igual = [0.0, 0.0, 0.0, 0.0]
con_menor = [0.0, 0.9, 56.1, 86.2]
pos = range(len(nombres))

plt.figure(figsize=(7, 4.2))
plt.bar([i - 0.2 for i in pos], con_menor_igual, width=0.4, label="con <=",
        color="tab:blue")
barras = plt.bar([i + 0.2 for i in pos], con_menor, width=0.4, label="con <",
                 color="tab:orange")
for b, v in zip(barras, con_menor):
    plt.text(b.get_x() + b.get_width() / 2, v + 1.5, f"{v}%", ha="center")
plt.xticks(list(pos), nombres)
plt.ylim(0, 100)
plt.ylabel("% de secuencias con un minimo mal")
plt.title("La version con < solo falla si hay valores repetidos")
plt.legend()
plt.tight_layout()
plt.savefig("ejercicio-03-fallos.png", dpi=120)
