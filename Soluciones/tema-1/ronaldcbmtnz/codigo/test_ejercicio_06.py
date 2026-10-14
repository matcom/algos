"""Casos de prueba del ejercicio 6.

Correr con `pytest test_ejercicio_06.py` o con `python test_ejercicio_06.py`.
"""

import random

from ejercicio_06 import (
    escalera, busqueda_por_filas, esta_ordenada, matriz_al_azar, escalera_del_adversario,
    matriz_del_adversario, optimo_exacto,
)


def presente(M, x):
    return any(x in fila for fila in M)


def test_correcta_contra_fuerza_bruta():
    rng = random.Random(1)
    for _ in range(3000):
        n = rng.randint(1, 12)
        M = matriz_al_azar(n, rng, salto=rng.choice([1, 2, 5]))
        x = rng.choice([rng.choice(rng.choice(M)), rng.randint(-2, M[-1][-1] + 2)])
        esta, pos = escalera(M, x)
        assert esta == presente(M, x)
        if esta:
            assert M[pos[0]][pos[1]] == x
        assert busqueda_por_filas(M, x)[0] == esta


def test_no_decreciente_tambien():
    # Con repetidos (filas y columnas solo no decrecientes) el invariante sigue valiendo.
    rng = random.Random(2)
    for _ in range(2000):
        n = rng.randint(1, 8)
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                M[i][j] = max(M[i - 1][j] if i else 0, M[i][j - 1] if j else 0) + rng.randint(0, 2)
        x = rng.randint(-1, M[-1][-1] + 1)
        assert escalera(M, x)[0] == presente(M, x)


def test_invariante_vigilado():
    rng = random.Random(3)
    for _ in range(500):
        n = rng.randint(1, 9)
        M = matriz_al_azar(n, rng)
        escalera(M, rng.randint(0, M[-1][-1] + 1), vigilar=True)


def test_a_lo_sumo_2n_menos_1():
    # Potencial (n - i) + (j + 1): baja 1 por comparación.
    rng = random.Random(4)
    for _ in range(2000):
        n = rng.randint(1, 20)
        M = matriz_al_azar(n, rng)
        camino = []
        escalera(M, rng.randint(0, M[-1][-1] + 1), camino)
        assert len(camino) <= 2 * n - 1


def test_matriz_del_adversario():
    # La matriz está ordenada, no tiene a x, y la escalera mira exactamente las 2n - 1 celdas.
    for n in range(1, 40):
        M, x = matriz_del_adversario(n)
        assert esta_ordenada(M) and not presente(M, x)
        camino = []
        assert escalera(M, x, camino) == (False, None)
        assert camino == escalera_del_adversario(n)
        assert len(camino) == 2 * n - 1


def test_cada_celda_de_la_escalera_puede_ser_x():
    # El corazón del adversario: poner x en cualquier celda de la escalera deja la
    # matriz ordenada, y solo cambia la respuesta de esa celda.
    for n in range(1, 25):
        M, x = matriz_del_adversario(n)
        for c in escalera_del_adversario(n):
            M2, _ = matriz_del_adversario(n, poner=c)
            assert esta_ordenada(M2) and presente(M2, x)
            distintas = [(i, j) for i in range(n) for j in range(n) if M[i][j] != M2[i][j]]
            assert distintas == [c]


def test_un_algoritmo_que_se_salta_una_celda_falla():
    # Cualquier recorrido que omita una celda de la escalera no distingue M de M2.
    n = 6
    M, x = matriz_del_adversario(n)
    for omitida in escalera_del_adversario(n):
        M2, _ = matriz_del_adversario(n, poner=omitida)
        miradas = [c for c in escalera_del_adversario(n) if c != omitida]
        assert all(M[i][j] == M2[i][j] for i, j in miradas)
        assert presente(M2, x) != presente(M, x)


def test_optimo_exacto_por_fuerza_bruta():
    for n in [1, 2, 3]:
        assert optimo_exacto(n)[0] == 2 * n - 1


if __name__ == "__main__":
    pruebas = [f for nombre, f in sorted(globals().items()) if nombre.startswith("test_")]
    for prueba in pruebas:
        prueba()
        print("ok", prueba.__name__)
    print(f"{len(pruebas)} pruebas pasaron")
