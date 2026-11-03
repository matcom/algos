"""Ejercicio 14 del Tema 1: el punto de rotación de un arreglo ordenado y rotado.

    python ejercicio-14.py

Imprime todas las tablas que cita ejercicio-14.md, corre las pruebas y regenera las
tres figuras (ejercicio-14-predicado.svg, ejercicio-14-arbol.svg y
ejercicio-14-errores.svg). Cada número que aparece en la prosa sale de aquí. Solo
necesita matplotlib.
"""

import math
import random
from functools import lru_cache

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt


# --------------------------------------------------------------------------
# 1. El modelo, los algoritmos y el adversario
# --------------------------------------------------------------------------

class Comparador:
    """El único acceso a los datos: comparar dos posiciones. Cuenta las preguntas."""

    def __init__(self, A):
        self.A, self.veces, self.preguntas = A, 0, []

    def greater(self, i, j):
        """¿A[i] > A[j]?"""
        self.veces += 1
        self.preguntas.append((i, j))
        return self.A[i] > self.A[j]

    def compare(self, i, j):
        """-1, 0 o 1, para la versión con repetidos."""
        self.veces += 1
        return (self.A[i] > self.A[j]) - (self.A[i] < self.A[j])


def rotado(B, k):
    """El arreglo ordenado B rotado para que su mínimo quede en la posición k."""
    n = len(B)
    return [B[(i - k) % n] for i in range(n)]


def brute_force(n, c):
    """Busca el único descenso A[i] > A[i+1]; si no hay, el arreglo no está rotado."""
    for i in range(n - 1):
        if c.greater(i, i + 1):
            return i + 1
    return 0


def rotation_point(n, c, referencia="ultimo"):
    """Búsqueda binaria del primer i con A[i] <= A[n-1]. referencia = "primero" es el
    error plantado de la sección 10: usa A[0] y busca el primer i con A[i] < A[0]."""
    lo, hi = 0, n - 1
    while lo < hi:
        m = (lo + hi) // 2
        if referencia == "ultimo":
            alto = c.greater(m, n - 1)               # A[m] > A[n-1]: m está antes de k
        else:
            alto = not c.greater(0, m)               # A[m] >= A[0]
        if alto:
            lo = m + 1
        else:
            hi = m
    return lo


def punto_vigilado(A):
    """El mismo algoritmo, comprobando el invariante (I) y el potencial en cada vuelta."""
    n, k = len(A), A.index(min(A))
    lo, hi = 0, n - 1
    vueltas = 0
    while lo < hi:
        assert all(A[i] > A[n - 1] for i in range(lo)) and A[hi] <= A[n - 1]
        assert lo <= k <= hi
        m = (lo + hi) // 2
        antes = hi - lo
        if A[m] > A[n - 1]:
            lo = m + 1
        else:
            hi = m
        assert hi - lo < antes
        vueltas += 1
    return lo, vueltas


def minimo_con_repetidos(n, c):
    """Para arreglos con repetidos: la referencia es A[hi], y si A[m] = A[hi] solo se
    puede descartar hi."""
    lo, hi = 0, n - 1
    while lo < hi:
        m = (lo + hi) // 2
        r = c.compare(m, hi)
        if r > 0:
            lo = m + 1
        elif r < 0:
            hi = m
        else:
            hi -= 1
    return lo


class Adversario:
    """No tiene arreglo: mantiene el conjunto de rotaciones compatibles con lo que ya
    contestó, y a cada pregunta contesta lo que deja más rotaciones vivas."""

    def __init__(self, n):
        self.vivas, self.veces, self.preguntas = set(range(n)), 0, []

    def greater(self, i, j):
        self.veces += 1
        self.preguntas.append((i, j))
        if i == j:
            return False
        a, b = min(i, j), max(i, j)
        # con a < b: A[a] > A[b] si y solo si el mínimo está en a+1..b
        si = {k for k in self.vivas if a < k <= b}
        no = self.vivas - si
        respuesta = len(si) > len(no)
        self.vivas = si if respuesta else no
        return respuesta if i < j else not respuesta


@lru_cache(maxsize=None)
def optimo(vivas, n):
    """El mejor peor caso de cualquier algoritmo de comparaciones, si las rotaciones
    todavía posibles son las del conjunto `vivas` (una máscara de bits)."""
    if vivas & (vivas - 1) == 0:
        return 0
    mejor = math.inf
    for a in range(n):
        for b in range(a + 1, n):
            T = ((1 << (b + 1)) - 1) ^ ((1 << (a + 1)) - 1)     # rotaciones a+1..b
            si, no = vivas & T, vivas & ~T
            if si and no:
                mejor = min(mejor, 1 + max(optimo(si, n), optimo(no, n)))
    return mejor


def seccion(titulo):
    print()
    print(titulo)
    print("-" * len(titulo))


def miles(x):
    return f"{x:,}".replace(",", " ")


def techo_log2(n):
    return (n - 1).bit_length()           # ceil(log2 n) para n >= 1


B12 = [3, 8, 11, 15, 22, 27, 31, 40, 46, 53, 61, 70]
K12 = 7


# --------------------------------------------------------------------------
# 2. Las tablas que cita la prosa
# --------------------------------------------------------------------------

def ejemplo_chico():
    seccion("§2. Ejemplo chico: n = 12, rotado para que el mínimo quede en 7")
    A = rotado(B12, K12)
    n = len(A)
    print("A =", " ".join(map(str, A)))
    print(f"A[i] <= A[11] = {A[-1]}:", " ".join("sí" if a <= A[-1] else "no" for a in A))
    print()
    print(f"{'paso':>4} {'lo':>3} {'hi':>3} {'m':>3} {'A[m]':>5}  respuesta")
    lo, hi, paso = 0, n - 1, 0
    while lo < hi:
        m = (lo + hi) // 2
        paso += 1
        alto = A[m] > A[-1]
        if alto:
            que = f"{A[m]} > {A[-1]}: k está después de m"
        else:
            que = f"{A[m]} <= {A[-1]}: k está en m o antes"
        print(f"{paso:>4} {lo:>3} {hi:>3} {m:>3} {A[m]:>5}  {que}")
        lo, hi = (m + 1, hi) if alto else (lo, m)
    c = Comparador(A)
    k = rotation_point(n, c)
    cb = Comparador(A)
    brute_force(n, cb)
    print(f"resultado: k = {k}, con {c.veces} comparaciones; la fuerza bruta usa "
          f"{cb.veces}; ceil(log2 12) = {techo_log2(n)}")
    return A


def costo_exacto():
    seccion("§6. El costo, para todo n hasta 300 y toda rotación")
    total = 0
    for n in range(1, 301):
        B = sorted(random.Random(n).sample(range(10 * n + 10), n))
        peor = 0
        for k in range(n):
            c = Comparador(rotado(B, k))
            assert rotation_point(n, c) == k
            assert c.veces in (techo_log2(n), n.bit_length() - 1)
            peor = max(peor, c.veces)
            total += 1
        assert peor == techo_log2(n)
        c = Comparador(rotado(B, 0))
        rotation_point(n, c)
        assert c.veces == techo_log2(n)
    print(f"{miles(total)} arreglos (n de 1 a 300, todas las rotaciones): todos "
          f"correctos, con floor(log2 n) o ceil(log2 n) comparaciones;")
    print("el peor caso es ceil(log2 n) para todo n, y lo alcanza el arreglo sin rotar")
    n = 1_000_000
    c = Comparador(list(range(n)))
    rotation_point(n, c)
    print(f"con n = 1 000 000 sin rotar: {c.veces} comparaciones; la fuerza bruta "
          f"haría {miles(n - 1)}")


def cota_minima():
    seccion("§7. La cota mínima: el adversario y todos los algoritmos")
    print(f"{'n':>8} {'algoritmo vs adversario':>24} {'fuerza bruta vs adversario':>27} "
          f"{'ceil(log2 n)':>13} {'óptimo por DP':>14}")
    for n in [1, 2, 3, 4, 5, 7, 8, 9, 12, 100, 1000, 100_000]:
        adv = Adversario(n)
        k = rotation_point(n, adv)
        assert adv.vivas == {k}
        bruta = "—"
        if n <= 1000:
            adv2 = Adversario(n)
            k2 = brute_force(n, adv2)
            assert adv2.vivas == {k2}
            bruta = str(adv2.veces)
        dp = str(optimo((1 << n) - 1, n)) if n <= 12 else "—"
        print(f"{n:>8} {adv.veces:>24} {bruta:>27} {techo_log2(n):>13} {dp:>14}")
    todos = all(optimo((1 << n) - 1, n) == techo_log2(n) for n in range(1, 13))
    print(f"DP sobre todos los algoritmos: óptimo = ceil(log2 n) para todo n <= 12: {todos}")


def arbol_de_decision(n=10):
    """Corre el algoritmo con cada rotación y guarda el camino de preguntas."""
    B = list(range(n))
    caminos = {}
    for k in range(n):
        A = rotado(B, k)
        c = Comparador(A)
        assert rotation_point(n, c) == k
        caminos[k] = [(i, A[i] > A[j]) for i, j in c.preguntas]
    return caminos


def romper():
    seccion("§8. Romper la cota: si se sabe que los valores son 0, 1, ..., n-1")
    for n, k in [(12, 7), (1000, 389), (10 ** 6, 123_456)]:
        A0 = (n - k) % n        # lo único que se lee: A[0] = (0 - k) mod n
        print(f"n = {miles(n)}, A[0] = {miles(A0)}: k = (n - A[0]) mod n = "
              f"{miles((n - A0) % n)}, con 0 comparaciones y una lectura")


def repetidos():
    seccion("§9. Con repetidos: rotaciones de 0 1 1 ... 1")
    print(f"{'n':>6} {'sin repetidos falla en':>23} {'con repetidos, peor':>20} "
          f"{'cota del adversario':>20}")
    for n in [8, 64, 512]:
        fallos, peor = 0, 0
        for k in range(n):
            A = rotado([0] + [1] * (n - 1), k)
            if rotation_point(n, Comparador(A)) != k:
                fallos += 1
            c = Comparador(A)
            assert minimo_con_repetidos(n, c) == k
            peor = max(peor, c.veces)
        print(f"{n:>6} {f'{fallos} de {n}':>23} {peor:>20} {math.ceil((n - 1) / 2):>20}")


def errores_plantados():
    seccion("§10. El error plantado: comparar con A[0] en vez de A[n-1]")
    rng = random.Random(10)

    def k_al_azar(nmax):
        def g():
            n = rng.randint(1, nmax)
            return n, rng.randrange(n)
        return g

    baterias = {
        "k al azar, n <= 10": k_al_azar(10),
        "k al azar, n <= 1000": k_al_azar(1000),
        "sin rotar": lambda: (rng.randint(2, 1000), 0),
    }
    tabla = {}
    print(f"{'batería':>22} {'casos':>6} {'con A[n-1]':>11} {'con A[0]':>9}")
    for nombre, g in baterias.items():
        casos = [g() for _ in range(2000)]
        malos = [0, 0]
        for n, k in casos:
            A = rotado(list(range(n)), k)
            for t, ref in enumerate(["ultimo", "primero"]):
                malos[t] += rotation_point(n, Comparador(A), ref) != k
        f = [100 * m / len(casos) for m in malos]
        tabla[nombre] = f
        print(f"{nombre:>22} {len(casos):>6} {f[0]:>10.1f}% {f[1]:>8.1f}%")
    # con n uniforme en 1..1000 y k uniforme en 0..n-1, un caso falla si y solo si
    # k = 0 y n >= 2 (el lema de la sección 10; la exhaustiva de abajo lo comprueba)
    p = sum(1 / m for m in range(2, 1001)) / 1000
    print(f"una batería de 100 casos como la de n <= 1000 no ve el error de A[0] con "
          f"probabilidad {(1 - p) ** 100:.2f}")
    fallos = set()
    for n in range(1, 60):
        for k in range(n):
            salida = rotation_point(n, Comparador(rotado(list(range(n)), k)), "primero")
            if salida != k:
                fallos.add((n, k, salida))
    assert fallos == {(n, 0, n - 1) for n in range(2, 60)}
    print(f"exhaustiva con n de 1 a 59: con A[0] falla en {len(fallos)} casos, los de "
          f"k = 0 y n >= 2, y devuelve n - 1")
    A = rotado(B12, 0)
    print(f"sobre A = {' '.join(map(str, A))}: con A[0] devuelve "
          f"{rotation_point(12, Comparador(A), 'primero')}, con A[n-1] devuelve "
          f"{rotation_point(12, Comparador(A))}")
    return tabla


# --------------------------------------------------------------------------
# 3. Pruebas
# --------------------------------------------------------------------------

def pruebas():
    seccion("Pruebas")
    comprobaciones = 0
    rng = random.Random(2026)

    # (a) el algoritmo contra la fuerza bruta y contra el mínimo, con valores al azar
    for _ in range(3000):
        n = rng.randint(1, 200)
        B = sorted(rng.sample(range(-10 ** 6, 10 ** 6), n))
        k = rng.randrange(n)
        A = rotado(B, k)
        assert rotation_point(n, Comparador(A)) == brute_force(n, Comparador(A)) == k
        assert A[k] == min(A)
        comprobaciones += 2

    # (b) el invariante (I) y el potencial, vigilados en cada vuelta
    vueltas = 0
    for _ in range(3000):
        n = rng.randint(1, 120)
        A = rotado(sorted(rng.sample(range(10 ** 5), n)), rng.randrange(n))
        k, v = punto_vigilado(A)
        assert k == A.index(min(A))
        vueltas += v
        comprobaciones += 1

    # (c) con repetidos, la versión que los tolera devuelve una posición del mínimo
    for _ in range(3000):
        n = rng.randint(1, 60)
        B = sorted(rng.randint(0, 5) for _ in range(n))
        A = rotado(B, rng.randrange(n))
        assert A[minimo_con_repetidos(n, Comparador(A))] == min(A)
        comprobaciones += 1

    print(f"{miles(comprobaciones)} comprobaciones ({miles(vueltas)} vueltas vigiladas), "
          f"0 fallos")


# --------------------------------------------------------------------------
# 4. Figuras
# --------------------------------------------------------------------------

TINTA, APAGADO, REGLA = "#1a1a1a", "#6b7280", "#d8dce3"
ACENTO, OSCURO, CALIDO, ALARMA = "#0891b2", "#0e7490", "#b45309", "#be123c"


def _estilo():
    plt.rcParams.update({
        "font.size": 9, "axes.edgecolor": APAGADO, "axes.labelcolor": TINTA,
        "xtick.color": APAGADO, "ytick.color": APAGADO,
        "figure.facecolor": "white", "svg.hashsalt": "ejercicio-14",
    })


def _guardar(fig, nombre):
    fig.tight_layout()
    fig.savefig(nombre, metadata={"Date": None})
    plt.close(fig)


def figura_predicado(A):
    n = len(A)
    fig, (ax, ax2) = plt.subplots(2, 1, figsize=(6.4, 4.0), sharex=True,
                                  gridspec_kw={"height_ratios": [2.2, 1.3]})
    colores = [CALIDO if a > A[-1] else OSCURO for a in A]
    ax.bar(range(n), A, color=colores, width=0.7)
    for i, a in enumerate(A):
        ax.text(i, a + 1.5, str(a), ha="center", fontsize=7, color=TINTA)
    ax.axhline(A[-1], color=ALARMA, lw=1, ls="--")
    ax.text(7.6, A[-1] + 2.5, f"A[{n - 1}] = {A[-1]}", color=ALARMA, fontsize=8,
            ha="left")
    ax.text(0, 74, "A[i] > A[n−1]: antes de k", color=CALIDO, fontsize=8)
    ax.text(7, 74, "A[i] ≤ A[n−1]: desde k", color=OSCURO, fontsize=8)
    ax.set_ylim(0, 82)
    ax.set_yticks([])
    ax.spines[["top", "right", "left"]].set_visible(False)
    lo, hi, fila = 0, n - 1, 0
    while True:
        ax2.plot([lo - 0.35, hi + 0.35], [-fila, -fila], color=ACENTO, lw=5,
                 solid_capstyle="butt", alpha=0.45)
        if lo >= hi:
            ax2.text(hi + 0.6, -fila, f"k = {lo}", va="center", fontsize=8, color=ALARMA)
            break
        m = (lo + hi) // 2
        ax2.plot([m], [-fila], "v", color=TINTA, ms=6)
        ax2.text(-0.9, -fila, f"paso {fila + 1}", va="center", ha="right", fontsize=7,
                 color=APAGADO)
        lo, hi = (m + 1, hi) if A[m] > A[-1] else (lo, m)
        fila += 1
    ax2.set_ylim(-fila - 0.6, 0.6)
    ax2.set_yticks([])
    ax2.set_xticks(range(n))
    ax2.set_xlabel("posición i")
    ax2.spines[["top", "right", "left"]].set_visible(False)
    _guardar(fig, "ejercicio-14-predicado.svg")


def figura_arbol(caminos, n=10):
    """Las hojas quedan en orden k = 0..n-1 de izquierda a derecha."""
    fig, ax = plt.subplots(figsize=(6.6, 3.0))
    nodos = {}           # prefijo de respuestas -> [m, rotaciones que pasan por ahí]
    for k, resp in caminos.items():
        for d in range(len(resp)):
            pref = tuple(r for _, r in resp[:d])
            nodos.setdefault(pref, [resp[d][0], []])[1].append(k)

    def xy(pref):
        hojas = nodos[pref][1]
        return sum(hojas) / len(hojas), -len(pref)

    for pref, (m, hojas) in nodos.items():
        x, y = xy(pref)
        for r in (False, True):
            hijo = pref + (r,)
            if hijo in nodos:
                hx, hy = xy(hijo)
            else:
                k = next(k for k in hojas if tuple(rr for _, rr in caminos[k]) == hijo)
                hx, hy = k, -len(caminos[k])
                ax.text(hx, hy - 0.1, f"k={k}", ha="center", va="top", fontsize=7,
                        color=ALARMA)
            ax.plot([x, hx], [y, hy], color=REGLA, lw=1, zorder=1)
            ax.text((x + hx) / 2 + (0.2 if r else -0.2), (y + hy) / 2,
                    ">" if r else "≤", fontsize=7, color=APAGADO, ha="center",
                    va="center")
        ax.text(x, y, f"A[{m}]:A[{n - 1}]", ha="center", va="center", fontsize=6.5,
                zorder=2, bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=OSCURO,
                                    lw=0.9))
    ax.set_ylim(-4.6, 0.4)
    ax.set_xlim(-0.8, n - 0.2)
    ax.axis("off")
    _guardar(fig, "ejercicio-14-arbol.svg")


def figura_errores(tabla):
    fig, ax = plt.subplots(figsize=(6.0, 2.8))
    nombres = list(tabla)
    ancho = 0.36
    for k, (etiqueta, color) in enumerate([("referencia A[n−1]", OSCURO),
                                           ("referencia A[0]", ALARMA)]):
        alturas = [tabla[b][k] for b in nombres]
        pos = [i + (k - 0.5) * ancho for i in range(len(nombres))]
        ax.bar(pos, alturas, ancho, color=color, label=etiqueta)
        for xx, h in zip(pos, alturas):
            ax.text(xx, h + 1.5, f"{h:.1f}", ha="center", fontsize=7, color=color)
    ax.set_xticks(range(len(nombres)))
    ax.set_xticklabels(nombres, fontsize=8)
    ax.set_ylabel("% de respuestas mal")
    ax.set_ylim(0, 112)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color=REGLA, lw=0.6)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    _guardar(fig, "ejercicio-14-errores.svg")


if __name__ == "__main__":
    A = ejemplo_chico()
    costo_exacto()
    cota_minima()
    romper()
    repetidos()
    tabla = errores_plantados()
    pruebas()
    _estilo()
    figura_predicado(A)
    figura_arbol(arbol_de_decision())
    figura_errores(tabla)
    print("\nfiguras: ejercicio-14-predicado.svg, ejercicio-14-arbol.svg, "
          "ejercicio-14-errores.svg")
