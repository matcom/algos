import importlib
import random
from itertools import combinations

mz = importlib.import_module("ejercicio-09-mezcla")
merge, merge_optimized = mz.merge, mz.merge_optimized


def intercalados(n):
    # todas las formas de repartir 0..2n-1 en dos listas ordenadas de largo n
    for lugares in combinations(range(2 * n), n):
        A = list(lugares)
        B = [v for v in range(2 * n) if v not in lugares]
        yield A, B


def perfecta(n):
    # la entrada del adversario: a1 < b1 < a2 < b2 < ... < an < bn
    return list(range(0, 2 * n, 2)), list(range(1, 2 * n, 2))


# ===============================================================
print("Prueba 1: dos trazas")
for A, B in [([1, 5, 9], [2, 3, 4]), perfecta(3)]:
    log = []
    R, c = merge_optimized(A, B, log)
    pares = "  ".join(f"{a}vs{b}" for a, b in log)
    estado = "bien" if R == sorted(A + B) else "MAL"
    print(f"A = {A}  B = {B}")
    print(f"  compara: {pares}")
    print(f"  resultado: {R}  ({c} comparaciones)  {estado}")
assert merge_optimized([1, 5, 9], [2, 3, 4])[0] == [1, 2, 3, 4, 5, 9]
assert merge_optimized(*perfecta(3))[0] != sorted(sum(perfecta(3), []))
print("OK\n")

# ===============================================================
print("Prueba 2: peor caso exacto, probando todas las formas de intercalar")
print(f"{'n':>3} {'intercalados':>13} {'optimizada':>11} {'mezcla normal':>14} {'cota 2n - 1':>12}")
for n in range(1, 9):
    peor_opt = peor_normal = 0
    for A, B in intercalados(n):
        peor_opt = max(peor_opt, merge_optimized(A, B)[1])
        peor_normal = max(peor_normal, merge(A, B)[1])
    print(f"{n:>3} {sum(1 for _ in intercalados(n)):>13} {peor_opt:>11} {peor_normal:>14} {2 * n - 1:>12}")
    assert peor_opt == max(0, 2 * n - 2) and peor_normal == 2 * n - 1
print("OK\n")

# ===============================================================
print("Prueba 3: la entrada del adversario, intercalada perfecta")
for n in [1, 2, 5, 10, 100]:
    A, B = perfecta(n)
    log = []
    R, c = merge_optimized(A, B, log)
    vecinos = {(2 * k, 2 * k + 1) for k in range(n)} | {(2 * k + 2, 2 * k + 1) for k in range(n - 1)}
    comparados = {(a, b) for a, b in log}
    faltan = sorted(vecinos - comparados)
    print(f"  n = {n:>3}: {c:>3} comparaciones, pares de vecinos sin comparar: {faltan}, "
          f"resultado {'bien' if R == sorted(A + B) else 'MAL'}")
    esperado = [(0, 1)] if n == 1 else [(2 * n - 2, 2 * n - 3), (2 * n - 2, 2 * n - 1)]
    assert faltan == esperado and c == max(0, 2 * n - 3) and R != sorted(A + B)
print("OK\n")

# ===============================================================
print("Prueba 4: el intercambio del adversario")
# en la intercalada perfecta se cambian a_n y b_n: las dos listas siguen ordenadas,
# la optimizada recibe las mismas respuestas y devuelve el mismo orden de posiciones
for n in [3, 6, 20]:
    A, B = perfecta(n)
    A2, B2 = A[:-1] + [B[-1]], B[:-1] + [A[-1]]
    assert A2 == sorted(A2) and B2 == sorted(B2)
    log1, log2 = [], []
    R1, _ = merge_optimized(A, B, log1)
    R2, _ = merge_optimized(A2, B2, log2)
    resp1 = [a <= b for a, b in log1]
    resp2 = [a <= b for a, b in log2]
    bien1, bien2 = R1 == sorted(A + B), R2 == sorted(A2 + B2)
    print(f"  n = {n:>2}: mismas respuestas: {resp1 == resp2}, "
          f"bien en la original: {bien1}, bien en la intercambiada: {bien2}")
    assert resp1 == resp2 and bien1 != bien2
print("OK\n")

# ===============================================================
print("Prueba 5: cuando falla, segun el generador de pruebas")


def falla(A, B):
    return merge_optimized(A, B)[0] != sorted(A + B)


rng = random.Random(5)


def al_azar(n):
    v = rng.sample(range(10 * n), 2 * n)
    return sorted(v[:n]), sorted(v[n:])


def mayor_en(lista, n):
    A, B = al_azar(n)
    if (max(A) > max(B)) != (lista == "A"):
        A, B = B, A
    return A, B


generadores = {
    "el mayor esta en A": lambda: mayor_en("A", rng.randint(1, 30)),
    "al azar": lambda: al_azar(rng.randint(1, 30)),
    "el mayor esta en B": lambda: mayor_en("B", rng.randint(1, 30)),
}
print(f"{'pruebas':>20} {'casos':>6} {'fallos':>8}")
for nombre, generar in generadores.items():
    f = sum(falla(*generar()) for _ in range(4000)) / 40
    print(f"{nombre:>20} {4000:>6} {f:>7.1f}%")
# falla exactamente cuando el mayor de todos esta en B
for n in range(1, 8):
    for A, B in intercalados(n):
        assert falla(A, B) == (max(B) > max(A))
print("en todos los intercalados con n <= 7: falla si y solo si el mayor de todos esta en B")
print("OK")
