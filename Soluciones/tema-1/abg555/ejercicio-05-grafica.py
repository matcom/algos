import importlib
import math
import random
import matplotlib.pyplot as plt

floyd = importlib.import_module("ejercicio-05-floyd")
has_cycle, has_cycle_bug, make_list = floyd.has_cycle, floyd.has_cycle_bug, floyd.make_list

# Figura 1: la lista del ejemplo (mu = 3, lam = 5) con forma de "rho"
mu, lam = 3, 5
pos = {}
for i in range(mu):                            # la cola, en linea recta
    pos[i] = (i * 1.3, 0)
r = 1.4
centro = (mu * 1.3 + r, 0)
for k in range(lam):                           # el ciclo, en circulo
    ang = math.pi - 2 * math.pi * k / lam
    pos[mu + k] = (centro[0] + r * math.cos(ang), centro[1] + r * math.sin(ang))

fig, ax = plt.subplots(figsize=(8, 3.6))
siguiente = {i: i + 1 for i in range(mu + lam - 1)}
siguiente[mu + lam - 1] = mu
for a, b in siguiente.items():
    ax.annotate("", xy=pos[b], xytext=pos[a],
                arrowprops=dict(arrowstyle="-|>", color="gray", lw=1.2,
                                shrinkA=14, shrinkB=14))
encuentro = 5                                  # se encuentran en la posicion 5
for i, (x, y) in pos.items():
    color = "#f6c9c9" if i == encuentro else ("#cfe8f3" if i >= mu else "white")
    ax.add_patch(plt.Circle((x, y), 0.32, facecolor=color, edgecolor="black", zorder=3))
    ax.text(x, y, str(i), ha="center", va="center", fontsize=12, zorder=4)
ax.text(1.3, -0.75, "cola: mu = 3 nodos", ha="center", fontsize=10)
ax.text(centro[0], -2.05, "ciclo: lam = 5 nodos", ha="center", fontsize=10, color="tab:blue")
ax.text(pos[encuentro][0] + 0.45, pos[encuentro][1] + 0.35, "se encuentran\n(vuelta 5)",
        fontsize=9, color="tab:red")
ax.text(pos[0][0], 0.55, "head", ha="center", fontsize=10)
ax.set_xlim(-0.8, centro[0] + r + 2.2)
ax.set_ylim(-2.4, 1.9)
ax.set_aspect("equal")
ax.axis("off")
plt.tight_layout()
plt.savefig("ejercicio-05-lista.png", dpi=120)

# Figura 2: el potencial vuelta a vuelta (mu = 10, lam = 15)
mu, lam = 10, 15
ts, fis = [], []
t = 0
while True:
    if t < mu:
        fi = (mu - t) + lam                    # fase 1: slow todavia no entra al ciclo
    else:
        fi = (-t) % lam                        # fase 2: distancia de fast hasta slow
    ts.append(t)
    fis.append(fi)
    if t >= 1 and t >= mu and fi == 0:
        break
    t += 1

plt.figure(figsize=(7.5, 4))
plt.plot(ts, fis, "o-", color="tab:blue")
plt.axvline(mu, color="gray", linestyle="--")
plt.text(mu + 0.2, max(fis) * 0.9, "slow entra al ciclo", fontsize=9)
plt.annotate("se encuentran", xy=(ts[-1], 0), xytext=(ts[-1] - 5, 6),
             arrowprops=dict(arrowstyle="->"), fontsize=9)
plt.xlabel("vuelta t")
plt.ylabel("potencial")
plt.title("El potencial baja en cada vuelta hasta llegar a 0 (mu = 10, lam = 15)")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("ejercicio-05-potencial.png", dpi=120)

# Figura 3: vueltas que da Floyd segun el largo n, en muchas listas


def vueltas(head):
    trace = []
    has_cycle(head, trace)
    return len(trace)


con_n, con_v, sin_n, sin_v = [], [], [], []
for mu in range(0, 61, 2):
    for lam in range(1, 61, 2):
        con_n.append(mu + lam)
        con_v.append(vueltas(make_list(mu, lam)[0]))
for n in range(0, 121):
    sin_n.append(n)
    sin_v.append(vueltas(make_list(n, 0)[0]))

plt.figure(figsize=(7.5, 4.2))
plt.scatter(con_n, con_v, s=8, alpha=0.5, label="con ciclo")
plt.scatter(sin_n, sin_v, s=8, color="tab:green", label="sin ciclo")
plt.plot([0, 120], [0, 120], "--", color="tab:red", label="n (la cota)")
plt.xlabel("n (nodos de la lista)")
plt.ylabel("vueltas")
plt.title("Floyd nunca da mas de n vueltas")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("ejercicio-05-vueltas.png", dpi=120)

# Figura 4: cuanto falla la version que solo revisa fast.next (de la prueba 7)


def falla(head):
    try:
        return has_cycle_bug(head) != has_cycle(head)
    except AttributeError:
        return True


random.seed(7)
generadores = {
    "con ciclo": lambda: make_list(random.randint(0, 60), random.randint(1, 60)),
    "sin ciclo,\nlargo impar": lambda: make_list(2 * random.randint(0, 30) + 1, 0),
    "sin ciclo,\nlargo par": lambda: make_list(2 * random.randint(1, 30), 0),
    "mezcladas": lambda: make_list(random.randint(1, 60), random.choice([0, random.randint(1, 60)])),
}
nombres = list(generadores)
fallos = [100 * sum(falla(g()[0]) for _ in range(3000)) / 3000 for g in generadores.values()]

plt.figure(figsize=(7, 4))
barras = plt.bar(nombres, fallos, color="tab:orange")
for b, f in zip(barras, fallos):
    plt.text(b.get_x() + b.get_width() / 2, f + 1.5, f"{f:.1f}%", ha="center")
plt.ylim(0, 110)
plt.ylabel("% de listas en que falla")
plt.title("La version que solo revisa fast.next falla con listas sin ciclo de largo par")
plt.tight_layout()
plt.savefig("ejercicio-05-fallos.png", dpi=120)
