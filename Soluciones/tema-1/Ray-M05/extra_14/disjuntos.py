def disjuntos(A, B, comparar=lambda x, y: (x > y) - (x < y)):
    i, j = 0, 0
    while i < len(A) and j < len(B):
        r = comparar(A[i], B[j])
        if r == 0:
            return i, j
        if r < 0:
            i += 1
        else:
            j += 1
    return None


def intercalada(n):
    return list(range(1, 2 * n, 2)), list(range(2, 2 * n + 1, 2))
