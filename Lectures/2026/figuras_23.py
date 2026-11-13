"""Figuras del capítulo 23: esquemas de aproximación.

Cada figura recibe lo que calculó el código del capítulo: los valores de la mochila y
los que salieron del redondeo con su μ, los tiempos medidos del FPTAS, la asignación
del PTAS de balanceo de carga con sus tareas largas, y la tabla de garantías de la
Parte III que el capítulo arma en su última sección.
"""

from tesserax import Canvas, Circle, Colors, Line, Point, Rect

from figuras import (
    ACENTO, ALARMA, APAGADO, CALIDO, CUERPO, OSCURO, PIE, REGLA, TINTA,
    _figura, _txt, sub, grafica_log_log,
)


def redondeo(v, vr, mu, ident="esq-redondeo", pie=""):
    """`v`: valores originales; `vr`: valores redondeados (v'_i = piso(v_i / mu));
    `mu`: el paso. Cada objeto es una columna: el contorno llega a v_i, el relleno a
    mu * v'_i, y la franja entre los dos es lo que se perdió, siempre menor que mu."""
    alto, ancho_col, sep = 170.0, 26.0, 14.0
    tope = max(v) * 1.05
    y = lambda x: alto - x / tope * alto
    n = len(v)
    ancho = n * (ancho_col + sep)
    with Canvas() as canvas:
        k = 0
        while k * mu <= tope:
            Line(Point(0, y(k * mu)), Point(ancho, y(k * mu)), stroke=REGLA, width=0.6)
            if k % 2 == 0:
                _txt(f"{k}μ", Point(-6, y(k * mu)), color=APAGADO, size=PIE, anchor="end")
            k += 1
        Line(Point(0, alto), Point(ancho, alto), stroke=APAGADO, width=1.0)
        for i in range(n):
            x = sep / 2 + i * (ancho_col + sep)
            alto_v, alto_r = v[i] / tope * alto, mu * vr[i] / tope * alto
            Rect(ancho_col, alto_r, fill=ACENTO.transparent(0.3), stroke=OSCURO,
                 width=0.9).move_to(Point(x, alto - alto_r), anchor="topleft")
            Rect(ancho_col, alto_v - alto_r, fill=CALIDO.transparent(0.35),
                 stroke=CALIDO, width=0.9).move_to(Point(x, alto - alto_v),
                                                  anchor="topleft")
            _txt(str(v[i]), Point(x + ancho_col / 2, alto - alto_v - 7), color=TINTA,
                 size=PIE)
            _txt(f"v'{sub(i + 1)}={vr[i]}", Point(x + ancho_col / 2, alto + 11),
                 color=OSCURO, size=PIE)
        Rect(9, 9, fill=ACENTO.transparent(0.3), stroke=OSCURO, width=0.9).move_to(
            Point(0, alto + 26), anchor="topleft")
        _txt("μ·v'ᵢ, lo que queda", Point(13, alto + 30.5), color=OSCURO, size=PIE,
             anchor="start")
        Rect(9, 9, fill=CALIDO.transparent(0.35), stroke=CALIDO, width=0.9).move_to(
            Point(ancho / 2, alto + 26), anchor="topleft")
        _txt("lo que se pierde, < μ", Point(ancho / 2 + 13, alto + 30.5), color=CALIDO,
             size=PIE, anchor="start")
    return _figura(canvas, ident, pie)


def tiempos(puntos, ident="esq-tiempo", pie=""):
    """`puntos`: [(1/ε, segundos)] medidos. Se dibuja al lado la recta que pasa por el
    último punto con pendiente 1, que es lo que predice O(n³/ε) con n fijo. Se ancla en
    el último porque es el que menos pesan los costos fijos y el ruido del reloj."""
    k0, t0 = puntos[-1]
    recta = [(k, t0 * k / k0) for k, _ in puntos]
    return grafica_log_log({"FPTAS medido": puntos, "pendiente 1": recta},
                           "1/ε", "segundos", ident=ident, pie=pie)


def ptas_carga(t, asign, largas, m, ident="esq-ptas", pie=""):
    """`t`: duraciones; `asign[j]`: la máquina de la tarea j; `largas`: los índices de
    las k tareas que se asignaron óptimas. Las tareas se dibujan en el orden en que el
    algoritmo las puso: primero las largas, después las cortas de mayor a menor."""
    escala, alto, sep = 9.0, 24.0, 8.0
    cargas = [0] * m
    orden = list(largas) + sorted((j for j in range(len(t)) if j not in largas),
                                  key=lambda j: -t[j])
    with Canvas() as canvas:
        for j in orden:
            i = asign[j]
            x0, w = cargas[i] * escala, t[j] * escala
            larga = j in largas
            Rect(w, alto, fill=(ACENTO if larga else CALIDO).transparent(0.2),
                 stroke=OSCURO if larga else CALIDO, width=0.9).move_to(
                Point(x0 + w / 2, i * (alto + sep) + alto / 2))
            _txt(str(t[j]), Point(x0 + w / 2, i * (alto + sep) + alto / 2),
                 color=TINTA, size=PIE)
            cargas[i] += t[j]
        for i in range(m):
            _txt(f"M{sub(i + 1)}", Point(-8, i * (alto + sep) + alto / 2),
                 color=APAGADO, size=CUERPO, anchor="end")
        fondo = m * (alto + sep)
        L = max(cargas)
        Line(Point(L * escala, -6), Point(L * escala, fondo), stroke=CALIDO, width=1.0)
        _txt(f"makespan = {L}", Point(L * escala + 4, -12), color=CALIDO, size=CUERPO,
             anchor="start")
        Rect(9, 9, fill=ACENTO.transparent(0.2), stroke=OSCURO, width=0.9).move_to(
            Point(0, fondo + 6), anchor="topleft")
        _txt("larga: asignación óptima", Point(13, fondo + 10.5), color=OSCURO,
             size=PIE, anchor="start")
        Rect(9, 9, fill=CALIDO.transparent(0.2), stroke=CALIDO, width=0.9).move_to(
            Point(150, fondo + 6), anchor="topleft")
        _txt("corta: regla de Graham", Point(163, fondo + 10.5), color=CALIDO,
             size=PIE, anchor="start")
    return _figura(canvas, ident, pie)


def mapa(clases, filas, ident="esq-mapa", pie=""):
    """`clases`: nombres de las columnas, de la garantía más fuerte a la más débil.
    `filas`: [(problema, logrado, excluido_hasta, capitulo)]: `logrado` es la columna
    de la mejor garantía demostrada; las columnas < `excluido_hasta` quedan excluidas
    si P != NP. Lo que queda entre las dos es lo que el libro no decide."""
    col, fila, izq = 62.0, 19.0, 150.0
    with Canvas() as canvas:
        for c, nombre in enumerate(clases):
            _txt(nombre, Point(izq + c * col + col / 2, -10), color=APAGADO, size=PIE)
        for r, (problema, logrado, excluido, cap) in enumerate(filas):
            yc = r * fila + fila / 2
            _txt(problema, Point(izq - 8, yc), color=TINTA, size=PIE, anchor="end")
            for c in range(len(clases)):
                x = izq + c * col
                if c < excluido:
                    fondo, borde = ALARMA.transparent(0.12), ALARMA.transparent(0.35)
                elif c < logrado:
                    fondo, borde = Colors.White, APAGADO
                else:
                    fondo, borde = ACENTO.transparent(0.10), REGLA
                Rect(col - 2, fila - 3, fill=fondo, stroke=borde, width=0.6).move_to(
                    Point(x + col / 2, yc))
                if c < excluido:
                    _txt("×", Point(x + col / 2, yc), color=ALARMA, size=CUERPO)
                elif c < logrado:
                    _txt("?", Point(x + col / 2, yc), color=APAGADO, size=CUERPO)
            Circle(4.5, fill=OSCURO, stroke=OSCURO).move_to(
                Point(izq + logrado * col + col / 2, yc))
            _txt(cap, Point(izq + len(clases) * col + 6, yc), color=APAGADO, size=PIE,
                 anchor="start")
        y = len(filas) * fila + 10
        Circle(4.5, fill=OSCURO, stroke=OSCURO).move_to(Point(izq, y))
        _txt("mejor garantía demostrada o citada", Point(izq + 8, y), color=OSCURO,
             size=PIE, anchor="start")
        _txt("×", Point(izq + 170, y), color=ALARMA, size=CUERPO)
        _txt("imposible si P ≠ NP", Point(izq + 178, y), color=ALARMA, size=PIE,
             anchor="start")
        if any(logrado > excluido for _, logrado, excluido, _ in filas):
            _txt("?", Point(izq + 290, y), color=APAGADO, size=CUERPO)
            _txt("el libro no lo decide", Point(izq + 298, y), color=APAGADO,
                 size=PIE, anchor="start")
    return _figura(canvas, ident, pie)
