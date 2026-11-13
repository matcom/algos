"""Figuras del capítulo 17: Cook-Levin, SAT y 3-SAT.

Cada figura recibe lo que calculó el código del capítulo: el árbol de ramas que
salió de simular la máquina, la tabla de la rama que acepta, las cláusulas que
devolvió la partición con la asignación que las satisface, y los tamaños de la
fórmula que el código contó.
"""

from tesserax import Canvas, Colors, Line, Point, Rect

from figuras import (
    ACENTO, ALARMA, APAGADO, CALIDO, CUERPO, OSCURO, PIE, REGLA, TINTA,
    _figura, _punto, _txt, grafica_log_log,
)


def _bonito(s):
    """q0 -> q₀, qa -> qₐ, _ -> ␣ para las etiquetas."""
    return {"q0": "q₀", "qa": "qₐ", "_": "␣"}.get(s, s)


def arbol(nodos, aristas, sucesores, ident="cl-arbol", pie=""):
    """`nodos`: {id: (paso, configuración)} y `aristas`: pares (padre, hijo), tal
    como los calculó el código. `sucesores` dice si una configuración se detuvo."""
    def etiqueta(c):
        p = next(k for k, s in enumerate(c) if s in ("q0", "qa"))
        return f"{_bonito(c[p])}, celda {p}"

    def tipo(c):
        if "qa" in c:
            return "acepta"
        return "rechaza" if sucesores(c) == [c] else "sigue"

    nodos = {v: (paso, etiqueta(c), tipo(c)) for v, (paso, c) in nodos.items()}
    por_nivel = {}
    for v, (nivel, _, _) in sorted(nodos.items()):
        por_nivel.setdefault(nivel, []).append(v)
    ancho_max = max(len(vs) for vs in por_nivel.values())
    paso_x, paso_y = 104.0, 40.0
    pos = {}
    for nivel, vs in por_nivel.items():
        x0 = (ancho_max - len(vs)) * paso_x / 2
        for k, v in enumerate(vs):
            pos[v] = Point(x0 + k * paso_x, nivel * paso_y)
    colores = {"sigue": TINTA, "acepta": OSCURO, "rechaza": APAGADO}
    with Canvas() as canvas:
        for u, v in aristas:
            Line(pos[u], pos[v], stroke=REGLA, width=1.2)
        for v, (nivel, etiqueta, tipo) in nodos.items():
            color = colores[tipo]
            fondo = ACENTO.transparent(0.15) if tipo == "acepta" else Colors.White
            Rect(92, 22, fill=fondo, stroke=color, width=1.0).move_to(pos[v])
            _txt(etiqueta, pos[v], color=color, size=CUERPO)
        for nivel in por_nivel:
            _txt(f"paso {nivel}", Point(-58, nivel * paso_y), color=APAGADO,
                 size=PIE, anchor="end")
    return _figura(canvas, ident, pie)


def tabla(filas, ventana, ident="cl-tabla", pie=""):
    """`filas`: la tabla, una tupla de símbolos por fila. `ventana`: (i, j), la
    esquina superior izquierda de la ventana de 2 × 3 que se resalta."""
    lado = 24.0
    vi, vj = ventana
    with Canvas() as canvas:
        for i, fila in enumerate(filas):
            _txt(f"fila {i}", Point(-12, i * lado + lado / 2), color=APAGADO,
                 size=PIE, anchor="end")
            for j, s in enumerate(fila):
                centro = Point(j * lado + lado / 2, i * lado + lado / 2)
                es_estado = s in ("q0", "qa")
                fondo = (ACENTO.transparent(0.18) if s == "qa" else
                         CALIDO.transparent(0.12) if es_estado else Colors.White)
                Rect(lado, lado, fill=fondo, stroke=REGLA, width=0.8).move_to(centro)
                _txt(_bonito(s), centro, color=TINTA, size=CUERPO)
        for j in range(len(filas[0])):
            _txt(str(j), Point(j * lado + lado / 2, -9), color=APAGADO, size=PIE)
        Rect(3 * lado, 2 * lado, fill=Colors.Transparent, stroke=ALARMA,
             width=2.2).move_to(Point(vj * lado + 1.5 * lado, vi * lado + lado))
    return _figura(canvas, ident, pie)


def cadena(original, partes, n, verdadero, ident="cl-cadena", pie=""):
    """`original`: la cláusula larga como enteros; las variables 1..n son las x y
    las demás las y nuevas. `partes`: las cláusulas de tres literales que devolvió
    la partición. `verdadero(l)`: el valor del literal l en la asignación que las
    satisface. Un literal verdadero va relleno."""
    def nombre(l):
        v = f"x{abs(l)}" if abs(l) <= n else f"y{abs(l) - n}"
        return ("¬" if l < 0 else "") + v

    valores = {nombre(l): verdadero(l) for c in partes + [original] for l in c}
    original = [nombre(l) for l in original]
    partes = [[nombre(l) for l in c] for c in partes]
    lado_w, lado_h, sep = 40.0, 20.0, 4.0

    def caja(x, y, lit):
        verdadero = valores[lit]
        nueva = "y" in lit
        borde = CALIDO if nueva else TINTA
        fondo = ACENTO.transparent(0.22) if verdadero else Colors.White
        Rect(lado_w, lado_h, fill=fondo, stroke=borde, width=1.0) \
            .move_to(Point(x + lado_w / 2, y))
        _txt(lit, Point(x + lado_w / 2, y), color=borde, size=CUERPO)

    with Canvas() as canvas:
        _txt("la cláusula", Point(-10, 0), color=APAGADO, size=PIE, anchor="end")
        for k, lit in enumerate(original):
            caja(k * (lado_w + sep), 0, lit)
        for n, c in enumerate(partes):          # dos partes por renglón
            x = (n % 2) * (3 * (lado_w + sep) + 18)
            y = 46.0 + (n // 2) * 30
            for k, lit in enumerate(c):
                caja(x + k * (lado_w + sep), y, lit)
        _txt("las partes", Point(-10, 46.0), color=APAGADO, size=PIE, anchor="end")
    return _figura(canvas, ident, pie)


def tamanos(series, ident="cl-tamanos", pie=""):
    """`series`: {nombre: [(t, cantidad), ...]} que contó el código."""
    return grafica_log_log(series, "t, pasos de la máquina", "cantidad",
                           ident=ident, pie=pie)
