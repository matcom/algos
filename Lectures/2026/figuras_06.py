"""Figuras del capítulo 6: divide y vencerás y recurrencias.

Cada función recibe el estado que calculó el código del capítulo y devuelve una
cadena `<figure>` para imprimir desde un bloque `echo=false output=asis`.
"""

import math

from tesserax import Canvas, Circle, Colors, Line, Point, Polyline, Rect

from figuras import (
    ACENTO, ALARMA, APAGADO, CALIDO, OSCURO, PIE, REGLA, TINTA,
    _figura, _punto, _txt, sup,
)
def _punteada(p, q, color=APAGADO, width=0.9, paso=4.0):
    """Línea de trazos hecha de segmentos: tesserax no tiene dasharray."""
    largo = math.hypot(q.x - p.x, q.y - p.y)
    k = max(1, int(largo / (2 * paso)))
    for i in range(k):
        t0, t1 = (2 * i) / (2 * k), (2 * i + 1) / (2 * k)
        Line(Point(p.x + (q.x - p.x) * t0, p.y + (q.y - p.y) * t0),
             Point(p.x + (q.x - p.x) * t1, p.y + (q.y - p.y) * t1),
             stroke=color, width=width)


# --------------------------------------------------------------------------
# el árbol de recursión de Karatsuba, con el trabajo por nivel
# --------------------------------------------------------------------------

def arbol_karatsuba(niveles, ident="arbol-karatsuba", pie=""):
    """`niveles[i]` es la lista de tamaños de las llamadas de profundidad i, en el
    orden en que se hicieron, tal como los registró la corrida. Arriba, los tres
    primeros niveles como árbol; abajo, una barra por nivel con la suma de tamaños."""
    ancho = 300.0
    with Canvas() as canvas:
        # el árbol: niveles 0, 1 y 2 (1, 3 y 9 cajas)
        centros = {}
        for d in range(min(3, len(niveles))):
            k = len(niveles[d])
            w = min(ancho / k - 4, 60)
            for i, tam in enumerate(niveles[d]):
                c = Point((i + 0.5) * ancho / k, d * 40)
                centros[(d, i)] = c
                if d:
                    Line(centros[(d - 1, i // 3)], c, stroke=REGLA.darker(0.25),
                         width=0.9)
            for i, tam in enumerate(niveles[d]):
                c = centros[(d, i)]
                raro = d and tam > niveles[0][0] / 2 ** d
                Rect(w, 15, fill=(CALIDO if raro else ACENTO).transparent(0.15),
                     stroke=CALIDO if raro else OSCURO, width=0.9).move_to(c)
                _txt(str(tam), c, color=TINTA, size=PIE)
        # las barras: una por nivel
        y0 = 3 * 40 + 6
        tope = max(sum(v) for v in niveles)
        _txt("nivel", Point(-6, y0 - 4), color=APAGADO, size=PIE, anchor="end")
        _txt("llamadas", Point(30, y0 - 4), color=APAGADO, size=PIE, anchor="end")
        _txt("suma de tamaños (el trabajo de partir y combinar)",
             Point(40, y0 - 4), color=APAGADO, size=PIE, anchor="start")
        for d, tams in enumerate(niveles):
            y = y0 + 10 + d * 15
            largo = sum(tams) / tope * (ancho - 70)
            _txt(str(d), Point(-6, y), color=APAGADO, size=PIE, anchor="end")
            _txt(str(len(tams)), Point(30, y), color=TINTA, size=PIE, anchor="end")
            Rect(max(largo, 0.5), 10, fill=ACENTO.transparent(0.25), stroke=OSCURO,
                 width=0.8).move_to(Point(40, y), anchor="left")
            texto = str(sum(tams))
            if d:
                texto += f"  (× {sum(tams) / sum(niveles[d - 1]):.2f})"
            _txt(texto, Point(44 + largo, y), color=TINTA, size=PIE, anchor="start")
    return _figura(canvas, ident, pie)


# --------------------------------------------------------------------------
# los grupos de 5 y lo que la mediana de medianas deja de cada lado
# --------------------------------------------------------------------------

def grupos_medianas(grupos, x, ident="grupos", pie=""):
    """`grupos` son los grupos tal como los formó el algoritmo y `x` el pivote que
    devolvió. La figura solo ordena para dibujar: cada columna de abajo hacia
    arriba, y las columnas por su mediana. Las medianas quedan en una fila."""
    columnas = []
    for G in grupos:
        G = sorted(G)
        columnas.append((G[(len(G) - 1) // 2], G))
    columnas.sort(key=lambda c: c[0])
    jx = [m for m, _ in columnas].index(x)
    # las etiquetas van a 11 pt y los números a 10,5: en la página la figura se ve
    # a su tamaño natural, y a 7,5 pt los números de los círculos no se leían
    grande, numero = 11.0, 10.5
    paso_x, paso_y, r = 36.0, 27.0, 12.0
    arriba = abajo = 0
    with Canvas() as canvas:
        for j, (m, G) in enumerate(columnas):
            im = (len(G) - 1) // 2
            for i, v in enumerate(G):
                p = Point(j * paso_x, -(i - im) * paso_y)
                seguro_mayor = j >= jx and i >= im
                seguro_menor = j <= jx and i <= im
                arriba += seguro_mayor and v != x     # x va en rojo, aparte
                abajo += seguro_menor and v != x
                if v == x:
                    relleno, borde, ancho_b = ALARMA.transparent(0.2), ALARMA, 1.8
                elif seguro_mayor:
                    relleno, borde, ancho_b = ACENTO.transparent(0.22), OSCURO, 1.2
                elif seguro_menor:
                    relleno, borde, ancho_b = CALIDO.transparent(0.2), CALIDO, 1.2
                else:
                    relleno, borde, ancho_b = Colors.White, APAGADO, 0.9
                Circle(r, fill=relleno, stroke=borde, width=ancho_b).move_to(p)
                _txt(str(v), p, color=TINTA, size=numero)
        x_der = (len(columnas) - 1) * paso_x
        _txt(f"medianas (en rojo, x = {x})", Point(x_der + 22, 0), color=APAGADO,
             size=grande, anchor="start")
        _txt(f"azul: {arriba} que seguro son ≥ x",
             Point(x_der + 22, -2.6 * paso_y), color=OSCURO, size=grande,
             anchor="start")
        _txt(f"naranja: {abajo} que seguro son ≤ x",
             Point(x_der + 22, 2.6 * paso_y), color=CALIDO, size=grande,
             anchor="start")
    return _figura(canvas, ident, pie)


# --------------------------------------------------------------------------
# tiempos en ejes logarítmicos con una marca vertical
# --------------------------------------------------------------------------

def grafica_log_log_marca(series, titulo_x, titulo_y, marca=None,
                          ident="tiempos", pie=""):
    """Como grafica_log_log, más una línea vertical de trazos en `marca`
    = (x, texto), que es el cruce que calculó el documento."""
    ancho, alto = 300.0, 180.0
    todos = [p for s in series.values() for p in s]
    x0 = math.floor(math.log2(min(x for x, _ in todos)))
    x1 = math.ceil(math.log2(max(x for x, _ in todos)))
    y0 = math.floor(min(math.log10(y) for _, y in todos))
    y1 = math.ceil(max(math.log10(y) for _, y in todos))
    px = lambda x: (math.log2(x) - x0) / ((x1 - x0) or 1) * ancho
    py = lambda y: alto - (math.log10(y) - y0) / ((y1 - y0) or 1) * alto
    colores = [CALIDO, APAGADO, OSCURO, ALARMA]
    with Canvas() as canvas:
        for e in range(x0, x1 + 1):
            Line(Point(px(2 ** e), 0), Point(px(2 ** e), alto), stroke=REGLA,
                 width=0.7)
            _txt(str(2 ** e), Point(px(2 ** e), alto + 12), color=APAGADO, size=PIE)
        for e in range(y0, y1 + 1):
            Line(Point(0, py(10 ** e)), Point(ancho, py(10 ** e)), stroke=REGLA,
                 width=0.7)
            _txt(f"10{sup(e)}", Point(-8, py(10 ** e)), color=APAGADO, size=PIE,
                 anchor="end")
        if marca:
            _punteada(Point(px(marca[0]), 0), Point(px(marca[0]), alto),
                      color=ALARMA, width=1.0)
            _txt(marca[1], Point(px(marca[0]) - 4, 10), color=ALARMA, size=PIE,
                 anchor="end")
        for k, (nombre, puntos) in enumerate(series.items()):
            color = colores[k % len(colores)]
            Polyline([Point(px(x), py(y)) for x, y in puntos], stroke=color,
                     width=1.7)
            for x, y in puntos:
                _punto(Point(px(x), py(y)), color, r=2.4)
            _txt(nombre, Point(ancho + 14, 12 + k * 15), color=color, size=PIE,
                 anchor="start")
        _txt(titulo_x, Point(ancho / 2, alto + 30), color=APAGADO, size=PIE)
        _txt(titulo_y, Point(-8, -12), color=APAGADO, size=PIE, anchor="end")
    return _figura(canvas, ident, pie)


# --------------------------------------------------------------------------
# una gráfica con x logarítmica e y lineal
# --------------------------------------------------------------------------

def grafica_log_lineal(series, titulo_x, titulo_y, ident="curvas", pie=""):
    """series: {nombre: [(x, y), ...]}, x > 0 en escala log10, y lineal desde 0."""
    ancho, alto = 300.0, 170.0
    todos = [p for s in series.values() for p in s]
    x0 = math.floor(math.log10(min(x for x, _ in todos)))
    x1 = math.ceil(math.log10(max(x for x, _ in todos)))
    tope = max(y for _, y in todos)
    paso = 5 if tope <= 30 else 10
    y1 = paso * math.ceil(tope / paso)
    px = lambda x: (math.log10(x) - x0) / ((x1 - x0) or 1) * ancho
    py = lambda y: alto - y / y1 * alto
    colores = [ALARMA, OSCURO, CALIDO]
    with Canvas() as canvas:
        for e in range(x0, x1 + 1):
            Line(Point(px(10 ** e), 0), Point(px(10 ** e), alto), stroke=REGLA,
                 width=0.7)
            _txt(f"10{sup(e)}", Point(px(10 ** e), alto + 12), color=APAGADO,
                 size=PIE)
        for v in range(0, int(y1) + 1, paso):
            Line(Point(0, py(v)), Point(ancho, py(v)), stroke=REGLA, width=0.7)
            _txt(str(v), Point(-8, py(v)), color=APAGADO, size=PIE, anchor="end")
        for k, (nombre, puntos) in enumerate(series.items()):
            color = colores[k % len(colores)]
            Polyline([Point(px(x), py(y)) for x, y in puntos], stroke=color,
                     width=1.7)
            for x, y in puntos:
                _punto(Point(px(x), py(y)), color, r=2.2)
            ultimo = puntos[-1]
            _txt(nombre, Point(ancho + 8, py(ultimo[1])), color=color, size=PIE,
                 anchor="start")
        _txt(titulo_x, Point(ancho / 2, alto + 30), color=APAGADO, size=PIE)
        _txt(titulo_y, Point(-8, -12), color=APAGADO, size=PIE, anchor="end")
    return _figura(canvas, ident, pie)


# --------------------------------------------------------------------------
# el trabajo por nivel de varios algoritmos, uno al lado del otro
# --------------------------------------------------------------------------

def perfiles_nivel(perfiles, ident="perfiles", pie=""):
    """perfiles: {nombre: [trabajo del nivel 0, del 1, ...]}. Cada panel
    normaliza por el nivel 0, así que la barra del nivel 0 mide 1."""
    alto, ancho_panel, sep = 110.0, 120.0, 26.0
    colores = [OSCURO, APAGADO, CALIDO]
    with Canvas() as canvas:
        for k, (nombre, valores) in enumerate(perfiles.items()):
            ox = k * (ancho_panel + sep)
            color = colores[k % len(colores)]
            tope = max(1.25, max(v / valores[0] for v in valores) * 1.1)
            w = ancho_panel / len(valores)
            Line(Point(ox, alto), Point(ox + ancho_panel, alto), stroke=APAGADO,
                 width=0.9)
            uno = alto - alto / tope
            for i, v in enumerate(valores):
                h = v / valores[0] / tope * alto
                Rect(w * 0.72, max(h, 0.5), fill=color.transparent(0.25),
                     stroke=color, width=0.8).move_to(
                    Point(ox + i * w + w * 0.14, alto - h), anchor="topleft")
            # la línea del nivel 0 va encima de las barras: debajo la tapaban
            _punteada(Point(ox - 4, uno), Point(ox + ancho_panel + 4, uno),
                      color=TINTA, width=1.0, paso=3)
            mayor = max(valores) / valores[0]
            _txt(f"máximo: × {mayor:.1f}" if mayor > 1.01 else "máximo: el nivel 0",
                 Point(ox + ancho_panel / 2, -10), color=color, size=PIE)
            _txt(nombre, Point(ox + ancho_panel / 2, alto + 13), color=color, size=PIE)
            _txt(f"{len(valores)} niveles", Point(ox + ancho_panel / 2, alto + 25),
                 color=APAGADO, size=PIE)
    return _figura(canvas, ident, pie)
