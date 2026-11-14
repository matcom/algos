"""Ejercicio 2. Búsqueda binaria: invariante, potencial y cota de información."""
import math
from itertools import product


def busqueda_binaria(A, x, vigilar=True):
    """Devuelve (resultado, comparaciones). Comprueba invariante y potencial."""
    lo, hi, comps = 0, len(A), 0
    while lo < hi:
        if vigilar:
            assert x not in A or x in A[lo:hi], "invariante roto"
        phi = hi - lo
        m = (lo + hi) // 2
        comps += 1
        if x == A[m]:
            return ("está", m), comps
        if x < A[m]:
            hi = m
        else:
            lo = m + 1
        assert 0 <= hi - lo <= phi // 2, "el potencial no baja a la mitad"
    return ("no está", None), comps


def variante_lo_igual_m(A, x, tope=1000):
    """Variante con lo = m: devuelve None si no termina en 'tope' vueltas."""
    lo, hi, vueltas = 0, len(A), 0
    while lo < hi:
        vueltas += 1
        if vueltas > tope:
            return None
        m = (lo + hi) // 2
        if x == A[m]:
            return m
        if x < A[m]:
            hi = m
        else:
            lo = m
    return -1


def busqueda_sin(A, k, x):
    """Un algoritmo que nunca mira A[k]: la búsqueda binaria sobre A sin esa
    posición (para el Lema 2). Devuelve (resultado con índices de A, comparaciones)."""
    B = A[:k] + A[k + 1:]
    (r, m), comps = busqueda_binaria(B, x, vigilar=False)
    if m is not None and m >= k:
        m += 1
    return (r, m), comps


if __name__ == "__main__":
    print(f"{'n':>4} {'peor caso medido':>17} {'ceil(log2(n+1))':>16} {'huecos n+1':>11}")
    for n in range(1, 130):
        A = [2 * i + 1 for i in range(n)]               # impares: 1, 3, ..., 2n-1
        consultas = list(range(0, 2 * n + 2))             # elementos y huecos
        peor = max(busqueda_binaria(A, x)[1] for x in consultas)
        cota = math.ceil(math.log2(n + 1))
        assert peor == cota, (n, peor, cota)
        if n in (1, 3, 7, 15, 31, 63, 127):
            print(f"{n:>4} {peor:>17} {cota:>16} {n + 1:>11}")
    print("peor caso = ceil(log2(n+1)) para todo 1 <= n <= 129")

    print("\nVariante con lo = m, A = [5], x = 7:",
          "no termina" if variante_lo_igual_m([5], 7) is None else "termina")
    print("Búsqueda binaria correcta, A = [5], x = 7:", busqueda_binaria([5], 7)[0])

    # El Lema 2 con un algoritmo que nunca mira A[5] = 11
    A = [1, 3, 5, 7, 9, 11, 13]
    print("\nAlgoritmo que nunca mira A[5] = 11:")
    for x in (10, 11, 12):
        print(f"  x = {x}: {busqueda_sin(A, 5, x)}")
