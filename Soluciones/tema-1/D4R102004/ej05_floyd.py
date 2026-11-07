"""Ejercicio 5: detección de ciclos de Floyd (liebre y tortuga), con el invariante
(tortuga = nodo t, liebre = nodo 2t) y el potencial d vigilados."""
import random


class Nodo:
    def __init__(self, i):
        self.i, self.siguiente = i, None


def construir(mu, lam):
    """Lista con mu nodos antes del ciclo y un ciclo de lam nodos (lam = 0: sin ciclo)."""
    nodos = [Nodo(i) for i in range(mu + lam)]
    for a, b in zip(nodos, nodos[1:]):
        a.siguiente = b
    if lam > 0:
        nodos[-1].siguiente = nodos[mu]          # el último vuelve a la entrada del ciclo
    return nodos[0] if nodos else None


def nodo_numero(inicio, k):
    """El nodo al que se llega desde el inicio con k pasos (None si se sale de la lista)."""
    x = inicio
    for _ in range(k):
        if x is None:
            return None
        x = x.siguiente
    return x


def tiene_ciclo(inicio, mu=None, lam=None):
    """Floyd. Si se dan mu y lam, vigila el invariante y el potencial. Devuelve (hay ciclo?, pasos)."""
    tortuga = liebre = inicio
    t = 0
    d_anterior = None
    while liebre is not None and liebre.siguiente is not None:
        tortuga = tortuga.siguiente
        liebre = liebre.siguiente.siguiente
        t += 1
        if mu is not None:
            # invariante: después de t pasos, tortuga = nodo t y liebre = nodo 2t
            assert tortuga is nodo_numero(inicio, t) and liebre is nodo_numero(inicio, 2 * t)
            if lam > 0 and t >= mu:
                # potencial: lo que le falta a la liebre para alcanzar a la tortuga en el ciclo
                d = (tortuga.i - liebre.i) % lam
                assert 0 <= d <= lam - 1
                assert d_anterior is None or d == d_anterior - 1   # baja exactamente 1
                d_anterior = d
        if tortuga is liebre:
            return True, t
    return False, t


random.seed(5)
for _ in range(3000):
    mu, lam = random.randint(0, 30), random.choice([0, random.randint(1, 30)])
    if mu + lam == 0:
        continue
    hay, pasos = tiene_ciclo(construir(mu, lam), mu, lam)
    assert hay == (lam > 0)
    n = mu + lam
    assert pasos <= (mu + lam if lam > 0 else n // 2)
print("3000 listas al azar (con y sin ciclo): respuesta correcta,")
print("invariante (tortuga = nodo t, liebre = nodo 2t) y potencial (d baja de 1 en 1) cumplidos\n")

print(f"{'mu':>6} {'lambda':>7} {'n':>6} {'pasos':>6}")
for mu, lam in [(0, 1), (0, 10), (10, 0), (10, 1), (2, 6), (100, 100), (500, 3), (3, 500), (1000, 0)]:
    print(f"{mu:>6} {lam:>7} {mu + lam:>6} {tiene_ciclo(construir(mu, lam))[1]:>6}")
