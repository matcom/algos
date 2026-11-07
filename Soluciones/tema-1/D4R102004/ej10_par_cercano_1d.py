"""Ejercicio 10: par más cercano en una dimensión.
1) La reducción: distinción de elementos se responde con "¿la distancia mínima es 0?".
2) El algoritmo de la rejilla (C2 §9) adaptado a la recta: cajas de lado δ/2,
   se miran 5 cajas (la propia y dos a cada lado). Costo esperado O(n)."""
import math
import random
import time


def fuerza_bruta(xs):
    return min(abs(a - b) for i, a in enumerate(xs) for b in xs[i + 1:])


def ordenando(xs):
    """El algoritmo de la conferencia 2 §3: ordenar y mirar consecutivos. Θ(n log n)."""
    s = sorted(xs)
    return min(b - a for a, b in zip(s, s[1:]))


def hay_repetidos(xs, par_mas_cercano):
    """La reducción: distinción de elementos usando un algoritmo de par más cercano."""
    return par_mas_cercano(xs) == 0


def rejilla_1d(xs, semilla=0):
    """Inserción incremental aleatoria con cajas de lado δ/2 en una tabla hash.
    Devuelve (distancia mínima, número de reconstrucciones)."""
    pts = list(xs)
    random.Random(semilla).shuffle(pts)
    delta = abs(pts[0] - pts[1])
    if delta == 0:
        return 0, 0
    lado = delta / 2
    cajas = {math.floor(p / lado): p for p in pts[:2]}
    reconstrucciones = 0
    for i in range(2, len(pts)):
        p = pts[i]
        c = math.floor(p / lado)               # la parte entera: fuera del modelo algebraico
        mejor = delta
        for vecina in range(c - 2, c + 3):     # 5 cajas: la propia y dos a cada lado
            q = cajas.get(vecina)              # acceso directo por índice: tampoco está en el modelo
            if q is not None and abs(p - q) < mejor:
                mejor = abs(p - q)
        if mejor == 0:
            return 0, reconstrucciones
        if mejor < delta:                      # δ bajó: rehacer las cajas
            delta, lado = mejor, mejor / 2
            cajas = {math.floor(q / lado): q for q in pts[:i + 1]}
            assert len(cajas) == i + 1         # invariante: a lo sumo un número por caja
            reconstrucciones += 1
        else:
            assert c not in cajas              # la caja de p estaba vacía
            cajas[c] = p
    return delta, reconstrucciones


# 1. Correctitud contra la fuerza bruta, incluidos repetidos
random.seed(10)
for _ in range(3000):
    n = random.randint(2, 30)
    xs = [random.choice([random.randint(0, 40), random.uniform(0, 100)]) for _ in range(n)]
    esperado = fuerza_bruta(xs)
    assert abs(rejilla_1d(xs, semilla=random.randint(0, 99))[0] - esperado) < 1e-9
    assert abs(ordenando(xs) - esperado) < 1e-9
    assert hay_repetidos(xs, ordenando) == (len(set(xs)) < len(xs))
print("3000 instancias (con y sin repetidos): rejilla, ordenamiento y reducción correctos\n")

# 2. Reconstrucciones contra 2 ln n, y tiempos
print(f"{'n':>9} {'reconstr.':>10} {'2 ln n':>7} {'rejilla':>9} {'ordenar':>9}")
for n in [1_000, 10_000, 100_000, 1_000_000]:
    xs = [random.random() for _ in range(n)]
    rs = [rejilla_1d(xs, semilla=s)[1] for s in range(3)] if n <= 100_000 else []
    t0 = time.perf_counter(); r, rec = rejilla_1d(xs); t1 = time.perf_counter()
    o = ordenando(xs); t2 = time.perf_counter()
    assert abs(r - o) < 1e-12
    prom = sum(rs) / len(rs) if rs else rec
    print(f"{n:>9,} {prom:>10.1f} {2 * math.log(n):>7.1f} {t1 - t0:>8.3f}s {t2 - t1:>8.3f}s")
