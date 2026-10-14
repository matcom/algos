"""Casos de prueba del ejercicio 14.

Correr con `pytest test_ejercicio_14.py` o con `python test_ejercicio_14.py`.
"""

import math
import random

from ejercicio_06 import patrones as patrones_de_matriz
from ejercicio_14 import (
    Comparador, interseccion, hay_comun, interseccion_galope, oraculo, intercalado_perfecto,
    entrada_con_par_igual, par_de_vecinos, patrones, optimo_exacto,
)


def listas(rng, n_max=30, rango=60):
    na, nb = rng.randint(0, n_max), rng.randint(0, n_max)
    rango = max(rango, na, nb)
    return sorted(rng.sample(range(rango), na)), sorted(rng.sample(range(rango), nb))


def test_correctos_contra_el_oraculo():
    rng = random.Random(1)
    for _ in range(5000):
        A, B = listas(rng, rango=rng.choice([10, 60, 10**6]))
        esperado = oraculo(A, B)
        assert interseccion(A, B) == esperado
        assert interseccion_galope(A, B) == esperado
        assert interseccion_galope(B, A) == esperado
        assert hay_comun(A, B) == bool(esperado)


def test_casos_borde():
    assert interseccion([], []) == [] and interseccion([1], []) == [] and interseccion([], [1]) == []
    assert interseccion([1, 2, 3], [1, 2, 3]) == [1, 2, 3]
    assert interseccion([1], [1]) == [1] and interseccion([1], [2]) == []


def test_invariante_vigilado():
    rng = random.Random(2)
    for _ in range(1000):
        A, B = listas(rng, n_max=15, rango=25)
        interseccion(A, B, vigilar=True)


def test_a_lo_sumo_2n_menos_1():
    # Potencial (n - i) + (n - j): baja al menos 1 por comparación.
    rng = random.Random(3)
    for _ in range(3000):
        n = rng.randint(1, 40)
        A = sorted(rng.sample(range(3 * n), n))
        B = sorted(rng.sample(range(3 * n), n))
        cmp = Comparador()
        interseccion(A, B, cmp)
        assert cmp.total <= 2 * n - 1


def test_intercalado_perfecto_usa_2n_menos_1():
    for n in range(1, 60):
        A, B = intercalado_perfecto(n)
        cmp = Comparador()
        assert interseccion(A, B, cmp) == [] and cmp.total == 2 * n - 1
        cmp = Comparador()
        assert not hay_comun(A, B, cmp) and cmp.total == 2 * n - 1


def test_variantes_del_adversario():
    # Cada variante: listas ordenadas, con un elemento común, y la única comparación
    # cuya respuesta cambia es la de su par de vecinos.
    for n in range(1, 25):
        A, B = intercalado_perfecto(n)
        for k in range(2 * n - 1):
            A2, B2 = entrada_con_par_igual(n, k)
            assert A2 == sorted(set(A2)) and B2 == sorted(set(B2))
            assert len(oraculo(A2, B2)) == 1
            cambios = [(i, j) for i in range(n) for j in range(n)
                       if (A[i] > B[j]) - (A[i] < B[j]) != (A2[i] > B2[j]) - (A2[i] < B2[j])]
            assert cambios == [par_de_vecinos(k)]


def test_quien_no_compara_un_par_no_distingue():
    # Las respuestas fuera del par k coinciden en el intercalado y en su variante k,
    # pero una tiene intersección vacía y la otra no.
    n = 7
    A, B = intercalado_perfecto(n)
    for k in range(2 * n - 1):
        A2, B2 = entrada_con_par_igual(n, k)
        i0, j0 = par_de_vecinos(k)
        for i in range(n):
            for j in range(n):
                if (i, j) != (i0, j0):
                    assert (A[i] > B[j]) - (A[i] < B[j]) == (A2[i] > B2[j]) - (A2[i] < B2[j])
        assert hay_comun(A, B) != hay_comun(A2, B2)


def test_patrones_son_delannoy():
    # Los órdenes relativos posibles son los números de Delannoy centrales.
    delannoy = [1, 3, 13, 63, 321, 1683]
    for n in range(1, 6):
        assert len(patrones(n)) == delannoy[n]


def test_mismos_patrones_que_el_ejercicio_6():
    # Con las columnas invertidas, los signos de A[i] - B[j] son patrones de una matriz
    # ordenada (ejercicio 6). Para n <= 3 son exactamente todos: los dos juegos coinciden.
    for n in [1, 2, 3]:
        de_listas = {tuple(signos[i * n + (n - 1 - c)] for i in range(n) for c in range(n))
                     for signos, _ in patrones(n)}
        assert de_listas == set(patrones_de_matriz(n))


def test_optimo_exacto_por_fuerza_bruta():
    for n in [1, 2, 3]:
        assert optimo_exacto(n)[0] == 2 * n - 1


def test_galope_gana_con_listas_desparejas():
    rng = random.Random(4)
    B = sorted(rng.sample(range(10**6), 10**4))
    A = sorted(rng.sample(range(10**6), 10))
    c1, c2 = Comparador(), Comparador()
    interseccion(A, B, c1)
    interseccion_galope(A, B, c2)
    assert c2.total * 10 < c1.total


if __name__ == "__main__":
    pruebas = [f for nombre, f in sorted(globals().items()) if nombre.startswith("test_")]
    for prueba in pruebas:
        prueba()
        print("ok", prueba.__name__)
    print(f"{len(pruebas)} pruebas pasaron")
