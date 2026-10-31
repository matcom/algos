import importlib
import math
import random
from itertools import combinations

md = importlib.import_module("ejercicio-07-mediana")
median_two, median_two_bug, valid_cuts = md.median_two, md.median_two_bug, md.valid_cuts


def oraculo(A, B):
    return sorted(A + B)[len(A) - 1]


def par_al_azar(n, rng, rango=None):
    rango = rango or 10 * n
    return sorted(rng.randint(0, rango) for _ in range(n)), sorted(rng.randint(0, rango) for _ in range(n))


def texto(v):
    return "-inf" if v == -md.INF else ("inf" if v == md.INF else str(v))


# ===============================================================
print("Prueba 1: la traza del ejemplo")
A = [1, 3, 8, 9, 15]
B = [7, 11, 18, 19, 21]
trace = []
r = median_two(A, B, trace)
print("A =", A, " B =", B, " (n = 5: el 5o menor de los 10)")
print(f"{'lo':>3} {'hi':>3} {'i':>3} {'j':>3} {'A[i-1]':>7} {'A[i]':>5} {'B[j-1]':>7} {'B[j]':>5}   decision")
for lo, hi, i, j, al, ar, bl, br in trace:
    if al > br:
        dec = "A[i-1] > B[j]: demasiados de A"
    elif bl > ar:
        dec = "B[j-1] > A[i]: muy pocos de A"
    else:
        dec = f"corte valido: max({texto(al)}, {texto(bl)}) = {max(al, bl)}"
    print(f"{lo:>3} {hi:>3} {i:>3} {j:>3} {texto(al):>7} {texto(ar):>5} {texto(bl):>7} {texto(br):>5}   {dec}")
print("todos juntos y ordenados:", sorted(A + B), "-> el 5o es", oraculo(A, B))
assert r == 9 == oraculo(A, B)
print("OK\n")

# ===============================================================
print("Prueba 2: casos borde")
casos = [
    ([4], [9], "n = 1"),
    ([1, 2, 3], [7, 8, 9], "todo A menor que todo B"),
    ([7, 8, 9], [1, 2, 3], "todo B menor que todo A"),
    ([1, 5, 9], [1, 5, 9], "los dos arreglos iguales"),
    ([2, 2, 2, 2], [2, 2, 2, 2], "todos iguales"),
    ([-9, -3, 0], [-5, 4, 6], "negativos"),
    ([1, 3, 5, 7], [2, 4, 6, 8], "intercalados"),
]
for a, b, txt in casos:
    assert median_two(a, b) == oraculo(a, b), txt
    print(f"  {txt:<30}OK")
print()

# ===============================================================
print("Prueba 3: el invariante vigilado")
# antes de cada vuelta: hay un corte valido en [lo, hi]
rng = random.Random(3)
vueltas = 0
for _ in range(3000):
    n = rng.randint(1, 30)
    A, B = par_al_azar(n, rng, rango=rng.choice([3, 10 * n]))
    validos = valid_cuts(A, B)
    assert validos                                 # siempre existe alguno
    trace = []
    median_two(A, B, trace)
    for lo, hi, *_ in trace:
        assert any(lo <= c <= hi for c in validos)
        vueltas += 1
print(f"invariante comprobado en {vueltas:,} vueltas, sin fallos")
print("OK\n")

# ===============================================================
print("Prueba 4: contra el oraculo (ordenar todo y tomar el n-esimo)")
rng = random.Random(4)
print(f"{'valores':>26} {'casos':>6} {'fallos':>7}")
for nombre, rango in [("al azar, casi sin repetir", None), ("con muchos repetidos (0..3)", 3)]:
    malos = 0
    for _ in range(4000):
        n = rng.randint(1, 50)
        A, B = par_al_azar(n, rng, rango)
        malos += median_two(A, B) != oraculo(A, B)
    print(f"{nombre:>26} {4000:>6} {malos:>7}")
    assert malos == 0
print("OK\n")

# ===============================================================
print("Prueba 5: el costo, comparaciones en el peor caso")
rng = random.Random(5)
print(f"{'n':>8} {'peor medido':>12} {'2*(floor(log2(n+1))+1)':>23} {'cota ceil(log2 2n)':>19} {'mezclar':>9}")
for n in [1, 2, 4, 10, 100, 1000, 10 ** 5]:
    peor = 0
    for _ in range(300 if n < 10 ** 5 else 30):
        A, B = par_al_azar(n, rng)
        stats = {}
        median_two(A, B, stats=stats)
        peor = max(peor, stats["comparisons"])
    tope = 2 * (math.floor(math.log2(n + 1)) + 1)
    print(f"{n:>8,} {peor:>12} {tope:>23} {math.ceil(math.log2(2 * n)):>19} {n:>9,}")
    assert peor <= tope
print("OK\n")

# ===============================================================
print("Prueba 6: cualquiera de los 2n elementos puede ser la respuesta")
for n in [1, 2, 3, 4, 5]:
    posiciones = set()
    for lugares_de_A in combinations(range(2 * n), n):   # todas las formas de intercalar
        A = list(lugares_de_A)
        B = [v for v in range(2 * n) if v not in lugares_de_A]
        m = median_two(A, B)
        posiciones.add(("A", A.index(m)) if m in A else ("B", B.index(m)))
    print(f"  n = {n}: {math.comb(2 * n, n):>3} intercalados, la respuesta aparece en "
          f"{len(posiciones):>2} posiciones distintas (2n = {2 * n})")
    assert len(posiciones) == 2 * n
print("OK\n")

# ===============================================================
print("Prueba 7: olvidar los centinelas de la izquierda")
rng = random.Random(7)
print(f"{'entradas':>30} {'casos':>6} {'fallos':>8}")
generadores = {
    "al azar, n de 20 a 50": lambda: par_al_azar(rng.randint(20, 50), rng),
    "al azar, n de 1 a 3": lambda: par_al_azar(rng.randint(1, 3), rng),
    "todo B menor que todo A": lambda: (lambda n: (sorted(rng.sample(range(100, 200), n)),
                                                   sorted(rng.sample(range(0, 100), n))))(rng.randint(2, 50)),
}
for nombre, generar in generadores.items():
    malos = 0
    for _ in range(3000):
        A, B = generar()
        malos += median_two_bug(A, B) != oraculo(A, B)
    print(f"{nombre:>30} {3000:>6} {100 * malos / 3000:>7.1f}%")
A, B = [7, 8, 9], [1, 2, 3]
print("contraejemplo: A =", A, " B =", B, "-> sin centinelas:", median_two_bug(A, B), " correcto:", oraculo(A, B))
assert median_two_bug(A, B) != oraculo(A, B)
print("OK")
