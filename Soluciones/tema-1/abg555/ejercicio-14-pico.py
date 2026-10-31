def peak_linear(A, stats=None):
    # Fuerza bruta: recorrer y quedarse con el mayor. n - 1 comparaciones.
    best = 0
    for i in range(1, len(A)):
        if stats is not None:
            stats["comparisons"] = stats.get("comparisons", 0) + 1
        if A[i] > A[best]:
            best = i
    return best


def peak_binary(A, trace=None, stats=None):
    # Pico de un arreglo unimodal: estrictamente creciente hasta el pico y
    # estrictamente decreciente despues. Compara cada vez dos vecinos.
    lo, hi = 0, len(A) - 1                 # invariante: el pico esta en [lo, hi]
    while lo < hi:
        if trace is not None:
            trace.append((lo, hi))
        if stats is not None:
            stats["comparisons"] = stats.get("comparisons", 0) + 1
        m = (lo + hi) // 2
        if A[m] < A[m + 1]:                # todavia subiendo: el pico esta a la derecha de m
            lo = m + 1
        else:                              # ya bajando: el pico es m o esta a su izquierda
            hi = m
    if trace is not None:
        trace.append((lo, hi))
    return lo


def peak_binary_bug(A):
    # Error: hi = m - 1 en vez de hi = m. Descarta m aunque m pueda ser el pico.
    lo, hi = 0, len(A) - 1
    while lo < hi:
        m = (lo + hi) // 2
        if A[m] < A[m + 1]:
            lo = m + 1
        else:
            hi = m - 1
    return max(lo, 0)


def unimodal(n, p):
    # Un arreglo unimodal de largo n con el pico en la posicion p, con valores distintos.
    return [i for i in range(p + 1)] + [p - (i - p) + 0.5 for i in range(p + 1, n)]
