"""Figuras de las conferencias de DAA 2026.

Cada función pública devuelve una cadena `<figure>` lista para imprimir desde un
bloque ```{python echo=false output=asis} de scriptorium.

Las figuras que ilustran un algoritmo reciben el estado que el algoritmo calculó
—el δ real, la franja real, la rejilla real— y nunca posiciones puestas a mano.
Así una figura no puede contradecir al código de la conferencia.

Convenio de coordenadas: las funciones reciben puntos en coordenadas de datos con
la `y` creciendo hacia arriba, y las vuelcan a coordenadas SVG (`y` hacia abajo).
"""

import math

from tesserax import (
    Canvas, Circle, Colors, Group, Line, Arrow, Point, Polyline, Rect, Text,
)
from tesserax.color import hex

# Paleta tomada del tema `note` de scriptorium, para que las figuras y el
# documento sean el mismo objeto visual.
TINTA = hex("#1a1a1a")
APAGADO = hex("#6b7280")
REGLA = hex("#d8dce3")
ACENTO = hex("#0891b2")
OSCURO = hex("#0e7490")
CALIDO = hex("#b45309")
ALARMA = hex("#be123c")

CUERPO = 9.0
PIE = 7.5

_SUB = "₀₁₂₃₄₅₆₇₈₉"
_SUP = {"-": "⁻", "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴",
        "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹"}


def sub(n):
    # el menos lleva su propio subíndice (U+208B); sin esto, sub(-1) revienta
    return "".join("\u208b" if c == "-" else _SUB[int(c)] for c in str(n))


def sup(n):
    return "".join(_SUP[c] for c in str(n))


# --------------------------------------------------------------------------
# infraestructura
# --------------------------------------------------------------------------

def _figura(canvas, ident, pie, padding=14):
    canvas.fit(padding)
    return (f'<figure id="fig-{ident}">{canvas}'
            f'<figcaption>{pie}</figcaption></figure>')


class Marco:
    """Vuelca coordenadas de datos a coordenadas de dibujo, con la y invertida."""

    def __init__(self, puntos, ancho=360.0, alto=200.0, margen=10.0):
        xs = [p[0] for p in puntos] or [0.0, 1.0]
        ys = [p[1] for p in puntos] or [0.0, 1.0]
        self.x0, self.x1 = min(xs), max(xs)
        self.y0, self.y1 = min(ys), max(ys)
        self.ancho, self.alto, self.margen = ancho, alto, margen
        dx = (self.x1 - self.x0) or 1.0
        dy = (self.y1 - self.y0) or 1.0
        self.escala = min((ancho - 2 * margen) / dx, (alto - 2 * margen) / dy)
        # sobrantes, para que el contenido quede centrado en el recuadro
        self.ox = (ancho - dx * self.escala) / 2
        self.oy = (alto - dy * self.escala) / 2

    def __call__(self, p):
        return Point(self.ox + (p[0] - self.x0) * self.escala,
                     self.alto - self.oy - (p[1] - self.y0) * self.escala)

    def largo(self, d):
        return d * self.escala


def _punto(xy, color=TINTA, r=2.6):
    return Circle(r, fill=color, stroke=color, width=0.5).move_to(xy)


# El `anchor` de Text no coloca nada: tesserax compensa el translate para que la
# caja quede igual, y move_to la recentra sobre el punto. El que alinea de verdad
# es el `anchor` de move_to, que sí es de caja.
_ANCLA = {"middle": "center", "start": "left", "end": "right"}


def _txt(texto, xy, color=TINTA, size=CUERPO, anchor="middle"):
    return Text(texto, size=size, fill=color, anchor="middle",
                font="Inter, sans-serif").move_to(xy, anchor=_ANCLA[anchor])


def _cota_h(a, b, y, texto, color=CALIDO, dy=-6):
    Line(Point(a, y), Point(b, y), stroke=color, width=0.9,
         marker_start="arrow", marker_end="arrow")
    _txt(texto, Point((a + b) / 2, y + dy), color=color, size=PIE)


def _cota_v(x, a, b, texto, color=CALIDO, dx=-10):
    Line(Point(x, a), Point(x, b), stroke=color, width=0.9,
         marker_start="arrow", marker_end="arrow")
    _txt(texto, Point(x + dx, (a + b) / 2), color=color, size=PIE,
         anchor="end" if dx < 0 else "start")


# --------------------------------------------------------------------------
# 1. el ciclo de las cinco preguntas
# --------------------------------------------------------------------------

ETAPAS = ["problema", "algoritmo", "correctitud", "complejidad", "cota mínima"]


def ciclo(resaltar=None, ident="ciclo", pie=""):
    rx, ry, w, h = 150.0, 78.0, 84.0, 24.0
    with Canvas() as canvas:
        centros = []
        for i in range(5):
            ang = -math.pi / 2 + i * 2 * math.pi / 5
            centros.append(Point(rx * math.cos(ang), ry * math.sin(ang)))
        for i in range(5):
            a, b = centros[i], centros[(i + 1) % 5]
            dx, dy = b.x - a.x, b.y - a.y
            n = math.hypot(dx, dy)
            ux, uy = dx / n, dy / n
            rec = (w / 2 + 6, h / 2 + 5)
            k1 = min(rec[0] / abs(ux) if ux else 1e9, rec[1] / abs(uy) if uy else 1e9)
            k2 = min(rec[0] / abs(ux) if ux else 1e9, rec[1] / abs(uy) if uy else 1e9)
            Arrow(Point(a.x + ux * k1, a.y + uy * k1),
                  Point(b.x - ux * k2, b.y - uy * k2),
                  stroke=REGLA.darker(0.35), width=1.1, marker_end="arrow")
        for i, c in enumerate(centros):
            activa = (i == resaltar)
            Rect(w, h, fill=ACENTO.transparent(0.14) if activa else Colors.White,
                 stroke=OSCURO if activa else APAGADO,
                 width=1.6 if activa else 0.9).move_to(c)
            _txt(ETAPAS[i], c, color=TINTA if activa else APAGADO, size=PIE)
    return _figura(canvas, ident, pie)


# --------------------------------------------------------------------------
# 2. dos problemas parecidos
# --------------------------------------------------------------------------

def dos_problemas(P, par, vecinos, ident="dos-problemas", pie=""):
    W, H = 188.0, 168.0
    with Canvas() as canvas:
        for k, (titulo, enlaces) in enumerate(
                [("par más cercano: una respuesta", [par]),
                 ("vecino más cercano: n respuestas", vecinos)]):
            with Group() as panel:
                m = Marco(P, ancho=W, alto=H, margen=14)
                Rect(W, H, stroke=REGLA, width=1.0).move_to(Point(W / 2, H / 2))
                for a, b in enlaces:
                    Line(m(a), m(b), stroke=ACENTO, width=1.4)
                for p in P:
                    _punto(m(p), APAGADO, r=2.2)
                for a, b in enlaces:
                    _punto(m(a), OSCURO, r=2.8)
                    _punto(m(b), OSCURO, r=2.8)
                if k == 0:   # sin el círculo, el par más cercano no se ve
                    c = Point((m(par[0]).x + m(par[1]).x) / 2,
                              (m(par[0]).y + m(par[1]).y) / 2)
                    Circle(13, stroke=ALARMA, width=1.2).move_to(c)
                _txt(titulo, Point(W / 2, H + 13), color=APAGADO, size=PIE)
            panel.translated(k * (W + 26), 0)
    return _figura(canvas, ident, pie)


# --------------------------------------------------------------------------
# 3. el calentamiento en una dimensión
# --------------------------------------------------------------------------

def recta_1d(xs, i, ident="recta-1d", pie=""):
    xs = sorted(xs)
    ancho = 370.0
    lo, hi = min(xs), max(xs)
    px = lambda x: (x - lo) / ((hi - lo) or 1) * ancho
    with Canvas() as canvas:
        Line(Point(-10, 0), Point(ancho + 10, 0), stroke=APAGADO, width=1.0)
        for k, x in enumerate(xs):
            activo = k in (i, i + 1)
            _punto(Point(px(x), 0), OSCURO if activo else TINTA,
                   r=3.4 if activo else 2.4)
            _txt(f"x{sub(k + 1)}", Point(px(x), -13),
                 color=OSCURO if activo else APAGADO, size=PIE)
        for k in range(len(xs) - 1):
            medio = (px(xs[k]) + px(xs[k + 1])) / 2
            _txt("·" if k != i else "", Point(medio, 16), color=REGLA, size=PIE)
        _cota_h(px(xs[i]), px(xs[i + 1]), 22, "el hueco mínimo", color=ACENTO, dy=12)
        _txt("hay n − 1 huecos entre consecutivos, y el par más cercano es uno de ellos",
             Point(ancho / 2, 48), color=APAGADO, size=PIE)
    return _figura(canvas, ident, pie)


# --------------------------------------------------------------------------
# 4. el corte, delta y la franja
# --------------------------------------------------------------------------

def corte_y_franja(Q, medio, delta, franja, par_izq, par_der,
                   ident="franja", pie=""):
    m = Marco(Q, ancho=360, alto=210, margen=16)
    corte = Q[medio][0]
    xc = m((corte, 0)).x
    semi = m.largo(delta)
    with Canvas() as canvas:
        Rect(2 * semi, m.alto, fill=ACENTO.transparent(0.13),
             stroke=Colors.Transparent).move_to(Point(xc, m.alto / 2))
        Line(Point(xc, -6), Point(xc, m.alto + 6), stroke=ALARMA, width=1.3)
        for j, p in enumerate(Q):
            _punto(m(p), OSCURO if j < medio else CALIDO, r=2.5)
        for j in franja:
            Circle(5.0, stroke=ACENTO, width=1.2).move_to(m(Q[j]))
        for (d2, par), color, nombre, lado in [
                (par_izq, OSCURO, "δ izq", -1), (par_der, CALIDO, "δ der", 1)]:
            if par is None:
                continue
            Line(m(par[0]), m(par[1]), stroke=color, width=2.2)
            c = Point((m(par[0]).x + m(par[1]).x) / 2,
                      (m(par[0]).y + m(par[1]).y) / 2)
            etq = Point(c.x + lado * 26, c.y - 16)
            Line(c, etq, stroke=color.transparent(0.45), width=0.7)
            _txt(nombre, Point(etq.x, etq.y - 6), color=color, size=PIE)
        _cota_h(xc - semi, xc + semi, m.alto + 18, "2δ", dy=11)
        _txt("L", Point(xc, -16), color=ALARMA, size=CUERPO)
        _txt("δ = mín(δ izquierda, δ derecha); solo los puntos de la franja "
             "pueden mejorarlo",
             Point(m.ancho / 2, m.alto + 40), color=APAGADO, size=PIE)
    return _figura(canvas, ident, pie)


# --------------------------------------------------------------------------
# 5 y 6. el rectángulo extremo, compartido por las dos figuras
# --------------------------------------------------------------------------

# Un punto por cuadrado, que es lo máximo que permite el lema. Coordenadas en
# unidades de δ: x ∈ [0, 2], y ∈ [0, 1], con la y creciendo hacia arriba.
_RELLENO = [(0.32, 0.36), (0.70, 0.22), (0.34, 0.70), (0.78, 0.58),
            (0.26, 0.30), (0.62, 0.34), (0.42, 0.68), (0.72, 0.72)]
_CELDAS = [(i, j) for j in range(2) for i in range(4)]
# el par a distancia menor que δ; p es el de abajo, que es el que escanea
_P, _Q = 6, 1


def rectangulo_extremo():
    """Los ocho puntos del rectángulo δ×2δ, en unidades de δ, en coordenadas de
    dibujo (la y crece hacia abajo), y las posiciones de p y q. Las figuras 5 y 6
    dibujan exactamente la misma configuración."""
    pts = []
    for k, (i, j) in enumerate(_CELDAS):
        fx, fy = _RELLENO[k]
        pts.append(((i + fx) / 2, (j + fy) / 2))
    return pts, _P, _Q


def empaquetamiento(ident="empaquetamiento", pie=""):
    D = 116.0
    alto_franja = D + 110
    with Canvas() as canvas:
        Rect(2 * D, alto_franja, fill=ACENTO.transparent(0.09),
             stroke=Colors.Transparent).move_to(
            Point(D, D / 2), anchor="center")
        for i in range(4):
            for j in range(2):
                Rect(D / 2, D / 2, stroke=REGLA.darker(0.2), width=0.9).move_to(
                    Point(i * D / 2, j * D / 2), anchor="topleft")
        Rect(2 * D, D, stroke=TINTA, width=1.8).move_to(
            Point(0, 0), anchor="topleft")
        Line(Point(D, -(alto_franja - D) / 2), Point(D, D + (alto_franja - D) / 2),
             stroke=ALARMA, width=1.3)
        _txt("L", Point(D + 9, D + 48), color=ALARMA, size=CUERPO)
        pts, p_idx, q_idx = rectangulo_extremo()
        for k, (x, y) in enumerate(pts):
            c = Point(x * D, y * D)   # la y del dibujo va hacia abajo
            if k == p_idx:
                p = c
            elif k == q_idx:
                q = c
            else:
                _punto(c, APAGADO, r=2.4)
            _txt(f"y{sub(sorted(range(8), key=lambda i: -pts[i][1]).index(k) + 1)}",
                 Point(c.x + 10, c.y - 7), color=REGLA.darker(0.45), size=PIE)
        Line(p, q, stroke=ACENTO, width=1.7)
        _punto(p, OSCURO, r=3.4)
        _punto(q, OSCURO, r=3.4)
        _txt("p", Point(p.x - 11, p.y - 7), color=OSCURO, size=CUERPO)
        _txt("q", Point(q.x - 11, q.y + 9), color=OSCURO, size=CUERPO)
        # la diagonal de un cuadrado vacío, arriba a la derecha
        Line(Point(1.5 * D, 0), Point(2.0 * D, 0.5 * D), stroke=CALIDO, width=1.2)
        _txt("δ/√2 < δ", Point(2.0 * D + 8, 0.30 * D), color=CALIDO, size=PIE,
             anchor="start")
        _cota_h(0, 2 * D, -16, "2δ, el ancho de la franja")
        _cota_v(-16, 0, D, "δ")
        _txt("cada cuadrado tiene lado δ/2 y por tanto a lo sumo un punto: "
             "el rectángulo entero aguanta 8",
             Point(D, D + 68), color=APAGADO, size=PIE)
    return _figura(canvas, ident, pie)


# --------------------------------------------------------------------------
# 6. el orden por y dentro de la franja
# --------------------------------------------------------------------------

def orden_por_y(k, a, b, ident="orden-y", pie=""):
    """`k` es cuántos puntos tiene la franja; (a, b) son las posiciones de p y q en
    el orden por y. El lema habla de posiciones en el orden, no de alturas, así que
    la figura las dibuja equiespaciadas."""
    paso = 26.0
    alto = (k - 1) * paso
    hasta = min(a + 7, k - 1)
    with Canvas() as canvas:
        Rect(120, (hasta - a) * paso, fill=ACENTO.transparent(0.14),
             stroke=Colors.Transparent).move_to(
            Point(22, alto - (a + hasta) / 2 * paso))
        Line(Point(0, -12), Point(0, alto + 12), stroke=REGLA.darker(0.25),
             width=1.0)
        for i in range(k):
            y = alto - i * paso
            activo = a <= i <= hasta
            color = OSCURO if i in (a, b) else (ACENTO if activo else APAGADO)
            Line(Point(-6, y), Point(6, y), stroke=color,
                 width=1.8 if i in (a, b) else 1.0)
            _punto(Point(0, y), color, r=3.2 if i in (a, b) else 2.2)
            _txt(f"y{sub(i + 1)}", Point(-15, y), color=color, size=PIE,
                 anchor="end")
        _txt("p", Point(13, alto - a * paso), color=OSCURO, size=CUERPO,
             anchor="start")
        _txt("q", Point(13, alto - b * paso), color=OSCURO, size=CUERPO,
             anchor="start")
        _cota_v(78, alto - a * paso, alto - hasta * paso,
                "los 7 siguientes", color=ACENTO, dx=8)
        _cota_v(-52, alto - a * paso, alto - b * paso, "d(p,q) < δ",
                color=CALIDO, dx=-8)
        _txt("y creciente ↑", Point(0, alto + 26), color=APAGADO, size=PIE)
        _txt(f"q está {b - a} posiciones después de p: el lema garantiza que "
             f"nunca pasa de 7",
             Point(0, alto + 40), color=APAGADO, size=PIE)
    return _figura(canvas, ident, pie)


# --------------------------------------------------------------------------
# 7. el árbol de recursión
# --------------------------------------------------------------------------

def arbol_recursion(niveles=4, ident="arbol-recursion", pie=""):
    ancho, paso_y = 250.0, 50.0
    with Canvas() as canvas:
        centros = {}
        for nivel in range(niveles):
            k = 2 ** nivel
            w = min(ancho / k - 5, 84)
            for i in range(k):
                c = Point((i + 0.5) * ancho / k, nivel * paso_y)
                centros[(nivel, i)] = c
                Rect(w, 16, fill=ACENTO.transparent(0.12), stroke=OSCURO,
                     width=0.9).move_to(c)
                if k <= 4:
                    _txt("n" if k == 1 else f"n/{k}", c, color=TINTA, size=PIE)
                if nivel:
                    Line(centros[(nivel - 1, i // 2)], c,
                         stroke=REGLA.darker(0.25), width=0.9)
            _txt("O(n)" if k == 1 else f"{k} × O(n/{k}) = O(n)",
                 Point(ancho + 40, nivel * paso_y), color=APAGADO, size=PIE,
                 anchor="start")
        _txt("⋮", Point(ancho / 2, (niveles - 0.45) * paso_y), color=APAGADO)
        _cota_v(-22, 0, (niveles - 1) * paso_y, "log₂ n niveles")
        _txt("total: O(n log n)", Point(ancho + 40, (niveles - 0.1) * paso_y),
             color=TINTA, size=CUERPO, anchor="start")
    return _figura(canvas, ident, pie)


# --------------------------------------------------------------------------
# 8. la reducción
# --------------------------------------------------------------------------

def reduccion(xs, ident="reduccion", pie=""):
    ancho = 300.0
    lo, hi = min(xs), max(xs)
    px = lambda x: (x - lo) / ((hi - lo) or 1) * ancho
    with Canvas() as canvas:
        _txt("distinción de elementos: ¿hay dos xᵢ iguales?",
             Point(ancho / 2, -36), color=TINTA, size=CUERPO)
        Line(Point(-14, 0), Point(ancho + 14, 0), stroke=APAGADO, width=1.0)
        for x in xs:
            _punto(Point(px(x), 0), TINTA, r=2.8)
        for x in xs:
            Arrow(Point(px(x), 14), Point(px(x), 52), stroke=ACENTO.transparent(0.55),
                  width=0.9, marker_end="arrow")
        _txt("xᵢ ↦ (xᵢ, 0)", Point(ancho + 22, 33), color=ACENTO, size=PIE,
             anchor="start")
        # el plano, con los puntos sobre el eje y = 0
        Rect(ancho + 40, 84, stroke=REGLA, width=1.0).move_to(
            Point(ancho / 2, 108))
        Line(Point(-14, 108), Point(ancho + 14, 108), stroke=APAGADO, width=1.0)
        Line(Point(-8, 74), Point(-8, 142), stroke=REGLA.darker(0.3), width=0.9)
        _txt("y", Point(-16, 78), color=APAGADO, size=PIE)
        for x in xs:
            _punto(Point(px(x), 108), OSCURO, r=2.8)
        # el par repetido, que es lo que la reducción detecta
        rep = [x for x in set(xs) if xs.count(x) > 1]
        if rep:
            Circle(11, stroke=ALARMA, width=1.3).move_to(Point(px(rep[0]), 108))
            _txt("distancia 0", Point(px(rep[0]), 134), color=ALARMA, size=PIE)
        _txt("par más cercano: ¿es 0 la distancia mínima?",
             Point(ancho / 2, 164), color=TINTA, size=CUERPO)
        _txt("la transformación cuesta O(n) y no prueba el signo de ningún polinomio",
             Point(ancho / 2, 180), color=APAGADO, size=PIE)
    return _figura(canvas, ident, pie)


# --------------------------------------------------------------------------
# 9. el árbol de decisión algebraico
# --------------------------------------------------------------------------

def arbol_decision(ident="arbol-decision", pie=""):
    ancho, paso_y = 330.0, 62.0
    nodos = {(0, 0): "x₁ − x₂",
             (1, 0): "x₁ − x₃", (1, 1): "sí", (1, 2): "x₂ − x₃",
             (2, 0): "…", (2, 1): "sí", (2, 2): "…",
             (2, 3): "…", (2, 4): "sí", (2, 5): "…"}
    anchos = {0: 1, 1: 3, 2: 6}
    pos = {k: Point((k[1] + 0.5) * ancho / anchos[k[0]], k[0] * paso_y)
           for k in nodos}
    aristas = [((0, 0), (1, 0), "< 0"), ((0, 0), (1, 1), "= 0"),
               ((0, 0), (1, 2), "> 0")]
    aristas += [((1, 0), (2, i), "") for i in (0, 1, 2)]
    aristas += [((1, 2), (2, i), "") for i in (3, 4, 5)]
    with Canvas() as canvas:
        for a, b, etq in aristas:
            Line(pos[a], pos[b], stroke=REGLA.darker(0.25), width=0.9)
            if etq:
                _txt(etq, Point((pos[a].x + pos[b].x) / 2 - 10,
                                (pos[a].y + pos[b].y) / 2 - 2),
                     color=APAGADO, size=PIE)
        for k, texto in nodos.items():
            hoja = texto == "sí"
            if hoja:
                Rect(30, 19, fill=CALIDO.transparent(0.16), stroke=CALIDO,
                     width=1.0).move_to(pos[k])
            else:
                Rect(46, 22, fill=Colors.White, stroke=OSCURO, width=1.1,
                     ).move_to(pos[k])
            _txt(texto, pos[k], color=CALIDO if hoja else TINTA, size=PIE)
        _txt("cada nodo prueba el signo de un polinomio de la entrada; "
             "la profundidad es el costo en el peor caso",
             Point(ancho / 2, 2.62 * paso_y), color=APAGADO, size=PIE)
    return _figura(canvas, ident, pie)


# --------------------------------------------------------------------------
# 10. la rejilla del algoritmo incremental
# --------------------------------------------------------------------------

def rejilla(ocupadas, lado, nuevo, radio=4, ident="rejilla", pie=""):
    """`ocupadas` es {(cx, cy): (x, y)} tal como lo tiene el algoritmo, `lado` es
    δ/2, y `nuevo` es el punto que se está insertando."""
    paso = 27.0
    cn = (int(nuevo[0] // lado), int(nuevo[1] // lado))
    # la rejilla real es enorme y casi vacía (por eso es una tabla hash y no un
    # arreglo); la figura recorta una ventana alrededor del punto que se inserta
    x0, x1 = cn[0] - radio, cn[0] + radio
    y0, y1 = cn[1] - radio, cn[1] + radio
    ocupadas = {c: p for c, p in ocupadas.items()
                if x0 <= c[0] <= x1 and y0 <= c[1] <= y1}
    px = lambda x, y: Point((x / lado - x0) * paso, (y1 + 1 - y / lado) * paso)
    with Canvas() as canvas:
        for cx in range(x0, x1 + 1):
            for cy in range(y0, y1 + 1):
                Rect(paso, paso, stroke=REGLA.darker(0.12), width=0.7).move_to(
                    px(cx * lado, (cy + 1) * lado), anchor="topleft")
        Rect(5 * paso, 5 * paso, fill=ACENTO.transparent(0.14), stroke=ACENTO,
             width=1.5).move_to(px((cn[0] - 2) * lado, (cn[1] + 3) * lado),
                                anchor="topleft")
        for c, p in ocupadas.items():
            _punto(px(p[0], p[1]), APAGADO, r=2.5)
        cp = px(nuevo[0], nuevo[1])
        Circle(2 * paso, stroke=ALARMA, width=1.2).move_to(cp)
        _punto(cp, ALARMA, r=3.4)
        _txt("p", Point(cp.x - 10, cp.y - 8), color=ALARMA, size=CUERPO)
        Line(cp, Point(cp.x + 2 * paso, cp.y), stroke=ALARMA, width=1.0,
             marker_end="arrow")
        _txt("δ", Point(cp.x + paso, cp.y + 9), color=ALARMA, size=PIE)
        alto = (y1 - y0 + 1) * paso
        _cota_h(0, paso, alto + 16, "δ/2", dy=11)
        _txt("un punto por celda; lo que está a menos de δ de p cae dentro "
             "del bloque de 5×5",
             Point((x1 - x0 + 1) * paso / 2, alto + 38), color=APAGADO, size=PIE)
    return _figura(canvas, ident, pie)


# --------------------------------------------------------------------------
# 11 y 12. las dos gráficas medidas
# --------------------------------------------------------------------------

def grafica_log_log(series, titulo_x, titulo_y, ident="tiempos", pie=""):
    """series: {nombre: [(x, y), ...]} con x, y > 0. Ejes logarítmicos hechos a
    mano, porque el Chart de tesserax fuerza el origen de la y en 0."""
    ancho, alto = 300.0, 180.0
    todos = [p for s in series.values() for p in s]
    x0 = math.floor(min(math.log10(x) for x, _ in todos))
    x1 = math.ceil(max(math.log10(x) for x, _ in todos))
    y0 = math.floor(min(math.log10(y) for _, y in todos))
    y1 = math.ceil(max(math.log10(y) for _, y in todos))
    px = lambda x: (math.log10(x) - x0) / ((x1 - x0) or 1) * ancho
    py = lambda y: alto - (math.log10(y) - y0) / ((y1 - y0) or 1) * alto
    colores = [OSCURO, CALIDO, ACENTO, ALARMA]
    with Canvas() as canvas:
        for e in range(x0, x1 + 1):
            Line(Point(px(10 ** e), 0), Point(px(10 ** e), alto),
                 stroke=REGLA, width=0.7)
            _txt(f"10{sup(e)}", Point(px(10 ** e), alto + 12), color=APAGADO,
                 size=PIE)
        for e in range(y0, y1 + 1):
            Line(Point(0, py(10 ** e)), Point(ancho, py(10 ** e)),
                 stroke=REGLA, width=0.7)
            _txt(f"10{sup(e)}", Point(-8, py(10 ** e)), color=APAGADO, size=PIE,
                 anchor="end")
        for k, (nombre, puntos) in enumerate(series.items()):
            color = colores[k % len(colores)]
            Polyline([Point(px(x), py(y)) for x, y in puntos], stroke=color,
                     width=1.7)
            for x, y in puntos:
                _punto(Point(px(x), py(y)), color, r=2.6)
            _txt(nombre, Point(ancho + 30, 12 + k * 15), color=color, size=PIE,
                 anchor="start")
        _txt(titulo_x, Point(ancho / 2, alto + 30), color=APAGADO, size=PIE)
        _txt(titulo_y, Point(-8, -12), color=APAGADO, size=PIE, anchor="end")
    return _figura(canvas, ident, pie)


def grafica_barras(grupos, series, titulo_y="", ident="reconstrucciones", pie=""):
    """grupos: etiquetas del eje x; series: {nombre: [un valor por grupo]}."""
    ancho, alto = 280.0, 145.0
    tope = max(v for vs in series.values() for v in vs) * 1.18
    colores = [OSCURO, CALIDO]
    ns = len(series)
    paso_g = ancho / len(grupos)
    w = paso_g / (ns + 1.6)
    with Canvas() as canvas:
        for e in range(0, int(tope) + 1, 5):
            Line(Point(0, alto - e / tope * alto),
                 Point(ancho, alto - e / tope * alto), stroke=REGLA, width=0.7)
            _txt(str(e), Point(-8, alto - e / tope * alto), color=APAGADO,
                 size=PIE, anchor="end")
        Line(Point(0, alto), Point(ancho, alto), stroke=APAGADO, width=1.0)
        for g, grupo in enumerate(grupos):
            base = g * paso_g + (paso_g - ns * w) / 2
            for k, (nombre, valores) in enumerate(series.items()):
                v = valores[g]
                h = v / tope * alto
                Rect(w, h, fill=colores[k].transparent(0.22), stroke=colores[k],
                     width=1.0).move_to(Point(base + k * w, alto - h),
                                        anchor="topleft")
                _txt(f"{v:.1f}", Point(base + (k + 0.5) * w, alto - h - 7),
                     color=colores[k], size=PIE)
            _txt(grupo, Point(g * paso_g + paso_g / 2, alto + 12), color=APAGADO,
                 size=PIE)
        for k, nombre in enumerate(series):
            _txt(nombre, Point(ancho + 10, 12 + k * 15), color=colores[k],
                 size=PIE, anchor="start")
        if titulo_y:
            _txt(titulo_y, Point(-8, -12), color=APAGADO, size=PIE, anchor="end")
    return _figura(canvas, ident, pie)


# ==========================================================================
# Conferencia 3: demostrar que un algoritmo es correcto
# ==========================================================================

# --------------------------------------------------------------------------
# 10. la fila de votos de Boyer-Moore
# --------------------------------------------------------------------------

def votos(A, parejas, contadores, candidatos, ident="votos", pie=""):
    """`parejas` son los pares de índices que el algoritmo canceló; `contadores` y
    `candidatos` son el estado después de procesar cada posición. Todo sale de
    correr el algoritmo: la figura no decide qué se cancela con qué."""
    paso, lado = 36.0, 24.0
    emparejado = {i for par in parejas for i in par}
    with Canvas() as canvas:
        for i, x in enumerate(A):
            c = Point(i * paso, 0)
            sobrevive = i not in emparejado
            Rect(lado, lado, fill=ACENTO.transparent(0.16) if sobrevive else Colors.White,
                 stroke=OSCURO if sobrevive else APAGADO,
                 width=1.5 if sobrevive else 0.9).move_to(c)
            _txt(str(x), c, color=TINTA if sobrevive else APAGADO, size=CUERPO)
            _txt(str(i + 1), Point(c.x, -lado / 2 - 34), color=REGLA.darker(0.4),
                 size=PIE)
            _txt(str(candidatos[i]), Point(c.x, lado / 2 + 13), color=APAGADO, size=PIE)
            _txt(str(contadores[i]), Point(c.x, lado / 2 + 27), color=CALIDO, size=PIE)
        for i, j in parejas:
            Line(Point(i * paso, -lado / 2 - 2), Point(j * paso, -lado / 2 - 2),
                 curvature=0.45, stroke=APAGADO, width=1.0)
        izq = -paso / 2 - 6
        _txt("candidato", Point(izq, lado / 2 + 13), color=APAGADO, size=PIE,
             anchor="end")
        _txt("contador", Point(izq, lado / 2 + 27), color=CALIDO, size=PIE,
             anchor="end")
        _txt("posición", Point(izq, -lado / 2 - 34), color=REGLA.darker(0.4),
             size=PIE, anchor="end")
    return _figura(canvas, ident, pie)


# --------------------------------------------------------------------------
# 11. un emparejamiento y la pareja que lo bloquea
# --------------------------------------------------------------------------

def emparejamiento(pref_a, pref_b, M, bloqueo=None, ident="emparejamiento", pie=""):
    """`pref_a[i]` es la lista de a_i (índices de b, de mejor a peor), y al revés
    `pref_b`. `M[i]` es el receptor de a_i. `bloqueo` es un par (i, j) que el
    llamador calculó con el verificador de estabilidad."""
    n = len(pref_a)
    paso_y, xa, xb = 34.0, 0.0, 190.0
    with Canvas() as canvas:
        pos_a = [Point(xa, k * paso_y) for k in range(n)]
        pos_b = [Point(xb, k * paso_y) for k in range(n)]
        for i, j in enumerate(M):
            Line(pos_a[i], pos_b[j], stroke=ACENTO, width=1.6)
        if bloqueo is not None:
            i, j = bloqueo
            Line(pos_a[i], pos_b[j], stroke=ALARMA, width=1.6)
        for k in range(n):
            for p, nombre, lista, lado in ((pos_a[k], f"a{sub(k + 1)}", pref_a[k], -1),
                                           (pos_b[k], f"b{sub(k + 1)}", pref_b[k], 1)):
                marca = bloqueo is not None and k == (bloqueo[0] if lado < 0 else bloqueo[1])
                Circle(9, fill=Colors.White, stroke=ALARMA if marca else TINTA,
                       width=1.4 if marca else 0.9).move_to(p)
                _txt(nombre, p, color=TINTA, size=PIE)
                otro = "b" if lado < 0 else "a"
                texto = " > ".join(f"{otro}{sub(x + 1)}" for x in lista)
                _txt(texto, Point(p.x + lado * 18, p.y), color=APAGADO, size=PIE,
                     anchor="end" if lado < 0 else "start")
        _txt("proponentes y sus listas", Point(xa - 40, -24), color=APAGADO, size=PIE)
        _txt("receptores y sus listas", Point(xb + 40, -24), color=APAGADO, size=PIE)
    return _figura(canvas, ident, pie)


# --------------------------------------------------------------------------
# 12. el primer rechazo por una pareja válida
# --------------------------------------------------------------------------

def primer_rechazo(ident="primer-rechazo", pie=""):
    """Diagrama de la demostración de optimalidad: no ilustra una ejecución, así
    que no recibe estado."""
    W = 170.0
    with Canvas() as canvas:
        for k, titulo in enumerate(["en el emparejamiento estable M′",
                                    "en la ejecución, al primer rechazo"]):
            with Group() as panel:
                a, a2 = Point(0, 0), Point(0, 64)
                b, b2 = Point(110, 0), Point(110, 64)
                if k == 0:
                    Line(a, b, stroke=ACENTO, width=1.6)
                    Line(a2, b2, stroke=ACENTO, width=1.6)
                else:
                    Line(a2, b, stroke=OSCURO, width=1.6)
                    Arrow(Point(98, 6), Point(14, 6), stroke=ALARMA, width=1.1,
                          marker_end="arrow")
                    _txt("rechaza", Point(56, -6), color=ALARMA, size=PIE)
                for p, nombre in ((a, "a"), (a2, "a′"), (b, "b"), (b2, "b′")):
                    Circle(9, fill=Colors.White, stroke=TINTA, width=0.9).move_to(p)
                    _txt(nombre, p, color=TINTA, size=PIE)
                _txt(titulo, Point(55, 96), color=APAGADO, size=PIE)
            panel.translated(k * (W + 24), 0)
        _txt("a′ prefiere b a b′ (todavía no lo ha rechazado ninguna pareja válida) "
             "y b prefiere a′ a a: (a′, b) bloquea M′",
             Point((2 * W + 24) / 2 - 30, 122), color=ALARMA, size=PIE)
    return _figura(canvas, ident, pie)


# ==========================================================================
# Conferencia 4: análisis amortizado
# ==========================================================================

# --------------------------------------------------------------------------
# 13. costo real, costo amortizado y potencial de la cola
# --------------------------------------------------------------------------

def cola_potencial(costos, amortizados, potencial, ident="cola-potencial", pie=""):
    """Tres series de la misma longitud, medidas por el código de la conferencia."""
    ancho, alto_c, alto_p = 360.0, 90.0, 55.0
    k = len(costos)
    paso = ancho / k
    tope_c = max(costos + amortizados)
    tope_p = max(potencial) or 1
    with Canvas() as canvas:
        Line(Point(0, alto_c), Point(ancho, alto_c), stroke=APAGADO, width=0.9)
        for i, c in enumerate(costos):
            h = c / tope_c * alto_c
            Rect(paso * 0.72, h, fill=CALIDO.transparent(0.25), stroke=CALIDO,
                 width=0.6).move_to(Point(i * paso, alto_c - h), anchor="topleft")
        Polyline([Point((i + 0.36) * paso, alto_c - a / tope_c * alto_c)
                  for i, a in enumerate(amortizados)], stroke=OSCURO, width=1.5)
        _txt("costo real", Point(ancho + 8, alto_c - 12), color=CALIDO, size=PIE,
             anchor="start")
        _txt("costo amortizado", Point(ancho + 8, alto_c - 26), color=OSCURO,
             size=PIE, anchor="start")
        base = alto_c + 24 + alto_p
        Line(Point(0, base), Point(ancho, base), stroke=APAGADO, width=0.9)
        Polyline([Point((i + 0.36) * paso, base - p / tope_p * alto_p)
                  for i, p in enumerate(potencial)], stroke=ACENTO, width=1.4)
        _txt("potencial Φ", Point(ancho + 8, base - alto_p / 2), color=ACENTO,
             size=PIE, anchor="start")
        _txt("operación", Point(ancho / 2, base + 12), color=APAGADO, size=PIE)
    return _figura(canvas, ident, pie)


# --------------------------------------------------------------------------
# 14. árboles binarios: un dibujante y sus usos
# --------------------------------------------------------------------------
# Un árbol es None o una tupla (etiqueta, izquierdo, derecho). Una etiqueta que
# empieza con "△" se dibuja como subárbol colgante, un triángulo.

def _dibujar_arbol(arbol, dx=22.0, dy=30.0, resaltar=(), origen=(0.0, 0.0)):
    orden = []

    def recorrer(t, d):
        if t is None:
            return
        recorrer(t[1], d + 1)
        orden.append((t, d))
        recorrer(t[2], d + 1)

    recorrer(arbol, 0)
    pos = {id(t): Point(origen[0] + i * dx, origen[1] + d * dy)
           for i, (t, d) in enumerate(orden)}
    for t, _ in orden:
        for hijo in (t[1], t[2]):
            if hijo is not None:
                Line(pos[id(t)], pos[id(hijo)], stroke=APAGADO, width=0.9)
    for t, _ in orden:
        p, etiqueta = pos[id(t)], str(t[0])
        if etiqueta.startswith("△"):
            Polyline([Point(p.x, p.y - 7), Point(p.x - 8, p.y + 8),
                      Point(p.x + 8, p.y + 8)], closed=True,
                     fill=REGLA.transparent(0.5), stroke=APAGADO, width=0.8)
            _txt(etiqueta[1:], Point(p.x, p.y + 16), color=APAGADO, size=PIE)
        else:
            activo = t[0] in resaltar
            Circle(8.5, fill=ACENTO.transparent(0.18) if activo else Colors.White,
                   stroke=OSCURO if activo else TINTA,
                   width=1.4 if activo else 0.9).move_to(p)
            _txt(etiqueta, p, color=TINTA, size=PIE)
    return len(orden) * dx, max((d for _, d in orden), default=0) * dy


def splay_casos(ident="splay-casos", pie=""):
    """Diagrama de la demostración: los tres pasos del splay, antes y después."""
    A, B, C, D = ("△A", None, None), ("△B", None, None), ("△C", None, None), ("△D", None, None)
    casos = [
        ("zig", ("y", ("x", A, B), C), ("x", A, ("y", B, C))),
        ("zig-zig", ("z", ("y", ("x", A, B), C), D), ("x", A, ("y", B, ("z", C, D)))),
        ("zig-zag", ("z", ("y", A, ("x", B, C)), D), ("x", ("y", A, B), ("z", C, D))),
    ]
    with Canvas() as canvas:
        y = 0.0
        for nombre, antes, despues in casos:
            _txt(nombre, Point(-14, y + 20), color=OSCURO, size=CUERPO, anchor="end")
            ancho, _ = _dibujar_arbol(antes, dy=25.0, resaltar=("x",), origen=(0, y))
            Arrow(Point(ancho + 6, y + 26), Point(ancho + 46, y + 26),
                  stroke=APAGADO, width=1.0, marker_end="arrow")
            _dibujar_arbol(despues, dy=25.0, resaltar=("x",), origen=(ancho + 60, y))
            y += 100
    return _figura(canvas, ident, pie)


def arboles_comparados(paneles, ident="arboles-comparados", pie=""):
    """`paneles` es una lista de (título, árbol); los árboles salen del estado
    real de las estructuras de la conferencia."""
    with Canvas() as canvas:
        x = 0.0
        for titulo, arbol in paneles:
            ancho, alto = _dibujar_arbol(arbol, dx=15.0, dy=19.0, origen=(x, 0))
            _txt(titulo, Point(x + ancho / 2 - 7, -18), color=APAGADO, size=PIE)
            x += ancho + 30
    return _figura(canvas, ident, pie)


# --------------------------------------------------------------------------
# 15. un bosque de union-find antes y después de comprimir
# --------------------------------------------------------------------------

def _dibujar_bosque(padre, nodos, camino=(), dx=24.0, dy=30.0, origen=(0.0, 0.0)):
    hijos = {v: [] for v in nodos}
    raices = []
    for v in nodos:
        (raices if padre[v] == v else hijos[padre[v]]).append(v)
    pos, x = {}, [0.0]

    def colocar(v, d):
        if not hijos[v]:
            pos[v] = Point(origen[0] + x[0], origen[1] + d * dy)
            x[0] += dx
            return
        for h in hijos[v]:
            colocar(h, d + 1)
        pos[v] = Point((pos[hijos[v][0]].x + pos[hijos[v][-1]].x) / 2,
                       origen[1] + d * dy)

    for r in raices:
        colocar(r, 0)
    for v in nodos:
        if padre[v] != v:
            en_camino = v in camino and padre[v] in camino
            Line(pos[v], pos[padre[v]], stroke=CALIDO if en_camino else APAGADO,
                 width=1.5 if en_camino else 0.9)
    for v in nodos:
        activo = v in camino
        Circle(8.5, fill=CALIDO.transparent(0.18) if activo else Colors.White,
               stroke=CALIDO if activo else TINTA, width=1.3 if activo else 0.9).move_to(pos[v])
        _txt(str(v), pos[v], color=TINTA, size=PIE)
    return x[0]


def compresion(antes, despues, nodos, camino, ident="compresion", pie=""):
    """`antes` y `despues` son los arreglos de padres reales, antes y después de
    un find sobre el primer nodo de `camino`."""
    with Canvas() as canvas:
        ancho = _dibujar_bosque(antes, nodos, camino=camino)
        _txt("antes del find", Point(ancho / 2 - 12, -20), color=APAGADO, size=PIE)
        Arrow(Point(ancho + 4, 45), Point(ancho + 40, 45), stroke=APAGADO, width=1.0,
              marker_end="arrow")
        ancho2 = _dibujar_bosque(despues, nodos, camino=camino, origen=(ancho + 56, 0))
        _txt("después: todo el camino cuelga de la raíz",
             Point(ancho + 56 + ancho2 / 2 - 12, -20), color=APAGADO, size=PIE)
    return _figura(canvas, ident, pie)
