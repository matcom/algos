"""Ejercicio 8: elementos que aparecen más de n/3 veces (Boyer-Moore con dos candidatos).
Vigila el invariante reforzado y compara el algoritmo verificado con el atajo
que devuelve los candidatos con contador positivo sin verificarlos."""
import random
from collections import Counter


def se_parte_en_ternas(S):
    """Un multiconjunto se parte en ternas de elementos distintos si y solo si su tamaño es
    múltiplo de 3 y ningún elemento ocupa más de un tercio (agrupando por clases y
    repartiendo la lista ordenada en las posiciones i, i + m, i + 2m, con m = |S|/3)."""
    S = sorted(S)
    if len(S) % 3:
        return False
    m = len(S) // 3
    return all(len({S[i], S[i + m], S[i + 2 * m]}) == 3 for i in range(m))


def primera_pasada(A, vigilar=False):
    c1, k1, c2, k2 = None, 0, None, 0
    for i, x in enumerate(A):
        if x == c1:
            k1 += 1
        elif x == c2:
            k2 += 1
        elif k1 == 0:
            c1, k1 = x, 1
        elif k2 == 0:
            c2, k2 = x, 1
        else:                       # x, c1 y c2 distintos: se tacha la terna
            k1 -= 1
            k2 -= 1
        if vigilar:
            # invariante: el prefijo = ternas de distintos + k1 copias de c1 + k2 copias de c2
            assert not (k1 > 0 and k2 > 0 and c1 == c2)
            resto = Counter(A[:i + 1])
            resto[c1] -= k1
            resto[c2] -= k2
            assert all(v >= 0 for v in resto.values())
            assert se_parte_en_ternas(list(resto.elements()))
    return c1, k1, c2, k2


def mas_de_un_tercio(A):
    """El algoritmo correcto: primera pasada y verificación."""
    c1, _, c2, _ = primera_pasada(A)
    return {c for c in (c1, c2) if c is not None and 3 * A.count(c) > len(A)}


def atajo(A):
    """La versión sin verificar: los candidatos con contador positivo."""
    c1, k1, c2, k2 = primera_pasada(A)
    return {c for c, k in ((c1, k1), (c2, k2)) if k > 0}


def oraculo(A):
    return {x for x, k in Counter(A).items() if 3 * k > len(A)}


# 1. Invariante vigilado y algoritmo correcto contra el oráculo
random.seed(8)
prefijos = 0
for _ in range(3000):
    A = [random.choice("ABCD") for _ in range(random.randint(1, 15))]
    primera_pasada(A, vigilar=True)
    assert mas_de_un_tercio(A) == oraculo(A)
    prefijos += len(A)
print(f"invariante comprobado en {prefijos:,} prefijos; algoritmo verificado correcto siempre")
print(f"contraejemplos del atajo: ABCD -> {atajo(list('ABCD'))}, AAAB -> {atajo(list('AAAB'))}\n")


# 2. Qué generadores atrapan al atajo
def plantados(cuantos):
    def generar(n):
        m = n // 3 + 1                                  # más de n/3 copias
        elegidos = random.sample("ABCDE", cuantos)
        A = [e for e in elegidos for _ in range(m)]
        A += [random.choice("ABCDE") for _ in range(n - len(A))]
        random.shuffle(A)
        return A
    return generar


generadores = {
    "dos plantados": (plantados(2), 4),              # n >= 4 para que quepan dos
    "uno plantado": (plantados(1), 1),
    "binario": (lambda n: [random.choice("AB") for _ in range(n)], 1),
    "3 símbolos": (lambda n: [random.choice("ABC") for _ in range(n)], 1),
    "5 símbolos": (lambda n: [random.choice("ABCDE") for _ in range(n)], 1),
}
print(f"{'generador':>15} {'atajo':>7} {'verificado':>11}")
for nombre, (generar, n_min) in generadores.items():
    casos = [generar(random.randint(n_min, 15)) for _ in range(4000)]
    f_atajo = 100 * sum(atajo(A) != oraculo(A) for A in casos) / len(casos)
    f_bien = 100 * sum(mas_de_un_tercio(A) != oraculo(A) for A in casos) / len(casos)
    print(f"{nombre:>15} {f_atajo:>6.1f}% {f_bien:>10.1f}%")
