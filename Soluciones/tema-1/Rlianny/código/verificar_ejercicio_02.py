#!/usr/bin/env python3
"""Verificación del ejercicio 2: búsqueda binaria.

Comprueba el invariante, el potencial, el peor caso exacto y la cota de
información ⌈log2(n+1)⌉, incluida una búsqueda exhaustiva sobre TODAS las
estrategias de comparaciones para n pequeño.

Python 3, sin dependencias externas.
"""
import random
import sys
from functools import lru_cache

sys.setrecursionlimit(10000)


# ---------------------------------------------------------------- utilidades

def cmp3(x, y):
    """Comparación con resultado -1 (<), 0 (=) o 1 (>). Cuenta como una."""
    return (x > y) - (x < y)


def techo_log2(k):
    """⌈log2 k⌉ exacto para k >= 1."""
    return (k - 1).bit_length()


def altura_minima(hojas, ramas):
    """Menor h con ramas**h >= hojas."""
    h, capacidad = 0, 1
    while capacidad < hojas:
        capacidad *= ramas
        h += 1
    return h


# ---------------------------------------------------------------- algoritmo

def busqueda_binaria(A, x, vigilar=None, registro=None):
    """Devuelve (salida, comparaciones).

    salida = ("está", i) con A[i] == x, o ("hueco", j) con A[j-1] < x < A[j].
    vigilar(lo, hi, k): se llama al empezar cada vuelta (k comparaciones hechas).
    registro: lista donde se anota (m, respuesta) de cada comparación.
    """
    n = len(A)
    lo, hi, comps = 0, n, 0
    if vigilar:
        vigilar(lo, hi, comps)
    while lo < hi:
        m = (lo + hi) // 2
        r = cmp3(x, A[m])          # una sola comparación
        comps += 1
        if registro is not None:
            registro.append((m, r))
        if r == 0:
            return ("está", m), comps
        if r < 0:
            hi = m
        else:
            lo = m + 1
        if vigilar:
            vigilar(lo, hi, comps)
    return ("hueco", lo), comps


# ------------------------------------------------ invariante y postcondición

def invariante(A, x, lo, hi):
    n = len(A)
    return (0 <= lo <= hi <= n
            and all(A[i] < x for i in range(lo))
            and all(A[i] > x for i in range(hi, n)))


def cumple_postcondicion(A, x, salida):
    tipo, k = salida
    n = len(A)
    if tipo == "está":
        return 0 <= k < n and A[k] == x
    return (0 <= k <= n and x not in A
            and (k == 0 or A[k - 1] < x) and (k == n or x < A[k]))


def referencia(A, x):
    if x in A:
        return ("está", A.index(x))
    return ("hueco", sum(1 for a in A if a < x))


def ejecutar_vigilada(A, x):
    """Corre la búsqueda comprobando invariante y potencial en cada vuelta."""
    n = len(A)
    previo = {"phi": n + 1}

    def vigilar(lo, hi, k):
        assert invariante(A, x, lo, hi), (A, x, lo, hi)
        phi = hi - lo
        assert phi < previo["phi"], (A, x, lo, hi)      # el potencial baja
        assert phi <= n // 2 ** k, (A, x, lo, hi, k)    # phi_k <= n // 2^k
        previo["phi"] = phi

    salida, comps = busqueda_binaria(A, x, vigilar)
    assert cumple_postcondicion(A, x, salida), (A, x, salida)
    assert comps <= techo_log2(n + 1), (A, x, comps)
    return salida, comps


# --------------------------------------------- peor caso y óptimo exhaustivo

def peor_caso_busqueda(n):
    A = [2 * (i + 1) for i in range(n)]
    return max(busqueda_binaria(A, x)[1] for x in range(0, 2 * n + 2))


def optimo_exhaustivo(n):
    """Mínimo, sobre todas las estrategias, del peor caso en comparaciones.

    El algoritmo solo ve el resultado de comparar x con elementos de A, así que
    solo distingue 2n+1 clases de entrada: la clase 2i+1 es x = A[i] y la clase
    par 2j es el hueco j. Su conocimiento es siempre un intervalo [l, r] de
    clases consistentes con lo respondido. Comparar con A[i] (clase c = 2i+1)
    deja [l, c-1] si x < A[i], deja {c} si x = A[i] y deja [c+1, r] si x > A[i].
    Comparar con un elemento fuera del intervalo no da información.
    El algoritmo termina cuando queda una sola clase (con dos clases habría
    dos salidas correctas distintas y se equivocaría en una).
    """
    @lru_cache(maxsize=None)
    def g(l, r):
        if l == r:
            return 0
        mejor = None
        primera = l if l % 2 == 1 else l + 1
        for c in range(primera, r + 1, 2):
            izq = g(l, c - 1) if c - 1 >= l else 0
            der = g(c + 1, r) if c + 1 <= r else 0
            v = 1 + max(izq, der)         # la rama "=" no cuesta nada más
            if mejor is None or v < mejor:
                mejor = v
        return mejor

    return g(0, 2 * n)


# ------------------------------------------------------------------- tablas

def tabla_traza():
    A, x = [2, 5, 9, 14, 20, 27, 35], 23
    print("### Tabla 1. Traza de `A = [2, 5, 9, 14, 20, 27, 35]`, `x = 23`\n")
    print("| vuelta | lo | hi | región `s = hi - lo` | m | A[m] | respuesta | nueva región |")
    print("|---|---|---|---|---|---|---|---|")
    lo, hi, v = 0, len(A), 0
    while lo < hi:
        m = (lo + hi) // 2
        r = cmp3(x, A[m])
        v += 1
        s = hi - lo
        simbolo = {-1: "x < A[m]", 0: "x = A[m]", 1: "x > A[m]"}[r]
        if r < 0:
            nhi, nlo = m, lo
        else:
            nlo, nhi = m + 1, hi
        print(f"| {v} | {lo} | {hi} | {s} | {m} | {A[m]} | {simbolo} | "
              f"[{nlo}, {nhi}) con s = {nhi - nlo} |")
        lo, hi = nlo, nhi
    salida, comps = busqueda_binaria(A, x)
    assert salida == ("hueco", lo) and comps == v == 3
    print(f"\nSalida: `{salida}`, con {comps} comparaciones.\n")


def tabla_peor_caso():
    print("### Tabla 2. Peor caso exacto de la búsqueda binaria y mínimo sobre todas las estrategias\n")
    print("| n | búsqueda binaria (peor caso) | ⌈log₂(n+1)⌉ | mínimo exhaustivo |")
    print("|---|---|---|---|")
    for n in range(0, 129):
        binaria = peor_caso_busqueda(n)
        formula = techo_log2(n + 1)
        optimo = optimo_exhaustivo(n)
        assert binaria == formula == optimo, (n, binaria, formula, optimo)
    for n in [0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 31, 32, 100, 127, 128]:
        print(f"| {n} | {peor_caso_busqueda(n)} | {techo_log2(n + 1)} | {optimo_exhaustivo(n)} |")
    for n in [1000, 1023, 1024]:
        binaria = peor_caso_busqueda(n)
        assert binaria == techo_log2(n + 1)
        print(f"| {n} | {binaria} | {techo_log2(n + 1)} | — |")
    print()


def tabla_trampa():
    print("### Tabla 3. Contar todas las salidas con tres ramas frente a contar solo los huecos\n")
    print("| n | salidas posibles `2n + 1`, tres ramas | huecos `n + 1`, dos ramas |")
    print("|---|---|---|")
    for n in [7, 100, 1000, 10 ** 6]:
        a = altura_minima(2 * n + 1, 3)
        b = altura_minima(n + 1, 2)
        assert b == techo_log2(n + 1) and a <= b
        print(f"| {n} | altura >= {a} | altura >= {b} |")
    print()


def tabla_bordes():
    print("### Tabla 4. Casos borde\n")
    print("| `A` | `x` | salida | comparaciones |")
    print("|---|---|---|---|")
    G = [2, 5, 9, 14, 20, 27, 35]
    casos = [([], 5), ([7], 3), ([7], 7), ([7], 9),
             (G, 1), (G, 2), (G, 14), (G, 23), (G, 35), (G, 40)]
    for A, x in casos:
        salida, comps = ejecutar_vigilada(A, x)
        assert salida == referencia(A, x)
        print(f"| `{A}` | {x} | `{salida}` | {comps} |")
    print()


# --------------------------------------------------------------- verificación

def exhaustivo_pequeno():
    casos = 0
    U = 8
    for mascara in range(2 ** U):
        A = [i for i in range(U) if mascara >> i & 1]
        for x in range(-1, U + 1):
            salida, _ = ejecutar_vigilada(A, x)
            assert salida == referencia(A, x)
            casos += 1
    return casos


def aleatorio(ensayos=3000, semilla=0):
    rnd = random.Random(semilla)
    for _ in range(ensayos):
        n = rnd.randint(0, 200)
        A = sorted(rnd.sample(range(-500, 500), n))
        if n and rnd.random() < 0.5:
            x = rnd.choice(A)
        else:
            x = rnd.randint(-520, 520)
        salida, _ = ejecutar_vigilada(A, x)
        assert salida == referencia(A, x), (A, x)
    return ensayos


def huecos_a_hojas_distintas(tope=200):
    """Los n+1 huecos dan n+1 caminos distintos, solo con respuestas < y >."""
    for n in range(0, tope + 1):
        A = [2 * (i + 1) for i in range(n)]
        caminos = set()
        for j in range(n + 1):
            registro = []
            salida, comps = busqueda_binaria(A, 2 * j + 1, registro=registro)
            assert salida == ("hueco", j)
            assert all(r != 0 for _, r in registro)
            assert comps <= techo_log2(n + 1)
            caminos.add(tuple(registro))
        assert len(caminos) == n + 1, n
    return tope


def hojas_n7():
    A = [2 * (i + 1) for i in range(7)]
    alturas = []
    for j in range(8):
        registro = []
        busqueda_binaria(A, 2 * j + 1, registro=registro)
        alturas.append(len(registro))
    assert alturas == [3] * 8
    return alturas


if __name__ == "__main__":
    tabla_traza()
    tabla_peor_caso()
    tabla_trampa()
    tabla_bordes()
    n1 = exhaustivo_pequeno()
    print(f"Exhaustivo (arreglos estrictamente crecientes con valores en 0..7, x en -1..8): "
          f"{n1} casos, invariante, potencial y resultado correctos.")
    n2 = aleatorio()
    print(f"Aleatorio (semilla 0, n <= 200): {n2} casos contra la referencia, sin discrepancias.")
    n3 = huecos_a_hojas_distintas()
    print(f"Huecos a hojas distintas: n = 0..{n3}, los n+1 huecos dan n+1 caminos distintos.")
    print(f"Alturas de las 8 hojas para n = 7: {hojas_n7()}")
    print("TODAS LAS VERIFICACIONES PASARON")
