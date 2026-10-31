import importlib
import math
import random

pk = importlib.import_module("ejercicio-14-pico")
peak_linear, peak_binary, peak_binary_bug, unimodal = (
    pk.peak_linear, pk.peak_binary, pk.peak_binary_bug, pk.unimodal)


def unimodal_al_azar(n, rng, p=None):
    # valores distintos al azar, ordenados para subir hasta p y bajar despues
    p = rng.randrange(n) if p is None else p
    v = rng.sample(range(10 * n), n)
    v.sort()
    pico = v.pop()                              # el mayor va en el pico
    rng.shuffle(v)
    izq, der = sorted(v[:p]), sorted(v[p:], reverse=True)
    return izq + [pico] + der


def comparaciones(A):
    stats = {}
    peak_binary(A, stats=stats)
    return stats.get("comparisons", 0)


# ===============================================================
print("Prueba 1: la traza del ejemplo")
A = [1, 4, 9, 12, 15, 11, 7, 2]
trace = []
p = peak_binary(A, trace)
print("A =", A)
print(f"{'lo':>4} {'hi':>4} {'m':>4} {'A[m]':>6} {'A[m+1]':>7}   decision")
for lo, hi in trace[:-1]:
    m = (lo + hi) // 2
    dec = "sube: el pico esta a la derecha" if A[m] < A[m + 1] else "baja: el pico es m o esta a la izquierda"
    print(f"{lo:>4} {hi:>4} {m:>4} {A[m]:>6} {A[m + 1]:>7}   {dec}")
print(f"pico en la posicion {p}, valor {A[p]}")
assert p == 4
print("OK\n")

# ===============================================================
print("Prueba 2: casos borde")
casos = [
    ([7], 0, "un solo elemento"),
    ([3, 8], 1, "dos, creciente"),
    ([8, 3], 0, "dos, decreciente"),
    ([1, 2, 3, 4, 5], 4, "todo creciente: el pico es el ultimo"),
    ([5, 4, 3, 2, 1], 0, "todo decreciente: el pico es el primero"),
    ([-9, -4, -1, -6], 2, "negativos"),
]
for arr, esperado, txt in casos:
    assert peak_binary(arr) == esperado, txt
    print(f"  {txt:<42}OK")
print()

# ===============================================================
print("Prueba 3: el invariante vigilado")
rng = random.Random(3)
vueltas = 0
for _ in range(3000):
    n = rng.randint(1, 60)
    A = unimodal_al_azar(n, rng)
    p = A.index(max(A))
    trace = []
    peak_binary(A, trace)
    for lo, hi in trace:
        assert lo <= p <= hi
        vueltas += 1
print(f"invariante comprobado en {vueltas:,} vueltas, sin fallos")
print("OK\n")

# ===============================================================
print("Prueba 4: contra el oraculo (recorrer todo)")
rng = random.Random(4)
malos = 0
for _ in range(5000):
    A = unimodal_al_azar(rng.randint(1, 200), rng)
    malos += peak_binary(A) != peak_linear(A)
print(f"5000 arreglos unimodales al azar: {malos} fallos")
assert malos == 0
print("OK\n")

# ===============================================================
print("Prueba 5: peor caso exacto, probando el pico en todas las posiciones")
print(f"{'n':>6} {'peor caso':>10} {'cota ceil(log2 n)':>18} {'fuerza bruta n - 1':>19}")
for n in [1, 2, 3, 8, 9, 100, 1000, 1024, 1025]:
    peor = max(comparaciones(unimodal(n, p)) for p in range(n))
    cota = math.ceil(math.log2(n))
    print(f"{n:>6} {peor:>10} {cota:>18} {n - 1:>19}")
    assert peor == cota
print("OK\n")

# ===============================================================
print("Prueba 6: cada posicion del pico llega a una hoja distinta (n = 8)")
n = 8
hojas = {}
for p in range(n):
    A = unimodal(n, p)
    trace = []
    peak_binary(A, trace)
    respuestas = "".join("<" if A[(lo + hi) // 2] < A[(lo + hi) // 2 + 1] else ">"
                         for lo, hi in trace[:-1])
    hojas[p] = respuestas
    print(f"  pico en {p}: respuestas {respuestas}")
assert len(set(hojas.values())) == n
print(f"{n} posiciones, {len(set(hojas.values()))} caminos distintos, largo maximo "
      f"{max(len(r) for r in hojas.values())} = ceil(log2 {n})")
print("OK\n")

# ===============================================================
print("Prueba 7: hi = m - 1 en vez de hi = m")
rng = random.Random(7)
print(f"{'pico':>28} {'casos':>6} {'fallos':>8}")
generadores = {
    "en una posicion al azar": lambda n: unimodal_al_azar(n, rng),
    "en el primer elemento": lambda n: unimodal_al_azar(n, rng, p=0),
    "en el ultimo elemento": lambda n: unimodal_al_azar(n, rng, p=n - 1),
}
for nombre, generar in generadores.items():
    malos = 0
    for _ in range(3000):
        A = generar(rng.randint(2, 100))
        malos += peak_binary_bug(A) != peak_linear(A)
    print(f"{nombre:>28} {3000:>6} {100 * malos / 3000:>7.1f}%")
A = [1, 5, 3]
print("contraejemplo: A = [1, 5, 3] ->", peak_binary_bug(A), " (el pico esta en 1)")
assert peak_binary_bug(A) != 1
print("OK\n")

# ===============================================================
print("Prueba 8: si se permiten valores iguales (no estrictamente unimodal)")
rng = random.Random(8)
malos = 0
for _ in range(3000):
    n = rng.randint(3, 60)
    p = rng.randrange(n)
    base = rng.randint(0, 5)
    A = [base] * p + [base + 10] + [base] * (n - p - 1)      # todo igual salvo el pico
    malos += A[peak_binary(A)] != max(A)
print(f"3000 arreglos 'planos con un pico': la busqueda binaria falla en {100 * malos / 3000:.1f}%")
A = [5, 5, 5, 5, 9, 5]
print("contraejemplo: A = [5, 5, 5, 5, 9, 5] -> posicion", peak_binary(A), "valor", A[peak_binary(A)])
print("OK")
