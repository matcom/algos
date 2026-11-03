"""Ejercicio 13: un splay tree que empieza como un camino, recorrido en orden.

    PrimerAcceso    el acceso a 1 sobre el camino de 16 nodos, paso por paso: cada
                    zig-zig sube a 1 por encima de dos nodos, y el camino queda partido a
                    la mitad
    VuelveAlCamino  el resto de la ronda, con el invariante (C) a la vista: después de
                    acceder a i, la raíz es i y a su izquierda cuelga el camino i-1, ..., 1;
                    al final el árbol es otra vez el camino

    uv run --python 3.13 --with manim manim -ql ejercicio-13.py PrimerAcceso

Cada nodo se dibuja a la altura de su profundidad; las rotaciones son las del splay de
ejercicio-13.py.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import DOWN, RIGHT, UP, Circle, FadeIn, Line, Scene, Transform, VGroup, Write

from comun import (AMARILLO, APAGADO, FONDO, GRIS, VERDE, Narrador, formula, rotulo,
                   titulo)

N = 16


class Nodo:
    def __init__(self, clave):
        self.clave, self.izq, self.der, self.padre = clave, None, None, None


def rotar(x):
    p, g = x.padre, x.padre.padre
    if p.izq is x:
        p.izq, x.der = x.der, p
        if p.izq:
            p.izq.padre = p
    else:
        p.der, x.izq = x.izq, p
        if p.der:
            p.der.padre = p
    p.padre, x.padre = x, g
    if g:
        if g.izq is p:
            g.izq = x
        else:
            g.der = x


def splay_por_pasos(x):
    """El splay, un paso (zig, zig-zig o zig-zag) por vez, con sus rotaciones."""
    while x.padre:
        p, g = x.padre, x.padre.padre
        if g is None:
            rotar(x)
            yield "zig", 1
        elif (g.izq is p) == (p.izq is x):
            rotar(p)
            rotar(x)
            yield "zig-zig", 2
        else:
            rotar(x)
            rotar(x)
            yield "zig-zag", 2


def camino(n):
    nodos = [Nodo(k) for k in range(1, n + 1)]
    for k in range(1, n):
        nodos[k].izq, nodos[k - 1].padre = nodos[k - 1], nodos[k]
    return nodos


def raiz_de(x):
    while x.padre:
        x = x.padre
    return x


def buscar(raiz, clave):
    x = raiz
    while x.clave != clave:
        x = x.izq if clave < x.clave else x.der
    return x


def profundidad(x):
    d = 0
    while x.padre:
        x, d = x.padre, d + 1
    return d


def posiciones(raiz):
    """clave -> punto: x según la clave, y según la profundidad."""
    pos, pila = {}, [(raiz, 0)]
    while pila:
        x, d = pila.pop()
        if x:
            pos[x.clave] = RIGHT * (x.clave - (N + 1) / 2) * 0.75 + UP * (2.45 - 0.33 * d)
            pila += [(x.izq, d + 1), (x.der, d + 1)]
    return pos


def aristas(raiz, pos, color_de=lambda a, b: APAGADO):
    res, pila = VGroup(), [raiz]
    while pila:
        x = pila.pop()
        for h in (x.izq, x.der):
            if h:
                color = color_de(x.clave, h.clave)
                res.add(Line(pos[x.clave], pos[h.clave], color=color,
                             stroke_width=3 if color == APAGADO else 5))
                pila.append(h)
    return res


def circulos(pos):
    return {k: VGroup(Circle(radius=0.19, stroke_color=GRIS, stroke_width=3,
                             fill_color=FONDO, fill_opacity=1),
                      formula(str(k), tam=24)).move_to(p) for k, p in pos.items()}


class PrimerAcceso(Scene):
    def construct(self):
        narr = Narrador()
        self.add(titulo(rf"Acceder a 1 en un camino de {N} nodos"))
        nodos = camino(N)
        raiz = nodos[-1]
        pos = posiciones(raiz)
        nodos_dib = circulos(pos)
        lineas = aristas(raiz, pos)
        self.play(FadeIn(lineas), *[FadeIn(c) for c in nodos_dib.values()], *narr.decir(
            rf"Cada nodo a la altura de su profundidad: 1 está a {N - 1}"))
        self.wait(0.8)
        x = nodos[0]
        nodos_dib[1][0].set_stroke(AMARILLO, 5)
        rot_total = 0
        cuenta = formula(r"\text{rotaciones: } 0", tam=36).move_to(RIGHT * 4.6 + DOWN * 2.2)
        self.play(FadeIn(cuenta))
        for tipo, r in splay_por_pasos(x):
            rot_total += r
            raiz = raiz_de(x)
            pos = posiciones(raiz)
            dicho = (r"Zig-zig: 1 sube por encima de dos nodos; el de arriba queda colgando "
                     r"a la derecha" if tipo == "zig-zig" else rf"Un {tipo} final")
            self.play(Transform(lineas, aristas(raiz, pos)),
                      *[c.animate.move_to(pos[k]) for k, c in nodos_dib.items()],
                      Transform(cuenta, formula(rf"\text{{rotaciones: }} {rot_total}",
                                                tam=36).move_to(cuenta)),
                      *narr.decir(dicho), run_time=0.8)
        self.wait(0.6)
        dos = buscar(raiz, 2)
        ruta = set()
        y = dos
        while y:
            ruta.add(y.clave)
            y = y.padre
        self.play(Transform(lineas, aristas(raiz, pos, lambda a, b: AMARILLO
                                            if a in ruta and b in ruta else APAGADO)),
                  *[nodos_dib[k][0].animate.set_stroke(AMARILLO if k in ruta else GRIS, 4)
                    for k in nodos_dib],
                  *narr.decir(rf"{rot_total} rotaciones, y el camino quedó partido a la "
                              rf"mitad: 2 está a profundidad {profundidad(dos)}",
                              color=AMARILLO))
        self.wait(2.5)


class VuelveAlCamino(Scene):
    def construct(self):
        narr = Narrador()
        self.add(titulo(r"El invariante (C): la ronda vuelve al camino"))
        inv = rotulo(r"después de acceder a $i$: la raíz es $i$\\y a su izquierda, el "
                     r"camino $i-1, \dots, 1$", 30, VERDE).move_to(RIGHT * 4.2 + DOWN * 1.4)
        nodos = camino(N)
        raiz = nodos[-1]
        pos = posiciones(raiz)
        nodos_dib = circulos(pos)
        lineas = aristas(raiz, pos)
        self.play(FadeIn(lineas), *[FadeIn(c) for c in nodos_dib.values()], Write(inv),
                  *narr.decir(r"Recorremos las claves en orden, desde el camino"))
        costos = []
        lista = formula(r"\text{costos:}", tam=30).move_to(DOWN * 2.6)
        self.play(FadeIn(lista))
        for clave in range(1, N + 1):
            x = buscar(raiz, clave)
            costos.append(max(sum(r for _, r in splay_por_pasos(x)), 1))
            raiz = x
            pos = posiciones(raiz)

            def color_de(a, b, i=clave):
                return VERDE if a <= i and b <= i else APAGADO

            self.play(Transform(lineas, aristas(raiz, pos, color_de)),
                      *[c.animate.move_to(pos[k]) for k, c in nodos_dib.items()],
                      Transform(lista, formula(r"\text{costos: }" + r"\ ".join(map(str, costos)),
                                               tam=30).move_to(DOWN * 2.6)),
                      *narr.decir(rf"Acceso a {clave}: costo {costos[-1]}"),
                      run_time=1.0 if clave <= 3 else 0.55)
            self.play(*[c[0].animate.set_stroke(VERDE if k <= clave else GRIS, 3)
                        for k, c in nodos_dib.items()], run_time=0.25)
        self.play(*narr.decir(rf"Total {sum(costos)}: al terminar, el árbol es otra vez el "
                              r"camino, y la ronda siguiente es idéntica", color=VERDE))
        self.wait(2.5)
