"""Ejercicio 6: búsqueda en una matriz con filas y columnas ordenadas. Dos escenas:

    Escalera    desde la esquina superior derecha, cada comparación descarta una fila o
                una columna; lo descartado es justo lo que dice el invariante, y el
                potencial filas + columnas baja de a uno
    Adversario  la matriz de las dos antidiagonales: la escalera mira las 2n - 1 celdas;
                la versión con j > 0 deja una sin mirar, y el adversario pone x ahí

    uv run --python 3.13 --with manim manim -ql ejercicio-06.py Escalera

La matriz de la primera escena es la de la figura 1 del ejercicio.
"""

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import (DOWN, LEFT, RIGHT, UP, Create, FadeIn, FadeOut, Flash, LaggedStart,
                   Scene, Square, SurroundingRectangle, Transform, VGroup, VMobject, Write)

from comun import (AMARILLO, APAGADO, AZUL, DORADO, FONDO, ROJO, VERDE, Narrador,
                   formula, rotulo, titulo)


def matriz_al_azar(n, rng, paso=3):
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            base = max(M[i - 1][j] if i else 0, M[i][j - 1] if j else 0)
            M[i][j] = base + rng.randint(1, paso)
    return M


def escalera(M, x, columna_cero=True):
    """La escalera de ejercicio-06.py, guardando cada celda que mira. Con
    columna_cero = False es el error plantado de la sección 7: while ... and j > 0."""
    n = len(M)
    i, j = 0, n - 1
    pasos = []
    while i < n and (j >= 0 if columna_cero else j > 0):
        r = (x > M[i][j]) - (x < M[i][j])
        pasos.append((i, j, r))
        if r == 0:
            break
        if r < 0:
            j -= 1
        else:
            i += 1
    return pasos


def grilla(M, lado, texto, centro):
    n = len(M)
    celdas = [[None] * n for _ in range(n)]
    todo = VGroup()
    for i in range(n):
        for j in range(n):
            cuadro = Square(side_length=lado, stroke_color=APAGADO, stroke_width=2,
                            fill_color=FONDO, fill_opacity=1)
            cuadro.move_to(centro + RIGHT * (j - (n - 1) / 2) * lado +
                           DOWN * (i - (n - 1) / 2) * lado)
            celdas[i][j] = VGroup(cuadro, formula(texto(M[i][j]), tam=26).move_to(cuadro))
            todo.add(celdas[i][j])
    return celdas, todo


class Escalera(Scene):
    def construct(self):
        narr = Narrador()
        M = matriz_al_azar(8, random.Random(6))
        x, n = 32, 8
        self.add(titulo(rf"Búsqueda en escalera de $x = {x}$"))
        celdas, todo = grilla(M, 0.6, str, LEFT * 2.2 + DOWN * 0.2)
        self.play(LaggedStart(*[FadeIn(c) for c in todo], lag_ratio=0.01), *narr.decir(
            r"Filas y columnas crecientes"))
        # Por qué la esquina superior derecha.
        fila0 = SurroundingRectangle(VGroup(*celdas[0]), color=AMARILLO, buff=0.03)
        col = SurroundingRectangle(VGroup(*[celdas[i][n - 1] for i in range(n)]),
                                   color=AMARILLO, buff=0.03)
        self.play(Create(fila0), Create(col), *narr.decir(
            r"La esquina es la mayor de su fila y la menor de su columna"))
        self.wait(1)
        self.play(FadeOut(fila0), FadeOut(col))

        inv = rotulo(r"$x$ no está en las filas de arriba\\ni en las columnas de la derecha",
                     32, VERDE).move_to(RIGHT * 4.2 + UP * 1.9)
        phi = formula(r"\Phi = (n - i) + (j + 1) = ", str(2 * n), tam=36, color=DORADO)
        phi.move_to(RIGHT * 4.2 + UP * 0.4)
        cuenta = formula(r"\text{comparaciones: } 0", tam=36).move_to(RIGHT * 4.2 + DOWN * 0.5)
        self.play(Write(inv), FadeIn(phi), FadeIn(cuenta))
        vivas = {(i, j) for i in range(n) for j in range(n)}
        for k, (i, j, r) in enumerate(escalera(M, x), start=1):
            marco = SurroundingRectangle(celdas[i][j], color=AMARILLO, buff=0.0,
                                         stroke_width=6)
            self.play(Create(marco), Transform(cuenta, formula(
                rf"\text{{comparaciones: }} {k}", tam=36).move_to(cuenta)), run_time=0.4)
            if r == 0:
                self.play(celdas[i][j][0].animate.set_fill(VERDE, 0.5), FadeOut(marco),
                          Flash(celdas[i][j], color=VERDE), *narr.decir(
                              rf"$M[{i}][{j}] = {x}$: encontrado con {k} comparaciones, y "
                              rf"$2n - 1 = {2 * n - 1}$", color=VERDE))
                break
            if r < 0:
                fuera = [(a, j) for a in range(i, n) if (a, j) in vivas]
                ni, nj = i, j - 1
                dicho = (rf"${M[i][j]} > {x}$: toda la columna {j} de aquí para abajo es "
                         r"mayor")
            else:
                fuera = [(i, b) for b in range(0, j + 1) if (i, b) in vivas]
                ni, nj = i + 1, j
                dicho = (rf"${M[i][j]} < {x}$: toda la fila {i} de aquí a la izquierda es "
                         r"menor")
            vivas -= set(fuera)
            self.play(*[celdas[a][b][0].animate.set_fill(VERDE, 0.16) for a, b in fuera],
                      *[celdas[a][b][1].animate.set_opacity(0.35) for a, b in fuera],
                      FadeOut(marco), Transform(phi, formula(
                          r"\Phi = (n - i) + (j + 1) = ", str((n - ni) + (nj + 1)), tam=36,
                          color=DORADO).move_to(phi)),
                      *narr.decir(dicho), run_time=0.8)
        self.wait(2.5)


class Adversario(Scene):
    def construct(self):
        narr = Narrador()
        n = 6
        x = n - 0.5
        A = [[n - 0.75 if i + j == n - 1 else n - 0.25 if i + j == n else i + j
              for j in range(n)] for i in range(n)]

        def texto(v):
            return f"{v:g}".replace(".", "{,}")

        self.add(titulo(r"El adversario: $2n - 1$ celdas donde puede estar $x$"))
        celdas, todo = grilla(A, 0.82, texto, LEFT * 2.6 + DOWN * 0.25)
        ex = formula(rf"x = {texto(x)}", tam=44, color=AMARILLO).move_to(RIGHT * 4.2 +
                                                                       UP * 2.2)
        self.play(FadeIn(todo), Write(ex), *narr.decir(
            r"$M[i][j] = i + j$, salvo dos antidiagonales pegadas a $x$"))
        diag = [(i, j) for i in range(n) for j in range(n) if i + j in (n - 1, n)]
        self.play(*[celdas[i][j][0].animate.set_fill(AZUL, 0.3) for i, j in diag],
                  *narr.decir(rf"${texto(n - 0.75)}$ justo debajo de $x$ y "
                              rf"${texto(n - 0.25)}$ justo encima: cualquiera de las "
                              rf"{len(diag)} puede valer $x$"))
        self.wait(1.2)

        def recorrer(pasos, color):
            camino = VMobject(stroke_color=color, stroke_width=5)
            camino.set_points_as_corners([celdas[i][j].get_center() for i, j, _ in pasos])
            return camino

        bien = escalera(A, x)
        cuenta = formula(rf"\text{{la escalera mira }} {len(bien)}", tam=36, color=VERDE)
        cuenta.move_to(RIGHT * 4.2 + UP * 1.0)
        camino = recorrer(bien, VERDE)
        self.play(Create(camino), FadeIn(cuenta), *narr.decir(
            rf"La escalera las recorre todas en zigzag: {len(bien)} comparaciones $= 2n - 1$"),
            run_time=3)
        self.wait(1)
        self.play(FadeOut(camino))

        mal = escalera(A, x, columna_cero=False)
        vistas = {(i, j) for i, j, _ in mal}
        (fi, fj), = [c for c in diag if c not in vistas]
        cod = rotulo(r"\texttt{while i < n and j > 0}", 32, ROJO).move_to(RIGHT * 4.2 +
                                                                         DOWN * 0.1)
        camino = recorrer(mal, ROJO)
        self.play(FadeIn(cod), Create(camino), *narr.decir(
            rf"Con \texttt{{j > 0}} se detiene antes: mira {len(mal)} y contesta "
            r"``no está''"), run_time=3)
        marco = SurroundingRectangle(celdas[fi][fj], color=ROJO, buff=0.0, stroke_width=6)
        self.play(Create(marco), *narr.decir(rf"Nunca miró la celda $({fi}, {fj})$"))
        self.wait(0.6)
        nuevo = formula(texto(x), tam=26, color=AMARILLO).move_to(celdas[fi][fj])
        vecinos = VGroup(
            SurroundingRectangle(celdas[fi - 1][fj], color=AMARILLO, buff=0.0),
            SurroundingRectangle(celdas[fi][fj + 1], color=AMARILLO, buff=0.0))
        orden = formula(rf"{texto(A[fi - 1][fj])} \le {texto(x)} \le "
                        rf"{texto(A[fi][fj + 1])}", tam=36, color=AMARILLO)
        orden.move_to(RIGHT * 4.2 + DOWN * 1.2)
        self.play(Transform(celdas[fi][fj][1], nuevo),
                  celdas[fi][fj][0].animate.set_fill(ROJO, 0.4), Create(vecinos),
                  Write(orden), *narr.decir(
                      r"El adversario pone $x$ ahí: la matriz sigue ordenada"))
        self.wait(1)
        self.play(FadeOut(vecinos), *narr.decir(
            r"Ninguna respuesta cambió y ahora $x$ sí está: la versión mala se equivoca",
            color=ROJO))
        self.wait(2.5)
