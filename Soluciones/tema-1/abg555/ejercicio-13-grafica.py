import importlib
import math
import random
import matplotlib.pyplot as plt

sp = importlib.import_module("ejercicio-13-splay")
access_sequence, move_to_root = sp.access_sequence, sp.move_to_root

# Figura 1: costo real de cada acceso y potencial, n = 200, claves en orden
n = 200
watch = []
access_sequence(n, range(1, n + 1), watch=watch)
reales = [c for c, _, _, _ in watch]
pot = [watch[0][1]] + [d for _, _, d, _ in watch]
fig, (a1, a2) = plt.subplots(2, 1, figsize=(9, 5.2), sharex=True)
a1.bar(range(1, n + 1), reales, color="tab:orange")
a1.set_yscale("log")
a1.set_ylabel("rotaciones")
a1.set_title("n = 200, claves en orden: el primer acceso cuesta 199 y los demas unas pocas rotaciones")
a2.plot(range(0, n + 1), pot, color="tab:green")
a2.axhline(math.lgamma(n + 1) / math.log(2), color="gray", linestyle="--", label="Phi del camino = log2 n!")
a2.set_xlabel("accesos hechos")
a2.set_ylabel("potencial  Phi")
a2.legend(fontsize=9)
plt.tight_layout()
plt.savefig("ejercicio-13-accesos.png", dpi=120)

# Figura 2: costo total segun n
rng = random.Random(6)
ns = [50, 100, 200, 400, 800, 1600]
real, cota, azar, raiz = [], [], [], []
for n in ns:
    real.append(sum(access_sequence(n, range(1, n + 1))))
    cota.append(n * (3 * math.log2(n) + 1) + math.lgamma(n + 1) / math.log(2))
    azar.append(sum(access_sequence(n, [rng.randint(1, n) for _ in range(n)])))
    if n <= 400:
        raiz.append(sum(access_sequence(n, list(range(1, n + 1)) * 2, reorganize=move_to_root)[n:]))
plt.figure(figsize=(7.5, 4.3))
plt.plot(ns, cota, "o--", color="tab:red", label="cota: n (3 log2 n + 1) + log2 n!")
plt.plot(ns, azar, "o-", color="tab:orange", label="splay, n accesos al azar")
plt.plot(ns, real, "o-", color="tab:blue", label="splay, claves 1..n en orden")
plt.plot(ns[:len(raiz)], raiz, "o-", color="gray", label="subir a la raiz, en orden")
plt.plot(ns, [4.5 * n for n in ns], ":", color="tab:blue", label="4.5 n")
plt.xscale("log")
plt.yscale("log")
plt.xlabel("n")
plt.ylabel("costo total (rotaciones)")
plt.title("En orden, splay es lineal: la cota n log n no es ajustada")
plt.legend(fontsize=8)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("ejercicio-13-total.png", dpi=120)
