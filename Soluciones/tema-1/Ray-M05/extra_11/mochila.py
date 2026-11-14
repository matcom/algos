def mochila(pesos, valores, W):
    M = [0] * (W + 1)
    for w, v in zip(pesos, valores):
        for c in range(W, -1, -1):
            if w <= c and v + M[c - w] > M[c]:
                M[c] = v + M[c - w]
    return M[W]
