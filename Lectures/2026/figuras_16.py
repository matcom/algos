"""Figuras del capítulo 16: P, NP y reducciones.

La figura de las tres vistas recibe el grafo y el conjunto independiente máximo que
calculó el código del capítulo. Las otras dos son diagramas de definiciones: no
ilustran la ejecución de ningún algoritmo.
"""

import math

from tesserax import Arrow, Canvas, Colors, Ellipse, Line, Point, Rect

from figuras import (
    ACENTO, ALARMA, APAGADO, CALIDO, CUERPO, OSCURO, PIE, REGLA, TINTA,
    _figura, _punto, _txt,
)


def _circulo(n, cx, cy, r):
    """Posiciones de dibujo de n vértices sobre un círculo, el 0 arriba."""
    return [Point(cx + r * math.sin(2 * math.pi * v / n),
                  cy - r * math.cos(2 * math.pi * v / n)) for v in range(n)]


def tres_vistas(n, aristas, S, ident="np-tres-vistas", pie=""):
    """`aristas`: pares (u, v) del grafo G. `S`: el conjunto independiente que
    encontró el código. Panel 1: G con S. Panel 2: el complemento con S, que es un
    clique. Panel 3: G con V − S, que cubre todas las aristas."""
    s = set(S)
    E = {frozenset(e) for e in aristas}
    comp = [(u, v) for u in range(n) for v in range(u + 1, n) if frozenset((u, v)) not in E]
    paneles = [
        ("G: S es independiente", aristas, s, ACENTO, lambda u, v: False),
        ("complemento de G: S es un clique", comp, s, ACENTO,
         lambda u, v: u in s and v in s),
        ("G: V − S cubre las aristas", aristas, set(range(n)) - s, CALIDO,
         lambda u, v: False),
    ]
    r, paso = 52.0, 150.0
    with Canvas() as canvas:
        for i, (titulo, E_i, marcados, color, gruesa) in enumerate(paneles):
            P = _circulo(n, i * paso + 60, 70, r)
            for u, v in E_i:
                if gruesa(u, v):
                    Line(P[u], P[v], stroke=color, width=2.6)
                else:
                    Line(P[u], P[v], stroke=TINTA, width=0.9)
            for v in range(n):
                relleno = color if v in marcados else Colors.White
                _punto(P[v], TINTA, r=9.5)
                _punto(P[v], relleno, r=8.3)
                _txt(str(v), P[v], color=Colors.White if v in marcados else TINTA,
                     size=CUERPO)
            _txt(titulo, Point(i * paso + 60, 70 + r + 24), color=APAGADO, size=CUERPO)
    return _figura(canvas, ident, pie)


def _caja(x, y, w, h, texto, color=TINTA, fondo=Colors.White):
    Rect(w, h, fill=fondo, stroke=color, width=1.0).move_to(Point(x + w / 2, y + h / 2))
    _txt(texto, Point(x + w / 2, y + h / 2), color=color, size=CUERPO)


def direcciones(ident="np-direcciones", pie=""):
    """Una reducción A ≤ₚ B como tubería, y qué se puede concluir en cada sentido."""
    with Canvas() as canvas:
        # el algoritmo para A que se arma con f y un algoritmo para B
        Rect(285, 62, fill=ACENTO.transparent(0.08), stroke=OSCURO, width=0.8) \
            .move_to(Point(192.5, 41))
        _txt("algoritmo para A", Point(192.5, 4), color=OSCURO, size=CUERPO)
        _caja(0, 25, 40, 30, "x")
        _caja(95, 25, 60, 30, "f(x)")
        _caja(205, 25, 115, 30, "algoritmo para B", color=OSCURO)
        _caja(375, 25, 55, 30, "sí / no")
        Arrow(Point(40, 40), Point(95, 40), stroke=TINTA, width=1.0)
        _txt("f", Point(60, 32), color=APAGADO, size=CUERPO)
        Arrow(Point(155, 40), Point(205, 40), stroke=TINTA, width=1.0)
        Arrow(Point(320, 40), Point(375, 40), stroke=TINTA, width=1.0)
        filas = [
            ("B ∈ P  ⇒  A ∈ P", "diseñar: la tubería es el algoritmo", True),
            ("A ∉ P  ⇒  B ∉ P", "dificultad: lo de este capítulo", True),
            ("A ∈ P  ⇒  nada sobre B", "B puede ser tan difícil como quiera", False),
            ("B ∉ P  ⇒  nada sobre A", "A puede resolverse sin pasar por B", False),
        ]
        for j, (formula, lectura, vale) in enumerate(filas):
            y = 100 + 20 * j
            color = OSCURO if vale else ALARMA
            _txt("sí" if vale else "no", Point(10, y), color=color, size=CUERPO)
            _txt(formula, Point(35, y), color=color, size=CUERPO, anchor="start")
            _txt(lectura, Point(205, y), color=APAGADO, size=CUERPO, anchor="start")
        Line(Point(0, 88), Point(430, 88), stroke=REGLA, width=0.8)
    return _figura(canvas, ident, pie)


def clases(ident="np-clases", pie=""):
    """Los dos mundos posibles. Izquierda: P ≠ NP. Derecha: P = NP. Las regiones
    respetan las definiciones: NP-completo es NP ∩ NP-duro, y con P = NP los dos
    lenguajes triviales quedan en P y fuera de NP-duro."""
    with Canvas() as canvas:
        # --- P ≠ NP
        _txt("si P ≠ NP", Point(170, -6), color=TINTA, size=CUERPO + 1)
        Ellipse(110, 62, fill=CALIDO.transparent(0.08), stroke=CALIDO, width=1.0) \
            .move_to(Point(250, 85))
        Ellipse(95, 62, fill=ACENTO.transparent(0.08), stroke=OSCURO, width=1.0) \
            .move_to(Point(95, 85))
        Ellipse(32, 28, fill=ACENTO.transparent(0.18), stroke=OSCURO, width=1.0) \
            .move_to(Point(48, 85))
        _txt("P", Point(48, 85), color=OSCURO, size=CUERPO + 1)
        _txt("NP", Point(95, 36), color=OSCURO, size=CUERPO + 1)
        _txt("NP-", Point(165, 79), color=TINTA, size=PIE)
        _txt("completo", Point(165, 90), color=TINTA, size=PIE)
        _txt("NP-duro", Point(300, 85), color=CALIDO, size=CUERPO + 1)
        _punto(Point(110, 100), TINTA, r=2.6)
        _txt("ni P ni", Point(110, 111), color=APAGADO, size=PIE)
        _txt("completo", Point(110, 120), color=APAGADO, size=PIE)
        # --- P = NP
        ox = 400
        _txt("si P = NP", Point(ox + 130, -6), color=TINTA, size=CUERPO + 1)
        Ellipse(115, 62, fill=CALIDO.transparent(0.08), stroke=CALIDO, width=1.0) \
            .move_to(Point(ox + 160, 85))
        Ellipse(70, 50, fill=ACENTO.transparent(0.18), stroke=OSCURO, width=1.0) \
            .move_to(Point(ox + 75, 85))
        _txt("P = NP", Point(ox + 60, 26), color=OSCURO, size=CUERPO + 1)
        _txt("NP-completo", Point(ox + 92, 88), color=TINTA, size=CUERPO)
        _punto(Point(ox + 22, 75), ALARMA, r=3.0)
        _txt("∅", Point(ox + 33, 75), color=ALARMA, size=CUERPO, anchor="start")
        _punto(Point(ox + 22, 98), ALARMA, r=3.0)
        _txt("Σ*", Point(ox + 30, 98), color=ALARMA, size=CUERPO, anchor="start")
        _txt("NP-duro", Point(ox + 230, 85), color=CALIDO, size=CUERPO + 1)
    return _figura(canvas, ident, pie)
