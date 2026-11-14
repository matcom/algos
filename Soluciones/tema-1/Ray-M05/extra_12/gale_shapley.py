from collections import deque


def gale_shapley_incompleto(pref_a, pref_b, traza=None):
    n_a, n_b = len(pref_a), len(pref_b)
    rango = [[0] * n_a for _ in range(n_b)]
    for b in range(n_b):
        for lugar, a in enumerate(pref_b[b]):
            rango[b][a] = lugar
    siguiente = [0] * n_a
    pareja_de_b = [None] * n_b
    libres = deque(a for a in range(n_a) if pref_a[a])
    propuestas = 0
    while libres:
        a = libres.popleft()
        b = pref_a[a][siguiente[a]]
        siguiente[a] += 1
        propuestas += 1
        actual = pareja_de_b[b]
        if actual is None:
            pareja_de_b[b] = a
            rechazado = None
        elif rango[b][a] < rango[b][actual]:
            pareja_de_b[b] = a
            rechazado = actual
        else:
            rechazado = a
        if rechazado is not None and siguiente[rechazado] < len(pref_a[rechazado]):
            libres.append(rechazado)
        if traza is not None:
            traza.append((a, b, rechazado))
    pareja_de_a = [None] * n_a
    for b, a in enumerate(pareja_de_b):
        if a is not None:
            pareja_de_a[a] = b
    return pareja_de_a, propuestas
