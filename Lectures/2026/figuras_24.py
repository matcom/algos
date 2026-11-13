"""Figuras del epílogo: problemas abiertos.

La figura recibe la tabla de cotas que imprime el propio epílogo, con su año y su
estado (publicada, preprint o manuscrito sin revisar), y no inventa ningún punto.
"""

from tesserax import Canvas, Line, Point

from figuras import (
    ACENTO, ALARMA, APAGADO, CALIDO, CUERPO, OSCURO, PIE, REGLA, TINTA,
    _figura, _punto, _txt,
)

_COLOR = {"publicada": OSCURO, "preprint": CALIDO, "sin revisar": ALARMA}


def omega(cotas, ident="epi-omega", pie=""):
    """`cotas`: lista de (año, cota, etiqueta, estado). Eje x: año; eje y: la cota
    superior de ω. Los puntos del mismo año se separan en x para que se lean."""
    x0, x1, y0, y1 = 1965, 2030, 2.0, 2.85
    W, H = 440.0, 250.0
    X = lambda a: (a - x0) / (x1 - x0) * W
    Y = lambda w: H - (w - y0) / (y1 - y0) * H
    with Canvas() as canvas:
        Line(Point(0, H), Point(W, H), stroke=TINTA, width=0.9)
        Line(Point(0, 0), Point(0, H), stroke=TINTA, width=0.9)
        for a in range(1970, 2031, 10):
            Line(Point(X(a), H), Point(X(a), H + 4), stroke=TINTA, width=0.8)
            _txt(str(a), Point(X(a), H + 13), color=APAGADO, size=PIE)
        for w in (2.0, 2.2, 2.4, 2.6, 2.8):
            Line(Point(-4, Y(w)), Point(0, Y(w)), stroke=TINTA, width=0.8)
            Line(Point(0, Y(w)), Point(W, Y(w)), stroke=REGLA, width=0.5)
            _txt(f"{w:.1f}".replace(".", ","), Point(-7, Y(w)), color=APAGADO,
                 size=PIE, anchor="end")
        _txt("cota superior de ω", Point(4, -10), color=APAGADO, size=PIE,
             anchor="start")
        # ω = 2 es la cota mínima trivial: hay que leer las n² entradas
        for xa in range(0, int(W), 8):   # tesserax no tiene dasharray: segmentos
            Line(Point(xa, Y(2.0)), Point(min(xa + 5, W), Y(2.0)), stroke=ACENTO,
                 width=1.2)
        _txt("ω ≥ 2: leer las n² entradas", Point(W - 4, Y(2.0) - 8), color=ACENTO,
             size=PIE, anchor="end")
        # puntos y escalera
        orden = sorted(cotas, key=lambda c: (c[0], -c[1]))
        visto = {}
        prev = None
        for anio, w, etq, estado in orden:
            k = visto.get(anio, 0)
            visto[anio] = k + 1
            x = X(anio)
            p = Point(x, Y(w))
            if prev is not None:
                Line(Point(prev.x, prev.y), Point(x, prev.y), stroke=REGLA.darker(0.2),
                     width=0.8)
                Line(Point(x, prev.y), p, stroke=REGLA.darker(0.2), width=0.8)
            _punto(p, color=_COLOR[estado], r=3.0)
            prev = p
        # etiquetas: las de puntos aislados al lado; el racimo 2024-2026 en una lista
        aislados = [c for c in orden if c[0] < 2020]
        racimo = [c for c in orden if c[0] >= 2020 and c[1] > 2.3]
        bajo = [c for c in orden if c[1] <= 2.3]
        for anio, w, etq, estado in aislados:
            _txt(etq, Point(X(anio) + 7, Y(w) - 2), color=_COLOR[estado], size=CUERPO,
                 anchor="start")
        xr, yr = X(1993), Y(2.66)
        for i, (anio, w, etq, estado) in enumerate(racimo):
            _txt(f"{anio}: {etq}", Point(xr, yr + 12 * i), color=_COLOR[estado],
                 size=CUERPO, anchor="start")
        for anio, w, etq, estado in bajo:
            _txt(etq, Point(X(anio) - 7, Y(w) + 1), color=_COLOR[estado], size=CUERPO,
                 anchor="end")
        # leyenda
        ly = H + 30
        for i, (estado, color) in enumerate(_COLOR.items()):
            x = 20 + i * 130
            _punto(Point(x, ly), color=color, r=3.0)
            _txt(estado, Point(x + 7, ly), color=color, size=CUERPO, anchor="start")
    return _figura(canvas, ident, pie)
