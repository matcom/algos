"""Ejercicio 5: Floyd, la tortuga y la liebre. Tres escenas, una por idea:

    Invariante      después de k vueltas, la tortuga está en x_k y la liebre en x_2k;
                    con ciclo se encuentran, sin ciclo la liebre llega al final
    Potencial       Φ baja 1 por vuelta: primero (μ - k) + λ, después la distancia D
    EntradaAlCiclo  desde el punto de encuentro, dos punteros a velocidad 1 se cruzan
                    en la entrada del ciclo

    uv run --python 3.13 --with manim manim -ql ejercicio-05.py Invariante

La lista es la de la figura 1 del ejercicio: cola de μ = 3 nodos y ciclo de λ = 5.
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import (DOWN, LEFT, PI, RIGHT, UP, Arc, Arrow, Brace, Circle, Create, Dot,
                   FadeIn, FadeOut, Flash, LaggedStart, MoveAlongPath, Rectangle, Scene,
                   SurroundingRectangle, TransformMatchingTex, VGroup, VMobject, Write)

from comun import (AMARILLO, APAGADO, AZUL, DORADO, FONDO, GRIS, VERDE, Narrador,
                   formula, rotulo, titulo)

MU, LAM = 3, 5
N = MU + LAM
RADIO_NODO = 0.34
CENTRO = RIGHT * 0.4 + DOWN * 0.1
R = 1.65


def siguiente(i):
    return i + 1 if i + 1 < N else MU


def angulo(i):
    """Ángulo del nodo i del ciclo, recorrido en el sentido de las agujas del reloj."""
    return PI - 2 * PI * (i - MU) / LAM


def posicion(i):
    if i < MU:
        return CENTRO + LEFT * (R + 1.45 * (MU - i))
    a = angulo(i)
    return CENTRO + R * (RIGHT * math.cos(a) + UP * math.sin(a))


def hacia_afuera(i):
    if i < MU:
        return UP
    a = angulo(i)
    return RIGHT * math.cos(a) + UP * math.sin(a)


def nodo(p, nombre, color=GRIS):
    c = Circle(radius=RADIO_NODO, stroke_color=color, stroke_width=3,
               fill_color=FONDO, fill_opacity=1).move_to(p)
    return VGroup(c, formula(nombre, tam=30).move_to(p))


def lista_rho():
    """Los nodos x_0 ... x_7 y sus flechas; las del ciclo son arcos de la circunferencia."""
    nodos = VGroup(*[nodo(posicion(i), f"x_{{{i}}}") for i in range(N)])
    flechas = VGroup()
    for i in range(MU):
        flechas.add(Arrow(posicion(i), posicion(i + 1), buff=RADIO_NODO + 0.04,
                          color=APAGADO, stroke_width=3, tip_length=0.18))
    d = (RADIO_NODO + 0.06) / R
    for i in range(MU, N):
        arco = Arc(radius=R, start_angle=angulo(i) - d, angle=-(2 * PI / LAM - 2 * d),
                   arc_center=CENTRO, color=APAGADO, stroke_width=3)
        arco.add_tip(tip_length=0.18)
        flechas.add(arco)
    return nodos, flechas


def ficha(letra, color):
    punto = Dot(radius=0.17, color=color)
    return VGroup(punto, formula(letra, tam=24, color=FONDO).move_to(punto))


def lugar(i, lado):
    """Dónde se dibuja una ficha sobre el nodo i: afuera del nodo, corrida a un lado."""
    afuera = hacia_afuera(i)
    costado = RIGHT * afuera[1] - UP * afuera[0]
    return posicion(i) + 0.62 * afuera + 0.2 * lado * costado


def camino(*puntos):
    v = VMobject()
    v.set_points_as_corners(list(puntos))
    return v


class Invariante(Scene):
    def construct(self):
        narr = Narrador()
        self.add(titulo(r"Después de $k$ vueltas: tortuga en $x_k$, liebre en $x_{2k}$"))
        nodos, flechas = lista_rho()
        self.play(LaggedStart(*[FadeIn(n, scale=0.8) for n in nodos], lag_ratio=0.08),
                  Create(flechas), run_time=1.6)
        cola = Brace(VGroup(*nodos[:MU]), DOWN, color=GRIS)
        mu = formula(r"\mu = 3", tam=34).next_to(cola, DOWN, buff=0.1)
        lam = formula(r"\lambda = 5", tam=34).move_to(CENTRO)
        self.play(FadeIn(cola), Write(mu), Write(lam), *narr.decir(
            r"Una cola de $\mu$ nodos y un ciclo de $\lambda$"))
        self.wait(0.8)

        tort, lieb = ficha("T", AZUL), ficha("L", AMARILLO)
        tort.move_to(lugar(0, -1))
        lieb.move_to(lugar(0, 1))
        panel = self.panel(0, 0, 0)
        self.play(FadeIn(tort), FadeIn(lieb), FadeOut(cola), FadeOut(mu), Write(panel),
                  *narr.decir(r"Las dos empiezan en la cabeza"))
        self.wait(0.5)

        t = h = k = 0
        while True:
            h1 = siguiente(h)
            h = siguiente(h1)
            t = siguiente(t)
            k += 1
            nuevo = self.panel(k, t, h)
            if t < MU:
                dicho = r"La tortuga todavía recorre la cola"
            elif t != h:
                dicho = (r"Las dos están en el ciclo, y $\lambda = 5$ no divide a "
                         rf"$2k - k = {k}$")
            else:
                dicho = rf"$\lambda = 5$ divide a $2k - k = {k}$: el mismo nodo"
            self.play(MoveAlongPath(lieb, camino(lieb.get_center(), lugar(h1, 1),
                                                 lugar(h, 1))),
                      tort.animate.move_to(lugar(t, -1)),
                      TransformMatchingTex(panel, nuevo), *narr.decir(dicho),
                      run_time=1.3)
            panel = nuevo
            self.wait(0.6)
            if t == h:
                break
        self.play(Flash(nodos[t], color=VERDE, flash_radius=0.6),
                  nodos[t][0].animate.set_stroke(VERDE))
        lema = formula(r"x_k = x_{2k}", r"\iff", r"k \ge \mu", r"\text{ y }",
                       r"\lambda \mid k", tam=40, color=AMARILLO)
        lema.move_to(DOWN * 2.55)
        self.play(Write(lema), *narr.decir(
            rf"Se encuentran en la vuelta $k^* = {k}$: el primer múltiplo de "
            r"$\lambda$ que es $\ge \mu$"))
        self.wait(2)

        # Sin ciclo: la liebre llega al final y nunca se cruzan.
        self.play(*[FadeOut(m) for m in (nodos, flechas, lam, tort, lieb, panel, lema)])
        self.sin_ciclo(narr)

    def panel(self, k, t, h):
        lineas = [formula(r"k", "=", str(k), tam=40),
                  formula(r"T", "=", f"x_{{{t}}}", tam=40, color=AZUL)]
        if 2 * k == h:
            lineas.append(formula(r"L", "=", f"x_{{{2 * k}}}", tam=40, color=AMARILLO))
        else:
            lineas.append(formula(r"L", "=", f"x_{{{2 * k}}}", "=", f"x_{{{h}}}", tam=40,
                                  color=AMARILLO))
        p = VGroup(*lineas).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        p.move_to(RIGHT * 3.4 + UP * 1.4, aligned_edge=LEFT)
        return p

    def sin_ciclo(self, narr):
        n = 7
        pos = [LEFT * 5.6 + RIGHT * 1.55 * i + UP * 0.3 for i in range(n)]
        nodos = VGroup(*[nodo(p, f"x_{{{i}}}") for i, p in enumerate(pos)])
        fin = formula(r"\bot", tam=44, color=GRIS).move_to(pos[-1] + RIGHT * 1.45)
        flechas = VGroup(*[Arrow(pos[i], pos[i + 1], buff=RADIO_NODO + 0.04,
                                 color=APAGADO, stroke_width=3, tip_length=0.18)
                           for i in range(n - 1)],
                         Arrow(pos[-1], fin.get_center(), buff=RADIO_NODO, color=APAGADO,
                               stroke_width=3, tip_length=0.18))
        self.play(LaggedStart(*[FadeIn(m, scale=0.8) for m in nodos], lag_ratio=0.06),
                  Create(flechas), FadeIn(fin), *narr.decir(
                      r"Sin ciclo: siete nodos, y el último apunta a \texttt{None}"))

        def arriba(i, lado):
            return pos[i] + UP * 0.62 + RIGHT * 0.2 * lado

        tort, lieb = ficha("T", AZUL), ficha("L", AMARILLO)
        tort.move_to(arriba(0, -1))
        lieb.move_to(arriba(0, 1))
        self.play(FadeIn(tort), FadeIn(lieb))
        t = h = vueltas = lecturas = 0
        while True:
            lecturas += 1                       # primera lectura de la liebre
            if h + 1 >= n:
                break
            h1, h = h + 1, h + 2
            lecturas += 1                       # segunda lectura
            if h >= n:
                break
            t += 1
            lecturas += 1                       # la lectura de la tortuga
            vueltas += 1
            self.play(MoveAlongPath(lieb, camino(lieb.get_center(), arriba(h1, 1),
                                                 arriba(h, 1))),
                      tort.animate.move_to(arriba(t, -1)), run_time=1.0)
            self.wait(0.3)
        self.play(lieb.animate.move_to(fin.get_center() + UP * 0.62),
                  Flash(fin, color=VERDE, flash_radius=0.45),
                  *narr.decir(rf"La liebre llega al final: no hay ciclo, en {vueltas} "
                              rf"vueltas y {lecturas} lecturas", color=VERDE))
        nota = rotulo(r"La tortuga nunca se cae de la lista:\\va detrás de la liebre",
                      34, AZUL).next_to(VGroup(*nodos), DOWN, buff=0.9)
        self.play(FadeIn(nota, shift=0.15 * UP))
        self.wait(2)


class Potencial(Scene):
    def construct(self):
        narr = Narrador()
        self.add(titulo(r"Algo que baja en cada vuelta: el potencial $\Phi$"))
        nodos, flechas = lista_rho()
        self.add(nodos, flechas)
        tort, lieb = ficha("T", AZUL), ficha("L", AMARILLO)
        tort.move_to(lugar(0, -1))
        lieb.move_to(lugar(0, 1))
        self.add(tort, lieb)

        base = RIGHT * 5.6 + DOWN * 2.2
        escala = 0.42
        barra = self.barra(MU + LAM, base, escala)
        regla = formula(r"\Phi", "=", r"(\mu - k)", "+", r"\lambda", tam=40, color=DORADO)
        regla.move_to(RIGHT * 4.6 + UP * 2.3)
        valor = self.valor(MU + LAM, barra)
        # Lo que cuenta Φ en la primera fase: la cola que le falta a la tortuga y el ciclo.
        resalte = {i: nodos[i][0].copy().set_fill(opacity=0).set_stroke(DORADO, 5)
                   for i in range(N)}
        self.play(FadeIn(barra), Write(regla), FadeIn(valor),
                  *[Create(r) for r in resalte.values()],
                  *narr.decir(r"Mientras la tortuga está en la cola: lo que le falta para "
                              r"entrar, más $\lambda$"))
        self.wait(1)

        t = h = k = 0
        arco = None
        while True:
            h1 = siguiente(h)
            h = siguiente(h1)
            t = siguiente(t)
            k += 1
            anims = [MoveAlongPath(lieb, camino(lieb.get_center(), lugar(h1, 1),
                                                lugar(h, 1))),
                     tort.animate.move_to(lugar(t, -1))]
            if t < MU:
                phi = (MU - k) + LAM
                anims.append(FadeOut(resalte.pop(t - 1)))
                dicho = rf"$\Phi = ({MU} - {k}) + {LAM} = {phi}$: baja 1"
            else:
                D = (-k) % LAM
                phi = D
                nuevo_arco = self.arco_distancia(h, D)
                if arco is None:
                    nueva_regla = formula(r"\Phi", "=", "D", tam=40, color=DORADO)
                    nueva_regla.move_to(regla)
                    anims += [*[FadeOut(r) for r in resalte.values()],
                              TransformMatchingTex(regla, nueva_regla), Create(nuevo_arco)]
                    regla = nueva_regla
                    arco = nuevo_arco
                    dicho = (rf"La tortuga entra al ciclo: $\Phi$ pasa a ser $D = {D}$, "
                             r"lo que le falta a la liebre")
                else:
                    anims.append(arco.animate.become(nuevo_arco))
                    dicho = (rf"La liebre avanza 2 y la tortuga 1: $D$ baja a {D}"
                             if D else r"$D = 0$: el mismo nodo, y el algoritmo se detiene")
            nueva_barra = self.barra(phi, base, escala)
            anims += [barra.animate.become(nueva_barra),
                      valor.animate.become(self.valor(phi, nueva_barra)),
                      *narr.decir(dicho)]
            self.play(*anims, run_time=1.4)
            self.wait(0.7)
            if t == h:
                break
        cierre = rotulo(r"Un entero $\ge 0$ que baja\\en cada vuelta: a lo sumo\\"
                        r"$\Phi_0 = \mu + \lambda = n$ vueltas", 32, DORADO)
        cierre.move_to(RIGHT * 5.1 + UP * 0.3)
        self.play(FadeOut(arco), Write(cierre),
                  Flash(nodos[t], color=VERDE, flash_radius=0.6))
        self.wait(2.5)

    def barra(self, phi, base, escala):
        b = Rectangle(width=0.7, height=max(phi * escala, 0.02), stroke_width=0,
                      fill_color=DORADO, fill_opacity=0.85)
        b.move_to(base, aligned_edge=DOWN)
        return b

    def valor(self, phi, barra):
        return formula(rf"\Phi = {phi}", tam=36, color=DORADO).next_to(barra, LEFT, 0.3)

    def arco_distancia(self, h, D):
        """El tramo del ciclo que la liebre tiene que recorrer para alcanzar a la
        tortuga: D pasos desde la liebre, en el sentido del recorrido."""
        return Arc(radius=R + 0.6, start_angle=angulo(h),
                   angle=-2 * PI * D / LAM if D else -0.001, arc_center=CENTRO,
                   color=DORADO, stroke_width=7)


class EntradaAlCiclo(Scene):
    def construct(self):
        narr = Narrador()
        self.add(titulo(r"De regalo: dónde empieza el ciclo"))
        nodos, flechas = lista_rho()
        self.add(nodos, flechas)
        # Floyd hasta el encuentro, sin animar: es la escena anterior.
        t = h = k = 0
        while True:
            h, t, k = siguiente(siguiente(h)), siguiente(t), k + 1
            if t == h:
                break
        p, q = ficha("P", AZUL), ficha("Q", AMARILLO)
        p.move_to(lugar(t, -1))
        q.move_to(lugar(t, 1))
        nodos[t][0].set_stroke(VERDE)
        self.play(FadeIn(p), FadeIn(q), *narr.decir(
            rf"Se encontraron en $x_{{{t}}}$, después de $k^* = {k}$ vueltas"))
        self.wait(0.8)
        self.play(p.animate.move_to(lugar(0, -1)),
                  *narr.decir(r"Uno vuelve a la cabeza, y los dos avanzan de a uno"))
        contador = formula("j", "=", "0", tam=40).move_to(RIGHT * 5.0 + UP * 2.0)
        self.play(Write(contador))
        a, b, j = 0, t, 0
        while a != b:
            a, b, j = siguiente(a), siguiente(b), j + 1
            nuevo = formula("j", "=", str(j), tam=40).move_to(contador)
            self.play(p.animate.move_to(lugar(a, -1)), q.animate.move_to(lugar(b, 1)),
                      TransformMatchingTex(contador, nuevo), run_time=1.0)
            contador = nuevo
            self.wait(0.4)
        self.play(Flash(nodos[a], color=VERDE, flash_radius=0.6),
                  nodos[a][0].animate.set_stroke(VERDE),
                  *narr.decir(rf"Se cruzan en $x_{{{a}}}$, la entrada, después de "
                              rf"$\mu = {j}$ pasos", color=VERDE))
        razon = rotulo(r"$x_j = x_{k^* + j} \iff j \ge \mu$, porque $k^*$ es múltiplo "
                       r"de $\lambda$", 36, AMARILLO).move_to(DOWN * 2.45)
        self.play(Write(razon))
        self.wait(1.5)

        # Una vuelta más cuenta λ.
        nuevo = formula(r"\lambda", "=", "0", tam=40).move_to(contador)
        self.play(FadeOut(p), TransformMatchingTex(contador, nuevo), *narr.decir(
            r"Una vuelta más desde la entrada cuenta $\lambda$"))
        contador = nuevo
        c, vuelta = a, 0
        while True:
            c, vuelta = siguiente(c), vuelta + 1
            nuevo = formula(r"\lambda", "=", str(vuelta), tam=40).move_to(contador)
            self.play(q.animate.move_to(lugar(c, 1)), TransformMatchingTex(contador, nuevo),
                      run_time=0.7)
            contador = nuevo
            if c == a:
                break
        self.play(Create(SurroundingRectangle(contador, color=GRIS, buff=0.15)),
                  *narr.decir(rf"$\mu = {j}$ y $\lambda = {vuelta}$, con "
                              r"$2\mu + \lambda$ lecturas más"))
        self.wait(2)
