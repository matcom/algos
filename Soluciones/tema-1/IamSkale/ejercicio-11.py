"""Ejercicio 11 ★★ — La mochila $O(nW)$ medida en bits (C1)

Código de validación de ejercicio-11.md.
Ejecutar con: python ejercicio-11.py
"""


# -------------------- Parte 1 --------------------

def mochila(pesos, valores, W, cuenta=None):
    mejor = [0] * (W + 1)
    for w, v in zip(pesos, valores):
        for c in range(W, w - 1, -1):
            if cuenta is not None:
                cuenta[0] += 1
            if mejor[c - w] + v > mejor[c]:
                mejor[c] = mejor[c - w] + v
    return mejor[W]

# -------------------- Parte 2 --------------------

from itertools import product
import random

def fuerza_bruta(pesos, valores, W):
    mejor = 0
    for elegidos in product([0, 1], repeat=len(pesos)):
        if sum(p for p, e in zip(pesos, elegidos) if e) <= W:
            mejor = max(mejor, sum(v for v, e in zip(valores, elegidos) if e))
    return mejor

rng = random.Random(11)
fallos = 0
for _ in range(500):
    n = rng.randint(0, 10)
    pesos = [rng.randint(1, 30) for _ in range(n)]
    valores = [rng.randint(1, 50) for _ in range(n)]
    W = rng.randint(0, 100)
    fallos += mochila(pesos, valores, W) != fuerza_bruta(pesos, valores, W)
if fallos == 0:
    print("500 instancias: la programación dinámica coincide con la fuerza bruta")
else:
    print(f"500 instancias: la programación dinámica difiere de la fuerza bruta en {fallos}")

# -------------------- Parte 3 --------------------

def bits(x):
    return max(1, x.bit_length())

pesos = [rng.randint(1, 10) for _ in range(20)]
valores = [rng.randint(1, 1000) for _ in range(20)]
tam_objetos = sum(bits(w) + bits(v) for w, v in zip(pesos, valores))

print(f"{'bits de W':>10} {'bits entrada':>13} {'operaciones':>12} {'cociente':>9}")
anterior = None
for k in range(10, 19):
    W = 2 ** k - 1
    cuenta = [0]
    mochila(pesos, valores, W, cuenta)
    b = tam_objetos + bits(W)
    cociente = "" if anterior is None else f"{cuenta[0] / anterior:.2f}"
    print(f"{k:>10} {b:>13} {cuenta[0]:>12,} {cociente:>9}")
    anterior = cuenta[0]

# -------------------- Parte 4 --------------------

segundos_por_año = 3600 * 24 * 365
print(f"{'bits de W':>10} {'operaciones':>12} {'tiempo':>20}")
for k in [16, 32, 48, 64, 128]:
    ops = 100 * 2 ** k
    s = ops / 10**9
    if s < 60:
        tiempo = f"{s:.3g} segundos"
    elif s < 86400:
        tiempo = f"{s / 3600:.3g} horas"
    elif s < segundos_por_año:
        tiempo = f"{s / 86400:.3g} días"
    else:
        tiempo = f"{s / segundos_por_año:.3g} años"
    print(f"{k:>10} {float(ops):>12.3g} {tiempo:>20}")
