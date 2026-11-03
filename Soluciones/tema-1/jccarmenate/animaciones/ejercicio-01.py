"""Ejercicio 1: qué compra una máquina mil veces más rápida.

    Factor  en escala logarítmica, mil veces más presupuesto sube la raya tres décadas.
            Con n^2 el tamaño avanza siempre 3/2 de década (por raíz de 1000), esté
            donde esté; con n log n el avance depende de dónde se empieza

    uv run --python 3.13 --with manim manim -ql ejercicio-01.py Factor

El barrido empieza en el ejemplo de la sección 2 (n0 = 1024 con n log2 n) y termina en
el escenario de una hora a 10^9 operaciones por segundo de la sección 4.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import (DOWN, LEFT, RIGHT, TEAL_C, UP, Arrow, Axes, Create, DashedLine,
                   DecimalNumber, DoubleArrow, Dot, FadeIn, Scene, ValueTracker, VGroup,
                   Write, always_redraw, smooth)

from comun import AMARILLO, AZUL, GRIS, Narrador, formula, rotulo, titulo

TEAL = TEAL_C


def log10_nlogn(x):
    """log10 de n log2 n, con n = 10^x."""
    return x + math.log10(x * math.log2(10))


def corte_nlogn(y):
    """El x con log10(n log2 n) = y: el tamaño, en décadas, que cabe en 10^y."""
    lo, hi = 0.3, 30.0
    for _ in range(80):
        medio = (lo + hi) / 2
        if log10_nlogn(medio) < y:
            lo = medio
        else:
            hi = medio
    return (lo + hi) / 2


class Factor(Scene):
    def construct(self):
        narr = Narrador()
        self.add(titulo(r"Mil veces más operaciones: ¿cuánto más grande es $n$?"))
        ejes = Axes(x_range=[0, 22, 1], y_range=[0, 24, 2], x_length=8.4, y_length=4.7,
                    tips=False, axis_config={"color": GRIS, "stroke_width": 2,
                                             "include_ticks": False})
        ejes.move_to(LEFT * 1.9 + UP * 0.05)
        marcas = VGroup()
        for x in (0, 5, 10, 15, 20):
            marcas.add(formula(f"10^{{{x}}}", tam=26, color=GRIS)
                       .next_to(ejes.c2p(x, 0), DOWN, 0.15))
        for y in (6, 12, 18, 24):
            marcas.add(formula(f"10^{{{y}}}", tam=26, color=GRIS)
                       .next_to(ejes.c2p(0, y), LEFT, 0.15))
        marcas.add(formula("n", tam=34, color=GRIS).next_to(ejes.c2p(22, 0), RIGHT, 0.15))
        marcas.add(rotulo("operaciones", 28, GRIS).next_to(ejes.c2p(0, 24), RIGHT, 0.2))
        cuad = ejes.plot(lambda x: 2 * x, x_range=[0, 12], color=AZUL, stroke_width=4)
        nlog = ejes.plot(log10_nlogn, x_range=[0.5, 22], color=TEAL, stroke_width=4)
        rot_c = formula("n^2", tam=40, color=AZUL).next_to(ejes.c2p(12, 24), RIGHT, 0.15)
        rot_n = formula(r"n \log_2 n", tam=40, color=TEAL)
        rot_n.next_to(ejes.c2p(19, log10_nlogn(19)), UP + LEFT, 0.1)
        self.play(Create(ejes), FadeIn(marcas), *narr.decir(
            r"Los dos ejes en escala logarítmica: cada marca es un factor 10"))
        self.play(Create(cuad), Create(nlog), Write(rot_c), Write(rot_n), *narr.decir(
            r"$n^2$ es una recta de pendiente 2; $n \log n$ casi una de pendiente 1"),
            run_time=1.8)
        self.wait(0.8)

        T = ValueTracker(math.log10(1024 * 10))

        def rayas():
            t = T.get_value()
            hoy = DashedLine(ejes.c2p(0, t), ejes.c2p(22, t), color=GRIS, stroke_width=2)
            mil = DashedLine(ejes.c2p(0, t + 3), ejes.c2p(22, t + 3), color=AMARILLO,
                             stroke_width=2.5)
            salto = DoubleArrow(ejes.c2p(21.3, t), ejes.c2p(21.3, t + 3), buff=0,
                                color=AMARILLO, stroke_width=3, tip_length=0.14)
            rot = formula(r"\times 1000", tam=30, color=AMARILLO).next_to(salto, RIGHT, 0.1)
            return VGroup(hoy, mil, salto, rot)

        def flecha(x0, x1, y, color):
            return VGroup(
                DashedLine(ejes.c2p(x0, y - 3), ejes.c2p(x0, y), color=color,
                           stroke_width=2, dash_length=0.06),
                Arrow(ejes.c2p(x0, y), ejes.c2p(x1, y), buff=0, color=color,
                      stroke_width=6, tip_length=0.16, max_tip_length_to_length_ratio=0.6),
                Dot(ejes.c2p(x0, y - 3), radius=0.07, color=color),
                Dot(ejes.c2p(x1, y), radius=0.07, color=color))

        presupuesto = always_redraw(rayas)
        self.play(FadeIn(presupuesto), *narr.decir(
            r"Gris, lo que alcanza hoy; amarillo, mil veces más: tres décadas más arriba"))
        self.wait(0.8)

        def flecha_cuad():
            t = T.get_value()
            return flecha(t / 2, (t + 3) / 2, t + 3, AZUL)

        def flecha_nlog():
            t = T.get_value()
            return flecha(corte_nlogn(t), corte_nlogn(t + 3), t + 3, TEAL)

        f_c, f_n = always_redraw(flecha_cuad), always_redraw(flecha_nlog)
        panel_c = formula(r"n^2:", r"\ \times", r"\,31.6", tam=44, color=AZUL)
        panel_n = formula(r"n \log n:", r"\ \times", tam=44, color=TEAL)
        panel = VGroup(panel_c, panel_n).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        panel.move_to(RIGHT * 4.6 + UP * 1.2)
        k = DecimalNumber(0, num_decimal_places=1, font_size=44, color=TEAL)
        k.add_updater(lambda m: m.set_value(
            10 ** (corte_nlogn(T.get_value() + 3) - corte_nlogn(T.get_value()))))
        k.add_updater(lambda m: m.next_to(panel_n, RIGHT, 0.12))
        k.update()
        self.play(Create(f_c), Create(f_n), FadeIn(panel), FadeIn(k), *narr.decir(
            r"Cada flecha va del $n$ de hoy al de mañana; su largo, en décadas, es el "
            r"factor"))
        self.wait(1.2)
        self.play(*narr.decir(r"Empezamos en el ejemplo de la sección 2: $n_0 = 1024$ "
                              r"con $n \log_2 n$"))
        self.wait(1.2)
        self.play(T.animate.set_value(20), *narr.decir(
            r"Con $n^2$ la flecha mide siempre $3/2$ de década: $\times \sqrt{1000}$, "
            r"esté donde esté"), run_time=6, rate_func=smooth)
        self.wait(0.8)
        hora = math.log10(3600 * 10 ** 9)
        self.play(T.animate.set_value(hora), *narr.decir(
            r"Con $n \log n$ el factor depende de dónde se empieza, y se acerca a mil "
            r"muy despacio"), run_time=3, rate_func=smooth)
        self.wait(0.6)
        self.play(*narr.decir(r"Una hora a $10^9$ operaciones por segundo: "
                              r"$\times 791$, no $\times 1000$", color=TEAL))
        self.wait(2.5)
