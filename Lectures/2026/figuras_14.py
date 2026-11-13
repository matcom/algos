"""Figuras del capítulo 14: flujo máximo con push-relabel.

Cada función recibe el estado que calculó el código del capítulo (las alturas, los
excesos y las capacidades residuales de cada paso) y no decide nada del algoritmo.
"""

import math

from tesserax import Canvas, Circle, Colors, Line, Point

from figuras import (
    ACENTO, ALARMA, APAGADO, CALIDO, CUERPO, OSCURO, PIE, REGLA, TINTA,
    _figura, _punto, _txt, sub,
)


# --------------------------------------------------------------------------
# 1. la red con cada vértice dibujado a su altura, en varios momentos
# --------------------------------------------------------------------------

def _recortar(a, b, r):
    """El segmento de a a b sin los r primeros ni los r últimos puntos."""
    d = math.hypot(b.x - a.x, b.y - a.y) or 1.0
    ux, uy = (b.x - a.x) / d, (b.y - a.y) / d
    return Point(a.x + r * ux, a.y + r * uy), Point(b.x - r * ux, b.y - r * uy)


def alturas(momentos, aristas, nombres, s, t, ident="pr-alturas", pie=""):
    """`momentos`: lista de (título, h, e, cap) con h, e por vértice y cap la lista
    de capacidades residuales de la Red (la arista i de `aristas` es la 2i, y su
    flujo es cap[2i + 1])."""
    n = len(nombres)
    dx, dy = 36.0, 15.0
    hmax = max(max(h) for _, h, _, _ in momentos)
    ancho_panel = dx * (n - 1) + 44
    with Canvas() as canvas:
        for p, (titulo, h, e, cap) in enumerate(momentos):
            x0 = p * ancho_panel
            pos = [Point(x0 + i * dx, (hmax - h[i]) * dy) for i in range(n)]
            # rejilla de alturas y la línea de V
            for k in range(hmax + 1):
                y = (hmax - k) * dy
                Line(Point(x0 - 8, y), Point(x0 + dx * (n - 1) + 8, y),
                     stroke=ALARMA if k == n else REGLA,
                     width=0.9 if k == n else 0.5)
                if p == 0:
                    _txt(str(k), Point(x0 - 14, y), color=APAGADO, size=PIE,
                         anchor="end")
            _txt("V", Point(x0 + dx * (n - 1) + 14, (hmax - n) * dy),
                 color=ALARMA, size=PIE, anchor="start")
            for i, (u, v, c) in enumerate(aristas):
                f = cap[2 * i + 1]
                lleno = f == c
                a, b = _recortar(pos[u], pos[v], 5.5)
                Line(a, b, stroke=OSCURO if lleno else (ACENTO if f > 0 else APAGADO),
                     width=0.8, marker_end="arrow")
            for i in range(n):
                activo = i not in (s, t) and e[i] > 0
                Circle(4.5, fill=CALIDO if activo else Colors.White,
                       stroke=CALIDO if activo else TINTA,
                       width=1.0).move_to(pos[i])
                _txt(nombres[i], Point(pos[i].x, pos[i].y - 12), size=CUERPO,
                     color=TINTA)
                if activo:
                    _txt(f"+{e[i]}", Point(pos[i].x + 6, pos[i].y + 10),
                         color=CALIDO, size=CUERPO, anchor="start")
            _txt(titulo, Point(x0 + dx * (n - 1) / 2, hmax * dy + 24),
                 color=APAGADO, size=CUERPO)
    return _figura(canvas, ident, pie)


# --------------------------------------------------------------------------
# 2. el potencial paso a paso
# --------------------------------------------------------------------------

COLOR_OP = {"reetiquetar": CALIDO, "saturante": ACENTO, "no saturante": OSCURO}


def potencial(pasos, ident="pr-potencial", pie=""):
    """`pasos`: lista de (operación, Φ después de la operación); el primero es
    ("inicio", Φ₀)."""
    ancho, alto = 330.0, 120.0
    tope = max(p for _, p in pasos) or 1
    sx = ancho / (len(pasos) - 1)
    sy = alto / tope
    P = lambda i, phi: Point(i * sx, alto - phi * sy)
    with Canvas() as canvas:
        for k in range(0, tope + 1, 5):
            Line(P(0, k), P(len(pasos) - 1, k), stroke=REGLA, width=0.5)
            _txt(str(k), Point(-6, alto - k * sy), color=APAGADO, size=PIE,
                 anchor="end")
        Line(P(0, 0), P(len(pasos) - 1, 0), stroke=APAGADO, width=0.9)
        for i in range(1, len(pasos)):
            op, phi = pasos[i]
            antes = pasos[i - 1][1]
            color = COLOR_OP[op]
            Line(P(i - 1, antes), P(i, antes), stroke=APAGADO, width=0.7)
            Line(P(i, antes), P(i, phi), stroke=color, width=2.4)
            _punto(P(i, phi), color, r=2.0)
        for j, (op, color) in enumerate(COLOR_OP.items()):
            _txt(op, Point(ancho + 12, 10 + 14 * j), color=color, size=PIE,
                 anchor="start")
        _txt("operación", Point(ancho / 2, alto + 14), color=APAGADO, size=PIE)
        _txt("Φ", Point(-6, -10), color=APAGADO, size=CUERPO, anchor="end")
    return _figura(canvas, ident, pie)
