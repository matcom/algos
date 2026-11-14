import random


def par_cercano_rejilla(x, azar=random, traza=None):
    n = len(x)
    orden = list(range(n))
    azar.shuffle(orden)
    p = [x[k] for k in orden]
    if traza is not None:
        traza.append(p)

    def construir(m, delta):
        return {p[k] // delta: k for k in range(m)}

    delta, a, b = abs(p[1] - p[0]), 0, 1
    if delta == 0:
        return 0, orden[0], orden[1]
    rejilla = construir(2, delta)
    for i in range(2, n):
        c = p[i] // delta
        cerca = [rejilla[v] for v in (c - 1, c, c + 1) if v in rejilla]
        mejor = min(cerca, key=lambda k: abs(p[i] - p[k]), default=None)
        if traza is not None:
            traza.append((i, delta, c, mejor))
        if mejor is not None and abs(p[i] - p[mejor]) < delta:
            delta, a, b = abs(p[i] - p[mejor]), mejor, i
            if delta == 0:
                break
            rejilla = construir(i + 1, delta)
        else:
            rejilla[c] = i
    return delta, orden[a], orden[b]
