#!/usr/bin/env python3
"""
verificar_ejercicio_14.py

Máximo de un arreglo unimodal de n valores distintos (crece y luego decrece),
por búsqueda binaria sobre la pendiente.

Modelo: comparaciones. Solo se pregunta A[i] < A[j] (cualquier par); cada una
cuenta 1. Con valores distintos cada pregunta tiene dos respuestas.
Solo Python 3, sin dependencias externas.

Qué verifica:
  1. Casos de prueba fijos y una traza.
  2. Invariante y potencial ejecutables (versión instrumentada).
  3. Búsqueda exhaustiva: todos los órdenes unimodales posibles, n <= 16.
  4. Pruebas aleatorias con valores reales y n grande.
  5. Cota inferior: las n entradas I_p dan n hojas distintas, y óptimo exacto
     por minimax sobre todos los algoritmos de comparaciones (n <= 8).
  6. Por qué hace falta "valores distintos": con repetidos el algoritmo falla
     y la cota baja a Omega(n) (minimax sobre la familia del adversario).
"""
import math
import random
from itertools import product
from functools import lru_cache


# ---------------------------------------------------------------- algoritmo
def pico(A, cuenta=None, respuestas=None):
    """Posición (base 0) del máximo de A. cuenta: lista [c] que se incrementa
    en 1 por comparación. respuestas: lista donde se anota cada respuesta."""
    c = cuenta if cuenta is not None else [0]
    lo, hi = 0, len(A) - 1
    while lo < hi:
        m = (lo + hi) // 2                  # lo <= m < hi
        c[0] += 1
        sube = A[m] < A[m + 1]
        if respuestas is not None:
            respuestas.append(sube)
        if sube:
            lo = m + 1
        else:
            hi = m
    return lo


def pico_instrumentado(A):
    """Misma lógica, con asserts del invariante y del potencial.
    p es la posición real del máximo (solo la usa la verificación)."""
    n = len(A)
    p = A.index(max(A))
    lo, hi = 0, n - 1
    while True:
        assert 0 <= lo <= hi <= n - 1 and lo <= p <= hi        # invariante
        if not lo < hi:
            break
        phi = hi - lo
        assert phi >= 1
        m = (lo + hi) // 2
        assert lo <= m < hi
        if A[m] < A[m + 1]:
            assert m < p                                        # el pico está a la derecha
            lo = m + 1
        else:
            assert m >= p                                       # el pico está en [lo, m]
            hi = m
        assert hi - lo < phi                                    # el potencial baja
    return lo


# ------------------------------------------------------------------ entradas
def es_unimodal_estricto(A):
    p = A.index(max(A))
    return (all(A[i] < A[i + 1] for i in range(p)) and
            all(A[i] > A[i + 1] for i in range(p, len(A) - 1)) and
            len(set(A)) == len(A))


def unimodales(n):
    """Todos los órdenes unimodales posibles con valores 0..n-1: se elige qué
    valores (salvo el máximo) quedan a la izquierda del pico. Son 2^(n-1)."""
    for mascara in range(2 ** (n - 1)):
        izq = [v for v in range(n - 1) if mascara >> v & 1]
        der = [v for v in range(n - 1) if not mascara >> v & 1]
        yield izq + [n - 1] + der[::-1]


def I(n, p):
    """Entrada de la cota inferior con pico en p (base 1): i si i <= p, -i si no."""
    return [i if i <= p else -i for i in range(1, n + 1)]


def cota(n):
    return math.ceil(math.log2(n)) if n > 1 else 0


def tabla(cabecera, filas):
    print("| " + " | ".join(cabecera) + " |")
    print("|" + "|".join("---" for _ in cabecera) + "|")
    for f in filas:
        print("| " + " | ".join(str(c) for c in f) + " |")
    print()


# ------------------------------------------------------ 1. casos de prueba fijos
def casos_de_prueba():
    casos = [
        ("n = 1", [7]),
        ("n = 2, sube", [1, 2]),
        ("n = 2, baja", [2, 1]),
        ("n = 3, pico al medio", [3, 9, 8]),
        ("solo creciente", [1, 2, 3, 4, 5]),
        ("solo decreciente", [5, 4, 3, 2, 1]),
        ("n = 7, pico en 4", [2, 5, 9, 14, 11, 7, 3]),
        ("n = 8, pico en 4", [1, 3, 5, 7, 6, 4, 2, 0]),
        ("n = 8, pico en 8", [1, 2, 3, 4, 5, 6, 7, 8]),
        ("n = 10, pico en 3", [1, 9, 20, 15, 14, 12, 8, 5, 3, 2]),
    ]
    filas = []
    for nombre, A in casos:
        c = [0]
        r = pico(A, c)
        assert A[r] == max(A) and pico_instrumentado(A) == r and c[0] <= cota(len(A))
        filas.append((nombre, A, r + 1, c[0], cota(len(A))))
    print("### Casos de prueba\n")
    tabla(["Caso", "A", "pico (base 1)", "comparaciones", "⌈log₂ n⌉"], filas)


def traza(A):
    n = len(A)
    filas, lo, hi = [], 1, n
    while lo < hi:
        m = (lo + hi) // 2
        sube = A[m - 1] < A[m]
        filas.append((f"[{lo}, {hi}]", m, f"A[{m}]={A[m-1]} < A[{m+1}]={A[m]}",
                      "sí → lo = m + 1" if sube else "no → hi = m"))
        if sube:
            lo = m + 1
        else:
            hi = m
    filas.append((f"[{lo}, {hi}]", "—", f"fin: p = {lo}", "—"))
    print(f"### Traza: A = {A}\n")
    tabla(["[lo, hi]", "m", "comparación", "resultado"], filas)


# ------------------------------------------------------ 2. búsqueda exhaustiva
def exhaustivo(nmax=16, instr_max=12):
    filas = []
    for n in range(1, nmax + 1):
        total, peor = 0, 0
        for A in unimodales(n):
            assert es_unimodal_estricto(A)
            c = [0]
            r = pico(A, c)
            assert A[r] == n - 1
            if n <= instr_max:
                assert pico_instrumentado(A) == r
            peor = max(peor, c[0])
            total += 1
        assert total == 2 ** (n - 1)
        assert peor == cota(n)
        filas.append((n, total, peor, cota(n)))
    print("### Búsqueda exhaustiva (todos los órdenes unimodales)\n")
    tabla(["n", "entradas", "peor caso observado", "⌈log₂ n⌉"], filas)


# ------------------------------------------------------- 3. pruebas aleatorias
def aleatorias(semilla=9):
    rng = random.Random(semilla)
    filas = []
    for n, pruebas in [(10, 5000), (1000, 3000), (100000, 300)]:
        peor = 0
        for _ in range(pruebas):
            vals = rng.sample(range(10 * n), n)
            M = max(vals)
            vals.remove(M)
            p = rng.randrange(n)                    # cuántos quedan a la izquierda
            A = sorted(vals[:p]) + [M] + sorted(vals[p:], reverse=True)
            assert es_unimodal_estricto(A)
            c = [0]
            r = pico(A, c)
            assert A[r] == M
            peor = max(peor, c[0])
        assert peor <= cota(n)
        filas.append((n, pruebas, peor, cota(n)))
    print("### Pruebas aleatorias (valores reales distintos)\n")
    tabla(["n", "pruebas", "peor caso observado", "⌈log₂ n⌉"], filas)


# ------------------------------------------------------- 4. cota: hojas y minimax
def hojas(nmax=40):
    for n in range(1, nmax + 1):
        trans = set()
        for p in range(1, n + 1):
            A = I(n, p)
            assert es_unimodal_estricto(A) and A.index(max(A)) == p - 1
            resp = []
            assert pico(A, None, resp) == p - 1
            trans.add(tuple(resp))
        assert len(trans) == n            # n entradas, n transcripciones distintas
    print(f"Las n entradas I_p dan n hojas distintas (n = 1..{nmax}).\n")


def optimo_exacto(nmax=8):
    filas = []
    for n in range(1, nmax + 1):
        ins = list(unimodales(n))
        pares = [(i, j) for i in range(n) for j in range(i + 1, n)]

        @lru_cache(maxsize=None)
        def f(estado):
            if len({ins[t].index(n - 1) for t in estado}) == 1:
                return 0
            mejor = 10 ** 9
            for i, j in pares:
                menor = frozenset(t for t in estado if ins[t][i] < ins[t][j])
                mayor = estado - menor
                if menor and mayor:
                    mejor = min(mejor, 1 + max(f(menor), f(mayor)))
            return mejor

        v = f(frozenset(range(len(ins))))
        assert v == cota(n)
        filas.append((n, len(ins), v, cota(n)))
    print("### Óptimo exacto por minimax (todos los algoritmos de comparaciones)\n")
    tabla(["n", "entradas", "óptimo exacto", "⌈log₂ n⌉"], filas)


# ------------------------------------------------- 5. por qué "valores distintos"
def con_repetidos(nmax=10):
    """Arreglos 0/1 no estrictamente unimodales: no decrecen hasta un punto y
    no crecen después."""
    filas = []
    for n in range(2, nmax + 1):
        total = fallan = 0
        for A in product([0, 1], repeat=n):
            A = list(A)
            ok = any(all(A[i] <= A[i + 1] for i in range(k)) and
                     all(A[i] >= A[i + 1] for i in range(k, n - 1))
                     for k in range(n))
            if not ok:
                continue
            total += 1
            fallan += A[pico(A)] != max(A)
        filas.append((n, total, fallan))
    print("### Con repetidos el algoritmo falla (arreglos 0/1 no estrictamente unimodales)\n")
    tabla(["n", "entradas", "donde falla"], filas)

    # familia del adversario: ceros con un solo 1; cada pregunta da <, = o >
    filas = []
    for n in range(1, 9):
        ins = [[1 if i == k else 0 for i in range(n)] for k in range(n)]
        pares = [(i, j) for i in range(n) for j in range(i + 1, n)]

        @lru_cache(maxsize=None)
        def g(estado):
            if len(estado) <= 1:
                return 0
            mejor = 10 ** 9
            for i, j in pares:
                partes = {}
                for k in estado:
                    s = (ins[k][i] > ins[k][j]) - (ins[k][i] < ins[k][j])
                    partes.setdefault(s, set()).add(k)
                if len(partes) < 2:
                    continue
                mejor = min(mejor, 1 + max(g(frozenset(q)) for q in partes.values()))
            return mejor

        v = g(frozenset(range(n)))
        assert v == n // 2
        filas.append((n, v, n // 2))
    print("### Familia del adversario con repetidos (ceros y un solo 1)\n")
    tabla(["n", "óptimo exacto en esa familia", "⌊n/2⌋"], filas)


if __name__ == "__main__":
    casos_de_prueba()
    traza([2, 5, 9, 14, 11, 7, 3])
    exhaustivo()
    aleatorias()
    hojas()
    optimo_exacto()
    con_repetidos()
    print("Todas las verificaciones pasaron.")
