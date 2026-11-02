"""Ejercicio 6: buscar x en una matriz n x n con filas y columnas crecientes.

Corre: python ejercicio-06.py   (pruebas, adversario y figura)
"""
import random

def escalera(A, x, comparar=None):
    """Búsqueda en escalera desde la esquina superior derecha.
    Devuelve ((i, j) o None, comparaciones). comparar(x, i, j) -> -1, 0, 1 (por defecto, lee A)."""
    n = len(A)
    if comparar is None:
        comparar = lambda x, i, j: (x > A[i][j]) - (x < A[i][j])
    i, j, comps = 0, n - 1, 0
    while i < n and j >= 0:
        comps += 1
        r = comparar(x, i, j)
        if r == 0:
            return (i, j), comps
        if r < 0:          # x < A[i][j]: toda la columna j desde la fila i es > x
            j -= 1
        else:              # x > A[i][j]: toda la fila i hasta la columna j es < x
            i += 1
    return None, comps


def escalera_vigilada(A, x):
    """Igual, pero comprueba el invariante y el potencial en cada paso."""
    n = len(A)
    i, j = 0, n - 1
    phi = (n - i) + (j + 1)
    while i < n and j >= 0:
        # I: fuera de la submatriz R = filas i..n-1 x columnas 0..j no hay ninguna x
        assert all(A[a][b] != x for a in range(n) for b in range(n) if not (a >= i and b <= j))
        if A[i][j] == x:
            return (i, j)
        if x < A[i][j]:
            j -= 1
        else:
            i += 1
        nuevo = (n - i) + (j + 1)
        assert nuevo == phi - 1        # Φ baja exactamente 1 por comparación
        phi = nuevo
    assert all(A[a][b] != x for a in range(n) for b in range(n))
    return None


def matriz_aleatoria(rng, n, rango):
    """Matriz con filas y columnas estrictamente crecientes: A[i][j] = acumulados aleatorios."""
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            base = max(A[i - 1][j] if i else 0, A[i][j - 1] if j else 0)
            A[i][j] = base + rng.randint(1, rango)
    return A


def es_ordenada(A):
    n = len(A)
    return all(A[i][j] < A[i][j + 1] for i in range(n) for j in range(n - 1)) and \
           all(A[i][j] < A[i + 1][j] for i in range(n - 1) for j in range(n))


class Adversario:
    """El adversario de las dos antidiagonales, con x = 0.
    - celdas con i + j < n - 1:  valor  i + j - n      (muy negativo, < x)
    - celdas con i + j = n - 1:  valor -1/2  ("<")     diagonal D1
    - celdas con i + j = n    :  valor +1/2  (">")     diagonal D2
    - celdas con i + j > n    :  valor  i + j          (muy positivo, > x)
    Nunca responde "=". Anota qué celdas de D1 y D2 se compararon."""
    def __init__(self, n):
        self.n, self.tocadas = n, set()

    def valor(self, i, j):
        n, d = self.n, i + j
        if d < n - 1: return d - n
        if d == n - 1: return -0.5
        if d == n: return 0.5
        return d

    def comparar(self, x, i, j):
        assert x == 0
        if i + j in (self.n - 1, self.n):
            self.tocadas.add((i, j))
        v = self.valor(i, j)
        return (x > v) - (x < v)

    def criticas(self):
        n = self.n
        return [(i, n - 1 - i) for i in range(n)] + [(i, n - i) for i in range(1, n)]

    def matriz(self, cambiar=None):
        """La matriz que el adversario tiene en mente; con cambiar=(i,j) esa celda pasa a ser x."""
        n = self.n
        A = [[self.valor(i, j) for j in range(n)] for i in range(n)]
        if cambiar:
            A[cambiar[0]][cambiar[1]] = 0
        return A


def pelear(algoritmo, n):
    """Corre `algoritmo` contra el adversario. Al final el adversario intenta llevarle la
    contraria: si la respuesta se puede contradecir, devuelve una matriz ordenada,
    consistente con todo lo que se respondió, donde esa respuesta es incorrecta."""
    adv = Adversario(n)
    res, comps = algoritmo(adv.comparar)
    if res is not None:
        # dijo "está" sin haber oído nunca "=": la matriz del adversario no tiene ningún 0
        B = adv.matriz()
    else:
        # dijo "no está": si se saltó una celda crítica, el adversario pone x ahí
        sin_mirar = [c for c in adv.criticas() if c not in adv.tocadas]
        if not sin_mirar:
            return comps, res, None         # respondió bien, pero pagó las 2n - 1
        B = adv.matriz(cambiar=sin_mirar[0])
    assert es_ordenada(B)
    # B es consistente con todas las respuestas que se dieron:
    assert all((0 > B[i][j]) - (0 < B[i][j]) == adv.comparar(0, i, j) for (i, j) in adv.tocadas)
    # y en B la respuesta del algoritmo es incorrecta:
    assert (B[res[0]][res[1]] != 0) if res is not None else any(0 in fila for fila in B)
    return comps, res, B


if __name__ == "__main__":
    rng = random.Random(2026)

    # 1. Correctitud: matrices aleatorias, invariante vigilado, x presente y ausente
    for _ in range(3000):
        n = rng.randint(0, 9)
        A = matriz_aleatoria(rng, n, rango=3)
        assert es_ordenada(A)
        valores = {v for fila in A for v in fila}
        for x in list(valores)[:5] + [rng.randint(-2, 3 * 2 * n + 3) for _ in range(5)]:
            p, c = escalera(A, x)
            assert (p is not None) == (x in valores)
            assert p is None or A[p[0]][p[1]] == x
            assert c <= 2 * n - 1 if n else c == 0
            assert escalera_vigilada(A, x) == p
    print("3000 matrices (n <= 9): correcto, invariante y potencial vigilados en cada paso")

    # 2. La escalera contra el adversario: hace exactamente 2n - 1 y no se deja engañar
    print(f"\n{'n':>5} {'comparaciones escalera':>23} {'cota 2n-1':>10}")
    for n in [1, 2, 3, 5, 10, 100, 1000]:
        comps, _, B = pelear(lambda cmp: escalera([[0] * n] * n, 0, cmp), n)
        assert B is None and comps == 2 * n - 1
        print(f"{n:>5} {comps:>23} {2 * n - 1:>10}")

    # 3. Algoritmos que hacen menos de 2n - 1 comparaciones: el adversario fabrica la matriz que los rompe
    def escalera_corta(cmp, n, k):
        """La escalera, pero se rinde tras k comparaciones."""
        i, j, c = 0, n - 1, 0
        while i < n and j >= 0 and c < k:
            c += 1
            r = cmp(0, i, j)
            if r == 0: return (i, j), c
            if r < 0: j -= 1
            else: i += 1
        return None, c

    def escalera_que_adivina(cmp, n, k):
        """La escalera, pero tras k comparaciones se rinde y dice "está" en la celda donde quedó."""
        i, j, c = 0, n - 1, 0
        while i < n and j >= 0 and c < k:
            c += 1
            r = cmp(0, i, j)
            if r == 0: return (i, j), c
            if r < 0: j -= 1
            else: i += 1
        return (min(i, n - 1), max(j, 0)), c

    def binaria_por_filas(cmp, n):
        """Búsqueda binaria en cada fila: n ⌈log2(n+1)⌉ comparaciones, más que 2n - 1, y correcta."""
        c = 0
        for i in range(n):
            lo, hi = 0, n
            while lo < hi:
                m = (lo + hi) // 2; c += 1
                r = cmp(0, i, m)
                if r == 0: return (i, m), c
                if r < 0: hi = m
                else: lo = m + 1
        return None, c

    def solo_diagonal(cmp, n):
        """Mira solo la antidiagonal principal (n comparaciones). Parece razonable; no lo es."""
        for i in range(n):
            if cmp(0, i, n - 1 - i) == 0:
                return (i, n - 1 - i), i + 1
        return None, n

    n = 8
    print(f"\nn = {n}:")
    for nombre, alg in [("escalera que se rinde en 2n-2", lambda c: escalera_corta(c, n, 2 * n - 2)),
                        ("escalera que adivina 'está'", lambda c: escalera_que_adivina(c, n, n)),
                        ("solo la antidiagonal", lambda c: solo_diagonal(c, n)),
                        ("búsqueda binaria por filas", lambda c: binaria_por_filas(c, n))]:
        comps, res, B = pelear(alg, n)
        if B is None:
            print(f"  {nombre:<32} {comps:>3} comparaciones: el adversario no lo engaña")
        elif res is not None:
            print(f"  {nombre:<32} {comps:>3} comparaciones: dice que está en {res}, pero la matriz del adversario no tiene ningún 0")
        else:
            p, _ = escalera(B, 0)
            print(f"  {nombre:<32} {comps:>3} comparaciones: dice 'no está', pero x = 0 está en {p}")
    _, _, B = pelear(lambda c: solo_diagonal(c, n), n)
    print("\nMatriz que rompe 'solo la antidiagonal' (x = 0; ±½ marcados como -h/+h):")
    for fila in B:
        print("  " + " ".join({-0.5: " -h", 0.5: " +h", 0: "  X"}.get(v, f"{v:>3}") for v in fila))

    # 4. Figuras: el recorrido de la escalera, y aparte las dos diagonales del adversario
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.patches import Rectangle
    except ImportError:
        print("(sin matplotlib: no se generan figuras)")
    else:
        n = 8
        A = matriz_aleatoria(random.Random(7), n, rango=4)
        x = 28                                   # no está: la escalera recorre todo su camino
        assert all(x not in fila for fila in A)
        camino, i, j = [], 0, n - 1
        while i < n and j >= 0:
            camino.append((i, j))
            if A[i][j] == x: break
            if x < A[i][j]: j -= 1
            else: i += 1
        fig, ax = plt.subplots(figsize=(5, 5))
        for a in range(n):
            for b in range(n):
                col = "#fde68a" if (a, b) in camino else "white"
                ax.add_patch(Rectangle((b, a), 1, 1, fc=col, ec="#999"))
                ax.text(b + .5, a + .5, A[a][b], ha="center", va="center", fontsize=9)
        ys, xs = zip(*[(a + .5, b + .5) for a, b in camino])
        ax.plot(xs, ys, "-", c="#b45309", lw=2, alpha=.7)
        ax.set_title(f"Escalera buscando x = {x} (no está): {len(camino)} comparaciones")
        ax.set_xlim(0, n); ax.set_ylim(n, 0); ax.set_aspect("equal"); ax.axis("off")
        fig.tight_layout()
        fig.savefig("ejercicio-06-escalera.png", dpi=150)

        fig, ax = plt.subplots(figsize=(5, 5))
        for a in range(n):
            for b in range(n):
                d = a + b
                col, txt = ("#bfdbfe", "<") if d < n - 1 else ("#fecaca", ">") if d > n else \
                           ("#2563eb", "−½") if d == n - 1 else ("#dc2626", "+½")
                ax.add_patch(Rectangle((b, a), 1, 1, fc=col, ec="#999"))
                ax.text(b + .5, a + .5, txt, ha="center", va="center", fontsize=9,
                        color="white" if d in (n - 1, n) else "#333")
        ax.set_title(f"Adversario (x = 0): 2n − 1 = {2 * n - 1} celdas críticas")
        ax.set_xlim(0, n); ax.set_ylim(n, 0); ax.set_aspect("equal"); ax.axis("off")
        fig.tight_layout()
        fig.savefig("ejercicio-06-adversario.png", dpi=150)
        print("\nfiguras: ejercicio-06-escalera.png, ejercicio-06-adversario.png")
