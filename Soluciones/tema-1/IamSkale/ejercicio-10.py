"""Ejercicio 10 ★★ — Par más cercano en una dimensión (C2, C5)

Código de validación de ejercicio-10.md.
Ejecutar con: python ejercicio-10.py
"""


# -------------------- Parte 1 --------------------

import math, random

def par_mas_cercano_1d_aleatorio(xs, semilla=0, accesos=None, permutar=True):
    """Devuelve (distancia mínima, par, reconstrucciones). Costo esperado O(n).
    Si se pasa accesos=[0], cuenta los accesos a la tabla hash."""
    cuenta = accesos if accesos is not None else [0]
    pts = list(xs)
    if permutar:
        random.Random(semilla).shuffle(pts)
    d, par = abs(pts[0] - pts[1]), (pts[0], pts[1])
    reconstrucciones = 0
    if d == 0:
        return 0, par, reconstrucciones
    lado = d / 2
    celda = lambda x: math.floor(x / lado)
    rejilla = {celda(q): q for q in pts[:2]}
    for i in range(2, len(pts)):
        p = pts[i]
        c, antes = celda(p), d
        for dc in (-2, -1, 0, 1, 2):                    # las 5 celdas vecinas
            q = rejilla.get(c + dc)
            cuenta[0] += 1
            if q is not None and abs(p - q) < d:
                d, par = abs(p - q), (q, p)
        if d == 0:
            return 0, par, reconstrucciones
        if d < antes:                                   # delta bajó: reconstruir
            lado = d / 2
            rejilla = {celda(q): q for q in pts[:i + 1]}
            cuenta[0] += i + 1
            reconstrucciones += 1
        else:
            rejilla[c] = p
            cuenta[0] += 1
    return d, par, reconstrucciones

# -------------------- Parte 2 --------------------

from itertools import combinations

def fuerza_bruta(xs):
    return min(abs(a - b) for a, b in combinations(xs, 2))

def por_ordenamiento(xs):
    s = sorted(xs)
    return min(b - a for a, b in zip(s, s[1:]))

casos = [[3.0, 1.0], [5, 1, 9, 3], [1, 2, 3, 4], [7, 7], [0.5, -2.0, 10.0, 0.75], [-5, 5, -5.5, 100]]
for xs in casos:
    d, par, _ = par_mas_cercano_1d_aleatorio(xs)
    print(f"{str(xs):<28} -> distancia {d}, par {par}")
    assert d == fuerza_bruta(xs) == por_ordenamiento(xs)

# -------------------- Parte 3 --------------------

rng = random.Random(10)
for prueba in range(3000):
    n = rng.randint(2, 60)
    escala = rng.choice([1, 1000, 1e-3])
    xs = [rng.randint(-50, 50) * escala if rng.random() < 0.3 else rng.uniform(-1e3, 1e3)
          for _ in range(n)]
    d, par, _ = par_mas_cercano_1d_aleatorio(xs, semilla=prueba)
    assert abs(d - fuerza_bruta(xs)) < 1e-12 and abs(par[0] - par[1]) == d
print("3000 pruebas contra la fuerza bruta: sin fallos")

# -------------------- Parte 4 --------------------

def hay_repetidos(xs):
    d, par, _ = par_mas_cercano_1d_aleatorio(xs)   # la entrada es la misma: x_i -> x_i
    return par[0] - par[1] == 0                     # una prueba de signo más

for xs in [[1, 2, 3], [1, 2, 1], [5.5, -1, 5.5, 3], list(range(1000)), list(range(999)) + [500]]:
    assert hay_repetidos(xs) == (len(set(xs)) < len(xs))
print("distinción de elementos resuelta correctamente mediante la reducción")

# -------------------- Parte 5 --------------------

print(f"{'n':>9} {'reconstrucciones':>17} {'2 ln n':>7} {'accesos / n':>12}")
for n in [10**3, 10**4, 10**5, 10**6]:
    xs = [rng.random() for _ in range(n)]
    rs, acc = [], []
    for s in range(3):
        a = [0]
        rs.append(par_mas_cercano_1d_aleatorio(xs, semilla=s, accesos=a)[2])
        acc.append(a[0] / n)
    assert par_mas_cercano_1d_aleatorio(xs)[0] == por_ordenamiento(xs)
    print(f"{n:>9,} {sum(rs) / 3:>17.1f} {2 * math.log(n):>7.1f} {sum(acc) / 3:>12.2f}")
