"""Ejercicio 6 ★★ — Buscar en una matriz con filas y columnas ordenadas (C3, C5)

Código de validación de ejercicio-06.md.
Ejecutar con: python ejercicio-06.py
"""


# -------------------- Parte 1 --------------------

def buscar(M, x, comparar):
    n = len(M)
    i, j = 0, n - 1
    while i < n and j >= 0:
        r = comparar(x, M[i][j])
        if r == 0:
            return (i, j)
        if r < 0:          # x < M[i][j]: toda la columna j (de la fila i hacia abajo) es mayor
            j -= 1
        else:              # x > M[i][j]: toda la fila i (de la columna j hacia la izquierda) es menor
            i += 1
    return None

# -------------------- Parte 2 --------------------

import random

class Contador:
    def __init__(self):
        self.n = 0
    def __call__(self, x, y):
        self.n += 1
        return (x > y) - (x < y)

def matriz_al_azar(n, rng, salto=3):
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            base = max(M[i - 1][j] if i else 0, M[i][j - 1] if j else 0)
            M[i][j] = base + rng.randint(0, salto)          # salto 0 permite repetidos
    return M

def esta(M, x):
    return any(x in fila for fila in M)

# -------------------- Parte 3 --------------------

rng = random.Random(6)
for n in range(1, 21):
    peor = 0
    for _ in range(30):
        M = matriz_al_azar(n, rng)
        for x in range(-1, M[-1][-1] + 2):
            c = Contador()
            r = buscar(M, x, c)
            assert (r is not None) == esta(M, x)
            assert r is None or M[r[0]][r[1]] == x
            assert c.n <= 2 * n - 1
            peor = max(peor, c.n)
    E = [[i * n + j for j in range(n)] for i in range(n)]   # entradas distintas
    c = Contador()
    buscar(E, E[n - 1][0], c)
    assert c.n == 2 * n - 1
print("correcto en todas las pruebas; nunca más de 2n - 1 comparaciones, y la esquina inferior izquierda las usa todas")

# -------------------- Parte 4 --------------------

from itertools import product

def matriz_adversario(n, eleccion=None):
    """eleccion[i] = valor en la celda (i, n-1-i); por defecto 2n-3."""
    M = [[2 * (i + j) for j in range(n)] for i in range(n)]
    for i in range(n):
        M[i][n - 1 - i] = 2 * n - 3 if eleccion is None else eleccion[i]
    return M

def ordenada(M):
    n = len(M)
    return all(M[i][j] <= M[i][j + 1] for i in range(n) for j in range(n - 1)) and \
           all(M[i][j] <= M[i + 1][j] for i in range(n - 1) for j in range(n))

for n in range(1, 8):
    x = 2 * n - 2
    for elec in product([2 * n - 3, x], repeat=n):         # las 2^n elecciones
        assert ordenada(matriz_adversario(n, elec))
print("la matriz del adversario está ordenada con cualquier elección en la antidiagonal (n <= 7)")

def celdas_comparadas(algoritmo, M, x):
    vistas = []
    def comparar(u, v_pos):
        vistas.append(v_pos)
        i, j = v_pos
        return (u > M[i][j]) - (u < M[i][j])
    # el algoritmo recibe una "matriz" de posiciones para que podamos saber qué celda compara
    P = [[(i, j) for j in range(len(M))] for i in range(len(M))]
    return algoritmo(P, x, comparar), vistas

for n in [4, 16, 64]:
    M = matriz_adversario(n)
    r, vistas = celdas_comparadas(buscar, M, 2 * n - 2)
    anti = {(i, n - 1 - i) for i in range(n)}
    print(f"n = {n:>2}: respuesta {r}, {len(vistas)} comparaciones, "
          f"{len(anti & set(vistas))} de {n} celdas de la antidiagonal comparadas")
    assert anti <= set(vistas)

# -------------------- Parte 5 --------------------

def buscar_con_presupuesto(presupuesto):
    def algoritmo(M, x, comparar):
        n = len(M)
        i, j, usadas = 0, n - 1, 0
        while i < n and j >= 0 and usadas < presupuesto:
            usadas += 1
            r = comparar(x, M[i][j])
            if r == 0:
                return M[i][j]
            if r < 0:
                j -= 1
            else:
                i += 1
        return None
    return algoritmo

def engañar(algoritmo, n):
    x = 2 * n - 2
    r1, vistas = celdas_comparadas(algoritmo, matriz_adversario(n), x)
    sin_ver = [i for i in range(n) if (i, n - 1 - i) not in vistas]
    if not sin_ver:
        return None
    i = sin_ver[0]
    eleccion = [2 * n - 3] * n
    eleccion[i] = x
    M2 = matriz_adversario(n, eleccion)
    r2, vistas2 = celdas_comparadas(algoritmo, M2, x)
    return (i, n - 1 - i), r1, r2, vistas == vistas2

n = 10
celda, r1, r2, mismas = engañar(buscar_con_presupuesto(n - 1), n)
print(f"celda nunca comparada: {celda}")
print(f"matriz original : x no está, el algoritmo dice {r1}")
print(f"matriz cambiada : x está en {celda}, el algoritmo dice {r2}  (mismas comparaciones: {mismas})")
assert mismas and r1 == r2 is None
assert engañar(buscar, n) is None          # la búsqueda completa no se deja engañar
