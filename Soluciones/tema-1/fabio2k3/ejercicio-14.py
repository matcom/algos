import random 

def minimo_rotado(A, check = False):
    l = 0
    h = len(A) - 1

    comparaciones = 0
    camino = []

    p = A.index(min(A)) if check else None

    while l < h:
        if check:
            assert l <= p <= h

        tam = h - l + 1
        mid = (l + h) // 2
        comparaciones += 1
        mayor = A[mid] > A[h]
        camino.append(mayor)

        if mayor:
            l = mid + 1
        else:
            h = mid
        if check:
            assert 1 <= h - l + 1 <= (tam + 1) // 2 < tam

    return l, comparaciones, tuple(camino)

def variante_mala(A):
    # Comparar con A[l]

    l = 0
    h = len(A) - 1

    while l < h:
        mid = (l + h) // 2
        if A[mid] >= A[l]:
            l = mid + 1
        else:
            h = mid

    return l


def con_repetidos(A):
    l = 0
    h = len(A) - 1
    comparaciones = 0

    while l < h:
        mid = (l + h) // 2
        comparaciones += 1

        if A[mid] > A[h]:
            l = mid + 1
        elif A[mid] < A[h]:
            h = mid
        else:
            h -= 1
    return A[l], comparaciones


def rotaciones(n, rng):
    base = sorted(rng.sample(range(10*n), n))
    return [base[r:] + base[:r] for r in range(n)]

def techo_log2(n):
    return (n - 1).bit_length()


if __name__ == "__main__":
    rng = random.Random(14)
    print("1) todas las rotaciones de un arreglo ordenado de elementos distintos")
    print(f"{'n':>4} {'rotaciones':>11} {'desacuerdos':>12} {'peor caso':>10} "
          f"{'ceil(log2 n)':>13} {'hojas del arbol':>16}")
    for n in [1, 2, 3, 4, 5, 8, 9, 16, 17, 33, 100, 1000]:
        malos = peor = 0
        hojas = set()
        for A in rotaciones(n, rng):
            i, c, camino = minimo_rotado(A, check=True)
            malos += A[i] != min(A)
            peor = max(peor, c)
            hojas.add(camino)
        assert peor <= techo_log2(n)
        print(f"{n:>4} {n:>11} {malos:>12} {peor:>10} {techo_log2(n):>13} {len(hojas):>16}")

    print()
    print("2) variante con A[lo] en vez de A[hi]: rotaciones en que falla")
    print(f"{'n':>4} {'falla en':>9} {'de':>5}")
    for n in [4, 8, 16, 100]:
        fallos = sum(A[variante_mala(A)] != min(A) for A in rotaciones(n, rng))
        print(f"{n:>4} {fallos:>9} {n:>5}")

    print()
    print("3) con elementos repetidos (todo unos, o un solo cero en cada posicion)")
    print(f"{'n':>4} {'entradas':>9} {'version distintos: fallos':>26} "
          f"{'version repetidos: fallos':>26} {'peor caso':>10} {'n-1':>5} {'cota n/2':>9}")
    for n in [8, 16, 64]:
        entradas = [[1] * n] + [[1] * k + [0] + [1] * (n - k - 1) for k in range(n)]
        sin = sum(A[minimo_rotado(A)[0]] != min(A) for A in entradas)
        con = sum(con_repetidos(A)[0] != min(A) for A in entradas)
        peor = max(con_repetidos(A)[1] for A in entradas)
        print(f"{n:>4} {len(entradas):>9} {sin:>26} {con:>26} {peor:>10} {n - 1:>5} {(n + 1) // 2:>9}")