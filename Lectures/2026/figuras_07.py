"""Figuras del capítulo 7: la transformada rápida de Fourier.

Cada función recibe el estado que calculó el código del capítulo: las raíces y sus
cuadrados, las mariposas que registró la FFT iterativa y los errores medidos.
"""

import math

from tesserax import Canvas, Circle, Colors, Line, Point, Polyline, Rect

from figuras import (
    ACENTO, ALARMA, APAGADO, CALIDO, CUERPO, OSCURO, PIE, REGLA, TINTA,
    _figura, _punto, _txt, sub, sup,
)


def _circulo(cx, cy, r, puntos, etiquetas, color, rotulo):
    """Dibuja el círculo unidad centrado en (cx, cy) con radio r y los puntos
    complejos dados, cada uno con su etiqueta afuera del círculo."""
    Circle(r, stroke=REGLA, width=1.0).move_to(Point(cx, cy))
    Line(Point(cx - r - 10, cy), Point(cx + r + 10, cy), stroke=REGLA, width=0.6)
    Line(Point(cx, cy - r - 10), Point(cx, cy + r + 10), stroke=REGLA, width=0.6)
    for z, etq in zip(puntos, etiquetas):
        p = Point(cx + r * z.real, cy - r * z.imag)
        Line(Point(cx, cy), p, stroke=color.transparent(0.35), width=0.7)
        _punto(p, color, r=3.2)
        ang = math.atan2(z.imag, z.real)
        c, s = math.cos(ang), math.sin(ang)
        # la etiqueta se ancla hacia afuera del círculo, para no tapar el punto
        ancla = "start" if c > 0.3 else "end" if c < -0.3 else "middle"
        d = 9 if ancla != "middle" else 13
        q = Point(cx + (r + d) * c, cy - (r + d) * s)
        _txt(etq, q, color=color, size=10.5, anchor=ancla)
    _txt(rotulo, Point(cx, cy + r + 34), color=APAGADO, size=CUERPO)


def raices(raices_n, cuadrados, ident="fft-raices", pie=""):
    """raices_n: las n raíces n-ésimas, en orden de k. cuadrados: {k: índice j de la
    raíz (n/2)-ésima que es el cuadrado de la raíz k}, calculado por el capítulo."""
    n = len(raices_n)
    m = n // 2
    destinos = [math.e ** (2j * math.pi * j / m) for j in range(m)]
    origen = {j: [k for k in range(n) if cuadrados[k] == j] for j in range(m)}
    r = 70.0
    with Canvas() as canvas:
        _circulo(0, 0, r, raices_n, [f"ω{sup(k)}" for k in range(n)], OSCURO,
                 f"las {n} raíces de orden {n}")
        _circulo(320, 0, r, destinos,
                 [f"de {', '.join(str(k) for k in origen[j])}" for j in range(m)],
                 CALIDO, f"sus cuadrados: las {m} raíces de orden {m}")
        Line(Point(r + 40, 0), Point(320 - r - 62, 0), stroke=APAGADO, width=1.1,
             marker_end="arrow")
        _txt("z ↦ z²", Point(149, -10), color=APAGADO, size=CUERPO)
    return _figura(canvas, ident, pie)


def mariposa(n, etapas, orden_entrada, ident="fft-mariposa", pie=""):
    """etapas: una lista por etapa con las mariposas (i, j, k, m) que ejecutó la FFT
    iterativa: combina las posiciones i y j con el factor ω_m^k.
    orden_entrada: qué a_t quedó en cada posición tras la inversión de bits."""
    dy, dx = 30.0, 120.0
    s = len(etapas)
    colores = [OSCURO, CALIDO, ACENTO, ALARMA]
    with Canvas() as canvas:
        for e, mariposas in enumerate(etapas):
            color = colores[e % len(colores)]
            x0, x1 = e * dx, (e + 1) * dx
            for i, j, k, m in mariposas:
                for a in (i, j):
                    for b in (i, j):
                        Line(Point(x0, a * dy), Point(x1, b * dy),
                             stroke=color.transparent(0.15 if a == b else 0.75),
                             width=1.0 if a != b else 0.8)
                # el factor multiplica la entrada de abajo, la posición j
                _txt(f"ω{sub(m)}{sup(k)}", Point(x0 + 4, j * dy + 9), color=color,
                     size=10.5, anchor="start")
            _txt(f"etapa {e + 1}: bloques de {etapas[e][0][3]}",
                 Point((x0 + x1) / 2, -22), color=color, size=PIE)
        for p in range(n):
            for e in range(s + 1):
                _punto(Point(e * dx, p * dy), TINTA, r=2.4)
            _txt(f"a{sub(orden_entrada[p])}", Point(-10, p * dy), size=10.5,
                 anchor="end")
            _txt(f"y{sub(p)}", Point(s * dx + 10, p * dy), size=10.5,
                 anchor="start")
    return _figura(canvas, ident, pie)


def error_redondeo(series, rotos, ident="fft-error", pie=""):
    """series: {k: [(N, error), ...]} con el error máximo medido contra el producto
    exacto. rotos: el conjunto de (k, N) donde algún coeficiente salió equivocado."""
    ancho, alto = 300.0, 180.0
    todos = [p for s in series.values() for p in s]
    x0 = math.floor(min(math.log2(x) for x, _ in todos))
    x1 = math.ceil(max(math.log2(x) for x, _ in todos))
    y0 = math.floor(min(math.log10(y) for _, y in todos))
    y1 = max(1, math.ceil(max(math.log10(y) for _, y in todos)))
    px = lambda x: (math.log2(x) - x0) / (x1 - x0) * ancho
    py = lambda y: alto - (math.log10(y) - y0) / (y1 - y0) * alto
    colores = [OSCURO, ACENTO, CALIDO, ALARMA]
    with Canvas() as canvas:
        for e in range(x0, x1 + 1, 2):
            Line(Point(px(2 ** e), 0), Point(px(2 ** e), alto), stroke=REGLA,
                 width=0.7)
            _txt(f"2{sup(e)}", Point(px(2 ** e), alto + 12), color=APAGADO, size=PIE)
        for e in range(y0, y1 + 1, 2):
            Line(Point(0, py(10 ** e)), Point(ancho, py(10 ** e)), stroke=REGLA,
                 width=0.7)
            _txt(f"10{sup(e)}", Point(-8, py(10 ** e)), color=APAGADO, size=PIE,
                 anchor="end")
        Rect(ancho, py(0.5), fill=ALARMA.transparent(0.08),
             stroke=Colors.Transparent).move_to(Point(0, 0), anchor="topleft")
        Line(Point(0, py(0.5)), Point(ancho, py(0.5)), stroke=ALARMA, width=1.0)
        _txt("1/2: redondea al entero equivocado", Point(4, py(0.5) - 8),
             color=ALARMA, size=PIE, anchor="start")
        for c, (k, puntos) in enumerate(series.items()):
            color = colores[c % len(colores)]
            Polyline([Point(px(x), py(y)) for x, y in puntos], stroke=color,
                     width=1.6)
            for x, y in puntos:
                roto = (k, x) in rotos
                _punto(Point(px(x), py(y)), ALARMA if roto else color,
                       r=3.6 if roto else 2.5)
            xu, yu = puntos[-1]
            _txt(f"base 10{sup(k)}", Point(ancho + 8, py(yu)), color=color, size=PIE,
                 anchor="start")
        _txt("N, el tamaño de la transformada", Point(ancho / 2, alto + 28),
             color=APAGADO, size=PIE)
        _txt("error máximo", Point(-8, -12), color=APAGADO, size=PIE, anchor="end")
    return _figura(canvas, ident, pie)
