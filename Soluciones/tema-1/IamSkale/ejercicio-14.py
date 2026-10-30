"""Ejercicio 14 ★★★ — Ciclo completo sobre un problema nuevo: mezclar $k$ listas ordenadas (C2 a C5)

Código de validación de ejercicio-14.md.
Ejecutar con: python ejercicio-14.py
"""


# -------------------- Parte 1 --------------------

def mezclar(I, D, cuenta):
    """Mezcla de la C5: a lo sumo len(I) + len(D) - 1 comparaciones."""
    R, i, j = [], 0, 0
    while i < len(I) and j < len(D):
        cuenta[0] += 1
        if I[i] <= D[j]:
            R.append(I[i]); i += 1
        else:
            R.append(D[j]); j += 1
    return R + I[i:] + D[j:]

def mezclar_k(listas, cuenta):
    k = len(listas)
    if k == 0:
        return []
    if k == 1:
        return list(listas[0])
    m = (k + 1) // 2
    return mezclar(mezclar_k(listas[:m], cuenta), mezclar_k(listas[m:], cuenta), cuenta)

# -------------------- Parte 2 --------------------

import math, random, heapq
from itertools import permutations

def D(k):
    d = math.ceil(math.log2(k)) if k > 1 else 0
    return k * d - 2 ** d + k

def peor_caso_dyv(k, n):
    return n * D(k) - (k - 1)

def info(k, n):
    """log2 de N! / (n!)^k."""
    return (math.lgamma(k * n + 1) - k * math.lgamma(n + 1)) / math.log(2)

# -------------------- Parte 3 --------------------

rng = random.Random(14)
desordenadas, excedidas = 0, 0
for _ in range(3000):
    k, n = rng.randint(1, 12), rng.randint(0, 8)
    listas = [sorted(rng.randint(0, 20) for _ in range(n)) for _ in range(k)]
    cuenta = [0]
    R = mezclar_k(listas, cuenta)
    desordenadas += R != sorted(x for L in listas for x in L)
    excedidas += cuenta[0] > max(0, peor_caso_dyv(k, n))
if desordenadas == excedidas == 0:
    print("3000 pruebas: salida ordenada y nunca más comparaciones que n·D(k) - (k-1)")
else:
    print(f"3000 pruebas: {desordenadas} salidas mal ordenadas y {excedidas} con más "
          f"comparaciones que n·D(k) - (k-1)")

# -------------------- Parte 4 --------------------

def patron(listas, n):
    """Etiquetas en orden global: en cada mezcla, I[:-1] < D[:-1] < I[-1] < D[-1]."""
    if len(listas) == 1:
        return [listas[0]] * n
    m = (len(listas) + 1) // 2
    a, b = patron(listas[:m], n), patron(listas[m:], n)
    return a[:-1] + b[:-1] + [a[-1], b[-1]]

def entrada_peor(k, n):
    listas = [[] for _ in range(k)]
    for valor, i in enumerate(patron(list(range(k)), n)):
        listas[i].append(valor)
    return listas

no_alcanzan = []
for k in [2, 3, 4, 5, 8, 13, 16]:
    for n in [1, 5, 50]:
        cuenta = [0]
        mezclar_k(entrada_peor(k, n), cuenta)
        if cuenta[0] != peor_caso_dyv(k, n):
            no_alcanzan.append((k, n))
if not no_alcanzan:
    print("la entrada construida alcanza exactamente n·D(k) - (k-1)")
else:
    print(f"la entrada construida no alcanza n·D(k) - (k-1) en {len(no_alcanzan)} de 21 casos (k, n): {no_alcanzan}")
print("k = 2:", [peor_caso_dyv(2, n) for n in range(1, 8)], "= 2n - 1 (C5 §6)")

exceso = max(D(k) / k - math.log2(k) for k in range(1, 10**5))
print(f"max de D(k)/k - log2 k para k < 10^5: {exceso:.4f}")
assert exceso < 0.09

# -------------------- Parte 5 --------------------

k, n = 3, 2
etiquetas = [i for i in range(k) for _ in range(n)]
intercalados = set(permutations(etiquetas))
peor = 0
for orden in intercalados:
    listas = [[] for _ in range(k)]
    for pos, i in enumerate(orden):
        listas[i].append(pos)
    cuenta = [0]
    assert mezclar_k(listas, cuenta) == list(range(k * n))
    peor = max(peor, cuenta[0])
print(f"k=3, n=2: {len(intercalados)} intercalados = 6!/(2!)^3; peor caso {peor}; "
      f"cota de información ceil(log2 90) = {math.ceil(math.log2(len(intercalados)))}")

# -------------------- Parte 6 --------------------

def secuencial(listas, cuenta):
    R = []
    for L in listas:
        R = mezclar(R, L, cuenta)
    return R

def con_heap(listas, cuenta):
    class E:
        __slots__ = ("v", "i", "j")
        def __init__(self, v, i, j): self.v, self.i, self.j = v, i, j
        def __lt__(self, o):
            cuenta[0] += 1
            return self.v < o.v
    h = [E(L[0], i, 0) for i, L in enumerate(listas) if L]
    heapq.heapify(h)
    R = []
    while h:
        e = h[0]
        R.append(e.v)
        if e.j + 1 < len(listas[e.i]):
            heapq.heapreplace(h, E(listas[e.i][e.j + 1], e.i, e.j + 1))
        else:
            heapq.heappop(h)
    return R

def ordenar_todo(listas, cuenta):                       # mergesort sobre la concatenación
    todo = [x for L in listas for x in L]
    return mezclar_k([[x] for x in todo], cuenta)

print(f"{'k':>4} {'n':>5} {'cota info':>10} {'D&C':>8} {'D&C/info':>9} {'heap':>8} "
      f"{'secuencial':>11} {'ordenar todo':>13}")
for k, n in [(2, 1000), (4, 1000), (16, 1000), (64, 1000), (10, 5000), (256, 200)]:
    listas = entrada_peor(k, n)
    fila = []
    for f in (mezclar_k, con_heap, secuencial, ordenar_todo):
        cuenta = [0]
        assert f(listas, cuenta) == list(range(k * n))
        fila.append(cuenta[0])
    cota = math.ceil(info(k, n))
    print(f"{k:>4} {n:>5} {cota:>10} {fila[0]:>8} {fila[0] / cota:>9.3f} {fila[1]:>8} "
          f"{fila[2]:>11} {fila[3]:>13}")
