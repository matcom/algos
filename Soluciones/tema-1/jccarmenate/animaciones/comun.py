"""Lo que comparten las animaciones: el estilo y unos pocos ayudantes de dibujo.

El estilo es el de 3Blue1Brown: fondo oscuro, texto y fórmulas en LaTeX, y pocos
colores, cada uno con un significado fijo en todas las escenas:

    AZUL      el estado del algoritmo (la ventana, los punteros, lo que queda)
    AMARILLO  lo que se está mirando o afirmando ahora (la comparación, el invariante)
    VERDE     lo que ya está decidido y es correcto
    ROJO      el error plantado, o lo que lo delata
    DORADO    el potencial
    GRIS      lo descartado o de fondo

Cada escena corre el algoritmo de verdad y anima la traza que produce: nada se coloca
a mano, así que la animación no puede contradecir al código del ejercicio.
"""

from manim import (BLUE_C, DOWN, GOLD_C, GREEN_C, GREY_B, GREY_D, RED_C, RIGHT, UP,
                   YELLOW_C, Arrow, FadeIn, FadeOut, Line, MathTex, Rectangle, Square, Tex,
                   VGroup, config)

config.background_color = "#0f1117"

AZUL = BLUE_C
AMARILLO = YELLOW_C
VERDE = GREEN_C
ROJO = RED_C
DORADO = GOLD_C
GRIS = GREY_B
APAGADO = GREY_D
FONDO = "#0f1117"


def rotulo(s, tam=36, color="#ffffff"):
    """Texto en LaTeX, con fórmulas entre $...$."""
    return Tex(s, font_size=tam, color=color)


def formula(*partes, tam=44, color="#ffffff"):
    return MathTex(*partes, font_size=tam, color=color)


def titulo(s, tam=40):
    t = rotulo(s, tam)
    t.to_edge(UP, buff=0.4)
    return t


def celda(valor, lado=0.75, tam=34, color=GRIS, relleno=FONDO):
    """Un cuadrado con un valor adentro: VGroup(marco, valor)."""
    marco = Square(side_length=lado, stroke_color=color, stroke_width=2.5,
                   fill_color=relleno, fill_opacity=1)
    v = MathTex(str(valor), font_size=tam)
    v.move_to(marco)
    return VGroup(marco, v)


def fila(valores, lado=0.75, sep=0.0, tam=34, color=GRIS):
    f = VGroup(*[celda(v, lado, tam, color) for v in valores])
    f.arrange(RIGHT, buff=sep)
    return f


def indices(celdas, tam=24):
    """Los índices 0, 1, ... debajo de una fila de celdas."""
    return VGroup(*[MathTex(str(i), font_size=tam, color=APAGADO).next_to(c, DOWN, 0.12)
                    for i, c in enumerate(celdas)])


def borde(celdas, i):
    """El borde izquierdo de la celda i; con i = len(celdas), el derecho de la última."""
    return celdas[i].get_left() if i < len(celdas) else celdas[-1].get_right()


def ventana(celdas, lo, hi, color=AZUL):
    """El rectángulo de la ventana semiabierta [lo, hi); vacía, es una raya en lo."""
    if lo < hi:
        r = Rectangle(width=borde(celdas, hi)[0] - borde(celdas, lo)[0] + 0.12,
                      height=celdas[0].height + 0.12, stroke_color=color, stroke_width=5)
        r.move_to((borde(celdas, lo) + borde(celdas, hi)) / 2)
        return r
    return Line(borde(celdas, lo) + UP * 0.55, borde(celdas, lo) + DOWN * 0.55,
                color=color, stroke_width=6)


def puntero(celdas, i, nombre, color=AZUL, corrimiento=0.0, abajo=1.15):
    """Una flecha que sube hasta el borde i de la fila, con su nombre debajo."""
    punta = borde(celdas, i) + DOWN * (celdas[0].height / 2 + 0.08)
    flecha = Arrow(punta + DOWN * (abajo - 0.5) + RIGHT * corrimiento, punta, buff=0,
                   color=color, stroke_width=4, tip_length=0.18)
    etiqueta = MathTex(nombre, font_size=32, color=color).next_to(flecha, DOWN, 0.08)
    return VGroup(flecha, etiqueta)


class Narrador:
    """La línea de texto al pie de la escena, que cuenta qué está pasando.

    `decir` reemplaza la línea anterior con un fundido corto hacia arriba y devuelve las
    animaciones, para jugarlas junto con otras."""

    def __init__(self, tam=34):
        self.tam = tam
        self.actual = None

    def decir(self, s, color="#ffffff"):
        # \mbox: una sola línea siempre; si no entra, se achica.
        nueva = rotulo(r"\mbox{" + s + "}", self.tam, color)
        if nueva.width > 13.2:
            nueva.scale_to_fit_width(13.2)
        nueva.to_edge(DOWN, buff=0.45)
        anims = [FadeIn(nueva, shift=0.15 * UP)]
        if self.actual is not None:
            anims.append(FadeOut(self.actual, shift=0.15 * UP))
        self.actual = nueva
        return anims
