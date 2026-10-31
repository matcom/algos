import importlib
import random
import matplotlib.pyplot as plt

mz = importlib.import_module("ejercicio-09-mezcla")
merge, merge_optimized = mz.merge, mz.merge_optimized

# Figura 1: la intercalada perfecta con n = 5 (como la figura 8 de la conferencia 5),
# con las comparaciones de la mezcla normal y de la optimizada
n = 5
A, B = list(range(0, 2 * n, 2)), list(range(1, 2 * n, 2))
pos = {}
for k in range(n):
    pos[A[k]] = (2 * k, 1)
    pos[B[k]] = (2 * k + 1, 0)
fig, axes = plt.subplots(2, 1, figsize=(8.5, 4.6))
for ax, (titulo, f) in zip(axes, [("mezcla normal", merge), ("mezcla optimizada", merge_optimized)]):
    log = []
    R, c = f(A, B, log)
    comparados = {(a, b) for a, b in log}
    vecinos = [(A[k], B[k]) for k in range(n)] + [(A[k + 1], B[k]) for k in range(n - 1)]
    for a, b in vecinos:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        if (a, b) in comparados:
            ax.plot([x1, x2], [y1, y2], color="tab:orange", lw=2)
        else:
            ax.plot([x1, x2], [y1, y2], color="tab:red", lw=2, linestyle=":")
    for v, (x, y) in pos.items():
        ax.add_patch(plt.Circle((x, y), 0.28, facecolor="white", edgecolor="black", zorder=3))
        nombre = f"a{A.index(v) + 1}" if v in A else f"b{B.index(v) + 1}"
        ax.text(x, y, nombre, ha="center", va="center", fontsize=10, zorder=4)
    bien = "bien" if R == sorted(A + B) else "MAL"
    ax.set_title(f"{titulo}: {c} comparaciones de {2 * n - 1} pares de vecinos, resultado {bien}",
                 fontsize=10)
    ax.set_xlim(-0.6, 2 * n - 0.4)
    ax.set_ylim(-0.5, 1.5)
    ax.set_aspect("equal")
    ax.axis("off")
plt.suptitle("Naranja: pares comparados.  Rojo punteado: pares de vecinos que nunca se compararon",
             fontsize=10)
plt.tight_layout()
plt.savefig("ejercicio-09-adversario.png", dpi=120)

# Figura 2: cuanto falla segun donde esta el mayor de todos
rng = random.Random(5)


def al_azar(n):
    v = rng.sample(range(10 * n), 2 * n)
    return sorted(v[:n]), sorted(v[n:])


def mayor_en(lista, n):
    A, B = al_azar(n)
    if (max(A) > max(B)) != (lista == "A"):
        A, B = B, A
    return A, B


generadores = {
    "el mayor\nesta en A": lambda: mayor_en("A", rng.randint(1, 30)),
    "al azar": lambda: al_azar(rng.randint(1, 30)),
    "el mayor\nesta en B": lambda: mayor_en("B", rng.randint(1, 30)),
}
fallos = []
for generar in generadores.values():
    malos = 0
    for _ in range(4000):
        A, B = generar()
        malos += merge_optimized(A, B)[0] != sorted(A + B)
    fallos.append(malos / 40)
plt.figure(figsize=(6.5, 3.8))
barras = plt.bar(list(generadores), fallos, color="tab:orange")
for b, f in zip(barras, fallos):
    plt.text(b.get_x() + b.get_width() / 2, f + 2, f"{f:.1f}%", ha="center")
plt.ylim(0, 112)
plt.ylabel("% de mezclas con resultado mal")
plt.title("La optimizada falla justo cuando el mayor de todos esta en B")
plt.tight_layout()
plt.savefig("ejercicio-09-fallos.png", dpi=120)
