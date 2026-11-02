import random
from collections import deque
from itertools import product

def gale_shapley(L, pref_b, orden="cola", semilla = 0, check = False):
    n = len(L)
    rango = [[0]* n for _ in range(n)]

    for b in range(n):
        for lugar, a in enumerate(pref_b[b]):
            rango[b][a] = lugar

    siguiente = [0] * n
    pareja_de_b = [None] * n
    libres = deque(range(n))
    azar = random.Random(semilla)
    propuestas = 0

    phi = sum(len(l) for l in L)

    while libres:
        if orden == "azar":
            libres.rotate(azar.randrange(len(libres)))
        a = libres.popleft() if orden == "cola" else libres.pop()
        if siguiente[a] == len(L[a]):
            continue

        b = L[a][siguiente[a]]
        siguiente[a] += 1
        propuestas += 1
        antes = pareja_de_b[b]

        if antes is None:
            pareja_de_b[b] = a
        elif rango[b][a] < rango[b][antes]:
            pareja_de_b[b] = a
            libres.append(antes)
        else:
            libres.append(a)

        if check:
            nuevo = sum(len(L[x]) - siguiente[x] for x in range(n))
            assert nuevo == phi - 1
            phi = nuevo
            assert pareja_de_b[b] is not None
            assert antes is None or rango[b][pareja_de_b[b]] <= rango[b][antes]

    M = [None] * n
    for b, a in enumerate(pareja_de_b):
        if a is not None:
            M[a] = b

    if check:
        assert propuestas <= sum(len(l) for l in L)
        for a in range(n):
            if M[a] is None:
                assert siguiente[a] == len(L[a])
            else:
                assert M[a] in L[a]

    return M, propuestas

def pares_bloqueantes(M, L, pref_b):
    n = len(M)
    pareja_de_b = {M[a]: a for a in range(n) if M[a] is not None}
    bloquenates = []

    for a in range(n):
        for b in L[a]:
            if b == M[a]:
                continue
            aPrefiere = M[a] is None or L[a].index(b) < L[a].index(M[a])
            bPrefiere = b not in pareja_de_b or pref_b[b].index(a) < pref_b[b].index(pareja_de_b[b])

            if aPrefiere and bPrefiere:
                bloquenates.append((a,b))

    return bloquenates

def instancia(n, rng, completas = False):
    L = []
    for _ in range(n):
        k = n if completas else rng.randint(0, n)
        L.append(rng.sample(range(n), k))
    pref_b = [rng.sample(range(n), n) for _ in range(n)]
    return L, pref_b

def todos_estables(L, pref_b):
    n = len(L)
    estables = []

    for eleecion in product(*[[None] + l for l in L]):
        usados = [b for b in eleecion if b is not None]

        if len(usados) == len(set(usados)) and not pares_bloqueantes(list(eleecion), L , pref_b):
            estables.append(list(eleecion))

    return estables

if __name__ == "__main__":
    L = [[0, 1], [0], []]                          # a3 no lista a nadie
    pref_b = [[1, 0, 2], [0, 1, 2], [2, 0, 1]]
    M, k = gale_shapley(L, pref_b)
    print("  parejas:", ", ".join(f"a{a + 1}-b{b + 1}" for a, b in enumerate(M) if b is not None),
          "| solos:", ", ".join(f"a{a + 1}" for a, b in enumerate(M) if b is None))
    print(f"  propuestas: {k}, suma de las listas: {sum(len(l) for l in L)}")
    print(f"  pares bloqueantes: {pares_bloqueantes(M, L, pref_b)}  "
          f"(b3 prefiere a a3 a quedar solo, pero a3 no lista a b3)")
    print()

    rng = random.Random(12)
    print(f"{'n':>3} {'instancias':>11} {'bloqueantes':>12} {'M entre los estables':>21} "
          f"{'propuestas':>11} {'suma listas':>12} {'solos':>6}")
    for n, veces in [(3, 500), (4, 300), (5, 100), (20, 100), (60, 20)]:
        bloq = entre = propuestas = suma = solos = 0
        for _ in range(veces):
            L, pref_b = instancia(n, rng)
            resultados = [gale_shapley(L, pref_b, o, s, check=True)
                          for o, s in [("cola", 0), ("pila", 0), ("azar", 1)]]
            M, k = resultados[0]
            bloq += sum(len(pares_bloqueantes(R, L, pref_b)) for R, _ in resultados)
            propuestas += k
            suma += sum(len(l) for l in L)
            solos += M.count(None)
            if n <= 5:
                entre += all(R in todos_estables(L, pref_b) for R, _ in resultados)
        marca = f"{entre} de {veces}" if n <= 5 else "-"
        print(f"{n:>3} {veces:>11} {bloq:>12} {marca:>21} {propuestas / veces:>11.1f} "
              f"{suma / veces:>12.1f} {solos / veces:>6.1f}")

    solos = 0
    for _ in range(200):
        L, pref_b = instancia(10, rng, completas=True)
        M, _ = gale_shapley(L, pref_b, check=True)
        assert not pares_bloqueantes(M, L, pref_b)
        solos += M.count(None)
    print()
    print(f"con listas completas (200 instancias, n = 10): {solos} proponentes solos")