"""Figuras del capítulo 15: algoritmos aleatorios II, Monte Carlo.

Cada función recibe el estado que calculó el código del capítulo: el orden real en
que una corrida de Karger contrajo las aristas, las fracciones de matrices erróneas
que pasaron k rondas de Freivalds, y las probabilidades de éxito medidas.
"""

import math

from tesserax import Canvas, Colors, Line, Point, Polyline

from figuras import (
    ACENTO, ALARMA, APAGADO, CALIDO, CUERPO, OSCURO, PIE, REGLA, TINTA,
    _figura, _punto, _txt, sup,
)


def _punteada(p, q, color=APAGADO, width=0.8, paso=3.0):
    """tesserax no tiene dasharray: la línea de trazos se hace con segmentos."""
    largo = math.dist((p.x, p.y), (q.x, q.y))
    k = max(1, int(largo / (2 * paso)))
    for i in range(k):
        a, b = 2 * i * paso / largo, min(1.0, (2 * i + 1) * paso / largo)
        Line(Point(p.x + (q.x - p.x) * a, p.y + (q.y - p.y) * a),
             Point(p.x + (q.x - p.x) * b, p.y + (q.y - p.y) * b),
             stroke=color, width=width)


def contraccion(n, aristas, pos, contraidas, ident="mc-contraccion", pie=""):
    """`contraidas` es la lista de aristas que la corrida contrajo, en orden.
    `pos[v]` es la posición de dibujo del vértice v, con la y hacia arriba."""
    escala, ancho, alto, por_fila = 42.0, 175.0, 112.0, 4
    padre = list(range(n))

    def raiz(x):
        while padre[x] != x:
            x = padre[x]
        return x

    with Canvas() as canvas:
        for t in range(len(contraidas) + 1):
            ox = (t % por_fila) * ancho
            oy = (t // por_fila) * alto
            P = {v: Point(ox + 12 + pos[v][0] * escala, oy + 22 + (1 - pos[v][1]) * escala)
                 for v in range(n)}
            hechas = set(contraidas[:t])
            siguiente = contraidas[t] if t < len(contraidas) else None
            for u, v in aristas:
                if (u, v) in hechas:                       # la arista que unió dos grupos
                    Line(P[u], P[v], stroke=ACENTO.transparent(0.35), width=7.0)
                elif raiz(u) == raiz(v):                   # lazo: ya no cuenta
                    _punteada(P[u], P[v], color=REGLA)
                elif (u, v) == siguiente:
                    Line(P[u], P[v], stroke=OSCURO, width=3.0)
                elif siguiente is None:                    # el corte que devuelve
                    Line(P[u], P[v], stroke=CALIDO, width=3.0)
                else:
                    Line(P[u], P[v], stroke=TINTA, width=0.9)
            for v in range(n):
                _punto(P[v], TINTA, r=8.5)
                _txt(str(v), P[v], color=Colors.White, size=CUERPO)
            vivos = n - t
            texto = (f"{vivos} vértices" if siguiente is not None
                     else f"2 vértices: corte de {sum(raiz(u) != raiz(v) for u, v in aristas)}")
            _txt(texto, Point(ox + 12 + 1.5 * escala, oy + 22 + escala + 18),
                 color=CALIDO if siguiente is None else APAGADO, size=11.0)
            if siguiente is not None:
                a, b = raiz(siguiente[0]), raiz(siguiente[1])
                padre[a] = b
    return _figura(canvas, ident, pie)


def _ejes_log(ancho, alto, xs, y0, y1, px, py, titulo_x, titulo_y):
    for e in range(y0, y1 + 1):
        Line(Point(0, py(10 ** e)), Point(ancho, py(10 ** e)), stroke=REGLA, width=0.7)
        _txt("1" if e == 0 else f"10{sup(e)}", Point(-8, py(10 ** e)), color=APAGADO,
             size=CUERPO, anchor="end")
    for x in xs:
        Line(Point(px(x), alto), Point(px(x), alto + 4), stroke=APAGADO, width=0.8)
        _txt(str(x), Point(px(x), alto + 13), color=APAGADO, size=CUERPO)
    _txt(titulo_x, Point(ancho / 2, alto + 29), color=APAGADO, size=CUERPO)
    _txt(titulo_y, Point(-8, py(10 ** y1) - 14), color=APAGADO, size=CUERPO,
         anchor="start")


def _serie(puntos, color, px, py, linea=True):
    vis = [(x, y) for x, y in puntos if y > 0]
    if linea and len(vis) > 1:
        Polyline([Point(px(x), py(y)) for x, y in vis], stroke=color, width=1.5)
    for x, y in vis:
        _punto(Point(px(x), py(y)), color, r=2.8)


def grafica_semilog(series, curva, titulo_x, titulo_y, ident, pie, y0=None):
    """`series`: lista de (nombre, [(x, y)], color), medidas. `curva`: (nombre,
    [(x, y)], color), la cota teórica, que se dibuja de trazos. Los y = 0 no se
    pueden dibujar en escala log y se omiten (el pie lo dice)."""
    ancho, alto = 300.0, 170.0
    todos = [p for _, s, _ in series for p in s if p[1] > 0] + curva[1]
    xs = sorted({x for x, _ in todos})
    y1 = 0
    y0 = y0 if y0 is not None else math.floor(min(math.log10(y) for _, y in todos))
    px = lambda x: (x - xs[0]) / ((xs[-1] - xs[0]) or 1) * ancho
    py = lambda y: alto - (math.log10(y) - y0) / ((y1 - y0) or 1) * alto
    with Canvas() as canvas:
        _ejes_log(ancho, alto, xs, y0, y1, px, py, titulo_x, titulo_y)
        nombre, puntos, color = curva
        for (xa, ya), (xb, yb) in zip(puntos, puntos[1:]):
            _punteada(Point(px(xa), py(ya)), Point(px(xb), py(yb)), color=color,
                      width=1.3)
        etiquetas = [(nombre, color, puntos[-1][1])]
        for nombre_s, puntos_s, color_s in series:
            _serie(puntos_s, color_s, px, py)
            ultimo = [y for _, y in puntos_s if y > 0][-1]
            etiquetas.append((nombre_s, color_s, ultimo))
        # etiquetas a la derecha, ordenadas por altura y separadas al menos 13
        etiquetas.sort(key=lambda e: py(e[2]))
        ys = []
        for _, _, y in etiquetas:
            yy = py(y)
            if ys and yy < ys[-1] + 13:
                yy = ys[-1] + 13
            ys.append(yy)
        for (texto, color, _), yy in zip(etiquetas, ys):
            _txt(texto, Point(ancho + 8, yy), color=color, size=CUERPO, anchor="start")
    return _figura(canvas, ident, pie)
