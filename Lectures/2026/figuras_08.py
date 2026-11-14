"""Figuras del capítulo 8: algoritmos aleatorios I, Las Vegas y costo esperado.

Cada función recibe el estado que calculó el código del capítulo: el orden real en
que una corrida eligió los pivotes, las comparaciones contadas en 10 000 corridas y
las probabilidades de colisión enumeradas sobre cada familia.
"""

from tesserax import Canvas, Colors, Line, Point, Rect

from figuras import (
    ACENTO, ALARMA, APAGADO, CALIDO, CUERPO, OSCURO, PIE, REGLA, TINTA,
    _figura, _punto, _txt, sub,
)


def pivotes_intervalo(n, orden, comparado, no_comparado, ident="lv-pivotes", pie=""):
    """`orden[r]` es en qué turno el elemento de rango r (1..n) fue pivote.
    `comparado` y `no_comparado` son pares (i, j) de rangos."""
    lado, paso = 24.0, 32.0
    cx = lambda r: (r - 1) * paso + paso / 2
    with Canvas() as canvas:
        _txt("turno en que fue pivote", Point(-10, -lado / 2 - 12), color=APAGADO,
             size=CUERPO, anchor="end")
        for r in range(1, n + 1):
            c = Point(cx(r), 0)
            Rect(lado, lado, fill=Colors.White, stroke=TINTA, width=0.9).move_to(c)
            _txt(f"z{sub(r)}", c, size=CUERPO)
            _txt(str(orden[r]) if r in orden else "·", Point(cx(r), -lado / 2 - 12),
                 color=APAGADO, size=CUERPO)
        for fila, ((i, j), color, texto) in enumerate([
                (comparado, OSCURO, "se comparan"),
                (no_comparado, ALARMA, "no se comparan")]):
            y = lado / 2 + 18 + fila * 34
            primero = min((r for r in range(i, j + 1) if r in orden),
                          key=lambda r: orden[r])
            Line(Point(cx(i) - lado / 2, y), Point(cx(j) + lado / 2, y),
                 stroke=color, width=1.4)
            for r in (i, j):
                Line(Point(cx(r), y - 5), Point(cx(r), y + 5), stroke=color, width=1.4)
            _punto(Point(cx(primero), y), color, r=4.0)
            _txt(f"z{sub(i)}…z{sub(j)}: el primer pivote es z{sub(primero)}, {texto}",
                 Point((cx(i) + cx(j)) / 2, y + 15), color=color, size=CUERPO)
    return _figura(canvas, ident, pie)


def histograma(valores, marcas, cubetas=30, ident="lv-histograma", pie=""):
    """`marcas` es una lista de (nombre, valor, color) que se dibujan como rectas."""
    ancho, alto = 300.0, 120.0
    lo = min(min(valores), min(v for _, v, _ in marcas))
    hi = max(max(valores), max(v for _, v, _ in marcas))
    w = (hi - lo) / cubetas
    cuenta = [0] * cubetas
    for v in valores:
        cuenta[min(int((v - lo) / w), cubetas - 1)] += 1
    tope = max(cuenta) * 1.1
    x = lambda v: (v - lo) / (hi - lo) * ancho
    with Canvas() as canvas:
        Line(Point(0, alto), Point(ancho, alto), stroke=APAGADO, width=1.0)
        for k, c in enumerate(cuenta):
            h = c / tope * alto
            if h > 0:
                Rect(ancho / cubetas, h, fill=ACENTO.transparent(0.25), stroke=OSCURO,
                     width=0.6).move_to(Point(k * ancho / cubetas, alto - h),
                                        anchor="topleft")
        for t in range(int(lo // 200 + 1) * 200, int(hi) + 1, 200):
            Line(Point(x(t), alto), Point(x(t), alto + 4), stroke=APAGADO, width=0.8)
            _txt(str(t), Point(x(t), alto + 12), color=APAGADO, size=CUERPO)
        for fila, (nombre, v, color) in enumerate(marcas):
            Line(Point(x(v), -6 - 15 * fila), Point(x(v), alto), stroke=color,
                 width=1.3)
            _txt(f"{nombre} = {v:,.0f}".replace(",", " "),
                 Point(x(v) + 4, -10 - 15 * fila), color=color, size=CUERPO,
                 anchor="start")
        _txt("comparaciones", Point(ancho, alto + 27), color=APAGADO, size=CUERPO,
             anchor="end")
        _txt(f"{max(cuenta)} corridas", Point(-6, alto - max(cuenta) / tope * alto),
             color=APAGADO, size=CUERPO, anchor="end")
    return _figura(canvas, ident, pie)


def _color_prob(p, m):
    if p == 0:
        return Colors.White
    if p <= 1 / m + 1e-12:
        return ACENTO.transparent(1 - 0.85 * p * m)
    return ALARMA.transparent(1 - p)


def colisiones(paneles, m, ident="lv-colisiones", pie=""):
    """`paneles` es una lista de (título, matriz) con matriz[x][y] la probabilidad
    de que x e y caigan en la misma cubeta."""
    celda, sep = 6.0, 60.0
    with Canvas() as canvas:
        for k, (titulo, M) in enumerate(paneles):
            u = len(M)
            x0 = k * (u * celda + sep)
            _txt(titulo, Point(x0 + u * celda / 2, -18), size=CUERPO)
            for x in range(u):
                for y in range(u):
                    if x == y:
                        continue
                    Rect(celda, celda, fill=_color_prob(M[x][y], m), stroke=REGLA,
                         width=0.15).move_to(Point(x0 + y * celda, x * celda),
                                             anchor="topleft")
            Rect(u * celda, u * celda, fill=Colors.Transparent, stroke=APAGADO,
                 width=0.6).move_to(Point(x0, 0), anchor="topleft")
            for t in range(0, u, 8):
                _txt(str(t), Point(x0 + t * celda + celda / 2, u * celda + 9),
                     color=APAGADO, size=PIE)
                _txt(str(t), Point(x0 - 4, t * celda + celda / 2), color=APAGADO,
                     size=PIE, anchor="end")
        ley = [(Colors.White, "0"), (ACENTO.transparent(0.15), f"1/{m}"),
               (ALARMA.transparent(0.5), "1/2"), (ALARMA, "1")]
        y0 = len(paneles[0][1]) * celda + 26
        for i, (color, texto) in enumerate(ley):
            Rect(10, 10, fill=color, stroke=APAGADO, width=0.5).move_to(
                Point(i * 60, y0), anchor="topleft")
            _txt(texto, Point(i * 60 + 14, y0 + 5), color=APAGADO, size=PIE,
                 anchor="start")
        _txt("probabilidad de que x e y choquen", Point(4 * 60 + 10, y0 + 5),
             color=APAGADO, size=PIE, anchor="start")
    return _figura(canvas, ident, pie)
