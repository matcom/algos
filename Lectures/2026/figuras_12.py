"""Figuras del capítulo 12: optimizaciones de programación dinámica.

Cada función recibe el estado que calculó el código del capítulo (la tabla de
raíces, las filas de Hirschberg y el corte elegido) y no decide nada del algoritmo.
"""

from tesserax import Canvas, Line, Point, Rect

from figuras import (
    ACENTO, ALARMA, APAGADO, CALIDO, CUERPO, OSCURO, PIE, REGLA, TINTA,
    _figura, _punto, _txt, sub,
)


# --------------------------------------------------------------------------
# 1. la tabla de raíces y la franja de una celda
# --------------------------------------------------------------------------

def raices(R, n, celda, ident="dpopt-raices", pie=""):
    """`R[i][j]` es la mayor raíz óptima de las claves i+1..j; `celda` = (i, j) es
    la que se resalta, junto con (i, j-1) y (i+1, j), que fijan su franja."""
    s = 36.0
    ci, cj = celda
    vecinas = {(ci, cj - 1), (ci + 1, cj)}
    with Canvas() as canvas:
        for j in range(1, n + 1):
            _txt(f"j={j}", Point((j - 0.5) * s, -12), color=APAGADO, size=CUERPO)
        for i in range(n):
            _txt(f"i={i}", Point(-10, (i + 0.5) * s), color=APAGADO, size=CUERPO,
                 anchor="end")
            for j in range(i + 1, n + 1):
                x, y = (j - 0.5) * s, (i + 0.5) * s
                if (i, j) == celda:
                    fondo, borde, ancho = CALIDO.transparent(0.22), CALIDO, 1.6
                elif (i, j) in vecinas:
                    fondo, borde, ancho = ACENTO.transparent(0.20), OSCURO, 1.4
                else:
                    fondo, borde, ancho = ACENTO.transparent(0.04), REGLA, 0.7
                Rect(s, s, fill=fondo, stroke=borde, width=ancho).move_to(Point(x, y))
                _txt(str(R[i][j]), Point(x, y), size=11.0,
                     color=CALIDO if (i, j) == celda else TINTA)
        lo, hi = R[ci][cj - 1], R[ci + 1][cj]
        _txt(f"franja de ({ci}, {cj}): raíces {lo} a {hi}",
             Point(0, n * s + 16), color=CALIDO, size=CUERPO, anchor="start")
    return _figura(canvas, ident, pie)


# --------------------------------------------------------------------------
# 2. Hirschberg: la fila media, F + B y los dos rectángulos que quedan
# --------------------------------------------------------------------------

def hirschberg_corte(X, Y, mid, F, B, k, ident="dpopt-hirschberg", pie=""):
    """Tabla de puntos (i, j), 0 <= i <= n, 0 <= j <= m. `F[j]` = LCS(X[:mid],
    Y[:j]), `B[j]` = LCS(X[mid:], Y[j:]) y `k` el corte que eligió el código."""
    s = 30.0
    n, m = len(X), len(Y)
    with Canvas() as canvas:
        Rect(m * s, n * s, fill=REGLA.transparent(0.35), stroke=REGLA,
             width=0.7).move_to(Point(0, 0), anchor="topleft")
        if k > 0 and mid > 0:
            Rect(k * s, mid * s, fill=ACENTO.transparent(0.22), stroke=OSCURO,
                 width=1.2).move_to(Point(0, 0), anchor="topleft")
        if k < m:
            Rect((m - k) * s, (n - mid) * s, fill=ACENTO.transparent(0.22),
                 stroke=OSCURO, width=1.2).move_to(Point(k * s, mid * s),
                                                  anchor="topleft")
        for j, y in enumerate(Y):
            _txt(y, Point((j + 0.5) * s, -10), size=CUERPO)
        for i, x in enumerate(X):
            _txt(x, Point(-10, (i + 0.5) * s), size=CUERPO)
        for j in range(m + 1):
            Line(Point(j * s, 0), Point(j * s, n * s), stroke=REGLA.darker(0.15),
                 width=0.4)
        for i in range(n + 1):
            Line(Point(0, i * s), Point(m * s, i * s), stroke=REGLA.darker(0.15),
                 width=0.4)
        Line(Point(-4, mid * s), Point(m * s + 4, mid * s), stroke=CALIDO,
             width=1.4)
        _txt(f"fila {mid}", Point(m * s + 8, mid * s), color=CALIDO, size=PIE,
             anchor="start")
        _punto(Point(k * s, mid * s), ALARMA, r=3.4)
        ybase = n * s + 14
        _txt("F+B", Point(-10, ybase), color=APAGADO, size=PIE, anchor="end")
        mejor = F[k] + B[k]
        for j in range(m + 1):
            v = F[j] + B[j]
            _txt(str(v), Point(j * s, ybase),
                 color=ALARMA if j == k else (CALIDO if v == mejor else APAGADO),
                 size=CUERPO if j == k else PIE)
        _txt(f"j = 0 … {m}", Point(m * s / 2, ybase + 14), color=APAGADO, size=PIE)
    return _figura(canvas, ident, pie)
