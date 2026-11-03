"""Ejercicio 10: el par más cercano en una dimensión, con una rejilla. Tres escenas:

    Rejilla          los puntos se insertan en orden al azar; cada celda de ancho δ tiene a
                     lo sumo un punto, y el punto nuevo consulta su celda y las dos vecinas
    HaciaAtras       fijado el conjunto de los i primeros, el último en llegar es
                     cualquiera de los i: reconstruye solo si es uno de los dos del par más
                     cercano, con probabilidad a lo sumo 2/i
    OrdenAdversario  con huecos n - 1, n - 2, ..., 1 en ese orden, δ baja en cada paso y
                     se reconstruye siempre; permutados, casi nunca

    uv run --python 3.13 --with manim manim -ql ejercicio-10.py Rejilla

El trabajo se cuenta como en la sección 5: 3 consultas por inserción, más lo que
cuesta reconstruir la tabla con los puntos insertados.
"""

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import (DOWN, LEFT, RIGHT, UP, Create, Dot, DoubleArrow, FadeIn, FadeOut, Flash,
                   NumberLine, Rectangle, Scene, SurroundingRectangle, Transform, VGroup,
                   Write)

from comun import (AMARILLO, APAGADO, AZUL, DORADO, GRIS, ROJO, VERDE, Narrador, formula,
                   rotulo, titulo)

PUNTOS = [3, 41, 77, 18, 60, 52, 90, 29, 66, 9, 85, 45]


def insertar_todos(pts):
    """El algoritmo de ejercicio-10.py sobre pts, en ese orden. Devuelve, por cada punto
    desde el tercero, (δ antes, su celda, δ después, si reconstruyó), y el trabajo."""
    d = abs(pts[0] - pts[1])
    pasos, trabajo = [], 0
    for i in range(2, len(pts)):
        p, c = pts[i], pts[i] // d
        mejor = min([d] + [abs(p - q) for q in pts[:i] if q // d in (c - 1, c, c + 1)])
        reconstruye = mejor < d
        trabajo += 3 + (i + 1 if reconstruye else 0)
        pasos.append((d, c, mejor, reconstruye))
        d = mejor
    return pasos, trabajo


class Rejilla(Scene):
    def construct(self):
        narr = Narrador()
        self.add(titulo(r"Celdas de ancho $\delta$: tres consultas por punto"))
        eje = NumberLine(x_range=[0, 100, 10], length=12, color=APAGADO,
                         include_numbers=False).shift(DOWN * 0.3)
        pts = list(PUNTOS)
        random.Random(1).shuffle(pts)
        pasos, _ = insertar_todos(pts)

        def celdas(d, resaltar=()):
            g = VGroup()
            for k in range(0, 100 // d + 1):
                x0 = k * d
                ancho = min(d, 100 - x0)
                if ancho <= 0:
                    break
                r = Rectangle(width=eje.n2p(ancho)[0] - eje.n2p(0)[0], height=0.7,
                              stroke_color=APAGADO, stroke_width=1.5,
                              fill_color=AMARILLO, fill_opacity=0.22 if k in resaltar else 0)
                r.move_to(eje.n2p(x0 + ancho / 2))
                g.add(r)
            return g

        d = abs(pts[0] - pts[1])
        rejilla = celdas(d)
        puntos = VGroup(*[Dot(eje.n2p(p), radius=0.1, color=AZUL) for p in pts[:2]])
        delta = formula(rf"\delta = {d}", tam=44, color=DORADO).move_to(LEFT * 4.6 + UP * 2.2)
        recon = formula(r"\text{reconstrucciones: } 0", tam=36).move_to(RIGHT * 3.8 + UP * 2.2)
        self.play(Create(eje), FadeIn(rejilla), FadeIn(puntos), Write(delta), FadeIn(recon),
                  *narr.decir(rf"Los dos primeros puntos están a {d}: la rejilla tiene "
                              r"celdas de ese ancho"))
        inv = rotulo(r"cada celda tiene a lo sumo un punto", 30, VERDE).move_to(UP * 1.25)
        self.play(FadeIn(inv))
        veces = 0
        for i, (d, c, mejor, reconstruye) in enumerate(pasos, start=2):
            p = pts[i]
            nuevo = Dot(eje.n2p(p), radius=0.12, color=AMARILLO)
            self.play(Transform(rejilla, celdas(d, {c - 1, c, c + 1})), FadeIn(nuevo, scale=2),
                      *narr.decir(rf"Llega {p}: miramos su celda y las dos vecinas"),
                      run_time=0.6)
            if reconstruye:
                q = min(q for q in pts[:i] if abs(p - q) == mejor)
                flecha = DoubleArrow(eje.n2p(min(p, q)) + UP * 0.6,
                                     eje.n2p(max(p, q)) + UP * 0.6, buff=0, color=ROJO,
                                     stroke_width=4, tip_length=0.12)
                dicho = rf"{q} está a {mejor}, menos que $\delta$"
                if p // d != q // d:
                    dicho += r": en la celda de al lado, no en la suya"
                self.play(Create(flecha), *narr.decir(dicho, color=ROJO), run_time=0.6)
                veces += 1
                self.play(Transform(rejilla, celdas(mejor)), FadeOut(flecha),
                          Transform(delta, formula(rf"\delta = {mejor}", tam=44, color=DORADO)
                                    .move_to(delta)),
                          Transform(recon, formula(rf"\text{{reconstrucciones: }} {veces}",
                                                   tam=36).move_to(recon)),
                          Flash(nuevo, color=ROJO), run_time=0.8)
            else:
                self.play(Transform(rejilla, celdas(d)), run_time=0.3)
            self.play(nuevo.animate.set_color(AZUL).scale(0.85), run_time=0.2)
        self.play(*narr.decir(rf"{len(pts)} puntos, {veces} reconstrucciones: el par más "
                              rf"cercano está a {pasos[-1][2]}", color=VERDE))
        self.wait(2.5)


class HaciaAtras(Scene):
    def construct(self):
        narr = Narrador()
        self.add(titulo(r"Análisis hacia atrás: ¿quién llegó último?"))
        conjunto = sorted(PUNTOS[:8])
        i = len(conjunto)
        eje = NumberLine(x_range=[0, 100, 10], length=12, color=APAGADO,
                         include_numbers=False).shift(UP * 0.4)
        puntos = VGroup(*[Dot(eje.n2p(p), radius=0.12, color=AZUL) for p in conjunto])
        nombres = VGroup(*[formula(str(p), tam=28, color=GRIS).next_to(d, DOWN, 0.25)
                           for p, d in zip(conjunto, puntos)])
        self.play(Create(eje), FadeIn(puntos), FadeIn(nombres), *narr.decir(
            rf"Fijemos el conjunto de los $i = {i}$ primeros, sin mirar en qué orden llegaron"))
        _, a, b = min((abs(a - b), a, b) for k, a in enumerate(conjunto)
                      for b in conjunto[k + 1:])
        par = [conjunto.index(a), conjunto.index(b)]
        self.play(*[puntos[k].animate.set_color(DORADO).scale(1.3) for k in par],
                  *narr.decir(rf"Su par más cercano, {a} y {b}, lo decide el conjunto"))
        self.wait(0.8)
        regla = rotulo(r"el paso $i$ reconstruye solo si el último en llegar es uno de los "
                       r"dos", 32, AMARILLO).move_to(UP * 2.3)
        self.play(FadeIn(regla))
        rng = random.Random(4)
        marca = None
        for _ in range(8):
            k = rng.randrange(i)
            sel = SurroundingRectangle(VGroup(puntos[k], nombres[k]), color=AMARILLO,
                                       buff=0.12)
            self.play(Transform(marca, sel) if marca else Create(sel), run_time=0.35)
            marca = marca or sel
            reconstruye = k in par
            color = ROJO if reconstruye else VERDE
            self.play(marca.animate.set_color(color), *narr.decir(
                rf"Llegó último {conjunto[k]}: "
                + ("reconstruye" if reconstruye else "no reconstruye"), color=color),
                run_time=0.35)
        self.play(FadeOut(marca))
        cuenta = formula(r"\Pr[\text{reconstruir en el paso } i] \le \frac{2}{i}", tam=44,
                         color=AMARILLO).move_to(DOWN * 1.35)
        self.play(Write(cuenta), *narr.decir(
            rf"Con orden uniforme, cada uno de los {i} es el último con la misma probabilidad"))
        self.wait(1)
        total = formula(r"\mathbb{E}[\text{trabajo}] \le \sum_i \Big(3 + \frac{2}{i}\cdot i"
                        r"\Big) = O(n)", tam=44, color=VERDE).move_to(DOWN * 2.35)
        self.play(Write(total), *narr.decir(r"Reconstruir cuesta $i$, pero pasa con "
                                            r"probabilidad $2/i$: en esperanza, 2 por paso"))
        self.wait(2.5)


class OrdenAdversario(Scene):
    def construct(self):
        narr = Narrador()
        self.add(titulo(r"Sin el azar: un orden que reconstruye siempre"))
        n = 8
        pts = [0]
        for hueco in range(n - 1, 0, -1):
            pts.append(pts[-1] + hueco)
        eje = NumberLine(x_range=[0, pts[-1], 1], length=11, color=APAGADO,
                         include_numbers=False, include_ticks=False).shift(UP * 0.6)
        huecos = VGroup(*[formula(str(pts[k + 1] - pts[k]), tam=28, color=GRIS)
                          .move_to((eje.n2p(pts[k]) + eje.n2p(pts[k + 1])) / 2 + UP * 0.45)
                          for k in range(n - 1)])
        self.play(Create(eje), FadeIn(huecos), *narr.decir(
            rf"Huecos de {n - 1}, {n - 2}, \dots, 1, insertados en ese orden"))
        pasos, trabajo = insertar_todos(pts)
        self.play(*[FadeIn(Dot(eje.n2p(p), radius=0.12, color=AZUL)) for p in pts[:2]])
        acumulado = 0
        cuenta = formula(r"\text{trabajo: } 0", tam=40).move_to(LEFT * 3.4 + DOWN * 1.2)
        self.play(FadeIn(cuenta))
        for i, (d, _, mejor, reconstruye) in enumerate(pasos, start=2):
            acumulado += 3 + (i + 1 if reconstruye else 0)
            nuevo = Dot(eje.n2p(pts[i]), radius=0.12, color=ROJO if reconstruye else AZUL)
            dicho = (rf"$\delta$ baja de {d} a {mejor}: reconstruir con los {i + 1}"
                     if reconstruye else r"$\delta$ no cambia")
            self.play(FadeIn(nuevo, scale=2), Transform(cuenta, formula(
                rf"\text{{trabajo: }} {acumulado}", tam=40).move_to(cuenta)),
                *narr.decir(dicho), run_time=0.6)
        orden = list(pts)
        random.Random(1).shuffle(orden)
        _, trabajo_azar = insertar_todos(orden)
        comparacion = VGroup(
            formula(rf"\text{{en este orden: }} {trabajo}", tam=40, color=ROJO),
            formula(rf"\text{{permutados al azar: }} {trabajo_azar}", tam=40, color=VERDE))
        comparacion.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 2.6 +
                                                                       DOWN * 1.5)
        self.play(FadeIn(comparacion, shift=0.1 * UP), *narr.decir(
            r"Cada paso reconstruye: $\sum i = \Theta(n^2)$. El azar es lo que lo evita"))
        self.wait(2.5)
