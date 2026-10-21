"""Ejercicio 11: la mochila 0/1 por programacion dinamica, O(nW), y el tamano de la entrada en bits (C1 sec. 8)."""
import itertools
import math
import random
import time

random.seed(11)


def mochila_tabla(w, v, W):
    """T[i][c] = mejor valor con los primeros i objetos y capacidad c. Devuelve (T, celdas evaluadas)."""
    n = len(w)
    T = [[0] * (W + 1) for _ in range(n + 1)]
    celdas = 0
    for i in range(1, n + 1):
        wi, vi = w[i - 1], v[i - 1]
        for c in range(W + 1):
            celdas += 1
            T[i][c] = T[i - 1][c]
            if wi <= c and T[i - 1][c - wi] + vi > T[i][c]:
                T[i][c] = T[i - 1][c - wi] + vi
    return T, celdas


def mochila_fila(w, v, W, descendente=True):
    """Una sola fila. Correcta solo con c descendente (T[c - wi] sigue siendo de la fila i-1)."""
    T = [0] * (W + 1)
    ops = 0
    for wi, vi in zip(w, v):
        rango = range(W, wi - 1, -1) if descendente else range(wi, W + 1)
        for c in rango:
            ops += 1
            if T[c - wi] + vi > T[c]:
                T[c] = T[c - wi] + vi
    return T[W], ops


def mochila_ilimitada_bruta(w, v, W):
    """Variante con objetos repetibles, por programacion dinamica independiente (para comparar con el bug)."""
    mejor = [0] * (W + 1)
    for c in range(1, W + 1):
        mejor[c] = max([mejor[c - 1]] + [mejor[c - wi] + vi for wi, vi in zip(w, v) if wi <= c])
    return mejor[W]


def bruta(w, v, W, k=None):
    n = len(w) if k is None else k
    best = 0
    for mask in range(1 << n):
        pw = sum(w[i] for i in range(n) if mask >> i & 1)
        if pw <= W:
            best = max(best, sum(v[i] for i in range(n) if mask >> i & 1))
    return best


def bits(x):
    return max(1, x.bit_length())


def tam_bits(w, v, W):
    """N = bits para escribir los pesos, valores y capacidad en binario."""
    return sum(bits(a) for a in w) + sum(bits(a) for a in v) + bits(W)


print("=== 1. Correctitud: la tabla contra fuerza bruta, e invariante T[i][c] vigilado ===")
total = celdas_vig = 0
for _ in range(3000):
    n = random.randint(1, 9)
    w = [random.randint(1, 12) for _ in range(n)]
    v = [random.randint(1, 30) for _ in range(n)]
    W = random.randint(0, 40)
    T, _c = mochila_tabla(w, v, W)
    assert T[n][W] == mochila_fila(w, v, W)[0] == bruta(w, v, W)
    for i in range(n + 1):                      # invariante: T[i][c] = mejor con los primeros i objetos y capacidad c
        for c in range(W + 1):
            assert T[i][c] == bruta(w, v, c, k=i)
            celdas_vig += 1
    total += 1
print(f"  {total} instancias (n<=9): tabla == una fila == fuerza bruta; invariante comprobado en {celdas_vig} celdas T[i][c]")

print()
print("=== 2. Por que c va hacia abajo: con c ascendente el objeto se puede usar varias veces ===")
w, v, W = [2], [3], 4
print(f"  un objeto de peso 2 y valor 3, W=4: descendente -> {mochila_fila(w, v, W)[0]} (correcto: 3); "
      f"ascendente -> {mochila_fila(w, v, W, descendente=False)[0]} (usa el objeto 2 veces)")
malas = igual_ilim = 0
for _ in range(3000):
    n = random.randint(1, 6)
    w = [random.randint(1, 10) for _ in range(n)]
    v = [random.randint(1, 20) for _ in range(n)]
    W = random.randint(1, 30)
    a = mochila_fila(w, v, W, descendente=False)[0]
    malas += a != bruta(w, v, W)
    igual_ilim += a == mochila_ilimitada_bruta(w, v, W)
print(f"  3000 instancias: el ascendente falla en {malas} ({100 * malas / 3000:.1f} %), y coincide con la mochila con repeticion en {igual_ilim} de 3000")

print()
print("=== 3. El costo: n (W + 1) celdas, y la memoria; con una fila O(W) ===")
for n, W in ((4, 1000), (10, 5000), (50, 2000)):
    w = [random.randint(1, 50) for _ in range(n)]
    v = [random.randint(1, 100) for _ in range(n)]
    T, celdas = mochila_tabla(w, v, W)
    _, ops = mochila_fila(w, v, W)
    print(f"  n={n:>2}, W={W:>5}: tabla {celdas} celdas evaluadas = n(W+1) = {n * (W + 1)}, memoria {(n + 1) * (W + 1)} celdas; "
          f"una fila: {W + 1} celdas, {ops} actualizaciones")
    assert celdas == n * (W + 1)

print()
print("=== 4. Tamano de la entrada en bits y la familia que no es polinomial en N ===")
print("  Familia F_k: n = 4 fijo, pesos y valores de k bits (con el bit alto en 1), W = 2^k.")
print(f"  {'k':>3} {'N (bits)':>9} {'n W':>12} {'celdas evaluadas':>17} {'celdas/2^k':>11} {'N^2':>8} {'N^3':>9}")
filas = []
for k in range(3, 19):
    n = 4
    w = [random.randint(2 ** (k - 1), 2 ** k - 1) for _ in range(n)]
    v = [random.randint(2 ** (k - 1), 2 ** k - 1) for _ in range(n)]
    W = 2 ** k
    N = tam_bits(w, v, W)
    _T, celdas = mochila_tabla(w, v, W)
    filas.append((k, N, celdas))
    print(f"  {k:>3} {N:>9} {n * W:>12} {celdas:>17} {celdas / 2 ** k:>11.2f} {N ** 2:>8} {N ** 3:>9}")
for (k1, N1, c1), (k2, N2, c2) in zip(filas, filas[1:]):
    assert c2 > 1.85 * c1         # cada bit de W duplica el costo (salvo el +n de la fila inicial)
print("  Cada bit mas de W (y de los demas numeros) duplica las celdas: costo = 2^{Theta(N)} para n fijo.")
print("  Como cada numero tiene exactamente k bits, N = 2nk + (k+1) = 9k+1 con n = 4, y las celdas son n(2^k+1) (verificado arriba hasta k = 18).")
print("  Primer k donde la tabla supera N^c (con esas formulas exactas):")
for c in (2, 3, 5, 10):
    kc = next(k for k in range(1, 400) if 4 * (2 ** k + 1) > (9 * k + 1) ** c)
    print(f"    N^{c:<2}: desde k = {kc:>3}  (N = {9 * kc + 1})")
print("  Ninguna potencia fija de N acota n(2^k+1) cuando k crece: para toda potencia hay un k a partir del cual la tabla es mayor.")

print()
print("=== 5. La primalidad por division (C1 sec. 8): divisiones contra bits ===")


def es_primo_mr(n):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def divisiones_primo(n):
    """Prueba divisores d = 2..isqrt(n). Devuelve (es primo, divisiones)."""
    cnt = 0
    for d in range(2, math.isqrt(n) + 1):
        cnt += 1
        if n % d == 0:
            return False, cnt
    return True, cnt


print(f"  {'bits de p':>9} {'primo p':>20} {'divisiones':>11} {'sqrt(p)':>11} {'divisiones/sqrt(p)':>19}")
datos_primo = []
for b in range(8, 43, 2):
    p = 2 ** b + 1
    while not es_primo_mr(p):
        p += 2
    es, cnt = divisiones_primo(p)
    assert es
    datos_primo.append((p.bit_length(), cnt))
    print(f"  {p.bit_length():>9} {p:>20} {cnt:>11} {math.isqrt(p):>11} {cnt / math.isqrt(p):>19.4f}")
for (b1, c1), (b2, c2) in zip(datos_primo, datos_primo[1:]):
    assert 1.9 < c2 / c1 < 2.1         # +2 bits  =>  x2  (sqrt(p) = 2^{b/2})
print("  Cada 2 bits mas multiplican las divisiones por 2 (cada bit, por raiz de 2): ~2^{b/2}, exponencial en los bits.")

print()
print("=== 6. El mismo bucle, en unario: polinomial ===")
print("  Con W escrito en unario (W simbolos) la entrada mide N' >= W + n, y n(W+1) <= n N': lineal en N'.")
for W in (10, 100, 1000):
    n = 4
    print(f"    W={W:>5}: N' >= {W + n} simbolos, celdas = {n * (W + 1)} <= n*N' = {n * (W + n)}")

print()
print("=== 7. Cambiar de unidades: la misma instancia en gramos y en miligramos ===")
base_w, base_v, base_W = [120, 200, 310, 450, 95], [60, 100, 180, 260, 40], 800
print(f"  {'unidad':>9} {'W':>10} {'N (bits)':>9} {'celdas':>12} {'celdas/base':>12} {'bits extra':>11}  mejor valor")
Nb = Cb = None
for j in range(0, 6):
    f = 10 ** j
    w = [a * f for a in base_w]
    W = base_W * f
    N = tam_bits(w, base_v, W)
    if j <= 3:
        T, celdas = mochila_tabla(w, base_v, W)
        mejor = T[len(w)][W]
    else:
        celdas, mejor = len(w) * (W + 1), "(no se corre; celdas = n(W+1))"
    if Nb is None:
        Nb, Cb = N, celdas
    print(f"  {'x10^' + str(j):>9} {W:>10} {N:>9} {celdas:>12} {celdas / Cb:>12.1f} {N - Nb:>11}  {mejor}")
print("  Multiplicar los pesos y la capacidad (6 numeros) por 10 agrega ~3,3 bits a cada uno: ~20 bits en total por cada factor 10,")
print("  pero multiplica por 10 el costo. Un algoritmo cuyo costo depende de la unidad elegida no es polinomial en el tamano.")

print()
print("=== 8. Otra pseudopolinomial: la tabla por valores, O(n V) con V = suma de valores ===")


def mochila_por_valores(w, v, W):
    """P[u] = peso minimo para alcanzar valor exactamente u con los objetos vistos (u = 0..V). Devuelve (mejor valor, celdas)."""
    V = sum(v)
    INF = float("inf")
    P = [0] + [INF] * V
    celdas = 0
    for wi, vi in zip(w, v):
        for u in range(V, vi - 1, -1):
            celdas += 1
            if P[u - vi] + wi < P[u]:
                P[u] = P[u - vi] + wi
    return max(u for u in range(V + 1) if P[u] <= W), celdas


ok = 0
for _ in range(2000):
    n = random.randint(1, 8)
    w = [random.randint(1, 20) for _ in range(n)]
    v = [random.randint(1, 25) for _ in range(n)]
    W = random.randint(0, 60)
    assert mochila_por_valores(w, v, W)[0] == mochila_fila(w, v, W)[0]
    ok += 1
print(f"  {ok} instancias: la tabla por valores == la tabla por peso")
n = 6
w = [random.randint(1, 20) for _ in range(n)]
v_chico = [random.randint(1, 20) for _ in range(n)]
v_grande = [x * 10 ** 6 for x in v_chico]
W = 10 ** 6
print(f"  pesos chicos, capacidad W = 10^6: tabla por peso: {mochila_fila(w, v_chico, W)[1]} actualizaciones; "
      f"tabla por valores con V = {sum(v_chico)}: {mochila_por_valores(w, v_chico, W)[1]} (mucho menos)")
print(f"  valores grandes (x10^6, V = {sum(v_grande)}), W = 1000: por peso {mochila_fila(w, v_grande, 1000)[1]} actualizaciones, "
      f"por valores {mochila_por_valores(w, v_grande, 1000)[1]} (mucho mas)")
print("  Cada una es pseudopolinomial en SU parametro: elegir bien depende de cual es chico.")

print()
print("=== 9. La idea del esquema de aproximacion: escalar los valores (solo como idea) ===")
eps = 0.1
peor = 1.0
for _ in range(300):
    n = random.randint(5, 25)
    w = [random.randint(1, 40) for _ in range(n)]
    W = random.randint(40, 300)
    v = [random.randint(1, 10 ** 9) for _ in range(n)]
    vmax = max(vi for wi, vi in zip(w, v) if wi <= W)
    mu = eps * vmax / n
    vs = [int(vi // mu) for vi in v]
    # optimo con valores escalados (tabla por peso con valores escalados, y recuperacion del conjunto)
    T, _c = mochila_tabla(w, vs, W)
    c, S = W, []
    for i in range(n, 0, -1):
        if T[i][c] != T[i - 1][c]:
            S.append(i - 1)
            c -= w[i - 1]
    aprox = sum(v[i] for i in S)
    opt = mochila_fila(w, v, W)[0]
    peor = min(peor, aprox / opt)
    assert aprox >= (1 - eps) * opt
print(f"  300 instancias con valores hasta 10^9, eps = {eps}: valor de la solucion escalada / optimo >= {peor:.4f} (garantia: >= {1 - eps})")
print("  Con los valores escalados V' = O(n^2/eps), la tabla por valores cuesta O(n^3/eps): polinomial en n y 1/eps.")

with open("ej11_mochila.dat", "w") as fh:
    fh.write("N celdas\n")
    for k, N, c in filas:
        fh.write(f"{N} {c}\n")
with open("ej11_primo.dat", "w") as fh:
    fh.write("bits div\n")
    for b, c in datos_primo:
        fh.write(f"{b} {c}\n")
