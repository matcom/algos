"""Ejercicio 12 ★★★ — Gale-Shapley con listas incompletas (C3)

Código de validación de ejercicio-12.md.
Ejecutar con: python ejercicio-12.py
"""


# -------------------- Parte 1 --------------------

from collections import deque
import random

def gale_shapley_incompleto(pref_a, pref_b, orden="cola", semilla=0):
    """pref_a[a], pref_b[b]: listas (posiblemente incompletas) en orden de preferencia.
    Devuelve (M, propuestas) con M[a] = receptor o None."""
    rango = [{a: lugar for lugar, a in enumerate(lista)} for lista in pref_b]
    siguiente = [0] * len(pref_a)
    pareja_de_b = [None] * len(pref_b)
    libres = deque(a for a in range(len(pref_a)) if pref_a[a])
    azar = random.Random(semilla)
    propuestas = 0

    def liberar(a):                      # vuelve a la cola solo si le queda alguien a quien proponer
        if siguiente[a] < len(pref_a[a]):
            libres.append(a)

    while libres:
        if orden == "azar":
            libres.rotate(azar.randrange(len(libres)))
        a = libres.popleft() if orden != "pila" else libres.pop()
        b = pref_a[a][siguiente[a]]
        siguiente[a] += 1
        propuestas += 1
        actual = pareja_de_b[b]
        if a not in rango[b]:            # b no lista a: rechazo
            liberar(a)
        elif actual is None:
            pareja_de_b[b] = a
        elif rango[b][a] < rango[b][actual]:
            pareja_de_b[b] = a
            liberar(actual)
        else:
            liberar(a)
    M = [None] * len(pref_a)
    for b, a in enumerate(pareja_de_b):
        if a is not None:
            M[a] = b
    return M, propuestas

# -------------------- Parte 2 --------------------

def aceptables(a, b, pref_a, pref_b):
    return b in pref_a[a] and a in pref_b[b]

def prefiere(lista, nuevo, actual):
    """¿Prefiere 'nuevo' a 'actual'? actual = None significa estar solo."""
    return actual is None or lista.index(nuevo) < lista.index(actual)

def pares_bloqueantes(M, pref_a, pref_b):
    pareja_de_b = {b: a for a, b in enumerate(M) if b is not None}
    return [(a, b) for a in range(len(pref_a)) for b in range(len(pref_b))
            if M[a] != b and aceptables(a, b, pref_a, pref_b)
            and prefiere(pref_a[a], b, M[a]) and prefiere(pref_b[b], a, pareja_de_b.get(b))]

def todos_los_emparejamientos(pref_a, pref_b):
    na = len(pref_a)
    def rec(a, usados):
        if a == na:
            yield []
            return
        for resto in rec(a + 1, usados):
            yield [None] + resto
        for b in pref_a[a]:
            if b not in usados and a in pref_b[b]:
                for resto in rec(a + 1, usados | {b}):
                    yield [b] + resto
    yield from rec(0, frozenset())

def estables(pref_a, pref_b):
    return [M for M in todos_los_emparejamientos(pref_a, pref_b) if not pares_bloqueantes(M, pref_a, pref_b)]

# -------------------- Parte 3 --------------------

pref_a = [[0, 1], [0], [0]]          # a0: b0 > b1;  a1: solo b0;  a2: solo b0
pref_b = [[1, 0, 2], [0]]            # b0: a1 > a0 > a2;  b1: solo a0
M, k = gale_shapley_incompleto(pref_a, pref_b)
print("resultado:", {f"a{a}": (f"b{b}" if b is not None else "solo") for a, b in enumerate(M)},
      f"en {k} propuestas")
print("pares bloqueantes:", pares_bloqueantes(M, pref_a, pref_b))
print("estables posibles:", estables(pref_a, pref_b))

# -------------------- Parte 4 --------------------

def instancia(na, nb, rng):
    pref_a = [rng.sample(range(nb), rng.randint(0, nb)) for _ in range(na)]
    pref_b = [rng.sample(range(na), rng.randint(0, na)) for _ in range(nb)]
    return pref_a, pref_b

def rango_para(a, b, pref_a):
    return len(pref_a[a]) if b is None else pref_a[a].index(b)    # estar solo es lo peor

rng = random.Random(12)
casos = 0
for _ in range(1500):
    na, nb = rng.randint(1, 5), rng.randint(1, 5)
    pref_a, pref_b = instancia(na, nb, rng)
    resultados = [gale_shapley_incompleto(pref_a, pref_b, orden=o, semilla=s)
                  for o, s in [("cola", 0), ("pila", 0), ("azar", 1), ("azar", 2)]]
    M, k = resultados[0]
    assert all(R == M for R, _ in resultados)                       # no depende del orden
    assert not pares_bloqueantes(M, pref_a, pref_b)                  # estable
    assert all(b is None or aceptables(a, b, pref_a, pref_b) for a, b in enumerate(M))
    assert k <= sum(len(l) for l in pref_a)                          # potencial
    E = estables(pref_a, pref_b)
    assert M in E
    for a in range(na):                                              # óptimo para proponentes
        assert rango_para(a, M[a], pref_a) == min(rango_para(a, X[a], pref_a) for X in E)
    emparejados = {frozenset(a for a, b in enumerate(X) if b is not None) for X in E}
    assert len(emparejados) == 1
    casos += 1
print(f"{casos} instancias: estable, independiente del orden, óptimo para proponentes, "
      f"<= L propuestas, y mismos emparejados en todos los estables")
