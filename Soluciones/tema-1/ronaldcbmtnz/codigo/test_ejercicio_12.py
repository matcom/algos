"""Casos de prueba del ejercicio 12.

Correr con `pytest test_ejercicio_12.py` o con `python test_ejercicio_12.py`.
"""

import random

from ejercicio_12 import (
    gale_shapley, gale_shapley_ingenuo, gale_shapley_sin_mirar_b, es_estable,
    es_emparejamiento, pares_bloqueantes, todos_los_estables, instancia, EJEMPLO,
)


def instancias(rng, cantidad, maximo=5):
    for _ in range(cantidad):
        yield instancia(rng.randint(1, maximo), rng.randint(1, maximo), rng.choice([0.2, 0.5, 0.8, 1.0]),
                        rng, receptores_completos=rng.random() < 0.5)


def test_estable_en_toda_estrategia():
    # Teorema 2: el resultado es un emparejamiento de pares aceptables sin pares bloqueantes.
    rng = random.Random(1)
    for pref_a, pref_b in instancias(rng, 1500, maximo=8):
        for orden, semilla in [("cola", 0), ("pila", 0), ("azar", 1), ("azar", 7)]:
            M, _ = gale_shapley(pref_a, pref_b, orden=orden, semilla=semilla)
            assert es_estable(M, pref_a, pref_b)


def test_potencial():
    # Una propuesta por vuelta, nunca repetida: a lo sumo Σ|L(a)| propuestas.
    rng = random.Random(2)
    for pref_a, pref_b in instancias(rng, 1500, maximo=10):
        traza = []
        _, propuestas = gale_shapley(pref_a, pref_b, traza=traza)
        hechas = [(a, b) for a, b, _, _ in traza]
        assert len(hechas) == len(set(hechas)) == propuestas <= sum(map(len, pref_a))
        assert all(b in pref_a[a] for a, b in hechas)


def test_al_terminar_cada_proponente_esta_emparejado_o_agoto_su_lista():
    rng = random.Random(3)
    for pref_a, pref_b in instancias(rng, 1500, maximo=8):
        traza = []
        M, _ = gale_shapley(pref_a, pref_b, traza=traza)
        propuso = {}
        for a, b, _, _ in traza:
            propuso.setdefault(a, set()).add(b)
        for a in range(len(pref_a)):
            assert M[a] is not None or propuso.get(a, set()) == set(pref_a[a])


def test_optimo_para_los_proponentes():
    # Teorema 3: cada proponente con su mejor pareja válida (o solo si no tiene ninguna).
    rng = random.Random(4)
    for pref_a, pref_b in instancias(rng, 800):
        M, _ = gale_shapley(pref_a, pref_b, orden="azar", semilla=3)
        estables = todos_los_estables(pref_a, pref_b)
        assert M in estables
        for a in range(len(pref_a)):
            validas = {E[a] for E in estables} - {None}
            if not validas:
                assert M[a] is None
            else:
                assert M[a] == min(validas, key=pref_a[a].index)


def test_hospitales_rurales():
    # Teorema 4: todos los emparejamientos estables emparejan exactamente a las mismas personas.
    rng = random.Random(5)
    for pref_a, pref_b in instancias(rng, 800):
        estables = todos_los_estables(pref_a, pref_b)
        assert estables                                      # siempre existe alguno
        a_emparejados = {frozenset(a for a, b in enumerate(E) if b is not None) for E in estables}
        b_emparejados = {frozenset(b for b in E if b is not None) for E in estables}
        assert len(a_emparejados) == len(b_emparejados) == 1


def test_ejemplo_del_informe():
    pref_a, pref_b = EJEMPLO
    M, propuestas = gale_shapley(*EJEMPLO)
    assert M == [1, 0, 2, None] and propuestas == 6
    assert todos_los_estables(pref_a, pref_b) == [M]


def test_version_ingenua_revienta():
    # Sin cambiar la condición del ciclo, quien agota su lista hace IndexError.
    try:
        gale_shapley_ingenuo([[0], [0]], [[0, 1]])
    except IndexError:
        pass
    else:
        raise AssertionError("la versión ingenua debió reventar")
    M, _ = gale_shapley([[0], [0]], [[0, 1]])
    assert M == [0, None]


def test_receptor_que_no_mira_su_lista():
    # Con receptores completos (el enunciado) el error es invisible; con listas
    # incompletas de los dos lados, empareja pares inaceptables.
    rng = random.Random(6)
    for pref_a, pref_b in instancias(rng, 1500):
        if all(len(lista) == len(pref_a) for lista in pref_b):
            assert gale_shapley_sin_mirar_b(pref_a, pref_b) == gale_shapley(pref_a, pref_b)[0]
    M = gale_shapley_sin_mirar_b([[0]], [[]])
    assert M == [0] and not es_emparejamiento(M, [[0]], [[]])


def test_pares_bloqueantes_con_solos():
    # La definición adaptada: dos solos que se aceptan mutuamente bloquean.
    assert pares_bloqueantes([None], [[0]], [[0]]) == [(0, 0)]
    assert pares_bloqueantes([None], [[0]], [[]]) == []          # b no acepta a a


if __name__ == "__main__":
    pruebas = [f for nombre, f in sorted(globals().items()) if nombre.startswith("test_")]
    for prueba in pruebas:
        prueba()
        print("ok", prueba.__name__)
    print(f"{len(pruebas)} pruebas pasaron")
