"""Ejercicio 7: la mediana de dos arreglos ordenados. Dos escenas:

    Corte      A[k] se empareja con B[n-1-k]; la pregunta "A[k] <= B[n-1-k]" da primero
               todos sí y después todos no, y la búsqueda binaria encuentra dónde cambia:
               ese corte dice cuántos de los n menores aporta A
    Centinela  cuando un arreglo está entero debajo del otro, el corte cae en un extremo
               y A[-1], que en Python es el último elemento, no hace de -infinito

    uv run --python 3.13 --with manim manim -ql ejercicio-07.py Corte

Los arreglos de la primera escena son los del ejemplo de la sección 2.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import (DOWN, LEFT, RIGHT, UP, Brace, CurvedArrow, Create, FadeIn, FadeOut,
                   Flash, LaggedStart, Line, Scene, Transform, VGroup, Write)

from comun import (AMARILLO, APAGADO, AZUL, GRIS, ROJO, VERDE, Narrador, fila, formula,
                   rotulo, titulo, ventana)

A = [3, 8, 11, 20, 24, 31, 40, 52]
B = [1, 5, 9, 14, 17, 26, 33, 45]


def corte(A, B):
    """La búsqueda binaria de ejercicio-07.py, guardando cada paso."""
    n = len(A)
    lo, hi = 0, n
    pasos = []
    while lo < hi:
        m = (lo + hi) // 2
        si = A[m] <= B[n - 1 - m]
        pasos.append((lo, hi, m, si))
        if si:
            lo = m + 1
        else:
            hi = m
    return lo, pasos


def mediana(A, B, i):
    n = len(A)
    if i == 0:
        return B[n - 1]
    if i == n:
        return A[n - 1]
    return max(A[i - 1], B[n - i - 1])


def mediana_con_menos_uno(A, B, i):
    """El error plantado de la sección 7: confiar en que A[-1] hace de -infinito."""
    n = len(A)
    return max(A[i - 1], B[n - i - 1])


class Corte(Scene):
    def construct(self):
        narr = Narrador()
        self.add(titulo(r"¿Cuántos de los $n$ menores aporta $A$?"))
        n = len(A)
        fa = fila(A, lado=0.85, tam=34).move_to(UP * 1.25 + RIGHT * 0.5)
        fb = fila(B, lado=0.85, tam=34, color=AZUL).move_to(DOWN * 0.95 + RIGHT * 0.5)
        ra = formula("A", tam=44).next_to(fa, LEFT, 0.4)
        rb = formula("B", tam=44, color=AZUL).next_to(fb, LEFT, 0.4)
        self.play(FadeIn(fa), FadeIn(fb), Write(ra), Write(rb), *narr.decir(
            r"Los $n$ menores son un prefijo de cada arreglo: basta saber cuántos aporta $A$"))
        self.wait(1)

        lineas = VGroup(*[Line(fa[k].get_bottom(), fb[n - 1 - k].get_top(), color=APAGADO,
                               stroke_width=2.5) for k in range(n)])
        self.play(LaggedStart(*[Create(l) for l in lineas], lag_ratio=0.12), *narr.decir(
            r"Emparejamos $A[k]$ con $B[n-1-k]$: el de $B$ que saldría si $A$ aportara "
            r"$k+1$"), run_time=2)
        respuestas = VGroup(*[
            rotulo("sí" if A[k] <= B[n - 1 - k] else "no", 30,
                   VERDE if A[k] <= B[n - 1 - k] else ROJO).next_to(fa[k], UP, 0.15)
            for k in range(n)])
        pregunta = formula(r"A[k] \le B[n-1-k]\,?", tam=38, color=AMARILLO)
        pregunta.move_to(UP * 2.45 + LEFT * 3.6)
        self.play(Write(pregunta), LaggedStart(*[FadeIn(r, shift=0.1 * DOWN)
                                                 for r in respuestas], lag_ratio=0.15),
                  *narr.decir(r"$A$ sube y $B$, leído al revés, baja: primero todos sí, "
                              r"después todos no"), run_time=2)
        self.wait(1.5)
        self.play(FadeOut(respuestas), lineas.animate.set_opacity(0.25))

        i, pasos = corte(A, B)
        caja = ventana(fa, 0, n)
        self.play(Create(caja), *narr.decir(r"Ese borde se busca con búsqueda binaria"))
        for lo, hi, m, si in pasos:
            linea = lineas[m]
            signo = r"\le" if si else ">"
            comp = formula(rf"A[{m}] = {A[m]}", signo, rf"{B[n - 1 - m]} = B[{n - 1 - m}]",
                           tam=38, color=VERDE if si else ROJO).move_to(DOWN * 2.35)
            self.play(linea.animate.set_opacity(1).set_color(AMARILLO).set_stroke(width=5),
                      fa[m][0].animate.set_stroke(AMARILLO, 5),
                      fb[n - 1 - m][0].animate.set_stroke(AMARILLO, 5), FadeIn(comp),
                      run_time=0.7)
            nlo, nhi = (m + 1, hi) if si else (lo, m)
            dicho = (r"Sí: el corte está después de $m$" if si else
                     r"No: el corte está en $m$ o antes")
            self.play(Transform(caja, ventana(fa, nlo, nhi)), *narr.decir(dicho),
                      linea.animate.set_opacity(0.25).set_color(APAGADO).set_stroke(width=2.5),
                      fa[m][0].animate.set_stroke(GRIS, 2.5),
                      fb[n - 1 - m][0].animate.set_stroke(AZUL, 2.5), FadeOut(comp),
                      run_time=0.9)
        self.play(FadeOut(caja), FadeOut(lineas))
        menores = [fa[k] for k in range(i)] + [fb[k] for k in range(n - i)]
        llave_a = Brace(VGroup(*fa[:i]), UP, color=VERDE)
        llave_b = Brace(VGroup(*fb[:n - i]), DOWN, color=VERDE)
        ta = formula(rf"i^* = {i}", tam=36, color=VERDE).next_to(llave_a, UP, 0.1)
        tb = formula(rf"n - i^* = {n - i}", tam=36, color=VERDE).next_to(llave_b, DOWN, 0.1)
        self.play(*[c[0].animate.set_fill(VERDE, 0.25) for c in menores], FadeOut(pregunta),
                  FadeIn(llave_a), FadeIn(llave_b), Write(ta), Write(tb), *narr.decir(
                      rf"Los {n} menores: {i} de $A$ y {n - i} de $B$"))
        med = mediana(A, B, i)
        cual = fa[i - 1] if A[i - 1] == med else fb[n - i - 1]
        self.play(Flash(cual, color=AMARILLO, flash_radius=0.6),
                  cual[0].animate.set_stroke(AMARILLO, 6), *narr.decir(
                      rf"La mediana es el mayor de los dos últimos: "
                      rf"$\max({A[i - 1]}, {B[n - i - 1]}) = {med}$, con "
                      rf"{len(pasos) + 1} comparaciones", color=AMARILLO))
        self.wait(2.5)


class Centinela(Scene):
    def construct(self):
        narr = Narrador()
        self.add(titulo(r"El centinela que Python no tiene"))
        A2, B2 = [21, 25, 30, 38], [2, 7, 9, 15]
        fa = fila(A2, lado=0.9, tam=36).move_to(UP * 1.0 + LEFT * 2.6)
        fb = fila(B2, lado=0.9, tam=36, color=AZUL).move_to(DOWN * 0.8 + LEFT * 2.6)
        ra = formula("A", tam=44).next_to(fa, LEFT, 0.4)
        rb = formula("B", tam=44, color=AZUL).next_to(fb, LEFT, 0.4)
        self.play(FadeIn(fa), FadeIn(fb), Write(ra), Write(rb), *narr.decir(
            r"Todo $A$ está por encima de todo $B$"))
        i, _ = corte(A2, B2)
        cod = rotulo(r"\texttt{max(A[i - 1], B[n - i - 1])}", 34).move_to(RIGHT * 3.4 +
                                                                         UP * 1.0)
        val = formula(rf"i^* = {i}", tam=40, color=AMARILLO).next_to(cod, DOWN, 0.4)
        self.play(FadeIn(cod), Write(val), *narr.decir(
            rf"El corte cae en un extremo: $i^* = {i}$, y $A$ no aporta nada"))
        self.wait(0.8)
        flecha = CurvedArrow(fa[0].get_top() + UP * 0.1, fa[-1].get_top() + UP * 0.1,
                             angle=-1.2, color=ROJO)
        idx = formula(r"A[-1]", tam=38, color=ROJO).next_to(flecha, UP, 0.1)
        self.play(Create(flecha), Write(idx), fa[-1][0].animate.set_stroke(ROJO, 6),
                  *narr.decir(r"Pero \texttt{A[-1]} no es $-\infty$: en Python es el "
                              r"último elemento"))
        mal = mediana_con_menos_uno(A2, B2, i)
        bien = mediana(A2, B2, i)
        res = VGroup(formula(rf"\text{{con }} A[-1]: \ {mal}", tam=40, color=ROJO),
                     formula(rf"\text{{la mediana: }} {bien}", tam=40, color=VERDE))
        res.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 3.4 + DOWN * 1.2)
        self.play(FadeIn(res[0], shift=0.1 * UP))
        self.play(FadeIn(res[1], shift=0.1 * UP), fb[-1][0].animate.set_stroke(VERDE, 6))
        self.wait(1)
        m = 10
        base, exp = f"{2 / math.comb(2 * m, m):.2e}".split("e")
        self.play(*narr.decir(
            rf"Al azar, con $n = {m}$, el corte cae en un extremo con probabilidad "
            rf"${base.replace('.', '{,}')} \cdot 10^{{{int(exp)}}}$", color=ROJO))
        self.wait(2.5)
