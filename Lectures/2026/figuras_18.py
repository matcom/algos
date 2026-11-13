"""Figuras del capítulo 18: reducciones desde 3-SAT a grafos.

Las tres primeras reciben el estado que calculó el código del capítulo: el grafo y el
independiente que encontró la búsqueda, los coloreos que encontró la enumeración del
gadget, y el coloreo que devolvió el decisor de 3-coloración. La cuarta es el mapa de
las reducciones demostradas: no ilustra la ejecución de ningún algoritmo.
"""

from tesserax import Arrow, Canvas, Colors, Line, Point, Rect

from figuras import (
    ACENTO, ALARMA, APAGADO, CALIDO, CUERPO, OSCURO, PIE, REGLA, TINTA,
    _figura, _punto, _txt,
)

# Colores de 3-coloración: T (verdadero), F (falso), B (base).
_RELLENO = {"T": ACENTO, "F": CALIDO, "B": REGLA}
_LETRA = {"T": Colors.White, "F": Colors.White, "B": TINTA}


def _literal(l):
    return ("¬" if l < 0 else "") + "x" + "₀₁₂₃₄₅₆₇₈₉"[abs(l)]


def _nodo(p, texto, relleno=Colors.White, letra=TINTA, r=10.0, borde=TINTA, size=CUERPO):
    _punto(p, borde, r=r + 1.0)
    _punto(p, relleno, r=r)
    _txt(texto, p, color=letra, size=size)


# --- 1. el grafo de conjunto independiente ------------------------------------------

def independiente(formula, S, ident="red-independiente", pie=""):
    """`formula`: lista de cláusulas de tres enteros (x_i es i, ¬x_i es -i). `S`: el
    conjunto independiente que encontró el código, como pares (cláusula, posición)."""
    S = set(S)
    paso, lado = 190.0, 70.0
    pos = {}
    for j, c in enumerate(formula):
        cx = j * paso
        esquinas = [Point(cx, 0), Point(cx - lado / 2, lado * 0.87), Point(cx + lado / 2, lado * 0.87)]
        for i in range(3):
            pos[(j, i)] = esquinas[i]
    with Canvas() as canvas:
        # aristas de conflicto: curvas, por debajo de los triángulos
        for (j, i), p in pos.items():
            for (k, h), q in pos.items():
                if (j, i) < (k, h) and j != k and formula[j][i] == -formula[k][h]:
                    curva = 0.35 if k - j > 1 else 0.18
                    Line(p, q, curvature=curva, stroke=CALIDO, width=1.3)
                    # canvas.fit no mide la flecha del arco (curva · distancia / 2,
                    # hacia arriba): un punto blanco en su cima la deja dentro.
                    flecha = curva * ((q.x - p.x) ** 2 + (q.y - p.y) ** 2) ** 0.5 / 2
                    _punto(Point((p.x + q.x) / 2, (p.y + q.y) / 2 - flecha - 2),
                           Colors.White, r=0.5)
        for j in range(len(formula)):
            for a, b in [(0, 1), (1, 2), (0, 2)]:
                Line(pos[(j, a)], pos[(j, b)], stroke=TINTA, width=1.0)
        for (j, i), p in pos.items():
            dentro = (j, i) in S
            _nodo(p, _literal(formula[j][i]), relleno=ACENTO if dentro else Colors.White,
                  letra=Colors.White if dentro else TINTA, r=13.0)
        for j, c in enumerate(formula):
            texto = "(" + " ∨ ".join(_literal(l) for l in c) + ")"
            _txt(texto, Point(j * paso, lado * 0.87 + 32), color=APAGADO, size=CUERPO)
    return _figura(canvas, ident, pie)


# --- 2. el gadget de cláusula y sus 8 casos -----------------------------------------

# Posiciones de dibujo del gadget, con las entradas a la izquierda y la paleta a la
# derecha. Las aristas son las del capítulo.
_POS = {
    "a": (0, 0), "b": (0, 44), "c": (0, 100),
    "p1": (50, 0), "q1": (50, 44), "r1": (88, 22),
    "p2": (128, 22), "q2": (128, 100), "r2": (170, 61),
    "F": (215, 38), "B": (215, 84),
}
_NOMBRE = {"a": "a", "b": "b", "c": "c", "p1": "p₁", "q1": "q₁", "r1": "r₁",
           "p2": "p₂", "q2": "q₂", "r2": "r₂", "F": "F", "B": "B"}


def _gadget(aristas, ox, oy, colores, r=9.0, nombres=False):
    P = {v: Point(ox + x, oy + y) for v, (x, y) in _POS.items()}
    for u, v in aristas:
        Line(P[u], P[v], stroke=TINTA, width=0.9)
    for v, p in P.items():
        if nombres:
            _nodo(p, _NOMBRE[v], r=r)
        else:
            k = colores[v]
            _nodo(p, k, relleno=_RELLENO[k], letra=_LETRA[k], r=r)


def gadget_casos(aristas, casos, ident="red-gadget-casos", pie=""):
    """`aristas`: las del gadget, como las define el capítulo. `casos`: lista de 8 pares ((a, b, c), coloreo), con a, b, c en {"T", "F"} y
    coloreo un dict de vértice a "T", "F" o "B", o None si la enumeración no
    encontró ninguno."""
    ancho, alto = 270.0, 150.0
    with Canvas() as canvas:
        _gadget(aristas, ancho / 2 + 10, 0, None, nombres=True)
        _txt("el gadget, con los nombres de sus vértices", Point(ancho / 2 + 117, 128),
             color=APAGADO, size=CUERPO)
        for i, ((a, b, c), col) in enumerate(casos):
            ox = (i % 2) * ancho
            oy = 160 + (i // 2) * alto
            titulo = f"a, b, c = {a}, {b}, {c}"
            if col is None:
                fijo = {"a": a, "b": b, "c": c, "F": "F", "B": "B"}
                P = {v: Point(ox + x, oy + y) for v, (x, y) in _POS.items()}
                for u, v in aristas:
                    Line(P[u], P[v], stroke=REGLA, width=0.9)
                for v, p in P.items():
                    if v in fijo:
                        k = fijo[v]
                        _nodo(p, k, relleno=_RELLENO[k], letra=_LETRA[k], r=9.0)
                    else:
                        _nodo(p, "", r=9.0, borde=ALARMA)
                _txt(titulo + ": ningún coloreo", Point(ox + 107, oy + 125),
                     color=ALARMA, size=CUERPO)
            else:
                _gadget(aristas, ox, oy, col)
                _txt(titulo, Point(ox + 107, oy + 125), color=TINTA, size=CUERPO)
    return _figura(canvas, ident, pie)


# --- 3. la instancia completa -------------------------------------------------------

def instancia(n, formula, aristas, coloreo, ident="red-instancia", pie=""):
    """`aristas`: las que construyó `a_coloracion` del capítulo. `coloreo`: dict de vértice a "T", "F" o "B", con los vértices que construye
    `a_coloracion` del capítulo: "T", "F", "B", los literales como enteros, y los del
    gadget de la cláusula j como pares (j, nombre)."""
    m = len(formula)
    sep = 62.0
    xs = {}
    for i in range(1, n + 1):
        xs[i] = (2 * i - 2) * sep
        xs[-i] = (2 * i - 1) * sep
    centro = (2 * n - 1) * sep / 2
    P = {"B": Point(centro, 0), "T": Point(centro - 180, -10), "F": Point(centro + 180, -10)}
    for l, x in xs.items():
        P[l] = Point(x, 80)
    ancho_g = 2 * n * sep / m
    for j in range(m):
        ox = j * ancho_g + ancho_g / 2 - 80
        local = {"p1": (0, 170), "q1": (40, 170), "r1": (20, 205),
                 "p2": (60, 230), "q2": (100, 205), "r2": (90, 265)}
        for v, (x, y) in local.items():
            P[(j, v)] = Point(ox + x, y)
    with Canvas() as canvas:
        for u, v in aristas:
            lejana = isinstance(u, tuple) and u[1] == "r2" and v in ("F", "B")
            curva = (0.25 if v == "F" else -0.2) if lejana else 0.0
            Line(P[u], P[v], curvature=curva,
                 stroke=APAGADO if lejana else TINTA, width=0.7 if lejana else 0.9)
        for v, p in P.items():
            k = coloreo[v]
            if isinstance(v, int):
                texto = _literal(v)
            elif isinstance(v, tuple):
                texto = _NOMBRE[v[1]]
            else:
                texto = v
            _nodo(p, texto, relleno=_RELLENO[k], letra=_LETRA[k], r=12.0, size=PIE + 0.5)
        for j, c in enumerate(formula):
            ox = j * ancho_g + ancho_g / 2 - 80
            _txt("(" + " ∨ ".join(_literal(l) for l in c) + ")", Point(ox + 50, 295),
                 color=APAGADO, size=CUERPO)
    return _figura(canvas, ident, pie)


# --- 4. el mapa de reducciones ------------------------------------------------------

def mapa(ident="red-mapa", pie=""):
    """Las reducciones demostradas hasta este capítulo, con el capítulo de cada una."""
    cajas = {
        "SAT": (0, 60), "3-SAT": (120, 60),
        "independiente": (260, 0), "clique": (410, -30), "vertex cover": (410, 30),
        "set cover": (560, 30), "3-coloración": (260, 120),
        "ciclo hamiltoniano": (410, 100), "suma de subconjuntos": (410, 160),
    }
    ancho = {k: 8 + 6.2 * len(k) for k in cajas}
    flechas = [("SAT", "3-SAT", "17", True), ("3-SAT", "independiente", "18", True),
               ("independiente", "clique", "16", True),
               ("independiente", "vertex cover", "16", True),
               ("vertex cover", "set cover", "18", True),
               ("3-SAT", "3-coloración", "18", True),
               ("3-SAT", "ciclo hamiltoniano", "19", False),
               ("3-SAT", "suma de subconjuntos", "19", False)]
    with Canvas() as canvas:
        for u, v, cap, hecha in flechas:
            (x1, y1), (x2, y2) = cajas[u], cajas[v]
            p = Point(x1 + ancho[u] / 2, y1)
            q = Point(x2 - ancho[v] / 2 - 2, y2)
            color = OSCURO if hecha else APAGADO
            Arrow(p, q, stroke=color, width=1.1 if hecha else 0.7)
            _txt(cap, Point((p.x + q.x) / 2, (p.y + q.y) / 2 - 7), color=color, size=PIE)
        for k, (x, y) in cajas.items():
            gris = k in ("ciclo hamiltoniano", "suma de subconjuntos")
            Rect(ancho[k], 20, fill=Colors.White, stroke=APAGADO if gris else TINTA,
                 width=0.9).move_to(Point(x, y))
            _txt(k, Point(x, y), color=APAGADO if gris else TINTA, size=CUERPO)
    return _figura(canvas, ident, pie)
