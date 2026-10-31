import importlib
import math
import random

par = importlib.import_module("ejercicio-10-par")
closest_pair_sort, closest_pair_grid, has_duplicates = (
    par.closest_pair_sort, par.closest_pair_grid, par.has_duplicates)


class Num:
    # un numero que cuenta cuantas veces se compara (para medir el ordenamiento)
    comparaciones = 0

    def __init__(self, v):
        self.v = v

    def __lt__(self, otro):
        Num.comparaciones += 1
        return self.v < otro.v

    def __sub__(self, otro):
        return self.v - otro.v


# ===============================================================
print("Prueba 1: la traza del ejemplo (sin barajar, para poder seguirla)")
xs = [10, 30, 22, 27, 5, 26]
trace = []
r = closest_pair_grid(xs, shuffle=False, trace=trace)
print(f"primeros dos: {xs[0]} y {xs[1]}, delta = {abs(xs[0] - xs[1])}, celdas de largo {abs(xs[0] - xs[1]) / 2}")
for p, delta, bajo, grid in trace:
    accion = "delta bajo: se reconstruye la rejilla" if bajo else "delta no cambia: se guarda"
    celdas = ", ".join(f"{c}:{q}" for c, q in sorted(grid.items()))
    print(f"  inserta {p:>3}: delta = {delta:>4}, {accion:<38} rejilla {{{celdas}}}")
print("resultado:", r, " ordenando:", closest_pair_sort(xs))
assert r == 1 == closest_pair_sort(xs)
print("OK\n")

# ===============================================================
print("Prueba 2: casos borde")
casos = [
    ([3, 8], 5, "dos puntos"),
    ([4, 9, 4], 0, "un repetido: distancia 0"),
    ([-7, -2, 3, 15], 5, "negativos"),
    ([0, 10, 20, 30, 40], 10, "equiespaciados: todos los pares empatan"),
    ([0.1, 0.35, 0.3, 0.9], 0.05, "decimales"),
    ([10 ** 9, 1, 10 ** 9 + 2, 500], 2, "rango enorme"),
]
for xs, esperado, txt in casos:
    r = closest_pair_grid(xs)
    assert abs(r - esperado) < 1e-9 and abs(r - closest_pair_sort(xs)) < 1e-9, txt
    print(f"  {txt:<42}OK")
print()

# ===============================================================
print("Prueba 3: el invariante de la rejilla vigilado")
# despues de cada insercion: a lo sumo un punto por celda, y delta es la distancia
# minima entre los puntos ya insertados
rng = random.Random(3)
pasos = 0
for _ in range(500):
    n = rng.randint(3, 40)
    xs = rng.sample(range(10 ** 6), n)
    trace = []
    closest_pair_grid(xs, seed=rng.random(), trace=trace)
    insertados = None
    for k, (p, delta, _, grid) in enumerate(trace):
        assert len(set(grid.values())) == len(grid)            # un punto por celda
        puntos = list(grid.values())
        assert abs(delta - closest_pair_sort(puntos)) < 1e-9   # delta es el minimo de lo insertado
        pasos += 1
print(f"invariante comprobado en {pasos:,} inserciones, sin fallos")
print("OK\n")

# ===============================================================
print("Prueba 4: contra el oraculo (ordenar y mirar vecinos)")
rng = random.Random(4)
print(f"{'puntos':>24} {'casos':>6} {'fallos':>7}")
for nombre, gen in [("enteros sin repetir", lambda n: rng.sample(range(10 ** 6), n)),
                    ("reales al azar", lambda n: [rng.random() for _ in range(n)]),
                    ("enteros con repetidos", lambda n: [rng.randint(0, 3 * n) for _ in range(n)])]:
    malos = 0
    for _ in range(2000):
        xs = gen(rng.randint(2, 200))
        malos += abs(closest_pair_grid(xs, seed=rng.random()) - closest_pair_sort(xs)) > 1e-12
    print(f"{nombre:>24} {2000:>6} {malos:>7}")
    assert malos == 0
print("OK\n")

# ===============================================================
print("Prueba 5: el costo, reconstrucciones y trabajo")
rng = random.Random(5)
print(f"{'n':>8} {'reconstrucciones':>17} {'2 ln n':>7} {'trabajo rejilla / n':>20} "
      f"{'comparaciones ordenando / n':>28}")
for n in [1_000, 10_000, 100_000]:
    xs = [rng.random() for _ in range(n)]
    rec = trabajo = 0
    for s in range(5):
        stats = {}
        closest_pair_grid(xs, seed=s, stats=stats)
        rec += stats["rebuilds"]
        trabajo += stats["lookups"] + stats["rebuilt_points"]
    Num.comparaciones = 0
    closest_pair_sort([Num(x) for x in xs])
    print(f"{n:>8,} {rec / 5:>17.1f} {2 * math.log(n):>7.1f} {trabajo / 5 / n:>20.1f} "
          f"{Num.comparaciones / n:>28.1f}")
print("OK\n")

# ===============================================================
print("Prueba 6: la reduccion, distincion de elementos con el par mas cercano")
rng = random.Random(6)
malos = 0
for _ in range(3000):
    n = rng.randint(2, 100)
    xs = [rng.randint(0, 5 * n) for _ in range(n)]
    malos += has_duplicates(xs) != (len(set(xs)) < n)
print(f"3000 listas: 'hay repetidos' segun el par mas cercano, contra contar con un conjunto: {malos} fallos")
assert malos == 0
print("OK\n")

# ===============================================================
print("Prueba 7: sin barajar, con un orden de insercion malo")
# p_k = 1 - 2^-k: cada punto nuevo esta mas cerca del anterior que todos los de antes,
# asi que si se insertan en orden delta baja en cada paso
print(f"{'n':>4} {'reconstrucciones sin barajar':>29} {'barajando (promedio)':>21} {'puntos reinsertados sin barajar':>32}")
for n in [10, 20, 40]:
    xs = [1 - 2 ** -k for k in range(n)]
    s1 = {}
    closest_pair_grid(xs, shuffle=False, stats=s1)
    total = 0
    for s in range(50):
        s2 = {}
        closest_pair_grid(xs, seed=s, stats=s2)
        total += s2["rebuilds"]
    print(f"{n:>4} {s1['rebuilds']:>29} {total / 50:>21.1f} {s1['rebuilt_points']:>32}")
    assert s1["rebuilds"] == n - 2
print("OK")
