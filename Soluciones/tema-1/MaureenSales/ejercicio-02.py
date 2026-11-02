"""Ejercicio 2 — Búsqueda binaria: invariante, potencial y cota de información

Código extraído de ejercicio-02.md, en el mismo orden en que aparece allí.
Ejecutar con:  python ejercicio-02.py
La salida esperada es la de la sección "Salida" de ejercicio-02.md.
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")   # para que la consola de Windows imprima δ, ≤, ⌈⌉...

# ----------------------------------------------------------------------
# Del md, sección: 2. Algoritmo
# ----------------------------------------------------------------------

def busqueda_binaria(A, x, comparar):
    """Devuelve ("está", posición) o ("hueco", número de hueco)."""
    lo, hi = 0, len(A)               # invariante: si x está, está en A[lo:hi]
    while lo < hi:
        m = (lo + hi) // 2
        r = comparar(x, A[m])        # -1, 0 o 1
        if r == 0:
            return ("está", m)
        if r < 0:
            hi = m
        else:
            lo = m + 1
    return ("hueco", lo)


# ----------------------------------------------------------------------
# Del md, sección: 8. Casos de prueba
# ----------------------------------------------------------------------

import bisect, itertools, math, random

def comparar_contado(contador):
    def comparar(x, y):
        contador[0] += 1
        return (x > y) - (x < y)
    return comparar

def busqueda_vigilada(A, x):
    """La misma búsqueda, comprobando (I+) y el potencial en cada vuelta."""
    lo, hi = 0, len(A)
    while lo < hi:
        assert all(A[k] < x for k in range(lo)), "falla (I+) a la izquierda"
        assert all(A[k] > x for k in range(hi, len(A))), "falla (I+) a la derecha"
        phi = hi - lo
        m = (lo + hi) // 2
        if x == A[m]:
            return ("está", m)
        if x < A[m]:
            hi = m
        else:
            lo = m + 1
        assert 0 <= hi - lo <= phi // 2, "el potencial no se dividió por 2"
    return ("hueco", lo)

def esperado(A, x):
    h = bisect.bisect_left(A, x)
    return ("está", h) if h < len(A) and A[h] == x else ("hueco", h)

# 1) y 2) exhaustivo: todos los arreglos estrictamente crecientes con valores pares en 0..12
casos = 0
for n in range(0, 8):
    for A in itertools.combinations(range(0, 13, 2), n):
        A = list(A)
        for x in range(-1, 14):                     # pares: presentes o no; impares: en huecos
            c = [0]
            assert busqueda_binaria(A, x, comparar_contado(c)) == esperado(A, x)
            assert busqueda_vigilada(A, x) == esperado(A, x)
            casos += 1
print(f"exhaustivo: {casos} casos correctos, (I+) y potencial vigilados")

random.seed(2026)
for _ in range(2000):
    A = sorted(random.sample(range(10**6), random.randint(0, 300)))
    x = random.randint(-5, 10**6 + 5)
    assert busqueda_binaria(A, x, comparar_contado([0])) == esperado(A, x)
print("aleatorio: 2000 casos correctos")

# 3) peor caso == ceil(log2(n+1)), sobre x en cada hueco y x igual a cada elemento
print(f"\n{'n':>5} {'peor caso medido':>17} {'ceil(log2(n+1))':>16}")
for n in [1, 2, 3, 6, 7, 8, 100, 1000, 1023, 1024]:
    A = list(range(0, 2 * n, 2))                     # pares; los impares caen en los huecos
    peor = 0
    for x in range(-1, 2 * n):
        c = [0]
        busqueda_binaria(A, x, comparar_contado(c))
        peor = max(peor, c[0])
    cota = math.ceil(math.log2(n + 1))
    print(f"{n:5} {peor:17} {cota:16}")
    assert peor == cota
print("la búsqueda binaria alcanza exactamente la cota del Lema 4")

# 4) el ejercicio 7 de C3: lo = m en lugar de lo = m + 1
def busqueda_lo_igual_m(A, x, max_vueltas=1000):
    lo, hi, vueltas = 0, len(A), 0
    while lo < hi:
        vueltas += 1
        if vueltas > max_vueltas:
            return ("no termina", lo, hi)
        m = (lo + hi) // 2
        if x == A[m]:
            return ("está", m)
        if x < A[m]:
            hi = m
        else:
            lo = m                                   # <- el cambio
    return ("hueco", lo)

encontrada = None
for n in range(1, 5):
    for A in itertools.combinations(range(0, 9, 2), n):
        for x in range(-1, 10):
            r = busqueda_lo_igual_m(list(A), x)
            if r[0] == "no termina":
                encontrada = (list(A), x, r)
                break
        if encontrada: break
    if encontrada: break
A, x, (_, lo, hi) = encontrada
print(f"\nlo = m: la entrada más chica que no termina es A = {A}, x = {x};"
      f" se queda con lo = {lo}, hi = {hi} (potencial {hi - lo})")
assert hi - lo == 1

# 5) variante de dos salidas
def rango(A, x, contador):
    lo, hi = 0, len(A)
    while lo < hi:
        mid = (lo + hi) // 2
        contador[0] += 1
        if A[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo

for n in range(0, 7):
    for A in itertools.combinations_with_replacement(range(4), n):
        A = list(A)
        for x in [-1, 0, 0.5, 1, 1.5, 2, 2.5, 3, 4]:
            assert rango(A, x, [0]) == bisect.bisect_left(A, x)
for n in [1, 7, 8, 1000]:
    A = list(range(n))
    peor = 0
    for x in range(-1, n):                           # las n+1 respuestas posibles
        c = [0]
        rango(A, x + 0.5, c)
        peor = max(peor, c[0])
    assert peor == math.ceil(math.log2(n + 1))
print("variante de dos salidas (con repetidos): correcta y con el mismo peor caso")
