"""Ejercicio 7 — Mediana de dos arreglos ordenados

Código extraído de ejercicio-07.md, en el mismo orden en que aparece allí.
Ejecutar con:  python ejercicio-07.py
La salida esperada es la de la sección "Salida" de ejercicio-07.md.
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")   # para que la consola de Windows imprima δ, ≤, ⌈⌉...

# ----------------------------------------------------------------------
# Del md, sección: 4. Algoritmo
# ----------------------------------------------------------------------

def mediana_dos(A, B, contador=None):
    """n-ésimo menor de A ∪ B, con len(A) == len(B) == n >= 1, ambos ordenados."""
    n = len(A)
    assert len(B) == n >= 1

    def menor(u, v):                       # comparación contada
        if contador is not None: contador[0] += 1
        return u < v

    lo, hi = 0, n
    while lo < hi:                         # invariante: lo <= i* <= hi
        i = (lo + hi) // 2                 # 0 <= i <= n-1, así que A[i] y B[n-1-i] existen
        if menor(A[i], B[n - 1 - i]):      # g(i) verdadero: i* > i
            lo = i + 1
        else:                              # g(i) falso: i* <= i
            hi = i
    i = lo
    j = n - i
    if i == 0: return B[j - 1]
    if j == 0: return A[i - 1]
    return B[j - 1] if menor(A[i - 1], B[j - 1]) else A[i - 1]


# ----------------------------------------------------------------------
# Del md, sección: 8. Casos de prueba
# ----------------------------------------------------------------------

import itertools, math, random

def todas_las_intercalaciones(n):
    """Todas las entradas con valores 1..2n distintos, salvo renombrar: C(2n, n)."""
    for S in itertools.combinations(range(1, 2 * n + 1), n):
        A = list(S)
        B = [v for v in range(1, 2 * n + 1) if v not in S]
        yield A, B

# 1) y 3) exhaustivo + peor caso de comparaciones
print(f"{'n':>3} {'entradas':>9} {'peor caso medido':>17} {'ceil(log2(n+1))+1':>18} {'cota ceil(log2 2n)':>19}")
for n in range(1, 9):
    peor, cuantas = 0, 0
    for A, B in todas_las_intercalaciones(n):
        c = [0]
        assert mediana_dos(A, B, c) == sorted(A + B)[n - 1]
        peor = max(peor, c[0]); cuantas += 1
    cota = math.ceil(math.log2(2 * n))
    garantia = math.ceil(math.log2(n + 1)) + 1
    print(f"{n:3} {cuantas:9} {peor:17} {garantia:18} {cota:19}")
    assert cota <= peor <= garantia

# 2) aleatorio con repetidos y n grande
random.seed(7)
for _ in range(3000):
    n = random.randint(1, 60)
    A = sorted(random.randint(0, 20) for _ in range(n))
    B = sorted(random.randint(0, 20) for _ in range(n))
    assert mediana_dos(A, B) == sorted(A + B)[n - 1]
print("3000 casos aleatorios con repetidos: OK")

# Ejemplo de la ilustración
assert mediana_dos([1, 4, 6, 9, 12], [2, 3, 7, 8, 10]) == 6

# 4) cada uno de los 2n elementos es la mediana de alguna entrada
for n in range(1, 9):
    alcanzados = set()
    for A, B in todas_las_intercalaciones(n):
        m = sorted(A + B)[n - 1]
        alcanzados.add(("A", A.index(m)) if m in A else ("B", B.index(m)))
    assert len(alcanzados) == 2 * n
print("para n = 1..8, las 2n posiciones posibles aparecen como respuesta: la cota de información aplica")

# Escala: n = 10^6, cuántas comparaciones
n = 10**6
A = list(range(0, 2 * n, 2)); B = list(range(1, 2 * n, 2))
c = [0]
r = mediana_dos(A, B, c)
print(f"n = 10^6: mediana = {r}, comparaciones = {c[0]} "
      f"(cota de información = {math.ceil(math.log2(2*n))})")
