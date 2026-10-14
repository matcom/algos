"""Casos de prueba del ejercicio 10.

Correr con `pytest test_ejercicio_10.py` o con `python test_ejercicio_10.py`.
Cada prueba comprueba una afirmación concreta del informe.
"""

import itertools
import math
import random
from fractions import Fraction

from ejercicio_10 import (
    Pruebas, _ordenar_por_mezcla, fuerza_bruta, ordenar_y_recorrer, ordenar_y_recorrer_rapido,
    distintos_por_reduccion, rejilla_1d, huecos_decrecientes, armonico,
    reconstrucciones_esperadas, log3_factorial,
)


def entradas_al_azar(rng, cantidad, n_max=60, rango=10**6):
    for _ in range(cantidad):
        n = rng.randint(2, n_max)
        r = rng.choice([5, 50, rango])               # rangos chicos: muchos empates y repetidos
        yield [rng.randint(-r, r) for _ in range(n)]


def comprobar(xs, resultado, delta):
    d, (i, j) = resultado[:2]
    assert d == delta
    assert i < j and abs(xs[i] - xs[j]) == delta


def test_todos_los_algoritmos_coinciden_con_la_fuerza_bruta():
    rng = random.Random(10)
    for xs in entradas_al_azar(rng, 1500):
        delta = fuerza_bruta(xs)[0]
        comprobar(xs, ordenar_y_recorrer(xs), delta)
        comprobar(xs, ordenar_y_recorrer_rapido(xs), delta)
        comprobar(xs, rejilla_1d(xs, semilla=rng.randrange(10**9)), delta)
        comprobar(xs, rejilla_1d(xs, barajar=False), delta)


def test_casos_borde():
    for xs in [[5, 9], [9, 5], [7, 7], [3, 3, 3, 3], [-10, 10, 0], [0, 2**100, 2**100 + 1],
               [10**18, -10**18, 1, 2]]:
        delta = fuerza_bruta(xs)[0]
        comprobar(xs, ordenar_y_recorrer(xs), delta)
        for s in range(20):
            comprobar(xs, rejilla_1d(xs, semilla=s), delta)


def test_fracciones_exactas():
    rng = random.Random(11)
    for _ in range(300):
        xs = [Fraction(rng.randint(-1000, 1000), rng.randint(1, 50)) for _ in range(rng.randint(2, 30))]
        delta = fuerza_bruta(xs)[0]
        comprobar(xs, ordenar_y_recorrer(xs), delta)
        comprobar(xs, rejilla_1d(xs, semilla=rng.randrange(10**9)), delta)


def test_lema_1_con_empates():
    # El mínimo sobre todos los pares es el mínimo sobre los consecutivos del orden.
    rng = random.Random(12)
    for xs in entradas_al_azar(rng, 1000, rango=20):
        s = sorted(xs)
        assert min(b - a for a, b in zip(s, s[1:])) == fuerza_bruta(xs)[0]


def test_tres_celdas_bastan():
    # Lema 7: si |x - y| < δ, sus celdas difieren en a lo sumo 1.
    rng = random.Random(13)
    for _ in range(20000):
        delta = rng.choice([1, 2, 3, 7, 10**9, Fraction(3, 7), Fraction(22, 5)])
        x = Fraction(rng.randint(-10**6, 10**6), rng.randint(1, 20))
        y = x + delta * Fraction(rng.randint(-999, 999), 1000)   # |x - y| < δ
        assert abs(x // delta - y // delta) <= 1


def test_un_punto_por_celda():
    # Lema 6: si todos los pares están a distancia >= δ, las celdas x // δ son distintas.
    rng = random.Random(14)
    for _ in range(2000):
        xs = rng.sample(range(-10**4, 10**4), rng.randint(2, 50))
        delta = fuerza_bruta(xs)[0]
        assert len({x // delta for x in xs}) == len(xs)


def test_invariantes_vigilados():
    # Teorema 8: después de cada inserción, δ es el mínimo de los insertados y
    # la rejilla tiene exactamente a los insertados, cada uno en su celda.
    rng = random.Random(15)
    for xs in entradas_al_azar(rng, 400, n_max=40):
        rejilla_1d(xs, semilla=rng.randrange(10**9), vigilar=True)


def test_los_n_factorial_ordenes_van_a_hojas_distintas():
    # Teorema 3, comprobado sobre el árbol de la reducción: n! caminos distintos,
    # todos con la respuesta "todos distintos", y profundidad >= ⌈log3 n!⌉.
    for n in range(2, 7):
        caminos = set()
        profundidad = 0
        for perm in itertools.permutations(range(1, n + 1)):
            pruebas = Pruebas()
            assert distintos_por_reduccion(list(perm), pruebas)
            caminos.add(tuple(pruebas.camino))
            profundidad = max(profundidad, len(pruebas.camino))
        assert len(caminos) == math.factorial(n)
        assert profundidad >= math.ceil(log3_factorial(n) - 1e-9)


def test_la_reduccion_decide_distincion():
    rng = random.Random(16)
    for xs in entradas_al_azar(rng, 1500, rango=30):
        assert distintos_por_reduccion(xs) == (len(set(xs)) == len(xs))


def test_las_pruebas_son_lineales_y_las_cuenta_el_camino():
    # El camino registra una prueba por comparación: las de la mezcla más n - 2 entre huecos.
    # Las pruebas son diferencias lineales (x_a - x_b y diferencias de huecos), así que sus
    # signos, y con ellos el camino, no cambian al escalar la entrada por c > 0 y trasladarla.
    rng = random.Random(17)
    for _ in range(300):
        n = rng.randint(2, 40)
        xs = [rng.randint(-10**6, 10**6) for _ in range(n)]
        pruebas, solo_mezcla, transformada = Pruebas(), Pruebas(), Pruebas()
        ordenar_y_recorrer(xs, pruebas)
        _ordenar_por_mezcla(list(range(n)), xs, solo_mezcla)
        assert len(pruebas.camino) == len(solo_mezcla.camino) + (n - 2)
        assert all(s in (-1, 0, 1) for s in pruebas.camino)
        ordenar_y_recorrer([3 * x - 17 for x in xs], transformada)
        assert transformada.camino == pruebas.camino
    pruebas = Pruebas()
    ordenar_y_recorrer(list(range(16, 0, -1)), pruebas)
    assert len(pruebas.camino) >= math.ceil(log3_factorial(16)) - 1


def test_huecos_decrecientes_sin_barajar():
    # Sección 5: sin barajar, se reconstruye en cada paso y se reinsertan n(n+1)/2 - 3 puntos.
    for n in [3, 10, 100, 500]:
        xs = huecos_decrecientes(n)
        delta, par, est = rejilla_1d(xs, barajar=False)
        assert delta == 1 and par == (n - 2, n - 1)
        assert est["reconstrucciones"] == n - 2
        assert est["reinserciones"] == n * (n + 1) // 2 - 3


def test_esperanza_exacta_sobre_todos_los_ordenes():
    # Teorema 9, sin azar: promediando sobre los n! órdenes de inserción, una entrada
    # con todas las distancias distintas da exactamente 2H_n - 3 reconstrucciones y
    # 2(n - 2) reinserciones.
    for n in [3, 4, 5, 6, 7]:
        xs = [2**k - 1 for k in range(n)]           # las diferencias 2^j - 2^i son todas distintas
        assert len({abs(a - b) for a, b in itertools.combinations(xs, 2)}) == n * (n - 1) // 2
        total_rec = total_rein = 0
        for orden in itertools.permutations(range(n)):
            _, _, est = rejilla_1d(xs, orden=list(orden))
            total_rec += est["reconstrucciones"]
            total_rein += est["reinserciones"]
        ordenes = math.factorial(n)
        H = sum(Fraction(1, k) for k in range(1, n + 1))
        assert Fraction(total_rec, ordenes) == 2 * H - 3
        assert Fraction(total_rein, ordenes) == 2 * (n - 2)


def test_con_empates_la_esperanza_no_sube():
    # Con pares más cercanos repetidos, reconstruir exige que el punto nuevo esté en
    # todos ellos: la probabilidad sigue siendo a lo sumo 2/m.
    for n in [4, 5, 6, 7]:
        xs = list(range(n))                          # todos los huecos iguales
        total = sum(rejilla_1d(xs, orden=list(o))[2]["reconstrucciones"]
                    for o in itertools.permutations(range(n)))
        H = sum(Fraction(1, k) for k in range(1, n + 1))
        assert Fraction(total, math.factorial(n)) <= 2 * H - 3


def test_esperanza_con_semillas():
    # La media sobre muchas semillas está a menos de 4 errores estándar de 2H_n - 3.
    for n, semillas in [(50, 1500), (500, 400)]:
        xs = random.Random(n).sample(range(10**9), n)
        rec = [rejilla_1d(xs, semilla=s)[2]["reconstrucciones"] for s in range(semillas)]
        media = sum(rec) / semillas
        error = (sum((r - media) ** 2 for r in rec) / (semillas - 1)) ** 0.5 / semillas**0.5
        assert abs(media - reconstrucciones_esperadas(n)) < 4 * error


if __name__ == "__main__":
    pruebas = [f for nombre, f in sorted(globals().items()) if nombre.startswith("test_")]
    for prueba in pruebas:
        prueba()
        print("ok", prueba.__name__)
    print(f"{len(pruebas)} pruebas pasaron")
