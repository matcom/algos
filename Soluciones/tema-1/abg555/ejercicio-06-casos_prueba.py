import importlib
import math
import random

mz = importlib.import_module("ejercicio-06-matriz")
search_matrix, search_matrix_top_left, is_sorted_matrix = (
    mz.search_matrix, mz.search_matrix_top_left, mz.is_sorted_matrix)
Adversary, staircase_with_oracle = mz.Adversary, mz.staircase_with_oracle


def matriz_al_azar(n, rng, salto=3):
    # filas y columnas crecientes: cada celda es el maximo de arriba e izquierda, mas algo
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            base = max(M[i - 1][j] if i else 0, M[i][j - 1] if j else 0)
            M[i][j] = base + rng.randint(0, salto)
    return M


def contiene(M, x):
    return any(x in fila for fila in M)


# ===============================================================
print("Prueba 1: la traza del ejemplo")
M = [[1, 4, 7, 11],
     [2, 5, 8, 12],
     [3, 6, 9, 16],
     [10, 13, 14, 17]]
for x in [6, 15]:
    trace = []
    r = search_matrix(M, x, trace)
    pasos = "  ".join(f"({i},{j})={M[i][j]}" for i, j in trace)
    print(f"x = {x:>2}: {pasos}  ->  {r}")
assert search_matrix(M, 6) == (2, 1) and search_matrix(M, 15) is None
print("OK\n")

# ===============================================================
print("Prueba 2: casos borde")
casos = [
    ([], 3, None, "matriz vacia"),
    ([[5]], 5, (0, 0), "1 x 1, esta"),
    ([[5]], 4, None, "1 x 1, no esta"),
    (M, 0, None, "x menor que todos"),
    (M, 99, None, "x mayor que todos"),
    (M, 1, (0, 0), "x en la esquina de arriba a la izquierda"),
    (M, 17, (3, 3), "x en la esquina de abajo a la derecha"),
    ([[1, 2], [2, 2]], 2, (0, 1), "valores repetidos"),
]
for mat, x, esperado, txt in casos:
    assert search_matrix(mat, x) == esperado, txt
    print(f"  {txt:<42}OK")
print()

# ===============================================================
print("Prueba 3: el invariante vigilado")
# en cada paso: si x esta en M, esta en las filas i.. y las columnas ..j
rng = random.Random(3)
pasos = 0
for _ in range(2000):
    n = rng.randint(1, 12)
    M = matriz_al_azar(n, rng)
    x = rng.randint(-1, M[-1][-1] + 1)
    trace = []
    search_matrix(M, x, trace)
    for i, j in trace:
        if contiene(M, x):
            assert any(M[a][b] == x for a in range(i, n) for b in range(0, j + 1))
        pasos += 1
print(f"invariante comprobado en {pasos:,} pasos, sin fallos")
print("OK\n")

# ===============================================================
print("Prueba 4: contra el oraculo")
rng = random.Random(4)
malos = 0
for _ in range(5000):
    n = rng.randint(1, 15)
    M = matriz_al_azar(n, rng)
    x = rng.randint(-1, M[-1][-1] + 1)
    r = search_matrix(M, x)
    malos += (r is None) == contiene(M, x) or (r is not None and M[r[0]][r[1]] != x)
print(f"5000 busquedas en matrices al azar: {malos} fallos")
assert malos == 0
print("OK\n")

# ===============================================================
print("Prueba 5: el potencial y el peor caso")
print(f"{'n':>6} {'peor caso medido':>17} {'2n - 1':>7} {'cota minima n':>14} {'n log2 n':>9} {'n^2':>9}")
for n in [1, 2, 4, 10, 50, 100, 500]:
    A = Adversary(n)
    M = A.matrix()                              # la matriz del adversario, sin x
    trace = []
    search_matrix(M, 0, trace)
    peor = len(trace)
    assert is_sorted_matrix(M) and peor == 2 * n - 1
    print(f"{n:>6} {peor:>17} {2 * n - 1:>7} {n:>14} {n * math.log2(n) if n > 1 else 0:>9.0f} {n * n:>9,}")
rng = random.Random(5)
for _ in range(2000):
    n = rng.randint(1, 20)
    M = matriz_al_azar(n, rng)
    trace = []
    search_matrix(M, rng.randint(-1, M[-1][-1] + 1), trace)
    assert len(trace) <= 2 * n - 1
print("en 2000 busquedas al azar nunca hay mas de 2n - 1 comparaciones")
print("OK\n")

# ===============================================================
print("Prueba 6: el adversario contra varios algoritmos (n = 8)")


def diagonal_principal(n, compare):
    for k in range(n):
        if compare(k, k) == 0:
            return (k, k)
    return None


def fila_y_columna(n, compare):
    for j in range(n):
        if compare(0, j) == 0:
            return (0, j)
    for i in range(n):
        if compare(i, n - 1) == 0:
            return (i, n - 1)
    return None


def escalera_cortada(n, compare):
    # la escalera, pero se rinde despues de n - 1 comparaciones
    usadas = [0]

    def limitado(i, j):
        usadas[0] += 1
        if usadas[0] > n - 1:
            raise StopIteration
        return compare(i, j)
    try:
        return staircase_with_oracle(n, limitado)
    except StopIteration:
        return None


def todas_las_celdas(n, compare):
    for i in range(n):
        for j in range(n):
            if compare(i, j) == 0:
                return (i, j)
    return None


algoritmos = {
    "escalera": staircase_with_oracle,
    "todas las celdas": todas_las_celdas,
    "diagonal principal": diagonal_principal,
    "fila 0 y ultima columna": fila_y_columna,
    "escalera con n-1 comparaciones": escalera_cortada,
}
n = 8
print(f"{'algoritmo':>32} {'comparaciones':>14} {'antidiagonal vista':>19} {'engañado':>9}")
for nombre, alg in algoritmos.items():
    adv = Adversary(n)
    respuesta = alg(n, adv.compare)
    faltan = [(i, n - 1 - i) for i in range(n) if (i, n - 1 - i) not in adv.asked]
    enganado = False
    if faltan:
        # la matriz con x en una celda que no miro es consistente con todas las respuestas
        M = adv.matrix(with_x_at=faltan[0])
        assert is_sorted_matrix(M) and contiene(M, 0)
        real = alg(n, lambda i, j: (M[i][j] > 0) - (M[i][j] < 0))
        enganado = real is None                   # dice "no esta", pero esta
        assert enganado
    print(f"{nombre:>32} {adv.comparisons:>14} {f'{len(adv.asked)} de {n}':>19} {'si' if enganado else 'no':>9}")
print("OK\n")

# ===============================================================
print("Prueba 7: empezar en la esquina de arriba a la izquierda")
rng = random.Random(7)
print(f"{'x':>22} {'busquedas':>10} {'fallos':>8}")
for nombre, presente in [("x esta en la matriz", True), ("x no esta", False)]:
    malos = 0
    for _ in range(3000):
        n = rng.randint(2, 10)
        M = matriz_al_azar(n, rng)
        if presente:
            x = M[rng.randrange(n)][rng.randrange(n)]
        else:
            x = rng.choice([v for v in range(M[-1][-1] + 2) if not contiene(M, v)] or [-1])
        r = search_matrix_top_left(M, x)
        malos += (r is None) == contiene(M, x)
    print(f"{nombre:>22} {3000:>10} {malos:>8}")
M = [[1, 2], [3, 4]]
print("contraejemplo: [[1, 2], [3, 4]], x = 3 ->", search_matrix_top_left(M, 3), " (esta en (1, 0))")
assert search_matrix_top_left(M, 3) is None
print("OK")
