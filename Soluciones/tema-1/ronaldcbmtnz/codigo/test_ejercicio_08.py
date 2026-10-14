"""Casos de prueba del ejercicio 8.

Correr con `pytest test_ejercicio_08.py` o con `python test_ejercicio_08.py`.
"""

import itertools
import random
from collections import Counter

from ejercicio_08 import (
    primera_pasada, se_parte_en_ternas, mas_de_un_tercio, sin_verificar, oraculo,
    GENERADORES, contraejemplo,
)


def test_dos_pasadas_exhaustivo():
    # Todas las palabras de largo <= 8 sobre 4 símbolos.
    for largo in range(0, 9):
        for A in itertools.product("ABCD", repeat=largo):
            A = list(A)
            assert mas_de_un_tercio(A) == oraculo(A)


def test_dos_pasadas_al_azar():
    rng = random.Random(1)
    for _ in range(3000):
        A = [rng.randrange(rng.randint(1, 8)) for _ in range(rng.randint(0, 60))]
        assert mas_de_un_tercio(A) == oraculo(A)


def test_invariante_vigilado():
    # La partición en ternas de distintos + copias de los candidatos, en cada prefijo.
    rng = random.Random(2)
    for _ in range(1500):
        A = [rng.choice("ABCDE"[:rng.randint(1, 5)]) for _ in range(rng.randint(0, 25))]
        primera_pasada(A, vigilar=True)


def test_lema_de_las_ternas():
    # Lema 1, contra una búsqueda exhaustiva de particiones en multiconjuntos chicos.
    def particion_exhaustiva(lista):
        if not lista:
            return True
        x = lista[0]
        for i, j in itertools.combinations(range(1, len(lista)), 2):
            if len({x, lista[i], lista[j]}) == 3:
                resto = [v for k, v in enumerate(lista) if k not in (0, i, j)]
                if particion_exhaustiva(resto):
                    return True
        return False

    for largo in range(0, 10):
        for A in itertools.combinations_with_replacement("ABCD", largo):
            assert se_parte_en_ternas(Counter(A)) == (largo % 3 == 0 and particion_exhaustiva(list(A)))


def test_tres_simbolos_contadores_f_menos_fmin():
    # Lema 4: con tres símbolos, los contadores finales son f - f_min.
    for largo in range(0, 10):
        for A in itertools.product("ABC", repeat=largo):
            f = Counter({s: 0 for s in "ABC"})
            f.update(A)
            fmin = min(f.values())
            finales = {c: k for c, k in primera_pasada(list(A)) if k > 0}
            assert finales == {s: f[s] - fmin for s in "ABC" if f[s] > fmin}


def test_sin_verificar_nunca_pierde_un_pesado():
    # Mitad buena del atajo: todo elemento con más de n/3 apariciones está en la salida.
    rng = random.Random(3)
    for _ in range(3000):
        A = [rng.choice("ABCDE") for _ in range(rng.randint(0, 40))]
        assert set(oraculo(A)) <= set(sin_verificar(A))


def test_dos_pesados_no_atrapan_al_atajo():
    # Teorema 3: con dos elementos de más de n/3 apariciones, la versión sin verificar acierta.
    rng = random.Random(4)
    generar = GENERADORES["dos pesados plantados"]
    for _ in range(5000):
        A = generar(rng, rng.randint(1, 60))
        assert len(oraculo(A)) == 2
        assert sin_verificar(A) == oraculo(A)


def test_todos_distintos_con_n_multiplo_de_3():
    # Otro generador ciego: cada tres elementos distintos el estado vuelve a vacío.
    for n in range(3, 60, 3):
        A = list(range(n))
        assert sin_verificar(A) == oraculo(A) == []
    assert sin_verificar(list(range(4))) != oraculo(list(range(4)))


def test_contraejemplos_minimos():
    assert contraejemplo(sin_verificar, "AB") == "AAB"
    assert contraejemplo(lambda A: mas_de_un_tercio(A, orden_malo=True), "AB") == "AAB"
    # Con el orden malo, AAB deja dos copias de A como candidatos y una terna las cancela.
    assert primera_pasada(list("AA"), orden_malo=True) == [("A", 1), ("A", 1)]


if __name__ == "__main__":
    pruebas = [f for nombre, f in sorted(globals().items()) if nombre.startswith("test_")]
    for prueba in pruebas:
        prueba()
        print("ok", prueba.__name__)
    print(f"{len(pruebas)} pruebas pasaron")
