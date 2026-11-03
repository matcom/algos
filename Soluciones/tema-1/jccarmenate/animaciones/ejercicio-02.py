"""Ejercicio 2: la búsqueda binaria. Cuatro escenas, una por idea:

    Invariante  lo que queda fuera de la ventana ya está decidido: a la izquierda,
                menor que x; a la derecha, mayor. Con la ventana vacía, el hueco
    Bits        el potencial que cuenta: hi - lo pierde por lo menos un bit por
                comparación, así que hay a lo sumo tantas comparaciones como bits de n
    Testigo     dos valores en huecos distintos no pueden llegar a la misma hoja, y
                entonces el árbol necesita n + 1 hojas: 2^h >= n + 1
    Estancada   el error lo = m: con un solo candidato y respuesta >, la ventana no
                cambia y el potencial se estanca

    uv run --python 3.13 --with manim manim -ql ejercicio-02.py Invariante

El arreglo y los valores buscados son los de las secciones 2 y 7 del ejercicio.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import (DOWN, LEFT, RIGHT, UP, Brace, Create, DashedLine, Dot, FadeIn,
                   FadeOut, LaggedStart, Line, ReplacementTransform, Scene, Transform,
                   VGroup, Write)

from comun import (AMARILLO, APAGADO, AZUL, DORADO, GRIS, ROJO, VERDE, Narrador, borde,
                   fila, formula, indices, puntero, rotulo, titulo, ventana)

A = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]


def traza(A, x, lo_mal=False, tope=None):
    """La búsqueda binaria de ejercicio-02.py, guardando cada paso. Con lo_mal = True es
    la variante lo = m de la sección 7; `tope` corta las vueltas si no termina."""
    pasos = []
    lo, hi = 0, len(A)
    while lo < hi and (tope is None or len(pasos) < tope):
        m = (lo + hi) // 2
        r = (x > A[m]) - (x < A[m])
        pasos.append((lo, hi, m, r))
        if r == 0:
            return pasos, ("está", m)
        if r < 0:
            hi = m
        else:
            lo = m if lo_mal else m + 1
    return pasos, ("hueco", lo)


def bits(s):
    return s.bit_length()


def punteros(celdas, lo, hi):
    if lo == hi:
        return VGroup(puntero(celdas, lo, r"\mathit{lo}", corrimiento=-0.35),
                      puntero(celdas, hi, r"\mathit{hi}", corrimiento=0.35))
    return VGroup(puntero(celdas, lo, r"\mathit{lo}"), puntero(celdas, hi, r"\mathit{hi}"))


def simbolo(r):
    return {-1: "<", 0: "=", 1: ">"}[r]


class Invariante(Scene):
    def construct(self):
        narr = Narrador()
        self.add(titulo(r"Lo que queda fuera de la ventana ya está decidido"))
        inv = formula(r"A[i] < x \ \text{ si } i < \mathit{lo}", r"\qquad",
                      r"A[i] > x \ \text{ si } i \ge \mathit{hi}", tam=40, color=AMARILLO)
        inv.shift(UP * 2.45)
        celdas = fila(A, lado=0.85, tam=36).shift(DOWN * 0.1 + RIGHT * 0.7)
        nums = indices(celdas)
        x = 50
        ex = formula("x", "=", str(x), tam=48, color=AMARILLO).move_to(LEFT * 5.6 + UP * 1.4)
        self.play(LaggedStart(*[FadeIn(c, shift=0.2 * UP) for c in celdas], lag_ratio=0.05),
                  FadeIn(nums), Write(ex), *narr.decir(
                      r"Un arreglo ordenado; buscamos $x = 50$, que no está"))
        pasos, (_, g) = traza(A, x)
        lo, hi = 0, len(A)
        caja = ventana(celdas, lo, hi)
        flechas = punteros(celdas, lo, hi)
        self.play(Create(caja), FadeIn(flechas), Write(inv), *narr.decir(
            r"El invariante habla de todo lo que queda \emph{fuera} de la ventana"))
        self.wait(1)

        izq = der = None
        for lo, hi, m, r in pasos:
            comp = formula(str(x), simbolo(r), str(A[m]), tam=48)
            comp.next_to(ex, DOWN, buff=0.35).align_to(ex, LEFT)
            self.play(celdas[m][0].animate.set_stroke(AMARILLO, 6), FadeIn(comp),
                      *narr.decir(rf"Comparamos con el del medio, $A[{m}] = {A[m]}$"),
                      run_time=0.9)
            if r < 0:
                nlo, nhi, tramo = lo, m, range(m, hi)
                dicho = (rf"$50 < {A[m]}$, y el arreglo está ordenado: todo desde "
                         rf"$A[{m}]$ es mayor")
            else:
                nlo, nhi, tramo = m + 1, hi, range(lo, m + 1)
                dicho = (rf"$50 > {A[m]}$, y el arreglo está ordenado: todo hasta "
                         rf"$A[{m}]$ es menor")
            anims = [celdas[i][0].animate.set_stroke(VERDE, 3).set_fill(VERDE, 0.18)
                     for i in tramo]
            anims += [Transform(caja, ventana(celdas, nlo, nhi)),
                      Transform(flechas, punteros(celdas, nlo, nhi))]
            if nlo > 0:
                nueva = self.llave(celdas, 0, nlo, "< 50")
                anims.append(Transform(izq, nueva) if izq else FadeIn(nueva))
                izq = izq or nueva
            if nhi < len(A):
                nueva = self.llave(celdas, nhi, len(A), "> 50")
                anims.append(Transform(der, nueva) if der else FadeIn(nueva))
                der = der or nueva
            self.play(*anims, FadeOut(comp), *narr.decir(dicho), run_time=1.3)
            self.wait(0.6)

        hueco = Line(borde(celdas, g) + UP * 0.75, borde(celdas, g) + DOWN * 0.75,
                     color=AMARILLO, stroke_width=8)
        self.play(Create(hueco), *narr.decir(
            rf"Ventana vacía: {g} elementos son menores que $x$, así que $x$ cae en el "
            rf"hueco $h_{g}$", color=AMARILLO))
        self.wait(2.5)

    def llave(self, celdas, desde, hasta, texto):
        llave = Brace(VGroup(*celdas[desde:hasta]), UP, color=VERDE, buff=0.12)
        return VGroup(llave, formula(texto, tam=36, color=VERDE).next_to(llave, UP, 0.08))


class Bits(Scene):
    def construct(self):
        narr = Narrador()
        self.add(titulo(r"El potencial que cuenta: los bits de $\mathit{hi} - \mathit{lo}$"))
        celdas = fila(A, lado=0.7, tam=30).shift(UP * 1.75 + RIGHT * 0.6)
        x = 50
        ex = formula("x", "=", str(x), tam=40, color=AMARILLO).next_to(celdas, LEFT, 0.4)
        pasos, _ = traza(A, x)
        lo, hi = 0, len(A)
        caja = ventana(celdas, lo, hi)
        self.add(celdas, ex)

        centro = DOWN * 0.35
        izq = formula(r"\mathit{hi} - \mathit{lo} \;=", tam=48).move_to(centro + LEFT * 3.4)
        digitos = self.binario(hi - lo, centro)
        dec = self.decimal(hi - lo, digitos)
        psi = self.psi(bits(hi - lo))
        cuenta = self.cuenta(0)
        self.play(Create(caja), Write(izq), FadeIn(digitos), FadeIn(dec), FadeIn(psi),
                  FadeIn(cuenta), *narr.decir(
                      r"El tamaño de la ventana, en binario: $\Psi$ es cuántos bits tiene"))
        self.wait(1)

        for c, (lo, hi, m, r) in enumerate(pasos, start=1):
            s = hi - lo
            nlo, nhi = (lo, m) if r < 0 else (m + 1, hi)
            nuevo = nhi - nlo
            # La mitad de s es s sin su último bit.
            self.play(celdas[m][0].animate.set_stroke(AMARILLO, 5),
                      digitos[-1].animate.shift(DOWN * 0.7).set_opacity(0),
                      *narr.decir(rf"Comparar con $A[{m}]$ deja a lo sumo "
                                  r"$\lfloor s/2 \rfloor$: $s$ sin su último bit"),
                      run_time=1.0)
            nuevos = self.binario(nuevo, centro)
            resto = VGroup(*digitos[:-1])
            anims = [ReplacementTransform(resto, nuevos) if len(resto) else FadeIn(nuevos),
                     Transform(dec, self.decimal(nuevo, nuevos)),
                     Transform(psi, self.psi(bits(nuevo))),
                     Transform(caja, ventana(celdas, nlo, nhi)),
                     Transform(cuenta, self.cuenta(c)),
                     celdas[m][0].animate.set_stroke(GRIS, 2.5)]
            anims += [celdas[i].animate.set_opacity(0.3)
                      for i in (range(m, hi) if r < 0 else range(lo, m + 1))]
            if nuevo < s // 2:
                dicho = (rf"Quedan {nuevo}, menos que $\lfloor {s}/2 \rfloor = {s // 2}$:"
                         r" un bit menos, por lo menos")
            else:
                dicho = rf"Quedan {nuevo} $= \lfloor {s}/2 \rfloor$: un bit menos"
            self.play(*anims, *narr.decir(dicho), run_time=1.2)
            self.remove(digitos[-1])
            digitos = nuevos
            self.wait(0.6)

        cota = formula(r"c \;\le\; \mathrm{bits}(n) = \lfloor \log_2 n \rfloor + 1",
                       tam=44, color=DORADO).move_to(DOWN * 1.9 + LEFT * 1.6)
        self.play(Write(cota), *narr.decir(
            rf"{len(pasos)} comparaciones: tantas como bits tiene $n = 10 = 1010_2$",
            color=DORADO))
        self.wait(2.5)

    def binario(self, s, centro):
        if s == 0:
            return VGroup(formula(r"0", tam=72, color=APAGADO).move_to(centro))
        g = VGroup(*[formula(b, tam=72, color=DORADO) for b in bin(s)[2:]])
        return g.arrange(RIGHT, buff=0.12).move_to(centro)

    def decimal(self, s, digitos):
        d = formula(rf"_{{2}} \;=\; {s}", tam=56, color=GRIS).next_to(digitos, RIGHT, 0.15)
        return d.align_to(digitos, DOWN)

    def psi(self, b):
        return formula(rf"\Psi = {b}", tam=48, color=DORADO).move_to(RIGHT * 4.7 +
                                                                     DOWN * 0.35)

    def cuenta(self, c):
        return formula(rf"\text{{comparaciones: }} {c}", tam=40).move_to(RIGHT * 4.3 +
                                                                       DOWN * 1.9)


class Testigo(Scene):
    """El argumento del testigo de la sección 6, como en la figura 1 del ejercicio."""

    def construct(self):
        narr = Narrador()
        self.add(titulo(r"Dos huecos distintos no pueden compartir hoja"))
        B = [10, 20, 30, 40, 50, 60]
        x1, x2, j = 15, 45, 2
        recta = Line(LEFT * 6.3, RIGHT * 6.3, color=GRIS, stroke_width=3).shift(UP * 1.2)

        def escala(v):
            return LEFT * 6.0 + RIGHT * v * 12 / 70 + UP * 1.2

        marcas = VGroup()
        for i, v in enumerate(B):
            p = escala(v)
            marcas.add(VGroup(Line(p + UP * 0.15, p + DOWN * 0.15, color=GRIS),
                              formula(f"A[{i}]", tam=28, color=GRIS).next_to(p, UP, 0.25)))
        bordes = [0] + B + [70]
        huecos = VGroup(*[formula(f"h_{{{g}}}", tam=26, color=APAGADO).move_to(
            escala((bordes[g] + bordes[g + 1]) / 2) + DOWN * 0.35)
            for g in range(len(B) + 1)])
        self.play(Create(recta), FadeIn(marcas), FadeIn(huecos), *narr.decir(
            r"Seis elementos y siete huecos; $x_1$ en $h_1$ y $x_2$ en $h_4$"))
        fichas = VGroup(self.ficha(r"x_1", AZUL, escala(x1)),
                        self.ficha(r"x_2", AZUL, escala(x2)))
        self.play(LaggedStart(*[FadeIn(f, shift=0.2 * DOWN) for f in fichas],
                              lag_ratio=0.3))
        self.wait(0.5)

        # Un algoritmo que lleva a x1 y a x2 a la misma hoja: solo compara afuera.
        preguntas = [4, 0, 5]
        encabezado = VGroup(formula("x_1", tam=34, color=AZUL),
                            formula("x_2", tam=34, color=AZUL))
        encabezado.arrange(RIGHT, buff=0.9).move_to(RIGHT * 1.6 + DOWN * 0.75)
        self.play(FadeIn(encabezado), *narr.decir(
            r"Si llegan a la misma hoja, ninguna comparación los separó"))
        filas = []
        for k, i in enumerate(preguntas):
            p = escala(B[i])
            corte = DashedLine(p + UP * 0.9, p + DOWN * 0.9, color=AMARILLO)
            rot = formula(f"A[{i}]\\,?", tam=32, color=AMARILLO)
            rot.move_to(LEFT * 1.2 + DOWN * (1.35 + 0.55 * k))
            resp = VGroup(*[formula(simbolo((v > B[i]) - (v < B[i])), tam=34).move_to(
                [encabezado[c].get_center()[0], rot.get_center()[1], 0])
                for c, v in enumerate((x1, x2))])
            self.play(Create(corte), FadeIn(rot), run_time=0.6)
            self.play(FadeIn(resp), FadeOut(corte), run_time=0.6)
            filas.append(rot)
        self.wait(0.6)
        # El testigo: A[j], entre los dos huecos, recibe las mismas respuestas.
        testigo = self.ficha(rf"A[{j}]", AMARILLO, escala(B[j]))
        col = formula(rf"A[{j}]", tam=34, color=AMARILLO).next_to(encabezado, RIGHT, 0.9)
        self.play(FadeIn(testigo, shift=0.2 * DOWN), FadeIn(col), *narr.decir(
            rf"Ninguna pregunta cayó entre $h_1$ y $h_4$: tomemos $x = A[{j}] = {B[j]}$"))
        resp_t = VGroup(*[formula(simbolo((B[j] > B[i]) - (B[j] < B[i])), tam=34,
                                  color=AMARILLO).move_to(
            [col.get_center()[0], filas[k].get_center()[1], 0])
            for k, i in enumerate(preguntas)])
        self.play(LaggedStart(*[FadeIn(r) for r in resp_t], lag_ratio=0.3))
        self.play(*narr.decir(r"Mismas respuestas, misma hoja: dice que $x$ no está, y "
                              r"$A[2]$ sí está", color=ROJO))
        self.wait(2)

        # Entonces los n + 1 huecos piden n + 1 hojas, y un árbol binario de altura h
        # tiene a lo sumo 2^h.
        fijos = {self.mobjects[0], narr.actual}
        self.play(*[FadeOut(m) for m in self.mobjects if m not in fijos])
        self.arbol(narr)

    def ficha(self, nombre, color, p):
        punto = Dot(p, radius=0.11, color=color)
        return VGroup(punto, formula(nombre, tam=30, color=color).next_to(punto, DOWN,
                                                                          0.75))

    def arbol(self, narr):
        n = 10
        pedidas = VGroup(*[Dot(radius=0.09, color=AMARILLO) for _ in range(n + 1)])
        pedidas.arrange(RIGHT, buff=0.3).move_to(DOWN * 2.35)
        pedido = formula(r"n + 1 = 11", r"\text{ huecos}", tam=34, color=AMARILLO)
        pedido.next_to(pedidas, UP, 0.2)
        self.play(FadeIn(pedidas), Write(pedido), *narr.decir(
            r"Con $n = 10$: once huecos, once hojas distintas"))
        anterior = None
        for h in range(5):
            cant = 2 ** h
            nivel = VGroup(*[Dot(radius=0.08, color=AZUL) for _ in range(cant)])
            nivel.arrange(RIGHT, buff=min(0.6, 7.0 / cant)).move_to(UP * (2.3 - 0.72 * h))
            color = VERDE if cant >= n + 1 else (ROJO if h == 3 else GRIS)
            rot = formula(rf"2^{h} = {cant}", tam=32, color=color)
            rot.move_to(RIGHT * 5.6 + UP * (2.3 - 0.72 * h))
            aristas = VGroup()
            if anterior is not None:
                for k, d in enumerate(nivel):
                    aristas.add(Line(anterior[k // 2].get_center(), d.get_center(),
                                     color=APAGADO, stroke_width=2))
            dicho = (rf"Altura {h}: a lo sumo {cant} hojas" if cant < n + 1 else
                     rf"Altura {h}: ${cant} \ge 11$, recién alcanza")
            self.play(Create(aristas), FadeIn(nivel), Write(rot), *narr.decir(dicho),
                      run_time=0.8)
            anterior = nivel
            self.wait(0.3)
        cota = formula(r"2^h \ge n + 1", r"\;\Longrightarrow\;",
                       r"h \ge \lceil \log_2 (n+1) \rceil = 4", tam=40, color=VERDE)
        cota.move_to(DOWN * 1.3)
        self.play(Write(cota), *narr.decir(
            r"Cada nivel a lo sumo duplica las hojas: la búsqueda binaria es óptima",
            color=VERDE))
        self.wait(2.5)


class Estancada(Scene):
    """El error lo = m de la sección 7, con el arreglo 2, 4, ..., 20."""

    def construct(self):
        narr = Narrador()
        self.add(titulo(r"El error \texttt{lo = m}: el potencial se estanca"))
        B = list(range(2, 21, 2))
        celdas = fila(B, lado=0.9, tam=36).shift(UP * 0.6)
        nums = indices(celdas)
        x = 7
        ex = formula("x", "=", str(x), tam=48, color=AMARILLO).move_to(LEFT * 5.2 + UP * 2.2)
        cod = rotulo(r"\texttt{if x > A[m]: lo = m}", 34, ROJO).move_to(RIGHT * 2.6 +
                                                                        UP * 2.2)
        self.play(FadeIn(celdas), FadeIn(nums), Write(ex), FadeIn(cod), *narr.decir(
            r"Buscamos $x = 7$, que no está y es mayor que $A[0]$"))
        pasos, _ = traza(B, x, lo_mal=True, tope=7)
        lo, hi = 0, len(B)
        caja = ventana(celdas, lo, hi)
        flechas = punteros(celdas, lo, hi)
        psi = formula(rf"\Psi = {bits(hi - lo)}", tam=48, color=DORADO)
        psi.move_to(RIGHT * 4.8 + DOWN * 1.6)
        vueltas = formula(r"\text{vuelta } 0", tam=40).move_to(LEFT * 4.6 + DOWN * 1.6)
        self.play(Create(caja), FadeIn(flechas), FadeIn(psi), FadeIn(vueltas))
        for k, (lo, hi, m, r) in enumerate(pasos, start=1):
            nlo, nhi = (lo, m) if r < 0 else (m, hi)
            atascado = (nlo, nhi) == (lo, hi)
            comp = formula(str(x), simbolo(r), str(B[m]), tam=44).next_to(ex, DOWN, 0.3)
            self.play(celdas[m][0].animate.set_stroke(AMARILLO, 6), FadeIn(comp),
                      run_time=0.6 if atascado else 0.8)
            if atascado:
                dicho, color = (r"Un solo candidato, menor que $x$: \texttt{lo = m} no "
                                r"mueve nada"), ROJO
            else:
                dicho, color = rf"$\Psi = {bits(nhi - nlo)}$: todavía baja", "#ffffff"
            self.play(Transform(caja, ventana(celdas, nlo, nhi,
                                              color=ROJO if atascado else AZUL)),
                      Transform(flechas, punteros(celdas, nlo, nhi)),
                      Transform(psi, formula(rf"\Psi = {bits(nhi - nlo)}", tam=48,
                                             color=ROJO if atascado else DORADO)
                                .move_to(psi)),
                      Transform(vueltas, formula(rf"\text{{vuelta }} {k}", tam=40)
                                .move_to(vueltas)),
                      celdas[m][0].animate.set_stroke(GRIS, 2.5), FadeOut(comp),
                      *narr.decir(dicho, color=color),
                      run_time=0.6 if atascado else 1.0)
        self.wait(0.5)
        bien = rotulo(r"Con \texttt{lo = m + 1}, la ventana se vacía y $x$ cae en $h_3$",
                      34, VERDE).move_to(DOWN * 2.4)
        self.play(FadeIn(bien, shift=0.15 * UP), *narr.decir(
            r"Solo pasa con $x$ ausente: la batería ``$x$ presente'' no lo ve nunca"))
        self.wait(2.5)
