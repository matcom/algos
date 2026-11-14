"""Ejercicio 5. Detección de ciclos con dos punteros (Floyd)."""
import math
import random


class Nodo:
    def __init__(self, v):
        self.v, self.next = v, None


def construir(mu, lam):
    """Lista con cola de largo mu y ciclo de largo lam (lam = 0: sin ciclo)."""
    n = mu + lam
    nodos = [Nodo(i) for i in range(n)]
    for i in range(n - 1):
        nodos[i].next = nodos[i + 1]
    if lam:
        nodos[-1].next = nodos[mu]
    return nodos[0] if nodos else None, nodos


def floyd(head, vigilar_nodos=None):
    """Devuelve (¿hay ciclo?, vueltas). Si recibe la lista de nodos x_i, comprueba
    el invariante slow = x_k, fast = x_2k (en el caso con ciclo, con índices
    módulo el ciclo)."""
    slow = fast = head
    vueltas = 0
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        vueltas += 1
        if vigilar_nodos is not None:
            xs = vigilar_nodos
            mu, lam = xs["mu"], xs["lam"]
            def x(j):                       # el nodo x_j (None si se sale de la lista)
                if lam == 0:
                    return xs["nodos"][j] if j < mu else None
                return xs["nodos"][j if j < mu + lam else mu + (j - mu) % lam]
            assert slow is x(vueltas)
            assert fast is x(2 * vueltas)
        if slow is fast:
            return True, vueltas
    return False, vueltas


if __name__ == "__main__":
    print(f"{'caso':>26} {'n':>3} {'mu':>3} {'lam':>4} {'vueltas':>8} {'prevista':>9}")
    for mu, lam in [(0, 3), (2, 3), (0, 0), (4, 0), (3, 0)]:
        head, nodos = construir(mu, lam)
        r, v = floyd(head, {"nodos": nodos, "mu": mu, "lam": lam})
        n = mu + lam
        prev = lam * math.ceil(max(mu, 1) / lam) if lam else n // 2
        assert r == (lam > 0) and v == prev
        print(f"{'ciclo' if lam else 'sin ciclo':>26} {n:>3} {mu:>3} {lam:>4} {v:>8} {prev:>9}")

    random.seed(1)
    casos = 0
    peor_razon = 0.0
    for _ in range(5000):
        mu, lam = random.randint(0, 25), random.choice([0, 0, 1, 2, 3, 5, 8, 13])
        head, nodos = construir(mu, lam)
        r, v = floyd(head, {"nodos": nodos, "mu": mu, "lam": lam})
        n = mu + lam
        prev = lam * math.ceil(max(mu, 1) / lam) if lam else n // 2
        assert r == (lam > 0) and v == prev
        if n:
            assert v <= max(n, 1)
            peor_razon = max(peor_razon, v / n)
        casos += 1
    print(f"\n{casos} listas aleatorias: respuesta correcta, invariante y número de "
          f"vueltas k* iguales a la fórmula; máx. vueltas/n = {peor_razon:.2f}")

    # Todas las listas de hasta N nodos. Una lista de n nodos queda determinada por
    # a dónde apunta el último: a None o a uno de los n nodos, así que hay n + 1
    # formas, una por cada (mu, lam) con mu + lam = n.
    N = 60
    formas = 0
    for n in range(0, N + 1):
        for lam in range(0, n + 1):
            mu = n - lam
            head, nodos = construir(mu, lam)
            r, v = floyd(head, {"nodos": nodos, "mu": mu, "lam": lam})
            prev = lam * math.ceil(max(mu, 1) / lam) if lam else n // 2
            assert r == (lam > 0) and v == prev and v <= max(n, 1)
            formas += 1
    print(f"todas las listas de hasta {N} nodos ({formas} formas): respuesta, "
          f"invariante y vueltas iguales a las fórmulas")
