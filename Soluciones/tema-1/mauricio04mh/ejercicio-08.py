"""Ejercicio 8. Elementos que aparecen más de n/3 veces (Misra-Gries, dos candidatos)."""
import random
from collections import Counter
from itertools import product


def candidatos(L, vigilar=False):
    c1 = c2 = None
    k1 = k2 = 0
    t = 0                                     # tríos cancelados
    for i, x in enumerate(L):
        if x == c1:
            k1 += 1
        elif x == c2:
            k2 += 1
        elif k1 == 0:
            c1, k1 = x, 1
        elif k2 == 0:
            c2, k2 = x, 1
        else:
            k1 -= 1
            k2 -= 1
            t += 1
        if vigilar:                           # invariante reforzado
            assert i + 1 == 3 * t + k1 + k2
            assert k1 >= 0 and k2 >= 0 and (c1 is None or c1 != c2)
            resto = Counter(L[:i + 1])
            if c1 is not None:
                resto[c1] -= k1
            if c2 is not None:
                resto[c2] -= k2
            assert all(v >= 0 for v in resto.values())
            assert sum(resto.values()) == 3 * t
            assert all(v <= t for v in resto.values())   # a lo sumo una copia por trío
    return (c1, k1), (c2, k2)


def oraculo(L):
    n = len(L)
    return {x for x, c in Counter(L).items() if 3 * c > n}


def sin_verificar(L):
    (c1, k1), (c2, k2) = candidatos(L)
    return {c for c, k in ((c1, k1), (c2, k2)) if k > 0}


def con_verificar(L):
    (c1, _), (c2, _) = candidatos(L)
    n = len(L)
    return {c for c in {c1, c2} if c is not None and 3 * L.count(c) > n}


S = "ABCDE"


def plantada_dos(n):
    a, b = random.sample(S, 2)
    t = n // 3 + 1
    L = [a] * t + [b] * t + [random.choice(S) for _ in range(n - 2 * t)]
    random.shuffle(L)
    return L


def plantada_una(n):
    a = random.choice(S)
    t = n // 3 + 1
    L = [a] * t + [random.choice(S) for _ in range(n - t)]
    random.shuffle(L)
    return L


generadores = {
    "plantada de dos": (plantada_dos, 6, 15),
    "plantada de uno": (plantada_una, 1, 15),
    "binario":         (lambda n: [random.choice("AB") for _ in range(n)], 1, 15),
    "3 símbolos":      (lambda n: [random.choice("ABC") for _ in range(n)], 1, 15),
    "5 símbolos":      (lambda n: [random.choice(S) for _ in range(n)], 1, 15),
    "todos distintos": (lambda n: random.sample(range(100), n), 1, 15),
}

if __name__ == "__main__":
    # 1. Trazas del enunciado
    for L in ([1, 2, 1, 2, 3, 1, 2], [1, 2, 3, 4, 5, 1, 1], [1, 2, 3, 4], [1, 2, 1, 3, 4],
              list("AAAAAB")):
        print(f"{str(L):<24} candidatos {candidatos(L, vigilar=True)}  "
              f"sin verificar {sin_verificar(L)}  con verificar {con_verificar(L)}  "
              f"oráculo {oraculo(L)}")

    # 2. El teorema, exhaustivo: todas las listas con 3 símbolos y largo <= 9
    total = 0
    for n in range(1, 10):
        for L in product("ABC", repeat=n):
            L = list(L)
            (c1, k1), (c2, k2) = candidatos(L, vigilar=True)
            activos = {c for c, k in ((c1, k1), (c2, k2)) if k > 0}
            assert oraculo(L) <= activos          # ninguna respuesta se pierde
            assert con_verificar(L) == oraculo(L)
            total += 1
    print(f"\nTeorema comprobado en las {total} listas con alfabeto ABC y largo 1–9")

    # 3. Banco de pruebas con generadores
    random.seed(5)
    print(f"\n{'generador':>16} {'sin verificar':>14} {'dos pasadas':>12}")
    for nombre, (generar, lo, hi) in generadores.items():
        casos = [generar(random.randint(lo, hi)) for _ in range(4000)]
        f1 = sum(sin_verificar(L) != oraculo(L) for L in casos) / len(casos)
        f2 = sum(con_verificar(L) != oraculo(L) for L in casos) / len(casos)
        print(f"{nombre:>16} {100 * f1:>13.1f}% {100 * f2:>11.1f}%")
