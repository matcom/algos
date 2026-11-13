"""Figuras del capítulo 13: flujo máximo con Dinic.

Cada función recibe el estado que calculó el código del capítulo (el flujo, la red
residual, los niveles, el lado S del corte) y no decide nada del algoritmo. Las
posiciones de los vértices son solo presentación.
"""

import math

from tesserax import Arrow, Canvas, Circle, Line, Point, Rect

from figuras import (
    ACENTO, ALARMA, APAGADO, CALIDO, CUERPO, OSCURO, PIE, REGLA, TINTA,
    _figura, _txt,
)

RADIO = 11.0


def _punteada(p, q, color=APAGADO, width=0.9, paso=3.5):
    """tesserax no tiene dasharray: la línea de trazos se hace con segmentos."""
    largo = math.hypot(q.x - p.x, q.y - p.y)
    k = max(1, int(largo / (2 * paso)))
    for i in range(k):
        t0, t1 = (2 * i) / (2 * k), (2 * i + 1) / (2 * k)
        Line(Point(p.x + (q.x - p.x) * t0, p.y + (q.y - p.y) * t0),
             Point(p.x + (q.x - p.x) * t1, p.y + (q.y - p.y) * t1),
             stroke=color, width=width)


def _arista(a, b, texto, color=TINTA, ancho=1.0, desplazar=0.0, lado=1.0,
            punteada=False, color_texto=None):
    """Flecha de `a` a `b` (centros de vértice) que empieza y acaba en el borde del
    círculo. `desplazar` la corre a lo largo de la normal, para las antiparalelas;
    la etiqueta va del lado `lado` de la normal."""
    dx, dy = b.x - a.x, b.y - a.y
    largo = math.hypot(dx, dy)
    ux, uy = dx / largo, dy / largo
    nx, ny = -uy, ux
    p = Point(a.x + ux * (RADIO + 1) + nx * desplazar, a.y + uy * (RADIO + 1) + ny * desplazar)
    q = Point(b.x - ux * (RADIO + 2) + nx * desplazar, b.y - uy * (RADIO + 2) + ny * desplazar)
    if punteada:
        _punteada(p, q, color=color, width=ancho)
    else:
        Arrow(p, q, stroke=color, width=ancho, marker_end="arrow")
    if texto:
        sep = 8.0 + abs(desplazar)
        m = Point((p.x + q.x) / 2 + lado * nx * sep, (p.y + q.y) / 2 + lado * ny * sep)
        _txt(texto, m, color=color_texto or color, size=CUERPO)


def _vertices(pos, nombres, origen, relleno=None):
    ox, oy = origen
    for v, (x, y) in pos.items():
        c = Point(ox + x, oy + y)
        Circle(RADIO, fill=(relleno or {}).get(v, "#ffffff"), stroke=TINTA,
               width=0.9).move_to(c)
        _txt(nombres[v], c, size=CUERPO + 1)


def _p(pos, v, origen):
    return Point(origen[0] + pos[v][0], origen[1] + pos[v][1])


def _lado(pos, u, v):
    """Pone la etiqueta del lado de afuera del dibujo (arriba en la fila de arriba,
    abajo en la de abajo); en las verticales, a la derecha."""
    (x1, y1), (x2, y2) = pos[u], pos[v]
    dx, dy = x2 - x1, y2 - y1
    largo = math.hypot(dx, dy)
    nx, ny = -dy / largo, dx / largo
    ym = (y1 + y2) / 2
    cy = sum(y for _, y in pos.values()) / len(pos)
    if abs(dx) < 1e-9:
        return 1.0 if nx > 0 else -1.0
    hacia_fuera = -1.0 if ym < cy else 1.0
    if abs(ym - cy) < 1e-9:
        hacia_fuera = -1.0
    return 1.0 if ny * hacia_fuera > 0 else -1.0


# --------------------------------------------------------------------------
# 1. un flujo y su red residual
# --------------------------------------------------------------------------

def red_y_residual(pos, nombres, aristas, flujo, residual, camino,
                   ident="dinic-residual", pie=""):
    """`aristas` = [(u, v, c)], `flujo[i]` el flujo de la arista i, `residual` =
    [(u, v, capacidad)] con capacidad > 0, y `camino` el conjunto de pares (u, v) de
    la residual que forman el camino de aumento."""
    sep = 330.0
    with Canvas() as canvas:
        o = (0.0, 0.0)
        for (u, v, c), f in zip(aristas, flujo):
            lleno = f == c
            _arista(_p(pos, u, o), _p(pos, v, o), f"{f}/{c}",
                    color=CALIDO if lleno else TINTA, ancho=1.3 if lleno else 0.9,
                    lado=_lado(pos, u, v))
        _vertices(pos, nombres, o)
        total = sum(f for (u, v, c), f in zip(aristas, flujo) if u == 0)
        _txt(f"flujo f, valor {total} (flujo/capacidad)", Point(140, 138),
             color=APAGADO, size=PIE)
        o = (sep, 0.0)
        pares = {(u, v) for u, v, _ in residual}
        for u, v, r in residual:
            doble = (v, u) in pares
            en_camino = (u, v) in camino
            inversa = not any(a == u and b == v for a, b, _ in aristas)
            color = ALARMA if en_camino else (OSCURO if inversa else APAGADO)
            _arista(_p(pos, u, o), _p(pos, v, o), str(r), color=color,
                    ancho=1.4 if en_camino else 0.9,
                    desplazar=4.0 if doble else 0.0,
                    lado=1.0 if doble else _lado(pos, u, v))
        _vertices(pos, nombres, o)
        _txt("red residual: gris, lo que sobra; azul, lo que se puede deshacer",
             Point(sep + 140, 138), color=APAGADO, size=PIE)
    return _figura(canvas, ident, pie)


# --------------------------------------------------------------------------
# 2. el grafo de niveles de una fase y su flujo bloqueante
# --------------------------------------------------------------------------

def grafo_niveles(pos, nombres, nivel, de_nivel, fuera, flujo_fase,
                  ident="dinic-niveles", pie=""):
    """`nivel[v]` lo dio la BFS; `de_nivel` = [(u, v, capacidad residual)] son las
    aristas con nivel[v] = nivel[u] + 1; `fuera` las residuales que no lo cumplen;
    `flujo_fase[(u, v)]` lo que empujó la fase por cada arista de nivel."""
    with Canvas() as canvas:
        o = (0.0, 0.0)
        xs = {}
        for v, l in enumerate(nivel):
            if l >= 0:
                xs.setdefault(l, pos[v][0])
        for l, x in sorted(xs.items()):
            Rect(46, 150, fill=ACENTO.transparent(0.06), stroke=REGLA,
                 width=0.6).move_to(Point(x, 50))
            _txt(f"nivel {l}", Point(x, -36), color=APAGADO, size=PIE)
        for u, v, r in fuera:
            _arista(_p(pos, u, o), _p(pos, v, o), "", color=REGLA.darker(0.2),
                    ancho=0.9, punteada=True)
        for u, v, r in de_nivel:
            f = flujo_fase.get((u, v), 0)
            lleno = f == r
            color = CALIDO if lleno else (OSCURO if f > 0 else APAGADO)
            _arista(_p(pos, u, o), _p(pos, v, o), f"{f}/{r}", color=color,
                    ancho=1.4 if lleno else (1.2 if f > 0 else 0.9),
                    lado=_lado(pos, u, v))
        _vertices(pos, nombres, o)
    return _figura(canvas, ident, pie)


# --------------------------------------------------------------------------
# 3. el corte mínimo que se lee al final
# --------------------------------------------------------------------------

def corte_minimo(pos, nombres, aristas, flujo, S, ident="dinic-corte", pie=""):
    """`S` es el conjunto de vértices alcanzables desde s en la residual final."""
    with Canvas() as canvas:
        o = (0.0, 0.0)
        relleno = {v: ACENTO.transparent(0.25) for v in S}
        for (u, v, c), f in zip(aristas, flujo):
            if u in S and v not in S:
                color, ancho = ALARMA, 1.5
            elif u not in S and v in S:
                color, ancho = OSCURO, 1.3
            else:
                color, ancho = REGLA.darker(0.35), 0.9
            _arista(_p(pos, u, o), _p(pos, v, o), f"{f}/{c}", color=color,
                    ancho=ancho, lado=_lado(pos, u, v),
                    color_texto=color if ancho > 1 else APAGADO)
        _vertices(pos, nombres, o, relleno)
        cap = sum(c for u, v, c in aristas if u in S and v not in S)
        lado_s = ", ".join(nombres[v] for v in sorted(S))
        _txt(f"S = {{{lado_s}}}: rojo, de S a T, saturadas; azul, de T a S, vacías;"
             f" capacidad {cap}", Point(140, 138), color=APAGADO, size=PIE)
    return _figura(canvas, ident, pie)
