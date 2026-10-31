import math
from functools import lru_cache


def mayor_n(costo, presupuesto):
    # el mayor n con costo(n) <= presupuesto (igual que en la conferencia)
    alto = 2
    while costo(alto) <= presupuesto:
        alto *= 2
    bajo = alto // 2
    while bajo + 1 < alto:
        medio = (bajo + alto) // 2
        if costo(medio) <= presupuesto:
            bajo = medio
        else:
            alto = medio
    return bajo


def factor(costo, presupuesto, veces=1000):
    return mayor_n(costo, veces * presupuesto) / mayor_n(costo, presupuesto)


def factor_formula(n, veces=1000):
    # resuelve k = veces * log n / (log n + log k) probando valores
    k = veces
    for _ in range(50):
        k = veces * math.log2(n) / (math.log2(n) + math.log2(k))
    return k


def cuadratico(n):
    return n * n


def n_log_n(n):
    return n * math.log2(n)


# Algoritmos de verdad, contando comparaciones en el peor caso
def selection_sort(n):
    return n * (n - 1) // 2


@lru_cache(maxsize=None)
def merge_sort(n):
    if n <= 1:
        return 0
    return merge_sort((n + 1) // 2) + merge_sort(n // 2) + n - 1


hora = 3600 * 10**9

# ===============================================================
print("=========== CASO n^2 ===========\n")

print("Prueba 1: el factor no depende del presupuesto")
print(f"{'presupuesto':>12} {'n antes':>14} {'n despues':>16} {'factor':>8}")
for e in range(6, 16, 3):
    p = 10**e
    antes = mayor_n(cuadratico, p)
    despues = mayor_n(cuadratico, 1000 * p)
    f = despues / antes
    print(f"{'10^' + str(e):>12} {antes:>14,} {despues:>16,} {f:>8.2f}")
    assert abs(f - math.sqrt(1000)) < 0.1
print("OK\n")

print("Prueba 2: selection sort de verdad (una hora a 10^9 op/s)")
antes = mayor_n(selection_sort, hora)
despues = mayor_n(selection_sort, 1000 * hora)
f = despues / antes
print(f"n antes = {antes:,}  n despues = {despues:,}  factor = {f:.1f}")
assert abs(f - math.sqrt(1000)) < 0.1
print("OK\n")

print("Prueba 3: otras mejoras de velocidad, el factor es sqrt(veces)")
print(f"{'mas rapida':>11} {'factor':>8} {'sqrt':>8}")
for veces in [10, 100, 1000, 10**6]:
    f = factor(cuadratico, hora, veces)
    print(f"{str(veces) + 'x':>11} {f:>8.1f} {math.sqrt(veces):>8.1f}")
    assert abs(f - math.sqrt(veces)) / math.sqrt(veces) < 0.01
print("OK\n")

# ===============================================================
print("=========== CASO n log n ===========\n")

print("Prueba 4: busqueda binaria contra la formula y la cota de abajo")
print(f"{'presupuesto':>12} {'n antes':>16} {'busqueda':>9} {'formula':>8} {'cota inf':>9}")
for e in range(4, 17, 2):
    p = 10**e
    antes = mayor_n(n_log_n, p)
    f = factor(n_log_n, p)
    formula = factor_formula(antes)
    cota = 1000 * math.log2(antes) / (math.log2(antes) + math.log2(1000))
    print(f"{'10^' + str(e):>12} {antes:>16,} {f:>9.1f} {formula:>8.1f} {cota:>9.1f}")
    assert abs(f - formula) < 1   # la formula coincide con la busqueda
    assert cota < f < 1000        # el factor queda entre las dos cotas
print("OK\n")

print("Prueba 5: merge sort de verdad (una hora a 10^9 op/s)")
antes = mayor_n(merge_sort, hora)
despues = mayor_n(merge_sort, 1000 * hora)
f = despues / antes
print(f"n antes = {antes:,}  n despues = {despues:,}  factor = {f:.1f}")
assert abs(f - 790) / 790 < 0.02
print("OK\n")

print("Prueba 6: otras mejoras de velocidad, el factor queda por debajo")
print(f"{'mas rapida':>11} {'factor':>10}")
for veces in [10, 100, 1000, 10**6]:
    f = factor(n_log_n, hora, veces)
    print(f"{str(veces) + 'x':>11} {f:>10.1f}")
    assert f < veces
print("OK")
