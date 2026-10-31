def merge(A, B, log=None):
    # La mezcla de siempre. Devuelve (lista mezclada, comparaciones).
    # Si se pasa una lista en log, guarda los pares que compara.
    R, i, j, comparisons = [], 0, 0, 0
    while i < len(A) and j < len(B):
        comparisons += 1
        if log is not None:
            log.append((A[i], B[j]))
        if A[i] <= B[j]:
            R.append(A[i])
            i += 1
        else:
            R.append(B[j])
            j += 1
    return R + A[i:] + B[j:], comparisons


def merge_optimized(A, B, log=None):
    # La mezcla "optimizada": cuando a la primera lista le queda un solo elemento,
    # deja de comparar, copia lo que queda de B y pone ese elemento al final.
    R, i, j, comparisons = [], 0, 0, 0
    while len(A) - i > 1 and j < len(B):
        comparisons += 1
        if log is not None:
            log.append((A[i], B[j]))
        if A[i] <= B[j]:
            R.append(A[i])
            i += 1
        else:
            R.append(B[j])
            j += 1
    if j == len(B):                          # B se acabo antes: lo que queda de A va al final
        return R + A[i:], comparisons
    return R + B[j:] + A[i:], comparisons    # A tiene un solo elemento: va al final
