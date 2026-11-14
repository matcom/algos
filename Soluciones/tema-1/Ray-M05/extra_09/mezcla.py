import sys
from itertools import combinations
from math import comb

from comun.tabla import tabla_md


def mezcla_optimizada(A, B, menor_o_igual=lambda x, y: x <= y):
    R, i, j = [], 0, 0
    while i < len(A) - 1 and j < len(B):
        if menor_o_igual(A[i], B[j]):
            R.append(A[i])
            i += 1
        else:
            R.append(B[j])
            j += 1
    return R + B[j:] + A[i:]


def intercalada(n):
    return list(range(1, 2 * n, 2)), list(range(2, 2 * n + 1, 2))


def contar(A, B):
    pares = []

    def menor_o_igual(x, y):
        pares.append((x, y))
        return x <= y

    return mezcla_optimizada(A, B, menor_o_igual), pares


def intercalaciones(n):
    for lugares in combinations(range(1, 2 * n + 1), n):
        en_A = set(lugares)
        yield list(lugares), [v for v in range(1, 2 * n + 1) if v not in en_A]


def _cuando_falla():
    filas = []
    for n in range(1, 9):
        peor, fallan, total = 0, 0, 0
        for A, B in intercalaciones(n):
            salida, pares = contar(A, B)
            falla = salida != sorted(A + B)
            assert falla == (A[-1] < B[-1])
            peor = max(peor, len(pares))
            fallan += falla
            total += 1
        filas.append([n, f"{total:,}", f"{fallan:,}", f"{fallan / total:.2f}", peor, 2 * n - 2])
        assert total == comb(2 * n, n) and 2 * fallan == total and peor == 2 * n - 2
    print(tabla_md(["n", "intercalaciones", "fallan", "fracción", "peor caso medido", "2n − 2"],
                   filas, "dddddd"))


SECCIONES = {
    "cuando_falla": _cuando_falla,
}

if __name__ == "__main__":
    SECCIONES[sys.argv[1]]()
