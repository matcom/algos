"""Figuras del capítulo 22: TSP métrico y redondeo de programas lineales.

Cada figura recibe lo que calculó el código del capítulo: el árbol mínimo, el
preorden y el recorrido del doble árbol; los vértices impares, el emparejamiento y el
recorrido de Christofides; y los vértices del poliedro que salieron de enumerar las
soluciones básicas.
"""

import itertools
import math
from fractions import Fraction

from tesserax import Arrow, Canvas, Circle, Colors, Line, Point

from figuras import (
    ACENTO, APAGADO, CALIDO, CUERPO, OSCURO, PIE, REGLA, TINTA, Marco,
    _figura, _punto, _txt,
)

_ANCHO, _ALTO, _SEP = 250.0, 220.0, 40.0


def _punteada(p, q, color=APAGADO, width=0.9, paso=3.0):
    """tesserax no tiene dasharray: la línea de trazos se hace con segmentos."""
    largo = math.hypot(q.x - p.x, q.y - p.y)
    k = max(1, int(largo / (2 * paso)))
    for i in range(k):
        t0, t1 = (2 * i) / (2 * k), (2 * i + 1) / (2 * k)
        Line(Point(p.x + (q.x - p.x) * t0, p.y + (q.y - p.y) * t0),
             Point(p.x + (q.x - p.x) * t1, p.y + (q.y - p.y) * t1),
             stroke=color, width=width)


def _panel(P, dx):
    marco = Marco(P, ancho=_ANCHO, alto=_ALTO, margen=22.0)
    return lambda p: Point(marco(p).x + dx, marco(p).y)


def _flecha(a, b, color, width=1.3, recorte=5.0):
    largo = math.hypot(b.x - a.x, b.y - a.y)
    ux, uy = (b.x - a.x) / largo, (b.y - a.y) / largo
    Arrow(Point(a.x + ux * recorte, a.y + uy * recorte),
          Point(b.x - ux * recorte, b.y - uy * recorte),
          stroke=color, width=width, marker_end="arrow")


def _gira(f, P, gira, color):
    for a, b in zip(gira, gira[1:] + gira[:1]):
        _flecha(f(P[a]), f(P[b]), color)


def _titulo(texto, dx):
    _txt(texto, Point(dx + _ANCHO / 2, -6), color=APAGADO, size=CUERPO)


def doble_arbol(P, arbol, orden, ident="tsp-doble-arbol", pie=""):
    """`arbol`: aristas del árbol mínimo; `orden`: el preorden, que es la gira."""
    izq, der = _panel(P, 0.0), _panel(P, _ANCHO + _SEP)
    pos = {v: k for k, v in enumerate(orden)}
    with Canvas() as canvas:
        _titulo("árbol mínimo y preorden", 0.0)
        for u, v in arbol:
            Line(izq(P[u]), izq(P[v]), stroke=OSCURO, width=2.2)
        for v, p in enumerate(P):
            q = izq(p)
            _punto(q, color=OSCURO, r=3.2)
            # la etiqueta va en la dirección más lejana de las aristas que llegan a v
            angulos = [math.atan2(izq(P[w if u == v else u]).y - q.y,
                                  izq(P[w if u == v else u]).x - q.x)
                       for u, w in arbol if v in (u, w)]
            def holgura(a):
                return min(abs((a - b + math.pi) % (2 * math.pi) - math.pi)
                           for b in angulos)
            mejor = max((k * math.pi / 8 for k in range(16)), key=holgura)
            ux, uy = math.cos(mejor), math.sin(mejor)
            _txt(str(pos[v] + 1), Point(q.x + 10 * ux, q.y + 10 * uy), color=OSCURO,
                 size=CUERPO)
        _titulo("recorrido con atajos", _ANCHO + _SEP)
        for u, v in arbol:
            _punteada(der(P[u]), der(P[v]), color=REGLA.darker(0.25), width=1.6)
        _gira(der, P, orden, CALIDO)
        for v, p in enumerate(P):
            _punto(der(p), color=OSCURO if v == orden[0] else TINTA, r=3.2)
    return _figura(canvas, ident, pie)


def christofides(P, arbol, impares, M, gira, ident="tsp-christofides", pie=""):
    """`impares`: vértices de grado impar del árbol; `M`: su emparejamiento mínimo;
    `gira`: el recorrido final, después de los atajos."""
    izq, der = _panel(P, 0.0), _panel(P, _ANCHO + _SEP)
    with Canvas() as canvas:
        _titulo("árbol + emparejamiento de los impares", 0.0)
        for u, v in arbol:
            Line(izq(P[u]), izq(P[v]), stroke=OSCURO, width=2.2)
        for u, v in M:
            Line(izq(P[u]), izq(P[v]), stroke=CALIDO, width=2.2)
        for v, p in enumerate(P):
            q = izq(p)
            if v in impares:
                Circle(6, fill=Colors.White, stroke=CALIDO, width=1.6).move_to(q)
            _punto(q, color=TINTA, r=2.6)
        y = _ALTO + 12
        Line(Point(10, y), Point(30, y), stroke=OSCURO, width=2.2)
        _txt("árbol", Point(35, y), color=OSCURO, size=CUERPO, anchor="start")
        Line(Point(85, y), Point(105, y), stroke=CALIDO, width=2.2)
        _txt("emparejamiento", Point(110, y), color=CALIDO, size=CUERPO, anchor="start")
        Circle(5, fill=Colors.White, stroke=CALIDO, width=1.6).move_to(Point(200, y))
        _txt("impar", Point(208, y), color=CALIDO, size=CUERPO, anchor="start")
        _titulo("circuito euleriano con atajos", _ANCHO + _SEP)
        _gira(der, P, gira, ACENTO)
        for v, p in enumerate(P):
            _punto(der(p), color=TINTA, r=3.2)
    return _figura(canvas, ident, pie)


def _rango(filas):
    M = [list(f) for f in filas]
    r = 0
    for c in range(len(M[0]) if M else 0):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c] / M[r][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        r += 1
    return r


def _etiqueta(x):
    return "(" + ", ".join("½" if v == Fraction(1, 2) else str(int(v)) for v in x) + ")"


def poliedro(vertices, restricciones, ident="tsp-poliedro", pie=""):
    """`vertices`: los del poliedro de vertex cover del triángulo, en el cubo
    [0,1]³; `restricciones`: pares (a, r) con a·x >= r. Dos vértices van unidos si
    las restricciones activas en los dos tienen rango 2 (forman una arista)."""
    L = 150.0

    def proy(x):
        x0, x1, x2 = (float(v) for v in x)
        return Point(L * (x0 + 0.42 * x1), -L * (x2 + 0.30 * x1))

    def activas(x):
        return [a for a, r in restricciones if sum(ai * xi for ai, xi in zip(a, x)) == r]

    with Canvas() as canvas:
        for u, v in itertools.combinations(itertools.product((0, 1), repeat=3), 2):
            if sum(a != b for a, b in zip(u, v)) == 1:
                _punteada(proy(u), proy(v), color=REGLA.darker(0.15), width=0.8)
        for u, v in itertools.combinations(vertices, 2):
            comunes = [a for a in activas(u) if a in activas(v)]
            if comunes and _rango(comunes) == 2:
                Line(proy(u), proy(v), stroke=OSCURO, width=1.4)
        for x in vertices:
            fracc = any(v == Fraction(1, 2) for v in x)
            p = proy(x)
            Circle(4.2, fill=CALIDO if fracc else OSCURO,
                   stroke=CALIDO if fracc else OSCURO).move_to(p)
            dx = 8 if x[0] >= 1 else -8
            _txt(_etiqueta(x), Point(p.x + dx, p.y - 8),
                 color=CALIDO if fracc else OSCURO, size=CUERPO,
                 anchor="start" if dx > 0 else "end")
        o = proy((0, 0, 0))
        for k, eje in enumerate(("x₀", "x₁", "x₂")):
            e = [0, 0, 0]
            e[k] = 1.18
            _flecha(o, proy(e), APAGADO, width=0.8, recorte=0.0)
            q = proy(e)
            _txt(eje, Point(q.x + 8, q.y), color=APAGADO, size=CUERPO)
    return _figura(canvas, ident, pie)
