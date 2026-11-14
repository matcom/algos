"""Figuras de las soluciones del Tema 1.

Cada figura se dibuja a partir del estado que calcula el código del ejercicio
(las celdas que la escalera compara de verdad, los pares que la mezcla compara de
verdad), nunca con posiciones puestas a mano. Así una figura no puede contradecir
al código.

Cada figura se guarda dos veces en `figuras/`, una para el tema claro y otra para el
oscuro, y el md elige la que corresponde con <picture>.

Los GIF animados (GIFS) se guardan con el fondo de cada tema, porque un GIF no
tiene transparencia parcial.

Uso:
    python figuras.py          # todas
    python figuras.py 6 9      # solo las de los ejercicios 6 y 9
"""
import importlib
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

# Paleta de las figuras de las conferencias (Lectures/2026/figuras.py), con una
# variante para fondo oscuro de la misma familia de colores.
TEMAS = {
    "claro": dict(tinta="#1a1a1a", apagado="#6b7280", regla="#d8dce3",
                  acento="#0891b2", oscuro="#0e7490", calido="#b45309",
                  alarma="#be123c", fondo="#ffffff", suave="#ecfeff"),
    "oscuro": dict(tinta="#e6edf3", apagado="#9198a1", regla="#3d444d",
                   acento="#22b8d6", oscuro="#67d4e8", calido="#e3a03b",
                   alarma="#f47185", fondo="#0d1117", suave="#0f2a33"),
}

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "svg.fonttype": "path",   # el texto viaja como trazos: se ve igual en cualquier visor
    "svg.hashsalt": "tema-1",  # ids fijos en el svg: regenerar no cambia el archivo
})


def ejercicio(n):
    return importlib.import_module(f"ejercicio-{n:02d}")


def guardar(dibujar, nombre):
    """Dibuja la figura con cada tema y la guarda en figuras/<nombre>-<tema>.svg."""
    os.makedirs(os.path.join(AQUI, "figuras"), exist_ok=True)
    for tema, t in TEMAS.items():
        fig = dibujar(t)
        ruta = os.path.join(AQUI, "figuras", f"{nombre}-{tema}.svg")
        fig.savefig(ruta, transparent=True, bbox_inches="tight", pad_inches=0.1,
                    metadata={"Date": None})   # sin fecha: regenerar no cambia el archivo
        plt.close(fig)
        print("escrita", os.path.relpath(ruta, AQUI))


def lienzo(ancho, alto):
    fig, ax = plt.subplots(figsize=(ancho, alto))
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


# --------------------------------------------------------------------------
# Ejercicio 6. La escalera y la matriz del adversario
# --------------------------------------------------------------------------

def recorrido_escalera(M, x):
    """Corre la escalera del ejercicio 6 y devuelve (resultado, celdas comparadas)."""
    e6 = ejercicio(6)
    vistas = []

    class Celda(float):
        def __new__(cls, valor, i, j):
            obj = super().__new__(cls, valor)
            obj.ij = (i, j)
            return obj

        def __eq__(self, otro):
            if not vistas or vistas[-1] != self.ij:
                vistas.append(self.ij)
            return float(self) == float(otro)

        __hash__ = float.__hash__

    W = [[Celda(v, i, j) for j, v in enumerate(fila)] for i, fila in enumerate(M)]
    resultado, comps = e6.escalera(W, float(x), vigilar=False)
    assert comps == len(vistas)
    return resultado, vistas


def _matriz(ax, M, t, origen=(0, 0), fondo=None, texto=None):
    """Dibuja M con la fila 0 arriba. fondo y texto: (i, j) -> color."""
    n = len(M)
    ox, oy = origen
    for i in range(n):
        for j in range(n):
            x, y = ox + j, oy + n - 1 - i
            color = (fondo or {}).get((i, j), "none")
            ax.add_patch(Rectangle((x, y), 1, 1, facecolor=color,
                                   edgecolor=t["regla"], lw=1))
            v = M[i][j]
            etiqueta = f"{v:g}" if v == int(v) else f"{v:.1f}"
            ax.text(x + 0.5, y + 0.5, etiqueta, ha="center", va="center",
                    color=(texto or {}).get((i, j), t["tinta"]), fontsize=10)


def _camino(ax, M, vistas, t, origen=(0, 0), final=None):
    """Recuadra las celdas comparadas y une con flechas el orden en que se miran."""
    n = len(M)
    ox, oy = origen
    centro = lambda ij: (ox + ij[1] + 0.5, oy + n - 1 - ij[0] + 0.5)
    for ij in vistas:
        x, y = centro(ij)
        ax.add_patch(Rectangle((x - 0.5, y - 0.5), 1, 1, facecolor="none",
                               edgecolor=t["calido"], lw=2.2))
    for a, b in zip(vistas, vistas[1:]):
        ax.add_patch(FancyArrowPatch(centro(a), centro(b), arrowstyle="-|>",
                                     mutation_scale=11, color=t["calido"], lw=1.4,
                                     shrinkA=11, shrinkB=11))
    if final is not None:
        ax.add_patch(FancyArrowPatch(centro(vistas[-1]), final, arrowstyle="-|>",
                                     mutation_scale=11, color=t["calido"], lw=1.4,
                                     shrinkA=11, shrinkB=0, linestyle="--"))


def fig_06_escalera(t):
    M = [[1, 4, 7, 11], [2, 5, 8, 12], [3, 6, 9, 16], [10, 13, 14, 17]]
    n = len(M)
    fig, ax = lienzo(7.4, 3.6)
    for k, x in enumerate((9, 15)):
        origen = (k * (n + 1.6), 0)
        resultado, vistas = recorrido_escalera(M, x)
        fondo = {resultado: t["suave"]} if resultado else {}
        _matriz(ax, M, t, origen, fondo=fondo)
        fuera = None
        if resultado is None:   # el último paso sale por abajo de la matriz
            i, j = vistas[-1]
            fuera = (origen[0] + j + 0.5, origen[1] - 0.45)
        _camino(ax, M, vistas, t, origen, final=fuera)
        estado = "está en " + str(resultado) if resultado else "no está"
        ax.text(origen[0] + n / 2, n + 0.45, f"x = {x}", ha="center",
                fontsize=12, fontweight="bold", color=t["tinta"])
        ax.text(origen[0] + n / 2, -0.95, f"{len(vistas)} comparaciones: {estado}",
                ha="center", fontsize=10, color=t["calido"])
    ax.set_xlim(-0.2, 2 * n + 1.8)
    ax.set_ylim(-1.3, n + 0.9)
    return fig


def fig_06_adversario(t):
    e6 = ejercicio(6)
    n, x = 4, 10
    M1 = e6.antidiagonal(n, x)
    _, vistas = recorrido_escalera(M1, x)
    antidiagonal = {(i, n - 1 - i) for i in range(n)}
    assert antidiagonal <= set(vistas)
    fondo = {ij: t["suave"] for ij in antidiagonal}
    texto = {(i, j): t["apagado"] for i in range(n) for j in range(n)
             if (i, j) not in antidiagonal}
    fig, ax = lienzo(6.8, 3.9)
    _matriz(ax, M1, t, fondo=fondo, texto=texto)
    _camino(ax, M1, vistas, t, final=(vistas[-1][1] + 0.5, -0.45))
    # cada etiqueta va junto a una celda de su región: (0, 0), (0, n-1) y (n-1, n-1)
    ax.text(-0.3, n - 0.5, "s ≤ n − 2:\nmenores que x", ha="right", va="center",
            fontsize=9, color=t["apagado"])
    ax.text(n + 0.3, n - 0.5, "s = n − 1 (antidiagonal):\nentre x y x + 1", va="center",
            fontsize=9, color=t["acento"], fontweight="bold")
    ax.text(n + 0.3, 0.5, "s ≥ n:\nmayores que x + 1", va="center",
            fontsize=9, color=t["apagado"])
    ax.text(n / 2, -0.95, f"la escalera hace {len(vistas)} = 2n − 1 comparaciones "
            f"y mira las {n} celdas de la antidiagonal",
            ha="center", fontsize=9.5, color=t["calido"])
    ax.text(n / 2, n + 0.35, f"M₁ con n = {n}, x = {x}", ha="center",
            fontsize=12, fontweight="bold", color=t["tinta"])
    ax.set_xlim(-2.4, n + 3.3)
    ax.set_ylim(-1.3, n + 0.8)
    return fig


# --------------------------------------------------------------------------
# Ejercicio 9. Los pares de vecinos que compara cada mezcla
# --------------------------------------------------------------------------

def fig_09_intercalado(t):
    e9 = ejercicio(9)
    A, B = [1, 3, 5], [2, 4, 6]
    n = len(A)
    vecinos = [frozenset((v, v + 1)) for v in range(1, 2 * n)]
    filas = [("mezcla normal", e9.mezcla), ("mezcla «optimizada»", e9.mezcla_optimizada)]
    fig, ax = lienzo(7.0, 4.6)
    paso, alto, sep = 1.25, 1.0, 3.1
    for k, (titulo, f) in enumerate(filas):
        y0 = -k * sep
        comparados = e9.pares_vecinos_comparados(A, B, f)
        assert comparados <= set(vecinos)
        salida, comps = f(A, B)
        pos = {v: ((v - 1) * paso, y0 + (alto if v in A else 0)) for v in A + B}
        for par in vecinos:
            u, v = sorted(par)
            (x1, y1), (x2, y2) = pos[u], pos[v]
            if par in comparados:
                ax.plot([x1, x2], [y1, y2], color=t["calido"], lw=2.2, zorder=1)
            else:
                ax.plot([x1, x2], [y1, y2], color=t["alarma"], lw=1.8, ls=(0, (3, 2.5)),
                        zorder=1)
        for v, (x, y) in pos.items():
            lista, i = ("a", A.index(v)) if v in A else ("b", B.index(v))
            ax.add_patch(Circle((x, y), 0.3, facecolor=t["fondo"],
                                edgecolor=t["acento"] if lista == "a" else t["tinta"],
                                lw=1.6, zorder=2))
            ax.text(x, y, f"{lista}{'₁₂₃₄₅₆₇₈₉'[i]}", ha="center", va="center",
                    fontsize=10, color=t["tinta"], zorder=3)
            ax.text(x, y + (0.5 if lista == "a" else -0.55), str(v), ha="center",
                    va="center", fontsize=8.5, color=t["apagado"])
        ax.text(-0.6, y0 + alto, "A", ha="right", va="center", color=t["acento"],
                fontsize=10, fontweight="bold")
        ax.text(-0.6, y0, "B", ha="right", va="center", color=t["tinta"],
                fontsize=10, fontweight="bold")
        ax.text(-0.9, y0 + alto + 0.75, f"{titulo}: {comps} de {len(vecinos)} pares "
                f"de vecinos comparados", fontsize=11, fontweight="bold",
                color=t["tinta"])
        bien = salida == sorted(A + B)
        ax.text((2 * n - 1) * paso + 0.7, y0 + alto / 2,
                f"salida {salida}\n" + ("correcta" if bien else "incorrecta"),
                va="center", fontsize=9.5, color=t["calido"] if bien else t["alarma"])
    ax.set_xlim(-1.2, (2 * n - 1) * paso + 4.3)
    ax.set_ylim(-sep - 0.9, alto + 1.2)
    return fig


# --------------------------------------------------------------------------
# utilidades para gráficas con ejes
# --------------------------------------------------------------------------

def coma(x, d=1):
    """Número con coma decimal, como en el texto."""
    return f"{x:.{d}f}".replace(".", ",")


def grafica(ancho, alto, filas=1, columnas=1):
    fig, ejes = plt.subplots(filas, columnas, figsize=(ancho, alto), squeeze=False)
    return fig, [ax for fila in ejes for ax in fila]


def estilo(ax, t, titulo=None, x=None, y=None):
    ax.set_facecolor("none")
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color(t["apagado"])
    ax.tick_params(colors=t["apagado"], labelcolor=t["tinta"], labelsize=9)
    ax.grid(True, color=t["regla"], lw=0.6, alpha=0.8)
    ax.set_axisbelow(True)
    if titulo:
        ax.set_title(titulo, color=t["tinta"], fontsize=11, fontweight="bold", loc="left")
    if x:
        ax.set_xlabel(x, color=t["tinta"], fontsize=10)
    if y:
        ax.set_ylabel(y, color=t["tinta"], fontsize=10)


def leyenda(ax, t, **kw):
    ley = ax.legend(frameon=False, fontsize=9, **kw)
    for texto in ley.get_texts():
        texto.set_color(t["tinta"])


def potencia(e):
    return f"10{''.join('⁰¹²³⁴⁵⁶⁷⁸⁹'[int(c)] for c in str(e))}"


# --------------------------------------------------------------------------
# Ejercicio 1. El factor de crecimiento del tamaño
# --------------------------------------------------------------------------

def fig_01_factor(t):
    e1 = ejercicio(1)
    exponentes = [e / 4 for e in range(4, 61)]
    ks = [e1.factor_nlogn(10 ** e) for e in exponentes]
    fig, (ax,) = grafica(6.6, 3.6)
    ax.plot(exponentes, ks, color=t["calido"], lw=2.2, label="costo c·n log₂ n")
    ax.axhline(1000 ** 0.5, color=t["acento"], lw=2.2, label="costo c·n²: √1000 ≈ 31,6")
    ax.axhline(1000, color=t["apagado"], lw=1.2, ls="--", label="costo lineal: 1000")
    for e in (3, 6, 9, 12):
        k = e1.factor_nlogn(10 ** e)
        ax.plot([e], [k], "o", color=t["calido"], ms=6, zorder=3)
        ax.annotate(coma(k), (e, k), textcoords="offset points", xytext=(0, -15),
                    ha="center", fontsize=9, color=t["calido"])
    ax.set_yscale("log")
    ax.set_ylim(15, 2500)
    ax.set_xticks(range(1, 16, 2))
    ax.set_xticklabels([potencia(e) for e in range(1, 16, 2)])
    estilo(ax, t, "Factor k = n₁ / n₀ con una máquina 1000 veces más rápida",
           "tamaño actual n₀", "factor k (escala logarítmica)")
    leyenda(ax, t, loc="center right")
    return fig


# --------------------------------------------------------------------------
# Ejercicio 2. El rango de la búsqueda binaria, vuelta por vuelta
# --------------------------------------------------------------------------

def traza_binaria(A, x):
    """Corre la búsqueda del ejercicio 2 y devuelve [(lo, hi, m), ...] y el resultado.
    Las m son las que el algoritmo mira; lo y hi se siguen con sus dos reglas."""
    e2 = ejercicio(2)
    miradas = []

    class Valor(int):
        def __eq__(self, otro):
            miradas.append(A.index(int(self)))
            return int(self) == int(otro)

        __hash__ = int.__hash__

    resultado, comps = e2.busqueda_binaria([Valor(a) for a in A], x, vigilar=False)
    assert comps == len(miradas)
    lo, hi, filas = 0, len(A), []
    for m in miradas:
        assert m == (lo + hi) // 2
        filas.append((lo, hi, m))
        if x < A[m]:
            hi = m
        elif x > A[m]:
            lo = m + 1
    return filas, (lo, hi), resultado


def fig_02_rango(t):
    A = [1, 3, 5, 7, 9, 11, 13]
    n = len(A)
    fig, ax = lienzo(8.4, 3.4)
    for col, x in enumerate((11, 8)):
        filas, (lo_f, hi_f), resultado = traza_binaria(A, x)
        ox = col * (n + 4.6)
        ax.text(ox + n / 2, 1.2, f"x = {x}", ha="center", fontsize=12,
                fontweight="bold", color=t["tinta"])
        if resultado[0] == "no está":
            filas = filas + [(lo_f, hi_f, None)]
        for r, (lo, hi, m) in enumerate(filas):
            y = -r * 1.35
            for j, a in enumerate(A):
                vivo = lo <= j < hi
                ax.add_patch(Rectangle((ox + j, y), 1, 1, edgecolor=t["regla"], lw=1,
                                       facecolor=t["suave"] if vivo else "none"))
                ax.text(ox + j + 0.5, y + 0.5, str(a), ha="center", va="center",
                        fontsize=10, color=t["tinta"] if vivo else t["apagado"])
            if m is not None:
                ax.add_patch(Rectangle((ox + m, y), 1, 1, facecolor="none",
                                       edgecolor=t["calido"], lw=2.2))
            ax.text(ox - 0.25, y + 0.5, f"{r + 1}" if m is not None else "fin",
                    ha="right", va="center", fontsize=9, color=t["apagado"])
            ax.text(ox + n + 0.25, y + 0.5, f"hi − lo = {hi - lo}", va="center",
                    fontsize=9, color=t["acento"])
        ax.text(ox + n / 2, -len(filas) * 1.35 + 0.55,
                f"{len(filas) - (resultado[0] == 'no está')} comparaciones: "
                + ("está en la posición " + str(resultado[1]) if resultado[0] == "está"
                   else "no está"),
                ha="center", fontsize=10, color=t["calido"])
    ax.set_xlim(-1.0, 2 * n + 7.4)
    ax.set_ylim(-4 * 1.35 + 0.1, 1.7)
    return fig


# --------------------------------------------------------------------------
# Ejercicio 3. Las dos pilas paralelas
# --------------------------------------------------------------------------

def fig_03_pilas(t):
    e3 = ejercicio(3)
    p = e3.PilaMin()
    estados = []
    for x in [5, 2, 7, 2]:
        p.push(x)
        estados.append((f"push({x})", list(p.v), list(p.m)))
    for _ in range(3):
        p.pop()
        estados.append(("pop()", list(p.v), list(p.m)))
    fig, ax = lienzo(8.4, 3.3)
    for c, (op, v, m) in enumerate(estados):
        ox = c * 2.75
        for i, (a, b) in enumerate(zip(v, m)):
            tope = i == len(v) - 1
            for dx, val, color in ((0, a, t["tinta"]), (1, b, t["acento"])):
                ax.add_patch(Rectangle((ox + dx, i), 1, 1, edgecolor=t["regla"], lw=1,
                                       facecolor=t["suave"] if (tope and dx) else "none"))
                ax.text(ox + dx + 0.5, i + 0.5, str(val), ha="center", va="center",
                        fontsize=10, color=color,
                        fontweight="bold" if (tope and dx) else "normal")
        ax.text(ox + 0.5, -0.45, "v", ha="center", fontsize=9, color=t["apagado"])
        ax.text(ox + 1.5, -0.45, "m", ha="center", fontsize=9, color=t["acento"])
        ax.text(ox + 1, 4.4, op, ha="center", fontsize=10, color=t["tinta"],
                family="DejaVu Sans Mono")
        ax.text(ox + 1, -1.15, f"mínimo() = {m[-1]}", ha="center", fontsize=9,
                color=t["calido"])
        assert m[-1] == min(v)
    ax.set_xlim(-0.3, len(estados) * 2.75)
    ax.set_ylim(-1.5, 4.9)
    return fig


# --------------------------------------------------------------------------
# Ejercicio 4. Costo real, potencial y costo amortizado del contador
# --------------------------------------------------------------------------

def fig_04_costos(t):
    e4 = ejercicio(4)
    cinta, cab, total = {}, 0, 0
    ms, pasos, totales, phis = [], [], [], []
    phi_antes = 0
    for m in range(1, 33):
        cab, c = e4.incremento(cinta, cab)
        phi = 2 * sum(1 for b in cinta.values() if b == "1")
        assert c + phi - phi_antes == 4                  # costo amortizado
        phi_antes = phi
        total += c
        ms.append(m); pasos.append(c); totales.append(total); phis.append(phi)
    fig, (ax1, ax2) = grafica(8.4, 3.4, 1, 2)
    izq = 16
    ax1.bar(ms[:izq], pasos[:izq], color=t["calido"], width=0.7, label="costo real (pasos)")
    ax1.plot(ms[:izq], phis[:izq], "o-", color=t["acento"], lw=1.4, ms=4,
             label="potencial Φ = 2·(unos), después")
    ax1.axhline(4, color=t["tinta"], lw=1.4, ls="--", label="costo amortizado = 4")
    estilo(ax1, t, "Cada incremento", "incremento m", "pasos")
    leyenda(ax1, t, loc="upper left")
    ax1.set_ylim(0, 13)
    ax1.set_xticks(range(2, izq + 1, 2))
    ax2.plot(ms, [4 * m for m in ms], color=t["apagado"], lw=1.4, ls="--", label="4m")
    ax2.plot(ms, totales, color=t["calido"], lw=2.2, label="total real = 4m − 2·s₂(m)")
    assert all(T == 4 * m - 2 * bin(m).count("1") for m, T in zip(ms, totales))
    estilo(ax2, t, "La suma de m incrementos", "m", "pasos acumulados")
    leyenda(ax2, t, loc="upper left")
    fig.tight_layout(w_pad=2.5)
    return fig


# --------------------------------------------------------------------------
# Ejercicio 5. Los dos punteros sobre la ρ
# --------------------------------------------------------------------------

def fig_05_rho(t):
    import math
    e5 = ejercicio(5)
    mu, lam = 2, 3
    head, nodos = e5.construir(mu, lam)
    hay, vueltas = e5.floyd(head)
    assert hay

    def x(k):                       # el nodo x_k: k saltos desde la cabeza
        nodo = head
        for _ in range(k):
            nodo = nodo.next
        return nodo

    pos = {0: (0, 0), 1: (1.2, 0)}
    centro = (3.1, 0)
    for i in range(lam):            # el ciclo, empezando por x_mu a la izquierda
        ang = math.pi - 2 * math.pi * i / lam
        pos[mu + i] = (centro[0] + 0.95 * math.cos(ang), 0.95 * math.sin(ang))
    fig, ejes = plt.subplots(1, vueltas + 1, figsize=(10.0, 2.7))
    for k, ax in enumerate(ejes):
        ax.set_aspect("equal"); ax.axis("off")
        for nodo in nodos:
            a, b = pos[nodo.v], pos[nodo.next.v]
            ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=10,
                                         color=t["apagado"], lw=1.1, shrinkA=10, shrinkB=10,
                                         connectionstyle="arc3,rad=-0.25" if nodo.v >= mu else "arc3"))
        s, f = x(k), x(2 * k)
        for nodo in nodos:
            px, py = pos[nodo.v]
            borde = t["calido"] if nodo is f else (t["acento"] if nodo is s else t["tinta"])
            ax.add_patch(Circle((px, py), 0.28, facecolor=t["fondo"], edgecolor=borde,
                                lw=2.2 if nodo in (s, f) else 1.2, zorder=2))
            ax.text(px, py, str(nodo.v + 1), ha="center", va="center", fontsize=10,
                    color=t["tinta"], zorder=3)
        sx, sy = pos[s.v]
        fx, fy = pos[f.v]
        if s is f:
            ax.text(sx, sy + 0.45, "slow = fast", ha="center", fontsize=9,
                    color=t["calido"], fontweight="bold")
        else:
            ax.text(sx, sy + 0.45, "slow", ha="center", fontsize=9, color=t["acento"])
            ax.text(fx, fy - 0.6, "fast", ha="center", fontsize=9, color=t["calido"])
        ax.set_title(f"k = {k}", color=t["tinta"], fontsize=11, fontweight="bold")
        ax.set_xlim(-0.45, 4.4)
        ax.set_ylim(-1.35, 1.35)
    assert x(vueltas) is x(2 * vueltas)
    return fig


# --------------------------------------------------------------------------
# Ejercicio 7. Lo que descarta cada vuelta de la mediana
# --------------------------------------------------------------------------

def fig_07_corte(t):
    e7 = ejercicio(7)
    A, B = list(range(1, 16, 2)), list(range(2, 17, 2))
    n = len(A)
    registro = []

    class V(int):
        def __lt__(self, otro):
            registro.append((int(self), int(otro)))
            return int(self) < int(otro)

    mediana, comps = e7.mediana([V(a) for a in A], [V(b) for b in B], vigilar=False)
    pares = registro[-comps:]       # las del algoritmo (antes van las del sorted interno)
    assert mediana == sorted(A + B)[n - 1]
    ia = ib = 0
    filas = []
    for a, b in pares[:-1]:
        i, j = A.index(a), B.index(b)
        filas.append((ia, ib, n - ia - ib, i, j))
        if a < b:
            ia = i + 1
        else:
            ib = j + 1
    filas.append((ia, ib, 1, ia, ib))
    fig, ax = lienzo(8.0, 5.6)
    alto = 3.1
    for r, (ia_r, ib_r, k, i, j) in enumerate(filas):
        y0 = -r * alto
        final = r == len(filas) - 1
        for fila_y, L, inicio, mirado in ((y0 + 1.1, A, ia_r, i), (y0, B, ib_r, j)):
            for c, v in enumerate(L):
                vivo = c >= inicio
                es_mediana = final and v == mediana
                ax.add_patch(Rectangle((c, fila_y), 1, 1, edgecolor=t["regla"], lw=1,
                                       facecolor=t["suave"] if es_mediana else "none"))
                ax.text(c + 0.5, fila_y + 0.5, str(v), ha="center", va="center",
                        fontsize=10, color=t["tinta"] if vivo else t["apagado"],
                        alpha=1 if vivo else 0.45)
            ax.add_patch(Rectangle((mirado, fila_y), 1, 1, facecolor="none",
                                   edgecolor=t["calido"], lw=2.2))
        ax.text(-0.3, y0 + 1.6, "A", ha="right", va="center", fontsize=10,
                color=t["apagado"])
        ax.text(-0.3, y0 + 0.5, "B", ha="right", va="center", fontsize=10,
                color=t["apagado"])
        if final:
            rotulo = f"fin, k = 1: min({A[i]}, {B[j]}) = {mediana}"
        else:
            rotulo = f"vuelta {r + 1}: k = {k}, h = {k // 2}: compara {A[i]} con {B[j]}"
        ax.text(n + 0.4, y0 + 1.05, rotulo, va="center", fontsize=10,
                color=t["tinta"], fontweight="bold" if final else "normal")
    ax.set_xlim(-0.8, n + 7.2)
    ax.set_ylim(-(len(filas) - 1) * alto - 0.2, 2.3)
    return fig


# --------------------------------------------------------------------------
# Ejercicio 8. Qué generador atrapa la versión sin verificar
# --------------------------------------------------------------------------

def fig_08_generadores(t):
    import random
    e8 = ejercicio(8)
    random.seed(5)                  # el mismo banco de pruebas que imprime ejercicio-08.py
    nombres, fallos = [], []
    for nombre, (generar, lo, hi) in e8.generadores.items():
        casos = [generar(random.randint(lo, hi)) for _ in range(4000)]
        fallos.append(100 * sum(e8.sin_verificar(L) != e8.oraculo(L) for L in casos) / len(casos))
        assert all(e8.con_verificar(L) == e8.oraculo(L) for L in casos)
        nombres.append(nombre)
    fig, (ax,) = grafica(6.6, 3.2)
    ys = range(len(nombres))[::-1]
    colores = [t["alarma"] if f == 0 else t["calido"] for f in fallos]
    ax.barh(ys, fallos, color=colores, height=0.6)
    for y, f in zip(ys, fallos):
        ax.text(f + 0.8, y, coma(f) + " %", va="center", fontsize=9,
                color=t["alarma"] if f == 0 else t["tinta"],
                fontweight="bold" if f == 0 else "normal")
    ax.set_yticks(list(ys))
    ax.set_yticklabels(nombres)
    ax.set_xlim(0, 62)
    estilo(ax, t, "Listas en que la versión sin verificar se equivoca",
           "porcentaje de 4000 listas (la de dos pasadas: 0 % en todos)")
    ax.grid(axis="y", visible=False)
    return fig


# --------------------------------------------------------------------------
# Ejercicio 10. La rejilla en una dimensión
# --------------------------------------------------------------------------

def fig_10_rejilla(t):
    import math
    e10 = ejercicio(10)
    pts = [7, 2.5, 9.1, 2.6]
    fig, ejes = plt.subplots(2, 1, figsize=(7.6, 3.6))
    for ax, i in zip(ejes, (2, 3)):
        delta = e10.par_mas_cercano_1d(pts[:i], barajar=False)[0]
        nuevo = e10.par_mas_cercano_1d(pts[:i + 1], barajar=False)[0]
        p = pts[i]
        k = math.floor(p / delta)
        cercano = min(pts[:i], key=lambda q: abs(p - q))
        ax.axis("off")
        ultima = max(k + 2, math.ceil(max(pts) / delta))
        for c in range(ultima):
            revisada = c in (k - 1, k, k + 1)
            ax.add_patch(Rectangle((c * delta, -0.35), delta, 0.7, lw=1,
                                   edgecolor=t["regla"],
                                   facecolor=t["suave"] if revisada else "none"))
            ax.text((c + 0.5) * delta, -0.62, f"celda {c}", ha="center", fontsize=8,
                    color=t["acento"] if revisada else t["apagado"])
        num = lambda q: f"{q:g}".replace(".", ",")
        juntos = abs(p - cercano) < 0.5         # rótulos a cada lado para no pisarse
        for q in pts[:i]:
            ax.plot([q], [0], "o", color=t["tinta"], ms=7, zorder=3)
            lado = "right" if (juntos and q == cercano) else "center"
            ax.text(q, 0.5, num(q), ha=lado, fontsize=9, color=t["tinta"])
        ax.plot([p], [0], "o", color=t["calido"], ms=7, zorder=4)
        ax.text(p, 0.5, num(p), ha="left" if juntos else "center", fontsize=9,
                color=t["calido"], fontweight="bold")
        if not juntos:
            ax.annotate("", (cercano, 0.12), (p, 0.12),
                        arrowprops=dict(arrowstyle="<->", color=t["calido"], lw=1.4))
        ax.text(1.0 * ultima * delta + 0.3, 0,
                f"δ = {num(round(delta, 9))}: llega {num(p)} (celda {k})\n"
                f"revisa {k - 1}, {k}, {k + 1}; nuevo δ = {num(round(nuevo, 9))}",
                va="center", fontsize=9, color=t["tinta"])
        ax.set_xlim(-0.3, ultima * delta + 5.6)
        ax.set_ylim(-0.85, 0.85)
    fig.tight_layout(h_pad=1.0)
    return fig


# --------------------------------------------------------------------------
# Ejercicio 11. El tamaño de la tabla contra el tamaño de la entrada
# --------------------------------------------------------------------------

def fig_11_bits(t):
    bits = list(range(1, 65))
    casillas = [4 * (2 ** (b - 1) + 1) for b in bits]      # n = 3, W = 2^(b-1)
    divisiones = [2 ** (b / 2) for b in bits]
    fig, (ax,) = grafica(6.6, 3.6)
    ax.plot(bits, casillas, color=t["calido"], lw=2.2,
            label="mochila: casillas (n+1)(W+1), n = 3")
    ax.plot(bits, divisiones, color=t["acento"], lw=2.2,
            label="primalidad por división: √N = 2^(b/2)")
    ax.plot(bits, [b ** 3 for b in bits], color=t["apagado"], lw=1.4, ls="--",
            label="un polinomio en el tamaño: b³")
    ax.set_yscale("log")
    estilo(ax, t, "Costo en función del número de bits b del número",
           "b = bits de W (o de N)", "operaciones (escala logarítmica)")
    leyenda(ax, t, loc="upper left")
    return fig


# --------------------------------------------------------------------------
# Ejercicio 12. El ejemplo de tres proponentes
# --------------------------------------------------------------------------

def fig_12_emparejamiento(t):
    e12 = ejercicio(12)
    L = [[0], [0, 1], [0]]
    PB = [[2, 1, 0], [0, 1, 2], [0, 1, 2]]
    M, _ = e12.gale_shapley_incompleto(L, PB, orden="cola")
    assert not e12.bloqueantes(L, PB, M)
    n = len(L)
    fig, ax = lienzo(5.6, 3.2)
    ya = {a: n - 1 - a for a in range(n)}
    pareja_de_a = {a: b for b, a in enumerate(M) if a is not None}
    for a in range(n):
        for lugar, b in enumerate(L[a]):
            casado = pareja_de_a.get(a) == b
            ax.plot([0, 3], [ya[a], ya[b]], color=t["acento"] if casado else t["regla"],
                    lw=3 if casado else 1.4, zorder=1,
                    ls="-" if casado else (0, (4, 3)))
    for a in range(n):
        ax.add_patch(Circle((0, ya[a]), 0.27, facecolor=t["fondo"],
                            edgecolor=t["tinta"], lw=1.4, zorder=2))
        ax.text(0, ya[a], f"a{'₁₂₃'[a]}", ha="center", va="center", fontsize=10,
                color=t["tinta"], zorder=3)
        lista = ", ".join(f"b{'₁₂₃'[b]}" for b in L[a])
        estado = "" if a in pareja_de_a else "  (solo)"
        ax.text(-0.45, ya[a], f"[{lista}]{estado}", ha="right", va="center", fontsize=9,
                color=t["alarma"] if estado else t["apagado"])
    for b in range(n):
        ax.add_patch(Circle((3, ya[b]), 0.27, facecolor=t["fondo"],
                            edgecolor=t["tinta"], lw=1.4, zorder=2))
        ax.text(3, ya[b], f"b{'₁₂₃'[b]}", ha="center", va="center", fontsize=10,
                color=t["tinta"], zorder=3)
    ax.text(3.45, ya[0], "prefiere a₃ > a₂ > a₁", va="center", fontsize=9,
            color=t["apagado"])
    ax.text(3.45, ya[2], "nadie lo propone", va="center", fontsize=9, color=t["apagado"])
    ax.plot([], [], color=t["acento"], lw=3, label="pareja del resultado")
    ax.plot([], [], color=t["regla"], lw=1.4, ls=(0, (4, 3)), label="aceptable, sin pareja")
    leyenda(ax, t, loc="upper center", bbox_to_anchor=(0.5, 0.02), ncol=2)
    ax.set_xlim(-2.6, 6.0)
    ax.set_ylim(-0.6, n - 0.4)
    return fig


# --------------------------------------------------------------------------
# Ejercicio 13. El splay sobre el camino con n = 4, y el costo total
# --------------------------------------------------------------------------

def _forma(x):
    return None if x is None else (x.k, _forma(x.izq), _forma(x.der))


def _dibujar_arbol(ax, forma, t, ox, resaltar):
    def recorrer(f, prof):
        if f is None:
            return
        k, izq, der = f
        for hijo in (izq, der):
            if hijo:
                ax.plot([ox + k, ox + hijo[0]], [-prof, -prof - 1], color=t["apagado"],
                        lw=1.2, zorder=1)
        ax.add_patch(Circle((ox + k, -prof), 0.3, facecolor=t["suave"] if k == resaltar
                            else t["fondo"], edgecolor=t["calido"] if k == resaltar
                            else t["tinta"], lw=2 if k == resaltar else 1.2, zorder=2))
        ax.text(ox + k, -prof, str(k), ha="center", va="center", fontsize=10,
                color=t["tinta"], zorder=3)
        recorrer(izq, prof + 1)
        recorrer(der, prof + 1)
    recorrer(forma, 0)


def fig_13_arboles(t):
    e13 = ejercicio(13)
    n = 4
    nodos, raiz = e13.camino_izquierdo(n)
    paneles = [("inicio", _forma(raiz), None)]
    for k in range(1, n + 1):
        rot = e13.splay(nodos[k])
        paneles.append((f"acceso {k}: {rot} rot.", _forma(nodos[k]), k))
    assert paneles[-1][1] == paneles[0][1]          # vuelve al camino de partida
    fig, ax = lienzo(10.0, 2.8)
    for c, (titulo, forma, k) in enumerate(paneles):
        ox = c * 5.2 - 1
        _dibujar_arbol(ax, forma, t, ox, k)
        ax.text(ox + 2.5, 0.75, titulo, ha="center", fontsize=10, color=t["tinta"],
                fontweight="bold")
    ax.set_xlim(-0.6, len(paneles) * 5.2 - 1.2)
    ax.set_ylim(-3.5, 1.1)
    return fig


def fig_13_costos(t):
    import math
    e13 = ejercicio(13)
    ns = [4, 8, 16, 32, 64, 128, 256, 512, 1024]
    splay = [e13.accesos_en_orden(n, e13.splay)[0] for n in ns]
    subir = [(n - 1) * (n + 2) // 2 for n in ns]
    assert subir[:4] == [e13.accesos_en_orden(n, e13.subir_a_la_raiz)[0] for n in ns[:4]]
    cota = [4 * n * math.log2(n) + n for n in ns]
    fig, (ax,) = grafica(6.6, 3.6)
    ax.plot(ns, subir, "o-", color=t["alarma"], lw=2, ms=4, label="subir a la raíz: (n−1)(n+2)/2")
    ax.plot(ns, cota, "o", color=t["apagado"], lw=1.6, ms=4, ls="--",
            label="cota del lema: 4n log₂ n + n")
    ax.plot(ns, splay, "o-", color=t["calido"], lw=2.2, ms=4, label="splay (real)")
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_xticks(ns)
    ax.set_xticklabels([str(n) for n in ns])
    estilo(ax, t, "Rotaciones totales al acceder a 1, …, n en orden", "n",
           "rotaciones (escala logarítmica)")
    leyenda(ax, t, loc="upper left")
    return fig


# --------------------------------------------------------------------------
# Ejercicio 14. El grafo de estados y las cuatro varillas
# --------------------------------------------------------------------------

def fig_14_estados(t):
    import math
    from itertools import product
    e14 = ejercicio(14)
    n = 3
    esquinas = {0: (0, 0), 1: (1, math.sqrt(3)), 2: (2, 0)}   # varillas 1, 2 y 3

    def posicion(estado):
        """El disco mayor elige el subtriángulo; dentro de él se intercambian las
        esquinas de las otras dos varillas, para que el estado «los menores en la
        tercera varilla» quede en el vértice que toca al subtriángulo vecino."""
        x = y = 0.0
        esq = dict(esquinas)
        for i in reversed(range(len(estado))):
            v = estado[i]
            x += esq[v][0] * 2 ** i
            y += esq[v][1] * 2 ** i
            b, c = [w for w in range(3) if w != v]
            esq[b], esq[c] = esq[c], esq[b]
        return x, y

    estados = list(product(range(3), repeat=n))
    inicio = (0,) * n
    camino = [inicio] + list(e14.estados_de(e14.resolver(n), n))
    en_camino = {frozenset(p) for p in zip(camino, camino[1:])}
    fig, ax = lienzo(5.4, 4.8)
    for u in estados:
        for v in e14.vecinos(u, 3):
            if u < v:
                (x1, y1), (x2, y2) = posicion(u), posicion(v)
                bueno = frozenset((u, v)) in en_camino
                ax.plot([x1, x2], [y1, y2], color=t["calido"] if bueno else t["regla"],
                        lw=3 if bueno else 1.2, zorder=1 if not bueno else 2)
    for u in estados:
        x, y = posicion(u)
        ax.add_patch(Circle((x, y), 0.16, facecolor=t["fondo"],
                            edgecolor=t["calido"] if u in camino else t["apagado"],
                            lw=1.4, zorder=3))
    for estado, texto, dy, va in ((inicio, "todos en la varilla 1", -0.45, "top"),
                                  ((2,) * n, "todos en la varilla 3", -0.45, "top"),
                                  ((1,) * n, "todos en la varilla 2", 0.45, "bottom")):
        x, y = posicion(estado)
        ax.text(x, y + dy, texto, ha="center", va=va, fontsize=9, color=t["tinta"])
    alto = max(posicion(u)[1] for u in estados)
    ax.text(-0.6, alto, f"{len(estados)} estados (n = {n})\ncamino del algoritmo:\n"
            f"{len(camino) - 1} movimientos", fontsize=9, color=t["calido"], va="top")
    ax.set_xlim(-1.4, 15.4)
    ax.set_ylim(-1.2, alto + 1.0)
    return fig


def fig_14_varillas(t):
    e14 = ejercicio(14)
    ns = list(range(1, 8))
    tres = [e14.bfs(n, 3)[0] for n in ns]
    cuatro = [e14.bfs(n, 4)[0] for n in ns]
    assert tres == [2 ** n - 1 for n in ns]
    fig, (ax,) = grafica(6.6, 3.4)
    ax.plot(ns, tres, "o-", color=t["acento"], lw=2.2, label="3 varillas: 2ⁿ − 1")
    ax.plot(ns, cuatro, "o-", color=t["calido"], lw=2.2, label="4 varillas (BFS)")
    for n, a, b in zip(ns, tres, cuatro):
        ax.annotate(str(a), (n, a), textcoords="offset points", xytext=(-4, 7),
                    ha="right", fontsize=9, color=t["acento"])
        ax.annotate(str(b), (n, b), textcoords="offset points", xytext=(4, -13),
                    ha="left", fontsize=9, color=t["calido"])
    ax.set_xticks(ns)
    estilo(ax, t, "Mínimo de movimientos, por búsqueda en anchura", "discos n",
           "movimientos")
    leyenda(ax, t, loc="upper left")
    return fig


# --------------------------------------------------------------------------
# GIF animados: un cuadro por paso del algoritmo
# --------------------------------------------------------------------------

def guardar_gif(cuadros, nombre, pausa=1100, pausa_final=2600):
    """cuadros(t) devuelve una lista de figuras del mismo tamaño. Se guardan en
    figuras/<nombre>-<tema>.gif con el fondo del tema (un GIF no tiene alfa real)."""
    import numpy as np
    from PIL import Image
    os.makedirs(os.path.join(AQUI, "figuras"), exist_ok=True)
    for tema, t in TEMAS.items():
        imagenes = []
        for fig in cuadros(t):
            fig.patch.set_facecolor(t["fondo"])
            fig.canvas.draw()
            rgb = np.asarray(fig.canvas.buffer_rgba())[:, :, :3]
            imagenes.append(Image.fromarray(rgb).convert("P", palette=Image.ADAPTIVE,
                                                         colors=64))
            plt.close(fig)
        ruta = os.path.join(AQUI, "figuras", f"{nombre}-{tema}.gif")
        duraciones = [pausa] * (len(imagenes) - 1) + [pausa_final]
        imagenes[0].save(ruta, save_all=True, append_images=imagenes[1:],
                         duration=duraciones, loop=0, disposal=2)
        print("escrita", os.path.relpath(ruta, AQUI))


def gif_06_escalera(t):
    """La zona R donde puede estar x, vuelta por vuelta, con x = 15."""
    M = [[1, 4, 7, 11], [2, 5, 8, 12], [3, 6, 9, 16], [10, 13, 14, 17]]
    n, x = len(M), 15
    resultado, vistas = recorrido_escalera(M, x)
    assert resultado is None
    estados = [(i, j) for i, j in vistas] + [None]
    cuadros = []
    for r, estado in enumerate(estados):
        fig, ax = plt.subplots(figsize=(6.4, 2.9), dpi=100)
        ax.set_aspect("equal"); ax.axis("off")
        if estado is None:
            i, j = vistas[-1]
            i, j = (i + 1, j) if x > M[i][j] else (i, j - 1)
        else:
            i, j = estado
        dentro = {(a, b) for a in range(n) for b in range(n) if a >= i and b <= j}
        fondo = {c: t["suave"] for c in dentro}
        texto = {(a, b): t["apagado"] for a in range(n) for b in range(n)
                 if (a, b) not in dentro}
        _matriz(ax, M, t, fondo=fondo, texto=texto)
        if estado is not None:
            ax.add_patch(Rectangle((j, n - 1 - i), 1, 1, facecolor="none",
                                   edgecolor=t["calido"], lw=2.6))
            v = M[i][j]
            if x < v:
                efecto = f"{x} < {v}: descarta la columna {j}"
            elif x > v:
                efecto = f"{x} > {v}: descarta la fila {i}"
            else:
                efecto = f"{x} = {v}: está"
            linea1 = f"vuelta {r + 1}: compara x con M[{i}][{j}] = {v}"
        else:
            linea1, efecto = f"i = {i} = n: la zona quedó vacía", "devuelve «no está»"
        phi = (n - i) + (j + 1)
        ax.text(n + 0.4, n - 0.6, f"x = {x}", fontsize=12, fontweight="bold",
                color=t["tinta"])
        ax.text(n + 0.4, n - 1.6, linea1, fontsize=10, color=t["tinta"])
        ax.text(n + 0.4, n - 2.2, efecto, fontsize=10, color=t["calido"])
        ax.text(n + 0.4, n - 3.2, f"zona R (sombreada): filas ≥ {i}, columnas ≤ {j}",
                fontsize=9, color=t["acento"])
        ax.text(n + 0.4, n - 3.8, f"Φ = (n − i) + (j + 1) = {phi}", fontsize=9,
                color=t["acento"])
        ax.set_xlim(-0.2, n + 5.6)
        ax.set_ylim(-0.4, n + 0.3)
        cuadros.append(fig)
    return cuadros


def gif_05_floyd(t):
    """slow y fast sobre una ρ con cola 3 y ciclo 5, hasta que coinciden."""
    import math
    e5 = ejercicio(5)
    mu, lam = 3, 5
    head, nodos = e5.construir(mu, lam)
    hay, vueltas = e5.floyd(head)
    assert hay and vueltas == lam * math.ceil(max(mu, 1) / lam)

    def x(k):
        nodo = head
        for _ in range(k):
            nodo = nodo.next
        return nodo

    pos = {i: (1.2 * i, 0) for i in range(mu)}
    centro = (1.2 * mu + 1.25, 0)
    for i in range(lam):
        ang = math.pi - 2 * math.pi * i / lam
        pos[mu + i] = (centro[0] + 1.25 * math.cos(ang), 1.25 * math.sin(ang))
    cuadros = []
    for k in range(vueltas + 1):
        fig, ax = plt.subplots(figsize=(7.2, 3.2), dpi=100)
        ax.set_aspect("equal"); ax.axis("off")
        for nodo in nodos:
            ax.add_patch(FancyArrowPatch(pos[nodo.v], pos[nodo.next.v], arrowstyle="-|>",
                                         mutation_scale=10, color=t["apagado"], lw=1.1,
                                         shrinkA=11, shrinkB=11,
                                         connectionstyle="arc3,rad=-0.2"
                                         if nodo.v >= mu else "arc3"))
        s, f = x(k), x(2 * k)
        for nodo in nodos:
            px, py = pos[nodo.v]
            borde = t["calido"] if nodo is f else (t["acento"] if nodo is s else t["tinta"])
            ax.add_patch(Circle((px, py), 0.3, facecolor=t["fondo"], edgecolor=borde,
                                lw=2.4 if nodo in (s, f) else 1.2, zorder=2))
            ax.text(px, py, f"x{'₀₁₂₃₄₅₆₇₈₉'[nodo.v]}", ha="center", va="center",
                    fontsize=9, color=t["tinta"], zorder=3)
        (sx, sy), (fx, fy) = pos[s.v], pos[f.v]
        if s is f:
            ax.text(sx, sy + 0.5, "slow = fast", ha="center", fontsize=9,
                    color=t["calido"], fontweight="bold")
        else:
            ax.text(sx, sy + 0.5, "slow", ha="center", fontsize=9, color=t["acento"])
            ax.text(fx, fy - 0.68, "fast", ha="center", fontsize=9, color=t["calido"])
        derecha = centro[0] + 2.0
        ax.text(derecha, 1.0, f"k = {k}", fontsize=12, fontweight="bold", color=t["tinta"])
        ax.text(derecha, 0.4, f"slow = x{k}, fast = x{2 * k}".translate(
            str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")), fontsize=10, color=t["tinta"])
        if k >= max(mu, 1):
            ax.text(derecha, -0.2, f"Φ = (−k) mod λ = {(-k) % lam}", fontsize=10,
                    color=t["acento"])
        else:
            ax.text(derecha, -0.2, "slow todavía en la cola", fontsize=10,
                    color=t["apagado"])
        ax.text(derecha, -0.8, f"μ = {mu}, λ = {lam}, k* = {vueltas}", fontsize=9,
                color=t["apagado"])
        ax.set_xlim(-0.5, derecha + 3.6)
        ax.set_ylim(-1.7, 1.7)
        cuadros.append(fig)
    return cuadros


def gif_13_splay(t):
    """Splay y subir a la raíz lado a lado, acceso por acceso, con n = 8."""
    e13 = ejercicio(13)
    n = 8
    lados = []
    for reorganizar in (e13.splay, e13.subir_a_la_raiz):
        nodos, raiz = e13.camino_izquierdo(n)
        estados, total = [(_forma(raiz), None, 0, 0)], 0
        for k in range(1, n + 1):
            rot = reorganizar(nodos[k])
            total += rot
            estados.append((_forma(nodos[k]), k, rot, total))
        lados.append(estados)
    assert lados[1][-1][3] == (n - 1) * (n + 2) // 2
    altura = lambda f: -1 if f is None else 1 + max(altura(f[1]), altura(f[2]))
    assert (altura(lados[0][1][0]), altura(lados[1][1][0])) == (5, 7)   # pie de la figura
    assert (lados[0][-1][3], lados[1][-1][3]) == (22, 35)
    cuadros = []
    for c in range(n + 1):
        fig, ax = plt.subplots(figsize=(8.6, 4.2), dpi=100)
        ax.set_aspect("equal"); ax.axis("off")
        for lado, (titulo, estados) in enumerate((("splay", lados[0]),
                                                  ("subir a la raíz", lados[1]))):
            forma, k, rot, total = estados[c]
            ox = lado * (n + 2.5) - 0.5
            _dibujar_arbol(ax, forma, t, ox, k)
            ax.text(ox + (n + 1) / 2, 1.3, titulo, ha="center", fontsize=11,
                    fontweight="bold", color=t["tinta"])
            detalle = ("camino inicial" if k is None else
                       f"acceso {k}: {rot} {'rotación' if rot == 1 else 'rotaciones'}; "
                       f"total {total}")
            ax.text(ox + (n + 1) / 2, 0.7, detalle, ha="center", fontsize=9.5,
                    color=t["calido"])
        ax.set_xlim(-0.2, 2 * n + 3.2)
        ax.set_ylim(-n + 0.4, 1.8)
        cuadros.append(fig)
    return cuadros


def caminos_de_busqueda(buscar, A, xs):
    """Corre `buscar` con cada x y devuelve {x: (camino, resultado)}. El camino es
    la lista de (posición de A comparada, respuesta «<», «=» o «>»)."""
    caminos = {}
    for x in xs:
        miradas = []

        class Valor(int):
            def __eq__(self, otro):
                miradas.append(self.pos)
                return int(self) == int(otro)

            __hash__ = int.__hash__

        envueltos = []
        for i, a in enumerate(A):
            v = Valor(a)
            v.pos = i
            envueltos.append(v)
        resultado, comps = buscar(envueltos, x)
        assert comps == len(miradas)
        camino = [(m, "<" if x < A[m] else ("=" if x == A[m] else ">")) for m in miradas]
        caminos[x] = (camino, resultado)
    return caminos


def _arbol_decision(ax, A, caminos, t, resaltar=None, marcadas=(), mal=False):
    """Dibuja el árbol de decisión que forman los caminos. Un nodo es el prefijo de
    camino que lleva a él. La posición horizontal es el orden: A[m] va en 2m + 1 y el
    hueco i en 2i, así que una hoja que reúne varios huecos queda en su promedio."""
    nodos, hojas = {}, {}
    for x, (camino, _) in caminos.items():
        for d, (m, _) in enumerate(camino):
            nodos[tuple(camino[:d])] = m
        if camino[-1][1] != "=":
            hojas.setdefault(tuple(camino), set()).add(sum(a < x for a in A))
    paso = 1.35                                     # separación entre niveles
    lugar = {pre: (2 * m + 1, -paso * len(pre)) for pre, m in nodos.items()}
    for hoja, huecos in hojas.items():
        lugar[hoja] = (sum(2 * h for h in huecos) / len(huecos), -paso * len(hoja))
    activo = set()
    if resaltar is not None:
        camino = caminos[resaltar][0]
        activo = {tuple(camino[:d]) for d in range(len(camino) + 1)}
    fuerte = t["alarma"] if mal else t["calido"]
    for pre, m in nodos.items():
        px, py = lugar[pre]
        for resp in "<>":
            hijo = pre + ((m, resp),)
            if hijo not in lugar:
                continue
            hx, hy = lugar[hijo]
            on = pre in activo and hijo in activo
            ax.plot([px, hx], [py, hy], color=fuerte if on else t["regla"],
                    lw=2.6 if on else 1.3, zorder=1)
            ax.text((px + hx) / 2 + (-0.35 if resp == "<" else 0.35), (py + hy) / 2 + 0.1,
                    resp, ha="center", fontsize=8, color=t["apagado"])
        ax.plot([px, px], [py, py - 0.42], color=t["regla"], lw=1.1, ls=(0, (2, 2)),
                zorder=1)
        ax.text(px, py - 0.58, "=", ha="center", fontsize=8, color=t["apagado"])
        ax.add_patch(Circle((px, py), 0.42, facecolor=t["fondo"],
                            edgecolor=fuerte if pre in activo else t["tinta"],
                            lw=2.2 if pre in activo else 1.2, zorder=2))
        ax.text(px, py, str(A[m]), ha="center", va="center", fontsize=10,
                color=t["tinta"], zorder=3)
    for hoja, huecos in hojas.items():
        hx, hy = lugar[hoja]
        on, marcada = hoja in activo, hoja in marcadas
        ancho = 1.0 + 0.8 * (len(huecos) - 1)
        ax.add_patch(Rectangle((hx - ancho / 2, hy - 0.3), ancho, 0.6, zorder=2,
                               facecolor=t["suave"] if (on or marcada) else t["fondo"],
                               edgecolor=fuerte if on else (t["acento"] if marcada
                                                            else t["apagado"]),
                               lw=2.2 if on else 1.2))
        ax.text(hx, hy, " ∪ ".join(f"h{'₀₁₂₃₄₅₆₇₈₉'[h]}" for h in sorted(huecos)),
                ha="center", va="center", fontsize=8.5, color=t["tinta"], zorder=3)


def gif_02_hojas(t):
    """Cada hueco llega a su propia hoja en el árbol de la búsqueda binaria."""
    e2 = ejercicio(2)
    A = [1, 3, 5, 7, 9, 11, 13]
    xs = list(range(0, 15))
    caminos = caminos_de_busqueda(lambda B, x: e2.busqueda_binaria(B, x, vigilar=False),
                                  A, xs)
    huecos = [x for x in xs if x not in A]
    hojas = [tuple(caminos[x][0]) for x in huecos]
    assert len(set(hojas)) == len(A) + 1 == 8                  # n + 1 hojas distintas
    assert {len(h) for h in hojas} == {3}                       # todas a profundidad 3

    def intervalo(i):
        if i == 0:
            return f"x < {A[0]}"
        if i == len(A):
            return f"x > {A[-1]}"
        return f"{A[i - 1]} < x < {A[i]}"

    cuadros = []
    for c in range(len(huecos) + 2):
        fig, ax = plt.subplots(figsize=(8.4, 3.7), dpi=100)
        ax.set_aspect("equal"); ax.axis("off")
        if 1 <= c <= len(huecos):
            x = huecos[c - 1]
            i = sum(a < x for a in A)
            marcadas = set(hojas[:c - 1])
            _arbol_decision(ax, A, caminos, t, resaltar=x, marcadas=marcadas)
            linea = f"x = {x} cae en el hueco h{'₀₁₂₃₄₅₆₇₈'[i]} ({intervalo(i)}): llega a su propia hoja"
        else:
            marcadas = set(hojas) if c else set()
            _arbol_decision(ax, A, caminos, t, marcadas=marcadas)
            linea = ("A = [1, 3, 5, 7, 9, 11, 13]: árbol de decisión de la búsqueda binaria"
                     if c == 0 else
                     "8 huecos, 8 hojas distintas: con altura h hay a lo sumo 2ʰ hojas, así que h ≥ 3")
        ax.text(7, 0.85, linea, ha="center", fontsize=10.5, color=t["tinta"],
                fontweight="bold" if c == len(huecos) + 1 else "normal")
        ax.set_xlim(-0.9, 14.9)
        ax.set_ylim(-4.55, 1.25)
        cuadros.append(fig)
    return cuadros


def gif_02_contradiccion(t):
    """Lema 2: un algoritmo que nunca mira A[5] = 11 lleva 10, 12 y 11 a la misma hoja."""
    e2 = ejercicio(2)
    A, k = [1, 3, 5, 7, 9, 11, 13], 5
    xs = list(range(0, 15))
    caminos = caminos_de_busqueda(lambda B, x: e2.busqueda_sin(B, k, x), A, xs)
    assert caminos[10][0] == caminos[12][0] == caminos[11][0]     # la misma hoja
    assert caminos[11][1][0] == "no está" and A[k] == 11          # y se equivoca
    hoja = tuple(caminos[10][0])
    pasos = [(None, "Un algoritmo que nunca compara con A[5] = 11", False),
             (10, "x₁ = 10 (hueco h₅: 9 < x < 11) llega a una hoja «no está»", False),
             (12, "x₂ = 12 (hueco h₆: 11 < x < 13) llega a la misma hoja", False),
             (11, "x = 11 = A[5] recibe las mismas respuestas: misma hoja, dice «no está»", True),
             (None, "pero 11 está en A: el algoritmo se equivoca (Lema 2)", True)]
    cuadros = []
    for x, linea, mal in pasos:
        fig, ax = plt.subplots(figsize=(8.4, 3.7), dpi=100)
        ax.set_aspect("equal"); ax.axis("off")
        _arbol_decision(ax, A, caminos, t, resaltar=11 if mal else x,
                        marcadas={hoja} if (x is not None or mal) else (), mal=mal)
        ax.text(7, 0.85, linea, ha="center", fontsize=10.5,
                color=t["alarma"] if mal else t["tinta"],
                fontweight="bold" if mal else "normal")
        ax.set_xlim(-0.9, 14.9)
        ax.set_ylim(-4.55, 1.25)
        cuadros.append(fig)
    return cuadros


GIFS = {
    2: [("ejercicio-02-hojas", gif_02_hojas),
        ("ejercicio-02-contradiccion", gif_02_contradiccion)],
    5: [("ejercicio-05-floyd", gif_05_floyd)],
    6: [("ejercicio-06-escalera-animada", gif_06_escalera)],
    13: [("ejercicio-13-splay-animado", gif_13_splay)],
}


FIGURAS = {
    1: [("ejercicio-01-factor", fig_01_factor)],
    2: [("ejercicio-02-rango", fig_02_rango)],
    3: [("ejercicio-03-pilas", fig_03_pilas)],
    4: [("ejercicio-04-costos", fig_04_costos)],
    5: [("ejercicio-05-rho", fig_05_rho)],
    6: [("ejercicio-06-escalera", fig_06_escalera),
        ("ejercicio-06-adversario", fig_06_adversario)],
    7: [("ejercicio-07-corte", fig_07_corte)],
    8: [("ejercicio-08-generadores", fig_08_generadores)],
    9: [("ejercicio-09-intercalado", fig_09_intercalado)],
    10: [("ejercicio-10-rejilla", fig_10_rejilla)],
    11: [("ejercicio-11-bits", fig_11_bits)],
    12: [("ejercicio-12-emparejamiento", fig_12_emparejamiento)],
    13: [("ejercicio-13-arboles", fig_13_arboles),
         ("ejercicio-13-costos", fig_13_costos)],
    14: [("ejercicio-14-estados", fig_14_estados),
         ("ejercicio-14-varillas", fig_14_varillas)],
}

if __name__ == "__main__":
    pedidos = [int(a) for a in sys.argv[1:]] or sorted(FIGURAS)
    for k in pedidos:
        for nombre, dibujar in FIGURAS[k]:
            guardar(dibujar, nombre)
        for nombre, cuadros in GIFS.get(k, []):
            guardar_gif(cuadros, nombre)
