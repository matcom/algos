"""Ejercicio 14: el punto de rotación de un arreglo ordenado y rotado. Tres escenas:

    PrimerSi        el arreglo no está ordenado, pero la fila de respuestas a
                    "A[i] <= A[n-1]" sí: primero no, después sí; la búsqueda binaria
                    encuentra el primer sí
    Adversario      cada comparación pregunta si k está en un intervalo; el adversario
                    contesta lo que deja más rotaciones vivas: la búsqueda binaria
                    necesita 4 = ceil(log2 12), la fuerza bruta 11
    ReferenciaCero  con el arreglo sin rotar, comparar con A[0] no tiene ninguna
                    posición con respuesta sí, y la búsqueda termina en n - 1

    uv run --python 3.13 --with manim manim -ql ejercicio-14.py PrimerSi

Los arreglos son los del ejemplo de la sección 2 y el de la sección 10.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import (DOWN, LEFT, ORANGE, RIGHT, UP, Create, DashedLine, Dot, FadeIn, FadeOut,
                   Flash, LaggedStart, Rectangle, Scene, Transform, VGroup, Write)

from comun import (AMARILLO, APAGADO, AZUL, GRIS, ROJO, VERDE, Narrador, formula, rotulo,
                   titulo)

A = [27, 31, 40, 46, 53, 61, 70, 3, 8, 11, 15, 22]
SIN_ROTAR = sorted(A)
BASE, ESCALA, ANCHO = -1.9, 0.05, 0.62


def punto_de_rotacion(A):
    """La búsqueda de ejercicio-14.py, guardando cada paso (lo, hi, m, sí)."""
    n = len(A)
    lo, hi = 0, n - 1
    pasos = []
    while lo < hi:
        m = (lo + hi) // 2
        si = not A[m] > A[n - 1]
        pasos.append((lo, hi, m, si))
        if si:
            hi = m
        else:
            lo = m + 1
    return lo, pasos


def con_referencia_cero(A):
    """El error plantado de la sección 10: comparar con A[0] en vez de A[n-1]."""
    n = len(A)
    lo, hi = 0, n - 1
    pasos = []
    while lo < hi:
        m = (lo + hi) // 2
        si = A[0] > A[m]
        pasos.append((lo, hi, m, si))
        if si:
            hi = m
        else:
            lo = m + 1
    return lo, pasos


def x_de(i, n):
    return (i - (n - 1) / 2) * 0.82 + 0.4


def barras(valores, k):
    """Una barra por elemento: el tramo alto (antes de k) en naranja, el bajo en azul."""
    n = len(valores)
    g = VGroup()
    for i, v in enumerate(valores):
        b = Rectangle(width=ANCHO, height=v * ESCALA, stroke_width=0,
                      fill_color=ORANGE if i < k else AZUL, fill_opacity=0.8)
        b.move_to(RIGHT * x_de(i, n) + UP * BASE, aligned_edge=DOWN)
        etiqueta = formula(str(v), tam=26).next_to(b, UP, 0.08)
        indice = formula(str(i), tam=22, color=APAGADO).move_to(RIGHT * x_de(i, n) +
                                                                UP * (BASE - 0.25))
        g.add(VGroup(b, etiqueta, indice))
    return g


def raya(valores, i, color, texto):
    n = len(valores)
    y = BASE + valores[i] * ESCALA
    linea = DashedLine(RIGHT * (x_de(0, n) - 0.5) + UP * y,
                       RIGHT * (x_de(n - 1, n) + 0.5) + UP * y, color=color)
    return VGroup(linea, formula(texto, tam=30, color=color).next_to(linea, LEFT, 0.15))


def marco(g, lo, hi, color=AZUL):
    n = len(g)
    izq, der = x_de(lo, n) - ANCHO / 2 - 0.08, x_de(hi, n) + ANCHO / 2 + 0.08
    r = Rectangle(width=der - izq, height=4.3, stroke_color=color, stroke_width=4)
    return r.move_to(RIGHT * (izq + der) / 2 + UP * (BASE + 1.95))


def respuestas(valores, si_de, y=2.45):
    n = len(valores)
    return VGroup(*[rotulo("sí" if si_de(i) else "no", 26, VERDE if si_de(i) else ROJO)
                    .move_to(RIGHT * x_de(i, n) + UP * y) for i in range(n)])


class PrimerSi(Scene):
    def construct(self):
        narr = Narrador()
        n = len(A)
        k, pasos = punto_de_rotacion(A)
        self.add(titulo(r"El arreglo no está ordenado; las respuestas, sí"))
        g = barras(A, k)
        self.play(LaggedStart(*[FadeIn(b, shift=0.2 * UP) for b in g], lag_ratio=0.05),
                  *narr.decir(r"Un arreglo ordenado y rotado: dos tramos crecientes"))
        ref = raya(A, n - 1, AMARILLO, r"A[n-1]")
        self.play(Create(ref), *narr.decir(r"Comparemos cada elemento con el último"))
        resp = respuestas(A, lambda i: A[i] <= A[n - 1])
        self.play(LaggedStart(*[FadeIn(r, shift=0.1 * DOWN) for r in resp], lag_ratio=0.1),
                  *narr.decir(r"$A[i] \le A[n-1]$: no en el tramo alto, sí en el bajo"),
                  run_time=1.8)
        self.wait(1.2)
        caja = marco(g, 0, n - 1)
        self.play(Create(caja), *narr.decir(r"$k$ es el primer sí: búsqueda binaria"))
        for lo, hi, m, si in pasos:
            barra = g[m][0]
            self.play(barra.animate.set_fill(AMARILLO, 1), run_time=0.4)
            nlo, nhi = (lo, m) if si else (m + 1, hi)
            dicho = (rf"$A[{m}] = {A[m]} \le {A[n - 1]}$: $k$ está en {m} o antes" if si else
                     rf"$A[{m}] = {A[m]} > {A[n - 1]}$: $k$ está después de {m}")
            self.play(Transform(caja, marco(g, nlo, nhi)),
                      barra.animate.set_fill(ORANGE if m < k else AZUL, 0.8),
                      *narr.decir(dicho), run_time=0.9)
        self.play(Flash(g[k][0], color=VERDE, flash_radius=0.5),
                  g[k][0].animate.set_fill(VERDE, 1),
                  *narr.decir(rf"$k = {k}$ con {len(pasos)} comparaciones: "
                              rf"$\lceil \log_2 {n} \rceil = {len(pasos)}$", color=VERDE))
        self.wait(2.5)


class Adversario(Scene):
    def construct(self):
        narr = Narrador()
        n = len(A)
        self.add(titulo(r"El adversario se queda con la mitad más grande"))
        puntos = VGroup(*[Dot(radius=0.14, color=AZUL) for _ in range(n)])
        puntos.arrange(RIGHT, buff=0.55).move_to(UP * 0.9)
        nombres = VGroup(*[formula(str(k), tam=28, color=GRIS).next_to(p, DOWN, 0.2)
                           for k, p in enumerate(puntos)])
        rot = rotulo(r"rotaciones posibles: $k = 0, \dots, n-1$", 32).move_to(UP * 2.3)
        self.play(FadeIn(puntos), FadeIn(nombres), FadeIn(rot), *narr.decir(
            r"Comparar $A[m]$ con $A[n-1]$ pregunta: ¿es $k > m$?"))
        cuenta = formula(r"\text{preguntas: } 0", tam=36).move_to(DOWN * 1.2 + LEFT * 3.2)
        vivas_txt = formula(rf"\text{{vivas: }} {n}", tam=36).move_to(DOWN * 1.2 + RIGHT * 3.2)
        self.play(FadeIn(cuenta), FadeIn(vivas_txt))
        vivas = set(range(n))
        lo, hi, c = 0, n - 1, 0
        while len(vivas) > 1:
            m = (lo + hi) // 2
            mayores = {k for k in vivas if k > m}
            resto = vivas - mayores
            quedan = mayores if len(mayores) >= len(resto) else resto
            muertas = vivas - quedan
            c += 1
            if quedan is mayores:
                lo = m + 1
                dicho = rf"¿$k > {m}$? Sí: deja {len(quedan)} vivas"
            else:
                hi = m
                dicho = rf"¿$k > {m}$? No: deja {len(quedan)} vivas"
            vivas = quedan
            self.play(*[puntos[k].animate.set_color(APAGADO).set_opacity(0.4) for k in muertas],
                      Transform(cuenta, formula(rf"\text{{preguntas: }} {c}", tam=36)
                                .move_to(cuenta)),
                      Transform(vivas_txt, formula(rf"\text{{vivas: }} {len(vivas)}", tam=36)
                                .move_to(vivas_txt)),
                      *narr.decir(dicho), run_time=0.9)
            self.wait(0.4)
        self.play(*narr.decir(rf"La búsqueda binaria necesita {c} preguntas contra el "
                              rf"adversario: $\lceil \log_2 {n} \rceil$", color=VERDE))
        self.wait(1.2)

        # La fuerza bruta pregunta por una sola rotación a la vez.
        self.play(*[p.animate.set_color(AZUL).set_opacity(1) for p in puntos],
                  Transform(cuenta, formula(r"\text{preguntas: } 0", tam=36).move_to(cuenta)),
                  Transform(vivas_txt, formula(rf"\text{{vivas: }} {n}", tam=36)
                            .move_to(vivas_txt)),
                  *narr.decir(r"La fuerza bruta pregunta ¿$A[i] > A[i+1]$?, es decir, "
                              r"¿$k = i + 1$?"))
        vivas = set(range(n))
        c = 0
        for i in range(n - 1):
            c += 1
            vivas.discard(i + 1)
            self.play(puntos[i + 1].animate.set_color(APAGADO).set_opacity(0.4),
                      Transform(cuenta, formula(rf"\text{{preguntas: }} {c}", tam=36)
                                .move_to(cuenta)),
                      Transform(vivas_txt, formula(rf"\text{{vivas: }} {len(vivas)}", tam=36)
                                .move_to(vivas_txt)), run_time=0.3)
        self.play(*narr.decir(rf"El adversario contesta siempre que no: {c} preguntas, "
                              r"$n - 1$", color=ROJO))
        self.wait(1)
        cota = formula(r"\text{tras } c \text{ preguntas quedan} \ge n / 2^c",
                       r"\;\Rightarrow\;", r"c \ge \lceil \log_2 n \rceil", tam=40,
                       color=AMARILLO).move_to(DOWN * 2.3)
        self.play(Write(cota))
        self.wait(2.5)


class ReferenciaCero(Scene):
    def construct(self):
        narr = Narrador()
        n = len(SIN_ROTAR)
        self.add(titulo(r"El arreglo sin rotar: $k = 0$"))
        g = barras(SIN_ROTAR, 0)
        self.play(FadeIn(g), *narr.decir(r"Sin rotar, el tramo alto está vacío"))
        casos = ((r"A[0]", 0, lambda i: SIN_ROTAR[i] < SIN_ROTAR[0], con_referencia_cero,
                  ROJO),
                 (r"A[n-1]", n - 1, lambda i: SIN_ROTAR[i] <= SIN_ROTAR[n - 1],
                  punto_de_rotacion, VERDE))
        for nombre, ref, si_de, buscar, color in casos:
            linea = raya(SIN_ROTAR, ref, AMARILLO, nombre)
            resp = respuestas(SIN_ROTAR, si_de)
            dicho = ("ninguna posición contesta sí" if color == ROJO else
                     "todas contestan sí")
            self.play(Create(linea), LaggedStart(*[FadeIn(r) for r in resp], lag_ratio=0.06),
                      *narr.decir(rf"Con referencia ${nombre}$: {dicho}"), run_time=1.5)
            self.wait(0.8)
            k, pasos = buscar(SIN_ROTAR)
            caja = marco(g, 0, n - 1, color=color)
            self.play(Create(caja))
            for lo, hi, m, si in pasos:
                nlo, nhi = (lo, m) if si else (m + 1, hi)
                self.play(Transform(caja, marco(g, nlo, nhi, color=color)), run_time=0.5)
            if color == ROJO:
                dicho = (rf"Devuelve {k}: la inicialización de (I) necesita una posición "
                         r"con sí, y no la hay")
            else:
                dicho = rf"Devuelve {k}: la posición $n-1$ siempre contesta sí"
            self.play(Flash(g[k][0], color=color, flash_radius=0.5),
                      *narr.decir(dicho, color=color))
            self.wait(1.5)
            self.play(FadeOut(linea), FadeOut(resp), FadeOut(caja))
        self.play(*narr.decir(r"El único caso que falla es $k = 0$: el que el azar casi "
                              r"no genera", color=ROJO))
        self.wait(2.5)
