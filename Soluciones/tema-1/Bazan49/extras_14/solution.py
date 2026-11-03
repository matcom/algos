def maximo_y_minimo(A):
    n = len(A)

    if n == 0:
        return None, None

    # Inicialización del primer par o elemento
    if n % 2 == 1:
        min_val = max_val = A[0]
        inicio = 1
    else:
        if A[0] <= A[1]:
            min_val, max_val = A[0], A[1]
        else:
            min_val, max_val = A[1], A[0]
        inicio = 2

    # Procesamiento por parejas
    for i in range(inicio, n, 2):
        x, y = A[i], A[i + 1]

        if x <= y:
            menor, mayor = x, y
        else:
            menor, mayor = y, x

        if menor < min_val:
            min_val = menor

        if mayor > max_val:
            max_val = mayor

    return min_val, max_val