"""Ejercicio 12. Gale-Shapley con listas incompletas."""
import random
from itertools import product


def gale_shapley_incompleto(listas_a, pref_b, orden="pila", semilla=0):
    """Devuelve (pareja_de_b, iteraciones). Comprueba que el potencial baja."""
    n = len(listas_a)
    rango = [[0] * n for _ in range(n)]
    for b in range(n):
        for lugar, a in enumerate(pref_b[b]):
            rango[b][a] = lugar
    siguiente = [0] * n
    pareja_de_b = [None] * n
    libres = list(range(n))
    azar = random.Random(semilla)
    iteraciones = 0

    def phi():
        return sum(len(listas_a[a]) - siguiente[a] for a in range(n)) + len(libres)

    anterior = phi()
    inicial = anterior
    while libres:
        if orden == "azar":
            libres.append(libres.pop(azar.randrange(len(libres))))
        a = libres.pop() if orden != "cola" else libres.pop(0)
        iteraciones += 1
        if siguiente[a] == len(listas_a[a]):
            pass                                        # lista agotada: se queda solo
        else:
            b = listas_a[a][siguiente[a]]
            siguiente[a] += 1
            actual = pareja_de_b[b]
            if actual is None:
                pareja_de_b[b] = a
            elif rango[b][a] < rango[b][actual]:
                pareja_de_b[b] = a
                libres.append(actual)
            else:
                libres.append(a)
        nuevo = phi()
        assert nuevo <= anterior - 1                     # el potencial baja al menos 1
        anterior = nuevo
    assert iteraciones <= inicial <= n * n + n
    return pareja_de_b, iteraciones


def bloqueantes(listas_a, pref_b, pareja_de_b):
    """Pares bloqueantes según la definición adaptada."""
    n = len(listas_a)
    pareja_de_a = {a: b for b, a in enumerate(pareja_de_b) if a is not None}
    res = []
    for a in range(n):
        for b in listas_a[a]:
            if pareja_de_a.get(a) == b:
                continue
            a_prefiere = a not in pareja_de_a or listas_a[a].index(b) < listas_a[a].index(pareja_de_a[a])
            b_prefiere = pareja_de_b[b] is None or pref_b[b].index(a) < pref_b[b].index(pareja_de_b[b])
            if a_prefiere and b_prefiere:
                res.append((a, b))
    return res


if __name__ == "__main__":
    # Ejemplos A y B del texto (índices desde 0)
    print("Ejemplo A:", gale_shapley_incompleto([[0], [0, 1]], [[0, 1], [0, 1]]))
    print("Ejemplo B:", gale_shapley_incompleto([[0], [0]], [[1, 0], [0, 1]]))
    # Ejemplo de tres proponentes: a1:[b1], a2:[b1,b2], a3:[b1]; b1: a3 > a2 > a1
    L = [[0], [0, 1], [0]]
    PB = [[2, 1, 0], [0, 1, 2], [0, 1, 2]]
    M, it = gale_shapley_incompleto(L, PB, orden="cola")
    print("Tres proponentes, cola:", M, "iteraciones", it, "bloqueantes", bloqueantes(L, PB, M))

    rng = random.Random(12)
    casos, sin_pareja, max_it = 0, 0, 0
    for _ in range(4000):
        n = rng.randint(1, 8)
        listas = [rng.sample(range(n), rng.randint(0, n)) for _ in range(n)]
        pref_b = [rng.sample(range(n), n) for _ in range(n)]
        resultados = set()
        for orden, s in [("pila", 0), ("cola", 0), ("azar", 1), ("azar", 2)]:
            M, it = gale_shapley_incompleto(listas, pref_b, orden, s)
            assert not bloqueantes(listas, pref_b, M)
            resultados.add(tuple(M))
            max_it = max(max_it, it)
        assert len(resultados) == 1                      # no depende del orden
        sin_pareja += sum(1 for a in range(n) if a not in [x for x in M if x is not None])
        casos += 1
    print(f"\n{casos} instancias aleatorias (n <= 8), 4 órdenes de ejecución cada una:")
    print("  sin parejas bloqueantes en todas; el resultado no depende del orden")
    print(f"  máx. iteraciones observadas: {max_it}  (cota n^2 + n)")
    print(f"  proponentes que quedaron solos en total: {sin_pareja}")
