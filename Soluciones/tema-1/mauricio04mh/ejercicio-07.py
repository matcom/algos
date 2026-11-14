"""Ejercicio 7. Mediana de dos arreglos ordenados con ceil(log2 n)+1 comparaciones."""
import math
import random


def mediana(A, B, vigilar=True):
    n = len(A)
    ia = ib = 0
    k = n
    comps = 0
    todos = sorted(A + B)
    while k > 1:
        if vigilar:
            assert ia + ib == n - k and ia >= 0 and ib >= 0 and k >= 1          # (I1)
            assert n - ia >= k and n - ib >= k
            vivos = sorted(A[ia:] + B[ib:])
            assert vivos[k - 1] == todos[n - 1]                                     # (I2)
        h = k // 2
        comps += 1
        if A[ia + h - 1] < B[ib + h - 1]:
            ia += h
        else:
            ib += h
        k -= h
    comps += 1
    return min(A[ia], B[ib]), comps


if __name__ == "__main__":
    A, B = [1, 4, 7, 10], [2, 3, 8, 9]
    print("n = 4:", mediana(A, B))
    A, B = list(range(1, 16, 2)), list(range(2, 17, 2))
    print("n = 8:", mediana(A, B))

    rng = random.Random(7)
    print(f"\n{'n':>5} {'entradas':>9} {'comparaciones (mín–máx)':>25} {'ceil(log2 n)+1':>15}")
    for n in [1, 2, 3, 4, 5, 8, 13, 16, 100, 1000]:
        usadas = set()
        pruebas = 400 if n <= 100 else 40
        for _ in range(pruebas):
            valores = rng.sample(range(10 * n), 2 * n)
            A = sorted(valores[:n])
            B = sorted(valores[n:])
            m, c = mediana(A, B, vigilar=(n <= 100))
            assert m == sorted(A + B)[n - 1]
            usadas.add(c)
        esperado = math.ceil(math.log2(n)) + 1 if n > 1 else 1
        assert usadas == {esperado}, (n, usadas, esperado)
        print(f"{n:>5} {pruebas:>9} {min(usadas):>13} – {max(usadas):<9} {esperado:>15}")

    print("\nCota de información: cada uno de los 2n elementos puede ser la mediana.")
    n = 4
    medianas = set()
    for _ in range(20000):
        v = rng.sample(range(2 * n), 2 * n)
        A, B = sorted(v[:n]), sorted(v[n:])
        x = sorted(A + B)[n - 1]
        medianas.add(("A", A.index(x)) if x in A else ("B", B.index(x)))
    print(f"n = {n}: posiciones distintas de la mediana observadas = {len(medianas)} (2n = {2 * n})")
