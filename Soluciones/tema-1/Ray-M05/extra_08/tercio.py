import random
import sys
from collections import Counter


def primera_pasada(A):
    c1, k1, c2, k2 = None, 0, None, 0
    for x in A:
        if k1 > 0 and x == c1:
            k1 += 1
        elif k2 > 0 and x == c2:
            k2 += 1
        elif k1 == 0:
            c1, k1 = x, 1
        elif k2 == 0:
            c2, k2 = x, 1
        else:
            k1 -= 1
            k2 -= 1
    return [(c, k) for c, k in ((c1, k1), (c2, k2)) if k > 0]


def mas_de_un_tercio(A):
    return {c for c, _ in primera_pasada(A) if 3 * A.count(c) > len(A)}


def atajo(A):
    return {c for c, _ in primera_pasada(A)}


def oraculo(A):
    return {x for x, k in Counter(A).items() if 3 * k > len(A)}


def dos_tercios_plantados(n):
    m1, m2 = random.sample("ABCDE", 2)
    A = [m1, m2] * (n // 3 + 1)
    A += [random.choice("ABCDE") for _ in range(n - len(A))]
    random.shuffle(A)
    return A


def se_parte_en_trios(S):
    return len(S) % 3 == 0 and all(3 * k <= len(S) for k in Counter(S).values())


def primera_pasada_vigilada(A):
    c1, k1, c2, k2 = None, 0, None, 0
    for i, x in enumerate(A):
        if k1 > 0 and x == c1:
            k1 += 1
        elif k2 > 0 and x == c2:
            k2 += 1
        elif k1 == 0:
            c1, k1 = x, 1
        elif k2 == 0:
            c2, k2 = x, 1
        else:
            k1 -= 1
            k2 -= 1
        resto = Counter(A[:i + 1])
        for c, k in ((c1, k1), (c2, k2)):
            if k > 0:
                resto[c] -= k
        assert not (k1 > 0 and k2 > 0 and c1 == c2), "candidatos distintos"
        assert all(v >= 0 for v in resto.values())
        assert se_parte_en_trios(list(resto.elements())), "tríos de distintos"
    return [(c, k) for c, k in ((c1, k1), (c2, k2)) if k > 0]


def _generador():
    random.seed(5)
    casos = [dos_tercios_plantados(random.randint(2, 15)) for _ in range(4000)]
    f_atajo = sum(atajo(A) != oraculo(A) for A in casos)
    f_bien = sum(mas_de_un_tercio(A) != oraculo(A) for A in casos)
    print(f"Sobre {len(casos):,} arreglos de largo entre 2 y 15, el atajo se equivoca en "
          f"{f_atajo} y la versión de dos pasadas en {f_bien}.")


def _vigilado():
    random.seed(3)
    prefijos = 0
    for _ in range(3000):
        A = [random.choice("ABCD") for _ in range(random.randint(1, 15))]
        primera_pasada_vigilada(A)
        prefijos += len(A)
    print(f"Invariante comprobado en {prefijos:,} prefijos, sin fallos.")


SECCIONES = {
    "generador": _generador,
    "vigilado": _vigilado,
}

if __name__ == "__main__":
    SECCIONES[sys.argv[1]]()
