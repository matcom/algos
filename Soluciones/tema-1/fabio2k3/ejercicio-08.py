import random

from collections import Counter
from itertools import permutations

def primera_pasada(A, check = False):
    c1 = None
    c2 = None
    k1 = k2 = 0

    for i, x in enumerate (A):
        if k1 > 0 and x == c1:
            k1 += 1
        elif k2 > 0 and x == c2:
            k2 += 1
        elif k1 == 0:
            c1 = x
            k1 = 1
        elif k2 == 0:
            c2 = x
            k2 = 1
        else:
            k1 -= 1
            k2 -= 1
        if check:
            assert k1 == 0 or k2 == 0 or c1 != c2
            resto = Counter(A[:i + 1])

            if k1 > 0:
                resto[c1] -= k1
            if k2 > 0:
                resto[c2] -= k2

            assert all(v >= 0 for v in resto.values())
            assert se_divide_en_tripletas(list(resto.elements()))
    return c1, k1, c2, k2

def se_divide_en_tripletas(Q):
    return len(Q) % 3 == 0 and all(3*k <= len(Q) for k in Counter(Q).values())

def candidatos(A, check = False):
    c1, k1, c2, k2 = primera_pasada(A, check)
    return [c for c, k in ((c1, k1), (c2, k2)) if k > 0]

def frecuentes(A, check = False):
    n = len(A)
    cuenta =Counter(A)
    return sorted(c for c in candidatos(A, check) if 3*cuenta[c] > n)

def atajo(A):
    return sorted(candidatos(A))

def oracle(A):
    return sorted(x for x, k in Counter(A).items() if 3*k > len(A))

def plantada1(n, r):
    m = r.choice("ABCDE")
    A = [m] * (n // 3 + 1) + [r.choice("ABCDE") for _ in range(n - n//3 -1)]
    r.shuffle(A)
    return A

def plantada2 (n,r):
    if 2 * (n//3 + 1) >n:
        return plantada1(n,r)
    a, b = r.sample("ABCDE", 2)
    k = n//3 + 1
    A = [a] * k + [b] * k + [r.choice("ABCDE") for _ in range(n - 2 * k)]

    r.shuffle(A)
    return A

def ternario_exacto(n,r):
    m = max(1, n//3)
    A = list("A" * m + "B" * m + "C"*m)
    r.shuffle(A)
    return A

def binario_balanceado(n,r):
    while True:
        A = [r.choice("AB") for _ in range(n)]
        if all(3*k > n for k in Counter(A).values()):
            return A



if __name__ == "__main__":
    print("contraejemplo minimo del atajo:")
    A = list("ABCD")
    print(f"  A = {A}  atajo = {atajo(A)}  correcto = {oracle(A)}")
    A = list("AABCD")
    print(f"  A = {A} atajo = {atajo(A)}  correcto = {oracle(A)}")
    print()

    generadores = {
        "plantada, 1 frecuente": plantada1,
        "plantada, 2 frecuentes": plantada2,
        "binario": lambda n, r: [r.choice("AB") for _ in range(n)],
        "3 símbolos": lambda n, r: [r.choice("ABC") for _ in range(n)],
        "5 símbolos": lambda n, r: [r.choice("ABCDE") for _ in range(n)],
        "ternario, n/3 exacto": ternario_exacto,
        "binario balanceado": binario_balanceado,
    }
    r = random.Random(5)
    print(f"{'generador':>24} {'atajo':>8} {'dos pasadas':>12}")
    for nombre, g in generadores.items():
        casos = []
        for _ in range(4000):
            n = 3 * r.randint(1, 5) if "n/3" in nombre else r.randint(1, 15)
            casos.append(g(n, r))
        f_atajo = sum(atajo(A) != oracle(A) for A in casos) / len(casos)
        f_bm = sum(frecuentes(A, check=True) != oracle(A) for A in casos) / len(casos)
        print(f"{nombre:>24} {100 * f_atajo:>7.1f}% {100 * f_bm:>11.1f}%")

    print()
    total = fallos = 0
    for m in range(1, 5):
        for P in set(permutations("A" * m + "B" * m + "C" * m)):
            total += 1
            fallos += atajo(list(P)) != oracle(list(P))
    print(f"ternario n/3 exacto, TODAS las permutaciones (m = 1..4): "
          f"{fallos} fallos de {total}")