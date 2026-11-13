"""Figuras del capítulo 21: algoritmos de aproximación.

Cada figura recibe lo que calculó el código del capítulo: las aristas que tomó el
emparejamiento maximal y el cubrimiento que salió, las cargas y la asignación de la
regla de Graham con sus dos cotas, y los centros y el radio del recorrido del más
lejano.
"""

import math

from tesserax import Canvas, Circle, Colors, Line, Point, Rect

from figuras import (
    ACENTO, APAGADO, CALIDO, CUERPO, OSCURO, PIE, REGLA, TINTA, Marco,
    _figura, _punto, _txt, sub,
)


def emparejamiento(n, aristas, M, C, ident="aprox-emparejamiento", pie=""):
    """`aristas`: el grafo; `M`: las aristas que tomó el algoritmo; `C`: el
    cubrimiento que devolvió. Los vértices van en círculo, numerados."""
    R = 92.0
    pos = {v: Point(R * math.cos(2 * math.pi * v / n - math.pi / 2),
                    R * math.sin(2 * math.pi * v / n - math.pi / 2))
           for v in range(n)}
    tomadas = {frozenset(e) for e in M}
    with Canvas() as canvas:
        for u, v in aristas:
            if frozenset((u, v)) not in tomadas:
                Line(pos[u], pos[v], stroke=REGLA.darker(0.15), width=1.0)
        for u, v in M:
            Line(pos[u], pos[v], stroke=CALIDO, width=3.0)
        for v in range(n):
            dentro = v in C
            Circle(9, fill=OSCURO if dentro else Colors.White,
                   stroke=OSCURO if dentro else TINTA, width=1.0).move_to(pos[v])
            _txt(str(v), pos[v], color=Colors.White if dentro else TINTA, size=CUERPO)
        y = R + 30
        Line(Point(-150, y), Point(-130, y), stroke=CALIDO, width=3.0)
        _txt("arista tomada (emparejamiento)", Point(-125, y), color=CALIDO,
             size=CUERPO, anchor="start")
        Circle(5, fill=OSCURO, stroke=OSCURO).move_to(Point(75, y))
        _txt("vértice del cubrimiento", Point(85, y), color=OSCURO, size=CUERPO,
             anchor="start")
    return _figura(canvas, ident, pie)


def graham(t, asign, m, ultima, ident="aprox-graham", pie=""):
    """`t`: duraciones en el orden de llegada; `asign[j]`: la máquina que eligió la
    regla para la tarea j; `ultima`: la última tarea de la máquina más cargada."""
    escala, alto, sep = 30.0, 24.0, 8.0
    cargas = [0] * m
    with Canvas() as canvas:
        for j, (x, i) in enumerate(zip(t, asign)):
            y = i * (alto + sep)
            x0 = cargas[i] * escala
            es = j == ultima
            Rect(x * escala, alto,
                 fill=CALIDO.transparent(0.25) if es else ACENTO.transparent(0.14),
                 stroke=CALIDO if es else OSCURO, width=1.4 if es else 0.9).move_to(
                Point(x0 + x * escala / 2, y + alto / 2))
            _txt(f"t{sub(j + 1)}={x}", Point(x0 + x * escala / 2, y + alto / 2),
                 color=CALIDO if es else TINTA, size=CUERPO)
            cargas[i] += x
        for i in range(m):
            _txt(f"M{sub(i + 1)}", Point(-8, i * (alto + sep) + alto / 2),
                 color=APAGADO, size=CUERPO, anchor="end")
        fondo = m * (alto + sep)
        prom = sum(t) / m
        for valor, texto, color, dy in ((prom, f"Σt/m = {sum(t)}/{m}", OSCURO, 13),
                                        (max(t), f"máx t = {max(t)}", APAGADO, 27)):
            x = valor * escala
            Line(Point(x, -6), Point(x, fondo + dy - 8), stroke=color, width=1.0)
            _txt(texto, Point(x, fondo + dy), color=color, size=CUERPO)
        L = max(cargas)
        x = L * escala
        Line(Point(x, -6), Point(x, fondo + 28), stroke=CALIDO, width=1.0)
        _txt(f"makespan = {L}", Point(x + 4, -12), color=CALIDO, size=CUERPO,
             anchor="start")
    return _figura(canvas, ident, pie)


def kcentro(P, centros, r, lejano, ident="aprox-kcentro", pie=""):
    """`P`: los puntos; `centros`: índices en el orden en que los eligió el
    recorrido; `r`: el radio que logró; `lejano`: el punto que lo realiza."""
    marco = Marco(P, ancho=330.0, alto=250.0, margen=34.0)
    with Canvas() as canvas:
        for c in centros:
            Circle(marco.largo(r), fill=ACENTO.transparent(0.07), stroke=ACENTO,
                   width=0.8).move_to(marco(P[c]))
        for j, p in enumerate(P):
            if j not in centros:
                _punto(marco(p), color=TINTA, r=2.4)
        q = marco(P[lejano])
        Circle(5.5, fill=Colors.White, stroke=CALIDO, width=1.4).move_to(q)
        _punto(q, color=CALIDO, r=2.4)
        for orden, c in enumerate(centros, start=1):
            p = marco(P[c])
            Rect(8, 8, fill=OSCURO, stroke=OSCURO).move_to(p)
            _txt(f"c{sub(orden)}", Point(p.x + 11, p.y - 9), color=OSCURO,
                 size=CUERPO)
        _txt(f"r = {r:.3f}", Point(q.x + 10, q.y + 12), color=CALIDO, size=CUERPO,
             anchor="start")
    return _figura(canvas, ident, pie)
