import random

def matriz_aleatoria(n, semilla):
    rng = random.Random(semilla)
    M = [[0]*n for _ in range(n)]
    M[0][0] = rng.randint(1, 5)
    for j in range(1, n):
        M[0][j] = M[0][j-1] + rng.randint(1, 5)
    for i in range(1, n):
        M[i][0] = M[i-1][0] + rng.randint(1, 5)
    for i in range(1, n):
        for j in range(1, n):
            M[i][j] = max(M[i-1][j], M[i][j-1]) + rng.randint(1, 5)
    return M

def buscar_staircase(M, x, contador=None):
    n = len(M)
    fila, col = 0, n - 1
    while 0 <= fila < n and 0 <= col < n:
        if contador is not None:
            contador[0] += 1
        v = M[fila][col]
        if v == x:
            return True
        elif v > x:
            col -= 1
        else:
            fila += 1
    return False

def buscar_fuerza_bruta(M, x):
    return any(x in fila for fila in M)

# 1) Correctitud contra fuerza bruta, matrices aleatorias, muchos valores de x
fallos = 0
pruebas = 0
for n in [1, 2, 3, 5, 10, 20, 50, 100]:
    for semilla in range(20):
        M = matriz_aleatoria(n, semilla)
        valores_presentes = set(v for fila in M for v in fila)
        candidatos = list(valores_presentes) + [min(valores_presentes) - 1, max(valores_presentes) + 1]
        rng2 = random.Random(semilla + 1000)
        candidatos += [rng2.randint(M[0][0] - 5, M[-1][-1] + 5) for _ in range(10)]
        for x in candidatos:
            pruebas += 1
            esperado = buscar_fuerza_bruta(M, x)
            obtenido = buscar_staircase(M, x)
            if obtenido != esperado:
                fallos += 1

print(f"pruebas: {pruebas}, fallos (deberia ser 0): {fallos}")

# 2) El peor caso existe: M[i][j] = i + j (creciente en filas y columnas) y x = n - 1/2 caen justo
#     en el hueco entre dos antidiagonales y fuerzan el camino de 2n-1 comparaciones.
print()
print("      n   comparaciones con x=n-0.5   2n-1")
for n in [2, 3, 10, 50, 1000]:
    M = [[i + j for j in range(n)] for i in range(n)]
    c = [0]
    buscar_staircase(M, n - 0.5, c)
    assert c[0] == 2 * n - 1
    print(f"{n:>7}{c[0]:>29}{2 * n - 1:>7}")

# 3) El argumento de la antidiagonal: n celdas pairwise incomparables.
#    Verificamos que modificar CUALQUIER UNA de ellas a un valor x (entre sus vecinos) preserva
#    el orden de filas y columnas, sin afectar ninguna otra celda.
print()
n = 6
M = matriz_aleatoria(n, semilla=7)
anti = [(i, n - 1 - i) for i in range(n)]
print("celdas de la antidiagonal:", str(anti).replace(" ", ""))

def es_valida(M):
    n = len(M)
    for i in range(n):
        for j in range(1, n):
            if M[i][j] <= M[i][j-1]:
                return False
    for j in range(n):
        for i in range(1, n):
            if M[i][j] <= M[i-1][j]:
                return False
    return True

fallos_adversario = 0
for (i, j) in anti:
    M2 = [fila[:] for fila in M]
    vecino_izq = M2[i][j-1] if j > 0 else M2[i][j] - 100
    vecino_arr = M2[i-1][j] if i > 0 else M2[i][j] - 100
    cota_inf = max(vecino_izq, vecino_arr)
    vecino_der = M2[i][j+1] if j < n-1 else M2[i][j] + 100
    vecino_aba = M2[i+1][j] if i < n-1 else M2[i][j] + 100
    cota_sup = min(vecino_der, vecino_aba)
    if cota_sup - cota_inf < 2:
        print(f"  (fila {i}, col {j}): no hay hueco entero, se omite (caso raro)")
        continue
    x = cota_inf + 1   # un valor que cabe estrictamente entre los vecinos
    M2[i][j] = x
    if not es_valida(M2):
        fallos_adversario += 1
    else:
        # ademas, ninguna OTRA celda de la antidiagonal cambio
        otras_iguales = all(M2[i2][j2] == M[i2][j2] for (i2, j2) in anti if (i2, j2) != (i, j))
        if not otras_iguales:
            fallos_adversario += 1
# 3b) La instancia concreta de la demostracion: M[i][j] = 2(i+j) y x = 2n-1 (impar, no esta en M).
#     x cabe estrictamente entre los vecinos de cada celda de la antidiagonal.
for n_ in range(1, 61):
    base = [[2 * (i + j) for j in range(n_)] for i in range(n_)]
    x_ = 2 * n_ - 1
    assert not buscar_fuerza_bruta(base, x_)
    for (i, j) in [(i, n_ - 1 - i) for i in range(n_)]:
        M2 = [fila[:] for fila in base]
        M2[i][j] = x_
        assert es_valida(M2) and buscar_fuerza_bruta(M2, x_)

print(f"fallos del argumento de independencia (deberia ser 0): {fallos_adversario}")
print(f"-> las {n} celdas de la antidiagonal se pueden modificar una por una, de forma independiente,")
print(f"   sin romper el orden de filas/columnas ni afectarse entre si.")
