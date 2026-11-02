import random

def build(m , l):
    n = m + l
    nxt = [i + 1  for i in range(n)]
    if n>0:
        nxt[n-1] = m if l > 0 else -1
    return nxt

def renombrar(nxt):
    n = len(nxt)
    perm = random.sample(range(n), n)
    new = [-1]*n

    for i in range(n):
        new[perm[i]] = perm[nxt[i]] if nxt[i] != -1 else -1

    return new, (perm[0] if n > 0 else -1)

def recorrido(nxt, head, large):
    camino, x = [] , head
    while len(camino) < large and x != -1:
        camino.append(x)
        x = nxt[x]
    return camino

def floyd(nxt, head, check = False):
    camino = recorrido(nxt, head, 2*len(nxt) + 2) if check else None

    t = h = head
    i = 0
    while h != -1 and nxt[h] != -1:
        if check:
            assert t == camino[i] and h == camino[2*i]
        t = nxt[t]
        h = nxt[nxt[h]]

        i += 1
        if t == h:
            return True, i

    return False, i

def tieneCiclo(nxt, head):
    visto , x = set(), head
    while x != -1:
        if x in visto:
            return True
        visto.add(x)
        x = nxt[x]
    return False

def esperadas(m, l):
    if l == 0:
        return None
    p = max(m , 1)
    return l * (-(-p // l))

if __name__ == "__main__":
    print(f"{'mu':>4} {'lam':>4} {'n':>4} {'iter':>5} {'esperadas':>10} {'cota':>5}")
    for mu, lam in [(0, 1), (0, 5), (1, 1), (3, 4), (7, 3), (10, 10), (25, 7), (40, 1), (6, 0), (7, 0)]:
        nxt, head = renombrar(build(mu, lam))
        hay, it = floyd(nxt, head, check=True)
        n = mu + lam
        cota = n if lam > 0 else n // 2
        esp = esperadas(mu, lam)
        assert hay == (lam > 0) and it <= cota and (esp is None or it == esp)
        print(f"{mu:>4} {lam:>4} {n:>4} {it:>5} {str(esp) if esp else '-':>10} {cota:>5}")

    random.seed(0)
    total = con_ciclo = desacuerdos = 0
    peor = 0.0
    for _ in range(2000):
        mu, lam = random.randint(0, 30), random.choice([0, 0, 1, 2, 3, 5, 8, 13])
        nxt, head = renombrar(build(mu, lam))
        hay, it = floyd(nxt, head, check=True)
        total += 1
        con_ciclo += hay
        desacuerdos += hay != tieneCiclo(nxt, head)
        if mu + lam > 0:
            peor = max(peor, it / (mu + lam))
    print()
    print(f"instancias:              {total}")
    print(f"con ciclo / sin ciclo:   {con_ciclo} / {total - con_ciclo}")
    print(f"desacuerdos con la referencia: {desacuerdos}")
    print(f"max iteraciones / n:     {peor:.2f}")