def kesimo_particion(a, b, k=None):
    """
    Encuentra el k-esimo menor elemento de dos arreglos ordenados.
    Para la mediana inferior de dos arreglos de longitud n, k = n.
    """
    n, m = len(a), len(b)

    if k is None:
        k = n

    if not (1 <= k <= n + m):
        raise ValueError("k debe estar entre 1 y n + m")

    lo, hi = max(0, k - m), min(n, k)

    while lo < hi:
        mid = (lo + hi + 1) // 2
        j = k - mid

        # Evaluacion de C1(mid): a[mid - 1] <= b[j]
        if mid == 0 or j >= m or a[mid - 1] <= b[j]:
            lo = mid
        else:
            hi = mid - 1

    # Particion final
    i, j = lo, k - lo

    # El k-esimo menor es el maximo de la mitad izquierda
    if i == 0:
        return b[j - 1]
    if j == 0:
        return a[i - 1]

    return max(a[i - 1], b[j - 1])