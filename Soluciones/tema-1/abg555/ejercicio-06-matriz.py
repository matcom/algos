def search_matrix(M, x, trace=None):
    # Busca x en una matriz n x n con filas y columnas ordenadas de forma creciente.
    # Empieza en la esquina de arriba a la derecha. Devuelve (i, j) o None.
    # Si se pasa una lista en trace, guarda (i, j) de cada celda que compara.
    n = len(M)
    i, j = 0, n - 1                          # invariante: si x esta, esta en filas i.., columnas ..j
    while i < n and j >= 0:
        if trace is not None:
            trace.append((i, j))
        if M[i][j] == x:
            return (i, j)
        if M[i][j] < x:
            i += 1                           # toda la fila i (hasta j) es menor que x
        else:
            j -= 1                           # toda la columna j (desde i) es mayor que x
    return None


def search_matrix_top_left(M, x):
    # Error: empezar en la esquina de arriba a la izquierda. Desde ahi, si M[i][j] < x
    # no se puede descartar ni la fila ni la columna; esta version avanza a la derecha.
    n = len(M)
    i, j = 0, 0
    while i < n and j < n:
        if M[i][j] == x:
            return (i, j)
        if M[i][j] < x:
            j += 1
        else:
            i += 1
    return None


def is_sorted_matrix(M):
    n = len(M)
    filas = all(M[i][j] <= M[i][j + 1] for i in range(n) for j in range(n - 1))
    columnas = all(M[i][j] <= M[i + 1][j] for i in range(n - 1) for j in range(n))
    return filas and columnas


class Adversary:
    # El adversario de la demostracion. Contesta como si la matriz fuera
    #   -1 arriba de la antidiagonal (i + j < n - 1)
    #   +1 abajo de la antidiagonal (i + j > n - 1)
    #   -1 en la antidiagonal (por ahora)
    # y x = 0. Anota que celdas de la antidiagonal le preguntaron.
    def __init__(self, n):
        self.n = n
        self.asked = set()
        self.comparisons = 0

    def compare(self, i, j):
        # devuelve el signo de M[i][j] - x
        self.comparisons += 1
        if i + j < self.n - 1:
            return -1
        if i + j > self.n - 1:
            return +1
        self.asked.add((i, j))
        return -1

    def matrix(self, with_x_at=None):
        # Una matriz concreta consistente con todas las respuestas.
        n = self.n
        M = [[-1 if i + j <= n - 1 else 1 for j in range(n)] for i in range(n)]
        if with_x_at is not None:
            i, j = with_x_at
            M[i][j] = 0
        return M


def staircase_with_oracle(n, compare):
    # La busqueda en escalera, pero preguntando al oraculo en vez de leer la matriz.
    i, j = 0, n - 1
    while i < n and j >= 0:
        s = compare(i, j)
        if s == 0:
            return (i, j)
        if s < 0:
            i += 1
        else:
            j -= 1
    return None
