#!/usr/bin/env python3
"""
verificar_ejercicio_07.py

Mediana de dos arreglos ordenados de largo n: el n-ésimo menor de los 2n
elementos. Búsqueda binaria sobre i = cuántos de los n menores vienen de A.

Modelo: comparaciones. Solo se comparan A[i] con B[j]; cada una cuenta 1.
Valores distintos. Solo Python 3, sin dependencias externas.

Qué verifica:
  1. Casos de prueba fijos.
  2. Invariante y potencial ejecutables (versión instrumentada).
  3. Búsqueda exhaustiva: todas las intercalaciones para n <= 9.
  4. Pruebas aleatorias contra fuerza bruta (sorted).
  5. Cota de información: hay exactamente 2n salidas posibles.
  6. Óptimo exacto por minimax sobre todos los algoritmos de comparaciones
     para n pequeño, contra la cota de información y contra el algoritmo.
"""
import math
import random
from itertools import combinations
from functools import lru_cache


# ---------------------------------------------------------------- algoritmo
def mediana(A, B, cuenta=None):
    """n-ésimo menor de A + B (A, B ordenados, largo n, valores distintos).
    cuenta: lista [c]; se incrementa en 1 por cada comparación A[.] < B[.]
    o max(A[.], B[.]). Devuelve (valor, i)."""
    n = len(A)
    c = cuenta if cuenta is not None else [0]
    lo, hi = 0, n
    while lo < hi:
        i = (lo + hi + 1) // 2            # lo < i <= hi, así que 1 <= i <= n
        c[0] += 1
        if A[i - 1] < B[n - i]:           # A[i] < B[n-i+1] en índices desde 1
            lo = i
        else:
            hi = i - 1
    i = lo
    if i == 0:
        return B[n - 1], i
    if i == n:
        return A[n - 1], i
    c[0] += 1
    return max(A[i - 1], B[n - i - 1]), i


def mediana_instrumentada(A, B):
    """Misma lógica, con asserts del invariante, del potencial y del
    resultado final."""
    n = len(A)

    def P(i):                              # P(0) = True, P(n+1) = False
        if i == 0:
            return True
        if i == n + 1:
            return False
        return A[i - 1] < B[n - i]

    lo, hi = 0, n
    while True:
        # Invariante: 0 <= lo <= hi <= n, P(lo) y no P(hi + 1)
        assert 0 <= lo <= hi <= n and P(lo) and not P(hi + 1)
        if not lo < hi:
            break
        phi = hi - lo
        i = (lo + hi + 1) // 2
        assert lo < i <= hi
        if A[i - 1] < B[n - i]:
            lo = i
        else:
            hi = i - 1
        assert hi - lo < phi               # el potencial baja
    i = lo
    S = A[:i] + B[:n - i]                  # los n menores
    assert sorted(S) == sorted(A + B)[:n]
    if i == 0:
        return B[n - 1]
    if i == n:
        return A[n - 1]
    return max(A[i - 1], B[n - i - 1])


# ------------------------------------------------------------------ entradas
def intercalaciones(n):
    """Todas las formas de repartir 0..2n-1 en dos listas ordenadas de largo n."""
    for S in combinations(range(2 * n), n):
        A = list(S)
        B = [x for x in range(2 * n) if x not in S]
        yield A, B


def cota_algoritmo(n):
    return math.ceil(math.log2(n + 1)) + 1


def cota_informacion(n):
    return math.ceil(math.log2(2 * n))


def tabla(cabecera, filas):
    print("| " + " | ".join(cabecera) + " |")
    print("|" + "|".join("---" for _ in cabecera) + "|")
    for f in filas:
        print("| " + " | ".join(str(c) for c in f) + " |")
    print()


# ------------------------------------------------------ 1. casos de prueba fijos
def casos_de_prueba():
    casos = [
        ("n = 1, A < B", [1], [2]),
        ("n = 1, B < A", [2], [1]),
        ("n = 2, A < B", [1, 2], [3, 4]),
        ("n = 2, B < A", [3, 4], [1, 2]),
        ("n = 2, intercaladas", [1, 3], [2, 4]),
        ("n = 3, intercaladas", [1, 3, 5], [2, 4, 6]),
        ("n = 4, mediana en A", [1, 2, 3, 10], [4, 5, 6, 7]),
        ("n = 5, mediana en B", [1, 2, 3, 4, 20], [5, 6, 7, 8, 9]),
        ("n = 6, mezcla", [2, 4, 6, 8, 10, 12], [1, 3, 5, 7, 9, 11]),
        ("n = 7, A grande", [11, 12, 13, 14, 15, 16, 17], [1, 2, 3, 4, 5, 6, 7]),
    ]
    filas = []
    for nombre, A, B in casos:
        n = len(A)
        c = [0]
        val, i = mediana(A, B, c)
        esperado = sorted(A + B)[n - 1]
        assert val == esperado and mediana_instrumentada(A, B) == esperado
        assert c[0] <= cota_algoritmo(n)
        filas.append((nombre, A, B, i, val, c[0]))
    print("### Casos de prueba\n")
    tabla(["Caso", "A", "B", "i", "mediana", "comparaciones"], filas)


def traza(A, B):
    n = len(A)
    filas, lo, hi = [], 0, n
    while lo < hi:
        i = (lo + hi + 1) // 2
        r = A[i - 1] < B[n - i]
        filas.append((f"[{lo}, {hi}]", i, f"A[{i}]={A[i-1]} < B[{n-i+1}]={B[n-i]}",
                      "sí" if r else "no"))
        if r:
            lo = i
        else:
            hi = i - 1
    filas.append((f"[{lo}, {hi}]", "—", "fin: i* = " + str(lo), "—"))
    print(f"### Traza: A = {A}, B = {B}\n")
    tabla(["[lo, hi]", "i", "comparación", "¿cierto?"], filas)


# ------------------------------------------------------ 2. búsqueda exhaustiva
def exhaustivo(nmax=9):
    filas = []
    for n in range(1, nmax + 1):
        total, peor = 0, 0
        for A, B in intercalaciones(n):
            c = [0]
            val, _ = mediana(A, B, c)
            assert val == sorted(A + B)[n - 1]
            assert mediana_instrumentada(A, B) == val
            peor = max(peor, c[0])
            total += 1
        assert peor <= cota_algoritmo(n)
        filas.append((n, total, peor, cota_algoritmo(n), cota_informacion(n)))
    print("### Búsqueda exhaustiva (todas las intercalaciones)\n")
    tabla(["n", "entradas", "peor caso observado",
           "⌈log₂(n+1)⌉ + 1", "⌈log₂ 2n⌉"], filas)


# ------------------------------------------------------- 3. pruebas aleatorias
def aleatorias(semilla=3):
    rng = random.Random(semilla)
    filas = []
    for n, pruebas in [(10, 5000), (100, 5000), (1000, 2000), (20000, 300)]:
        peor = 0
        for _ in range(pruebas):
            vals = rng.sample(range(10 * n), 2 * n)
            vals.sort()
            idx = set(rng.sample(range(2 * n), n))
            if rng.random() < 0.1:                  # casos extremos
                idx = set(range(n)) if rng.random() < 0.5 else set(range(n, 2 * n))
            A = [vals[k] for k in range(2 * n) if k in idx]
            B = [vals[k] for k in range(2 * n) if k not in idx]
            c = [0]
            val, _ = mediana(A, B, c)
            assert val == vals[n - 1]
            peor = max(peor, c[0])
        assert peor <= cota_algoritmo(n)
        filas.append((n, pruebas, peor, cota_algoritmo(n)))
    print("### Pruebas aleatorias contra fuerza bruta\n")
    tabla(["n", "pruebas", "peor caso observado", "⌈log₂(n+1)⌉ + 1"], filas)


# ------------------------------------------------ 4. cota de información: 2n salidas
def identidad_mediana(posA, posB, n):
    """Quién es el n-ésimo menor: ('A', k) o ('B', k), con k desde 1."""
    orden = sorted([(p, "A", k + 1) for k, p in enumerate(posA)] +
                   [(p, "B", k + 1) for k, p in enumerate(posB)])
    _, arr, k = orden[n - 1]
    return (arr, k)


def salidas(nmax=9):
    filas = []
    for n in range(1, nmax + 1):
        sal = set()
        for S in combinations(range(2 * n), n):
            posA = list(S)
            posB = [x for x in range(2 * n) if x not in S]
            sal.add(identidad_mediana(posA, posB, n))
        assert len(sal) == 2 * n
        # el patrón A^(k-1) B^(n-k) A A^(n-k) B^k hace de A[k] la mediana
        for k in range(1, n + 1):
            patron = "A" * (k - 1) + "B" * (n - k) + "A" + "A" * (n - k) + "B" * k
            posA = [p for p, ch in enumerate(patron) if ch == "A"]
            posB = [p for p, ch in enumerate(patron) if ch == "B"]
            assert identidad_mediana(posA, posB, n) == ("A", k)
        filas.append((n, 2 * n, len(sal), cota_informacion(n)))
    print("### Salidas posibles (cota de información)\n")
    tabla(["n", "2n", "salidas distintas", "⌈log₂ 2n⌉"], filas)


# ------------------------------------- 5. óptimo exacto (minimax, todos los algoritmos)
def optimo_exacto(nmax=5):
    filas = []
    for n in range(1, nmax + 1):
        inter = []
        for S in combinations(range(2 * n), n):
            posA = tuple(S)
            posB = tuple(x for x in range(2 * n) if x not in S)
            inter.append((posA, posB, identidad_mediana(posA, posB, n)))

        @lru_cache(maxsize=None)
        def f(estado):
            if len({s[2] for s in estado}) == 1:
                return 0
            mejor = 10 ** 9
            for i in range(n):
                for j in range(n):
                    menor = frozenset(s for s in estado if s[0][i] < s[1][j])
                    mayor = estado - menor
                    if menor and mayor:
                        mejor = min(mejor, 1 + max(f(menor), f(mayor)))
            return mejor

        opt = f(frozenset(inter))
        peor = max(mediana(A, B, c := [0]) and c[0]
                   for A, B in intercalaciones(n))
        assert cota_informacion(n) <= opt <= peor
        filas.append((n, len(inter), cota_informacion(n), opt, peor))
    print("### Óptimo exacto por minimax (todos los algoritmos de comparaciones)\n")
    tabla(["n", "intercalaciones", "⌈log₂ 2n⌉", "óptimo exacto",
           "nuestro algoritmo (peor caso)"], filas)


if __name__ == "__main__":
    casos_de_prueba()
    traza([1, 3, 5, 7, 9, 11, 13], [2, 4, 6, 8, 10, 12, 14])
    exhaustivo()
    aleatorias()
    salidas()
    optimo_exacto()
    print("Todas las verificaciones pasaron.")
