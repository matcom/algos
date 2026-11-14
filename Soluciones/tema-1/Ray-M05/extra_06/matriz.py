import sys

from comun.tabla import tabla_md


def escalera(n, comparar):
    i, j = 0, n - 1
    camino = []
    while i < n and j >= 0:
        camino.append((i, j))
        r = comparar(i, j)
        if r == 0:
            return True, camino
        if r < 0:
            j -= 1
        else:
            i += 1
    return False, camino


def familia(n, en_x=()):
    x = 2 * (n + 1)
    M = [[2 * (i + j) for j in range(1, n + 1)] for i in range(1, n + 1)]
    for i in range(n):
        M[i][n - 1 - i] = x if i in en_x else x - 1
    return M, x


def es_creciente(M):
    n = len(M)
    return all(M[i][j] < M[i][j + 1] for i in range(n) for j in range(n - 1)) and \
        all(M[i][j] < M[i + 1][j] for i in range(n - 1) for j in range(n))


def busqueda_por_filas(n, comparar):
    camino = []
    for i in range(n):
        lo, hi = 0, n
        while lo < hi:
            m = (lo + hi) // 2
            camino.append((i, m))
            r = comparar(i, m)
            if r == 0:
                return True, camino
            if r < 0:
                hi = m
            else:
                lo = m + 1
    return False, camino


def primera_columna_y_fila(n, comparar):
    camino = []
    lo, hi = 0, n
    while lo < hi:
        m = (lo + hi) // 2
        camino.append((m, 0))
        r = comparar(m, 0)
        if r == 0:
            return True, camino
        if r < 0:
            hi = m
        else:
            lo = m + 1
    fila = lo - 1
    if fila < 0:
        return False, camino
    lo, hi = 0, n
    while lo < hi:
        m = (lo + hi) // 2
        camino.append((fila, m))
        r = comparar(fila, m)
        if r == 0:
            return True, camino
        if r < 0:
            hi = m
        else:
            lo = m + 1
    return False, camino


def enfrentar(algoritmo, n):
    M, x = familia(n)

    def comparar(i, j):
        return (x > M[i][j]) - (x < M[i][j])

    respuesta, camino = algoritmo(n, comparar)
    vistas = {i for i, j in camino if i + j == n - 1}
    faltan = [i for i in range(n) if i not in vistas]
    if not faltan:
        return len(camino), len(vistas), None


    trampa, _ = familia(n, en_x={faltan[0]}) if not respuesta else familia(n)
    assert es_creciente(trampa)

    def comparar_trampa(i, j):
        return (x > trampa[i][j]) - (x < trampa[i][j])

    respuesta_trampa, _ = algoritmo(n, comparar_trampa)
    hay_x = any(x in fila for fila in trampa)
    assert respuesta_trampa == respuesta and respuesta_trampa != hay_x
    return len(camino), len(vistas), trampa


ALGORITMOS = {
    "escalera": escalera,
    "búsqueda binaria en cada fila": busqueda_por_filas,
    "primera columna y después una fila": primera_columna_y_fila,
}


def _adversario():
    filas = []
    for nombre, algoritmo in ALGORITMOS.items():
        for n in (8, 64):
            comparaciones, vistas, trampa = enfrentar(algoritmo, n)
            filas.append([nombre, n, comparaciones, f"{vistas} de {n}",
                          "no" if trampa is None else "sí"])
    print(tabla_md(["algoritmo", "n", "comparaciones", "antidiagonal comparada",
                    "el adversario lo engaña"], filas, "idddc"))


def _trampa():
    n = 4
    _, _, trampa = enfrentar(primera_columna_y_fila, n)
    _, x = familia(n)
    k = next(i for i in range(n) if trampa[i][n - 1 - i] == x) + 1
    filas = "\n".join("    " + "  ".join(f"{v:>2}" for v in fila) for fila in trampa)
    print(f"Con $n = {n}$ y $x = {x}$, el algoritmo de la primera columna da la misma respuesta "
          f"en $B$, que no contiene a $x$, y en $B^{{({k})}}$, que lo tiene en la casilla "
          f"$({k}, {n + 1 - k})$, que nunca miró:\n\n```\n{filas}\n```")


SECCIONES = {
    "adversario": _adversario,
    "trampa": _trampa,
}

if __name__ == "__main__":
    SECCIONES[sys.argv[1]]()
