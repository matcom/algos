import importlib
import random
import matplotlib.pyplot as plt

mochila = importlib.import_module("ejercicio-11-mochila")
knapsack = mochila.knapsack

# Figura 1: celdas medidas segun los bits de W, contra los bits de n
# (izquierda: crece W; derecha: crece n con W fijo)
random.seed(4)
ks, celdas_k = [], []
for k in range(4, 21):
    W = 2 ** k - 1
    w = [random.randint(1, W) for _ in range(3)]
    v = [random.randint(1, 1000) for _ in range(3)]
    stats = {}
    knapsack(w, v, W, stats)
    ks.append(k)
    celdas_k.append(stats["cells"])

ns, celdas_n = [], []
for n in range(1, 18):
    W = 1023                                    # W fijo de 10 bits
    w = [random.randint(1, W) for _ in range(n)]
    v = [random.randint(1, 1000) for _ in range(n)]
    stats = {}
    knapsack(w, v, W, stats)
    ns.append(n)
    celdas_n.append(stats["cells"])

fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 4))
a1.plot(ks, celdas_k, "o-", color="tab:red")
a1.set_yscale("log")
a1.set_xlabel("bits de W  (n = 3 fijo)")
a1.set_ylabel("celdas de la tabla")
a1.set_title("Cada bit de W duplica el trabajo")
a1.grid(alpha=0.3)
a2.plot(ns, celdas_n, "o-", color="tab:blue")
a2.set_xlabel("n, cantidad de objetos  (W = 1023 fijo)")
a2.set_ylabel("celdas de la tabla")
a2.set_title("Cada objeto suma lo mismo")
a2.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("ejercicio-11-bits.png", dpi=120)

# Figura 2: mochila y primalidad contra un algoritmo polinomial, segun los bits
bs = list(range(4, 65, 2))
plt.figure(figsize=(7.5, 4.3))
plt.plot(bs, [100 * 2 ** b for b in bs], color="tab:red", label="mochila, n = 100:  100 · 2^b")
plt.plot(bs, [2 ** (b / 2) for b in bs], color="tab:orange", label="primalidad por division:  2^(b/2)")
plt.plot(bs, [b ** 3 for b in bs], color="tab:blue", label="un polinomio:  b³")
plt.axhline(3.6e12, color="gray", linestyle="--", label="una hora a 10^9 op/s")
plt.yscale("log")
plt.xlabel("b, bits del numero (W o el n de la primalidad)")
plt.ylabel("operaciones")
plt.title("Las dos son rectas en escala logaritmica: crecen como 2^b")
plt.legend(fontsize=9)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("ejercicio-11-comparacion.png", dpi=120)
