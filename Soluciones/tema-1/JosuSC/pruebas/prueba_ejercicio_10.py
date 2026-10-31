#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejercicio 10 - Casos de prueba
Par más cercano en una dimensión: la reducción desde ED y el algoritmo
aleatorio de rejilla y tabla hash (costo esperado lineal).

Qué se comprueba:
  1. La reducción: para TODOS los vectores de {0..4}^n con n <= 5,
     "todos distintos" <=> el par más cercano tiene x_i != x_j
     (el Lema 1 del ejercicio, que es lo único que la reducción agrega).
  2. Correctitud del algoritmo aleatorio: 8000 instancias de enteros
     (con rangos hasta 10^12 y muchos repetidos) y 800 de racionales
     exactos, contra el mínimo de las brechas del orden.
  3. La probabilidad de reconstruir en el paso k pegada a la cota 2/k
     (el Paso 1 de la sección 4.5).
  4. Las operaciones de diccionario por punto se quedan en ~6 aunque n
     crezca de mil a cien mil: es lo que "rompe" la cota Omega(n log n)
     del modelo de árboles de decisión.

Ejecutar:  python3 prueba_ejercicio_10.py   (tarda unos segundos)
Solo usa la biblioteca estándar.
"""

import itertools
import random
from fractions import Fraction


def par_ordenando(x):
    """El determinista de referencia: ordenar y mirar vecinos (Lema 0)."""
    idx = sorted(range(len(x)), key=lambda i: x[i])
    return min(zip(idx, idx[1:]), key=lambda p: abs(x[p[0]] - x[p[1]]))


def distintos_via_reduccion(x):
    i, j = par_ordenando(x)
    return x[i] != x[j]                    # el único test extra de la reducción


def par_aleatorio(x, ops=None, rng=None):
    """El algoritmo de la sección 4.2, con contadores opcionales."""
    rng = rng or random
    n = len(x)
    orden = list(range(n))
    rng.shuffle(orden)
    p0, p1 = orden[0], orden[1]
    delta = abs(x[p0] - x[p1])
    par = (p0, p1)
    if delta == 0:
        return par, delta
    celdas = {}

    def reconstruir(k):
        celdas.clear()
        for t in orden[:k]:
            celdas[x[t] // delta] = t
        if ops is not None:
            ops["dic"] += k
            ops["reconstrucciones"] += 1
            ops["trabajo_rec"] += k

    reconstruir(2)
    if ops is not None:
        ops["reconstrucciones"] -= 1        # la inicial no cuenta
        ops["trabajo_rec"] -= 2
    for k in range(2, n):
        p = orden[k]
        c = x[p] // delta
        mejor, cand = delta, None
        for d in (c - 1, c, c + 1):         # solo 3 celdas
            q = celdas.get(d)
            if ops is not None:
                ops["dic"] += 1
            if q is not None and abs(x[p] - x[q]) < mejor:
                mejor, cand = abs(x[p] - x[q]), q
        if cand is None:
            celdas[c] = p
            if ops is not None:
                ops["dic"] += 1
        else:
            delta, par = mejor, (p, cand)
            if delta == 0:
                return par, delta
            reconstruir(k + 1)
            if ops is not None:
                ops["rebuild_en"].append(k + 1)
    return par, delta


def referencia(x):
    s = sorted(x)
    return min(b - a for a, b in zip(s, s[1:]))


def main():
    # ------------------------------------------------------------------
    # 1) La reducción ED <= par más cercano, exhaustivo
    # ------------------------------------------------------------------
    tot = 0
    for n in range(2, 6):
        for x in itertools.product(range(5), repeat=n):
            assert distintos_via_reduccion(list(x)) == (len(set(x)) == n)
            tot += 1

    # ------------------------------------------------------------------
    # 2) Correctitud del algoritmo aleatorio
    # ------------------------------------------------------------------
    random.seed(1)
    casos = 0
    for _ in range(8000):                   # enteros, con y sin muchos repetidos
        n = random.randint(2, 30)
        R = random.choice([3, 10, 100, 10**6, 10**12])
        x = [random.randint(-R, R) for _ in range(n)]
        (i, j), d = par_aleatorio(x)
        assert i != j and abs(x[i] - x[j]) == d == referencia(x), (x, i, j, d)
        casos += 1
    for _ in range(800):                    # racionales exactos
        n = random.randint(2, 25)
        x = [Fraction(random.randint(-50, 50), random.randint(1, 9)) for _ in range(n)]
        (i, j), d = par_aleatorio(x)
        assert i != j and abs(x[i] - x[j]) == d == referencia(x)
        casos += 1

    # ------------------------------------------------------------------
    # 3) Probabilidad de reconstruir en el paso k, frente a la cota 2/k
    # ------------------------------------------------------------------
    random.seed(7)
    n, T = 100, 4000
    cuenta = {}
    for _ in range(T):
        x = [random.randint(0, 10**15) for _ in range(n)]
        ops = {"dic": 0, "reconstrucciones": 0, "trabajo_rec": 0, "rebuild_en": []}
        par_aleatorio(x, ops)
        for k in ops["rebuild_en"]:
            cuenta[k] = cuenta.get(k, 0) + 1
    for k in range(3, 11):
        empirica = cuenta.get(k, 0) / T
        assert empirica <= 2 / k + 0.05, (k, empirica)
        assert empirica >= 2 / k - 0.08, (k, empirica)

    # ------------------------------------------------------------------
    # 4) Operaciones por punto: planas, mientras log2 n crece
    # ------------------------------------------------------------------
    random.seed(2026)
    medias = {}
    for n, T in [(10**3, 60), (10**4, 24), (10**5, 8)]:
        acc = []
        for _ in range(T):
            x = [random.randint(0, 10**15) for _ in range(n)]
            ops = {"dic": 0, "reconstrucciones": 0, "trabajo_rec": 0, "rebuild_en": []}
            par_aleatorio(x, ops)
            acc.append(ops["dic"] / n)
        medias[n] = sum(acc) / len(acc)
        assert 4 <= medias[n] <= 9, (n, medias[n])
    m1, m2, m3 = medias[10**3], medias[10**4], medias[10**5]
    assert max(m1, m2, m3) < 1.6 * min(m1, m2, m3)          # planas
    import math
    assert math.log2(10**5) / math.log2(10**3) > 1.6        # ...mientras log n crece 67%

    print("ejercicio 10: todo correcto")
    print(f"  reducción ED <= par más cercano: {tot} vectores exhaustivos")
    print(f"  correctitud: {casos} instancias (enteros hasta 1e12 y racionales exactos)")
    print("  P(reconstruir en paso k) <= 2/k + 0.05 y pegada a 2/k para k = 3..10")
    print(f"  ops de diccionario por punto: {m1:.2f} (n=1e3), {m2:.2f} (n=1e4), {m3:.2f} (n=1e5)")


if __name__ == "__main__":
    main()
