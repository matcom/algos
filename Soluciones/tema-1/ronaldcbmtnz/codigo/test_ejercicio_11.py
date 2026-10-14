"""Casos de prueba del ejercicio 11.

Correr con `pytest test_ejercicio_11.py` o con `python test_ejercicio_11.py`.
Cada prueba comprueba una afirmación concreta del informe.
"""

import math
import random

from ejercicio_11 import (
    mochila, mochila_fuerza_bruta, mochila_rapida, bits, tamano_entrada,
    tamano_unario, celdas, familia_capacidad, familia_dos_objetos,
    familia_numeros, es_primo, es_primo_miller_rabin, mayor_primo,
    divisiones_peor_caso,
)


def instancia_al_azar(rng, n_max=10, peso_max=30, valor_max=50, W_max=100):
    n = rng.randint(0, n_max)
    pesos = [rng.randint(1, peso_max) for _ in range(n)]
    valores = [rng.randint(1, valor_max) for _ in range(n)]
    return pesos, valores, rng.randint(0, W_max)


def test_programacion_dinamica_coincide_con_fuerza_bruta():
    # Teorema 1: el valor es óptimo y el conjunto reconstruido lo alcanza sin pasarse.
    rng = random.Random(11)
    for _ in range(600):
        pesos, valores, W = instancia_al_azar(rng)
        valor, elegidos, _ = mochila(pesos, valores, W)
        assert valor == mochila_fuerza_bruta(pesos, valores, W)
        assert sum(pesos[i] for i in elegidos) <= W
        assert sum(valores[i] for i in elegidos) == valor


def test_casos_borde():
    assert mochila([], [], 10)[:2] == (0, [])
    assert mochila([5], [7], 0)[:2] == (0, [])
    assert mochila([5], [7], 5)[:2] == (7, [0])
    assert mochila([5], [7], 4)[:2] == (0, [])
    # El goloso por valor/peso falla aquí; la programación dinámica no.
    assert mochila([10, 20, 30], [60, 100, 120], 50)[:2] == (220, [1, 2])


def test_celdas_exactas():
    # Proposición 2: la recurrencia se evalúa exactamente n·(W+1) veces, en toda entrada.
    rng = random.Random(12)
    for _ in range(200):
        pesos, valores, W = instancia_al_azar(rng)
        assert mochila(pesos, valores, W)[2] == celdas(len(pesos), W)


def test_version_rapida_coincide():
    rng = random.Random(13)
    for _ in range(300):
        pesos, valores, W = instancia_al_azar(rng, n_max=15, W_max=300)
        assert mochila_rapida(pesos, valores, W) == mochila(pesos, valores, W)[0]


def test_tamano_entrada():
    assert bits(0) == 1 and bits(1) == 1 and bits(7) == 3 and bits(8) == 4
    # n = 1 (1 bit), peso 1, valor 1, W = 7 (3 bits).
    assert tamano_entrada([1], [1], 7) == 6
    # n = 2 (2 bits), pesos 3 y 4 (2 + 3 bits), valores 5 y 1 (3 + 1), W = 10 (4).
    assert tamano_entrada([3, 4], [5, 1], 10) == 15


def test_familia_capacidad_es_exponencial():
    # Teorema 3: s = b + 3 y las celdas son 2^b = 2^(s-3).
    for b in range(1, 300):
        p, v, W = familia_capacidad(b)
        s = tamano_entrada(p, v, W)
        assert s == b + 3
        assert celdas(len(p), W) == 2 ** (s - 3)


def test_familia_dos_objetos_resiste_el_recorte():
    # Observación de la sección 4: con W <- min(W, suma de pesos) sigue siendo exponencial.
    for b in range(2, 300):
        p, v, W = familia_dos_objetos(b)
        s = tamano_entrada(p, v, W)
        assert s == 3 * b + 5
        recortado = min(W, sum(p))
        assert recortado == W
        assert celdas(len(p), recortado) >= 2 ** ((s - 5) // 3 + 1)


def test_recorte_no_cambia_la_respuesta():
    rng = random.Random(14)
    for _ in range(300):
        pesos, valores, W = instancia_al_azar(rng, W_max=400)
        assert mochila(pesos, valores, min(W, sum(pesos)))[0] == mochila(pesos, valores, W)[0]


def test_cotas_superiores():
    # Teorema 3, cota superior: celdas <= s·2^s. Proposición 4: en unario, celdas <= s_u².
    rng = random.Random(15)
    for _ in range(500):
        pesos, valores, W = instancia_al_azar(rng, n_max=20, peso_max=10**6, W_max=10**6)
        c = celdas(len(pesos), W)
        assert c <= tamano_entrada(pesos, valores, W) * 2 ** tamano_entrada(pesos, valores, W)
        assert c <= tamano_unario(pesos, valores, W) ** 2


def test_polinomial_con_numeros_acotados():
    # Con pesos de 4 bits, W <= 15n y las celdas son O(s²).
    for n in range(1, 400):
        p, v, W = familia_numeros(n, 4)
        assert celdas(n, W) <= tamano_entrada(p, v, W) ** 2


def test_reparto_del_mismo_tamano():
    # Tabla 3: con s ≈ 512 fijo, cuantos más objetos y menos bits por número, más barato.
    anterior = math.inf
    for n in [1, 2, 4, 8, 16, 32]:
        b = 1
        while tamano_entrada(*familia_numeros(n, b + 1)) <= 512:
            b += 1
        p, v, W = familia_numeros(n, b)
        c = celdas(n, W)
        assert c < anterior
        anterior = c


def test_un_bit_mas():
    # Un bit más en W duplica las celdas; dos bits más en N duplican las divisiones.
    for b in range(1, 100):
        assert celdas(1, familia_capacidad(b + 1)[2]) == 2 * celdas(1, familia_capacidad(b)[2])
    for b in range(16, 60, 2):
        razon = divisiones_peor_caso(b + 2) / divisiones_peor_caso(b)
        assert 1.99 < razon < 2.01


def test_es_primo_reproduce_la_conferencia_1():
    # C1, §1: 8, 99, 999 y 31 621 divisiones.
    for n, divisiones in [(97, 8), (10_007, 99), (1_000_003, 999), (1_000_000_007, 31_621)]:
        assert es_primo(n) == (True, divisiones)


def test_miller_rabin_coincide_con_la_division():
    for n in range(0, 30_000):
        assert es_primo_miller_rabin(n) == es_primo(n)[0]
    # Pseudoprimos fuertes y números de Carmichael: compuestos. El último engaña
    # a los 12 primeros primos como bases; la base 41 lo atrapa.
    for n in [2047, 3277, 4033, 561, 1105, 1729, 3215031751, 2152302898747,
              318665857834031151167461]:
        assert not es_primo_miller_rabin(n)
    assert 2**81 < 3317044064679887385961981


def test_peor_caso_de_la_primalidad():
    # El mayor primo de b bits hace ⌊√p⌋ - 1 divisiones, y no hay primos entre él y 2^b.
    for b in range(4, 25):
        p = mayor_primo(b)
        assert es_primo(p) == (True, divisiones_peor_caso(b))
        assert p.bit_length() == b
        assert not any(es_primo(q)[0] for q in range(p + 1, 2**b))


if __name__ == "__main__":
    pruebas = [f for nombre, f in sorted(globals().items()) if nombre.startswith("test_")]
    for prueba in pruebas:
        prueba()
        print("ok", prueba.__name__)
    print(f"{len(pruebas)} pruebas pasaron")
