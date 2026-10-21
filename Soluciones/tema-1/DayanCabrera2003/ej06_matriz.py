"""Ejercicio 6: busqueda en una matriz n x n con filas y columnas ordenadas (C3, C5).
Modelo: la unica operacion es comparar x con A[i][j] (3 resultados); se cuentan las comparaciones."""
import itertools
import math
import random

random.seed(6)


class Oraculo:
    """Matriz oculta; consulta(i, j) devuelve -1, 0, +1 segun x <, =, > A[i][j]. Registra las consultas."""
    def __init__(self, A, x):
        self.A, self.x = A, x
        self.consultas = []                 # lista de (i, j, respuesta)

    def consulta(self, i, j):
        a = self.A[i][j]
        r = -1 if self.x < a else (0 if self.x == a else 1)
        self.consultas.append((i, j, r))
        return r


def escalera(n, o):
    """Desde la esquina superior derecha. Invariante: si x esta, esta en A[i..n-1][0..j]."""
    i, j = 0, n - 1
    while i < n and j >= 0:
        r = o.consulta(i, j)
        if r == 0:
            return True
        if r < 0:           # x < A[i][j]: toda la columna j (filas >= i) es > x
            j -= 1
        else:               # x > A[i][j]: toda la fila i (columnas <= j) es < x
            i += 1
    return False


def esquina_00(n, o):
    """Desde (0,0): no hay regla que descarte una fila o columna entera; solo se puede avanzar a ciegas
    por la fila 0 y la columna 0 (aqui: recorre toda la matriz por filas, n^2 comparaciones)."""
    for i in range(n):
        for j in range(n):
            if o.consulta(i, j) == 0:
                return True
    return False


def solo_antidiagonal(n, o):
    """Candidato natural a n comparaciones: mirar solo la antidiagonal i + j = n - 1."""
    return any(o.consulta(i, n - 1 - i) == 0 for i in range(n))


def omite_esquina(n, o):
    """La escalera, pero no compara la ultima celda (n-1, 0), que esta en la antidiagonal."""
    i, j = 0, n - 1
    while i < n and j >= 0:
        if (i, j) == (n - 1, 0):
            return False
        r = o.consulta(i, j)
        if r == 0:
            return True
        if r < 0:
            j -= 1
        else:
            i += 1
    return False


def fuerza_bruta(A, x):
    return any(x == v for fila in A for v in fila)


def matriz_aleatoria(n, k):
    """Filas y columnas no decrecientes, con duplicados (incrementos 0..k)."""
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            base = max(A[i - 1][j] if i else 0, A[i][j - 1] if j else 0)
            A[i][j] = base + random.randint(0, k)
    return A


print("=== 1. Escalera contra fuerza bruta en matrices aleatorias con duplicados ===")
total = 0
maxc = {}
for n in range(1, 31):
    for _ in range(40):
        A = matriz_aleatoria(n, random.choice([0, 1, 2, 5]))
        for x in range(-1, A[n - 1][n - 1] + 2):
            o = Oraculo(A, x)
            assert escalera(n, o) == fuerza_bruta(A, x), (n, x)
            maxc[n] = max(maxc.get(n, 0), len(o.consultas))
            total += 1
            assert len(o.consultas) <= 2 * n - 1
print(f"  {total} pares (matriz, x), n = 1..30: la escalera coincide con la fuerza bruta y usa <= 2n-1 comparaciones")
print("  maximo observado por n (aleatorias):", {n: maxc[n] for n in (1, 2, 3, 5, 10, 20, 30)})

print()
print("=== 2. Peor caso exacto: A[i][j] = 2(i+j), x = 2n-3 ===")
malos = 0
for n in range(1, 101):
    A = [[2 * (i + j) for j in range(n)] for i in range(n)]
    o = Oraculo(A, 2 * n - 3)
    assert escalera(n, o) is False
    malos += len(o.consultas) != 2 * n - 1
print(f"  n = 1..100: comparaciones == 2n-1 en todos salvo {malos}")
n = 5
A = [[2 * (i + j) for j in range(n)] for i in range(n)]
o = Oraculo(A, 2 * n - 3)
escalera(n, o)
print(f"  n=5: celdas consultadas en orden: {[(i, j) for i, j, r in o.consultas]}")
print("  Exhaustivo para n = 2 (entradas 0..4) y n = 3 (entradas 0..3): maximo de comparaciones sobre toda matriz ordenada y todo x")
for n, vmax in ((2, 4), (3, 3)):
    mx, cuentan = 0, 0
    for vals in itertools.product(range(vmax + 1), repeat=n * n):
        A = [list(vals[i * n:(i + 1) * n]) for i in range(n)]
        if not all(A[i][j] <= A[i][j + 1] for i in range(n) for j in range(n - 1)):
            continue
        if not all(A[i][j] <= A[i + 1][j] for i in range(n - 1) for j in range(n)):
            continue
        cuentan += 1
        for x2 in range(-1, 2 * vmax + 2):
            x = x2 / 2
            o = Oraculo(A, x)
            assert escalera(n, o) == fuerza_bruta(A, x)
            mx = max(mx, len(o.consultas))
    print(f"    n={n}: {cuentan} matrices ordenadas, maximo = {mx} (2n-1 = {2 * n - 1})")
    assert mx == 2 * n - 1

print()
print("=== 3. El adversario como programa: x = 2n-3, responde segun N[i][j] = 2(i+j) ===")


def adversario(n, algoritmo):
    """Ejecuta 'algoritmo' contra el adversario. Si el algoritmo termina sin consultar alguna celda p de las
    diagonales i+j = n-1 (n celdas) o i+j = n-2 (n-1 celdas), construye N_p (N con la celda p puesta a x)
    y comprueba que el algoritmo, corrido sobre N_p, da la misma transcripcion y la misma respuesta."""
    x = 2 * n - 3
    N = [[2 * (i + j) for j in range(n)] for i in range(n)]
    o = Oraculo(N, x)
    resp = algoritmo(n, o)
    diag = [(i, n - 1 - i) for i in range(n)] + [(i, n - 2 - i) for i in range(n - 1)]
    consultadas = {(i, j) for i, j, r in o.consultas}
    sin_consultar = [p for p in diag if p not in consultadas]
    # N no contiene x: la respuesta correcta en N es False
    if resp is True:
        return "ERROR en N (dijo que x esta y no esta)", len(o.consultas), sin_consultar, None
    if not sin_consultar:
        return "correcto (consulto las 2n-1 celdas)", len(o.consultas), sin_consultar, None
    p = sin_consultar[0]
    Np = [fila[:] for fila in N]
    Np[p[0]][p[1]] = x
    # N_p sigue siendo estrictamente creciente por filas y columnas
    assert all(Np[i][j] < Np[i][j + 1] for i in range(n) for j in range(n - 1))
    assert all(Np[i][j] < Np[i + 1][j] for i in range(n - 1) for j in range(n))
    assert fuerza_bruta(Np, x)
    o2 = Oraculo(Np, x)
    resp2 = algoritmo(n, o2)
    assert o2.consultas == o.consultas and resp2 == resp
    return "ERROR en N_p con p=" + str(p), len(o.consultas), sin_consultar, Np


for nombre, alg in (("escalera", escalera), ("omite (n-1,0)", omite_esquina),
                    ("solo antidiagonal", solo_antidiagonal), ("esquina (0,0), n^2", esquina_00)):
    print(f"  {nombre}:")
    for n in (3, 6, 12):
        veredicto, c, falt, Np = adversario(n, alg)
        print(f"    n={n:>2}: {c:>3} comparaciones; celdas de las 2n-1 sin consultar: {len(falt)}; {veredicto}")
n = 3
_, _, falt, Np = adversario(3, solo_antidiagonal)
print(f"  Matriz del adversario para 'solo antidiagonal', n=3 (x = {2 * n - 3}, celda p = {falt[0]} puesta a x):")
for fila in Np:
    print("    ", fila)

print()
print("=== 4. Informacion contra el adversario (n x n) ===")
print(f"  {'n':>5} {'log2(n^2+1)':>12} {'log2 C(2n,n)':>13} {'2n-1 (exacto)':>14}")
for n in (1, 2, 5, 10, 50, 100, 1000):
    print(f"  {n:>5} {math.log2(n * n + 1):>12.1f} {math.log2(math.comb(2 * n, n)):>13.1f} {2 * n - 1:>14}")
print("  C(2n,n) = numero de fronteras monotonas posibles {A < x}; cada comparacion da 2 respuestas utiles")


print()
print("=== 5. Matriz m x n con m <= n: escalera contra galopar por filas ===")
def escalera_mn(m, n, o):
    i, j = 0, n - 1
    while i < m and j >= 0:
        r = o.consulta(i, j)
        if r == 0:
            return True
        if r < 0:
            j -= 1
        else:
            i += 1
    return False


def galope(m, n, o):
    """Fila a fila; en la fila i, galopa hacia la izquierda desde j buscando la mayor columna c <= j con
    A[i][c] <= x (busqueda exponencial + binaria); las columnas > c se descartan para toda fila >= i."""
    j = n - 1
    for i in range(m):
        if j < 0:
            return False
        r = o.consulta(i, j)
        if r == 0:
            return True
        if r > 0:
            continue                             # A[i][j] < x: la fila i no sirve; pasar a la siguiente
        # A[i][j] > x: galopar a la izquierda
        paso, hi = 1, j                          # hi: columna con A[i][hi] > x
        while True:
            c = max(hi - paso, 0)
            r = o.consulta(i, c)
            if r == 0:
                return True
            if r > 0:
                lo = c                           # A[i][lo] < x
                break
            hi = c
            if c == 0:
                return False                     # toda la fila i es > x, y las siguientes tambien
            paso *= 2
        while hi - lo > 1:                       # busqueda binaria entre lo (< x) y hi (> x)
            mid = (lo + hi) // 2
            r = o.consulta(i, mid)
            if r == 0:
                return True
            if r > 0:
                lo = mid
            else:
                hi = mid
        j = lo                                   # columnas > lo descartadas; la fila i se agota en lo
    return False


def matriz_mn(m, n, k):
    A = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            base = max(A[i - 1][j] if i else 0, A[i][j - 1] if j else 0)
            A[i][j] = base + random.randint(0, k)
    return A


for m, n in ((4, 4), (4, 64), (8, 512), (16, 4096), (64, 64)):
    peor_g = peor_e = 0
    for _ in range(300):
        A = matriz_mn(m, n, random.choice([1, 3, 50]))
        for x in random.sample(range(-1, A[m - 1][n - 1] + 2), min(25, A[m - 1][n - 1] + 3)):
            og, oe = Oraculo(A, x), Oraculo(A, x)
            assert galope(m, n, og) == fuerza_bruta(A, x) == escalera_mn(m, n, oe)
            peor_g = max(peor_g, len(og.consultas))
            peor_e = max(peor_e, len(oe.consultas))
    cota = 2 * m * (math.log2(1 + n / m) + 2) + m
    inf = m * math.ceil(math.log2(n // m + 1))
    print(f"  m={m:>2}, n={n:>4}: escalera peor={peor_e:>4} (m+n-1={m + n - 1:>4});  galope peor medido={peor_g:>4}; "
          f"cota 2m(log2(1+n/m)+2)+m = {cota:>7.1f};  cota inferior m*ceil(log2(n/m+1)) = {inf}")
    assert peor_g <= cota


print()
print("=== 6. Familia de bloques (cota inferior m x n): cada fila tiene su bloque, bloques disjuntos ===")
def familia_bloques(m, n, huecos):
    """Fila i: bloque de s columnas en [(m-1-i)s, (m-i)s - 1]. Izquierda del bloque: valores muy negativos;
    derecha: muy positivos; bloque: s valores a ambos lados de x=0, con x en el hueco huecos[i] (0..s)."""
    s = n // m
    GRANDE = 10 ** 6
    A = [[0] * n for _ in range(m)]
    for i in range(m):
        lo, hi = (m - 1 - i) * s, (m - i) * s - 1
        for c in range(n):
            if c < lo:
                A[i][c] = -GRANDE + i + c
            elif c > hi:
                A[i][c] = GRANDE + i + c
            else:
                t = c - lo                       # posicion dentro del bloque, 0..s-1
                A[i][c] = (t - huecos[i]) * 2 + 1 if t >= huecos[i] else (t - huecos[i]) * 2 - 1
    return A


ok = True
for m, n in ((3, 12), (4, 16), (5, 40)):
    for _ in range(200):
        s = n // m
        A = familia_bloques(m, n, [random.randint(0, s) for _ in range(m)])
        ok &= all(A[i][j] < A[i][j + 1] for i in range(m) for j in range(n - 1))
        ok &= all(A[i][j] < A[i + 1][j] for i in range(m - 1) for j in range(n))
        ok &= not fuerza_bruta(A, 0)
print(f"  familia valida (filas y columnas estrictamente crecientes, x=0 ausente) en 600 matrices aleatorias: {ok}")
for m, n in ((8, 512), (16, 4096)):
    s = n // m
    peor = 0
    for _ in range(300):
        A = familia_bloques(m, n, [random.randint(0, s) for _ in range(m)])
        o = Oraculo(A, 0)
        assert galope(m, n, o) is False
        peor = max(peor, len(o.consultas))
    print(f"  m={m:>2}, n={n:>4}, s={s}: el galope hace hasta {peor} comparaciones; cota inferior m*ceil(log2(s+1)) = "
          f"{m * math.ceil(math.log2(s + 1))}")
