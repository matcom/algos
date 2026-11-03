"""Ejercicio 3: la pila con mínimo. Dos escenas:

    Paralela   las diez operaciones de la sección 2: cada celda de M es el mínimo del
               prefijo de S hasta su altura, así que al hacer pop, el mínimo de antes
               está guardado justo debajo
    Repetidos  la versión compacta con <= y con <, lado a lado, sobre la secuencia más
               corta que rompe la de <: push 0, push 0, pop

    uv run --python 3.13 --with manim manim -ql ejercicio-03.py Paralela
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import (DOWN, LEFT, RIGHT, UP, Create, FadeIn, FadeOut, Flash, Line, Scene,
                   SurroundingRectangle, Transform, TransformFromCopy, VGroup, Write)

from comun import (AMARILLO, APAGADO, AZUL, GRIS, ROJO, VERDE, Narrador, celda,
                   formula, rotulo, titulo)

OPERACIONES = [("push", 5), ("push", 7), ("push", 3), ("push", 3),
               ("push", 8), ("push", 1), ("pop", None), ("pop", None),
               ("pop", None), ("push", 4)]


class Columna:
    """Una pila dibujada como columna de celdas que crece hacia arriba. `valores` es la
    pila de verdad; `celdas`, su dibujo."""

    def __init__(self, x, base, nombre, color=GRIS, lado=0.62):
        self.x, self.base, self.lado, self.color = x, base, lado, color
        self.valores, self.celdas = [], []
        self.piso = Line(RIGHT * (x - 0.55) + UP * base, RIGHT * (x + 0.55) + UP * base,
                         color=APAGADO, stroke_width=3)
        self.nombre = formula(nombre, tam=36, color=GRIS).next_to(self.piso, DOWN, 0.15)

    def lugar(self, i):
        return RIGHT * self.x + UP * (self.base + self.lado / 2 + i * self.lado)

    def push(self, valor):
        c = celda(valor, self.lado, tam=30, color=self.color)
        c.move_to(self.lugar(len(self.celdas)))
        self.valores.append(valor)
        self.celdas.append(c)
        return c

    def pop(self):
        return self.valores.pop(), self.celdas.pop()


class Paralela(Scene):
    def construct(self):
        narr = Narrador()
        self.add(titulo(r"La pila de los mínimos, en paralelo"))
        inv = formula(r"M[i] = \min(S[0], \dots, S[i])", tam=40, color=AMARILLO)
        inv.shift(UP * 2.5 + RIGHT * 3.2)
        S = Columna(-1.6, -2.3, "S")
        M = Columna(0.2, -2.3, "M", color=AZUL)
        self.play(Create(S.piso), Create(M.piso), Write(S.nombre), Write(M.nombre),
                  Write(inv), *narr.decir(r"$S$ es la pila; $M$ guarda, a cada altura, el "
                                          r"mínimo de lo que hay hasta ahí"))
        op_rot = minimo = None
        for nombre, x in OPERACIONES:
            texto = (rf"\texttt{{push({x})}}" if nombre == "push"
                     else r"\texttt{pop()}")
            nuevo_rot = rotulo(texto, 38).move_to(LEFT * 4.8 + UP * 1.0)
            self.play(Transform(op_rot, nuevo_rot) if op_rot else FadeIn(nuevo_rot),
                      run_time=0.5)
            op_rot = op_rot or nuevo_rot
            if nombre == "push":
                cs = S.push(x)
                self.play(FadeIn(cs, shift=0.4 * DOWN), run_time=0.6)
                if not M.valores:
                    cm = M.push(x)
                    self.play(TransformFromCopy(cs, cm), *narr.decir(
                        r"La pila estaba vacía: el mínimo es el único elemento"))
                else:
                    tope, arriba = M.valores[-1], M.celdas[-1]
                    signo = "<" if x < tope else r"\ge"
                    comp = formula(str(x), signo, str(tope), tam=40, color=AMARILLO)
                    comp.next_to(arriba, RIGHT, 0.5)
                    self.play(arriba[0].animate.set_stroke(AMARILLO, 5), FadeIn(comp),
                              run_time=0.6)
                    if x < tope:
                        cm = M.push(x)
                        origen, dicho = cs, rf"${x} < {tope}$: el mínimo nuevo es {x}"
                    else:
                        cm = M.push(tope)
                        origen, dicho = arriba, (rf"${x} \ge {tope}$: se copia el mínimo de "
                                                 r"abajo")
                    self.play(TransformFromCopy(origen, cm), FadeOut(comp),
                              arriba[0].animate.set_stroke(AZUL, 2.5), *narr.decir(dicho))
                # El invariante en la posición nueva: el prefijo de S y su mínimo.
                prefijo = SurroundingRectangle(VGroup(*S.celdas), color=AMARILLO, buff=0.05)
                self.play(Create(prefijo), cm[0].animate.set_stroke(AMARILLO, 5),
                          run_time=0.5)
                self.play(FadeOut(prefijo), cm[0].animate.set_stroke(AZUL, 2.5),
                          run_time=0.4)
            else:
                sale, cs = S.pop()
                _, cm = M.pop()
                self.play(FadeOut(cs, shift=0.4 * UP), FadeOut(cm, shift=0.4 * UP),
                          *narr.decir(rf"Sale el {sale}, de las dos pilas a la vez"),
                          run_time=0.7)
                self.play(M.celdas[-1][0].animate.set_stroke(VERDE, 5), *narr.decir(
                    rf"El mínimo de antes, {M.valores[-1]}, estaba guardado justo debajo"),
                    run_time=0.6)
                self.play(M.celdas[-1][0].animate.set_stroke(AZUL, 2.5), run_time=0.3)
            nuevo_min = formula(r"\texttt{min()} = ", str(M.valores[-1]), tam=40,
                                color=VERDE).move_to(RIGHT * 4.3 + DOWN * 0.3)
            self.play(Transform(minimo, nuevo_min) if minimo else FadeIn(nuevo_min),
                      run_time=0.4)
            minimo = minimo or nuevo_min
            self.wait(0.3)
        self.play(*narr.decir(r"Cada operación toca solo los topes: $O(1)$ en el peor caso",
                              color=VERDE))
        self.wait(2.5)


class Repetidos(Scene):
    def construct(self):
        narr = Narrador()
        self.add(titulo(r"Guardar solo los récords: $\le$ contra $<$"))
        paneles = {}
        for centro, estricto, color in ((-3.4, False, VERDE), (3.4, True, ROJO)):
            S = Columna(centro - 0.8, -1.9, "S", lado=0.8)
            M = Columna(centro + 0.8, -1.9, "M", color=AZUL, lado=0.8)
            signo = "<" if estricto else r"\le"
            cod = rotulo(rf"\texttt{{if x}} ${signo}$ \texttt{{M[-1]: M.append(x)}}", 30,
                         color).move_to(RIGHT * centro + UP * 2.4)
            self.add(S.piso, M.piso, S.nombre, M.nombre, cod)
            paneles[estricto] = (S, M)
        self.play(*narr.decir(r"La misma pila compacta, con una sola diferencia: "
                              r"$\le$ o $<$ en el push"))
        self.wait(0.8)

        def push(estricto, x):
            S, M = paneles[estricto]
            cs = S.push(x)
            anims = [FadeIn(cs, shift=0.4 * DOWN)]
            if not M.valores or (x < M.valores[-1] if estricto else x <= M.valores[-1]):
                anims.append(TransformFromCopy(cs, M.push(x)))
            return anims

        for dicho in (r"\texttt{push(0)}: entra en las dos $M$",
                      r"Otro \texttt{push(0)}: con $\le$ entra en $M$; con $<$ no, porque $0 < 0$ es falso"):
            self.play(*push(False, 0), *push(True, 0), *narr.decir(dicho), run_time=1.0)
            self.wait(0.8)

        # pop compara por valor con el tope de M.
        anims = []
        for estricto in (False, True):
            S, M = paneles[estricto]
            sale, cs = S.pop()
            anims.append(FadeOut(cs, shift=0.4 * UP))
            if M.valores and sale == M.valores[-1]:
                anims.append(FadeOut(M.pop()[1], shift=0.4 * UP))
        self.play(*anims, *narr.decir(r"\texttt{pop()}: el 0 que sale es igual al tope de $M$, "
                                      r"y se lo lleva"), run_time=1.0)
        self.wait(0.6)
        S, M = paneles[True]
        vacia = rotulo(r"vacía", 34, ROJO).move_to(M.lugar(0))
        mal = formula(r"\texttt{min()}", r"\ ?", tam=40, color=ROJO)
        mal.move_to(RIGHT * 3.4 + UP * 1.2)
        bien = formula(r"\texttt{min()} = 0", tam=40, color=VERDE)
        bien.move_to(LEFT * 3.4 + UP * 1.2)
        self.play(FadeIn(vacia), Write(mal), Write(bien), Flash(M.piso, color=ROJO),
                  *narr.decir(r"Con $<$, el 0 que salió se llevó el récord del otro 0: "
                              r"$S$ tiene un 0 y $M$ está vacía", color=ROJO))
        self.wait(2.5)
