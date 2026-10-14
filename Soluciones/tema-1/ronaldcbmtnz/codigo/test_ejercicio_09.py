"""Casos de prueba del ejercicio 9.

Correr con `pytest test_ejercicio_09.py` o con `python test_ejercicio_09.py`.
"""

import math
import random

from ejercicio_09 import (
    mezcla, mezcla_optimizada, mezcla_sin_la_ultima, mezcla_con_atajo, correr,
    es_correcta_en, intercalados, intercalado_perfecto, adversario,
)


def test_peor_caso_de_la_optimizada():
    # Sección 2: exactamente 2n - 2 comparaciones en el peor caso (0 con n = 1).
    for n in range(1, 9):
        peor = max(correr(mezcla_optimizada, A, B)[1] for A, B in intercalados(n))
        assert peor == max(2 * n - 2, 0)


def test_la_mezcla_usa_2n_menos_1_y_es_correcta():
    for n in range(1, 9):
        peor = 0
        for A, B in intercalados(n):
            r, c = correr(mezcla, A, B)
            assert r == sorted(A + B)
            peor = max(peor, c)
        assert peor == 2 * n - 1


def test_promedio_exacto_de_la_mezcla():
    # Costo promedio sobre intercalados: 2n - 2n/(n+1).
    for n in range(1, 9):
        total = sum(correr(mezcla, A, B)[1] for A, B in intercalados(n))
        assert math.isclose(total / math.comb(2 * n, n), 2 * n - 2 * n / (n + 1))


def test_falla_si_y_solo_si_a_n_menor_que_b_n():
    # Teorema 2, con valores distintos.
    for n in range(1, 9):
        for A, B in intercalados(n):
            assert es_correcta_en(mezcla_optimizada, A, B) == (A[-1] > B[-1])


def test_falla_exactamente_en_la_mitad():
    for n in range(1, 9):
        fallos = sum(not es_correcta_en(mezcla_optimizada, A, B) for A, B in intercalados(n))
        assert 2 * fallos == math.comb(2 * n, n)


def test_con_repetidos_tambien():
    # Con empates, falla si y solo si a_n < b_n (estricto).
    rng = random.Random(1)
    for _ in range(3000):
        n = rng.randint(1, 10)
        A = sorted(rng.randrange(6) for _ in range(n))
        B = sorted(rng.randrange(6) for _ in range(n))
        assert es_correcta_en(mezcla_optimizada, A, B) == (A[-1] >= B[-1])


def test_falla_en_el_intercalado_perfecto():
    for n in range(1, 30):
        A, B = intercalado_perfecto(n)
        r, c = correr(mezcla_optimizada, A, B)
        assert r != sorted(A + B)
        assert c == max(2 * n - 3, 0)


def test_detector_del_adversario():
    # Encuentra entradas malas para las dos "optimizaciones" y ninguna para las correctas.
    for n in range(1, 12):
        for malo in (mezcla_optimizada, mezcla_sin_la_ultima):
            res = adversario(malo, n)
            assert res is not None and not es_correcta_en(malo, res["A"], res["B"])
        for bueno in (mezcla, mezcla_con_atajo):
            assert adversario(bueno, n) is None


if __name__ == "__main__":
    pruebas = [f for nombre, f in sorted(globals().items()) if nombre.startswith("test_")]
    for prueba in pruebas:
        prueba()
        print("ok", prueba.__name__)
    print(f"{len(pruebas)} pruebas pasaron")
