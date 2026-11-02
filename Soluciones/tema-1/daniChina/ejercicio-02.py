import math

# Ejercicio 2, Tema 1: invariante, potencial y cota de informacion
# de la busqueda binaria.
#
# Invariante: todos los elementos de A[:lo] son menores que x
#             y todos los de A[hi:] son mayores que x.
# Potencial:  p = hi - lo  (baja en cada vuelta, siempre p >= 0)
# Cota:       hacen falta al menos ceil(log2(n+1)) comparaciones.


def busqueda_binaria(A, x):
    """Devuelve (("esta", pos) o ("hueco", h), cantidad de comparaciones)."""
    lo, hi = 0, len(A)
    comparaciones = 0
    while lo < hi:
        m = (lo + hi) // 2
        comparaciones += 1          # una comparacion: <, = o >
        if x == A[m]:
            return ("esta", m), comparaciones
        if x < A[m]:
            hi = m
        else:
            lo = m + 1
    return ("hueco", lo), comparaciones


def busqueda_vigilada(A, x):
    """Lo mismo, pero comprueba el invariante y el potencial en cada vuelta."""
    lo, hi = 0, len(A)
    comparaciones = 0
    while True:
        # invariante: lo de la izquierda es menor, lo de la derecha es mayor
        assert all(a < x for a in A[:lo]) and all(a > x for a in A[hi:])
        if lo >= hi:
            break
        p = hi - lo                 # potencial antes de la vuelta
        m = (lo + hi) // 2
        comparaciones += 1
        if x == A[m]:
            return ("esta", m), comparaciones
        if x < A[m]:
            hi = m
        else:
            lo = m + 1
        p_nuevo = hi - lo
        assert 0 <= p_nuevo < p     # el potencial baja
        assert p_nuevo <= p // 2    # y de hecho se parte (al menos) a la mitad
    return ("hueco", lo), comparaciones


def peor_caso(n):
    """Peor caso medido: probamos todos los x (los que estan y todos los huecos)."""
    A = [2 * i for i in range(n)]
    peor = 0
    for x in range(-1, 2 * n):      # pares: estan; impares y -1: huecos
        resultado, c = busqueda_vigilada(A, x)
        if x % 2 == 0 and 0 <= x < 2 * n:
            assert resultado == ("esta", x // 2)
        else:
            assert resultado[0] == "hueco"
        peor = max(peor, c)
    return peor


if __name__ == "__main__":
    # traza para n = 7 buscando un valor que no esta
    A = [10, 20, 30, 40, 50, 60, 70]
    x = 45
    lo, hi = 0, len(A)
    print(f"Traza con A = {A}, x = {x}")
    while lo < hi:
        m = (lo + hi) // 2
        print(f"  lo = {lo}, hi = {hi}, p = {hi - lo}, m = {m}, A[m] = {A[m]}")
        if x < A[m]:
            hi = m
        else:
            lo = m + 1
    print(f"  lo = {lo}, hi = {hi}, p = {hi - lo} -> x cae en el hueco {lo}")
    print()

    print(f"{'n':>5} {'huecos':>7} {'cota':>5} {'peor caso':>10} {'2^cota':>7}")
    for n in [1, 2, 3, 4, 7, 8, 15, 16, 100, 1000]:
        cota = math.ceil(math.log2(n + 1))
        peor = peor_caso(n)
        print(f"{n:>5} {n + 1:>7} {cota:>5} {peor:>10} {2 ** cota:>7}")

    # comprobacion para todos los n de 1 a 200
    for n in range(1, 201):
        assert peor_caso(n) == math.ceil(math.log2(n + 1))
    print("\nPara todo n de 1 a 200: peor caso = ceil(log2(n+1))")
