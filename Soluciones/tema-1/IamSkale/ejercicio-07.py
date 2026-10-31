"""Ejercicio 7 ★★★ — Mediana de dos arreglos ordenados (C2, C3, C5)

Código de validación de ejercicio-07.md.
Ejecutar con: python ejercicio-07.py
"""


# -------------------- Parte 1 --------------------

def n_esimo(A, B, comparar):
    """n-ésimo menor de A + B (A y B ordenados, de largo n >= 1)."""
    n = len(A)
    lo, hi = 0, n + 1                    # invariante: P(lo) verdadero; hi = n+1 o P(hi) falso
    while hi - lo > 1:
        m = (lo + hi) // 2               # 1 <= m <= n
        if comparar(A[m - 1], B[n - m]) <= 0:
            lo = m
        else:
            hi = m
    i, j = lo, n - lo                    # i = i*: cuántos aporta A
    if i == 0:
        return B[j - 1]
    if j == 0:
        return A[i - 1]
    return A[i - 1] if comparar(A[i - 1], B[j - 1]) >= 0 else B[j - 1]

# -------------------- Parte 2 --------------------

import math, random
from itertools import combinations

class Contador:
    def __init__(self):
        self.n = 0
    def __call__(self, x, y):
        self.n += 1
        return (x > y) - (x < y)

def oraculo(A, B):
    return sorted(A + B)[len(A) - 1]

# -------------------- Parte 3 --------------------

casos = [
    ([1], [2]),                       # n = 1
    ([1, 2, 3], [4, 5, 6]),           # todo A antes que B
    ([4, 5, 6], [1, 2, 3]),           # todo B antes que A
    ([1, 3, 5], [2, 4, 6]),           # intercalados
    ([2, 2, 2], [2, 2, 2]),           # todo igual
    ([1, 1, 9, 9], [1, 9, 9, 9]),     # repetidos
]
for A, B in casos:
    r = n_esimo(A, B, Contador())
    print(f"A={A}, B={B} -> {r}  (oráculo {oraculo(A, B)})")
    assert r == oraculo(A, B)

# -------------------- Parte 4 --------------------

for n in range(1, 10):
    peor = 0
    for idx_A in combinations(range(2 * n), n):
        A = list(idx_A)
        B = [v for v in range(2 * n) if v not in idx_A]
        c = Contador()
        assert n_esimo(A, B, c) == oraculo(A, B)
        peor = max(peor, c.n)
    assert peor <= math.ceil(math.log2(n + 1)) + 1
    print(f"n = {n}: {math.comb(2 * n, n):>6} entradas, peor caso {peor} comparaciones, "
          f"cota de información {math.ceil(math.log2(2 * n))}")

# -------------------- Parte 5 --------------------

rng = random.Random(7)
for _ in range(20000):
    n = rng.randint(1, 60)
    A = sorted(rng.randint(0, 10) for _ in range(n))
    B = sorted(rng.randint(0, 10) for _ in range(n))
    assert n_esimo(A, B, Contador()) == oraculo(A, B)

for n in [10**3, 10**5, 10**6]:
    A = sorted(rng.random() for _ in range(n))
    B = sorted(rng.random() for _ in range(n))
    c = Contador()
    assert n_esimo(A, B, c) == oraculo(A, B)
    print(f"n = {n:>8,}: {c.n} comparaciones (log2(n+1)+1 = {math.ceil(math.log2(n + 1)) + 1})")

# -------------------- Parte 6 --------------------

def testigo(n, en_A, k):
    """Entrada con valores 0..2n-1 donde el n-ésimo menor es A[k] (en_A) o B[k]."""
    valores = list(range(2 * n))
    abajo, objetivo, arriba = valores[:n - 1], valores[n - 1], valores[n:]
    propios = abajo[:k] + [objetivo] + arriba[:n - 1 - k]       # el array del objetivo
    otros = abajo[k:] + arriba[n - 1 - k:]
    A, B = (propios, otros) if en_A else (otros, propios)
    return sorted(A), sorted(B)

for n in [1, 2, 5, 8, 13]:
    posiciones = set()
    for en_A in (True, False):
        for k in range(n):
            A, B = testigo(n, en_A, k)
            assert len(A) == len(B) == n
            r = oraculo(A, B)
            pos = ("A", A.index(r)) if r in A else ("B", B.index(r))
            assert pos == (("A" if en_A else "B"), k)
            posiciones.add(pos)
    print(f"n = {n:>2}: {len(posiciones)} salidas distintas -> al menos ceil(log2 {2 * n}) = "
          f"{math.ceil(math.log2(2 * n))} comparaciones")
