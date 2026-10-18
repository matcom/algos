#!/usr/bin/env python3
"""
Verificación del Ejercicio 6: búsqueda en matriz n×n con filas y columnas ordenadas.

Convención de conteo (la misma del markdown): cada vez que se compara A[r][c]
con x cuenta como UNA comparación, y el resultado puede ser <, = o >.

Qué hace:
  1. Implementa el algoritmo del puntero que empieza en (1,n), con camino y conteo.
  2. Verifica los casos C1..C5 sobre la matriz 3×3 del ejemplo ilustrado.
  3. C6: matriz con valores repetidos, para varios x.
  4. C7: peor caso. Búsqueda EXHAUSTIVA en n = 1..4 del máximo de comparaciones,
     más una familia explícita de matrices que lo alcanza para cualquier n.
  5. Pruebas aleatorias contra fuerza bruta (corrección y cota de comparaciones).

Todas las posiciones se imprimen con índices desde 1: (fila, columna).

Uso:  python3 verificar_ejercicio_06.py
"""
import random


# ----------------------------------------------------------------------------
# Algoritmo
# ----------------------------------------------------------------------------
def buscar(A, x):
    """Devuelve (encontrado, comparaciones, camino). camino = casillas comparadas."""
    n = len(A)
    r, c = 0, n - 1              # r = 1, c = n  (índices desde 0 internamente)
    comparaciones = 0
    camino = []
    while r < n and c >= 0:
        comparaciones += 1
        camino.append((r + 1, c + 1))
        v = A[r][c]
        if v == x:
            return True, comparaciones, camino
        if v > x:
            c -= 1               # se descarta la columna c
        else:
            r += 1               # se descarta la fila r
    return False, comparaciones, camino


def es_valida(A):
    n = len(A)
    return all(A[i][j] <= A[i][j + 1] for i in range(n) for j in range(n - 1)) and \
           all(A[i][j] <= A[i + 1][j] for i in range(n - 1) for j in range(n))


def esta(A, x):
    return any(x in fila for fila in A)


def fmt_camino(camino, encontrado):
    txt = " → ".join(f"({r},{c})" for r, c in camino)
    return txt if encontrado else txt + " → fuera"


def fmt_matriz(A):
    ancho = max(len(str(v)) for fila in A for v in fila)
    return "\n".join("  ".join(str(v).rjust(ancho) for v in fila) for fila in A)


# ----------------------------------------------------------------------------
# C1..C5: matriz del ejemplo ilustrado
# ----------------------------------------------------------------------------
M3 = [[2, 5, 9],
      [4, 6, 10],
      [7, 8, 12]]

CASOS_M3 = [
    # id,  qué prueba,                                  x
    ("C1", "`x` presente en posición intermedia",        6),
    ("C2", "`x` menor que el mínimo",                    1),
    ("C3", "`x` mayor que el máximo",                    13),
    ("C4", "`x` en la esquina superior izquierda",       2),
    ("C5", "`x` ausente, valor intermedio",              3),
]


def casos_m3():
    print("=" * 78)
    print("CASOS C1..C5  (matriz del ejemplo ilustrado, n = 3)")
    print("=" * 78)
    assert es_valida(M3)
    print(fmt_matriz(M3), "\n")
    filas = []
    for cid, que, x in CASOS_M3:
        enc, comps, camino = buscar(M3, x)
        assert enc == esta(M3, x), f"{cid}: respuesta incorrecta"
        assert comps <= 2 * len(M3) - 1
        filas.append(f"| {cid} | {que} | {x} | {'sí' if enc else 'no'} | {comps} | "
                     f"{fmt_camino(camino, enc)} |")
        print(f"  {cid}: OK  x={x:<3} {'sí' if enc else 'no'}  comparaciones={comps}  "
              f"{fmt_camino(camino, enc)}")
    return filas


# ----------------------------------------------------------------------------
# C6: valores repetidos
# ----------------------------------------------------------------------------
REP = [[1, 1, 3],
       [1, 2, 3],
       [2, 2, 5]]


def caso_repetidos():
    print()
    print("=" * 78)
    print("C6  VALORES REPETIDOS")
    print("=" * 78)
    assert es_valida(REP)
    print(fmt_matriz(REP), "\n")
    filas = []
    for x in range(0, 7):
        enc, comps, camino = buscar(REP, x)
        assert enc == esta(REP, x), f"C6 x={x}: respuesta incorrecta"
        assert comps <= 2 * len(REP) - 1
        print(f"  x={x}: {'sí' if enc else 'no'}  comparaciones={comps}  "
              f"{fmt_camino(camino, enc)}")
    # Filas para la tabla final (se imprimen al final del script)
    for sufijo, x, que in (("a", 3, "repetidos en la columna del puntero; `x` en (1,3)"),
                           ("b", 1, "`x` repetido varias veces; se detiene en la primera aparición que visita"),
                           ("c", 2, "`x` repetido; el puntero baja una fila antes de encontrarlo"),
                           ("d", 4, "`x` ausente entre repetidos")):
        enc, comps, camino = buscar(REP, x)
        filas.append(f"| C6{sufijo} | {que} | {x} | {'sí' if enc else 'no'} | {comps} | "
                     f"{fmt_camino(camino, enc)} |")
    return filas


# ----------------------------------------------------------------------------
# C7: peor caso
# ----------------------------------------------------------------------------
def matrices_ordenadas(n, k):
    """Todas las matrices n×n con valores en 0..k, filas y columnas no decrecientes."""
    A = [[0] * n for _ in range(n)]

    def rec(pos):
        if pos == n * n:
            yield [fila[:] for fila in A]
            return
        i, j = divmod(pos, n)
        lo = max(A[i][j - 1] if j > 0 else 0, A[i - 1][j] if i > 0 else 0)
        for v in range(lo, k + 1):
            A[i][j] = v
            yield from rec(pos + 1)

    yield from rec(0)


def maximo_exhaustivo(n, k):
    """Máximo de comparaciones sobre TODAS las matrices y todos los x en -1..k+1."""
    mejor = {"todo": (0, None, None), "ausente": (0, None, None), "presente": (0, None, None)}
    cuenta_matrices = 0
    for A in matrices_ordenadas(n, k):
        cuenta_matrices += 1
        for x in range(-1, k + 2):
            enc, comps, _ = buscar(A, x)
            assert enc == esta(A, x)
            clave = "presente" if enc else "ausente"
            for c in (clave, "todo"):
                if comps > mejor[c][0]:
                    mejor[c] = (comps, [fila[:] for fila in A], x)
    return mejor, cuenta_matrices


def familia_peor_caso(n):
    """A[i][j] = 2*((j-1)*n + i): la columna j es mayor que toda la columna j-1.
    Con x = 2n+1 (impar, entre la columna 1 y la columna 2) el puntero recorre
    toda la fila 1 hacia la izquierda y toda la columna 1 hacia abajo."""
    A = [[2 * (j * n + i + 1) for j in range(n)] for i in range(n)]
    return A, 2 * n + 1


def peor_caso():
    print()
    print("=" * 78)
    print("C7  PEOR CASO")
    print("=" * 78)

    print("\n(a) Búsqueda exhaustiva: máximo de comparaciones sobre TODAS las matrices")
    print("    ordenadas con valores 0..k y todos los x en -1..k+1\n")
    print("| n | k | matrices | máx. (todo) | máx. (x presente) | máx. (x ausente) | 2n − 1 |")
    print("|---|---|----------|-------------|-------------------|------------------|--------|")
    ejemplos = {}
    for n, k in ((1, 4), (2, 4), (3, 4), (4, 3)):
        mejor, cuenta = maximo_exhaustivo(n, k)
        cota = 2 * n - 1
        assert mejor["todo"][0] == cota, f"n={n}: el máximo exhaustivo no es 2n-1"
        print(f"| {n} | {k} | {cuenta} | {mejor['todo'][0]} | {mejor['presente'][0]} | "
              f"{mejor['ausente'][0]} | {cota} |")
        ejemplos[n] = mejor

    for n in (2, 3):
        for etiqueta in ("presente", "ausente"):
            comps, A, x = ejemplos[n][etiqueta]
            print(f"\n    Primer ejemplo con n={n} y x {etiqueta}: x={x}, comparaciones={comps}")
            print("    " + fmt_matriz(A).replace("\n", "\n    "))
            _, _, camino = buscar(A, x)
            print(f"    camino: {fmt_camino(camino, etiqueta == 'presente')}")

    print("\n(b) En la matriz del ejemplo ilustrado (n = 3), máximo por valor de x")
    mx, xs = 0, []
    for x in range(0, 15):
        enc, comps, _ = buscar(M3, x)
        if comps > mx:
            mx, xs = comps, [x]
        elif comps == mx:
            xs.append(x)
    print(f"    máximo = {mx} comparaciones, alcanzado con x ∈ {xs}")
    for x in xs:
        enc, comps, camino = buscar(M3, x)
        print(f"    x={x}: {'sí' if enc else 'no'}  {fmt_camino(camino, enc)}")
    filas_m3 = []
    for x in xs:
        enc, comps, camino = buscar(M3, x)
        filas_m3.append(f"| C7a | peor caso en la matriz del ejemplo | {x} | {'sí' if enc else 'no'} | "
                        f"{comps} | {fmt_camino(camino, enc)} |")
    ausentes = [x for x in range(-5, 30) if not esta(M3, x) and buscar(M3, x)[1] == mx]
    print(f"    ¿hay algún x ENTERO ausente con {mx} comparaciones en esa matriz? "
          f"{'sí: ' + str(ausentes) if ausentes else 'no'}")

    print("\n(c) Familia explícita que alcanza 2n − 1 con x AUSENTE, para cualquier n")
    for n in range(1, 41):
        A, x = familia_peor_caso(n)
        assert es_valida(A) and not esta(A, x)
        enc, comps, _ = buscar(A, x)
        assert not enc and comps == 2 * n - 1, f"familia falla en n={n}"
    print("    Verificado para n = 1..40: comparaciones = 2n − 1 exactamente.")
    A, x = familia_peor_caso(3)
    enc, comps, camino = buscar(A, x)
    print(f"\n    Ejemplo n=3, x={x}:")
    print("    " + fmt_matriz(A).replace("\n", "\n    "))
    print(f"    comparaciones = {comps}   camino: {fmt_camino(camino, enc)}")
    filas_fam = [f"| C7b | peor caso con `x` ausente (otra matriz 3×3, ver abajo) | {x} | no | {comps} | "
                 f"{fmt_camino(camino, enc)} |"]
    return filas_m3 + filas_fam, A


# ----------------------------------------------------------------------------
# Pruebas aleatorias
# ----------------------------------------------------------------------------
def matriz_aleatoria(n, rnd, paso_max):
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            base = max(A[i - 1][j] if i else 0, A[i][j - 1] if j else 0)
            A[i][j] = base + rnd.randint(0, paso_max)   # 0 => repetidos
    return A


def pruebas_aleatorias(semilla=2026):
    print()
    print("=" * 78)
    print("PRUEBAS ALEATORIAS contra fuerza bruta")
    print("=" * 78)
    rnd = random.Random(semilla)
    total = 0
    maximo_visto = {}
    for _ in range(600):
        n = rnd.randint(1, 30)
        A = matriz_aleatoria(n, rnd, rnd.choice([1, 2, 5]))
        assert es_valida(A)
        for x in range(-1, A[-1][-1] + 2):
            enc, comps, _ = buscar(A, x)
            assert enc == esta(A, x), "respuesta distinta a la fuerza bruta"
            assert comps <= 2 * n - 1, "se pasó de 2n − 1"
            maximo_visto[n] = max(maximo_visto.get(n, 0), comps)
            total += 1
    print(f"  OK: {total} búsquedas en matrices de n = 1..30 (con repetidos), "
          f"todas correctas y con comparaciones ≤ 2n − 1.")


if __name__ == "__main__":
    f_m3 = casos_m3()
    f_rep = caso_repetidos()
    f_peor, A_fam = peor_caso()
    pruebas_aleatorias()

    print()
    print("=" * 78)
    print("TABLA COMPLETA PARA PEGAR EN EL MARKDOWN")
    print("=" * 78)
    print("\nMatriz de C1..C5 y C7a:\n")
    print("```\n" + fmt_matriz(M3) + "\n```\n")
    print("Matriz de C6 (con repetidos):\n")
    print("```\n" + fmt_matriz(REP) + "\n```\n")
    print("Matriz de C7b (peor caso con x ausente):\n")
    print("```\n" + fmt_matriz(A_fam) + "\n```\n")
    print("| ID | Qué prueba | `x` | Resultado | Comparaciones | Recorrido del puntero |")
    print("|----|------------|-----|-----------|---------------|-----------------------|")
    for f in f_m3 + f_rep + f_peor:
        print(f)
    print("\nTodo verificado.")
