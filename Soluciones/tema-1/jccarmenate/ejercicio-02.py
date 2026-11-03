"""Ejercicio 2 del Tema 1: invariante, potencial y cota de información de la búsqueda
binaria.

    python ejercicio-02.py

Imprime todas las tablas que cita ejercicio-02.md, corre las pruebas y regenera las
tres figuras (ejercicio-02-arbol.svg, ejercicio-02-testigo.svg y
ejercicio-02-errores.svg). Cada número que aparece en la prosa sale de aquí. Solo
necesita matplotlib.
"""

import math
import random

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt


# --------------------------------------------------------------------------
# 1. El algoritmo
# --------------------------------------------------------------------------

class Comparador:
    """Compara x con un elemento del arreglo: -1 si x es menor, 0 si es igual, 1 si es
    mayor. Cuenta cuántas veces se le preguntó, que es el costo en el modelo."""

    def __init__(self):
        self.veces = 0

    def __call__(self, x, y):
        self.veces += 1
        return (x > y) - (x < y)


def binary_search(A, x, compare):
    """A ordenado de forma no decreciente. Devuelve ("está", i) con A[i] == x, o
    ("hueco", g) si x no está, donde g es la cantidad de elementos menores que x."""
    lo, hi = 0, len(A)
    while lo < hi:
        m = (lo + hi) // 2
        r = compare(x, A[m])
        if r == 0:
            return ("está", m)
        if r < 0:
            hi = m
        else:
            lo = m + 1
    return ("hueco", lo)


def correcta(A, x, resultado):
    # el oráculo: mirar el arreglo entero
    tipo, i = resultado
    if tipo == "está":
        return 0 <= i < len(A) and A[i] == x
    if tipo == "hueco":
        return x not in A and i == sum(a < x for a in A)
    return False                                   # "no termina"


def bits(n):
    # cantidad de bits de n; para n >= 1 es floor(log2 n) + 1 = ceil(log2(n + 1))
    return n.bit_length()


def techo_log2(m):
    # ceil(log2 m) para m >= 1, sin flotantes: 2^(k-1) < m <= 2^k
    return (m - 1).bit_length()


def techo_log3(m):
    k, p = 0, 1
    while p < m:
        k, p = k + 1, 3 * p
    return k


def seccion(titulo):
    print()
    print(titulo)
    print("-" * len(titulo))


def miles(x):
    return f"{x:,}".replace(",", " ")


# --------------------------------------------------------------------------
# 2. Las tablas que cita la prosa
# --------------------------------------------------------------------------

EJEMPLO = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]


def traza(A, x):
    lo, hi = 0, len(A)
    print(f"x = {x}")
    print(f"{'paso':>4} {'lo':>3} {'hi':>3} {'hi - lo':>7} {'bits':>4} {'m':>3} "
          f"{'A[m]':>5}  respuesta")
    paso = 0
    while lo < hi:
        paso += 1
        m = (lo + hi) // 2
        signo = "<" if x < A[m] else "=" if x == A[m] else ">"
        print(f"{paso:>4} {lo:>3} {hi:>3} {hi - lo:>7} {bits(hi - lo):>4} {m:>3} "
              f"{A[m]:>5}  x {signo} {A[m]}")
        if x == A[m]:
            print(f"resultado: está en la posición {m}, con {paso} comparaciones")
            return
        if x < A[m]:
            hi = m
        else:
            lo = m + 1
    print(f"{'':>4} {lo:>3} {hi:>3} {hi - lo:>7} {bits(hi - lo):>4}")
    print(f"resultado: no está, cae en el hueco {lo}, con {paso} comparaciones")


def ejemplo_chico():
    seccion("§2. Ejemplo chico: A = " + " ".join(map(str, EJEMPLO)))
    traza(EJEMPLO, 50)
    print()
    traza(EJEMPLO, 16)


def busqueda_vigilada(A, x):
    """La búsqueda binaria con el invariante y los dos potenciales vigilados por
    assert en cada vuelta. Devuelve (resultado, vueltas)."""
    lo, hi, vueltas = 0, len(A), 0
    while True:
        assert 0 <= lo <= hi <= len(A)
        assert all(a < x for a in A[:lo]) and all(a > x for a in A[hi:])
        if lo >= hi:
            return ("hueco", lo), vueltas
        vueltas += 1
        antes = hi - lo
        m = (lo + hi) // 2
        assert lo <= m < hi                        # m cae dentro de la ventana
        if x == A[m]:
            return ("está", m), vueltas
        if x < A[m]:
            hi = m
        else:
            lo = m + 1
        assert hi - lo < antes                     # baja el potencial hi - lo
        assert bits(hi - lo) <= bits(antes) - 1    # y su cantidad de bits baja en 1
        assert vueltas <= bits(len(A))


def invariante_vigilado():
    seccion("§4. El invariante y los potenciales, vigilados con assert")
    rng = random.Random(4)
    busquedas = vueltas = 0
    for _ in range(20_000):
        A = sorted(rng.randrange(12) for _ in range(rng.randint(0, 20)))
        x = rng.randint(-1, 12)
        resultado, v = busqueda_vigilada(A, x)
        assert correcta(A, x, resultado)
        busquedas += 1
        vueltas += v
    print(f"{miles(busquedas)} búsquedas sobre arreglos ordenados con repetidos, "
          f"{miles(vueltas)} vueltas vigiladas, 0 fallos")

    # sin la precondición: arreglos en orden al azar
    rotos = mal = 0
    pruebas = 20_000
    for _ in range(pruebas):
        A = [rng.randrange(12) for _ in range(rng.randint(1, 20))]
        x = rng.choice(A) if rng.random() < 0.5 else rng.randint(-1, 12)
        try:
            busqueda_vigilada(A, x)
        except AssertionError:
            rotos += 1
        mal += not correcta(A, x, binary_search(A, x, Comparador()))
    print(f"sobre {miles(pruebas)} arreglos en orden al azar: el invariante se rompe "
          f"en {100 * rotos / pruebas:.1f}% de las búsquedas y la respuesta está "
          f"mal en {100 * mal / pruebas:.1f}%")


def peor_caso_exhaustivo(n):
    """Corre la búsqueda sobre los 2n + 1 resultados posibles de A = 2, 4, ..., 2n: los
    x pares están en el arreglo y los impares caen en cada uno de los n + 1 huecos."""
    A = list(range(2, 2 * n + 1, 2))
    peor = 0
    for x in range(1, 2 * n + 2):
        c = Comparador()
        assert correcta(A, x, binary_search(A, x, c))
        peor = max(peor, c.veces)
    return peor


def optimo_por_dp(N):
    """opt[s] = el menor peor caso de CUALQUIER algoritmo de comparaciones cuando quedan
    s candidatos. Comparar con el candidato j deja j a la izquierda y s - 1 - j a la
    derecha, y el '=' termina. Comparar fuera de la ventana no aporta nada."""
    opt = [0] * (N + 1)
    for s in range(1, N + 1):
        opt[s] = 1 + min(max(opt[j], opt[s - 1 - j]) for j in range(s))
    return opt


def peor_caso():
    seccion("§5 y §6. Peor caso de la búsqueda binaria, cota y óptimo")
    opt = optimo_por_dp(1000)
    print(f"{'n':>8} {'peor caso medido':>17} {'ceil(log2(n+1))':>16} "
          f"{'óptimo por DP':>14}")
    for n in [1, 2, 3, 4, 7, 8, 10, 15, 16, 100, 255, 256, 1000]:
        print(f"{n:>8} {peor_caso_exhaustivo(n):>17} {techo_log2(n + 1):>16} "
              f"{opt[n]:>14}")
    for n in [10**4, 10**6]:
        A = list(range(2, 2 * n + 1, 2))
        c = Comparador()
        binary_search(A, 0, c)                  # x menor que todos
        print(f"{n:>8} {c.veces:>17} {techo_log2(n + 1):>16} {'—':>14}")
    total = sum(2 * n + 1 for n in range(301))
    assert all(peor_caso_exhaustivo(n) == techo_log2(n + 1) for n in range(301))
    assert all(opt[n] == techo_log2(n + 1) for n in range(1001))
    print(f"n de 0 a 300, todos los resultados posibles: {miles(total)} búsquedas, "
          f"todas correctas, peor caso = ceil(log2(n+1)) en los 301 valores")
    print("DP sobre todos los algoritmos: óptimo = ceil(log2(n+1)) para todo n <= 1000")
    n = 10**6
    A = list(range(2, 2 * n + 1, 2))
    c = Comparador()
    binary_search(A, 0, c)
    print(f"con n = {miles(n)}: x menor que todos usa {c.veces} comparaciones = "
          f"bits de n; una búsqueda lineal usaría hasta {miles(n)}")


def cuenta_ingenua():
    seccion("§6. La cuenta ingenua contra la cuenta por huecos")
    print(f"{'n':>9} {'ceil(log3(2n+1))':>17} {'ceil(log2(n+1))':>16}")
    for n in [10, 1000, 10**6]:
        print(f"{n:>9} {techo_log3(2 * n + 1):>17} {techo_log2(n + 1):>16}")


def arbol_de_decision(n):
    """Corre la búsqueda binaria con un valor de cada hueco, x = 2g + 1, y pega los
    caminos en un árbol: cada nodo interno es la posición con la que compara."""
    A = list(range(2, 2 * n + 1, 2))
    raiz = {}
    for x in range(1, 2 * n + 2, 2):
        camino = []

        def compare(x, y):
            r = (x > y) - (x < y)
            camino.append((A.index(y), r))
            return r

        resultado = binary_search(A, x, compare)
        nodo = raiz
        for j, r in camino:
            assert nodo.setdefault("pos", j) == j   # dos caminos coinciden donde se cruzan
            nodo = nodo.setdefault(r, {})
        nodo["hoja"] = resultado
    return raiz


def hojas_de_hueco(arbol, prof=0):
    if "hoja" in arbol:
        return [(arbol["hoja"][1], prof)] if arbol["hoja"][0] == "hueco" else []
    return hojas_de_hueco(arbol[-1], prof + 1) + hojas_de_hueco(arbol[1], prof + 1)


def arbol_n10():
    seccion("§6. El árbol de decisión para n = 10")
    arbol = arbol_de_decision(10)
    hojas = hojas_de_hueco(arbol)
    print(f"hojas de hueco: {len(hojas)}, todas distintas: "
          f"{len({g for g, _ in hojas}) == len(hojas)}")
    print("profundidad de cada hueco: " + " ".join(f"h{g}:{p}" for g, p in sorted(hojas)))
    print(f"altura: {max(p for _, p in hojas)},  ceil(log2 11) = {techo_log2(11)}")


# --------------------------------------------------------------------------
# 3. Los errores plantados
# --------------------------------------------------------------------------

VARIANTES = ["correcta", "lo = m", "hi = m - 1"]


def busqueda_variante(A, x, variante):
    lo, hi, vueltas = 0, len(A), 0
    while lo < hi:
        vueltas += 1
        if vueltas > 2 * len(A) + 5:
            return ("no termina", None)
        m = (lo + hi) // 2
        if x == A[m]:
            return ("está", m)
        if x < A[m]:
            hi = m - 1 if variante == "hi = m - 1" else m
        else:
            lo = m if variante == "lo = m" else m + 1
    return ("hueco", lo)


def _arreglo(rng):
    return sorted(rng.sample(range(100), rng.randint(1, 15)))


def _presente(rng):
    A = _arreglo(rng)
    return A, rng.choice(A)


def _ausente(rng):
    A = _arreglo(rng)
    return A, rng.choice([v for v in range(-1, 101) if v not in A])


def _al_azar(rng):
    return _arreglo(rng), rng.randint(-1, 100)


GENERADORES = {"x presente": _presente, "x ausente": _ausente, "x al azar": _al_azar}


def errores_plantados():
    seccion("§7. Dos errores plantados contra cuatro baterías de pruebas")
    rng = random.Random(7)
    baterias = {nombre: [g(rng) for _ in range(4000)] for nombre, g in GENERADORES.items()}
    baterias["exhaustivo, n <= 6"] = [(list(range(2, 2 * n + 1, 2)), x)
                                      for n in range(7) for x in range(1, 2 * n + 2)]
    fallos = {}
    print(f"{'batería':>19} {'casos':>6} " + " ".join(f"{v:>11}" for v in VARIANTES))
    for nombre, casos in baterias.items():
        fila = []
        for v in VARIANTES:
            malos = sum(not correcta(A, x, busqueda_variante(A, x, v)) for A, x in casos)
            fila.append(100 * malos / len(casos))
        fallos[nombre] = fila
        print(f"{nombre:>19} {len(casos):>6} " + " ".join(f"{f:>10.1f}%" for f in fila))

    # cómo falla cada una
    todos = [caso for casos in baterias.values() for caso in casos]
    cuelga = sum(busqueda_variante(A, x, "lo = m")[0] == "no termina"
                 for A, x in baterias["x ausente"])
    mal_y_termina = sum(busqueda_variante(A, x, "lo = m")[0] != "no termina"
                        and not correcta(A, x, busqueda_variante(A, x, "lo = m"))
                        for A, x in todos)
    predicho = sum((busqueda_variante(A, x, "lo = m")[0] == "no termina")
                   == (x not in A and x > A[0]) for A, x in todos if A)
    print(f"lo = m con x ausente: {miles(cuelga)} de 4 000 no terminan")
    print(f"lo = m, en las cuatro baterías: {mal_y_termina} respuestas equivocadas que "
          f"terminan; 'no termina si y solo si x no está y x > A[0]' se cumple en "
          f"{miles(predicho)} de {miles(sum(1 for A, _ in todos if A))} casos")
    A = list(range(2, 21, 2))
    colgados = [g for g in range(11) if busqueda_variante(A, 2 * g + 1, "lo = m")[0]
                == "no termina"]
    print(f"con A = 2, 4, ..., 20, lo = m no termina en los huecos "
          f"{', '.join(map(str, colgados))}")
    mal_presente = [(A, x) for A, x in baterias["x presente"]
                    if not correcta(A, x, busqueda_variante(A, x, "hi = m - 1"))]
    tipos = {busqueda_variante(A, x, "hi = m - 1")[0] for A, x in mal_presente}
    print(f"hi = m - 1 con x presente: cuando falla, contesta {sorted(tipos)}")
    return fallos


# --------------------------------------------------------------------------
# 4. Comparaciones de dos vías
# --------------------------------------------------------------------------

def two_way_binary_search(A, x, less):
    """Solo pregunta 'a < b?'. El ciclo busca la cantidad de elementos menores que x,
    y una última pregunta decide si x está."""
    lo, hi = 0, len(A)
    while lo < hi:                       # invariante: A[:lo] < x <= A[hi:]
        m = (lo + hi) // 2
        if less(A[m], x):
            lo = m + 1
        else:
            hi = m
    if lo < len(A) and not less(x, A[lo]):
        return ("está", lo)
    return ("hueco", lo)


class Menor:
    def __init__(self):
        self.veces = 0

    def __call__(self, a, b):
        self.veces += 1
        return a < b


def dos_vias():
    seccion("§8. Si cada pregunta solo contesta sí o no")
    print(f"{'n':>6} {'peor caso medido':>17} {'ceil(log2(2n+1))':>17} "
          f"{'ceil(log2(n+1)) + 1':>20}")
    for n in [1, 2, 10, 100, 1000]:
        A = list(range(2, 2 * n + 1, 2))
        peor = 0
        for x in range(1, 2 * n + 2):
            c = Menor()
            assert correcta(A, x, two_way_binary_search(A, x, c))
            peor = max(peor, c.veces)
        print(f"{n:>6} {peor:>17} {techo_log2(2 * n + 1):>17} "
              f"{techo_log2(n + 1) + 1:>20}")


# --------------------------------------------------------------------------
# 5. Pruebas
# --------------------------------------------------------------------------

def pruebas():
    seccion("Pruebas")
    comprobaciones = 0
    rng = random.Random(2026)

    # (a) la búsqueda contra el oráculo, con repetidos, arreglo vacío y x en los bordes
    for _ in range(30_000):
        A = sorted(rng.randrange(30) for _ in range(rng.randint(0, 40)))
        x = rng.randint(-2, 32)
        assert correcta(A, x, binary_search(A, x, Comparador()))
        comprobaciones += 1

    # (b) todos los resultados posibles para n <= 300, y su peor caso exacto
    for n in range(301):
        assert peor_caso_exhaustivo(n) == techo_log2(n + 1)
        comprobaciones += 2 * n + 1

    # (c) bits(n) = ceil(log2(n + 1)) y ceil(log2(2n + 1)) = ceil(log2(n + 1)) + 1
    for n in range(1, 100_000):
        assert bits(n) == techo_log2(n + 1) == math.floor(math.log2(n)) + 1
        assert techo_log2(2 * n + 1) == techo_log2(n + 1) + 1
        comprobaciones += 2

    # (d) la DP sobre todos los algoritmos da la cota, para n <= 1000
    opt = optimo_por_dp(1000)
    for n in range(1001):
        assert opt[n] == techo_log2(n + 1)
        comprobaciones += 1

    # (e) en el árbol de n = 1..64, los n + 1 huecos caen en hojas distintas
    for n in range(1, 65):
        hojas = hojas_de_hueco(arbol_de_decision(n))
        assert sorted(g for g, _ in hojas) == list(range(n + 1))
        assert max(p for _, p in hojas) == techo_log2(n + 1)
        comprobaciones += 1

    # (f) la versión de dos vías contra el oráculo
    for _ in range(30_000):
        A = sorted(rng.randrange(30) for _ in range(rng.randint(0, 40)))
        x = rng.randint(-2, 32)
        c = Menor()
        assert correcta(A, x, two_way_binary_search(A, x, c))
        assert c.veces <= techo_log2(2 * len(A) + 1)
        comprobaciones += 1

    print(f"{miles(comprobaciones)} comprobaciones, 0 fallos")


# --------------------------------------------------------------------------
# 6. Figuras
# --------------------------------------------------------------------------

TINTA, APAGADO, REGLA = "#1a1a1a", "#6b7280", "#d8dce3"
ACENTO, OSCURO, CALIDO, ALARMA = "#0891b2", "#0e7490", "#b45309", "#be123c"


def _estilo():
    plt.rcParams.update({
        "font.size": 9, "axes.edgecolor": APAGADO, "axes.labelcolor": TINTA,
        "xtick.color": APAGADO, "ytick.color": APAGADO,
        "figure.facecolor": "white", "svg.hashsalt": "ejercicio-02",
    })


def _guardar(fig, nombre):
    fig.tight_layout()
    fig.savefig(nombre, metadata={"Date": None})
    plt.close(fig)


def figura_arbol():
    n = 10
    arbol = arbol_de_decision(n)
    fig, ax = plt.subplots(figsize=(7.2, 3.5))
    altura = techo_log2(n + 1)

    def dibujar(nodo, prof):
        # en orden, los nodos son h0 A[0] h1 A[1] ... A[n-1] hn: x = 2g o 2i + 1
        if "hoja" in nodo:
            g = nodo["hoja"][1]
            ax.text(2 * g, -prof, f"h{g}", ha="center", va="center", fontsize=8,
                    color="white", bbox={"boxstyle": "square,pad=0.3",
                                         "facecolor": CALIDO, "edgecolor": "none"})
            return 2 * g
        i = nodo["pos"]
        for r in (-1, 1):
            hijo = nodo[r]
            xh = (2 * hijo["hoja"][1] if "hoja" in hijo else 2 * hijo["pos"] + 1)
            ax.plot([2 * i + 1, xh], [-prof, -prof - 1], color=APAGADO, lw=0.9, zorder=1)
            ax.text((2 * i + 1 + xh) / 2 + (-0.35 if r < 0 else 0.35), -prof - 0.45,
                    "<" if r < 0 else ">", color=APAGADO, fontsize=7, ha="center")
            dibujar(hijo, prof + 1)
        ax.text(2 * i + 1, -prof, f"A[{i}]", ha="center", va="center", fontsize=8,
                color=TINTA, zorder=3, bbox={"boxstyle": "round,pad=0.3",
                                             "facecolor": "white", "edgecolor": OSCURO})
        return 2 * i + 1

    dibujar(arbol, 0)
    for p in range(altura + 1):
        ax.axhline(-p, color=REGLA, lw=0.6, zorder=0)
        ax.text(-1.6, -p, f"{p}", color=APAGADO, ha="right", va="center", fontsize=8)
    ax.text(-1.6, 0.75, "comparaciones", color=APAGADO, ha="right", fontsize=8)
    ax.set_xlim(-2.5, 2 * n + 1)
    ax.set_ylim(-altura - 0.6, 0.9)
    ax.axis("off")
    _guardar(fig, "ejercicio-02-arbol.svg")


def figura_testigo():
    n = 7
    fig, ax = plt.subplots(figsize=(7.2, 1.9))
    xs = [2 * i + 1 for i in range(n)]            # A[i] en x = 2i + 1, hueco g en x = 2g
    g1, g2, testigo = 1, 4, 2
    ax.axvspan(2 * g1, 2 * g2, color=ALARMA, alpha=0.08, lw=0)
    ax.plot([-0.8, 2 * n + 0.8], [0, 0], color=APAGADO, lw=1)
    for i, x in enumerate(xs):
        dentro = g1 <= i < g2
        ax.plot([x], [0], "o", ms=7, color=ALARMA if dentro else OSCURO, zorder=3)
        ax.text(x, -0.42, f"A[{i}]", ha="center", fontsize=8,
                color=ALARMA if dentro else TINTA)
    for g in range(n + 1):
        ax.text(2 * g, 0.28, f"h{g}", ha="center", fontsize=7.5, color=APAGADO)
    for g, nombre in [(g1, "x₁"), (g2, "x₂")]:
        ax.plot([2 * g], [0], "v", ms=8, color=CALIDO, zorder=4)
        ax.text(2 * g, 0.62, nombre, ha="center", fontsize=9, color=CALIDO)
    ax.annotate("x = A[2] recibe las mismas\nrespuestas que x₁", (xs[testigo], -0.12),
                xytext=(xs[testigo] + 6.2, -0.95), color=ALARMA, fontsize=8,
                arrowprops={"arrowstyle": "->", "color": ALARMA, "lw": 0.8})
    ax.text(2 * g1 + 0.1, -1.0, "nadie compara con A[1], A[2], A[3]", color=ALARMA,
            fontsize=8)
    ax.set_xlim(-1, 2 * n + 1)
    ax.set_ylim(-1.2, 0.9)
    ax.axis("off")
    _guardar(fig, "ejercicio-02-testigo.svg")


def figura_errores(fallos):
    fig, ax = plt.subplots(figsize=(6.6, 3.0))
    nombres = list(fallos)
    colores = [OSCURO, ALARMA, CALIDO]
    ancho = 0.26
    for k, (v, color) in enumerate(zip(VARIANTES, colores)):
        alturas = [fallos[b][k] for b in nombres]
        pos = [i + (k - 1) * ancho for i in range(len(nombres))]
        ax.bar(pos, alturas, ancho, color=color, label=v)
        for x, h in zip(pos, alturas):
            ax.text(x, h + 1.2, f"{h:.0f}", ha="center", fontsize=7, color=color)
    ax.set_xticks(range(len(nombres)))
    ax.set_xticklabels(nombres)
    ax.set_ylabel("% de búsquedas mal")
    ax.set_ylim(0, 105)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color=REGLA, lw=0.6)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    _guardar(fig, "ejercicio-02-errores.svg")


if __name__ == "__main__":
    ejemplo_chico()
    invariante_vigilado()
    peor_caso()
    cuenta_ingenua()
    arbol_n10()
    fallos = errores_plantados()
    dos_vias()
    pruebas()
    _estilo()
    figura_arbol()
    figura_testigo()
    figura_errores(fallos)
    print("\nfiguras: ejercicio-02-arbol.svg, ejercicio-02-testigo.svg, "
          "ejercicio-02-errores.svg")
