"""Ejercicio 12: Gale-Shapley con listas incompletas. Dos escenas:

    Propuestas   la instancia de la sección 2, propuesta por propuesta: cada proponente
                 recorre su lista, los rechazos se tachan, a2 agota la suya y se queda
                 solo, y a b3 no lo lista nadie
    Verificador  el error de rendirse una propuesta antes: sus dos parejas bloqueantes
                 tienen un proponente solo, así que un verificador con la definición de
                 listas completas no ve ninguna

    uv run --python 3.13 --with manim manim -ql ejercicio-12.py Propuestas
"""

import sys
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import (DOWN, LEFT, RIGHT, UP, Arrow, Circle, Create, DashedLine, FadeIn,
                   FadeOut, Flash, Line, Scene, VGroup)

from comun import (AMARILLO, APAGADO, AZUL, GRIS, ROJO, VERDE, Narrador, formula, rotulo,
                   titulo)

PREF_A = [[3, 1], [0, 1], [0, 3], [0, 3]]
PREF_B = [[2, 0, 1, 3], [0, 3, 1, 2], [1, 2, 3, 0], [3, 0, 2, 1]]
YS = [1.55, 0.5, -0.55, -1.6]


def gale_shapley(pref_a, pref_b, uno_antes=False):
    """La versión de ejercicio-12.py (con cola), guardando cada propuesta. Con
    uno_antes = True es el error de la sección 7."""
    rank = [{a: i for i, a in enumerate(pref_b[b])} for b in range(len(pref_b))]
    next_choice = [0] * len(pref_a)
    match_of_b = [None] * len(pref_b)
    corte = 1 if uno_antes else 0

    def has_more(a):
        return next_choice[a] < len(pref_a[a]) - corte

    free = deque(a for a in range(len(pref_a)) if has_more(a))
    traza = []
    while free:
        a = free.popleft()
        lugar = next_choice[a]
        b = pref_a[a][lugar]
        next_choice[a] += 1
        current = match_of_b[b]
        if current is None:
            match_of_b[b], rejected = a, None
        elif rank[b][a] < rank[b][current]:
            match_of_b[b], rejected = a, current
        else:
            rejected = a
        solo = rejected is not None and not has_more(rejected)
        traza.append((a, lugar, b, current, match_of_b[b], rejected, solo))
        if rejected is not None and has_more(rejected):
            free.append(rejected)
    M = [None] * len(pref_a)
    for b, a in enumerate(match_of_b):
        if a is not None:
            M[a] = b
    return M, traza


def bloqueantes(M, pref_a, pref_b, vieja=False):
    """Las parejas bloqueantes de M. Con vieja = True, la definición de listas
    completas: solo mira pares en los que los dos tienen pareja."""
    match_of_b = {b: a for a, b in enumerate(M) if b is not None}
    res = []
    for a in range(len(pref_a)):
        for b in pref_a[a]:
            if M[a] == b:
                continue
            otro = match_of_b.get(b)
            if vieja and (M[a] is None or otro is None):
                continue
            quiere_a = M[a] is None or pref_a[a].index(b) < pref_a[a].index(M[a])
            quiere_b = otro is None or pref_b[b].index(a) < pref_b[b].index(otro)
            if quiere_a and quiere_b:
                res.append((a, b))
    return res


class Instancia:
    def __init__(self):
        self.A = [self.agente(f"a_{i + 1}", AZUL, -1.7, YS[i]) for i in range(4)]
        self.B = [self.agente(f"b_{i + 1}", GRIS, 1.7, YS[i]) for i in range(4)]
        self.listas = []
        for i, pref in enumerate(PREF_A):
            items = VGroup()
            for k, b in enumerate(pref):
                if k:
                    items.add(formula(">", tam=30, color=APAGADO))
                items.add(formula(f"b_{b + 1}", tam=30))
            items.arrange(RIGHT, buff=0.15).next_to(self.A[i], LEFT, 0.4)
            self.listas.append(items)
        self.listas_b = [formula(" > ".join(f"a_{x + 1}" for x in PREF_B[i]), tam=28,
                                 color=GRIS).next_to(self.B[i], RIGHT, 0.4)
                         for i in range(4)]
        self.grises = VGroup(*[self.linea(a, b, APAGADO, 2) for a in range(4)
                               for b in PREF_A[a]])

    @staticmethod
    def agente(nombre, color, x, y):
        c = Circle(radius=0.32, stroke_color=color, stroke_width=3).move_to([x, y, 0])
        return VGroup(c, formula(nombre, tam=30).move_to(c))

    def item(self, a, lugar):
        return self.listas[a][2 * lugar]

    def linea(self, a, b, color, ancho):
        return Line(self.A[a][0].get_right(), self.B[b][0].get_left(), color=color,
                    stroke_width=ancho)

    def todo(self):
        return VGroup(self.grises, *self.A, *self.B, *self.listas, *self.listas_b)


class Propuestas(Scene):
    def construct(self):
        narr = Narrador()
        self.add(titulo(r"Gale-Shapley con listas incompletas"))
        ins = Instancia()
        self.play(FadeIn(ins.todo()), *narr.decir(
            r"Cada proponente lista solo a los receptores que acepta"))
        self.wait(1)
        M, traza = gale_shapley(PREF_A, PREF_B)
        juntos = {}
        for a, lugar, b, antes, despues, rejected, solo in traza:
            item = ins.item(a, lugar)
            flecha = Arrow(ins.A[a][0].get_right(), ins.B[b][0].get_left(), buff=0.05,
                           color=AMARILLO, stroke_width=5, tip_length=0.18)
            self.play(item.animate.set_color(AMARILLO), FadeIn(flecha), *narr.decir(
                rf"$a_{a + 1}$ le propone a $b_{b + 1}$, el siguiente de su lista"),
                run_time=0.6)
            anims = [FadeOut(flecha)]
            if despues == a:
                if b in juntos:
                    anims.append(FadeOut(juntos[b]))
                juntos[b] = ins.linea(a, b, AZUL, 6)
                anims += [Create(juntos[b]), item.animate.set_color("#ffffff")]
                dicho = (rf"$b_{b + 1}$ estaba libre: acepta" if antes is None else
                         rf"$b_{b + 1}$ prefiere $a_{a + 1}$ a $a_{antes + 1}$: lo cambia")
            else:
                dicho = rf"$b_{b + 1}$ prefiere a $a_{antes + 1}$: rechaza a $a_{a + 1}$"
                anims.append(Flash(ins.B[b][0], color=ROJO, flash_radius=0.45))
            if rejected is not None:
                tachar = ins.item(rejected, PREF_A[rejected].index(b))
                anims.append(tachar.animate.set_color(ROJO).set_opacity(0.45))
            self.play(*anims, *narr.decir(dicho), run_time=0.8)
            if solo:
                self.play(ins.A[rejected][0].animate.set_stroke(APAGADO, 3),
                          ins.A[rejected][1].animate.set_color(APAGADO),
                          *narr.decir(rf"$a_{rejected + 1}$ agotó su lista: "
                                      r"\texttt{has\_more} es falso y se queda solo",
                                      color=AMARILLO))
                self.wait(0.8)
        sin_pareja = [b for b in range(4) if b not in M]
        self.play(*[ins.B[b][0].animate.set_stroke(APAGADO) for b in sin_pareja],
                  *narr.decir(r"A $b_3$ no lo lista nadie: también queda solo"))
        self.wait(0.8)
        n_bloq = len(bloqueantes(M, PREF_A, PREF_B))
        self.play(*narr.decir(rf"Parejas bloqueantes: {n_bloq}. Es el único emparejamiento "
                              r"estable de la instancia", color=VERDE))
        self.wait(2.5)


class Verificador(Scene):
    def construct(self):
        narr = Narrador()
        self.add(titulo(r"El error de rendirse una propuesta antes"))
        ins = Instancia()
        cod = rotulo(r"\texttt{next\_choice[a] < len(pref\_a[a]) - 1}", 30, ROJO)
        cod.move_to(UP * 2.45)
        self.play(FadeIn(ins.todo()), FadeIn(cod), *narr.decir(
            r"El proponente se rinde sin probar al último de su lista"))
        malo, _ = gale_shapley(PREF_A, PREF_B, uno_antes=True)
        lineas = [ins.linea(a, b, AZUL, 6) for a, b in enumerate(malo) if b is not None]
        solos = [a for a in range(4) if malo[a] is None]
        self.play(*[Create(l) for l in lineas],
                  *[ins.A[a][0].animate.set_stroke(APAGADO, 3) for a in solos],
                  *[ins.A[a][1].animate.set_color(APAGADO) for a in solos],
                  *narr.decir(r"El resultado: " + ", ".join(
                      rf"$a_{a + 1}$--$b_{b + 1}$" if b is not None else rf"$a_{a + 1}$ solo"
                      for a, b in enumerate(malo))))
        self.wait(1)
        vieja = bloqueantes(malo, PREF_A, PREF_B, vieja=True)
        nueva = bloqueantes(malo, PREF_A, PREF_B)
        caja_v = rotulo(rf"definición vieja: {len(vieja)} bloqueantes", 32, VERDE)
        caja_v.move_to(DOWN * 2.45 + LEFT * 3.4)
        self.play(FadeIn(caja_v), *narr.decir(
            r"Un verificador copiado de listas completas solo mira pares con los dos "
            r"emparejados"))
        self.wait(1)
        rayas = [DashedLine(ins.A[a][0].get_right(), ins.B[b][0].get_left(), color=ROJO,
                            stroke_width=5) for a, b in nueva]
        caja_n = rotulo(rf"definición nueva: {len(nueva)} bloqueantes", 32, ROJO)
        caja_n.move_to(DOWN * 2.45 + RIGHT * 3.4)
        pares = ", ".join(rf"$(a_{a + 1}, b_{b + 1})$" for a, b in nueva)
        self.play(*[Create(r) for r in rayas], FadeIn(caja_n), *narr.decir(
            rf"Con ``$a$ está solo'' en la definición: {pares}", color=ROJO))
        self.play(*[Flash(ins.A[a][0], color=ROJO, flash_radius=0.45) for a, _ in nueva])
        self.play(*narr.decir(r"Las dos tienen un proponente solo: la definición vieja no "
                              r"las puede ver", color=ROJO))
        self.wait(2.5)
