"""Ejercicio 6 del Tema 1: buscar x en una matriz n x n con filas y columnas crecientes.

La búsqueda en escalera (desde la esquina superior derecha), su invariante y la
cota del adversario, que resulta exacta: 2n - 1 comparaciones.

Uso:
    python ejercicio_06.py             imprime las tablas del informe
    python ejercicio_06.py --figuras   además regenera la figura

Las pruebas están en test_ejercicio_06.py.
"""

import itertools
import random
import sys
from functools import lru_cache
from pathlib import Path


# ---------------------------------------------------------------------------
# 1. La búsqueda en escalera
# ---------------------------------------------------------------------------

def escalera(M, x, camino=None, vigilar=False):
    """Decide si x está en M. Compara x con una celda por vuelta (tres salidas).

    Devuelve (True, (i, j)) o (False, None). Si se pasa `camino`, anota las celdas
    comparadas.
    """
    n = len(M)
    i, j = 0, n - 1
    while i < n and j >= 0:
        if vigilar:
            assert all(M[r][c] != x for r in range(n) for c in range(n) if r < i or c > j)
        if camino is not None:
            camino.append((i, j))
        if M[i][j] == x:
            return True, (i, j)
        if M[i][j] > x:
            j -= 1                      # la columna j, de la fila i para abajo, es > x
        else:
            i += 1                      # la fila i, de la columna j para la izquierda, es < x
    return False, None


def busqueda_por_filas(M, x, camino=None):
    """Alternativa: búsqueda binaria en cada fila. n·⌈log2(n+1)⌉ comparaciones."""
    for i, fila in enumerate(M):
        lo, hi = 0, len(fila)
        while lo < hi:
            m = (lo + hi) // 2
            if camino is not None:
                camino.append((i, m))
            if fila[m] == x:
                return True, (i, m)
            if fila[m] < x:
                lo = m + 1
            else:
                hi = m
    return False, None


def esta_ordenada(M):
    n = len(M)
    return (all(M[i][j] < M[i][j + 1] for i in range(n) for j in range(n - 1)) and
            all(M[i][j] < M[i + 1][j] for i in range(n - 1) for j in range(n)))


def matriz_al_azar(n, rng, salto=4):
    """Filas y columnas estrictamente crecientes: M[i][j] = max(arriba, izquierda) + salto al azar."""
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            base = max(M[i - 1][j] if i else 0, M[i][j - 1] if j else 0)
            M[i][j] = base + rng.randint(1, salto)
    return M


# ---------------------------------------------------------------------------
# 2. El adversario: la escalera de 2n - 1 celdas
# ---------------------------------------------------------------------------

def escalera_del_adversario(n):
    """Las celdas de D0 (i + j = n - 1) y D1 (i + j = n), en el orden del camino."""
    celdas = []
    for i in range(n):
        celdas.append((i, n - 1 - i))           # D0
        if i + 1 < n:
            celdas.append((i + 1, n - 1 - i))   # D1
    return celdas


def matriz_del_adversario(n, x=None, poner=None):
    """Arriba de D0 valores < x, D0 = x - 1, D1 = x + 1, abajo de D1 valores > x.

    Con x = 2n las celdas fuera de la escalera valen 2(i + j) - 1 arriba de D0 y
    2(i + j) + 1 abajo de D1. Si `poner` es una
    celda de la escalera, esa celda pasa a valer x: la matriz sigue ordenada y
    ahora contiene a x.
    """
    x = 2 * n if x is None else x
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            s = i + j
            if s < n - 1:
                M[i][j] = 2 * s - 2 * n + x - 1          # < x - 1 y creciente
            elif s == n - 1:
                M[i][j] = x - 1
            elif s == n:
                M[i][j] = x + 1
            else:
                M[i][j] = 2 * s - 2 * n + x + 1          # > x + 1 y creciente
    if poner is not None:
        i, j = poner
        M[i][j] = x
    return M, x


# ---------------------------------------------------------------------------
# 3. El óptimo exacto por fuerza bruta (juego contra todos los patrones de signos)
# ---------------------------------------------------------------------------

def patrones(n):
    """Todos los patrones de signos (-1, 0, 1) de M - x posibles para una matriz ordenada.

    Filas y columnas no decrecientes en el signo, y sin dos ceros vecinos (los
    valores son estrictamente crecientes, así que un 0 no puede repetirse en su
    fila ni en su columna).
    """
    resultado = []
    for valores in itertools.product((-1, 0, 1), repeat=n * n):
        P = [valores[k * n:(k + 1) * n] for k in range(n)]
        ok = True
        for i in range(n):
            for j in range(n):
                if j + 1 < n and (P[i][j] > P[i][j + 1] or P[i][j] == P[i][j + 1] == 0):
                    ok = False
                if i + 1 < n and (P[i][j] > P[i + 1][j] or P[i][j] == P[i + 1][j] == 0):
                    ok = False
        if ok:
            resultado.append(valores)
    return resultado


def optimo_exacto(n):
    """Profundidad mínima de un árbol de decisión que decide si hay un 0 (x está)."""
    todos = patrones(n)
    celdas = range(n * n)

    @lru_cache(maxsize=None)
    def costo(indices):
        tiene = {0 in todos[k] for k in indices}
        if len(tiene) <= 1:
            return 0
        mejor = None
        for c in celdas:
            grupos = {}
            for k in indices:
                grupos.setdefault(todos[k][c], []).append(k)
            if len(grupos) == 1:
                continue
            peor = max(costo(tuple(g)) for g in grupos.values())
            if mejor is None or 1 + peor < mejor:
                mejor = 1 + peor
        return mejor

    return costo(tuple(range(len(todos)))), len(todos)


# ---------------------------------------------------------------------------
# 4. Tablas
# ---------------------------------------------------------------------------

def tabla_adversario():
    print("Tabla 1. En la matriz del adversario la escalera mira exactamente las 2n - 1 celdas")
    print(f"{'n':>5} {'comparaciones':>14} {'2n - 1':>7} {'mira todas las de la escalera':>30}"
          f" {'cada celda puede ser x':>23}")
    for n in [1, 2, 3, 5, 10, 100, 1000]:
        M, x = matriz_del_adversario(n)
        camino = []
        escalera(M, x, camino)
        celdas = escalera_del_adversario(n)
        variantes_ok = all(esta_ordenada(matriz_del_adversario(n, poner=c)[0]) for c in celdas) \
            if n <= 100 else "—"
        print(f"{n:>5} {len(camino):>14} {2 * n - 1:>7} {str(camino == celdas):>30} {str(variantes_ok):>23}")
    print()


def tabla_optimo():
    print("Tabla 2. Óptimo exacto por fuerza bruta (todos los patrones de signos)")
    for n in [1, 2, 3]:
        opt, cuantos = optimo_exacto(n)
        print(f"  n = {n}: {cuantos} patrones posibles, óptimo = {opt}, 2n - 1 = {2 * n - 1}")
    print()


def tabla_comparaciones():
    print("Tabla 3. Peor caso medido sobre matrices al azar (x presente y ausente)")
    print(f"{'n':>6} {'escalera':>9} {'2n - 1':>7} {'binaria por filas':>18} {'n⌈log2(n+1)⌉':>14}")
    rng = random.Random(6)
    for n in [4, 16, 64, 256]:
        peor_e = peor_f = 0
        for _ in range(60):
            M = matriz_al_azar(n, rng)
            for x in [rng.choice(rng.choice(M)), rng.randint(0, M[-1][-1] + 1)]:
                c1, c2 = [], []
                escalera(M, x, c1)
                busqueda_por_filas(M, x, c2)
                peor_e, peor_f = max(peor_e, len(c1)), max(peor_f, len(c2))
        print(f"{n:>6} {peor_e:>9} {2 * n - 1:>7} {peor_f:>18} {n * n.bit_length():>14}")
    print()


# ---------------------------------------------------------------------------
# 5. Figura
# ---------------------------------------------------------------------------

AZUL, NARANJA, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
TINTA, TINTA_2, TENUE, SUPERFICIE = "#0b0b0b", "#52514e", "#898781", "#fcfcfb"


def figura(destino):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches

    plt.rcParams.update({"font.family": ["Segoe UI", "DejaVu Sans"], "font.size": 10,
                         "axes.titlecolor": TINTA, "axes.titlesize": 12, "axes.titleweight": "bold",
                         "axes.titlelocation": "left", "figure.facecolor": SUPERFICIE,
                         "savefig.dpi": 150, "savefig.bbox": "tight"})
    fig, (izq, der) = plt.subplots(1, 2, figsize=(11, 5.4))

    # Izquierda: la búsqueda en una matriz al azar, con lo descartado.
    rng = random.Random(3)
    n = 7
    M = matriz_al_azar(n, rng, salto=6)
    x = M[4][2]
    camino = []
    escalera(M, x, camino)
    descartadas = {}
    i, j = 0, n - 1
    for (a, b) in camino[:-1]:
        if M[a][b] > x:
            for r in range(a, n):
                descartadas.setdefault((r, b), "mayor")
        else:
            for c in range(0, b + 1):
                descartadas.setdefault((a, c), "menor")
    for r in range(n):
        for c in range(n):
            tipo = descartadas.get((r, c))
            color = {"mayor": "#fbe0d4", "menor": "#d6efe5"}.get(tipo, SUPERFICIE)
            izq.add_patch(patches.Rectangle((c, -r), 0.95, 0.95, facecolor=color, edgecolor="#c3c2b7"))
            izq.text(c + 0.47, -r + 0.47, str(M[r][c]), ha="center", va="center", fontsize=9,
                     color=TINTA if tipo is None else TINTA_2)
    for k, (a, b) in enumerate(camino):
        izq.add_patch(patches.Rectangle((b, -a), 0.95, 0.95, fill=False, edgecolor=AZUL, linewidth=2.2))
        izq.text(b + 0.82, -a + 0.82, str(k + 1), ha="center", va="center", fontsize=7, color=AZUL)
    izq.set_xlim(-0.1, n + 0.1)
    izq.set_ylim(-n + 0.85, 1.1)
    izq.set_aspect("equal")
    izq.axis("off")
    izq.set_title(f"Buscar x = {x}: {len(camino)} comparaciones")
    izq.text(0, -n + 0.55, "verde: fila descartada (todo < x)   naranja: columna descartada (todo > x)",
             fontsize=8, color=TINTA_2)

    # Derecha: la matriz del adversario.
    n = 7
    M, x = matriz_del_adversario(n)
    celdas = set(escalera_del_adversario(n))
    for r in range(n):
        for c in range(n):
            s = r + c
            color = SUPERFICIE
            if s == n - 1:
                color = "#cfe0f6"
            elif s == n:
                color = "#fbe0d4"
            der.add_patch(patches.Rectangle((c, -r), 0.95, 0.95, facecolor=color, edgecolor="#c3c2b7"))
            der.text(c + 0.47, -r + 0.47, str(M[r][c]), ha="center", va="center", fontsize=9,
                     color=TINTA if (r, c) in celdas else TENUE)
    camino = escalera_del_adversario(n)
    xs = [c + 0.47 for r, c in camino]
    ys = [-r + 0.47 for r, c in camino]
    der.plot(xs, ys, color=AZUL, linewidth=5, alpha=0.18, solid_capstyle="round")
    der.set_xlim(-0.1, n + 0.1)
    der.set_ylim(-n + 0.85, 1.1)
    der.set_aspect("equal")
    der.axis("off")
    der.set_title(f"El adversario, x = {x}: 2n − 1 = {2 * n - 1} celdas libres")
    der.text(0, -n + 0.55, "azul: D₀ = x − 1    naranja: D₁ = x + 1    cualquiera puede valer x",
             fontsize=8, color=TINTA_2)
    destino.mkdir(exist_ok=True)
    fig.savefig(destino / "ejercicio-06-escalera.png")
    plt.close(fig)
    print(f"figura escrita en {destino}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    tabla_adversario()
    tabla_optimo()
    tabla_comparaciones()
    if "--figuras" in sys.argv:
        figura(Path(__file__).resolve().parent.parent / "figuras")
