"""
Tema 1, ejercicio 6: buscar un valor x en una matriz n x n con filas y
columnas ordenadas de forma creciente.

  * algoritmo en O(n) comparaciones (busqueda en escalera)
  * correctitud parcial con un invariante, terminacion con un potencial (C3)
  * cota minima Omega(n) con un adversario (C5)

Modelo (como la busqueda binaria de C5): el algoritmo solo compara x con
una entrada A[i][j] y obtiene -1, 0 o +1 segun A[i][j] <, = o > x.
Uso:  python ejercicio6_matriz.py
"""
import random
from pathlib import Path


# ----------------------------------------------------------------------------
# El algoritmo
# ----------------------------------------------------------------------------
def buscar(n, cmp):
    """cmp(i, j) devuelve -1, 0, +1 segun A[i][j] <, =, > x.
    Devuelve (esta, comparaciones)."""
    i, j = 0, n - 1                      # esquina superior derecha
    comparaciones = 0
    while i < n and j >= 0:
        r = cmp(i, j)
        comparaciones += 1
        if r == 0:
            return True, comparaciones
        if r > 0:                        # A[i][j] > x: sobra la columna j
            j -= 1
        else:                            # A[i][j] < x: sobra la fila i
            i += 1
    return False, comparaciones


def buscar_en_matriz(A, x):
    return buscar(len(A), lambda i, j: (A[i][j] > x) - (A[i][j] < x))


def esta_oraculo(A, x):
    return any(x in fila for fila in A)


# ----------------------------------------------------------------------------
# Version vigilada: ejecuta el invariante y el potencial de la demostracion
# ----------------------------------------------------------------------------
def buscar_vigilado(A, x):
    n = len(A)
    i, j = 0, n - 1
    comparaciones = 0
    phi_prev = None
    verdad = esta_oraculo(A, x)
    while True:
        # INVARIANTE: si x esta en A, esta en las filas i..n-1, columnas 0..j
        region = [A[r][c] for r in range(i, n) for c in range(j + 1)]
        assert (x in region) == verdad
        # POTENCIAL: filas que quedan + columnas que quedan
        phi = (n - i) + (j + 1)
        assert phi >= 0 and (phi_prev is None or phi == phi_prev - 1)
        phi_prev = phi
        if not (i < n and j >= 0):       # region vacia
            assert verdad is False
            assert comparaciones <= max(2 * n - 1, 0)
            return False, comparaciones
        comparaciones += 1
        if A[i][j] == x:
            assert verdad is True
            assert comparaciones <= 2 * n - 1
            return True, comparaciones
        if A[i][j] > x:
            j -= 1
        else:
            i += 1


# ----------------------------------------------------------------------------
# Generador de matrices ordenadas
# ----------------------------------------------------------------------------
def es_ordenada(A, estricta=False):
    n = len(A)
    ok = (lambda a, b: a < b) if estricta else (lambda a, b: a <= b)
    filas = all(ok(A[i][j], A[i][j + 1]) for i in range(n) for j in range(n - 1))
    cols = all(ok(A[i][j], A[i + 1][j]) for i in range(n - 1) for j in range(n))
    return filas and cols


def matriz_ordenada(n, rng, rango):
    """Ordenar cada fila y despues cada columna deja las filas ordenadas."""
    A = [sorted(rng.randrange(rango) for _ in range(n)) for _ in range(n)]
    cols = [sorted(A[i][j] for i in range(n)) for j in range(n)]
    return [[cols[j][i] for j in range(n)] for i in range(n)]


# ----------------------------------------------------------------------------
# Cota minima: el adversario
# ----------------------------------------------------------------------------
def matrices_adversario(n, c=None):
    """M0: la antidiagonal (i + j = n - 1) vale x - 1 y no hay x.
    M1: igual a M0, salvo que la celda c de la antidiagonal vale x.
    Con x = 3(n-1) ambas tienen filas y columnas estrictamente crecientes."""
    x = 3 * (n - 1)
    M0 = [[3 * (i + j) for j in range(n)] for i in range(n)]
    for k in range(n):
        M0[k][n - 1 - k] = x - 1
    if c is None:
        return M0, x
    M1 = [fila[:] for fila in M0]
    M1[c][n - 1 - c] = x
    return M0, M1, x


def buscar_apurado(n, cmp):
    """Algoritmo que se rinde: hace a lo sumo n - 1 comparaciones."""
    i, j = 0, n - 1
    for _ in range(n - 1):
        if not (i < n and j >= 0):
            break
        r = cmp(i, j)
        if r == 0:
            return True
        if r > 0:
            j -= 1
        else:
            i += 1
    return False


def jugar_adversario(alg, n):
    """Corre 'alg' contra M0. Si deja una celda de la antidiagonal sin
    preguntar, construye M1 y comprueba que 'alg' da la misma respuesta."""
    M0, x = matrices_adversario(n)
    preguntadas = set()

    def cmp0(i, j):
        preguntadas.add((i, j))
        return (M0[i][j] > x) - (M0[i][j] < x)

    resp = alg(n, cmp0)
    resp = resp[0] if isinstance(resp, tuple) else resp
    sin_preguntar = [k for k in range(n) if (k, n - 1 - k) not in preguntadas]
    if not sin_preguntar:
        return resp, len(preguntadas), None
    c = sin_preguntar[0]
    M0, M1, x = matrices_adversario(n, c)
    assert es_ordenada(M0, True) and es_ordenada(M1, True)
    assert all(M0[i][j] == M1[i][j] for (i, j) in preguntadas)
    resp1 = alg(n, lambda i, j: (M1[i][j] > x) - (M1[i][j] < x))
    resp1 = resp1[0] if isinstance(resp1, tuple) else resp1
    assert resp1 == resp                 # mismas respuestas, misma salida
    mal = "M1 (tiene x)" if resp is False else "M0 (no tiene x)"
    return resp, len(preguntadas), mal


# ----------------------------------------------------------------------------
# Animacion (opcional, necesita Pillow)
# ----------------------------------------------------------------------------
def generar_gif(A, x, ruta):
    from PIL import Image, ImageDraw, ImageFont

    try:
        fuente = ImageFont.load_default(size=18)
        chica = ImageFont.load_default(size=14)
    except TypeError:
        fuente = chica = ImageFont.load_default()
    n = len(A)
    C, X0, Y0 = 64, 40, 70
    W, H = 2 * X0 + C * n, Y0 + C * n + 60

    def cuadro(i, j, actual, color, msg, phi, paso):
        im = Image.new("RGB", (W, H), "white")
        d = ImageDraw.Draw(im)
        d.text((15, 10), f"x = {x}      paso {paso}", fill="black", font=fuente)
        for a in range(n):
            for b in range(n):
                activa = a >= i and b <= j
                fondo = "#ffffff" if activa else "#dddddd"
                if actual and (a, b) == (i, j):
                    fondo = color
                x0, y0 = X0 + b * C, Y0 + a * C
                d.rectangle([x0, y0, x0 + C, y0 + C], fill=fondo,
                            outline="#555555", width=2)
                d.text((x0 + C // 2 - 12, y0 + C // 2 - 9), str(A[a][b]),
                       fill="black" if activa else "#999999", font=fuente)
        d.text((15, Y0 + C * n + 12), msg, fill="#b00020", font=chica)
        d.text((15, Y0 + C * n + 34), f"Phi = (n - i) + (j + 1) = {phi}",
               fill="#444444", font=chica)
        return im

    frames, i, j, paso = [], 0, n - 1, 0
    while i < n and j >= 0:
        paso += 1
        v = A[i][j]
        phi = (n - i) + (j + 1)
        if v == x:
            frames.append(cuadro(i, j, True, "#7fd18b",
                                 f"A[{i}][{j}] = {v} = x: encontrado", phi, paso))
            break
        if v > x:
            frames.append(cuadro(i, j, True, "#ffe27a",
                                 f"A[{i}][{j}] = {v} > x: se descarta la columna {j}",
                                 phi, paso))
            j -= 1
        else:
            frames.append(cuadro(i, j, True, "#ffe27a",
                                 f"A[{i}][{j}] = {v} < x: se descarta la fila {i}",
                                 phi, paso))
            i += 1
    else:
        frames.append(cuadro(i, j, False, "", "region vacia: x no esta",
                             (n - i) + (j + 1), paso + 1))
    frames += [frames[-1]] * 2
    frames[0].save(ruta, save_all=True, append_images=frames[1:],
                   duration=1100, loop=0)


# ----------------------------------------------------------------------------
# Experimentos
# ----------------------------------------------------------------------------
EJEMPLO = [[1, 4, 7, 11, 15],
           [2, 5, 8, 12, 19],
           [3, 6, 9, 16, 22],
           [10, 13, 14, 17, 24],
           [18, 21, 23, 26, 30]]


def traza(A, x):
    n = len(A)
    print(f"Traza con x = {x} (n = {n}):")
    print(f"{'paso':>5} {'(i,j)':>7} {'A[i][j]':>8} {'resultado':>10} {'phi':>5}")
    i, j, paso = 0, n - 1, 0
    while i < n and j >= 0:
        paso += 1
        v = A[i][j]
        res = "=" if v == x else (">" if v > x else "<")
        print(f"{paso:>5} {str((i, j)):>7} {v:>8} {res:>10} {(n - i) + (j + 1):>5}")
        if v == x:
            return
        if v > x:
            j -= 1
        else:
            i += 1
    print("      region vacia -> False")


def exhaustivo():
    rng = random.Random(6)
    casos, peor = 0, 0
    for n in range(1, 9):
        for rango in (4, 30, 1000):
            for _ in range(150):
                A = matriz_ordenada(n, rng, rango)
                assert es_ordenada(A)
                xs = {-1, rango} | {rng.randrange(rango) for _ in range(6)}
                xs |= {A[rng.randrange(n)][rng.randrange(n)] for _ in range(6)}
                for x in xs:
                    esta, k = buscar_vigilado(A, x)      # los assert viven aqui
                    assert esta == esta_oraculo(A, x)
                    assert (esta, k) == buscar_en_matriz(A, x)
                    peor = max(peor, k - (2 * n - 1))
                    casos += 1
    print(f"invariante, potencial y resultado comprobados en {casos} casos "
          f"(n <= 8), sin fallos; maximo de (comparaciones - (2n-1)) = {peor}")


def experimento_adversario():
    print(f"{'n':>4} {'buscar: preguntas':>18} {'antidiag. vistas':>17} "
          f"{'apurado: preguntas':>19} {'se equivoca en':>16}")
    for n in (3, 5, 8, 16, 32):
        r, preg, mal = jugar_adversario(buscar, n)
        assert mal is None and preg >= n         # un algoritmo correcto las ve todas
        M0, x = matrices_adversario(n)
        _, k = buscar(n, lambda i, j: (M0[i][j] > x) - (M0[i][j] < x))
        r2, preg2, mal2 = jugar_adversario(buscar_apurado, n)
        print(f"{n:>4} {k:>18} {n:>17} {preg2:>19} {str(mal2):>16}")


def main():
    traza(EJEMPLO, 14)
    print()
    exhaustivo()
    print()
    experimento_adversario()
    print()
    try:
        ruta = Path(__file__).with_name("matriz_animacion.gif")
        generar_gif(EJEMPLO, 14, ruta)
        print("animacion guardada en", ruta.name)
    except ImportError:
        print("(sin Pillow: se omite la animacion)")


if __name__ == "__main__":
    main()
