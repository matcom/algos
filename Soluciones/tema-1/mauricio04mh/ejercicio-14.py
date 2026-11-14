"""Ejercicio 14 del Tema 1: Torres de Hanoi, algoritmo y cota minima coinciden.

Uso: python3 ejercicio-14.py

Los discos se numeran 1 (el mas pequeno) .. n (el mas grande). Las varillas
son 1, 2 y 3. Todas las comprobaciones son con assert y no usan azar.
"""
from collections import deque
from itertools import product


# ---------------------------------------------------------------- algoritmo
def hanoi(n, origen, destino, auxiliar, movimientos):
    """El algoritmo recursivo (seccion «El algoritmo» del md)."""
    if n == 0:
        return
    hanoi(n - 1, origen, auxiliar, destino, movimientos)
    movimientos.append((n, origen, destino))
    hanoi(n - 1, auxiliar, destino, origen, movimientos)


def resolver(n):
    movimientos = []
    hanoi(n, 1, 3, 2, movimientos)
    return movimientos


# ------------------------------------------- simulador con la especificacion
def mover(pilas, disco, o, d):
    """Mueve un disco y comprueba las dos reglas del juego."""
    assert pilas[o] and pilas[o][-1] == disco, "el disco no esta en la cima"
    assert not pilas[d] or pilas[d][-1] > disco, "disco grande sobre pequeno"
    pilas[d].append(pilas[o].pop())


def pre(n, o, d, a, pilas):
    """Pre(n): los discos n..1 son la cima de origen; lo demas es mayor que n."""
    cima_ok = n == 0 or pilas[o][-n:] == list(range(n, 0, -1))
    resto_ok = all(x > n for x in pilas[d] + pilas[a])
    return cima_ok and resto_ok


def hanoi_vigilado(n, o, d, a, pilas, cuenta):
    """El mismo algoritmo, pero comprueba Pre(n) al entrar y Post(n) al salir.

    cuenta[0] = llamadas con n >= 1; cuenta[1] = de ellas, las que entran con
    alguna de las otras dos varillas no vacia (la precondicion 'varillas
    vacias' seria falsa en ellas)."""
    if n == 0:
        return
    assert pre(n, o, d, a, pilas), f"Pre({n}) falsa"
    cuenta[0] += 1
    cuenta[1] += bool(pilas[d] or pilas[a])
    antes = {k: list(v) for k, v in pilas.items()}
    hanoi_vigilado(n - 1, o, a, d, pilas, cuenta)
    mover(pilas, n, o, d)
    hanoi_vigilado(n - 1, a, d, o, pilas, cuenta)
    # Post(n): n..1 en la cima de destino; lo demas, intacto
    assert pilas[d][-n:] == list(range(n, 0, -1))
    assert pilas[d][:-n] == antes[d]
    assert pilas[o] == antes[o][:-n]
    assert pilas[a] == antes[a]


# ------------------------------------------------ oraculo: busqueda en anchura
def vecinos(estado, p):
    """Estados alcanzables con un movimiento legal. estado[i] = varilla (0..p-1)
    del disco i (el disco 0 es el mas pequeno)."""
    for i in range(len(estado)):
        a = estado[i]
        if any(estado[j] == a for j in range(i)):
            continue                     # un disco mas pequeno lo tapa
        for b in range(p):
            if b == a or any(estado[j] == b for j in range(i)):
                continue                 # mismo sitio, o tapado en el destino
            yield estado[:i] + (b,) + estado[i + 1:]


def bfs(n, p=3):
    """Devuelve (distancia minima, numero de caminos minimos)."""
    inicio, fin = (0,) * n, (p - 1,) * n
    dist, formas = {inicio: 0}, {inicio: 1}
    cola = deque([inicio])
    while cola:
        u = cola.popleft()
        for v in vecinos(u, p):
            if v not in dist:
                dist[v], formas[v] = dist[u] + 1, 0
                cola.append(v)
            if dist[v] == dist[u] + 1:
                formas[v] += formas[u]
    return dist[fin], formas[fin]


def lema_disco_grande(n):
    """Lema B: en TODO estado legal, cuando el disco n se puede mover, los
    otros n-1 estan en la tercera varilla. Comprueba los 3^n estados."""
    movibles = 0
    for estado in product(range(3), repeat=n):
        for v in vecinos(estado, 3):
            if v[-1] != estado[-1]:                  # se movio el disco n
                tercera = 3 - estado[-1] - v[-1]
                assert all(x == tercera for x in estado[:-1]), estado
                movibles += 1
    return movibles


def estados_de(movimientos, n):
    """Aplica una lista de movimientos a la configuracion inicial."""
    estado = [0] * n
    for disco, o, d in movimientos:
        assert estado[disco - 1] == o - 1
        assert all(estado[j] not in (o - 1, d - 1) for j in range(disco - 1))
        estado[disco - 1] = d - 1
        yield tuple(estado)


# ------------------------------------------- extension: Frame-Stewart (4 varillas)
def frame_stewart(n):
    """Movimientos del algoritmo de Frame-Stewart con 4 varillas:
    FS(n) = min_k 2 FS(k) + (2^(n-k) - 1), con FS(0) = 0 y FS(1) = 1."""
    fs = [0, 1]
    for m in range(2, n + 1):
        fs.append(min(2 * fs[k] + 2 ** (m - k) - 1 for k in range(1, m)))
    return fs[n]


def mejor_k(n):
    return min(range(1, n), key=lambda k: 2 * frame_stewart(k) + 2 ** (n - k) - 1)


def hanoi_discos(discos, o, d, a, movimientos):
    """El algoritmo de 3 varillas sobre una lista de discos (de menor a mayor)."""
    if not discos:
        return
    hanoi_discos(discos[:-1], o, a, d, movimientos)
    movimientos.append((discos[-1], o, d))
    hanoi_discos(discos[:-1], a, d, o, movimientos)


def fs_mover(discos, o, d, a, b, movimientos):
    """Frame-Stewart: los k menores a una auxiliar con 4 varillas, el resto al
    destino con 3 (la varilla de los k menores no se puede usar), y los k encima."""
    n = len(discos)
    if n == 0:
        return
    if n == 1:
        movimientos.append((discos[0], o, d))
        return
    k = mejor_k(n)
    fs_mover(discos[:k], o, a, d, b, movimientos)
    hanoi_discos(discos[k:], o, d, b, movimientos)
    fs_mover(discos[:k], a, d, o, b, movimientos)


def simular(movimientos, n, p):
    """Aplica los movimientos con p varillas, comprobando las reglas; devuelve las pilas."""
    pilas = {v: [] for v in range(1, p + 1)}
    pilas[1] = list(range(n, 0, -1))
    for disco, o, d in movimientos:
        mover(pilas, disco, o, d)
    return pilas


# -------------------------------------------------------------------- pruebas
if __name__ == "__main__":
    # 1. Traza de n = 3
    print("n = 3:", " ".join(f"{d}:{o}->{x}" for d, o, x in resolver(3)))
    print()

    # 2. Costo exacto y recurrencia
    print(f"{'n':>3} {'movimientos':>12} {'2^n - 1':>10} {'2T(n-1)+1':>10}")
    anterior = 0
    for n in range(1, 13):
        m = len(resolver(n))
        assert m == 2 ** n - 1 == 2 * anterior + 1
        if n <= 6 or n == 12:
            print(f"{n:>3} {m:>12,} {2 ** n - 1:>10,} {2 * anterior + 1:>10,}")
        anterior = m
    print()

    # 3. Correctitud: Pre/Post en cada llamada, con discos mayores ya colocados
    for n in range(0, 9):
        pilas = {1: list(range(n, 0, -1)), 2: [], 3: []}
        cuenta = [0, 0]
        hanoi_vigilado(n, 1, 3, 2, pilas, cuenta)
        assert pilas == {1: [], 2: [], 3: list(range(n, 0, -1))}
        if n == 8:
            print(f"n = {n}: Pre y Post vigiladas en {cuenta[0]} llamadas; "
                  f"{cuenta[1]} entran con otra varilla no vacia")
    pilas = {1: [9, 8, 3, 2, 1], 2: [7], 3: [6, 5]}   # hay discos mayores
    hanoi_vigilado(3, 1, 3, 2, pilas, [0, 0])
    assert pilas == {1: [9, 8], 2: [7], 3: [6, 5, 3, 2, 1]}
    print("subproblema n = 3 con discos mayores en las tres varillas:",
          pilas)
    print()

    # 4. El algoritmo es un camino legal que lleva de (0,..,0) a (2,..,2)
    for n in range(1, 11):
        *_, final = estados_de(resolver(n), n)
        assert final == (2,) * n
    print("el algoritmo produce un camino legal hasta el estado final (n <= 10)")
    print()

    # 5. Cota minima: oraculo de busqueda en anchura sobre los 3^n estados
    print(f"{'n':>3} {'estados 3^n':>12} {'minimo (BFS)':>13} {'2^n - 1':>8} "
          f"{'caminos minimos':>16} {'2M(n-1)+1':>10}")
    minimo_ant = 0
    for n in range(1, 11):
        minimo, formas = bfs(n)
        assert minimo == 2 ** n - 1 and formas == 1
        assert minimo >= 2 * minimo_ant + 1              # la recurrencia de la cota
        print(f"{n:>3} {3 ** n:>12,} {minimo:>13} {2 ** n - 1:>8} "
              f"{formas:>16} {2 * minimo_ant + 1:>10}")
        minimo_ant = minimo
    print()

    # 6. Lema B comprobado en todos los estados
    for n in range(1, 9):
        movibles = lema_disco_grande(n)
    print(f"lema del disco grande: comprobado en los 3^n estados, n <= 8 "
          f"(n = 8: {movibles} movimientos posibles del disco 8 en todo el "
          f"grafo, todos con los demas en la tercera varilla)")
    print()

    # 7. El modelo importa: con 4 varillas la cota 2^n - 1 deja de valer
    print("con 4 varillas, minimo por BFS:",
          [bfs(n, 4)[0] for n in range(1, 8)],
          " (con 3 varillas:", [2 ** n - 1 for n in range(1, 8)], ")")
    print()

    # 8. Extension: el algoritmo de Frame-Stewart con 4 varillas
    print(f"{'n':>3} {'Frame-Stewart':>14} {'minimo (BFS)':>13} {'k elegido':>10}")
    for n in range(1, 10):
        movimientos = []
        fs_mover(list(range(1, n + 1)), 1, 4, 2, 3, movimientos)
        assert simular(movimientos, n, 4)[4] == list(range(n, 0, -1))
        assert len(movimientos) == frame_stewart(n) == bfs(n, 4)[0]
        print(f"{n:>3} {len(movimientos):>14} {bfs(n, 4)[0]:>13} "
              f"{mejor_k(n) if n > 1 else '-':>10}")
    # los incrementos: FS(n) - FS(n-1) = 2^t, con t(t+1)/2 < n <= (t+1)(t+2)/2
    for n in range(1, 61):
        t = 0
        while (t + 1) * (t + 2) // 2 < n:
            t += 1
        assert frame_stewart(n) - frame_stewart(n - 1) == 2 ** t
    print("FS(n) - FS(n-1) = 2^t para t(t+1)/2 < n <= (t+1)(t+2)/2, n <= 60;",
          "FS(20) =", frame_stewart(20), "contra 2^20 - 1 =", 2 ** 20 - 1)
