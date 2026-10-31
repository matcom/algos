INF = float("inf")


def median_two(A, B, trace=None, stats=None):
    # A y B ordenados, los dos de largo n >= 1. Devuelve el n-esimo menor de los 2n.
    # Busca cuantos elementos i se toman de A (y j = n - i de B) para formar los
    # n menores. Un corte i es valido si A[i-1] <= B[j] y B[j-1] <= A[i].
    n = len(A)
    lo, hi = 0, n                              # invariante: hay un corte valido en [lo, hi]
    while True:
        i = (lo + hi) // 2
        j = n - i
        a_left = A[i - 1] if i > 0 else -INF   # centinelas: si un lado no tiene elementos
        a_right = A[i] if i < n else INF
        b_left = B[j - 1] if j > 0 else -INF
        b_right = B[j] if j < n else INF
        if trace is not None:
            trace.append((lo, hi, i, j, a_left, a_right, b_left, b_right))
        if stats is not None:
            stats["comparisons"] = stats.get("comparisons", 0) + 1
        if a_left > b_right:                   # se tomaron demasiados de A
            hi = i - 1
            continue
        if stats is not None:
            stats["comparisons"] += 1
        if b_left > a_right:                   # se tomaron muy pocos de A
            lo = i + 1
            continue
        return max(a_left, b_left)             # corte valido: el mayor de los n menores


def median_two_bug(A, B):
    # Error: olvida el centinela de la izquierda. Con i = 0, A[i - 1] es A[-1],
    # que en Python es el ultimo elemento de A (y no da error).
    n = len(A)
    lo, hi = 0, n
    for _ in range(4 * n + 10):
        i = (lo + hi) // 2
        j = n - i
        a_left = A[i - 1]
        a_right = A[i] if i < n else INF
        b_left = B[j - 1]
        b_right = B[j] if j < n else INF
        if a_left > b_right:
            hi = i - 1
        elif b_left > a_right:
            lo = i + 1
        else:
            return max(a_left, b_left)
    return None


def valid_cuts(A, B):
    # Todos los cortes validos, por fuerza bruta (para las pruebas).
    n = len(A)
    res = []
    for i in range(n + 1):
        j = n - i
        a_left = A[i - 1] if i > 0 else -INF
        a_right = A[i] if i < n else INF
        b_left = B[j - 1] if j > 0 else -INF
        b_right = B[j] if j < n else INF
        if a_left <= b_right and b_left <= a_right:
            res.append(i)
    return res
