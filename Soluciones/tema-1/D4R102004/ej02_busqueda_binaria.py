"""Ejercicio 2: búsqueda binaria con el invariante y el potencial vigilados,
y su peor caso comparado con la cota de información ⌈log2(n+1)⌉."""
import math
import random


def busqueda_binaria(A, x):
    """Precondición: A ordenado. Devuelve (posición o -1, comparaciones)."""
    lo, hi = 0, len(A)
    comparaciones = 0
    while lo < hi:
        # invariante: si x está en A, está en A[lo:hi]
        assert x not in A or x in A[lo:hi]
        potencial = hi - lo
        m = (lo + hi) // 2
        assert lo <= m < hi
        comparaciones += 1                      # una comparación de tres resultados
        if A[m] == x:
            return m, comparaciones
        if x < A[m]:
            hi = m
        else:
            lo = m + 1
        assert 0 <= hi - lo < potencial         # el potencial baja y no es negativo
    assert x not in A                           # conclusión: rango vacío ⇒ no está
    return -1, comparaciones


# 1. Correctitud contra la búsqueda lineal, con invariante y potencial vigilados
random.seed(2)
for _ in range(5000):
    n = random.randint(0, 30)
    A = sorted(random.sample(range(100), n))
    x = random.randint(-5, 105)
    pos, _ = busqueda_binaria(A, x)
    assert (pos == -1 and x not in A) or A[pos] == x
print("5000 búsquedas al azar: correctas, invariante y potencial cumplidos\n")

# 2. Peor caso: probar un x en cada hueco y cada elemento
print(f"{'n':>6} {'peor caso medido':>17} {'⌈log2(n+1)⌉':>13}")
for n in [1, 2, 3, 7, 8, 15, 100, 1000, 1023, 1024]:
    A = list(range(0, 2 * n, 2))                # elementos pares
    candidatos = range(-1, 2 * n + 1)           # los impares caen en los n+1 huecos
    peor = max(busqueda_binaria(A, x)[1] for x in candidatos)
    print(f"{n:>6} {peor:>17} {math.ceil(math.log2(n + 1)):>13}")
