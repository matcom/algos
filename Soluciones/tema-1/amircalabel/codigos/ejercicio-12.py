import random

def gale_shapley_incompleto(pref_a, pref_b):
    """pref_a[a] es la lista (posiblemente parcial) de receptores que a lista.
    pref_b[b] es la lista (posiblemente parcial) de proponentes que b lista.
    Devuelve el emparejamiento M (lista de receptor o None)."""
    n = len(pref_a)
    # Rango de a en la lista de b: rango[b][a] = posición, o +inf si no está
    rango = [[float('inf')] * n for _ in range(n)]
    for b in range(n):
        for lugar, a in enumerate(pref_b[b]):
            rango[b][a] = lugar
    siguiente = [0] * n
    pareja_de_b = [None] * n
    libres = list(range(n))
    while libres:
        a = libres.pop()
        if siguiente[a] >= len(pref_a[a]):
            continue  # a propuso a todos los de su lista, queda soltero
        b = pref_a[a][siguiente[a]]
        siguiente[a] += 1
        actual = pareja_de_b[b]
        if actual is None:
            pareja_de_b[b] = a
        elif rango[b][a] < rango[b][actual]:
            pareja_de_b[b] = a
            libres.append(actual)
        else:
            libres.append(a)
    M = [None] * n
    for b, a in enumerate(pareja_de_b):
        if a is not None:
            M[a] = b
    return M

def pares_bloqueantes(M, pref_a, pref_b):
    """Verifica si hay parejas bloqueantes con la definición adaptada."""
    n = len(M)
    pareja_de_b = {b: a for a, b in enumerate(M) if b is not None}
    bloqueantes = []
    for a in range(n):
        for b in pref_a[a]:
            if M[a] == b:
                continue  # ya están juntos
            # ¿a prefiere b a M(a) o está soltero?
            prefiere_a = M[a] is None or pref_a[a].index(b) < pref_a[a].index(M[a])
            # ¿b prefiere a a M(b) o está soltero?
            if b not in pareja_de_b:
                prefiere_b = True
            else:
                actual = pareja_de_b[b]
                prefiere_b = a in pref_b[b] and (actual not in pref_b[b] or pref_b[b].index(a) < pref_b[b].index(actual))
            if prefiere_a and prefiere_b and a in pref_b[b]:
                bloqueantes.append((a, b))
    return bloqueantes

def instancia_incompleta(n, prob=0.7, rng=None):
    """Genera listas incompletas: cada uno lista a cada del otro lado con prob."""
    if rng is None:
        rng = random.Random()
    pref_a = []
    for a in range(n):
        lista = [b for b in range(n) if rng.random() < prob]
        rng.shuffle(lista)
        pref_a.append(lista)
    pref_b = []
    for b in range(n):
        lista = [a for a in range(n) if rng.random() < prob]
        rng.shuffle(lista)
        pref_b.append(lista)
    return pref_a, pref_b

def main():
    rng = random.Random(7)
    print(f"{'n':>4} {'instancias':>11} {'bloqueantes':>12} {'solteros':>9}")
    for n, veces in [(5, 200), (10, 100), (20, 50)]:
        bloqueantes = 0
        solteros = 0
        for _ in range(veces):
            pref_a, pref_b = instancia_incompleta(n, 0.7, rng)
            M = gale_shapley_incompleto(pref_a, pref_b)
            bloqueantes += len(pares_bloqueantes(M, pref_a, pref_b))
            solteros += sum(1 for m in M if m is None)
        print(f"{n:>4} {veces:>11} {bloqueantes:>12} {solteros/veces:>9.1f}")

if __name__ == "__main__":
    main()
