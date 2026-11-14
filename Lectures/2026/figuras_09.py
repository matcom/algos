"""Figuras del capítulo 9: algoritmos golosos con argumentos de intercambio.

Cada función recibe el estado que calculó el código del capítulo (órdenes, tiempos
de terminación, retrasos, contenidos de la caché pedido a pedido) y no decide nada
del algoritmo.
"""

from tesserax import Canvas, Colors, Line, Point, Rect

from figuras import (
    ACENTO, ALARMA, APAGADO, CALIDO, CUERPO, OSCURO, PIE, REGLA, TINTA,
    _figura, _punto, _txt,
)


# --------------------------------------------------------------------------
# 1. un orden con una inversión vecina, antes y después del intercambio
# --------------------------------------------------------------------------

def inversion(t, d, filas, par, ident="golosos-inversion", pie=""):
    """`filas` es una lista de (título, orden, finales, retrasos) que calculó el
    capítulo; `par` son las dos tareas (índices) que se intercambian."""
    u, alto, sep = 20.0, 22.0, 78.0
    total = sum(t)
    with Canvas() as canvas:
        for r, (titulo, orden, finales, retrasos) in enumerate(filas):
            y = r * sep
            _txt(titulo, Point(-12, y), color=APAGADO, size=PIE, anchor="end")
            inicio = 0
            for i in orden:
                x0, x1 = inicio * u, finales[i] * u
                marcada = i in par
                Rect(x1 - x0, alto,
                     fill=CALIDO.transparent(0.18) if marcada else ACENTO.transparent(0.10),
                     stroke=CALIDO if marcada else OSCURO,
                     width=1.4 if marcada else 0.8).move_to(Point((x0 + x1) / 2, y))
                _txt(f"{i + 1}", Point((x0 + x1) / 2, y - 3), size=CUERPO)
                _txt(f"d={d[i]}", Point((x0 + x1) / 2, y + 7), color=APAGADO, size=PIE)
                ell = retrasos[i]
                _txt(f"ℓ={ell}", Point((x0 + x1) / 2, y - alto / 2 - 8),
                     color=ALARMA if ell > 0 else APAGADO, size=PIE)
                inicio = finales[i]
            # eje de tiempo
            ye = y + alto / 2 + 6
            Line(Point(0, ye), Point(total * u, ye), stroke=REGLA.darker(0.3), width=0.7)
            for s in range(total + 1):
                Line(Point(s * u, ye), Point(s * u, ye + 3), stroke=REGLA.darker(0.3),
                     width=0.7)
                if s % 2 == 0:
                    _txt(str(s), Point(s * u, ye + 10), color=APAGADO, size=PIE)
            L = max(retrasos)
            _txt(f"L = {L}", Point(total * u + 14, y), color=ALARMA if L else TINTA,
                 size=CUERPO, anchor="start")
    return _figura(canvas, ident, pie)


# --------------------------------------------------------------------------
# 2 y 3. la caché pedido a pedido
# --------------------------------------------------------------------------

def _casillas(seq, caches, k, hasta):
    """Asigna cada elemento a una casilla fija mientras está en la caché: el que
    entra ocupa la casilla del que sale. Es solo presentación."""
    casillas, filas = [None] * k, []
    for t in range(hasta):
        actual = caches[t]
        for s in range(k):
            if casillas[s] is not None and casillas[s] not in actual:
                casillas[s] = None
        for x in sorted(actual):
            if x not in casillas:
                casillas[casillas.index(None)] = x
        filas.append(list(casillas))
    return filas


def _fila_cache(seq, caches, k, y0, desde, hasta, nombre, marcar=(),
                paso=26.0, lado=20.0):
    filas = _casillas(seq, caches, k, hasta)
    fallos = 0
    for t in range(desde, hasta):
        x = (t - desde) * paso
        antes = caches[t - 1] if t > 0 else frozenset()
        fallo = seq[t] not in antes
        fallos += fallo
        if fallo:
            _punto(Point(x, y0 - lado / 2 - 6), ALARMA, r=2.4)
        traidos = caches[t] - antes - {seq[t]}
        for s in range(k):
            c = Point(x, y0 + s * lado)
            v = filas[t][s]
            pedido = v == seq[t]
            raro = v in traidos
            Rect(lado, lado,
                 fill=ACENTO.transparent(0.18) if pedido else Colors.White,
                 stroke=CALIDO if (v in marcar or raro) else (OSCURO if pedido else REGLA.darker(0.3)),
                 width=1.5 if (v in marcar or raro) else 0.8).move_to(c)
            if v is not None:
                _txt(v, c, color=CALIDO if raro else TINTA, size=CUERPO)
    _txt(nombre, Point(-lado / 2 - 8, y0 + (k - 1) * lado / 2), color=TINTA,
         size=PIE, anchor="end")
    return fallos


def _cabecera(seq, desde, hasta, y, paso=26.0):
    for t in range(desde, hasta):
        x = (t - desde) * paso
        _txt(str(t + 1), Point(x, y - 12), color=APAGADO, size=PIE)
        _txt(seq[t], Point(x, y), color=TINTA, size=CUERPO)


def traza(seq, k, filas, ident="golosos-traza", pie=""):
    """`filas` es una lista de (nombre, caches) con caches[t] el contenido después
    de atender el pedido t, como lo calculó la simulación del capítulo."""
    lado, sep = 20.0, 0.0
    with Canvas() as canvas:
        _cabecera(seq, 0, len(seq), -28)
        y = 0.0
        for nombre, caches in filas:
            _fila_cache(seq, caches, k, y, 0, len(seq), nombre)
            y += k * lado + 26
        _punto(Point(len(seq) * 26.0 - 8, -40), ALARMA, r=2.4)
        _txt("fallo", Point(len(seq) * 26.0 - 2, -40), color=ALARMA, size=PIE,
             anchor="start")
    return _figura(canvas, ident, pie)


def transformacion(seq, k, S, Sp, desde, hasta, e, f, ident="golosos-transformacion",
                   pie=""):
    """`S` y `Sp` son las dos planificaciones que construyó el capítulo, pedido a
    pedido; se dibujan los pedidos `desde` .. `hasta - 1`."""
    lado = 20.0
    with Canvas() as canvas:
        _cabecera(seq, desde, hasta, -28)
        _fila_cache(seq, S, k, 0, desde, hasta, "S", marcar=(e, f))
        _fila_cache(seq, Sp, k, k * lado + 26, desde, hasta, "S′", marcar=(e, f))
    return _figura(canvas, ident, pie)
