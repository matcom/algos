"""Ejercicio 12: Gale-Shapley con listas incompletas.

Corre: python ejercicio-12.py  (prueba el algoritmo adaptado contra fuerza bruta, con tres
órdenes de ejecución, vigila el potencial, y muestra qué pasa con el algoritmo original y
con la definición vieja de pareja bloqueante)
"""
import itertools
import random
from collections import deque


def gale_shapley(pref_a, pref_b, orden="cola", semilla=0, traza=None, vigilar=False):
    """pref_a[a]: los receptores que a acepta, del mejor al peor (puede ser incompleta).
    pref_b[b]: los proponentes que b acepta, del mejor al peor.
    Devuelve (M, propuestas) con M[a] = pareja de a, o None si se queda solo."""
    rango = [{a: lugar for lugar, a in enumerate(lista)} for lista in pref_b]
    siguiente = [0] * len(pref_a)
    pareja_de_b = [None] * len(pref_b)
    libres = deque(a for a in range(len(pref_a)) if pref_a[a])
    azar = random.Random(semilla)
    propuestas = 0
    phi = sum(len(lista) for lista in pref_a)          # propuestas que quedan por hacer

    while libres:
        if orden == "azar":
            libres.rotate(azar.randrange(len(libres)))
        a = libres.popleft() if orden == "cola" else libres.pop()
        b = pref_a[a][siguiente[a]]
        siguiente[a] += 1
        propuestas += 1
        actual = pareja_de_b[b]
        if a not in rango[b]:                          # b no acepta a a: lo rechaza
            rechazado = a
        elif actual is None or rango[b][a] < rango[b][actual]:
            pareja_de_b[b], rechazado = a, actual
        else:
            rechazado = a
        if rechazado is not None and siguiente[rechazado] < len(pref_a[rechazado]):
            libres.append(rechazado)                   # le quedan receptores en su lista
        # si no le quedan, se queda solo: prefiere eso a uno que no listó
        if traza is not None:
            traza.append((a, b, actual, pareja_de_b[b]))
        if vigilar:
            nuevo = sum(len(l) for l in pref_a) - sum(siguiente)
            assert nuevo == phi - 1 and nuevo >= 0     # Φ baja exactamente 1 por propuesta
            phi = nuevo

    M = [None] * len(pref_a)
    for b, a in enumerate(pareja_de_b):
        if a is not None:
            M[a] = b
    return M, propuestas


def prefiere(lista, x, y):
    """¿Prefiere x a y quien tiene esta lista? Estar solo (None) va después de todos los
    de la lista, y antes de cualquiera que no está en la lista."""
    rx = lista.index(x) if x in lista else (len(lista) if x is None else len(lista) + 1)
    ry = lista.index(y) if y in lista else (len(lista) if y is None else len(lista) + 1)
    return rx < ry


def bloqueantes(M, pref_a, pref_b):
    """Definición nueva: (a, b) bloquea si se aceptan mutuamente, no están juntos, y cada
    uno está solo o prefiere al otro a su pareja actual."""
    M_b = {b: a for a, b in enumerate(M) if b is not None}
    return [(a, b) for a in range(len(pref_a)) for b in pref_a[a]
            if a in pref_b[b] and M[a] != b
            and prefiere(pref_a[a], b, M[a]) and prefiere(pref_b[b], a, M_b.get(b))]


def bloqueantes_vieja(M, pref_a, pref_b):
    """Definición de la conferencia 3, aplicada sin pensar: solo mira a los que tienen pareja."""
    M_b = {b: a for a, b in enumerate(M) if b is not None}
    return [(a, b) for a in range(len(pref_a)) for b in pref_a[a]
            if M[a] is not None and b in M_b and M[a] != b
            and prefiere(pref_a[a], b, M[a]) and prefiere(pref_b[b], a, M_b[b])]


def aceptable(M, pref_a, pref_b):
    """Nadie quedó con alguien que no listó."""
    return all(b is None or (b in pref_a[a] and a in pref_b[b]) for a, b in enumerate(M))


def todos_estables(pref_a, pref_b):
    """Fuerza bruta: todos los emparejamientos aceptables sin parejas bloqueantes."""
    na, opciones = len(pref_a), [lista + [None] for lista in pref_a]
    res = []
    for M in itertools.product(*opciones):
        usados = [b for b in M if b is not None]
        if len(usados) == len(set(usados)) and aceptable(list(M), pref_a, pref_b) \
                and not bloqueantes(list(M), pref_a, pref_b):
            res.append(list(M))
    return res


def instancia(rng, na, nb, receptores_completos):
    pref_a = [rng.sample(range(nb), rng.randint(0, nb)) for _ in range(na)]
    if receptores_completos:
        pref_b = [rng.sample(range(na), na) for _ in range(nb)]
    else:
        pref_b = [rng.sample(range(na), rng.randint(0, na)) for _ in range(nb)]
    return pref_a, pref_b


def gale_shapley_original(pref_a, pref_b):
    """El de la conferencia 3, que supone listas completas: no saca de la cola a quien agotó su lista."""
    rango = [{a: l for l, a in enumerate(lista)} for lista in pref_b]
    siguiente, pareja_de_b = [0] * len(pref_a), [None] * len(pref_b)
    libres = deque(range(len(pref_a)))
    while libres:
        a = libres.popleft()
        b = pref_a[a][siguiente[a]]            # IndexError si a ya le propuso a toda su lista
        siguiente[a] += 1
        actual = pareja_de_b[b]
        if actual is None:
            pareja_de_b[b] = a
        elif rango[b][a] < rango[b][actual]:
            pareja_de_b[b] = a; libres.append(actual)
        else:
            libres.append(a)


def gale_shapley_olvidadizo(pref_a, pref_b):
    """Error plantado: al desplazado no se lo vuelve a poner en la cola."""
    rango = [{a: l for l, a in enumerate(lista)} for lista in pref_b]
    siguiente, pareja_de_b = [0] * len(pref_a), [None] * len(pref_b)
    libres = deque(a for a in range(len(pref_a)) if pref_a[a])
    while libres:
        a = libres.popleft()
        b = pref_a[a][siguiente[a]]
        siguiente[a] += 1
        actual = pareja_de_b[b]
        if a in rango[b] and (actual is None or rango[b][a] < rango[b][actual]):
            pareja_de_b[b] = a                 # ... y `actual` queda libre, pero nadie lo anota
        elif siguiente[a] < len(pref_a[a]):
            libres.append(a)
    M = [None] * len(pref_a)
    for b, a in enumerate(pareja_de_b):
        if a is not None:
            M[a] = b
    return M


if __name__ == "__main__":
    rng = random.Random(2026)

    # 1. El algoritmo adaptado contra fuerza bruta
    casos = 0
    for receptores_completos in (True, False):
        for _ in range(1500):
            na, nb = rng.randint(1, 5), rng.randint(1, 5)
            pref_a, pref_b = instancia(rng, na, nb, receptores_completos)
            estables = todos_estables(pref_a, pref_b)
            resultados = []
            for orden in ("cola", "pila", "azar"):
                M, k = gale_shapley(pref_a, pref_b, orden, semilla=casos, vigilar=True)
                assert aceptable(M, pref_a, pref_b)                  # nadie con alguien que no listó
                assert not bloqueantes(M, pref_a, pref_b)            # estable
                assert k <= sum(len(l) for l in pref_a)              # cota del potencial
                resultados.append(M)
            assert resultados[0] == resultados[1] == resultados[2]   # no depende del orden
            M = resultados[0]
            assert M in estables
            # óptimo para los proponentes: cada uno tiene la mejor pareja posible entre los estables
            for a in range(na):
                assert all(not prefiere(pref_a[a], E[a], M[a]) for E in estables)
            # los que tienen pareja son los mismos en todos los estables
            solos = {tuple(a for a in range(na) if E[a] is None) for E in estables}
            assert len(solos) == 1
            casos += 1
    print(f"{casos} instancias (la mitad con receptores de lista completa, la mitad incompleta), "
          f"3 órdenes cada una:")
    print("  estable, aceptable, el mismo para los 3 órdenes, óptimo para los proponentes,")
    print("  potencial vigilado, y los mismos solos que en todos los emparejamientos estables")

    # 2. Propuestas contra la cota del potencial
    print(f"\n{'n':>5} {'largo de cada lista':>21} {'cota Σ|L(a)|':>13} {'propuestas':>11} {'n²':>8}")
    for n in [10, 100, 1000]:
        for largo in [3, n // 2]:
            pref_a = [rng.sample(range(n), largo) for _ in range(n)]
            pref_b = [rng.sample(range(n), n) for _ in range(n)]
            M, k = gale_shapley(pref_a, pref_b)
            cota = sum(len(l) for l in pref_a)
            assert k <= cota and not bloqueantes(M, pref_a, pref_b) if n <= 100 else k <= cota
            print(f"{n:>5} {largo:>21} {cota:>13} {k:>11} {n * n:>8}")

    # 3. El algoritmo original con listas incompletas
    fallos = total = 0
    for _ in range(2000):
        pref_a, pref_b = instancia(rng, 5, 5, True)
        if any(len(l) == 0 for l in pref_a):
            continue
        total += 1
        try:
            gale_shapley_original(pref_a, pref_b)
        except IndexError:
            fallos += 1
    print(f"\nAlgoritmo original con listas incompletas: se cae (IndexError) en {fallos} de {total} "
          f"instancias ({100 * fallos / total:.1f} %)")
    assert fallos > 0

    # 4. El error plantado y las dos definiciones de pareja bloqueante
    vieja = nueva = inestables = 0
    ejemplo = None
    for _ in range(2000):
        pref_a, pref_b = instancia(rng, 5, 5, True)
        M = gale_shapley_olvidadizo(pref_a, pref_b)
        if bloqueantes(M, pref_a, pref_b):
            inestables += 1
            nueva += 1
            vieja += bool(bloqueantes_vieja(M, pref_a, pref_b))
            if ejemplo is None and not bloqueantes_vieja(M, pref_a, pref_b) and len(pref_a) <= 5:
                ejemplo = (pref_a, pref_b, M, bloqueantes(M, pref_a, pref_b))
    print(f"\nVersión que olvida al desplazado, 2000 instancias 5x5: {inestables} inestables")
    print(f"  la definición vieja de pareja bloqueante detecta {vieja} ({100 * vieja / inestables:.1f} %)")
    print(f"  la definición nueva detecta {nueva} (100 %)")
    assert vieja < nueva
    # el contraejemplo más chico: a0 es desplazado por a1 y nadie lo vuelve a poner en la cola
    pref_a, pref_b = [[0, 1], [0]], [[1, 0], [0]]
    M = gale_shapley_olvidadizo(pref_a, pref_b)
    assert M == [None, 0] and bloqueantes(M, pref_a, pref_b) == [(0, 1)] and not bloqueantes_vieja(M, pref_a, pref_b)
    assert gale_shapley(pref_a, pref_b)[0] == [1, 0]

    # 5. Un ejemplo chico para el documento
    pref_a = [[0, 1], [0], [0, 1]]
    pref_b = [[1, 2, 0], [0, 2, 1]]
    traza = []
    M, k = gale_shapley(pref_a, pref_b, traza=traza)
    print("\nEjemplo: a0 lista b0, b1; a1 lista b0; a2 lista b0, b1. b0: a1 > a2 > a0; b1: a0 > a2 > a1")
    for paso, (a, b, antes, despues) in enumerate(traza, 1):
        print(f"  {paso}. a{a} -> b{b}: tenía {'nadie' if antes is None else f'a{antes}'}, "
              f"se queda con a{despues}")
    print(f"  resultado: {['a%d-%s' % (a, 'solo' if b is None else 'b%d' % b) for a, b in enumerate(M)]}, "
          f"{k} propuestas")
    assert not bloqueantes(M, pref_a, pref_b) and M == [1, 0, None]
