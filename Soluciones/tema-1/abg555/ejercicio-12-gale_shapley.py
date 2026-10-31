import random
from collections import deque
from itertools import permutations


def gale_shapley(pref_a, pref_b, order="queue", seed=0, trace=None):
    # pref_a[a]: la lista de a, de su favorito hacia abajo (puede estar incompleta).
    # pref_b[b]: la lista de b, de su favorito hacia abajo (puede estar incompleta).
    # Devuelve (M, proposals), con M[a] = la pareja de a, o None si queda solo.
    rank = [{a: place for place, a in enumerate(lst)} for lst in pref_b]
    next_place = [0] * len(pref_a)             # a que lugar de su lista va a proponer a
    partner_of_b = [None] * len(pref_b)
    free = deque(a for a in range(len(pref_a)) if pref_a[a])
    rng = random.Random(seed)
    proposals = 0

    while free:                                # solo estan los libres que les queda lista
        if order == "random":                  # rotar cuesta O(n); solo es para las pruebas
            free.rotate(rng.randrange(len(free)))
        a = free.popleft() if order == "queue" else free.pop()
        b = pref_a[a][next_place[a]]
        next_place[a] += 1
        proposals += 1
        current = partner_of_b[b]
        if a not in rank[b]:                   # b no listo a a: lo rechaza
            loser = a
        elif current is None:                  # b esta libre: acepta
            partner_of_b[b] = a
            loser = None
        elif rank[b][a] < rank[b][current]:    # b prefiere a a: cambia
            partner_of_b[b] = a
            loser = current
        else:                                  # b prefiere a su pareja: rechaza
            loser = a
        if trace is not None:
            trace.append((a, b, current, partner_of_b[b]))
        if loser is not None and next_place[loser] < len(pref_a[loser]):
            free.append(loser)                 # si ya no le queda lista, se queda solo

    M = [None] * len(pref_a)
    for b, a in enumerate(partner_of_b):
        if a is not None:
            M[a] = b
    return M, proposals


def gale_shapley_bug(pref_a, pref_b):
    # Error: copia el algoritmo de listas completas y no revisa si a se quedo sin lista.
    rank = [{a: place for place, a in enumerate(lst)} for lst in pref_b]
    next_place = [0] * len(pref_a)
    partner_of_b = [None] * len(pref_b)
    free = deque(range(len(pref_a)))
    while free:
        a = free.popleft()
        b = pref_a[a][next_place[a]]           # IndexError si la lista de a se acabo
        next_place[a] += 1
        current = partner_of_b[b]
        if a not in rank[b]:
            free.append(a)
        elif current is None:
            partner_of_b[b] = a
        elif rank[b][a] < rank[b][current]:
            partner_of_b[b] = a
            free.append(current)
        else:
            free.append(a)
    M = [None] * len(pref_a)
    for b, a in enumerate(partner_of_b):
        if a is not None:
            M[a] = b
    return M


def prefers(lst, x, y):
    # True si en la lista lst, x esta antes que y. Estar solo (None) va despues de todos.
    if y is None:
        return True
    return lst.index(x) < lst.index(y)


def blocking_pairs(M, pref_a, pref_b):
    # Oraculo por fuerza bruta: los pares (a, b) que se aceptan mutuamente, no estan
    # juntos, y los dos prefieren estar juntos a como estan (pareja o solos).
    partner_of_b = {b: a for a, b in enumerate(M) if b is not None}
    return [(a, b) for a in range(len(pref_a)) for b in pref_a[a]
            if a in pref_b[b] and M[a] != b
            and prefers(pref_a[a], b, M[a])
            and prefers(pref_b[b], a, partner_of_b.get(b))]


def blocking_pairs_old(M, pref_a, pref_b):
    # La definicion de listas completas, copiada sin adaptar: solo mira parejas
    # donde los dos tienen pareja.
    partner_of_b = {b: a for a, b in enumerate(M) if b is not None}
    return [(a, b) for a in range(len(pref_a)) for b in pref_a[a]
            if M[a] is not None and b in partner_of_b and M[a] != b
            and a in pref_b[b]
            and prefers(pref_a[a], b, M[a])
            and prefers(pref_b[b], a, partner_of_b[b])]


def unacceptable(M, pref_a, pref_b):
    # Parejas formadas con alguien que no esta en la lista del otro.
    return [(a, b) for a, b in enumerate(M)
            if b is not None and (b not in pref_a[a] or a not in pref_b[b])]


def is_stable(M, pref_a, pref_b):
    return not unacceptable(M, pref_a, pref_b) and not blocking_pairs(M, pref_a, pref_b)


def all_matchings(n_a, n_b):
    # Todos los emparejamientos posibles (cada uno puede quedar solo). Solo para n chico.
    opciones = list(range(n_b)) + [None] * n_a
    vistos = set()
    for p in permutations(opciones, n_a):
        if p not in vistos:
            vistos.add(p)
            yield list(p)


def random_instance(n_a, n_b, rng, complete_b=True):
    # Listas de los proponentes de largo al azar (0 a n_b). Los receptores con listas
    # completas, o tambien incompletas si complete_b es False.
    pref_a = [rng.sample(range(n_b), rng.randint(0, n_b)) for _ in range(n_a)]
    if complete_b:
        pref_b = [rng.sample(range(n_a), n_a) for _ in range(n_b)]
    else:
        pref_b = [rng.sample(range(n_a), rng.randint(0, n_a)) for _ in range(n_b)]
    return pref_a, pref_b
