"""Ejercicio 9. Mezcla normal, mezcla «optimizada» y la cota 2n-1."""


def mezcla(A, B):
    n = len(A)
    i = j = comps = 0
    salida = []
    while i < n and j < n:
        comps += 1
        if A[i] <= B[j]:
            salida.append(A[i]); i += 1
        else:
            salida.append(B[j]); j += 1
    return salida + A[i:] + B[j:], comps


def mezcla_optimizada(A, B):
    n = len(A)
    i = j = comps = 0
    salida = []
    while n - i > 1 and j < n:
        comps += 1
        if A[i] <= B[j]:
            salida.append(A[i]); i += 1
        else:
            salida.append(B[j]); j += 1
    return salida + B[j:] + A[i:], comps


def pares_vecinos_comparados(A, B, ejecutar):
    """Pares (a, b) que la mezcla comparó, registrados con un envoltorio."""
    visto = set()

    class V(int):
        def __le__(self, otro):
            visto.add(frozenset((int(self), int(otro))))
            return int(self) <= int(otro)

    ejecutar([V(a) for a in A], [V(b) for b in B])
    return visto


if __name__ == "__main__":
    from itertools import combinations

    A, B = [2, 4, 6], [1, 3, 5]
    print("ejemplo A=[2,4,6], B=[1,3,5]:", mezcla_optimizada(A, B), "(correcta:", sorted(A + B), ")")

    print(f"\n{'n':>3} {'normal máx.':>12} {'2n-1':>5} {'optimizada máx.':>16} {'2n-2':>5} {'entradas incorrectas':>21} {'de':>6}")
    for n in range(2, 8):
        peor_n = peor_o = incorrectas = total = 0
        for elegidos in combinations(range(2 * n), n):          # todas las intercalaciones
            A = list(elegidos)
            B = [x for x in range(2 * n) if x not in elegidos]
            m1, c1 = mezcla(A, B)
            m2, c2 = mezcla_optimizada(A, B)
            assert m1 == sorted(A + B)
            peor_n, peor_o = max(peor_n, c1), max(peor_o, c2)
            incorrectas += m2 != sorted(A + B)
            total += 1
        assert peor_n == 2 * n - 1 and peor_o == 2 * n - 2
        print(f"{n:>3} {peor_n:>12} {2 * n - 1:>5} {peor_o:>16} {2 * n - 2:>5} {incorrectas:>21} {total:>6}")

    print("\nEntrada del adversario (cadena intercalada) para n = 3:")
    A, B = [1, 3, 5], [2, 4, 6]
    print("  mezcla normal      :", mezcla(A, B))
    print("  mezcla optimizada  :", mezcla_optimizada(A, B))
    vistos = pares_vecinos_comparados(A, B, mezcla)
    print("  pares comparados por la normal:", sorted(tuple(sorted(p)) for p in vistos))
    vistos = pares_vecinos_comparados(A, B, mezcla_optimizada)
    print("  pares comparados por la optimizada:", sorted(tuple(sorted(p)) for p in vistos))
    print("Entrada gemela A'=[1,3,6], B'=[2,4,5]:", mezcla_optimizada([1, 3, 6], [2, 4, 5]))
