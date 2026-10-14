"""Ejercicio 13 del Tema 1: splay tree que empieza como un camino, accesos 1..n en orden.

Compara la cota que da el lema de acceso (conferencia 4, §5) con el costo real.

Uso:
    python ejercicio_13.py             imprime las tablas del informe
    python ejercicio_13.py --figuras   además regenera las figuras

Las pruebas están en test_ejercicio_13.py.
"""

import math
import random
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# 1. El splay tree de la conferencia 4
# ---------------------------------------------------------------------------

class Nodo:
    __slots__ = ("clave", "izq", "der", "padre")

    def __init__(self, clave):
        self.clave, self.izq, self.der, self.padre = clave, None, None, None


def rotar(x):
    """Sube x un nivel rotando la arista con su padre. Preserva el orden."""
    p, g = x.padre, x.padre.padre
    if p.izq is x:
        p.izq, x.der = x.der, p
        if p.izq:
            p.izq.padre = p
    else:
        p.der, x.izq = x.izq, p
        if p.der:
            p.der.padre = p
    p.padre, x.padre = x, g
    if g:
        if g.izq is p:
            g.izq = x
        else:
            g.der = x


def splay(x):
    rotaciones = 0
    while x.padre:
        p, g = x.padre, x.padre.padre
        if g is None:                                   # zig
            rotar(x)
            rotaciones += 1
        elif (g.izq is p) == (p.izq is x):              # zig-zig: primero el padre
            rotar(p)
            rotar(x)
            rotaciones += 2
        else:                                           # zig-zag
            rotar(x)
            rotar(x)
            rotaciones += 2
    return rotaciones


def subir_a_la_raiz(x):
    rotaciones = 0
    while x.padre:
        rotar(x)
        rotaciones += 1
    return rotaciones


def buscar(raiz, clave):
    x = raiz
    while x.clave != clave:
        x = x.izq if clave < x.clave else x.der
    return x


def camino(n):
    """El árbol inicial: n en la raíz, cada clave hija izquierda de la siguiente."""
    nodos = [Nodo(k) for k in range(1, n + 1)]
    for k in range(1, n):
        nodos[k].izq, nodos[k - 1].padre = nodos[k - 1], nodos[k]
    return nodos[-1]


def tamanos(raiz):
    """s(x) para cada nodo, sin recursión (los caminos son profundos)."""
    orden, pila = [], [raiz]
    while pila:
        x = pila.pop()
        orden.append(x)
        if x.izq:
            pila.append(x.izq)
        if x.der:
            pila.append(x.der)
    s = {}
    for x in reversed(orden):
        s[x] = 1 + (s[x.izq] if x.izq else 0) + (s[x.der] if x.der else 0)
    return s


def potencial(raiz):
    """Φ = Σ log2 s(x)."""
    return sum(math.log2(v) for v in tamanos(raiz).values())


def es_de_busqueda(raiz):
    """Recorrido en orden iterativo: las claves salen crecientes y los punteros a padre cuadran."""
    claves, pila, x = [], [], raiz
    while pila or x:
        while x:
            if x.izq and x.izq.padre is not x:
                return False
            if x.der and x.der.padre is not x:
                return False
            pila.append(x)
            x = x.izq
        x = pila.pop()
        claves.append(x.clave)
        x = x.der
    return claves == sorted(claves) and raiz.padre is None


def es_camino_izquierdo(raiz, tope, fondo=1):
    """True si raiz es tope, su hijo izquierdo tope - 1, ..., hasta fondo, sin hijos derechos."""
    x, k = raiz, tope
    while x:
        if x.clave != k or x.der is not None:
            return False
        x, k = x.izq, k - 1
    return k == fondo - 1


def invariante_secuencial(raiz, k):
    """Después de acceder a k: raíz k y subárbol izquierdo = camino k-1, ..., 1."""
    if raiz.clave != k:
        return False
    return raiz.izq is None if k == 1 else es_camino_izquierdo(raiz.izq, k - 1)


def profundidad_maxima(raiz):
    mejor, pila = 0, [(raiz, 0)]
    while pila:
        x, d = pila.pop()
        mejor = max(mejor, d)
        for h in (x.izq, x.der):
            if h:
                pila.append((h, d + 1))
    return mejor


# ---------------------------------------------------------------------------
# 2. Experimentos
# ---------------------------------------------------------------------------

def acceder(raiz, clave, reorganizar=splay):
    x = buscar(raiz, clave)
    return x, max(reorganizar(x), 1)                    # costo: rotaciones, o 1 si ya es la raíz


def recorrido(n, rondas=1, reorganizar=splay):
    """Accede a 1..n en orden, `rondas` veces, desde el camino. Devuelve los costos."""
    raiz, costos = camino(n), []
    for _ in range(rondas):
        for clave in range(1, n + 1):
            raiz, c = acceder(raiz, clave, reorganizar)
            costos.append(c)
    return costos, raiz


def al_azar(n, m, semilla=0):
    rng = random.Random(semilla)
    raiz, total = camino(n), 0
    for _ in range(m):
        raiz, c = acceder(raiz, rng.randint(1, n))
        total += c
    return total


def descomposicion(n):
    """Una pasada 1..n con el potencial medido en cada acceso.

    Devuelve real, Σ amortizado real, Σ de las cotas del lema por acceso, Φ_0, Φ_final y
    la cantidad de accesos donde el lema fallaría (debe ser 0).
    """
    raiz = camino(n)
    phi0 = fi = potencial(raiz)
    real = amortizado = cotas = 0.0
    fallos = 0
    log_n = math.log2(n)
    for clave in range(1, n + 1):
        x = buscar(raiz, clave)
        r_x = math.log2(tamanos(raiz)[x]) if clave != raiz.clave else log_n
        c = max(splay(x), 1)
        raiz = x
        nuevo = potencial(raiz)
        a = c + nuevo - fi
        cota = 3 * (log_n - r_x) + 1
        fallos += a > cota + 1e-9
        real += c
        amortizado += a
        cotas += cota
        fi = nuevo
    return dict(real=real, amortizado=amortizado, cotas=cotas, phi0=phi0, phi_final=fi,
                fallos=fallos, global_=n * (3 * log_n + 1) + phi0)


def cota_global(n, m=None):
    """La cuenta de la C4, §5: m(3 log2 n + 1) + Φ_0, con Φ_0 = log2 n! (el camino)."""
    m = n if m is None else m
    return m * (3 * math.log2(n) + 1) + math.lgamma(n + 1) / math.log(2)


# ---------------------------------------------------------------------------
# 3. Tablas
# ---------------------------------------------------------------------------

def tabla_una_pasada():
    print("Tabla 1. Una pasada 1..n desde el camino: real contra la cota del lema")
    print(f"{'n':>8} {'real':>10} {'real / n':>9} {'cota':>12} {'cota / real':>12}"
          f" {'primer acceso':>14} {'¿vuelve al camino?':>19}")
    for n in [100, 1000, 10**4, 10**5]:
        costos, raiz = recorrido(n)
        print(f"{n:>8} {sum(costos):>10} {sum(costos) / n:>9.3f} {cota_global(n):>12.0f}"
              f" {cota_global(n) / sum(costos):>12.2f} {costos[0]:>14}"
              f" {str(es_camino_izquierdo(raiz, n)):>19}")
    print()


def tabla_rondas():
    print("Tabla 2. Rotaciones por acceso en la sección 6 (tres rondas) y en una sola")
    print(f"{'n':>6} {'1 ronda':>8} {'3 rondas':>9} {'rondas 2 y 3':>13} {'subir a la raíz (3)':>20}")
    for n in [100, 200, 400, 800]:
        uno, _ = recorrido(n, 1)
        tres, _ = recorrido(n, 3)
        raiz_tres, _ = recorrido(n, 3, subir_a_la_raiz)
        print(f"{n:>6} {sum(uno) / n:>8.2f} {sum(tres) / (3 * n):>9.2f} {sum(tres[n:]) / (2 * n):>13.2f}"
              f" {sum(raiz_tres) / (3 * n):>20.1f}")
    print()


def tabla_descomposicion():
    print("Tabla 3. Dónde está la holgura (una pasada, potencial medido en cada acceso)")
    print(f"{'n':>6} {'Σ real':>8} {'Σ amort.':>9} {'Σ cotas lema':>13} {'Φ_0':>8} {'Φ_final':>8}"
          f" {'cota global':>12} {'violaciones':>12}")
    for n in [100, 200, 400, 800, 1600]:
        d = descomposicion(n)
        print(f"{n:>6} {d['real']:>8.0f} {d['amortizado']:>9.0f} {d['cotas']:>13.0f} {d['phi0']:>8.0f}"
              f" {d['phi_final']:>8.0f} {d['global_']:>12.0f} {d['fallos']:>12}")
    print()


def tabla_al_azar():
    print("Tabla 4. Accesos al azar (3n desde el camino): el lema no es flojo en general")
    print(f"{'n':>8} {'por acceso':>11} {'log2 n':>7} {'cociente':>9}")
    for n in [100, 1000, 10**4, 10**5]:
        total = al_azar(n, 3 * n)
        print(f"{n:>8} {total / (3 * n):>11.2f} {math.log2(n):>7.2f} {total / (3 * n) / math.log2(n):>9.2f}")
    print()


# ---------------------------------------------------------------------------
# 4. Figuras
# ---------------------------------------------------------------------------

AZUL, NARANJA, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
TINTA, TINTA_2, TENUE, REJILLA, SUPERFICIE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"


def _estilo(plt):
    plt.rcParams.update({
        "font.family": ["Segoe UI", "DejaVu Sans"], "font.size": 10,
        "axes.edgecolor": "#c3c2b7", "axes.labelcolor": TINTA_2, "axes.titlecolor": TINTA,
        "axes.titlesize": 12, "axes.titleweight": "bold", "axes.titlelocation": "left",
        "axes.facecolor": SUPERFICIE, "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.color": REJILLA, "grid.linewidth": 0.6,
        "xtick.color": TENUE, "ytick.color": TENUE, "xtick.labelcolor": TINTA_2,
        "ytick.labelcolor": TINTA_2, "figure.facecolor": SUPERFICIE, "legend.frameon": False,
        "legend.labelcolor": TINTA_2, "lines.linewidth": 2, "savefig.dpi": 150,
        "savefig.bbox": "tight",
    })


def figura_por_acceso(plt, destino):
    ns = [2**k for k in range(5, 18)]
    secuencial = [sum(recorrido(n)[0]) / n for n in ns]
    azar = [al_azar(n, 3 * n) / (3 * n) for n in ns]
    cota = [cota_global(n) / n for n in ns]
    fig, ax = plt.subplots(figsize=(8, 4.4))
    ax.plot(ns, cota, color=TENUE, linestyle=(0, (4, 3)), linewidth=1.6,
            label="cota del lema + §5, por acceso: 3 log₂ n + 1 + log₂(n!)/n")
    ax.plot(ns, azar, "o-", color=NARANJA, markersize=5, label="accesos al azar (3n desde el camino)")
    ax.plot(ns, secuencial, "o-", color=AZUL, markersize=5, label="claves 1..n en orden, una pasada")
    ax.set_xscale("log", base=2)
    ax.set_xlabel("n")
    ax.set_ylabel("rotaciones por acceso")
    ax.set_title("En orden, el costo por acceso no crece; la cota sí")
    ax.legend(loc="upper left")
    fig.savefig(destino / "ejercicio-13-por-acceso.png")
    plt.close(fig)


def figura_acceso_a_acceso(plt, destino, n=1024):
    raiz = camino(n)
    fi = potencial(raiz)
    log_n = math.log2(n)
    acum_real, acum_cotas, potenciales = [0], [0], [fi]
    for clave in range(1, n + 1):
        x = buscar(raiz, clave)
        r_x = math.log2(tamanos(raiz)[x]) if clave != raiz.clave else log_n
        c = max(splay(x), 1)
        raiz = x
        fi = potencial(raiz)
        acum_real.append(acum_real[-1] + c)
        acum_cotas.append(acum_cotas[-1] + 3 * (log_n - r_x) + 1)
        potenciales.append(fi)
    xs = list(range(0, n + 1))
    phi0 = potenciales[0]
    fig, (izq, der) = plt.subplots(1, 2, figsize=(10.5, 4.2))
    izq.plot(xs, [phi0 + k * (3 * log_n + 1) for k in xs], color=TENUE, linestyle=(0, (4, 3)),
             linewidth=1.5, label="cota de la §5: Φ₀ + k(3 log₂ n + 1)")
    izq.plot(xs, acum_cotas, color=AQUA, label="suma de las cotas del lema, acceso a acceso")
    izq.plot(xs, acum_real, color=NARANJA, label="costo real acumulado")
    izq.set_xlabel("accesos hechos (claves 1..k)")
    izq.set_ylabel("rotaciones acumuladas")
    izq.set_title("Dos capas de holgura")
    izq.legend(loc="upper left", fontsize=8.5)
    der.plot(xs, potenciales, color=AZUL)
    der.axhline(phi0, color=TENUE, linewidth=1, linestyle=(0, (4, 3)))
    der.text(n * 0.03, phi0 * 1.02, "Φ₀ = log₂ n!  (el camino)", color=TINTA_2, fontsize=9)
    der.set_xlabel("accesos hechos")
    der.set_ylabel("potencial Φ = Σ log₂ s(x)")
    der.set_title("Los primeros accesos descargan Φ; la pasada lo recarga")
    fig.suptitle(f"Splay sobre el camino de n = {n} nodos, claves en orden", x=0.01, ha="left",
                 fontsize=10, color=TINTA_2)
    fig.tight_layout()
    fig.savefig(destino / "ejercicio-13-acceso-a-acceso.png")
    plt.close(fig)


def figuras():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    _estilo(plt)
    destino = Path(__file__).resolve().parent.parent / "figuras"
    destino.mkdir(exist_ok=True)
    figura_por_acceso(plt, destino)
    figura_acceso_a_acceso(plt, destino)
    print(f"figuras escritas en {destino}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    tabla_una_pasada()
    tabla_rondas()
    tabla_descomposicion()
    tabla_al_azar()
    if "--figuras" in sys.argv:
        figuras()
