"""Ejercicio 5 del Tema 1: detección de ciclos de Floyd (la tortuga y la liebre).

Una lista enlazada es un arreglo `sig`: sig[v] es el nodo siguiente a v, o None.
Desde un nodo inicial x_0 la sucesión x_{i+1} = sig[x_i] termina en None (no hay
ciclo) o tiene forma de ρ: una cola de μ nodos y un ciclo de λ nodos.

Uso:
    python ejercicio_05.py             imprime las tablas del informe
    python ejercicio_05.py --figuras   además regenera las figuras

Las pruebas están en test_ejercicio_05.py.
"""

import itertools
import math
import random
import sys
from pathlib import Path


class Lista:
    """Envuelve `sig` y cuenta cuántas veces se sigue un puntero."""

    def __init__(self, sig):
        self.sig = sig
        self.evaluaciones = 0

    def f(self, v):
        self.evaluaciones += 1
        return self.sig[v]


# ---------------------------------------------------------------------------
# 1. El algoritmo
# ---------------------------------------------------------------------------

def floyd(lista, inicio, traza=None):
    """Devuelve (hay_ciclo, vueltas). En `traza` anota (tortuga, liebre) tras cada vuelta."""
    tortuga = liebre = inicio
    vueltas = 0
    while liebre is not None:
        siguiente = lista.f(liebre)
        if siguiente is None:
            break
        tortuga = lista.f(tortuga)
        liebre = lista.f(siguiente)
        vueltas += 1
        if traza is not None:
            traza.append((tortuga, liebre))
        if tortuga == liebre:
            return True, vueltas
    return False, vueltas


def floyd_completo(lista, inicio):
    """Detecta el ciclo y, si lo hay, calcula μ (largo de la cola) y λ (largo del ciclo)."""
    tortuga = liebre = inicio
    while True:
        if liebre is None:
            return None
        siguiente = lista.f(liebre)
        if siguiente is None:
            return None
        tortuga = lista.f(tortuga)
        liebre = lista.f(siguiente)
        if tortuga == liebre:
            break
    # El encuentro fue en t*, múltiplo de λ: desde x_0 y desde x_{t*} se llega juntos a x_μ.
    a, b, mu = inicio, liebre, 0
    while a != b:
        a, b, mu = lista.f(a), lista.f(b), mu + 1
    # Una vuelta al ciclo desde x_μ.
    lam, c = 1, lista.f(a)
    while c != a:
        c, lam = lista.f(c), lam + 1
    return mu, lam


def con_conjunto(lista, inicio):
    """La alternativa obvia: guardar los nodos vistos. Memoria μ + λ, evaluaciones μ + λ."""
    vistos = {}
    v, i = inicio, 0
    while v is not None and v not in vistos:
        vistos[v] = i
        v, i = lista.f(v), i + 1
    if v is None:
        return None, len(vistos)
    return (vistos[v], i - vistos[v]), len(vistos)


# ---------------------------------------------------------------------------
# 2. La verdad, calculada sin Floyd
# ---------------------------------------------------------------------------

def forma(sig, inicio):
    """(μ, λ) si hay ciclo, o ("sin ciclo", n) con n nodos, recorriendo con un diccionario."""
    vistos = {}
    v, i = inicio, 0
    while v is not None and v not in vistos:
        vistos[v] = i
        v, i = sig[v], i + 1
    if v is None:
        return ("sin ciclo", i)
    return (vistos[v], i - vistos[v])


def encuentro_teorico(mu, lam):
    """t*: el menor t >= max(1, μ) múltiplo de λ."""
    return lam * max(1, math.ceil(mu / lam))


def construir(mu, lam, rng=None, sobrantes=0):
    """Una lista con cola μ y ciclo λ (λ = 0: lista de μ nodos sin ciclo), con nombres al azar.

    `sobrantes` agrega nodos que no se alcanzan desde el inicio.
    """
    total = mu + lam + sobrantes
    nombres = list(range(total))
    if rng is not None:
        rng.shuffle(nombres)
    sig = [None] * total
    camino = nombres[:mu + lam]
    for a, b in zip(camino, camino[1:]):
        sig[a] = b
    if lam > 0:
        sig[camino[-1]] = camino[mu]
    for v in nombres[mu + lam:]:
        sig[v] = rng.choice(nombres) if rng is not None and rng.random() < 0.5 else None
    inicio = camino[0] if camino else None
    return sig, inicio


def potencial(mu, lam, t):
    """Φ_t del informe, para la lista con ciclo (μ, λ) tras t vueltas."""
    if t < mu:
        return (mu - t) + lam
    r = (-t) % lam
    return r if r else lam


# ---------------------------------------------------------------------------
# 3. Tablas
# ---------------------------------------------------------------------------

def tabla_exhaustiva(N=6):
    print(f"Tabla 1. Todas las listas de hasta {N} nodos ((N+1)^N funciones, todo inicio)")
    casos = ciclos = 0
    vueltas_max_relativa = 0
    for n in range(1, N + 1):
        for sig in itertools.product([None] + list(range(n)), repeat=n):
            for inicio in range(n):
                casos += 1
                verdad = forma(sig, inicio)
                lista = Lista(sig)
                hay, vueltas = floyd(lista, inicio)
                if verdad[0] == "sin ciclo":
                    assert not hay and vueltas == verdad[1] // 2
                else:
                    ciclos += 1
                    mu, lam = verdad
                    assert hay and vueltas == encuentro_teorico(mu, lam) <= mu + lam
                    assert floyd_completo(Lista(sig), inicio) == (mu, lam)
                    vueltas_max_relativa = max(vueltas_max_relativa, vueltas / (mu + lam))
    print(f"  {casos} listas, {ciclos} con ciclo: todas correctas;"
          f" máx vueltas/(μ+λ) = {vueltas_max_relativa:.3f}")
    print()


def tabla_encuentros():
    print("Tabla 2. Vuelta del encuentro t* contra μ + λ")
    print(f"{'μ':>4} {'λ':>4} {'t* medido':>10} {'t* teórico':>11} {'μ+λ':>5} {'evaluaciones':>13}"
          f" {'3(μ+λ)':>7}")
    rng = random.Random(1)
    for mu, lam in [(0, 1), (0, 10), (1, 1), (5, 3), (3, 5), (10, 10), (11, 10), (100, 7),
                    (7, 100), (1000, 1)]:
        sig, inicio = construir(mu, lam, rng)
        lista = Lista(sig)
        hay, vueltas = floyd(lista, inicio)
        print(f"{mu:>4} {lam:>4} {vueltas:>10} {encuentro_teorico(mu, lam):>11} {mu + lam:>5}"
              f" {lista.evaluaciones:>13} {3 * (mu + lam):>7}")
    print()


def tabla_traza(mu=4, lam=7):
    print(f"Tabla 3. Traza con μ = {mu}, λ = {lam} (nodo = índice en la sucesión, mod el ciclo)")
    sig, inicio = construir(mu, lam)
    traza = []
    floyd(Lista(sig), inicio, traza)
    print(f"{'t':>3} {'tortuga x_t':>12} {'liebre x_2t':>12} {'Φ_t':>5}")
    print(f"{0:>3} {'x_0':>12} {'x_0':>12} {potencial(mu, lam, 0):>5}")
    for t, (a, b) in enumerate(traza, 1):
        fi = "encuentro" if a == b else potencial(mu, lam, t)
        print(f"{t:>3} {'x_' + str(a):>12} {'x_' + str(b):>12} {fi:>5}")
    print()


# ---------------------------------------------------------------------------
# 4. Figuras
# ---------------------------------------------------------------------------

AZUL, NARANJA, AQUA, AMARILLO = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
ROJO = "#e34948"
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


def figura_rho(plt, destino, mu=4, lam=7):
    fig, ax = plt.subplots(figsize=(8.6, 4.4))
    ax.set_aspect("equal")
    ax.axis("off")
    radio = 1.6
    centro = (mu * 1.1 + radio, 0)
    pos = {}
    for i in range(mu):
        pos[i] = (i * 1.1, 0)
    for j in range(lam):
        ang = math.pi - 2 * math.pi * j / lam
        pos[mu + j] = (centro[0] + radio * math.cos(ang), centro[1] + radio * math.sin(ang))
    # aristas
    orden = list(range(mu + lam)) + [mu]
    for a, b in zip(orden, orden[1:]):
        (x1, y1), (x2, y2) = pos[a], pos[b]
        ax.annotate("", xy=(x1 + 0.82 * (x2 - x1), y1 + 0.82 * (y2 - y1)),
                    xytext=(x1 + 0.18 * (x2 - x1), y1 + 0.18 * (y2 - y1)),
                    arrowprops=dict(arrowstyle="-|>", color=TENUE, linewidth=1.2))
    t_star = encuentro_teorico(mu, lam)
    encuentro = mu + (t_star - mu) % lam
    for v, (x, y) in pos.items():
        color = AQUA if v < mu else AZUL
        if v == encuentro:
            color = ROJO
        ax.plot(x, y, "o", color=color, markersize=21, markeredgecolor=SUPERFICIE, markeredgewidth=2)
        ax.text(x, y, f"x{v}", ha="center", va="center", color="white",
                fontsize=8 if v < 10 else 7, fontweight="bold")
    ax.text(pos[0][0], -0.75, "x₀: empiezan\nlas dos", ha="center", fontsize=9, color=TINTA_2)
    ax.text(pos[mu][0] - 1.1, 0.75, f"x{mu} = x_μ:\nentrada al ciclo", ha="center", fontsize=9,
            color=TINTA_2)
    xe, ye = pos[encuentro]
    ax.annotate(f"se encuentran en t* = {t_star}:\ntortuga en x_{t_star}, liebre en x_{2 * t_star}\n"
                f"({2 * t_star} − {t_star} = {t_star}, múltiplo de λ = {lam})",
                (xe, ye), xytext=(centro[0] + radio + 0.6, 1.2), fontsize=9, color=TINTA,
                arrowprops=dict(arrowstyle="-", color=TENUE, linewidth=1))
    ax.text(mu * 0.55 - 0.5, -1.55, f"cola: μ = {mu} nodos", fontsize=9, color="#1a7a55")
    ax.text(centro[0] - 0.6, -radio - 0.55, f"ciclo: λ = {lam} nodos", fontsize=9, color=AZUL)
    ax.set_xlim(-0.8, centro[0] + radio + 4.6)
    ax.set_ylim(-radio - 0.8, radio + 0.6)
    ax.set_title("La ρ: una cola de μ nodos y un ciclo de λ")
    fig.savefig(destino / "ejercicio-05-rho.png")
    plt.close(fig)


def figura_potencial(plt, destino):
    fig, ax = plt.subplots(figsize=(8, 4.2))
    casos = [(0, 9, AZUL), (6, 9, NARANJA), (14, 5, AQUA), (3, 14, AMARILLO)]
    for mu, lam, color in casos:
        t_star = encuentro_teorico(mu, lam)
        ts = list(range(0, t_star))
        ax.plot(ts, [potencial(mu, lam, t) for t in ts], "o-", color=color, markersize=4,
                label=f"μ = {mu}, λ = {lam}: se encuentran en t* = {t_star}")
        ax.plot([t_star], [0], "o", color=color, markersize=8, markeredgecolor=SUPERFICIE,
                markeredgewidth=1.5)
    ax.set_xlabel("vuelta t")
    ax.set_ylabel("potencial Φ_t")
    ax.set_title("El potencial baja en cada vuelta: en la cola de a 1, al entrar al ciclo puede saltar")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=2)
    fig.savefig(destino / "ejercicio-05-potencial.png")
    plt.close(fig)


def figuras():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    _estilo(plt)
    destino = Path(__file__).resolve().parent.parent / "figuras"
    destino.mkdir(exist_ok=True)
    figura_rho(plt, destino)
    figura_potencial(plt, destino)
    print(f"figuras escritas en {destino}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    tabla_traza()
    tabla_encuentros()
    tabla_exhaustiva(6)
    if "--figuras" in sys.argv:
        figuras()
