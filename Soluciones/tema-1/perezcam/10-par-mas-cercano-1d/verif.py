"""Ejercicio 10 - par mas cercano en una dimension.

El listado del algoritmo que aparece en ejercicio-10.tex es literalmente la funcion
par_cercano_incremental_1d de este archivo (el .tex la incluye con \\lstinputlisting).
Todo lo que se imprime es ASCII porque el .tex pega la salida tal cual.
"""
import math
import random
import statistics
import time
from itertools import permutations


# ------------------------------------------------------------------ referencias (oraculos)
def par_cercano_fuerza_bruta(P):
    return min(abs(P[a] - P[b]) for a in range(len(P)) for b in range(a + 1, len(P)))


def par_cercano_ordenando(P):
    Q = sorted(P)
    return min(Q[i + 1] - Q[i] for i in range(len(Q) - 1))


# ------------------------------------------------------------------ el algoritmo del ejercicio
def par_cercano_incremental_1d(P, semilla=0, mezclar=True):
    """Rejilla de lado delta, ventana de 3 celdas. Devuelve (delta, reconstrucciones, trabajo)."""
    pts = list(P)
    if len(pts) < 2:
        raise ValueError("hacen falta al menos 2 puntos")
    if mezclar:
        random.Random(semilla).shuffle(pts)
    delta = abs(pts[0] - pts[1])
    if delta == 0:                                   # repetido: la respuesta es 0
        return 0, 0, 0
    celda = lambda x, lado: math.floor(x / lado)
    rejilla = {celda(pts[0], delta): pts[0], celda(pts[1], delta): pts[1]}
    reconstrucciones = trabajo = 0
    for i in range(2, len(pts)):
        p = pts[i]
        c = celda(p, delta)
        antes = delta
        for dc in (-1, 0, 1):                        # ventana de 3 celdas
            q = rejilla.get(c + dc)
            if q is not None and abs(p - q) < delta:
                delta = abs(p - q)
        if delta == 0:                               # p repite un valor ya insertado
            return 0, reconstrucciones, trabajo
        if delta < antes:                            # delta bajo: reconstruir la rejilla
            rejilla = {celda(q, delta): q for q in pts[:i + 1]}
            reconstrucciones += 1
            trabajo += i + 1
        else:
            rejilla[c] = p                           # la celda estaba vacia (invariante)
    return delta, reconstrucciones, trabajo
# ---- fin del listado


def incremental_variante(P, factor, radio, semilla=0):
    """Misma idea con lado = factor*delta y ventana +-radio, solo para mostrar variantes mal elegidas."""
    pts = list(P)
    random.Random(semilla).shuffle(pts)
    delta = abs(pts[0] - pts[1])
    if delta == 0:
        return 0
    celda = lambda x, lado: math.floor(x / lado)
    rejilla = {celda(pts[0], factor * delta): pts[0], celda(pts[1], factor * delta): pts[1]}
    for i in range(2, len(pts)):
        p = pts[i]
        c = celda(p, factor * delta)
        antes = delta
        for dc in range(-radio, radio + 1):
            q = rejilla.get(c + dc)
            if q is not None and abs(p - q) < delta:
                delta = abs(p - q)
        if delta == 0:
            return 0
        if delta < antes:
            rejilla = {celda(q, factor * delta): q for q in pts[:i + 1]}
        else:
            rejilla[c] = p
    return delta


def H(n):
    return sum(1 / k for k in range(1, n + 1))


# ================================================================== 1. correctitud
print("== 1. correctitud contra los oraculos ==")
random.seed(0)
fallos = 0
for s in range(3000):
    P = [random.uniform(-1000, 1000) for _ in range(random.randint(2, 100))]
    if abs(par_cercano_ordenando(P) - par_cercano_incremental_1d(P, semilla=s)[0]) > 1e-9:
        fallos += 1
print(f"reales uniformes   : 3000 instancias, fallos (deberia ser 0): {fallos}")

fallos = con_cero = 0
for s in range(3000):
    n = random.randint(2, 40)
    P = [random.randint(0, n * n) for _ in range(n)]       # enteros: aritmetica exacta, a veces hay repetidos
    esperado = par_cercano_fuerza_bruta(P)
    obtenido = par_cercano_incremental_1d(P, semilla=s)[0]
    con_cero += (esperado == 0)
    if esperado != obtenido:
        fallos += 1
print(f"enteros con repetidos: 3000 instancias ({con_cero} con respuesta 0), fallos (deberia ser 0): {fallos}")

# ================================================================== 2. la rejilla: lado y ventana
print()
print("== 2. rejilla: lado y ventana ==")
d = 1.0
for (lado, p, q) in [(0.5, 0.49, 1.48), (1.0, 0.9, 1.1)]:
    cp, cq = math.floor(p / lado), math.floor(q / lado)
    print(f"delta=1, lado={lado}: p={p}, q={q}, |p-q|={abs(p - q):.2f} < delta, celdas {cp} y {cq}, difieren en {abs(cp - cq)}")

random.seed(5)
def ventana_no_alcanza(factor, radio, ensayos=20000):
    malos = 0
    for _ in range(ensayos):
        S = [random.uniform(0, 10) for _ in range(random.randint(3, 8))]
        delta = par_cercano_ordenando(S)
        lado = factor * delta
        q = random.choice(S)
        p = q + random.uniform(-delta, delta)
        if abs(math.floor(p / lado) - math.floor(q / lado)) > radio:
            malos += 1
    return malos

print()
print("vecino a distancia < delta que queda fuera de la ventana (20000 ensayos):")
for factor, radio in [(0.5, 2), (0.5, 1), (1.0, 1), (1.0, 0)]:
    print(f"   lado = {factor:>3} * delta, ventana de {2 * radio + 1} celdas: {ventana_no_alcanza(factor, radio):>5}")

random.seed(8)
print()
print("algoritmo completo con cada variante (2000 instancias de n=10..60, resultado distinto del correcto):")
instancias = [[random.uniform(0, 1) for _ in range(random.randint(10, 60))] for _ in range(2000)]
for factor, radio in [(1.0, 1), (0.5, 2), (0.5, 1), (1.0, 0)]:
    malos = sum(abs(incremental_variante(P, factor, radio, semilla=k) - par_cercano_ordenando(P)) > 1e-12
                for k, P in enumerate(instancias))
    print(f"   lado = {factor:>3} * delta, ventana de {2 * radio + 1} celdas: {malos:>4} errores")

random.seed(6)
def max_por_celda(S, factor):
    lado = factor * par_cercano_ordenando(S)
    cuenta = {}
    for x in S:
        k = math.floor(x / lado)
        cuenta[k] = cuenta.get(k, 0) + 1
    return max(cuenta.values())
conjuntos = [[random.uniform(0, 100) for _ in range(random.randint(2, 60))] for _ in range(5000)]
print()
print(f"maximo de puntos en una celda (5000 conjuntos): lado=delta -> {max(max_por_celda(S, 1.0) for S in conjuntos)},"
      f" lado=delta/2 -> {max(max_por_celda(S, 0.5) for S in conjuntos)}")

# ================================================================== 3. reconstrucciones
print()
print("== 3. reconstrucciones: media sobre barajados distintos del MISMO conjunto ==")
print(f"{'n':>8} {'semillas':>9} {'media':>7} {'desv':>6} {'2 ln n':>8} {'2H_n-3':>8} {'trabajo/n':>10}")
random.seed(11)
for n, semillas in [(1_000, 200), (10_000, 200), (100_000, 200), (1_000_000, 20)]:
    P = [random.random() for _ in range(n)]
    res = [par_cercano_incremental_1d(P, semilla=s) for s in range(semillas)]
    xs = [r for _, r, _ in res]
    print(f"{n:>8} {semillas:>9} {statistics.mean(xs):>7.2f} {statistics.pstdev(xs):>6.2f}"
          f" {2 * math.log(n):>8.2f} {2 * H(n) - 3:>8.2f} {statistics.mean(t for _, _, t in res) / n:>10.2f}")

# ================================================================== 4. peor caso
print()
print("== 4. peor caso: x_k = 2^-k, el mismo conjunto con y sin barajar ==")
n = 800
P = [2.0 ** -k for k in range(1, n + 1)]
_, r0, t0 = par_cercano_incremental_1d(P, mezclar=False)
print(f"sin barajar (orden k=1..n): {r0} reconstrucciones en {n - 2} pasos, trabajo = {t0:,} (n^2/2 = {n * n // 2:,})")
res = [par_cercano_incremental_1d(P, semilla=s) for s in range(200)]
print(f"barajando (200 semillas)  : reconstrucciones media {statistics.mean(r for _, r, _ in res):.1f},"
      f" trabajo medio {statistics.mean(t for _, _, t in res):,.0f}, maximo {max(t for _, _, t in res):,}")

print("orden de insercion en el que TODOS los pasos reconstruyen (enumerando las n! permutaciones):")
for n in (5, 6, 7, 8):
    P = [2.0 ** -k for k in range(1, n + 1)]
    malas = sum(par_cercano_incremental_1d(list(perm), mezclar=False)[1] == n - 2 for perm in permutations(P))
    print(f"   n={n}: {malas} de {math.factorial(n)} permutaciones; 2^(n-1) = {2 ** (n - 1)}; probabilidad 2^(n-1)/n! = {malas / math.factorial(n):.4f}")

# ================================================================== 5. tiempos
print()
print("== 5. tiempos en Python (ordenar: mejor de 3; rejilla: media de 5 barajados) ==")
print(f"{'n':>8} {'ordenar':>9} {'rejilla':>9} {'ord us/pto':>11} {'rej us/pto':>11} {'log2 n':>7} {'rej/ord':>8}")
random.seed(3)
for n in [10_000, 100_000, 1_000_000]:
    P = [random.random() for _ in range(n)]
    t_ord = float("inf")
    for _ in range(3):
        t0 = time.perf_counter(); par_cercano_ordenando(P); t_ord = min(t_ord, time.perf_counter() - t0)
    ts = []
    for s in range(5):
        t0 = time.perf_counter(); par_cercano_incremental_1d(P, semilla=s); ts.append(time.perf_counter() - t0)
    t_rej = statistics.mean(ts)
    print(f"{n:>8} {t_ord:>8.3f}s {t_rej:>8.3f}s {1e6 * t_ord / n:>11.3f} {1e6 * t_rej / n:>11.3f}"
          f" {math.log2(n):>7.1f} {t_rej / t_ord:>8.1f}")

# ================================================================== 6. la reduccion y la cota
print()
print("== 6. la reduccion y la cota ==")
random.seed(3)
fallos_red = 0
for _ in range(5000):
    n = random.randint(2, 30)
    base = [random.randint(0, 15) for _ in range(n)]
    if (par_cercano_ordenando([float(x) for x in base]) == 0.0) != (len(set(base)) < len(base)):
        fallos_red += 1
print(f"reduccion (distancia 0 syss hay repetido): 5000 pruebas, fallos (deberia ser 0): {fallos_red}")


def camino_insercion_binaria(perm):
    """Secuencia de respuestas de las comparaciones al ordenar perm por insercion binaria."""
    orden, camino = [], []
    for x in perm:
        lo, hi = 0, len(orden)
        while lo < hi:
            m = (lo + hi) // 2
            menor = orden[m] < x
            camino.append(menor)
            if menor:
                lo = m + 1
            else:
                hi = m
        orden.insert(lo, x)
    return tuple(camino)

print()
print("un algoritmo de comparaciones (insercion binaria) sobre las n! permutaciones de entradas distintas:")
print(f"{'n':>3} {'n!':>6} {'hojas distintas':>16} {'prof. maxima':>13} {'ceil(log2 n!)':>14} {'ceil(log3 n!)':>14}")
for n in range(3, 9):
    caminos = [camino_insercion_binaria(p) for p in permutations(range(n))]
    lg = math.lgamma(n + 1)
    print(f"{n:>3} {math.factorial(n):>6} {len(set(caminos)):>16} {max(map(len, caminos)):>13}"
          f" {math.ceil(lg / math.log(2) - 1e-9):>14} {math.ceil(lg / math.log(3) - 1e-9):>14}")

# ================================================================== 7. la franja en una dimension
print()
print("== 7. la franja de C2 en una dimension: cuantos puntos aporta cada lado ==")


def dyv_1d(Q, maximos):
    """Divide y venceras sobre Q ordenada y sin repetidos. maximos = [max izq, max der] de la franja."""
    n = len(Q)
    if n <= 3:
        return min(Q[b] - Q[a] for a in range(n) for b in range(a + 1, n))
    m = n // 2
    delta = min(dyv_1d(Q[:m], maximos), dyv_1d(Q[m:], maximos))     # mejor par del MISMO lado
    L = Q[m]
    izq = [x for x in Q[:m] if x > L - delta]                         # (L-delta, L]
    der = [x for x in Q[m:] if x < L + delta]                         # [L, L+delta)
    maximos[0] = max(maximos[0], len(izq))
    maximos[1] = max(maximos[1], len(der))
    for a in izq:                                                     # sin suponer el lema: todos los cruces
        for b in der:
            delta = min(delta, b - a)
    return delta

random.seed(9)
maximos, fallos = [0, 0], 0
for _ in range(3000):
    Q = sorted(random.sample(range(10 ** 6), random.randint(2, 200)))
    if dyv_1d(Q, maximos) != par_cercano_ordenando(Q):
        fallos += 1
print(f"3000 instancias: fallos {fallos}, maximo de puntos de la franja a la izquierda de L: {maximos[0]},"
      f" a la derecha: {maximos[1]}")
