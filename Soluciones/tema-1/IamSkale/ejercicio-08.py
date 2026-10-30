"""Ejercicio 8 ★★ — Elementos que aparecen más de $n/3$ veces (C3)

Código de validación de ejercicio-08.md.
Ejecutar con: python ejercicio-08.py
"""


# -------------------- Parte 1 --------------------

def primera_pasada(A):
    c1, n1, c2, n2 = None, 0, None, 0
    for x in A:
        if x == c1:
            n1 += 1
        elif x == c2:
            n2 += 1
        elif n1 == 0:
            c1, n1 = x, 1
        elif n2 == 0:
            c2, n2 = x, 1
        else:                       # x distinto de los dos candidatos, ambos con copias
            n1 -= 1
            n2 -= 1
    return c1, n1, c2, n2

def mas_de_un_tercio(A):
    c1, n1, c2, n2 = primera_pasada(A)
    candidatos = [c for c, k in ((c1, n1), (c2, n2)) if k > 0]
    # segunda pasada: verificar
    return sorted(c for c in candidatos if 3 * A.count(c) > len(A))

# -------------------- Parte 2 --------------------

def atajo(A):
    c1, n1, c2, n2 = primera_pasada(A)
    return sorted(c for c, k in ((c1, n1), (c2, n2)) if k > 0)

# -------------------- Parte 3 --------------------

import random
from collections import Counter

def oraculo(A):
    return sorted(x for x, k in Counter(A).items() if 3 * k > len(A))

# -------------------- Parte 4 --------------------

for s in ["", "A", "AB", "ABB", "AAB", "ABC", "AABBC", "ABCABCAAB", "AAABBBCC", "ABACADAEA"]:
    A = list(s)
    print(f"{s!r:>13}: correcto={mas_de_un_tercio(A)}  atajo={atajo(A)}  oráculo={oraculo(A)}")
    assert mas_de_un_tercio(A) == oraculo(A)

# -------------------- Parte 5 --------------------

def se_parte_en_ternas(S):
    return len(S) % 3 == 0 and all(3 * k <= len(S) for k in Counter(S).values())

def primera_pasada_vigilada(A):
    c1, n1, c2, n2 = None, 0, None, 0
    for i, x in enumerate(A):
        if x == c1:
            n1 += 1
        elif x == c2:
            n2 += 1
        elif n1 == 0:
            c1, n1 = x, 1
        elif n2 == 0:
            c2, n2 = x, 1
        else:
            n1 -= 1
            n2 -= 1
        resto = Counter(A[:i + 1])
        resto[c1] -= n1
        resto[c2] -= n2
        assert c1 != c2 and resto[c1] >= 0 and resto[c2] >= 0
        assert se_parte_en_ternas(list(resto.elements()))
    return c1, n1, c2, n2

random.seed(3)
prefijos, fallos = 0, 0
for _ in range(3000):
    A = [random.choice("ABCD") for _ in range(random.randint(1, 15))]
    try:
        primera_pasada_vigilada(A)
    except AssertionError:                     # algún prefijo rompió el invariante
        fallos += 1
    prefijos += len(A)
if fallos == 0:
    print("invariante comprobado en", prefijos, "prefijos, sin fallos")
else:
    print(f"el invariante falla en {fallos} de 3000 arreglos ({prefijos} prefijos)")

# -------------------- Parte 6 --------------------

def un_plantado(n):
    m = random.choice("ABCDE")
    k = n // 3 + 1
    A = [m] * k + [random.choice("ABCDE") for _ in range(n - k)]
    random.shuffle(A)
    return A

def dos_plantados(n):
    a, b = random.sample("ABCDE", 2)
    k = n // 3 + 1
    if 2 * k > n:
        return [a] * n
    A = [a] * k + [b] * k + [random.choice("ABCDE") for _ in range(n - 2 * k)]
    random.shuffle(A)
    return A

generadores = {
    "dos plantados":   dos_plantados,
    "un plantado":     un_plantado,
    "binario":         lambda n: [random.choice("AB") for _ in range(n)],
    "3 símbolos":      lambda n: [random.choice("ABC") for _ in range(n)],
    "5 símbolos":      lambda n: [random.choice("ABCDE") for _ in range(n)],
}

random.seed(5)
print(f"{'generador':>16} {'atajo':>8} {'con verificación':>17}")
for nombre, generar in generadores.items():
    casos = [generar(random.randint(1, 15)) for _ in range(4000)]
    f_atajo = sum(atajo(A) != oraculo(A) for A in casos) / len(casos)
    f_bien = sum(mas_de_un_tercio(A) != oraculo(A) for A in casos) / len(casos)
    print(f"{nombre:>16} {100 * f_atajo:>7.1f}% {100 * f_bien:>16.1f}%")
    assert f_bien == 0
