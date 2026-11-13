"""Figuras del capítulo 20: resolver exacto un problema NP-duro.

Cada figura recibe lo que calculó el código del capítulo: el registro de nodos que
dejó branch and bound, el registro del árbol de búsqueda de vertex cover y las
llamadas que contó la ramificación de conjunto independiente.
"""

import math

from tesserax import Canvas, Colors, Line, Point, Polyline, Rect

from figuras import (
    ACENTO, ALARMA, APAGADO, CALIDO, CUERPO, OSCURO, PIE, REGLA, TINTA,
    _figura, _punto, _txt, sup,
)


def _coma(x, d=1):
    return f"{x:.{d}f}".replace(".", ",")


def _posiciones(nodos, padre_de, dx, dy):
    """Coloca las hojas de izquierda a derecha en el orden del registro (que es el de
    la búsqueda) y cada padre en el medio de sus hijos."""
    hijos = {v: [] for v in nodos}
    raiz = None
    for v in nodos:
        p = padre_de[v]
        if p is None:
            raiz = v
        else:
            hijos[p].append(v)
    pos, siguiente = {}, [0]

    def colocar(v, nivel):
        if not hijos[v]:
            pos[v] = Point(siguiente[0] * dx, nivel * dy)
            siguiente[0] += 1
            return
        for h in hijos[v]:
            colocar(h, nivel + 1)
        xs = [pos[h].x for h in hijos[v]]
        pos[v] = Point((min(xs) + max(xs)) / 2, nivel * dy)

    colocar(raiz, 0)
    return pos


def arbol_bb(registro, ident="exactos-bb", pie=""):
    """`registro`: los nodos que visitó `mochila_bb`, con su padre, la decisión que
    los creó, el valor acumulado, la cota y si se abrieron, se podaron o son hoja."""
    nodos = [r["id"] for r in registro]
    padre_de = {r["id"]: r["padre"] for r in registro}
    datos = {r["id"]: r for r in registro}
    pos = _posiciones(nodos, padre_de, dx=46.0, dy=50.0)
    with Canvas() as canvas:
        for v in nodos:
            p = padre_de[v]
            if p is not None:
                r = datos[v]
                color = APAGADO if r["estado"] == "poda" else REGLA
                Line(pos[p], pos[v], stroke=color, width=1.1)
                mx = (pos[p].x + pos[v].x) / 2
                my = (pos[p].y + pos[v].y) / 2
                signo, obj = r["etiqueta"][0], int(r["etiqueta"][1:])
                texto = f"{'+' if signo == '+' else '−'}{obj}"
                _txt(texto, Point(mx + (-9 if pos[v].x < pos[p].x else 9), my),
                     color=CALIDO if signo == "+" else APAGADO, size=PIE)
        for v in nodos:
            r = datos[v]
            if r["estado"] == "poda":
                fondo, borde, color = Colors.White, APAGADO, APAGADO
            elif r["estado"] == "hoja":
                fondo, borde, color = ACENTO.transparent(0.15), OSCURO, OSCURO
            else:
                fondo, borde, color = Colors.White, TINTA, TINTA
            Rect(40, 26, fill=fondo, stroke=borde, width=1.0).move_to(pos[v])
            _txt(str(r["val"]), Point(pos[v].x, pos[v].y - 5), color=color,
                 size=CUERPO)
            cota = "—" if r["estado"] == "hoja" else _coma(r["cota"])
            _txt(cota, Point(pos[v].x, pos[v].y + 7), color=color, size=PIE)
            if r["estado"] == "poda":
                _txt("✗", Point(pos[v].x, pos[v].y + 22), color=ALARMA, size=CUERPO)
    return _figura(canvas, ident, pie)


def arbol_cover(registro, ident="exactos-cover", pie=""):
    """`registro`: los nodos de `cover_k`, en el orden de la búsqueda, con la arista
    que eligió cada uno, el vértice que lo creó y cómo terminó."""
    nodos = list(range(len(registro)))
    padre_de = {i: r["padre"] for i, r in enumerate(registro)}
    pos = _posiciones(nodos, padre_de, dx=34.0, dy=52.0)
    with Canvas() as canvas:
        for i in nodos:
            p = padre_de[i]
            if p is not None:
                Line(pos[p], pos[i], stroke=REGLA, width=1.1)
                mx = (pos[p].x + pos[i].x) / 2
                my = (pos[p].y + pos[i].y) / 2
                _txt(registro[i]["etiqueta"],
                     Point(mx + (-7 if pos[i].x < pos[p].x else 7), my),
                     color=CALIDO, size=PIE)
        for i in nodos:
            r = registro[i]
            if r.get("fin") == "no":
                Rect(26, 18, fill=Colors.White, stroke=APAGADO,
                     width=1.0).move_to(pos[i])
                _txt("✗", pos[i], color=ALARMA, size=CUERPO)
            elif r.get("fin") == "sí":
                Rect(26, 18, fill=ACENTO.transparent(0.15), stroke=OSCURO,
                     width=1.0).move_to(pos[i])
                _txt("✓", pos[i], color=OSCURO, size=CUERPO)
            else:
                u, v = r["arista"]
                Rect(30, 18, fill=Colors.White, stroke=TINTA,
                     width=1.0).move_to(pos[i])
                _txt(f"{u}–{v}", pos[i], color=TINTA, size=PIE)
        niveles = max(p.y for p in pos.values())
        x0 = min(p.x for p in pos.values()) - 30
        for nivel in range(int(round(niveles / 52.0)) + 1):
            _txt(f"k = {registro[0]['k'] - nivel}", Point(x0, nivel * 52.0),
                 color=APAGADO, size=PIE, anchor="end")
    return _figura(canvas, ident, pie)


def grafica_semilog(series, titulo_x, titulo_y, ident="exactos-llamadas", pie=""):
    """series: {nombre: [(n, valor), ...]}, con la y en escala logarítmica."""
    ancho, alto = 300.0, 190.0
    todos = [p for s in series.values() for p in s]
    x0, x1 = min(x for x, _ in todos), max(x for x, _ in todos)
    y0 = math.floor(min(math.log10(y) for _, y in todos))
    y1 = math.ceil(max(math.log10(y) for _, y in todos))
    px = lambda x: (x - x0) / ((x1 - x0) or 1) * ancho
    py = lambda y: alto - (math.log10(y) - y0) / ((y1 - y0) or 1) * alto
    colores = [OSCURO, CALIDO, APAGADO, ALARMA]
    with Canvas() as canvas:
        for x in sorted({x for x, _ in todos}):
            Line(Point(px(x), 0), Point(px(x), alto), stroke=REGLA, width=0.5)
            _txt(str(x), Point(px(x), alto + 12), color=APAGADO, size=PIE)
        paso = 1 if y1 - y0 <= 8 else 2
        for e in range(y0, y1 + 1, paso):
            Line(Point(0, py(10 ** e)), Point(ancho, py(10 ** e)), stroke=REGLA,
                 width=0.7)
            _txt(f"10{sup(e)}", Point(-8, py(10 ** e)), color=APAGADO, size=PIE,
                 anchor="end")
        for k, (nombre, puntos) in enumerate(series.items()):
            color = colores[k % len(colores)]
            Polyline([Point(px(x), py(y)) for x, y in puntos], stroke=color,
                     width=1.7)
            for x, y in puntos:
                _punto(Point(px(x), py(y)), color, r=2.4)
            _txt(nombre, Point(ancho + 12, 12 + k * 15), color=color, size=CUERPO,
                 anchor="start")
        _txt(titulo_x, Point(ancho / 2, alto + 28), color=APAGADO, size=PIE)
        _txt(titulo_y, Point(-8, -12), color=APAGADO, size=PIE, anchor="end")
    return _figura(canvas, ident, pie)
