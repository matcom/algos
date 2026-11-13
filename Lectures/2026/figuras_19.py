"""Figuras del capítulo 19: reducciones a secuencias y números.

Cada figura recibe lo que calculó el código del capítulo: el grafo que construyó
`a_hamiltoniano` con el ciclo que encontró la búsqueda, la tabla de dígitos que
construyó `a_suma` con el subconjunto elegido, y la lista de reducciones demostradas.
"""

from tesserax import Arrow, Canvas, Colors, Line, Point, Polyline, Rect

from figuras import (
    ACENTO, APAGADO, CALIDO, CUERPO, OSCURO, PIE, REGLA, TINTA,
    _figura, _punto, _txt, sub,
)


def _literal(l):
    return ("¬" if l < 0 else "") + "x" + sub(abs(l))


# --- 1. las filas del ciclo hamiltoniano ------------------------------------------

def filas(n, clausulas, arcos, ciclo, valor, ident="rn-filas", pie=""):
    """`arcos`: los que construyó `a_hamiltoniano`. `ciclo`: la lista de vértices del
    ciclo que encontró la búsqueda, empezando en "s". `valor`: la asignación que se lee
    del ciclo (fila i de izquierda a derecha si y solo si x_i es verdadera). Cada
    vértice de cláusula se dibuja debajo de la fila desde la que el ciclo se desvía."""
    k = len(clausulas)
    b = 3 * k + 3
    dx, dy = 30.0, 66.0
    fila_desvio = {x[1]: ciclo[r - 1][1] for r, x in enumerate(ciclo) if x[0] == "c"}

    def pos(v):
        if v == "s":
            return Point(-30, dy)
        if v == "t":
            return Point(-30, dy * n)
        if v[0] == "c":
            j = v[1]
            return Point((3 * j + 0.5) * dx, dy * fila_desvio[j] + 30)
        _, i, p = v
        return Point(p * dx, dy * i)

    pasos = [(ciclo[r], ciclo[(r + 1) % len(ciclo)]) for r in range(len(ciclo))]
    en_ciclo = set(pasos)
    with Canvas() as canvas:
        vistos = set()
        for u, w in arcos:
            par = frozenset((u, w))
            if (u, w) in en_ciclo or (w, u) in en_ciclo or par in vistos or par == {"s", "t"}:
                continue
            vistos.add(par)
            Line(pos(u), pos(w), stroke=REGLA, width=0.8)
        for u, w in pasos:
            p, q = pos(u), pos(w)
            if u == "t" and w == "s":
                Polyline([Point(p.x - 8, p.y), Point(-58, p.y), Point(-58, q.y),
                          Point(q.x - 8, q.y)], stroke=OSCURO, width=1.6)
                continue
            clausula = any(isinstance(x, tuple) and x[0] == "c" for x in (u, w))
            Line(p, q, stroke=CALIDO if clausula else OSCURO, width=1.8)
        for i in range(1, n + 1):
            for p in range(1, b + 1):
                hueco = p % 3 == 2
                _punto(pos(("v", i, p)), APAGADO if hueco else TINTA, r=2.8)
            sentido = "de izquierda a derecha" if valor[i] else "de derecha a izquierda"
            _txt(f"x{sub(i)} = {'V' if valor[i] else 'F'}: {sentido}",
                 Point(b * dx + 16, dy * i), color=OSCURO, size=CUERPO, anchor="start")
        for j, c in enumerate(clausulas, 1):
            q = pos(("c", j))
            Rect(20, 16, fill=Colors.White, stroke=CALIDO, width=1.0).move_to(q)
            _txt(f"c{sub(j)}", q, color=CALIDO, size=CUERPO)
            _txt("(" + " ∨ ".join(_literal(l) for l in c) + ")",
                 Point(q.x, q.y + 17), color=APAGADO, size=PIE)
        for v in ("s", "t"):
            Rect(18, 16, fill=Colors.White, stroke=TINTA, width=1.0).move_to(pos(v))
            _txt(v, pos(v), color=TINTA, size=CUERPO)
        for p in range(1, b + 1):
            _txt(str(p), Point(p * dx, dy - 14), color=APAGADO, size=PIE)
    return _figura(canvas, ident, pie)


# --- 2. la tabla de suma de subconjuntos ------------------------------------------

def tabla(n, k, filas_tabla, meta, elegidas, ident="rn-tabla", pie=""):
    """`filas_tabla`: lista de (nombre, dígitos) tal como la armó `a_suma`, con los
    dígitos en el orden x_1..x_n, C_1..C_k. `meta`: los dígitos de T. `elegidas`: los
    nombres del subconjunto que suma T, calculado por el código."""
    cols = [f"x{sub(i)}" for i in range(1, n + 1)] + [f"C{sub(j)}" for j in range(1, k + 1)]
    dx, dy = 36.0, 20.0
    x0 = 56.0
    with Canvas() as canvas:
        for c, nombre in enumerate(cols):
            _txt(nombre, Point(x0 + c * dx, 0), color=APAGADO, size=CUERPO)
        Line(Point(x0 - dx, 8), Point(x0 + (len(cols) - 0.5) * dx + 80, 8),
             stroke=REGLA, width=0.8)
        Line(Point(x0 + (n - 0.5) * dx, -6), Point(x0 + (n - 0.5) * dx,
             dy * (len(filas_tabla) + 2) + 4), stroke=REGLA, width=0.8)
        for r, (nombre, digs) in enumerate(filas_tabla):
            y = dy * (r + 1) + 4
            sel = nombre in elegidas
            if sel:
                Rect((len(cols) + 1) * dx + 70, dy - 2, fill=ACENTO.transparent(0.14),
                     stroke=ACENTO.transparent(0.0), width=0).move_to(Point(x0 + (len(cols) - 2) * dx / 2 + 40, y))
            color = TINTA if sel else APAGADO
            _txt(nombre, Point(x0 - dx, y), color=color, size=CUERPO)
            for c, d in enumerate(digs):
                _txt(str(d) if d else "·", Point(x0 + c * dx, y), color=color, size=CUERPO)
            _txt("".join(map(str, digs)).lstrip("0") or "0",
                 Point(x0 + len(cols) * dx + 6, y), color=color, size=CUERPO, anchor="start")
        y = dy * (len(filas_tabla) + 1) + 10
        Line(Point(x0 - dx, y - 8), Point(x0 + (len(cols) - 0.5) * dx + 80, y - 8),
             stroke=TINTA, width=0.8)
        _txt("T", Point(x0 - dx, y), color=OSCURO, size=CUERPO)
        for c, d in enumerate(meta):
            _txt(str(d), Point(x0 + c * dx, y), color=OSCURO, size=CUERPO)
        _txt("".join(map(str, meta)), Point(x0 + len(cols) * dx + 6, y), color=OSCURO,
             size=CUERPO, anchor="start")
    return _figura(canvas, ident, pie)


# --- 3. el mapa de reducciones de la Parte III ------------------------------------

def mapa(reducciones, ident="rn-mapa", pie=""):
    """`reducciones`: lista de (desde, hacia, capítulo), la misma que imprime el
    código de la §12."""
    cajas = {
        "SAT": (0, 120), "3-SAT": (110, 120),
        "independiente": (260, 0), "clique": (420, -30), "vertex cover": (420, 30),
        "set cover": (570, 30), "3-coloración": (260, 70),
        "ciclo ham. dirigido": (260, 150), "ciclo ham. no dirigido": (420, 150),
        "TSP": (570, 150),
        "suma de subconjuntos": (260, 230), "mochila": (420, 230),
    }
    ancho = {k: 12 + 5.6 * len(k) for k in cajas}
    nuevos = {v for _, v, c in reducciones if c == 19}
    with Canvas() as canvas:
        for u, v, cap in reducciones:
            (x1, y1), (x2, y2) = cajas[u], cajas[v]
            p = Point(x1 + ancho[u] / 2, y1)
            q = Point(x2 - ancho[v] / 2 - 2, y2)
            color = CALIDO if cap == 19 else APAGADO
            Arrow(p, q, stroke=color, width=1.1)
            _txt(str(cap), Point((p.x + q.x) / 2, (p.y + q.y) / 2 - 8), color=color,
                 size=CUERPO)
        for nombre, (x, y) in cajas.items():
            nuevo = nombre in nuevos
            Rect(ancho[nombre], 20, fill=CALIDO.transparent(0.10) if nuevo else Colors.White,
                 stroke=CALIDO if nuevo else TINTA, width=0.9).move_to(Point(x, y))
            _txt(nombre, Point(x, y), color=TINTA, size=CUERPO)
    return _figura(canvas, ident, pie)
