import importlib
import math
import random

bs = importlib.import_module("ejercicio-02-busqueda")
binary_search, binary_search_bug, comparisons = bs.binary_search, bs.binary_search_bug, bs.comparisons

# ===============================================================
print("Prueba 1: las trazas del ejemplo")
A = [3, 8, 15, 21, 30, 42, 57]
for x in [30, 10]:
    trace = []
    r = binary_search(A, x, trace)
    print(f"x = {x}:")
    print(f"{'vuelta':>8} {'lo':>4} {'hi':>4} {'hi - lo':>8}")
    for t, (lo, hi) in enumerate(trace):
        print(f"{t:>8} {lo:>4} {hi:>4} {hi - lo:>8}")
    print("  resultado:", r)
assert binary_search(A, 30) == ("found", 4)
assert binary_search(A, 10) == ("gap", 2)
print("OK\n")

# ===============================================================
print("Prueba 2: casos borde")
casos = [
    ([], 5, ("gap", 0), "arreglo vacio"),
    ([7], 7, ("found", 0), "un elemento, esta"),
    ([7], 3, ("gap", 0), "un elemento, x menor"),
    ([7], 9, ("gap", 1), "un elemento, x mayor"),
    (A, 3, ("found", 0), "x es el primero"),
    (A, 57, ("found", 6), "x es el ultimo"),
    (A, 1, ("gap", 0), "x menor que todos"),
    (A, 99, ("gap", 7), "x mayor que todos"),
]
for arr, x, esperado, txt in casos:
    assert binary_search(arr, x) == esperado, txt
    print(f"  {txt:<30}OK")
print()

# ===============================================================
print("Prueba 3: el invariante vigilado")
# antes de cada vuelta: si x esta en A, esta en A[lo:hi]; y 0 <= lo <= hi <= n
random.seed(3)
vueltas = 0
for _ in range(3000):
    n = random.randint(0, 40)
    A = sorted(random.sample(range(200), n))
    x = random.randrange(-5, 205)
    trace = []
    binary_search(A, x, trace)
    for lo, hi in trace:
        assert 0 <= lo <= hi <= n
        if x in A:
            assert x in A[lo:hi]
        vueltas += 1
print(f"invariante comprobado en {vueltas:,} vueltas, sin fallos")
print("OK\n")

# ===============================================================
print("Prueba 4: contra el oraculo")
random.seed(4)
malos = 0
for _ in range(5000):
    n = random.randint(0, 40)
    A = sorted(random.sample(range(200), n))
    x = random.randrange(-5, 205)
    tipo, k = binary_search(A, x)
    if tipo == "found":
        malos += A[k] != x
    else:
        bien = x not in A and all(a < x for a in A[:k]) and all(a > x for a in A[k:])
        malos += not bien
print(f"5000 busquedas: {malos} fallos")
assert malos == 0
print("OK\n")

# ===============================================================
print("Prueba 5: el potencial hi - lo")
# en cada vuelta el potencial queda en a lo sumo la mitad
random.seed(5)
for _ in range(3000):
    n = random.randint(1, 1000)
    A = list(range(0, 2 * n, 2))
    x = random.randrange(-1, 2 * n + 1)
    trace = []
    binary_search(A, x, trace)
    pot = [hi - lo for lo, hi in trace]
    for antes, despues in zip(pot, pot[1:]):
        assert despues <= antes // 2
print("en 3000 busquedas el potencial siempre baja al menos a la mitad")
print("OK\n")

# ===============================================================
print("Prueba 6: peor caso exacto contra la cota de informacion")
print(f"{'n':>6} {'peor caso':>10} {'ceil(log2(n+1))':>16} {'busqueda lineal':>16}")
for n in [1, 2, 3, 7, 8, 100, 1000, 1023, 1024]:
    A = list(range(0, 2 * n, 2))
    candidatos = list(range(-1, 2 * n + 1))          # todos los elementos y todos los huecos
    peor = max(comparisons(A, x) for x in candidatos)
    cota = math.ceil(math.log2(n + 1))
    print(f"{n:>6} {peor:>10} {cota:>16} {n:>16}")
    assert peor == cota
print("OK\n")

# ===============================================================
print("Prueba 7: lo = m en vez de lo = m + 1")
random.seed(7)
print(f"{'x':>22} {'busquedas':>10} {'no terminan':>12}")
for nombre, presente in [("x esta en el arreglo", True), ("x no esta", False)]:
    colgadas = 0
    for _ in range(3000):
        n = random.randint(1, 40)
        A = sorted(random.sample(range(0, 400, 2), n))
        x = random.choice(A) if presente else random.randrange(1, 400, 2)
        colgadas += binary_search_bug(A, x) is None
    print(f"{nombre:>22} {3000:>10} {colgadas:>12}")
    if presente:
        assert colgadas == 0
print("contraejemplo mas chico: A = [1], x = 2 ->", binary_search_bug([1], 2))
assert binary_search_bug([1], 2) is None
print("OK")
