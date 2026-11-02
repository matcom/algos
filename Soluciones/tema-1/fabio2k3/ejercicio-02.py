# Caso de Prueba del ejercicio 2

import random
import math

def busqueda_vigilida(Q, x):
    l = 0
    r = len(Q) - 1
    comparaciones = 0
    phiAnt = r - l + 2  # una unidad mas que el potencial inicial

    while l <= r:
        assert all(Q[i] < x for i in range(l))
        assert all(Q[i] > x for i in range(r + 1, len(Q)))

        phi = r - l + 1
        assert 1 <= phi < phiAnt
        phiAnt = phi

        m = (l+r) // 2
        comparaciones += 1

        if Q[m] == x:
            return m, comparaciones
        elif Q[m] < x:
            l = m + 1
        else:
            r = m - 1

    return -1, comparaciones

random.seed(0)
for _ in range(20000):
    n = random.randint(0,40)
    Q = sorted(random.sample(range(100), n))
    x = random.choice(Q) if Q and random.random() < 0.5 else random.randint(-5,105)

    res, c = busqueda_vigilida(Q, x)

    assert (res == - 1) == (x not in Q)
    assert res == -1 or Q[res] == x
    assert c == 0 if n == 0 else c <= math.floor(math.log2(n)) + 1

print("FETEN")