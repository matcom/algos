"""Figuras del capítulo 1: qué significa que un algoritmo es eficiente.

Cada función recibe el estado que calculó el código del capítulo: la trayectoria
que siguió el cabezal de la máquina de Turing simulada y los tamaños de entrada que
encontró la búsqueda binaria de la §7.
"""

import math

from tesserax import Canvas, Line, Point, Polyline, Rect

from figuras import (
    ACENTO, ALARMA, APAGADO, CALIDO, CUERPO, OSCURO, PIE, REGLA, TINTA,
    _figura, _punto, _txt, sup,
)


def cinta(w, camino, i, ident="eficiencia-cinta", pie=""):
    """w: la palabra escrita en la cinta. camino: la posición del cabezal después
    de cada paso, tal como la registró la simulación. i: la celda a la que se
    quiere llegar en el panel de arriba."""
    lado = 26.0
    celdas = len(w) + 2                      # un blanco a cada lado
    px = lambda pos: (pos + 1) * lado + lado / 2
    with Canvas() as canvas:
        # la cinta, con la palabra y un blanco a cada lado
        for k in range(celdas):
            Rect(lado, lado, stroke=TINTA, width=0.8).move_to(
                Point(k * lado + lado / 2, lado / 2))
            simbolo = w[k - 1] if 1 <= k <= len(w) else "␣"
            _txt(simbolo, Point(k * lado + lado / 2, lado / 2),
                 color=TINTA if 1 <= k <= len(w) else APAGADO, size=11)
        for k in range(len(w)):
            _txt(str(k), Point(px(k), -8), color=APAGADO, size=PIE)
        # el cabezal en la celda 0
        Polyline([Point(px(0) - 6, lado + 13), Point(px(0) + 6, lado + 13),
                  Point(px(0), lado + 4)], closed=True, fill=ACENTO, stroke=ACENTO)
        # llegar a la celda i cuesta i movimientos
        y = lado + 22
        for k in range(i):
            Line(Point(px(k) + 3, y), Point(px(k + 1) - 3, y), stroke=CALIDO,
                 width=1.1, marker_end="arrow")
        _txt(f"llegar a la celda {i}: {i} movimientos", Point(px(i) + 18, y),
             color=CALIDO, size=CUERPO, anchor="start")
        # la trayectoria del cabezal: posición en x, tiempo hacia abajo
        y0, dt = lado + 50, 3.4
        Line(Point(0, y0), Point(celdas * lado, y0), stroke=REGLA, width=0.7)
        pasos = len(camino) - 1
        Line(Point(-6, y0), Point(-6, y0 + pasos * dt), stroke=APAGADO,
             width=0.8, marker_end="arrow")
        _txt("tiempo", Point(-12, y0 + pasos * dt / 2), color=APAGADO, size=PIE,
             anchor="end")
        Polyline([Point(px(pos), y0 + t * dt) for t, pos in enumerate(camino)],
                 stroke=OSCURO, width=1.2)
        _punto(Point(px(camino[-1]), y0 + pasos * dt), ALARMA, r=3.0)
        _txt(f"{pasos} pasos con n = {len(w)}",
             Point(celdas * lado + 10, y0 + pasos * dt), color=ALARMA,
             size=CUERPO, anchor="start")
    return _figura(canvas, ident, pie)


def hora(filas, factores, ident="eficiencia-hora", pie=""):
    """filas: {costo: [el mayor n que cabe en una hora con cada factor]}, con los
    números que calculó la búsqueda binaria. factores: los multiplicadores de
    velocidad, en el mismo orden (el primero es la máquina de hoy)."""
    ancho, fila = 330.0, 30.0
    todos = [n for ns in filas.values() for n in ns]
    e0 = math.floor(math.log10(min(todos)))
    e1 = math.ceil(math.log10(max(todos)))
    px = lambda n: (math.log10(n) - e0) / (e1 - e0) * ancho
    colores = [APAGADO, ACENTO, TINTA]
    bonito = {"n^2": "n²", "n^3": "n³", "2^n": "2ⁿ"}
    alto = fila * len(filas)
    with Canvas() as canvas:
        for e in range(e0, e1 + 1, 2):
            Line(Point(px(10 ** e), -6), Point(px(10 ** e), alto), stroke=REGLA,
                 width=0.7)
            _txt(f"10{sup(e)}", Point(px(10 ** e), alto + 12), color=APAGADO,
                 size=PIE)
        _txt("mayor n que se resuelve en una hora (escala logarítmica)",
             Point(ancho / 2, alto + 28), color=APAGADO, size=PIE)
        for r, (nombre, ns) in enumerate(filas.items()):
            y = r * fila + fila / 2
            _txt(bonito.get(nombre, nombre), Point(-10, y), color=TINTA, size=CUERPO,
                 anchor="end")
            Line(Point(px(ns[0]), y), Point(px(ns[-1]), y), stroke=CALIDO,
                 width=2.2)
            for n, color in zip(ns, colores):
                _punto(Point(px(n), y), color, r=3.4)
            r = ns[-1] / ns[0]
            _txt(f"×{r:.0f}" if r >= 100 else "×" + f"{r:.3g}".replace(".", ","), Point(max(px(ns[-1]), px(ns[0])) + 10, y),
                 color=CALIDO, size=CUERPO, anchor="start")
        for k, (f, color) in enumerate(zip(factores, colores)):
            x = k * 95.0
            _punto(Point(x, -22), color, r=3.4)
            texto = "la máquina de hoy" if f == 1 else f"{f} veces más rápida"
            _txt(texto, Point(x + 8, -22), color=color, size=PIE, anchor="start")
    return _figura(canvas, ident, pie)
