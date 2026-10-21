"""Ejercicio 10: par mas cercano en una dimension (C2 sec. 3, 8, 9, 10).
Rejilla de intervalos semiabiertos de largo delta con tabla hash; aritmetica EXACTA (enteros y racionales)."""
import itertools
import math
import random
import time
from fractions import Fraction
from functools import cmp_to_key

random.seed(10)


def fuerza_bruta(P):
    return min(abs(a - b) for a, b in itertools.combinations(P, 2))


class Cuenta:
    def __init__(self):
        self.busquedas = self.inserciones = self.reconstrucciones = self.ins_reconstruccion = 0


def ordenar_y_recorrer(P):
    """C2 sec. 3: ordenar y mirar los n-1 pares consecutivos."""
    S = sorted(P)
    return min(S[i + 1] - S[i] for i in range(len(S) - 1))


def par_rejilla(P, semilla=0, cta=None, orden=None):
    """Insercion incremental con rejilla. Devuelve (distancia, par). P: enteros o Fraction (division exacta).
    orden='tal_cual' no baraja (para el ejemplo adversarial)."""
    cta = cta if cta is not None else Cuenta()
    pts = list(P)
    if orden != "tal_cual":
        random.Random(semilla).shuffle(pts)
    d = abs(pts[0] - pts[1])
    par = (pts[0], pts[1])
    if d == 0:                                  # borde: delta = 0 solo ocurre con un repetido; no hay rejilla de lado 0
        return 0, par
    rejilla = {pts[0] // d: pts[0], pts[1] // d: pts[1]}
    cta.inserciones += 2
    for i in range(2, len(pts)):
        p = pts[i]
        k = p // d                              # celda [k d, (k+1) d): parte entera exacta
        mejor, qmejor = d, None
        for dk in (-1, 0, 1):                   # 3 celdas: (p-d, p+d) cabe en k-1, k, k+1
            cta.busquedas += 1
            q = rejilla.get(k + dk)
            if q is not None and abs(p - q) < mejor:
                mejor, qmejor = abs(p - q), q
        if qmejor is not None:                  # delta baja
            if mejor == 0:                      # repetido: 0 es la distancia minima posible, devolver de inmediato
                return 0, (p, qmejor)
            d, par = mejor, (p, qmejor)
            rejilla = {x // d: x for x in pts[:i + 1]}      # reconstruir con el lado nuevo
            assert len(rejilla) == i + 1                    # invariante: una celda, a lo sumo un punto
            cta.reconstrucciones += 1
            cta.ins_reconstruccion += i + 1
        else:
            rejilla[k] = p
            cta.inserciones += 1
    return d, par


def radix_par(P, U):
    """Enteros en [0, U): LSD radix de 2 pasadas con base b = ceil(sqrt(U)), luego recorrido de consecutivos.
    Devuelve (distancia, operaciones sobre arreglos)."""
    b = math.isqrt(U - 1) + 1
    ops = 0
    A = list(P)
    for exp in (1, b):
        cont = [0] * (b + 1)
        for x in A:
            cont[(x // exp) % b + 1] += 1
            ops += 1
        for r in range(b):
            cont[r + 1] += cont[r]
            ops += 1
        B = [0] * len(A)
        for x in A:
            dig = (x // exp) % b
            B[cont[dig]] = x
            cont[dig] += 1
            ops += 2
        A = B
    d = min(A[i + 1] - A[i] for i in range(len(A) - 1))
    ops += len(A) - 1
    return d, ops


print("=== 1. Correctitud contra fuerza bruta: enteros, con muchos repetidos y bordes ===")
total = dup = 0
for _ in range(20000):
    n = random.randint(2, 60)
    rango = random.choice([3, 10, 50, 1000, 10 ** 9])
    P = [random.randint(-rango, rango) for _ in range(n)]
    if len(set(P)) < n:
        dup += 1
    d, par = par_rejilla(P, semilla=random.randrange(10 ** 6))
    assert d == fuerza_bruta(P) == ordenar_y_recorrer(P)
    assert abs(par[0] - par[1]) == d
    total += 1
print(f"  {total} instancias (n 2..60, rangos de 3 a 10^9 con repetidos, negativos): rejilla == fuerza bruta == ordenar+recorrer; "
      f"{dup} con repetidos")
for P in ([0, 5, 10, 15, 20, 25], [0, 7, 14, 21, 28, 35, 42], [0, 5, 10, 15, 20, 26], [1, 2], [4, 4], [0, 100, 101]):
    ok = all(par_rejilla(P, semilla=s)[0] == fuerza_bruta(P) for s in range(50))
    print(f"  bordes: P = {P}: 50 permutaciones, distancia {fuerza_bruta(P)} correcta: {ok}")
tot = 0
for _ in range(3000):
    n = random.randint(2, 40)
    P = [Fraction(random.randint(-200, 200), random.randint(1, 12)) for _ in range(n)]
    d, par = par_rejilla(P, semilla=random.randrange(10 ** 6))
    assert d == fuerza_bruta(P)
    tot += 1
print(f"  {tot} instancias con racionales (Fraction): correcto; la division por d es exacta, sin errores de redondeo")
progresiones = 0
for paso in (1, 2, 3, 7, 1000):
    for n in (2, 3, 10, 50):
        P = [paso * i for i in range(n)]
        for s in range(20):
            assert par_rejilla(P, semilla=s)[0] == paso
            progresiones += 1
print(f"  {progresiones} progresiones aritmeticas (todas las distancias iguales a delta, puntos justo en los bordes de celda): correcto")

print()
print("=== 2. El caso delta = 0 (repetidos): se devuelve 0 al detectar la colision ===")
for P in ([3, 3, 9, 12], [9, 12, 3, 3], [1, 5, 9, 13, 5], list(range(100)) + [57]):
    for s in (0, 1):
        c = Cuenta()
        d, par = par_rejilla(P, semilla=s, cta=c)
        print(f"  P={str(P)[:34]:<36} semilla {s}: distancia {d}, par {par}, busquedas {c.busquedas}, reconstrucciones {c.reconstrucciones}")
print("  sin repetidos delta > 0 siempre (distancia positiva entre enteros distintos); con repetidos no se construye lado 0:")
print("  delta = 0 solo se alcanza con un par igual, y el algoritmo termina ahi.")

print()
print("=== 3. Operaciones contra n: rejilla (accesos a la tabla) contra ordenar (comparaciones) ===")


class Cmp:
    n = 0


def comparaciones_ordenar(P):
    Cmp.n = 0

    def cmp(a, b):
        Cmp.n += 1
        return (a > b) - (a < b)
    sorted(P, key=cmp_to_key(cmp))
    return Cmp.n


def H(n):
    return sum(1 / k for k in range(1, n + 1))


print(f"  {'n':>8} {'accesos tabla':>14} {'por punto':>10} {'reconstr.':>10} {'2H_n - 3':>9} {'compar. ordenar':>16} {'n log2 n':>12} {'t rejilla':>10} {'t sorted':>9}")
for n, semillas in ((1000, 200), (10_000, 50), (100_000, 8), (1_000_000, 2)):
    P = random.sample(range(n * n if n <= 100_000 else 10 ** 12), n)
    accesos, recs = [], []
    for s in range(semillas):
        c = Cuenta()
        par_rejilla(P, semilla=s, cta=c)
        accesos.append(c.busquedas + c.inserciones + c.ins_reconstruccion)
        recs.append(c.reconstrucciones)
    t0 = time.perf_counter()
    par_rejilla(P, semilla=0)
    t_rej = time.perf_counter() - t0
    t0 = time.perf_counter()
    sorted(P)
    t_sort = time.perf_counter() - t0
    comp = comparaciones_ordenar(P)
    print(f"  {n:>8} {sum(accesos) / len(accesos):>14.0f} {sum(accesos) / len(accesos) / n:>10.2f} {sum(recs) / len(recs):>10.1f} "
          f"{2 * H(n) - 3:>9.1f} {comp:>16} {n * math.log2(n):>12.0f} {t_rej:>9.2f}s {t_sort:>8.2f}s")
print("  (acceso de tabla = busqueda + insercion + insercion durante reconstruccion; el orden de ordenar es n log2 n)")

print()
print("=== 4. Reconstrucciones: media sobre muchas permutaciones contra la cota 2 H_n - 3 ===")
print(f"  {'n':>6} {'permutaciones':>14} {'media':>7} {'maximo':>7} {'2H_n - 3':>9}")
for n, perms in ((10, 4000), (100, 4000), (1000, 1000)):
    P = random.sample(range(n * n * 4), n)
    rs = []
    for s in range(perms):
        c = Cuenta()
        par_rejilla(P, semilla=s, cta=c)
        rs.append(c.reconstrucciones)
    print(f"  {n:>6} {perms:>14} {sum(rs) / len(rs):>7.2f} {max(rs):>7} {2 * H(n) - 3:>9.2f}")
    assert sum(rs) / len(rs) <= 2 * H(n) - 3 + 0.2

print()
print("=== 5. Sin el azar: un orden adversarial fuerza una reconstruccion por insercion ===")
for n in (200, 800):
    P = [2 ** k for k in range(n)]              # insertados de mayor a menor: cada uno mas cerca del anterior
    P_adv = P[::-1]
    c1, c2 = Cuenta(), Cuenta()
    par_rejilla(P_adv, cta=c1, orden="tal_cual")
    par_rejilla(P, semilla=1, cta=c2)
    print(f"  n={n}: orden adversarial: {c1.reconstrucciones} reconstrucciones, {c1.ins_reconstruccion} inserciones en reconstrucciones "
          f"(~ n^2/2 = {n * n // 2});  barajado: {c2.reconstrucciones} reconstrucciones, {c2.ins_reconstruccion} inserciones")

print()
print("=== 6. Otra salida del modelo: radix sort sobre enteros de rango acotado ===")
print(f"  {'n':>8} {'U = n^2':>14} {'ops radix (2 pasadas + recorrido)':>34} {'por punto':>10} {'n log2 n':>12}")
for n in (1000, 10_000, 100_000, 1_000_000):
    U = n * n
    P = random.sample(range(U), n)
    d, ops = radix_par(P, U)
    if n <= 10_000:
        assert d == ordenar_y_recorrer(P)
    print(f"  {n:>8} {U:>14} {ops:>34} {ops / n:>10.2f} {n * math.log2(n):>12.0f}")
ok = 0
for _ in range(2000):
    n = random.randint(2, 60)
    U = random.choice([4, 10, 100, 10 ** 4])
    P = [random.randrange(U) for _ in range(n)]
    d, _ops = radix_par(P, U)
    assert d == fuerza_bruta(P)
    ok += 1
print(f"  {ok} instancias pequenas (con repetidos): radix + recorrido == fuerza bruta")
