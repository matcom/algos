"""Ejercicio 2 ★ — Búsqueda binaria: invariante, potencial y cota de información (C3, C5)

Código de validación de ejercicio-02.md.
Ejecutar con: python ejercicio-02.py
"""


# -------------------- Parte 1 --------------------

def busqueda_binaria(A, x, comparar):
    """Devuelve ("está", posición) o ("hueco", número de hueco)."""
    lo, hi = 0, len(A)              # invariante: si x está, está en A[lo:hi]
    while lo < hi:
        m = (lo + hi) // 2
        r = comparar(x, A[m])       # -1, 0 o 1
        if r == 0:
            return ("está", m)
        if r < 0:
            hi = m
        else:
            lo = m + 1
    return ("hueco", lo)

# -------------------- Parte 2 --------------------

import math, random, bisect

class Contador:
    def __init__(self):
        self.n = 0
    def __call__(self, x, y):
        self.n += 1
        return (x > y) - (x < y)

def oraculo(A, x):
    if x in A:
        return ("está", A.index(x))
    return ("hueco", bisect.bisect_left(A, x))

# -------------------- Parte 3 --------------------

incorrectas, peores_distintos = 0, 0
for n in range(0, 65):
    A = list(range(0, 2 * n, 2))              # 0, 2, 4, ...: los impares caen en huecos
    peor = 0
    for x in range(-1, 2 * n + 1):
        c = Contador()
        incorrectas += busqueda_binaria(A, x, c) != oraculo(A, x)
        peor = max(peor, c.n)
    peores_distintos += peor != math.ceil(math.log2(n + 1))
if incorrectas == peores_distintos == 0:
    print("correcta en todos los casos, y el peor caso es exactamente ceil(log2(n+1)) para n = 0..64")
else:
    print(f"{incorrectas} búsquedas incorrectas y {peores_distintos} valores de n con peor caso "
          f"distinto de ceil(log2(n+1)), para n = 0..64")

# -------------------- Parte 4 --------------------

def busqueda_vigilada(A, x):
    lo, hi = 0, len(A)
    while lo < hi:
        assert all(A[j] < x for j in range(lo)) and all(A[j] > x for j in range(hi, len(A)))
        phi = hi - lo
        m = (lo + hi) // 2
        if x == A[m]:
            return ("está", m)
        if x < A[m]:
            hi = m
        else:
            lo = m + 1
        assert hi - lo <= phi // 2              # el potencial al menos se divide por 2
    assert lo == hi
    return ("hueco", lo)

random.seed(2)
fallos = 0
for _ in range(3000):
    A = sorted(random.sample(range(1000), random.randint(0, 60)))
    x = random.randrange(-5, 1005)
    try:
        fallos += busqueda_vigilada(A, x) != oraculo(A, x)
    except AssertionError:                     # se rompió el invariante o el potencial
        fallos += 1
if fallos == 0:
    print("invariante y potencial comprobados en 3000 búsquedas al azar")
else:
    print(f"{fallos} de 3000 búsquedas al azar fallan el invariante, el potencial o el oráculo")

# -------------------- Parte 5 --------------------

print(f"{'n':>6} {'huecos':>7} {'peor caso medido':>17} {'ceil(log2(n+1))':>16}")
for n in [1, 7, 8, 100, 1000, 10**5]:
    A = list(range(0, 2 * n, 2))
    peor = 0
    for x in range(-1, 2 * n + 1, 2):         # un valor por hueco
        c = Contador()
        busqueda_binaria(A, x, c)
        peor = max(peor, c.n)
    print(f"{n:>6} {n + 1:>7} {peor:>17} {math.ceil(math.log2(n + 1)):>16}")

# -------------------- Parte 6 --------------------

def busqueda_mala(A, x, max_vueltas=1000):
    lo, hi = 0, len(A)
    vueltas = 0
    while lo < hi:
        vueltas += 1
        if vueltas > max_vueltas:
            return "no termina"
        m = (lo + hi) // 2
        if x == A[m]:
            return ("está", m)
        if x < A[m]:
            hi = m
        else:
            lo = m                                 # el error: debería ser m + 1
    return ("hueco", lo)

print(busqueda_mala([10], 20), "  <- con A = [10], x = 20: lo=0, hi=1, m=0 y lo no se mueve")
