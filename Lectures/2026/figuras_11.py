"""Figuras del capítulo 11: programación dinámica sobre árboles y subconjuntos.

Cada función recibe el estado que calculó el código del capítulo (los padres, los
pesos, los dos valores de cada vértice, los valores re-enraizados, los tiempos) y no
decide nada del algoritmo.
"""

import math

from tesserax import Canvas, Circle, Line, Point, Polyline, Rect

from figuras import (
    ACENTO, ALARMA, APAGADO, CALIDO, CUERPO, OSCURO, PIE, REGLA, TINTA,
    _figura, _punto, _txt, sup,
)
from tesserax import Colors


def _posiciones(padre, dx=62.0, dy=58.0):
    """Hojas en orden de recorrido, cada padre centrado sobre sus hijos."""
    n = len(padre)
    hijos = [[] for _ in range(n)]
    for v in range(1, n):
        hijos[padre[v]].append(v)
    x, prof = [0.0] * n, [0] * n
    siguiente = [0]

    def colocar(v):
        if not hijos[v]:
            x[v] = siguiente[0] * dx
            siguiente[0] += 1
            return
        for c in hijos[v]:
            prof[c] = prof[v] + 1
            colocar(c)
        x[v] = sum(x[c] for c in hijos[v]) / len(hijos[v])

    colocar(0)
    return {v: Point(x[v], prof[v] * dy) for v in range(n)}, hijos


def _aristas(padre, pos, resaltada=None):
    for v in range(1, len(padre)):
        marcada = v == resaltada
        Line(pos[padre[v]], pos[v], stroke=ALARMA if marcada else APAGADO,
             width=2.4 if marcada else 1.0)


# --------------------------------------------------------------------------
# 1. el árbol con los dos valores de cada vértice
# --------------------------------------------------------------------------

def arbol_dos_valores(padre, w, tom, no, conjunto, ident="dp-arboles-dos-valores",
                      pie=""):
    """`conjunto` es el conjunto óptimo que reconstruyó el capítulo."""
    pos, _ = _posiciones(padre)
    with Canvas() as canvas:
        _aristas(padre, pos)
        for v, p in pos.items():
            dentro = v in conjunto
            Circle(12, fill=OSCURO.transparent(0.22) if dentro else Colors.White,
                   stroke=OSCURO if dentro else TINTA,
                   width=1.8 if dentro else 0.9).move_to(p)
            _txt(str(w[v]), p, size=CUERPO)
            _txt(f"v{v}", Point(p.x - 15, p.y - 13), color=APAGADO, size=PIE,
                 anchor="end")
            etiqueta = f"{tom[v]} | {no[v]}"
            Rect(len(etiqueta) * 5.2 + 4, 12, fill=Colors.White,
                 stroke=Colors.White, width=0).move_to(Point(p.x, p.y + 22))
            _txt(etiqueta, Point(p.x, p.y + 22), color=CALIDO, size=CUERPO)
    return _figura(canvas, ident, pie)


# --------------------------------------------------------------------------
# 2. re-enraizamiento: lo que sube y lo que baja por una arista
# --------------------------------------------------------------------------

def reenraizar(padre, w, tom, no, arr_tom, arr_no, v, ident="dp-arboles-reenraizar",
               pie=""):
    """`v` es el vértice cuya arista con su padre se resalta. Los valores que
    suben son (tom[v], no[v]); los que bajan, (arr_tom[v], arr_no[v])."""
    pos, hijos = _posiciones(padre)
    debajo, pila = set(), [v]
    while pila:
        u = pila.pop()
        debajo.add(u)
        pila.extend(hijos[u])
    with Canvas() as canvas:
        _aristas(padre, pos, resaltada=v)
        for u, p in pos.items():
            color = OSCURO if u in debajo else CALIDO
            Circle(12, fill=color.transparent(0.16), stroke=color, width=1.0).move_to(p)
            _txt(str(w[u]), p, size=CUERPO)
            _txt(f"v{u}", Point(p.x - 15, p.y - 13), color=APAGADO, size=PIE,
                 anchor="end")
        a, b = pos[padre[v]], pos[v]
        m = Point((a.x + b.x) / 2, (a.y + b.y) / 2)
        lado = 1 if b.x >= a.x else -1
        ancla = "start" if lado > 0 else "end"
        _txt(f"sube ({tom[v]}, {no[v]})", Point(m.x + lado * 14, m.y + 9),
             color=OSCURO, size=CUERPO, anchor=ancla)
        _txt(f"baja ({arr_tom[v]}, {arr_no[v]})", Point(m.x + lado * 14, m.y - 9),
             color=CALIDO, size=CUERPO, anchor=ancla)
    return _figura(canvas, ident, pie)


# --------------------------------------------------------------------------
# 3. tiempos con la y logarítmica y la x lineal
# --------------------------------------------------------------------------

def grafica_semilog(series, titulo_x, titulo_y, ident="dp-arboles-tiempos", pie=""):
    """series: {nombre: [(n, segundos), ...]}. La x es lineal porque n es pequeño
    y lo que se quiere ver es la pendiente de una exponencial."""
    ancho, alto = 300.0, 180.0
    todos = [p for s in series.values() for p in s]
    x0, x1 = min(x for x, _ in todos), max(x for x, _ in todos)
    y0 = math.floor(min(math.log10(y) for _, y in todos))
    y1 = math.ceil(max(math.log10(y) for _, y in todos))
    px = lambda x: (x - x0) / ((x1 - x0) or 1) * ancho
    py = lambda y: alto - (math.log10(y) - y0) / ((y1 - y0) or 1) * alto
    colores = [CALIDO, OSCURO, ACENTO, ALARMA]
    with Canvas() as canvas:
        for x in range(x0, x1 + 1):
            Line(Point(px(x), 0), Point(px(x), alto), stroke=REGLA, width=0.5)
            _txt(str(x), Point(px(x), alto + 12), color=APAGADO, size=PIE)
        for e in range(y0, y1 + 1):
            Line(Point(0, py(10 ** e)), Point(ancho, py(10 ** e)), stroke=REGLA,
                 width=0.7)
            _txt(f"10{sup(e)}", Point(-8, py(10 ** e)), color=APAGADO, size=PIE,
                 anchor="end")
        for k, (nombre, puntos) in enumerate(series.items()):
            color = colores[k % len(colores)]
            Polyline([Point(px(x), py(y)) for x, y in puntos], stroke=color, width=1.7)
            for x, y in puntos:
                _punto(Point(px(x), py(y)), color, r=2.6)
            _txt(nombre, Point(ancho + 12, 12 + k * 15), color=color, size=CUERPO,
                 anchor="start")
        _txt(titulo_x, Point(ancho / 2, alto + 28), color=APAGADO, size=PIE)
        _txt(titulo_y, Point(-8, -12), color=APAGADO, size=PIE, anchor="end")
    return _figura(canvas, ident, pie)
