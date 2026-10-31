def binary_search(A, x, trace=None):
    # Busca x en el arreglo ordenado A.
    # Devuelve ("found", posicion) o ("gap", numero de hueco).
    # Si se pasa una lista en trace, guarda (lo, hi) antes de cada vuelta.
    lo, hi = 0, len(A)                     # invariante: si x esta, esta en A[lo:hi]
    while lo < hi:
        if trace is not None:
            trace.append((lo, hi))
        m = (lo + hi) // 2
        if x == A[m]:
            return ("found", m)
        if x < A[m]:
            hi = m
        else:
            lo = m + 1
    if trace is not None:
        trace.append((lo, hi))
    return ("gap", lo)


def binary_search_bug(A, x, max_steps=1000):
    # Error: lo = m en vez de lo = m + 1. Devuelve None si no termina en max_steps.
    lo, hi = 0, len(A)
    for _ in range(max_steps):
        if lo >= hi:
            return ("gap", lo)
        m = (lo + hi) // 2
        if x == A[m]:
            return ("found", m)
        if x < A[m]:
            hi = m
        else:
            lo = m
    return None


def comparisons(A, x):
    # Cuantas comparaciones con elementos de A hace la busqueda (una por vuelta).
    trace = []
    result = binary_search(A, x, trace)
    return len(trace) - (1 if result[0] == "gap" else 0)
