"""Casos de prueba del ejercicio 5.

Correr con `pytest test_ejercicio_05.py` o con `python test_ejercicio_05.py`.
"""

import itertools
import random

from ejercicio_05 import (
    Lista, floyd, floyd_completo, con_conjunto, forma, encuentro_teorico,
    construir, potencial,
)


def test_exhaustivo_hasta_5_nodos():
    # Todas las funciones sig: {0..n-1} -> {None, 0..n-1} y todo nodo inicial.
    for n in range(1, 6):
        for sig in itertools.product([None] + list(range(n)), repeat=n):
            for inicio in range(n):
                verdad = forma(sig, inicio)
                hay, vueltas = floyd(Lista(sig), inicio)
                if verdad[0] == "sin ciclo":
                    assert not hay and vueltas == verdad[1] // 2
                    assert floyd_completo(Lista(sig), inicio) is None
                else:
                    mu, lam = verdad
                    assert hay and vueltas == encuentro_teorico(mu, lam)
                    assert floyd_completo(Lista(sig), inicio) == (mu, lam)


def test_lista_vacia():
    assert floyd(Lista([]), None) == (False, 0)
    assert floyd_completo(Lista([]), None) is None


def test_listas_grandes_con_nombres_al_azar():
    rng = random.Random(1)
    for _ in range(300):
        mu, lam = rng.randint(0, 3000), rng.randint(0, 3000)
        sig, inicio = construir(mu, lam, rng, sobrantes=rng.randint(0, 50))
        hay, vueltas = floyd(Lista(sig), inicio)
        if lam == 0:
            assert not hay and vueltas == mu // 2
        else:
            assert hay and vueltas == encuentro_teorico(mu, lam)
            assert floyd_completo(Lista(sig), inicio) == (mu, lam)


def test_invariante_tortuga_xt_liebre_x2t():
    # Después de t vueltas, tortuga = x_t y liebre = x_2t; antes de t*, nunca iguales.
    rng = random.Random(2)
    for _ in range(300):
        mu, lam = rng.randint(0, 60), rng.randint(1, 60)
        sig, inicio = construir(mu, lam, rng)
        x = [inicio]
        for _ in range(4 * (mu + lam) + 4):
            x.append(sig[x[-1]])
        traza = []
        floyd(Lista(sig), inicio, traza)
        for t, (tortuga, liebre) in enumerate(traza, 1):
            assert tortuga == x[t] and liebre == x[2 * t]
            assert (tortuga == liebre) == (t == len(traza))


def test_potencial_baja():
    # Φ_t baja en cada vuelta: de a 1 en la cola y en el ciclo, al menos 1 al entrar.
    for mu in range(0, 40):
        for lam in range(1, 40):
            t_star = encuentro_teorico(mu, lam)
            valores = [potencial(mu, lam, t) for t in range(t_star)]
            assert all(a > b for a, b in zip(valores, valores[1:]))
            assert all(v >= 1 for v in valores)
            assert valores[0] <= mu + lam
            assert t_star <= mu + lam


def test_evaluaciones():
    # Floyd sigue a lo sumo 3(μ+λ) punteros; el conjunto, exactamente μ+λ pero con memoria μ+λ.
    rng = random.Random(3)
    for _ in range(300):
        mu, lam = rng.randint(0, 500), rng.randint(1, 500)
        sig, inicio = construir(mu, lam, rng)
        lista = Lista(sig)
        floyd(lista, inicio)
        assert lista.evaluaciones <= 3 * (mu + lam)
        lista = Lista(sig)
        (m, l), memoria = con_conjunto(lista, inicio)
        assert (m, l) == (mu, lam) and lista.evaluaciones == memoria == mu + lam


def test_sin_ciclo_evaluaciones():
    # Sin ciclo y con n nodos, Floyd sigue a lo sumo 3⌊n/2⌋ + 2 punteros.
    for n in range(0, 300):
        sig, inicio = construir(n, 0)
        lista = Lista(sig)
        hay, vueltas = floyd(lista, inicio)
        assert not hay and vueltas == n // 2
        assert lista.evaluaciones <= 3 * (n // 2) + 2


if __name__ == "__main__":
    pruebas = [f for nombre, f in sorted(globals().items()) if nombre.startswith("test_")]
    for prueba in pruebas:
        prueba()
        print("ok", prueba.__name__)
    print(f"{len(pruebas)} pruebas pasaron")
