"""Casos de prueba del ejercicio 1.

Correr con `pytest test_ejercicio_01.py` o con `python test_ejercicio_01.py`.
Cada prueba comprueba una afirmación concreta del informe.
"""

import math
import random

from ejercicio_01 import (
    HORA, M, COSTOS, nlogn, mayor_n, factor_medido, factor_potencia,
    iterados_nlogn, factor_nlogn, cota_inferior_nlogn, contraccion_nlogn, factor_lambert,
    tamano_lambert, insercion, mezcla, peor_caso, costo_insercion,
    costo_mezcla, costo_patologico, costo_orden_menor,
)


def test_mayor_n_cumple_su_definicion():
    # costo(n) <= B < costo(n + 1): es el mayor, no solo uno que cabe.
    random.seed(1)
    costos = [lambda n: n, lambda n: n * n, nlogn, costo_insercion, costo_mezcla]
    for costo in costos:
        for _ in range(300):
            B = random.randint(10, 10**12)
            n = mayor_n(costo, B)
            assert costo(n) <= B < costo(n + 1)


def test_reproduce_la_tabla_de_la_conferencia_1():
    # C1, §7: n log n pasa de 9.86e10 a 7.8e13 y n² de 1.9e6 a 6e7.
    esperado = {"n": ("3.6e+12", "3.6e+15"), "n log n": ("9.86e+10", "7.8e+13"),
                "n^2": ("1.9e+06", "6e+07"), "n^3": ("1.53e+04", "1.53e+05"),
                "2^n": ("41", "51")}
    for nombre, (hoy, nuevo) in esperado.items():
        costo = COSTOS[nombre]
        assert f"{mayor_n(costo, HORA):.3g}" == hoy
        assert f"{mayor_n(costo, M * HORA):.3g}" == nuevo


def test_cuadratico_no_depende_de_la_constante_ni_del_presupuesto():
    # Sección 2: el factor es √1000 salvo el redondeo a enteros, que mueve
    # n'/n a lo sumo en √1000/n.
    for c in [0.5, 1, 3, 1000]:
        for B in [10**10, 10**14, HORA, 10**20]:
            costo = lambda n, c=c: c * n * n
            n = mayor_n(costo, B)
            assert abs(factor_medido(costo, B) - math.sqrt(M)) <= 2 * math.sqrt(M) / n


def test_potencias():
    # n^a da m^(1/a): lineal 1000, cuadrático 31.6, cúbico 10.
    assert math.isclose(factor_potencia(1), 1000)
    assert math.isclose(factor_potencia(2), math.sqrt(1000))
    assert math.isclose(factor_potencia(3), 10)
    assert abs(factor_medido(COSTOS["n^3"], HORA) - 10) < 1e-3


def test_nlogn_entre_las_cotas_de_la_proposicion_1():
    # M·L/(L + log2 M) < k < M para todo tamaño inicial.
    for n in [2, 10, 10**3, 10**6, 10**9, 10**12, 10**18, 10**30, 10**100]:
        k = factor_nlogn(n)
        assert cota_inferior_nlogn(n) < k < M


def test_iterados_alternan_y_convergen():
    # Lema de la sección 3.3: los iterados impares quedan debajo del factor,
    # los pares encima, y la distancia se multiplica por a lo sumo q(n) en cada paso.
    for n in [10**3, 10**6, 10**9, mayor_n(nlogn, HORA), 10**18]:
        k = factor_nlogn(n)
        q = contraccion_nlogn(n)
        it = iterados_nlogn(n, pasos=4)
        for t in range(1, 4):
            assert (it[t] < k) if t % 2 else (it[t] > k)
            assert abs(it[t] - k) <= q * abs(it[t - 1] - k)
    # Para la máquina de la conferencia, q ≈ 0.031: un dígito y medio por paso.
    assert 0.031 < contraccion_nlogn(mayor_n(nlogn, HORA)) < 0.032


def test_nlogn_busqueda_formula_y_lambert_coinciden():
    # Tres caminos independientes dan el mismo número.
    for B in [10**10, 10**12, HORA, 10**15]:
        medido = factor_medido(nlogn, B)
        punto_fijo = factor_nlogn(tamano_lambert(B))
        lambert = factor_lambert(B)
        assert math.isclose(punto_fijo, lambert, rel_tol=1e-9)
        assert math.isclose(medido, lambert, rel_tol=1e-5)
    assert abs(factor_medido(nlogn, HORA) - 791.3657) < 1e-4


def test_la_base_del_logaritmo_y_la_constante_no_importan_dado_n():
    # Sección 3.1: con el mismo tamaño inicial n0, c·n·log_b n da el mismo
    # factor para cualquier c y cualquier base b.
    for n0 in [10**6, 10**9, 10**12]:
        factores = []
        for b in [2, math.e, 10]:
            for c in [0.01, 1, 50]:
                costo = lambda n, b=b, c=c: c * n * math.log(n, b)
                assert mayor_n(costo, costo(n0)) == n0
                factores.append(factor_medido(costo, costo(n0)))
        assert max(factores) - min(factores) <= 2 / n0 * max(factores)


def test_los_algoritmos_ordenan():
    random.seed(2)
    for _ in range(300):
        A = [random.randint(-50, 50) for _ in range(random.randint(0, 40))]
        assert insercion(A)[0] == sorted(A)
        assert mezcla(A)[0] == sorted(A)


def test_formulas_de_peor_caso_por_fuerza_bruta():
    # Sección 5: el máximo sobre las n! permutaciones coincide con la fórmula.
    for n in range(9):
        assert peor_caso(insercion, n) == costo_insercion(n)
        assert peor_caso(mezcla, n) == costo_mezcla(n)


def test_formula_de_mezcla_cumple_la_recurrencia():
    # W(n) = W(⌈n/2⌉) + W(⌊n/2⌋) + n - 1, para n mucho más grandes que la fuerza bruta.
    for n in range(2, 5000):
        assert costo_mezcla(n) == costo_mezcla((n + 1) // 2) + costo_mezcla(n // 2) + n - 1


def test_algoritmos_reales():
    # Inserción da √1000; mezcla, un poco menos que n·log2 n por su término -n.
    assert abs(factor_medido(costo_insercion, HORA) - math.sqrt(M)) < 1e-4
    assert 780 < factor_medido(costo_mezcla, HORA) < factor_medido(nlogn, HORA)


def test_costo_patologico_es_theta_n2_y_creciente():
    # n² <= T(n) <= 2n² y T no decrece (la Proposición 3 lo necesita).
    previo = 0
    for n in range(1, 200000):
        t = costo_patologico(n)
        assert n * n <= t <= 2 * n * n
        assert t >= previo
        previo = t


def test_theta_no_basta():
    # Sección 4: el factor del costo patológico recorre casi toda la banda
    # [√500, √2000] y nunca sale de ella.
    factores = [factor_medido(costo_patologico, 10 ** (e / 8)) for e in range(64, 241)]
    assert min(factores) < 22.5 and max(factores) > 43.5
    assert all(math.sqrt(M / 2) * 0.999 <= f <= math.sqrt(2 * M) * 1.001 for f in factores)
    # El término lineal hace que el algoritmo "parezca lineal" mientras domina.
    assert factor_medido(costo_orden_menor, 10**8) > 900
    assert abs(factor_medido(costo_orden_menor, 10**30) - math.sqrt(M)) < 1e-4


if __name__ == "__main__":
    pruebas = [f for nombre, f in sorted(globals().items()) if nombre.startswith("test_")]
    for prueba in pruebas:
        prueba()
        print("ok", prueba.__name__)
    print(f"{len(pruebas)} pruebas pasaron")
