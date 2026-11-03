"""Ejercicio 4: el contador binario en una máquina de Turing. Dos escenas:

    Monedas  el incremento caro de la sección 3, 10111 + 1, pagado con monedas: cada 1
             lleva dos, una paga la ida del acarreo y otra la vuelta; el incremento trae
             4, gasta 2 y deja 2 pegadas al 1 nuevo. Amortizado: 4
    Cabezal  el mismo tipo de incremento con el cabezal en cada extremo del número, y
             el promedio de pasos por incremento de las dos máquinas

    uv run --python 3.13 --with manim manim -ql ejercicio-04.py Monedas

Las dos tablas de transiciones son las de ejercicio-04.py.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import (DOWN, LEFT, PI, RIGHT, UP, Circle, FadeIn, FadeOut, LaggedStart,
                   Rectangle, Scene, Transform, Triangle, VGroup, Write)

from comun import (AMARILLO, APAGADO, AZUL, DORADO, GRIS, ROJO, VERDE, Narrador, celda,
                   formula, rotulo, titulo)

BLANCO = "□"
INCREMENTAR = {
    ("carry", "1"): ("0", -1, "carry"),
    ("carry", "0"): ("1", +1, "back"),
    ("carry", BLANCO): ("1", +1, "back"),
    ("back", "0"): ("0", +1, "back"),
    ("back", BLANCO): (BLANCO, -1, "halt"),
}
INCREMENTAR_DESDE_MSB = {
    ("go", "0"): ("0", +1, "go"),
    ("go", "1"): ("1", +1, "go"),
    ("go", BLANCO): (BLANCO, -1, "carry"),
    ("carry", "1"): ("0", -1, "carry"),
    ("carry", "0"): ("1", -1, "back"),
    ("carry", BLANCO): ("1", -1, "back"),
    ("back", "0"): ("0", -1, "back"),
    ("back", "1"): ("1", -1, "back"),
    ("back", BLANCO): (BLANCO, +1, "halt"),
}
COLOR_ESTADO = {"carry": AMARILLO, "back": AZUL, "go": GRIS, "halt": GRIS}


def correr(delta, cinta, cabezal, estado):
    """Como en ejercicio-04.py, pero devuelve también los pasos:
    (estado, posición, leído, escrito, posición siguiente, estado siguiente)."""
    pasos = []
    while estado != "halt":
        leido = cinta.get(cabezal, BLANCO)
        escribe, mueve, nuevo = delta[(estado, leido)]
        pasos.append((estado, cabezal, leido, escribe, cabezal + mueve, nuevo))
        if escribe == BLANCO:
            cinta.pop(cabezal, None)
        else:
            cinta[cabezal] = escribe
        cabezal += mueve
        estado = nuevo
    return cabezal, pasos


def contar_hasta(delta, inicial, v):
    cinta, cabezal = {0: "0"}, 0
    for _ in range(v):
        cabezal, _ = correr(delta, cinta, cabezal, inicial)
    return cinta, cabezal


class Cinta:
    def __init__(self, posiciones, y, lado=0.85, x=0.0):
        self.pos = list(posiciones)
        self.celdas = VGroup(*[celda(r"\square", lado, tam=34, color=APAGADO)
                               for _ in self.pos])
        self.celdas.arrange(RIGHT, buff=0.06).move_to(RIGHT * x + UP * y)

    def de(self, p):
        return self.celdas[self.pos.index(p)]

    def simbolo_en(self, p, s):
        return formula(r"\square" if s == BLANCO else s, tam=34,
                       color=APAGADO if s == BLANCO else "#ffffff").move_to(self.de(p))

    def escribir(self, cinta):
        for p, c in zip(self.pos, self.celdas):
            c[1].become(self.simbolo_en(p, cinta.get(p, BLANCO)))


def flecha_cabezal(color):
    return Triangle(color=color, fill_color=color, fill_opacity=1).scale(0.16).rotate(PI)


def moneda():
    return Circle(radius=0.12, stroke_color="#b8860b", stroke_width=2,
                  fill_color=DORADO, fill_opacity=1)


class Monedas(Scene):
    def construct(self):
        narr = Narrador()
        self.add(titulo(r"Dos monedas por cada 1: el incremento cuesta 4"))
        cinta, cabezal = contar_hasta(INCREMENTAR, "carry", 23)
        tira = Cinta(range(-6, 2), y=0.5, x=-1.3)
        tira.escribir(cinta)
        cab = flecha_cabezal(AMARILLO).next_to(tira.de(cabezal), UP, 0.12)
        estado = rotulo(r"\texttt{carry}", 30, AMARILLO).next_to(cab, UP, 0.08)
        self.play(FadeIn(tira.celdas), FadeIn(cab), FadeIn(estado), *narr.decir(
            r"La cinta tiene $10111 = 23$, y el cabezal está en el bit menos significativo"))

        # Dos monedas debajo de cada 1: el potencial 2·(unos).
        bolsas = {}
        for p in tira.pos:
            if cinta.get(p) == "1":
                debajo = tira.de(p).get_bottom() + DOWN * 0.28
                bolsas[p] = [moneda().move_to(debajo + LEFT * 0.15),
                             moneda().move_to(debajo + RIGHT * 0.15)]
        todas = [m for b in bolsas.values() for m in b]
        phi = formula(r"\Phi = 2 \cdot \text{unos} = ", str(len(todas)), tam=40,
                      color=DORADO).move_to(RIGHT * 4.3 + DOWN * 1.3)
        self.play(LaggedStart(*[FadeIn(m, scale=0.5) for m in todas], lag_ratio=0.08),
                  Write(phi), *narr.decir(r"Cada 1 lleva dos monedas pegadas: eso es el "
                                          r"potencial"))
        self.wait(0.8)
        banco = [moneda().move_to(RIGHT * (3.7 + 0.32 * i) + UP * 1.9) for i in range(4)]
        cobro = rotulo(r"el incremento cobra 4", 32, DORADO).move_to(RIGHT * 4.2 + UP * 2.4)
        pasos_txt = formula(r"\text{pasos} = 0", tam=40).move_to(RIGHT * 4.3 + UP * 0.9)
        self.play(LaggedStart(*[FadeIn(m, scale=0.5) for m in banco], lag_ratio=0.1),
                  FadeIn(cobro), FadeIn(pasos_txt))
        self.wait(0.5)

        antes = len(todas)
        cabezal, pasos = correr(INCREMENTAR, cinta, cabezal, "carry")
        for k, (est, p, leido, escribe, siguiente, nuevo) in enumerate(pasos, start=1):
            if est == "carry" and leido == "1":
                paga = bolsas[p].pop(0)
                dicho = r"El acarreo borra un 1: lo paga una de sus monedas"
            elif est == "back" and bolsas.get(p):
                paga = bolsas[p].pop(0)
                dicho = r"A la vuelta, la otra moneda de ese 1 paga el paso"
            else:
                paga = banco.pop(0)
                dicho = (r"Escribir el 1 lo paga el incremento" if est == "carry" else
                         r"El último paso, de vuelta al principio, también")
            color = COLOR_ESTADO[nuevo]
            self.play(paga.animate.move_to(cab.get_center()).scale(0.6), *narr.decir(dicho),
                      run_time=0.6)
            self.play(FadeOut(paga),
                      tira.de(p)[1].animate.become(tira.simbolo_en(p, escribe)),
                      cab.animate.next_to(tira.de(siguiente), UP, 0.12).set_color(color),
                      estado.animate.become(rotulo(rf"\texttt{{{nuevo}}}", 30, color)
                                            .next_to(tira.de(siguiente), UP, 0.48)),
                      Transform(pasos_txt, formula(rf"\text{{pasos}} = {k}", tam=40)
                                .move_to(pasos_txt)),
                      run_time=0.6)
        # Las dos monedas que sobran quedan pegadas al 1 nuevo.
        nuevo_uno = next(p for (_, p, _, escrito, _, _) in pasos if escrito == "1")
        debajo = tira.de(nuevo_uno).get_bottom() + DOWN * 0.28
        despues = 2 * sum(1 for s in cinta.values() if s == "1")
        self.play(banco[0].animate.move_to(debajo + LEFT * 0.15),
                  banco[1].animate.move_to(debajo + RIGHT * 0.15),
                  Transform(phi, formula(r"\Phi = 2 \cdot \text{unos} = ", str(despues),
                                         tam=40, color=DORADO).move_to(phi)),
                  *narr.decir(r"Las dos que sobran quedan pegadas al 1 nuevo"))
        self.wait(0.6)
        c = len(pasos)
        cuenta = formula(rf"\hat c = c + \Delta\Phi = {c} + ({despues} - {antes}) = "
                         rf"{c + despues - antes}", tam=44, color=VERDE)
        cuenta.move_to(DOWN * 1.9 + LEFT * 1.3)
        self.play(Write(cuenta), *narr.decir(
            r"Ninguna cuenta queda en rojo: $m$ incrementos cuestan menos de $4m$",
            color=VERDE))
        self.wait(2.5)


class Cabezal(Scene):
    def construct(self):
        narr = Narrador()
        self.add(titulo(r"¿Y si el cabezal empieza en el otro extremo?"))
        v = 100
        tiras = []
        for y, delta, inicial, nombre in ((1.6, INCREMENTAR, "carry",
                                           r"desde el bit menos significativo"),
                                          (-0.6, INCREMENTAR_DESDE_MSB, "go",
                                           r"desde el bit más significativo")):
            cinta, cabezal = contar_hasta(delta, inicial, v)
            tira = Cinta(range(-7, 2), y=y, lado=0.72, x=-1.6)
            tira.escribir(cinta)
            cab = flecha_cabezal(COLOR_ESTADO[inicial]).next_to(tira.de(cabezal), UP, 0.1)
            rot = rotulo(nombre, 30, GRIS).next_to(tira.celdas, UP, 0.55).align_to(
                tira.celdas, LEFT)
            cuenta = formula(r"\text{pasos} = 0", tam=38).next_to(tira.celdas, RIGHT, 0.6)
            self.add(tira.celdas, cab, rot, cuenta)
            _, pasos = correr(delta, cinta, cabezal, inicial)
            tiras.append((tira, cab, cuenta, pasos))
        self.play(*narr.decir(r"Las dos cintas tienen $1100100 = 100$; sumamos 1"))
        self.wait(0.6)

        for k in range(max(len(t[3]) for t in tiras)):
            anims = []
            for tira, cab, cuenta, pasos in tiras:
                if k < len(pasos):
                    _, p, _, escribe, sig, nuevo = pasos[k]
                    anims += [tira.de(p)[1].animate.become(tira.simbolo_en(p, escribe)),
                              cab.animate.next_to(tira.de(sig), UP, 0.1)
                              .set_color(COLOR_ESTADO[nuevo]),
                              Transform(cuenta, formula(rf"\text{{pasos}} = {k + 1}",
                                                        tam=38).move_to(cuenta))]
            dicho = {1: r"Arriba: 2 pasos, y listo",
                     4: r"Abajo: hay que caminar todo el número, ida y vuelta"}.get(k)
            self.play(*anims, *(narr.decir(dicho) if dicho else []), run_time=0.35)
        self.wait(1)

        quedan = {self.mobjects[0], narr.actual}
        self.play(*[FadeOut(m) for m in self.mobjects if m not in quedan])
        self.promedios(narr)

    def promedios(self, narr):
        ms = [16, 256, 4096, 65536]
        datos = []
        for delta, inicial in ((INCREMENTAR, "carry"), (INCREMENTAR_DESDE_MSB, "go")):
            cinta, cabezal, total, fila = {0: "0"}, 0, 0, []
            for m in range(1, ms[-1] + 1):
                cabezal, pasos = correr(delta, cinta, cabezal, inicial)
                total += len(pasos)
                if m in ms:
                    fila.append(total / m)
            datos.append(fila)
        base, escala, ancho = DOWN * 2.3, 0.11, 0.55
        barras = []
        for i, m in enumerate(ms):
            x = -4.2 + 2.6 * i
            grupo = VGroup()
            for j, color in ((0, AZUL), (1, ROJO)):
                b = Rectangle(width=ancho, height=datos[j][i] * escala, stroke_width=0,
                              fill_color=color, fill_opacity=0.85)
                b.move_to(RIGHT * (x + (j - 0.5) * (ancho + 0.08)) + base, aligned_edge=DOWN)
                num = formula(f"{datos[j][i]:.2f}", tam=26, color=color).next_to(b, UP, 0.08)
                grupo.add(b, num)
            grupo.add(formula(f"m = {m}", tam=28, color=GRIS)
                      .move_to(RIGHT * x + base + DOWN * 0.35))
            barras.append(grupo)
        leyenda = VGroup(rotulo(r"desde el menos significativo", 28, AZUL),
                         rotulo(r"desde el más significativo", 28, ROJO))
        leyenda.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(LEFT * 3.4 + UP * 2.2)
        rot = rotulo(r"pasos por incremento, en promedio", 32).move_to(RIGHT * 2.8 + UP * 2.4)
        self.play(FadeIn(leyenda), FadeIn(rot), *narr.decir(
            r"El promedio de pasos por incremento en los $m$ primeros"))
        for g in barras:
            self.play(FadeIn(g, shift=0.2 * UP), run_time=0.7)
        self.play(*narr.decir(r"Desde el menos significativo, 4; desde el más, crece como "
                              r"$2 \log_2 m$: ningún potencial lo arregla", color=ROJO))
        self.wait(2.5)
