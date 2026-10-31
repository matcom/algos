import importlib
import random
import time

mochila = importlib.import_module("ejercicio-11-mochila")
knapsack, knapsack_table, brute_force, input_bits = (
    mochila.knapsack, mochila.knapsack_table, mochila.brute_force, mochila.input_bits)

segundos_por_ano = 3600 * 24 * 365

# ===============================================================
print("Prueba 1: el ejemplo hecho a mano")
weights, values, W = [1, 3, 4, 5], [1, 4, 5, 7], 7
tabla = knapsack_table(weights, values, W)
print("objetos (peso, valor):", list(zip(weights, values)), " capacidad W =", W)
print(f"{'':>14}" + "".join(f"{c:>4}" for c in range(W + 1)) + "   <- capacidad c")
for i, fila in enumerate(tabla):
    nombre = "ninguno" if i == 0 else f"hasta el {i}"
    print(f"{nombre:>14}" + "".join(f"{x:>4}" for x in fila))
print("respuesta:", tabla[-1][-1])
assert tabla[-1][-1] == 9 == knapsack(weights, values, W)
print("OK\n")

# ===============================================================
print("Prueba 2: casos borde")
casos = [
    (([], [], 10), 0, "sin objetos"),
    (([3, 4], [5, 6], 0), 0, "capacidad 0"),
    (([8], [100], 7), 0, "un objeto que no cabe"),
    (([7], [100], 7), 100, "un objeto que cabe justo"),
    (([1, 2, 3], [1, 2, 3], 100), 6, "caben todos"),
    (([5, 5], [3, 3], 9), 3, "dos iguales y solo cabe uno"),
    (([4, 3, 3], [5, 4, 4], 6), 8, "el mas valioso no es parte de la respuesta"),
]
for (w, v, cap), esperado, texto in casos:
    assert knapsack(w, v, cap) == esperado, texto
    print(f"  {texto:<46}OK")
print()

# ===============================================================
print("Prueba 3: contra el oraculo (fuerza bruta, 2^n subconjuntos)")
random.seed(3)
malos = 0
for _ in range(2000):
    n = random.randint(0, 10)
    w = [random.randint(1, 30) for _ in range(n)]
    v = [random.randint(1, 50) for _ in range(n)]
    cap = random.randint(0, 100)
    malos += knapsack(w, v, cap) != brute_force(w, v, cap)
print(f"2000 instancias con n de 0 a 10: {malos} fallos")
assert malos == 0
print("OK\n")

# ===============================================================
print("Prueba 4: celdas segun los bits de W (n = 3 objetos fijos)")
random.seed(4)
print(f"{'bits de W':>10} {'W':>10} {'bits entrada':>13} {'celdas':>12} {'tiempo':>9}")
anterior = None
for k in range(8, 21, 2):
    W = 2 ** k - 1                             # el mayor numero de k bits
    w = [random.randint(1, W) for _ in range(3)]
    v = [random.randint(1, 1000) for _ in range(3)]
    stats = {}
    inicio = time.perf_counter()
    knapsack(w, v, W, stats)
    seg = time.perf_counter() - inicio
    print(f"{k:>10} {W:>10,} {input_bits(w, v, W):>13} {stats['cells']:>12,} {seg:>8.3f}s")
    assert stats["cells"] == 4 * (W + 1)
    if anterior is not None:
        assert stats["cells"] == 4 * anterior   # 2 bits mas -> 4 veces mas celdas
    anterior = stats["cells"]
print("OK\n")

# ===============================================================
print("Prueba 5: la misma instancia escrita con numeros mas grandes")
w, v, W = [1, 3, 4, 5], [1, 4, 5, 7], 7
print(f"{'factor':>8} {'W':>8} {'respuesta':>10} {'bits entrada':>13} {'celdas':>10}")
for f in [1, 10, 100, 1000]:
    wf, Wf = [x * f for x in w], W * f
    stats = {}
    r = knapsack(wf, v, Wf, stats)
    print(f"{f:>8} {Wf:>8,} {r:>10} {input_bits(wf, v, Wf):>13} {stats['cells']:>10,}")
    assert r == 9
print("OK\n")

# ===============================================================
print("Prueba 6: mochila contra primalidad por division, a 10^9 operaciones por segundo")


def tiempo(ops):
    s = ops / 10**9
    for nombre, unidad in [("anos", segundos_por_ano), ("dias", 86400), ("horas", 3600),
                           ("minutos", 60)]:
        if s >= unidad:
            return f"{s / unidad:.3g} {nombre}"
    return f"{s:.3g} segundos"


print(f"{'bits':>5} {'primalidad (2^(b/2))':>24} {'mochila n=100 (100 * 2^b)':>28}")
for b in [16, 32, 64, 128]:
    print(f"{b:>5} {tiempo(2 ** (b // 2)):>24} {tiempo(100 * 2 ** b):>28}")
print("OK")
