import importlib
import random
import matplotlib.pyplot as plt

gs = importlib.import_module("ejercicio-12-gale_shapley")
gale_shapley, gale_shapley_bug, random_instance = gs.gale_shapley, gs.gale_shapley_bug, gs.random_instance

# Figura 1: el ejemplo, con las listas y el resultado
pref_a = [[0, 1], [0], [0, 2]]
pref_b = [[2, 0, 1], [0, 1, 2], [0, 1, 2]]
M, _ = gale_shapley(pref_a, pref_b)

fig, ax = plt.subplots(figsize=(8, 3.6))
ya = {a: 2 - a for a in range(3)}
yb = {b: 2 - b for b in range(3)}
for a, lst in enumerate(pref_a):               # lo que lista cada proponente, en gris
    for b in lst:
        ax.plot([0, 3], [ya[a], yb[b]], color="lightgray", lw=1, zorder=1)
for a, b in enumerate(M):                      # el resultado, en azul
    if b is not None:
        ax.plot([0, 3], [ya[a], yb[b]], color="tab:blue", lw=2.5, zorder=2)
for a in range(3):
    solo = M[a] is None
    ax.add_patch(plt.Circle((0, ya[a]), 0.22, facecolor="#f6c9c9" if solo else "white",
                            edgecolor="black", zorder=3))
    ax.text(0, ya[a], f"a{a + 1}", ha="center", va="center", zorder=4)
    lista = " > ".join(f"b{b + 1}" for b in pref_a[a])
    ax.text(-0.35, ya[a], lista + ("   (solo)" if solo else ""), ha="right", va="center", fontsize=10)
for b in range(3):
    solo = b not in M
    ax.add_patch(plt.Circle((3, yb[b]), 0.22, facecolor="#f6c9c9" if solo else "white",
                            edgecolor="black", zorder=3))
    ax.text(3, yb[b], f"b{b + 1}", ha="center", va="center", zorder=4)
    lista = " > ".join(f"a{a + 1}" for a in pref_b[b])
    ax.text(3.35, yb[b], lista + ("   (solo)" if solo else ""), ha="left", va="center", fontsize=10)
ax.text(1.5, -0.75, "gris: lo que lista cada proponente   azul: el resultado   rojo: queda solo",
        ha="center", fontsize=9)
ax.set_xlim(-2.6, 5.6)
ax.set_ylim(-1, 2.5)
ax.set_aspect("equal")
ax.axis("off")
plt.tight_layout()
plt.savefig("ejercicio-12-ejemplo.png", dpi=120)

# Figura 2: propuestas contra L, el largo total de las listas
rng = random.Random(6)
Ls, ks = [], []
for _ in range(600):
    na, nb = rng.randint(2, 40), rng.randint(2, 40)
    pa, pb = random_instance(na, nb, rng)
    _, k = gale_shapley(pa, pb, order="random", seed=rng.random())
    Ls.append(sum(len(lst) for lst in pa))
    ks.append(k)

plt.figure(figsize=(7.5, 4.2))
plt.scatter(Ls, ks, s=8, alpha=0.5, label="una instancia al azar")
tope = max(Ls)
plt.plot([0, tope], [0, tope], "--", color="tab:red", label="L (la cota del potencial)")
plt.xlabel("L, suma de los largos de las listas de los proponentes")
plt.ylabel("propuestas")
plt.title("Nunca hay mas propuestas que L")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("ejercicio-12-propuestas.png", dpi=120)

# Figura 3: cuanto falla el algoritmo de listas completas copiado sin adaptar (prueba 7)


def falla(pa, pb):
    try:
        return gale_shapley_bug(pa, pb) != gale_shapley(pa, pb)[0]
    except IndexError:
        return True


rng = random.Random(7)
generadores = {
    "completas,\nn x n": lambda: ([rng.sample(range(6), 6) for _ in range(6)],
                                  [rng.sample(range(6), 6) for _ in range(6)]),
    "completas,\n6 x 4": lambda: ([rng.sample(range(4), 4) for _ in range(6)],
                                  [rng.sample(range(6), 6) for _ in range(4)]),
    "proponentes\nincompletos": lambda: random_instance(6, 6, rng),
    "los dos\nincompletos": lambda: random_instance(6, 6, rng, complete_b=False),
}
nombres = list(generadores)
fallos = [sum(falla(*g()) for _ in range(3000)) / 30 for g in generadores.values()]

plt.figure(figsize=(7, 4))
barras = plt.bar(nombres, fallos, color="tab:orange")
for b, f in zip(barras, fallos):
    plt.text(b.get_x() + b.get_width() / 2, f + 1.5, f"{f:.1f}%", ha="center")
plt.ylim(0, 112)
plt.ylabel("% de instancias en que falla")
plt.title("Las pruebas con listas completas de n x n no lo atrapan")
plt.tight_layout()
plt.savefig("ejercicio-12-fallos.png", dpi=120)
