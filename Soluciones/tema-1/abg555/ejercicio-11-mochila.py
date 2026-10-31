from itertools import combinations


def knapsack(weights, values, W, stats=None):
    # Programacion dinamica: best[c] = el mejor valor con capacidad c
    # usando los objetos vistos hasta ahora. Es la tabla de (n+1) x (W+1)
    # de siempre, guardando solo la fila anterior.
    # Si se pasa un diccionario en stats, cuenta las celdas que llena.
    best = [0] * (W + 1)
    cells = W + 1                              # la fila 0
    for w, v in zip(weights, values):
        for c in range(W, -1, -1):             # de derecha a izquierda: cada objeto una vez
            if w <= c and best[c - w] + v > best[c]:
                best[c] = best[c - w] + v
        cells += W + 1
    if stats is not None:
        stats["cells"] = cells
    return best[W]


def knapsack_table(weights, values, W):
    # La version con la tabla entera, solo para mostrarla en la prueba 1.
    n = len(weights)
    best = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        w, v = weights[i - 1], values[i - 1]
        for c in range(W + 1):
            best[i][c] = best[i - 1][c]
            if w <= c and best[i - 1][c - w] + v > best[i][c]:
                best[i][c] = best[i - 1][c - w] + v
    return best


def brute_force(weights, values, W):
    # Prueba los 2^n subconjuntos: obviamente correcto, solo sirve para n chico.
    n = len(weights)
    best = 0
    for k in range(n + 1):
        for subset in combinations(range(n), k):
            if sum(weights[i] for i in subset) <= W:
                best = max(best, sum(values[i] for i in subset))
    return best


def input_bits(weights, values, W):
    # El tamano de la entrada: los bits de todos los numeros escritos en binario.
    return sum(max(x.bit_length(), 1) for x in weights + values + [W])
