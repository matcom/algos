"""Figuras del capítulo 10: matroides.

Cada función recibe el estado que calculó el código del capítulo (qué aristas tomó el
goloso, cuáles el óptimo, qué tareas aceptó) y no decide nada del algoritmo. Las
posiciones de los vértices son solo presentación.
"""

from tesserax import Canvas, Circle, Line, Point, Rect

from figuras import (
    ACENTO, ALARMA, APAGADO, CALIDO, CUERPO, OSCURO, PIE, REGLA, TINTA,
    _figura, _txt,
)


def _grafo(pos, aristas, origen, estilo, etiquetas=None, color_vertice=None, escala=1.0):
    """Dibuja un grafo. `estilo(e)` devuelve (color, ancho) de la arista `e`;
    `etiquetas[e]` es el texto junto a la arista; `color_vertice[v]` su relleno."""
    ox, oy = origen

    def p(v):
        x, y = pos[v]
        return Point(ox + x * escala, oy + y * escala)

    for e in aristas:
        color, ancho = estilo(e)
        a, b = p(e[0]), p(e[1])
        Line(a, b, stroke=color, width=ancho)
        if etiquetas and e in etiquetas:
            mx, my = (a.x + b.x) / 2, (a.y + b.y) / 2
            dx, dy = b.y - a.y, a.x - b.x            # normal a la arista
            largo = (dx * dx + dy * dy) ** 0.5 or 1.0
            _txt(etiquetas[e], Point(mx + 9 * dx / largo, my + 9 * dy / largo),
                 color=color if ancho > 1.5 else APAGADO, size=CUERPO)
    for v in pos:
        relleno = (color_vertice or {}).get(v, "#ffffff")
        Circle(9, fill=relleno, stroke=TINTA, width=0.9).move_to(p(v))
        _txt(str(v), p(v), size=CUERPO)


# --------------------------------------------------------------------------
# 1. el diamante: el goloso contra el óptimo en emparejamientos
# --------------------------------------------------------------------------

def diamante(pos, aristas, pesos, goloso, optimo, ident="matroides-diamante", pie=""):
    """`goloso` y `optimo` son los conjuntos de aristas que calculó el capítulo."""
    sep = 170.0
    with Canvas() as canvas:
        for k, (titulo, elegidas) in enumerate([("goloso", goloso), ("óptimo", optimo)]):
            ox = k * sep
            color = ALARMA if k == 0 else ACENTO
            _grafo(pos, aristas, (ox, 0),
                   lambda e: (color, 3.2) if e in elegidas else (REGLA.darker(0.15), 1.0),
                   etiquetas={e: str(pesos[e]) for e in aristas})
            total = sum(pesos[e] for e in elegidas)
            _txt(f"{titulo}: peso {total}", Point(ox + 50, 128), color=color, size=CUERPO)
    return _figura(canvas, ident, pie)


# --------------------------------------------------------------------------
# 2. el intercambio entre dos bosques
# --------------------------------------------------------------------------

def intercambio(pos, aristas, A, B, componente, sirven, ident="matroides-intercambio",
                pie=""):
    """`componente[v]` es el número de la componente de `v` en el bosque `A`;
    `sirven` son las aristas de `B` que se pueden agregar a `A`."""
    tonos = ["#cffafe", "#fde68a", "#e9d5ff", "#fecdd3"]
    relleno = {v: tonos[componente[v] % len(tonos)] for v in pos}
    sep = 230.0
    with Canvas() as canvas:
        def estilo_a(e):
            return (ACENTO, 3.0) if e in A else (REGLA.darker(0.1), 0.8)

        def estilo_b(e):
            if e in sirven:
                return (ALARMA, 3.4)
            if e in B and e in A:
                return (OSCURO, 3.0)
            if e in B:
                return (CALIDO, 3.0)
            return (REGLA.darker(0.1), 0.8)

        _grafo(pos, aristas, (0, 0), estilo_a, color_vertice=relleno)
        _grafo(pos, aristas, (sep, 0), estilo_b, color_vertice=relleno)
        _txt(f"A: {len(A)} aristas, {len(set(componente.values()))} componentes",
             Point(80, 122), color=ACENTO, size=CUERPO)
        _txt(f"B: {len(B)} aristas", Point(sep + 80, 122), color=CALIDO, size=CUERPO)
        _txt("en rojo, la única de B − A que une dos componentes de A",
             Point(sep + 80, 136), color=ALARMA, size=PIE)
    return _figura(canvas, ident, pie)


# --------------------------------------------------------------------------
# 3. tareas unitarias: el horario del goloso
# --------------------------------------------------------------------------

def horario(d, w, orden, rechazadas, ident="matroides-horario", pie=""):
    """`orden` son las tareas aceptadas (índices) en el orden en que se atienden;
    `rechazadas` las que el goloso descartó."""
    lado, alto = 84.0, 50.0
    with Canvas() as canvas:
        for s in range(len(orden)):
            x = s * lado
            Rect(lado, alto, fill="#ffffff", stroke=REGLA.darker(0.3),
                 width=0.7).move_to(Point(x + lado / 2, 0))
            _txt(f"{s} a {s + 1}", Point(x + lado / 2, alto / 2 + 10), color=APAGADO,
                 size=PIE)
        for s, i in enumerate(orden):
            x = s * lado
            Rect(lado - 6, alto - 6, fill=ACENTO.transparent(0.12), stroke=OSCURO,
                 width=1.0).move_to(Point(x + lado / 2, 0))
            _txt(f"tarea {i + 1}", Point(x + lado / 2, -7), size=CUERPO)
            _txt(f"d={d[i]}  w={w[i]}", Point(x + lado / 2, 9), color=APAGADO, size=CUERPO)
        x0 = (len(orden) + 0.3) * lado
        Line(Point(len(orden) * lado, -alto / 2 - 8), Point(len(orden) * lado, alto / 2 + 16),
             stroke=TINTA, width=1.2)
        for k, i in enumerate(rechazadas):
            x = x0 + k * lado
            Rect(lado - 6, alto - 6, fill=ALARMA.transparent(0.10), stroke=ALARMA,
                 width=1.0).move_to(Point(x + lado / 2, 0))
            _txt(f"tarea {i + 1}", Point(x + lado / 2, -7), color=ALARMA, size=CUERPO)
            _txt(f"d={d[i]}  w={w[i]}", Point(x + lado / 2, 9), color=ALARMA, size=CUERPO)
        _txt("a tiempo, por plazo", Point(len(orden) * lado / 2, -alto / 2 - 12),
             color=OSCURO, size=PIE)
        _txt(f"rechazadas: penalización {sum(w[i] for i in rechazadas)}",
             Point(x0 + len(rechazadas) * lado / 2, -alto / 2 - 12), color=ALARMA, size=PIE)
    return _figura(canvas, ident, pie)
