"""Casos de prueba del ejercicio 2.

Correr con `pytest test_ejercicio_02.py` o con `python test_ejercicio_02.py`.
"""

import random

from ejercicio_02 import (
    busqueda_binaria, potenciales, bits, cota_informacion, peor_caso,
    caminos_de_los_huecos, falla, SinTerminar,
)


def arreglos(rng, cantidad):
    for _ in range(cantidad):
        n = rng.randint(0, 40)
        if rng.random() < 0.5:
            A = sorted(rng.sample(range(200), n))
        else:
            A = sorted(rng.randrange(8) for _ in range(n))      # con repetidos
        yield A, rng.randrange(-3, 205)


def test_postcondicion():
    # "está" con A[m] == x, o "hueco" con A[lo-1] < x < A[lo] y x ausente.
    rng = random.Random(1)
    for A, x in arreglos(rng, 5000):
        tipo, k = busqueda_binaria(A, x)
        if tipo == "está":
            assert A[k] == x
        else:
            assert x not in A
            assert (k == 0 or A[k - 1] < x) and (k == len(A) or A[k] > x)


def test_invariante_vigilado():
    # El invariante se comprueba al empezar cada vuelta; un fallo levanta AssertionError.
    rng = random.Random(2)
    for A, x in arreglos(rng, 2000):
        busqueda_binaria(A, x, vigilar=True)


def test_potencial_baja_y_se_parte_a_la_mitad():
    # Φ = hi - lo baja en cada vuelta, a lo sumo a ⌊Φ/2⌋; Ψ = bits(Φ) baja al menos 1.
    rng = random.Random(3)
    for A, x in arreglos(rng, 3000):
        fi, psi = potenciales(A, x)
        for antes, despues in zip(fi, fi[1:]):
            assert despues <= antes // 2
        for antes, despues in zip(psi, psi[1:]):
            assert despues <= antes - 1
        assert len(fi) <= bits(len(A))


def test_peor_caso_igual_a_la_cota():
    # Teorema: el peor caso es exactamente ⌈log2(n+1)⌉ para todo n.
    for n in range(1, 600):
        assert peor_caso(n) == cota_informacion(n)
    assert cota_informacion(7) == 3 and cota_informacion(8) == 4


def test_huecos_a_hojas_distintas():
    # Lema 4 de la C5: los n + 1 huecos van a hojas distintas, y por caminos sin '='.
    for n in range(0, 200):
        caminos = caminos_de_los_huecos(n)
        assert len(caminos) == n + 1 == len(set(caminos))
        assert all(0 not in c for c in caminos)


def test_lo_igual_m_no_termina():
    # El potencial no baja con hi - lo = 1 y A[lo] < x: el ejemplo mínimo.
    try:
        busqueda_binaria([1], 2, variante="lo = m", limite=100)
    except SinTerminar:
        pass
    else:
        raise AssertionError("la variante lo = m debió quedarse en un ciclo")


def test_lo_igual_m_termina_si_x_esta():
    # Por eso las pruebas con x presente no lo atrapan nunca.
    rng = random.Random(4)
    for _ in range(3000):
        A = sorted(rng.sample(range(500), rng.randint(1, 40)))
        x = rng.choice(A)
        assert busqueda_binaria(A, x, variante="lo = m", limite=200) == busqueda_binaria(A, x)


def test_hi_igual_m_menos_1_pierde_a_x():
    # El ejemplo mínimo: x está justo a la izquierda del primer m.
    assert busqueda_binaria([1, 2], 1, variante="hi = m - 1") == ("hueco", 0)
    assert falla([1, 2], 1, "hi = m - 1", mirar_hueco=False)


def test_hi_igual_m_menos_1_no_se_equivoca_en_esta_si_x_falta():
    # Si x no está, igual dice "no está": solo el hueco puede salir mal.
    rng = random.Random(5)
    for _ in range(3000):
        A = sorted(rng.sample(range(0, 1000, 2), rng.randint(1, 40)))
        x = rng.randrange(1, 1000, 2)
        assert not falla(A, x, "hi = m - 1", mirar_hueco=False)


if __name__ == "__main__":
    pruebas = [f for nombre, f in sorted(globals().items()) if nombre.startswith("test_")]
    for prueba in pruebas:
        prueba()
        print("ok", prueba.__name__)
    print(f"{len(pruebas)} pruebas pasaron")
