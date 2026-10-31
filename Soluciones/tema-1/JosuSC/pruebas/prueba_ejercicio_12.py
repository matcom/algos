#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejercicio 12 - Casos de prueba
Gale-Shapley con listas incompletas (aceptabilidad y solteros).

Qué se comprueba:
  1. Sobre instancias aleatorias con listas incompletas, con TRES órdenes
     de ejecución (cola, pila, azar):
       - cero parejas bloqueantes (estabilidad, con solteros incluidos);
       - todo par emparejado es factible (b en L_a y a en L_b);
       - el emparejamiento es EL MISMO en los tres órdenes (los proponentes
         consiguen su mejor pareja válida, no depende del orden);
       - las propuestas no pasan de sum |L_a| (el potencial de la sección 3).
  2. Casos borde construidos a mano: listas vacías, aceptabilidad unilateral.
  3. La trampa de la sección 8: la variante en la que el receptor acepta a
     un proponente que no lista devuelve pares NO factibles. Se encuentra
     en cuanto se busca un poco.

Ejecutar:  python3 prueba_ejercicio_12.py
Solo usa la biblioteca estándar.
"""

import random
from collections import deque


def gale_shapley_incompleto(pref_a, pref_b, orden="cola", rng=None):
    """pref_a[a]: lista L_a de receptores aceptables en orden de preferencia.
    pref_b[b]: lista L_b de proponentes aceptables en orden de preferencia."""
    rng = rng or random
    n = len(pref_a)
    rango = {b: {a: lugar for lugar, a in enumerate(pref_b[b])} for b in range(n)}
    siguiente = [0] * n
    pareja_de_b = [None] * n
    libres = deque(a for a in range(n) if pref_a[a])     # solo quien tiene lista
    propuestas = 0
    while libres:
        if orden == "cola":
            a = libres.popleft()
        elif orden == "pila":
            a = libres.pop()
        else:                                            # azar
            i = rng.randrange(len(libres))
            a = libres[i]
            del libres[i]
        if siguiente[a] == len(pref_a[a]):
            continue                    # agotó su lista: soltero definitivo
        b = pref_a[a][siguiente[a]]
        siguiente[a] += 1
        propuestas += 1
        if a not in rango[b]:
            libres.append(a)            # b no lista a a: rechazo directo
            continue
        actual = pareja_de_b[b]
        if actual is None or rango[b][a] < rango[b][actual]:
            pareja_de_b[b] = a
            if actual is not None:
                libres.append(actual)
        else:
            libres.append(a)
    M = {a: b for b, a in enumerate(pareja_de_b) if a is not None}
    return M, propuestas


def gale_shapley_sin_factibilidad(pref_a, pref_b):
    """La trampa de la sección 8: el receptor acepta a un NO aceptable si está libre."""
    n = len(pref_a)
    rango = {b: {a: lugar for lugar, a in enumerate(pref_b[b])} for b in range(n)}
    siguiente = [0] * n
    pareja_de_b = [None] * n
    libres = deque(a for a in range(n) if pref_a[a])
    while libres:
        a = libres.popleft()
        if siguiente[a] == len(pref_a[a]):
            continue
        b = pref_a[a][siguiente[a]]
        siguiente[a] += 1
        actual = pareja_de_b[b]
        if a not in rango[b]:
            if actual is None:
                pareja_de_b[b] = a      # <-- el error: lo acepta igual
            else:
                libres.append(a)
            continue
        # si b quedó con un inaceptable, cualquier listado lo desplaza
        if actual is None or actual not in rango[b] or rango[b][a] < rango[b][actual]:
            pareja_de_b[b] = a
            if actual is not None:
                libres.append(actual)
        else:
            libres.append(a)
    return {a: b for b, a in enumerate(pareja_de_b) if a is not None}


def pares_bloqueantes_incompleto(M, pref_a, pref_b):
    """El verificador de estabilidad: mira todos los pares factibles, con solteros."""
    pareja_de_b = {b: a for a, b in M.items()}
    bloqueantes = []
    for a in range(len(pref_a)):
        for b in pref_a[a]:                        # solo receptores que a lista
            if a not in pref_b[b]:
                continue                           # (a, b) no es factible
            if M.get(a) == b:
                continue
            if M.get(a) is not None and pref_a[a].index(M[a]) < pref_a[a].index(b):
                continue
            if b in pareja_de_b and pref_b[b].index(pareja_de_b[b]) < pref_b[b].index(a):
                continue
            bloqueantes.append((a, b))
    return bloqueantes


def instancia_aleatoria(n, p, rng):
    pref_a, pref_b = [], []
    for _ in range(n):
        orden = list(range(n))
        rng.shuffle(orden)
        pref_a.append([b for b in orden if rng.random() < p])
    for _ in range(n):
        orden = list(range(n))
        rng.shuffle(orden)
        pref_b.append([a for a in orden if rng.random() < p])
    return pref_a, pref_b


def main():
    rng = random.Random(2026)

    # ------------------------------------------------------------------
    # 1) Aleatorio: tres órdenes de ejecución, mismo resultado, estable
    # ------------------------------------------------------------------
    instancias = 150
    total_propuestas = 0
    for _ in range(instancias):
        n = rng.randint(5, 10)
        p = rng.choice([0.4, 0.6, 0.8])
        pref_a, pref_b = instancia_aleatoria(n, p, rng)
        techo = sum(len(L) for L in pref_a)

        resultados = []
        for orden in ("cola", "pila", "azar"):
            M, prop = gale_shapley_incompleto(pref_a, pref_b, orden,
                                              rng=random.Random(7) if orden == "azar" else None)
            assert prop <= techo, (orden, prop, techo)          # el potencial
            assert pares_bloqueantes_incompleto(M, pref_a, pref_b) == []
            for a, b in M.items():                              # factibilidad
                assert b in pref_a[a] and a in pref_b[b], (a, b)
            resultados.append(M)
            total_propuestas += prop
        assert resultados[0] == resultados[1] == resultados[2]  # mejor(a) único

    # ------------------------------------------------------------------
    # 2) Casos borde construidos a mano
    # ------------------------------------------------------------------
    # listas vacías: todos solteros
    M, prop = gale_shapley_incompleto([[], []], [[], []])
    assert M == {} and prop == 0
    # aceptabilidad unilateral: a0 lista a b0 pero b0 no
    M, prop = gale_shapley_incompleto([[0], []], [[], []])
    assert M == {} and prop == 1
    # un solo par mutuo
    M, prop = gale_shapley_incompleto([[0]], [[0]])
    assert M == {0: 0} and prop == 1
    # competencia: dos proponentes por un receptor que prefiere a a0
    M, prop = gale_shapley_incompleto([[0], [0]], [[0, 1], []])
    assert M == {0: 0} and prop == 2          # a1 rechazado, queda soltero
    # soltero por agotamiento: b0 solo lista a a1, y a0 solo lista a b0
    M, prop = gale_shapley_incompleto([[0], [0]], [[1], []])
    assert M == {1: 0} and prop == 2          # a0 no es aceptable para b0

    # ------------------------------------------------------------------
    # 3) La trampa: aceptar al inaceptable rompe la factibilidad
    # ------------------------------------------------------------------
    rng2 = random.Random(5)
    hallado = None
    for _ in range(200):
        n = rng2.randint(5, 8)
        pref_a, pref_b = instancia_aleatoria(n, 0.5, rng2)
        M_mala = gale_shapley_sin_factibilidad(pref_a, pref_b)
        malos = [(a, b) for a, b in M_mala.items()
                 if not (b in pref_a[a] and a in pref_b[b])]
        if malos:
            hallado = (pref_a, pref_b, M_mala, malos)
            break
    assert hallado is not None, "la trampa debería aparecer rápido"
    pref_a, pref_b, M_mala, malos = hallado
    # y el algoritmo correcto sobre la misma instancia no tiene ese problema
    M_buena, _ = gale_shapley_incompleto(pref_a, pref_b)
    assert all(b in pref_a[a] and a in pref_b[b] for a, b in M_buena.items())
    assert pares_bloqueantes_incompleto(M_buena, pref_a, pref_b) == []

    print("ejercicio 12: todo correcto")
    print(f"  {instancias} instancias aleatorias x 3 órdenes: estables, factibles,")
    print("  y el MISMO emparejamiento en los tres órdenes (mejor(a) no depende del orden)")
    print(f"  propuestas <= sum |L_a| siempre (potencial); promedio {total_propuestas / (3 * instancias):.1f}")
    print("  casos borde: listas vacías, unilateral, competencia, soltero por agotamiento")
    print(f"  la trampa (aceptar inaceptables) aparece sola: pares no factibles {malos}")


if __name__ == "__main__":
    main()
