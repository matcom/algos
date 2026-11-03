"""Ejercicio 9: el merge "optimizado" y la cota inferior del merge. Dos escenas:

    Intercambio  en la entrada intercalada a1 < b1 < ... < a5 < b5, intercambiar dos
                 vecinos que nunca se compararon deja las listas ordenadas y todas las
                 respuestas iguales, pero cambia la salida: hay que comparar los 2n - 1
    Optimizada   el merge optimizado sobre esa entrada: 7 comparaciones, dos pares de
                 vecinos sin comparar, y b5 antes que a5

    uv run --python 3.13 --with manim manim -ql ejercicio-09.py Intercambio
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import (DOWN, LEFT, RIGHT, TEAL_C, UP, ArcBetweenPoints, Create, DashedVMobject,
                   Dot, FadeIn, FadeOut, LaggedStart, Line, Scene, Transform, VGroup, Write)

from comun import (APAGADO, AZUL, GRIS, ROJO, VERDE, Narrador, celda, formula, rotulo,
                   titulo)

N = 5
TEAL = TEAL_C
# La entrada intercalada: a_k = 2k - 1 y b_k = 2k, así que a1 < b1 < a2 < ... < b5.
NOMBRES = [f"{'a' if v % 2 else 'b'}_{(v + 1) // 2}" for v in range(1, 2 * N + 1)]


def color_de(nombre):
    return AZUL if nombre[0] == "a" else TEAL


def optimized_merge(I, D):
    """La de ejercicio-09.py, anotando los pares comparados."""
    R, i, j, comparados = [], 0, 0, []
    while len(I) - i > 1 and j < len(D):
        comparados.append((I[i], D[j]))
        if I[i] <= D[j]:
            R.append(I[i])
            i += 1
        else:
            R.append(D[j])
            j += 1
    if j == len(D):
        return R + I[i:], comparados
    return R + D[j:] + I[i:], comparados


class Recta:
    """Los 2n valores sobre una recta, con sus nombres debajo."""

    def __init__(self, y=0.3):
        self.pos = {v: LEFT * 5.4 + RIGHT * 1.2 * (v - 1) + UP * y
                    for v in range(1, 2 * N + 1)}
        self.linea = Line(LEFT * 6.2 + UP * y, RIGHT * 6.2 + UP * y, color=APAGADO)
        self.puntos = {v: Dot(p, radius=0.11, color=color_de(NOMBRES[v - 1]))
                       for v, p in self.pos.items()}
        self.nombres = {v: formula(NOMBRES[v - 1], tam=34, color=color_de(NOMBRES[v - 1]))
                        .next_to(p, DOWN, 0.25) for v, p in self.pos.items()}

    def todo(self):
        return VGroup(self.linea, *self.puntos.values(), *self.nombres.values())

    def arco(self, u, v, color=APAGADO, ancho=3):
        return ArcBetweenPoints(self.pos[u] + UP * 0.15, self.pos[v] + UP * 0.15,
                                angle=-1.6, color=color, stroke_width=ancho)


def salida(nombres, y):
    f = VGroup(*[celda(n, 0.7, tam=30, color=color_de(n)) for n in nombres])
    return f.arrange(RIGHT, buff=0.05).move_to(UP * y)


class Intercambio(Scene):
    def construct(self):
        narr = Narrador()
        self.add(titulo(r"Por qué el merge cuesta $2n - 1$ comparaciones"))
        r = Recta()
        listas = VGroup(formula(r"I = (a_1, \dots, a_5)", tam=36, color=AZUL),
                        formula(r"D = (b_1, \dots, b_5)", tam=36, color=TEAL))
        listas.arrange(RIGHT, buff=1.2).move_to(UP * 2.35)
        self.play(Create(r.linea), LaggedStart(*[FadeIn(VGroup(r.puntos[v], r.nombres[v]))
                                                 for v in r.pos], lag_ratio=0.08),
                  Write(listas), *narr.decir(
                      r"El adversario contesta como si la entrada fuera la intercalada"))
        arcos = VGroup(*[r.arco(v, v + 1) for v in range(1, 2 * N)])
        cuenta = formula(r"2n - 1 = 9 \text{ pares de vecinos}", tam=36, color=GRIS)
        cuenta.move_to(DOWN * 1.35)
        self.play(LaggedStart(*[Create(a) for a in arcos], lag_ratio=0.1), Write(cuenta),
                  *narr.decir(r"Cada par de vecinos tiene uno de cada lista"), run_time=2)
        self.wait(1)

        u, v = 5, 6                       # a3 y b3
        sin_ver = DashedVMobject(r.arco(u, v, ROJO, 5), num_dashes=12)
        self.play(FadeOut(arcos[u - 1]), Create(sin_ver), *narr.decir(
            rf"Supongamos que un algoritmo termina sin comparar ${NOMBRES[u - 1]}$ con "
            rf"${NOMBRES[v - 1]}$"))
        self.wait(0.8)
        antes = salida([NOMBRES[w - 1] for w in range(1, 2 * N + 1)], -2.2)
        self.play(FadeOut(cuenta), FadeIn(antes), *narr.decir(
            r"La salida correcta para la intercalada"))
        self.wait(0.6)
        # Intercambiar los valores: los dos puntos cambian de lugar.
        self.play(r.puntos[u].animate.move_to(r.pos[v]), r.puntos[v].animate.move_to(r.pos[u]),
                  r.nombres[u].animate.next_to(r.pos[v], DOWN, 0.25),
                  r.nombres[v].animate.next_to(r.pos[u], DOWN, 0.25),
                  *narr.decir(r"Intercambiemos sus valores: $I$ y $D$ siguen ordenadas"),
                  run_time=1.5)
        self.wait(0.6)
        self.play(*narr.decir(r"Ninguna comparación hecha cambia: no tocó a los dos "
                              r"a la vez, y nada queda entre ellos"))
        self.wait(1)
        orden = list(range(1, 2 * N + 1))
        orden[u - 1], orden[v - 1] = orden[v - 1], orden[u - 1]
        despues = salida([NOMBRES[w - 1] for w in orden], -2.2)
        despues[u - 1][0].set_stroke(ROJO, 6)
        despues[v - 1][0].set_stroke(ROJO, 6)
        self.play(Transform(antes, despues), *narr.decir(
            r"Pero la salida correcta sí cambia: con las mismas respuestas, se equivoca "
            r"en una de las dos", color=ROJO))
        self.wait(1.2)
        self.play(*narr.decir(r"Todo algoritmo correcto compara los $2n - 1$ pares",
                              color=VERDE))
        self.wait(2.5)


class Optimizada(Scene):
    def construct(self):
        narr = Narrador()
        self.add(titulo(r"El merge optimizado sobre la entrada del adversario"))
        r = Recta()
        cod = rotulo(r"\texttt{while len(I) - i > 1 and j < len(D)}", 30, ROJO)
        cod.move_to(UP * 2.4)
        self.play(FadeIn(r.todo()), FadeIn(cod), *narr.decir(
            r"Deja de comparar cuando a $I$ le queda un solo elemento"))
        I = list(range(1, 2 * N + 1, 2))
        D = list(range(2, 2 * N + 1, 2))
        res, comparados = optimized_merge(I, D)
        final = salida([NOMBRES[w - 1] for w in res], -1.9)
        cuenta = formula(r"\text{comparaciones: } 0", tam=36).move_to(RIGHT * 4.6 + DOWN * 1.0)
        self.play(FadeIn(cuenta))
        for k, (x, y) in enumerate(comparados, start=1):
            menor = min(x, y)
            self.play(Create(r.arco(menor, max(x, y), VERDE, 4)),
                      Transform(cuenta, formula(rf"\text{{comparaciones: }} {k}", tam=36)
                                .move_to(cuenta)),
                      r.puntos[menor].animate.set_opacity(0.35),
                      FadeIn(final[k - 1], shift=0.2 * DOWN), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(c, shift=0.2 * DOWN) for c in final[len(comparados):]],
                              lag_ratio=0.3), *narr.decir(
            r"Con $a_5$ solo en $I$, pone el resto de $D$ y después $a_5$"))
        self.wait(0.6)
        comparados_set = {(min(x, y), max(x, y)) for x, y in comparados}
        faltan = [(v, v + 1) for v in range(1, 2 * N) if (v, v + 1) not in comparados_set]
        rojos = VGroup(*[DashedVMobject(r.arco(u, v, ROJO, 5), num_dashes=10)
                         for u, v in faltan])
        nombres = ", ".join(rf"$({NOMBRES[u - 1]}, {NOMBRES[v - 1]})$" for u, v in faltan)
        self.play(Create(rojos), *narr.decir(
            rf"{len(comparados)} comparaciones de $2n - 1 = {2 * N - 1}$: nunca miró "
            rf"{nombres}", color=ROJO))
        self.wait(1)
        malos = [k for k, w in enumerate(res) if w != k + 1]
        self.play(*[final[k][0].animate.set_stroke(ROJO, 6) for k in malos], *narr.decir(
            r"Y justo ahí se equivoca: $b_5$ antes que $a_5$, pero $a_5 < b_5$",
            color=ROJO))
        self.wait(2.5)
