"""Ejercicio 8: los elementos que aparecen más de n/3 veces. Dos escenas:

    Trios      la primera pasada sobre A B C A B A D B A E A B: cada elemento termina
               como copia viva de un candidato o dentro de un trío de tres distintos,
               que es el invariante (T); después, la verificación
    OrdenMalo  la variante que llena un lugar libre antes de mirar el otro candidato,
               sobre A B B C B A: dos copias vivas de B en lugares distintos, y la A
               final las cancela juntas en un trío que no es de distintos

    uv run --python 3.13 --with manim manim -ql ejercicio-08.py Trios

El orden de los if es el de first_pass en ejercicio-08.py.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import (DOWN, LEFT, RIGHT, UP, FadeIn, FadeOut, Scene, SurroundingRectangle,
                   Transform, VGroup, Write)

from comun import (AMARILLO, AZUL, GRIS, ROJO, VERDE, Narrador, celda, formula, rotulo,
                   titulo)

VIOLETA = "#c792ea"
COLOR = {"A": AZUL, "B": VIOLETA}


def ficha(letra, lado=0.6):
    f = celda(letra, lado, tam=34, color=COLOR.get(letra, GRIS))
    f[1].set_color(COLOR.get(letra, "#ffffff"))
    return f


def pasos_de(A, orden_malo):
    """first_pass de ejercicio-08.py, anotando qué hace con cada elemento:
    ("sube", lugar), ("nuevo", lugar) o ("trio", (i, copia de c1, copia de c2)),
    junto con los candidatos y contadores que quedan."""
    c, k, copias = [None, None], [0, 0], [[], []]
    pasos = []
    for i, x in enumerate(A):
        if k[0] > 0 and x == c[0]:
            lugar, que = 0, "sube"
        elif orden_malo and k[0] == 0:
            lugar, que = 0, "nuevo"
        elif k[1] > 0 and x == c[1]:
            lugar, que = 1, "sube"
        elif k[0] == 0:
            lugar, que = 0, "nuevo"
        elif k[1] == 0:
            lugar, que = 1, "nuevo"
        else:
            trio = (i, copias[0].pop(), copias[1].pop())
            k = [k[0] - 1, k[1] - 1]
            pasos.append(("trio", trio, list(c), list(k)))
            continue
        if que == "nuevo":
            c[lugar], k[lugar], copias[lugar] = x, 1, [i]
        else:
            k[lugar] += 1
            copias[lugar].append(i)
        pasos.append((que, lugar, list(c), list(k)))
    return pasos


def pasada(escena, narr, A, orden_malo):
    seq = VGroup(*[ficha(x, 0.62) for x in A]).arrange(RIGHT, buff=0.06).move_to(UP * 2.25)
    escena.play(FadeIn(seq), *narr.decir(r"Dos lugares: un candidato y cuántas copias "
                                         r"vivas tiene"))
    rot = [formula(r"c_1", tam=38).move_to(LEFT * 6.3 + UP * 0.6),
           formula(r"c_2", tam=38).move_to(LEFT * 6.3 + DOWN * 0.55)]
    cuentas = [formula(r"k_1 = 0", tam=36).move_to(LEFT * 2.6 + UP * 0.6),
               formula(r"k_2 = 0", tam=36).move_to(LEFT * 2.6 + DOWN * 0.55)]
    escena.play(*[FadeIn(m) for m in rot + cuentas])

    def lugar_de(l, j):
        return LEFT * (5.5 - 0.68 * j) + (UP * 0.6 if l == 0 else DOWN * 0.55)

    vivas = [[], []]        # las fichas de cada lugar, en orden
    fichas = {}
    trios = 0
    c = k = None
    for i, (que, dato, c, k) in enumerate(pasos_de(A, orden_malo)):
        x = A[i]
        marco = SurroundingRectangle(seq[i], color=AMARILLO, buff=0.03)
        f = ficha(x, 0.58).move_to(seq[i])
        fichas[i] = f
        escena.play(FadeIn(marco), seq[i].animate.set_opacity(0.3), run_time=0.35)
        escena.add(f)
        if que == "trio":
            _, p1, p2 = dato
            grupo = [f, fichas[p1], fichas[p2]]
            vivas[0].remove(fichas[p1])
            vivas[1].remove(fichas[p2])
            distintos = len({x, A[p1], A[p2]}) == 3
            columna = RIGHT * (-1.0 + 1.0 * trios)
            destinos = [columna + UP * (0.62 - 0.6 * j) for j in range(3)]
            anims = [g.animate.move_to(d) for g, d in zip(grupo, destinos)]
            anims += [v.animate.move_to(lugar_de(l, j)) for l in (0, 1)
                      for j, v in enumerate(vivas[l])]
            if distintos:
                dicho = rf"{x} es distinto de los dos: con una copia de cada uno, un trío"
            else:
                dicho = (rf"{x} cancela las dos copias de {A[p1]}: un trío que no es de "
                         r"distintos")
            escena.play(*anims, FadeOut(marco), *narr.decir(
                dicho, color="#ffffff" if distintos else ROJO), run_time=1.0)
            escena.play(FadeIn(SurroundingRectangle(VGroup(*grupo), buff=0.06,
                                                    color=VERDE if distintos else ROJO)),
                        run_time=0.4)
            trios += 1
        else:
            l = dato
            otro = 1 - l
            rompe = que == "nuevo" and k[otro] > 0 and c[otro] == x
            if rompe:
                dicho = (rf"{x} pasa al lugar {l + 1}, pero ya es el candidato {otro + 1}: "
                         r"se rompe $c_1 \ne c_2$")
            elif que == "nuevo":
                dicho = rf"El lugar {l + 1} estaba libre: {x} pasa a ser candidato"
            else:
                dicho = rf"{x} ya es el candidato {l + 1}: una copia viva más"
            vivas[l].append(f)
            escena.play(f.animate.move_to(lugar_de(l, len(vivas[l]) - 1)), FadeOut(marco),
                        *narr.decir(dicho, color=ROJO if rompe else "#ffffff"), run_time=0.8)
            if rompe:
                escena.wait(1.2)
        escena.play(*[Transform(cuentas[l], formula(rf"k_{l + 1} = {k[l]}", tam=36)
                                .move_to(cuentas[l])) for l in (0, 1)], run_time=0.3)
    return c, k


class Trios(Scene):
    def construct(self):
        narr = Narrador()
        self.add(titulo(r"Tachar tríos de distintos: el invariante (T)"))
        A = list("ABCABADBAEAB")
        inv = rotulo(r"Lo leído es: tríos de distintos\\$+$ $k_1$ copias de $c_1$\\"
                     r"$+$ $k_2$ copias de $c_2$", 32, AMARILLO).move_to(RIGHT * 4.6 + UP * 0.2)
        self.play(Write(inv))
        c, k = pasada(self, narr, A, orden_malo=False)
        self.wait(0.8)
        n = len(A)
        candidatos = [c[l] for l in (0, 1) if k[l] > 0]
        lineas = VGroup()
        for x in candidatos:
            cuenta = A.count(x)
            ok = 3 * cuenta > n
            lineas.add(formula(rf"\text{{{x}}}: {cuenta}", r">" if ok else r"\not>",
                               rf"{n}/3", tam=40, color=VERDE if ok else ROJO))
        lineas.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 4.6 + DOWN * 1.9)
        self.play(FadeOut(inv), FadeIn(lineas, shift=0.1 * UP), *narr.decir(
            r"Ser candidato vivo no alcanza: hay que contar, en una segunda pasada"))
        resultado = [x for x in candidatos if 3 * A.count(x) > n]
        self.play(*narr.decir(rf"Más de un tercio: solo {', '.join(resultado)}",
                              color=VERDE))
        self.wait(2.5)


class OrdenMalo(Scene):
    def construct(self):
        narr = Narrador()
        self.add(titulo(r"El orden de los \texttt{if} sostiene una cláusula"))
        A = list("ABBCBA")
        cod = rotulo(r"\texttt{elif k1 == 0:} antes de mirar si $x$ es $c_2$", 32, ROJO)
        cod.move_to(RIGHT * 3.6 + UP * 0.9)
        clausula = rotulo(r"(T) pide $c_1 \ne c_2$\\si los dos están vivos", 32, AMARILLO)
        clausula.move_to(RIGHT * 4.4 + DOWN * 0.4)
        self.play(FadeIn(cod), Write(clausula))
        c, k = pasada(self, narr, A, orden_malo=True)
        self.wait(0.6)
        verdad = [x for x in sorted(set(A)) if 3 * A.count(x) > len(A)]
        devuelve = sorted(x for x in {c[l] for l in (0, 1) if k[l] > 0}
                          if 3 * A.count(x) > len(A))
        res = VGroup(
            rotulo(rf"verificado devuelve: {', '.join(devuelve) or 'nada'}", 34, ROJO),
            rotulo(rf"la verdad: {', '.join(verdad)}, que aparece {A.count(verdad[0])} "
                   rf"veces de {len(A)}", 34, VERDE))
        res.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(RIGHT * 3.4 + DOWN * 2.0)
        self.play(FadeIn(res, shift=0.1 * UP), *narr.decir(
            r"Deja afuera una respuesta correcta, y verificar no lo arregla: solo filtra",
            color=ROJO))
        self.wait(2.5)
