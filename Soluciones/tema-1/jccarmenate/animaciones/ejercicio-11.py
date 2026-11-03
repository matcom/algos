"""Ejercicio 11: la mochila en O(nW) y el tamaño de la entrada. Dos escenas:

    Fila  un objeto de peso 3 y valor 5 sobre la fila de capacidades 0..9, recorrida de
          mayor a menor y de menor a mayor: al revés, desde la capacidad 6 cada celda
          lee una que ya usó el objeto, y la 9 lo usa tres veces
    Bits  agregar un bit a W duplica la tabla, pero a la entrada solo le suma un bit:
          O(nW) es exponencial en lo que cuesta escribir W

    uv run --python 3.13 --with manim manim -ql ejercicio-11.py Fila

El objeto y la capacidad de la primera escena son los de la sección 6 del ejercicio.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import (DOWN, LEFT, RIGHT, UP, CurvedArrow, FadeIn, FadeOut, Rectangle, Scene,
                   Transform, VGroup, Write)

from comun import (AMARILLO, AZUL, DORADO, GRIS, ROJO, VERDE, Narrador, fila, formula,
                   indices, rotulo, titulo)

PESO, VALOR, W = 3, 5, 9


def recorrer(descendente):
    """La fila de mochila() en ejercicio-11.py con un solo objeto; anota qué valor lee
    cada actualización en la celda c - peso."""
    mejor = [0] * (W + 1)
    orden = range(W, PESO - 1, -1) if descendente else range(PESO, W + 1)
    pasos = []
    for c in orden:
        nuevo = max(mejor[c], mejor[c - PESO] + VALOR)
        pasos.append((c, mejor[c - PESO], nuevo))
        mejor[c] = nuevo
    return pasos, mejor


class Fila(Scene):
    def construct(self):
        narr = Narrador()
        self.add(titulo(r"Por qué la fila se recorre de mayor a menor"))
        obj = formula(rf"\text{{un objeto: peso }} {PESO}, \text{{ valor }} {VALOR}", tam=38,
                      color=AMARILLO).move_to(UP * 2.45)
        cod = formula(r"\texttt{best}[c] = \max(\texttt{best}[c],\ "
                      r"\texttt{best}[c - 3] + 5)", tam=36).move_to(UP * 1.75)
        filas = {}
        for y, desc, nombre, color in ((0.45, True, r"de mayor a menor", VERDE),
                                       (-1.55, False, r"de menor a mayor", ROJO)):
            f = fila([0] * (W + 1), lado=0.72, tam=32).move_to(UP * y + RIGHT * 0.9)
            rot = rotulo(nombre, 30, color).next_to(f, LEFT, 0.35)
            filas[desc] = (f, indices(f, 22), rot)
        self.play(Write(obj), FadeIn(cod), *[FadeIn(VGroup(*v)) for v in filas.values()],
                  *narr.decir(r"La fila guarda el mejor valor para cada capacidad $c$ de 0 "
                              r"a 9"))
        self.wait(0.8)
        for desc in (True, False):
            f = filas[desc][0]
            pasos, mejor = recorrer(desc)
            self.play(*narr.decir(
                r"De mayor a menor: $c - 3$ todavía tiene el valor \emph{sin} el objeto"
                if desc else
                r"De menor a mayor: desde $c = 6$, $c - 3$ ya se actualizó, "
                r"\emph{con} el objeto",
                color=VERDE if desc else ROJO))
            for c, leido, nuevo in pasos:
                flecha = CurvedArrow(f[c - PESO].get_top() + UP * 0.05,
                                     f[c].get_top() + UP * 0.05, angle=-1.0,
                                     color=AMARILLO, stroke_width=3, tip_length=0.14)
                color = ROJO if leido > 0 else VERDE
                self.play(FadeIn(flecha), f[c - PESO][0].animate.set_stroke(AMARILLO, 5),
                          run_time=0.3)
                self.play(f[c][1].animate.become(formula(str(nuevo), tam=32, color=color)
                                                 .move_to(f[c])),
                          f[c][0].animate.set_stroke(color, 4),
                          f[c - PESO][0].animate.set_stroke(GRIS, 2.5), FadeOut(flecha),
                          run_time=0.35)
            if desc:
                dicho = rf"Capacidad 9: {mejor[W]}, el objeto usado una vez"
            else:
                dicho = rf"Capacidad 9: {mejor[W]}, el mismo objeto usado {mejor[W] // VALOR} veces"
            self.play(*narr.decir(dicho, color=VERDE if desc else ROJO))
            self.wait(1)
        self.play(*narr.decir(r"Al revés calcula la mochila con repetición; solo se nota si "
                              r"un objeto cabe dos veces", color=ROJO))
        self.wait(2.5)


class Bits(Scene):
    def construct(self):
        narr = Narrador()
        self.add(titulo(r"$O(nW)$, con $W$ medido en bits"))
        unidad = 0.035                      # ancho de una celda de la tabla
        rot_bits = rotulo(r"$W$, como se escribe:", 32, AZUL).move_to(LEFT * 4.6 + UP * 2.3)
        rot_tabla = rotulo(r"la tabla, una celda por capacidad:", 32, DORADO)
        rot_tabla.move_to(LEFT * 3.7 + UP * 0.25)
        self.play(FadeIn(rot_bits), FadeIn(rot_tabla))
        bits_w = tabla = lectura = None
        for b in range(3, 9):
            W_b = 2 ** b
            nuevos = VGroup(*[formula("1" if k == 0 else "0", tam=40, color=AZUL)
                              for k in range(b + 1)])
            nuevos.arrange(RIGHT, buff=0.08).move_to(LEFT * 6.3 + UP * 1.5, aligned_edge=LEFT)
            barra = Rectangle(width=W_b * unidad, height=0.8, stroke_width=0,
                              fill_color=DORADO, fill_opacity=0.85)
            barra.move_to(LEFT * 6.3 + DOWN * 0.6, aligned_edge=LEFT)
            texto = VGroup(
                formula(rf"W = 2^{{{b}}} = {W_b}", tam=36),
                formula(rf"\text{{bits de }} W: {b + 1}", tam=36, color=AZUL),
                formula(rf"\text{{celdas por objeto: }} {W_b + 1}", tam=36, color=DORADO))
            texto.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(RIGHT * 3.6 + DOWN * 2.1)
            if bits_w is None:
                self.play(FadeIn(nuevos), FadeIn(barra), FadeIn(texto), *narr.decir(
                    r"Cada bit más de $W$ es un símbolo más en la entrada"))
                bits_w, tabla, lectura = nuevos, barra, texto
            else:
                self.play(Transform(bits_w, nuevos), Transform(tabla, barra),
                          Transform(lectura, texto), *narr.decir(
                              r"Un bit más: la entrada crece en uno, la tabla se duplica"),
                          run_time=1.0)
            self.wait(0.6)
        self.play(*narr.decir(r"$nW < b \cdot 2^b$: polinomial en el \emph{valor} de $W$, "
                              r"exponencial en sus bits", color=ROJO))
        self.wait(2.5)
