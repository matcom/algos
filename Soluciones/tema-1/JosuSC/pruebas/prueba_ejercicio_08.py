#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejercicio 8 - Casos de prueba
El elemento que aparece más de n/3 veces (Misra-Gries con k = 3).

Qué se comprueba:
  1. Exhaustivo: TODOS los arreglos sobre {A,B,C} de largo 0..9
     (29524 arreglos): las dos pasadas aciertan siempre contra el oráculo.
  2. Los contraejemplos del ejercicio, uno por uno:
       [A,B,C,A,B,C,D,D]  -> el atajo dice [D], la verdad es []
       [B,B,B,B,B,A,A,C]  -> el atajo dice [A,B], la verdad es [B]
       [E,E,E,E,C]        -> el atajo dice [C,E], la verdad es [E]
       A^9 B              -> el atajo dice [A,B], la verdad es [A]
  3. El invariante vigilado en ejecución: en cada prefijo, todo elemento con
     más de un tercio de las apariciones es uno de los dos candidatos
     (y c1 != c2 cuando ambos contadores son positivos).
  4. La tabla de generadores de la sección 7, con la MISMA semilla y el
     MISMO orden de generación (seed 7, 5000 casos, n en [3,20]):
     el único generador que no atrapa al atajo es mayoría plantada con
     m1 != m2; las dos pasadas no fallan con ninguno.

Ejecutar:  python3 prueba_ejercicio_08.py
Solo usa la biblioteca estándar.
"""

import itertools
import random
from collections import Counter


def candidatos_n3(A):
    """Primera pasada: los dos candidatos y sus contadores."""
    c1, n1 = None, 0
    c2, n2 = None, 0
    for x in A:
        if n1 > 0 and x == c1:
            n1 += 1
        elif n2 > 0 and x == c2:
            n2 += 1
        elif n1 == 0:
            c1, n1 = x, 1
        elif n2 == 0:
            c2, n2 = x, 1
        else:
            n1 -= 1          # x distinto de ambos: se cancela una terna
            n2 -= 1
    return c1, n1, c2, n2


def mayoria_n3(A):
    """Dos pasadas: verifica los candidatos contra el umbral n/3."""
    c1, n1, c2, n2 = candidatos_n3(A)
    return sorted({c for c in (c1, c2) if c is not None and 3 * A.count(c) > len(A)})


def atajo(A):
    """La versión que NO verifica: devuelve los de contador positivo."""
    c1, n1, c2, n2 = candidatos_n3(A)
    return sorted({c for c, n in ((c1, n1), (c2, n2)) if c is not None and n > 0})


def oraculo_n3(A):
    n = len(A)
    return sorted({x for x, k in Counter(A).items() if 3 * k > n})


def candidatos_n3_vigilado(A):
    """Primera pasada comprobando el invariante tras cada prefijo."""
    c1, n1 = None, 0
    c2, n2 = None, 0
    for i, x in enumerate(A, start=1):
        if n1 > 0 and x == c1:
            n1 += 1
        elif n2 > 0 and x == c2:
            n2 += 1
        elif n1 == 0:
            c1, n1 = x, 1
        elif n2 == 0:
            c2, n2 = x, 1
        else:
            n1 -= 1
            n2 -= 1
        # c1 != c2 si ambos contadores son positivos
        assert not (n1 > 0 and n2 > 0 and c1 == c2), (A[:i], c1, n1, c2, n2)
        # el teorema, prefijo por prefijo: quien supera el tercio del prefijo
        # es uno de los dos candidatos
        prefijo = A[:i]
        for elem, k in Counter(prefijo).items():
            if 3 * k > i:
                assert elem in (c1, c2), (prefijo, elem, c1, c2)
    return c1, n1, c2, n2


def main():
    # ------------------------------------------------------------------
    # 1) Exhaustivo sobre {A,B,C}
    # ------------------------------------------------------------------
    alfabeto = "ABC"
    total = 0
    for largo in range(10):
        for tupla in itertools.product(alfabeto, repeat=largo):
            A = list(tupla)
            assert mayoria_n3(A) == oraculo_n3(A), A
            total += 1

    # ------------------------------------------------------------------
    # 2) Los contraejemplos del ejercicio, uno por uno
    # ------------------------------------------------------------------
    contraejemplos = [
        (["A", "B", "C", "A", "B", "C", "D", "D"], ["D"], []),          # sección 6
        (["B", "B", "B", "B", "B", "A", "A", "C"], ["A", "B"], ["B"]),  # 3 símbolos
        (["E", "E", "E", "E", "C"], ["C", "E"], ["E"]),                 # m1 = m2 plantado
        (["A"] * 9 + ["B"], ["A", "B"], ["A"]),                         # A^9 B
    ]
    for A, mal_atajo, verdad in contraejemplos:
        assert atajo(A) == mal_atajo, (A, atajo(A))
        assert mayoria_n3(A) == verdad == oraculo_n3(A), (A, mayoria_n3(A))

    # ------------------------------------------------------------------
    # 3) El invariante vigilado en ejecución (aleatorio + los contraejemplos)
    # ------------------------------------------------------------------
    random.seed(3)
    vigilados = 0
    for _ in range(4000):
        n = random.randint(0, 25)
        A = [random.choice("ABCDEFGH") for _ in range(n)]
        candidatos_n3_vigilado(A)
        vigilados += 1
    for A, *_ in contraejemplos:
        candidatos_n3_vigilado(A)

    # sin duplicados en la salida de las dos pasadas
    for _ in range(4000):
        n = random.randint(0, 25)
        A = [random.choice("ABCDEF") for _ in range(n)]
        r = mayoria_n3(A)
        assert r == sorted(set(r)) == oraculo_n3(A)

    # ------------------------------------------------------------------
    # 4) La tabla de generadores (mismo seed y mismo orden que el ejercicio)
    # ------------------------------------------------------------------
    def plantada_distinta(n):
        m1, m2 = random.sample("ABCDEF", 2)          # forzadas distintas
        return ([m1] * (n // 3 + 1) + [m2] * (n // 3 + 1)
                + [random.choice("ABCDEF") for _ in range(n - 2 * (n // 3 + 1))])

    def plantada_sin_forzar(n):
        m1, m2 = random.choice("ABCDEF"), random.choice("ABCDEF")
        return ([m1] * (n // 3 + 1) + [m2] * (n // 3 + 1)
                + [random.choice("ABCDEF") for _ in range(n - 2 * (n // 3 + 1))])

    generadores = {
        "mayoría plantada (m1 != m2)": plantada_distinta,
        "mayoría plantada (sin forzar)": plantada_sin_forzar,
        "binario": lambda n: [random.choice("AB") for _ in range(n)],
        "3 símbolos": lambda n: [random.choice("ABC") for _ in range(n)],
        "5 símbolos": lambda n: [random.choice("ABCDE") for _ in range(n)],
        "8 símbolos": lambda n: [random.choice("ABCDEFGH") for _ in range(n)],
    }

    random.seed(7)
    print(f"{'generador':>32} {'atajo':>8} {'dos pasadas':>12}")
    for nombre, generar in generadores.items():
        casos = [generar(random.randint(3, 20)) for _ in range(5000)]
        f_atajo = sum(atajo(A) != oraculo_n3(A) for A in casos) / len(casos)
        f_correcto = sum(mayoria_n3(A) != oraculo_n3(A) for A in casos) / len(casos)
        print(f"{nombre:>32} {100 * f_atajo:>7.1f}% {100 * f_correcto:>11.1f}%")
        assert f_correcto == 0.0, nombre
        if nombre.startswith("mayoría plantada (m1"):
            assert f_atajo == 0.0, (nombre, f_atajo)      # el único que no la atrapa
        else:
            assert f_atajo > 0.05, (nombre, f_atajo)

    print("ejercicio 8: todo correcto")
    print(f"  exhaustivo sobre {{A,B,C}}: {total} arreglos, dos pasadas impecables")
    print("  los 4 contraejemplos del ejercicio reproducidos exactamente")
    print(f"  invariante vigilado prefijo por prefijo en {vigilados} arreglos aleatorios")
    print("  tabla de generadores reproducida (seed 7): solo 'plantada m1 != m2' no atrapa al atajo")


if __name__ == "__main__":
    main()
