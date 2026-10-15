"""Ejercicio 10 del Tema 1: par más cercano en una dimensión.

Los bloques van en el orden de ejercicio-10.md, y cada uno imprime lo que el .md
muestra debajo de él. Ejecutarlo desde Soluciones/tema-1/alinadelanoval/:

    pip install tesserax        # para las figuras
    python codigo/ejercicio-10.py
"""

# == bloque: imports (oculto)
import math
import random
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[3] / "Lectures" / "2026"))   # donde vive figuras.py
try:
    import figuras as F
except ImportError:
    F = None
    print("sin tesserax no se regeneran las figuras")

def guardar(figura, nombre):
    svg = figura[figura.index("<svg"):figura.index("</svg>") + len("</svg>")]
    vb = svg.split('viewBox="')[1].split('"')[0].split()   # fondo blanco para GitHub
    fondo = f'<rect x="{vb[0]}" y="{vb[1]}" width="{vb[2]}" height="{vb[3]}" fill="white"/>'
    (AQUI.parent / "figuras" / nombre).write_text(svg.replace(">", ">" + fondo, 1),
                                                  encoding="utf-8")

def tope(x1, x2, y, texto, color, dy=-8):
    """Una cota con topes verticales en los extremos, sin puntas de flecha."""
    F.Line(F.Point(x1, y), F.Point(x2, y), stroke=color, width=1.0)
    for xx in (x1, x2):
        F.Line(F.Point(xx, y - 4), F.Point(xx, y + 4), stroke=color, width=1.0)
    F._txt(texto, F.Point((x1 + x2) / 2, y + dy), color=color, size=F.PIE)

def flecha(p, q, color=None, ancho=0.8, punta=4.0):
    """Una flecha fina con punta pequeña: la línea termina donde empieza la punta."""
    color = color or F.TINTA
    d = math.hypot(q.x - p.x, q.y - p.y)
    ux, uy = (q.x - p.x) / d, (q.y - p.y) / d
    base = F.Point(q.x - ux * punta * 1.6, q.y - uy * punta * 1.6)
    F.Line(p, base, stroke=color, width=ancho)
    F.Polyline([q, F.Point(base.x - uy * punta * 0.7, base.y + ux * punta * 0.7),
                F.Point(base.x + uy * punta * 0.7, base.y - ux * punta * 0.7)],
               closed=True, fill=color, stroke=color, width=0.5)

def arco(p, q, control, color, ancho=1.6, punta=5.0, pasos=24):
    """Un arco (Bézier cuadrática de p a q) con punta pequeña en q."""
    pts = [F.Point((1 - t) ** 2 * p.x + 2 * (1 - t) * t * control.x + t * t * q.x,
                   (1 - t) ** 2 * p.y + 2 * (1 - t) * t * control.y + t * t * q.y)
           for t in (k / pasos for k in range(pasos + 1))]
    F.Polyline(pts[:-2], stroke=color, width=ancho)
    flecha(pts[-3], pts[-1], color=color, ancho=ancho, punta=punta)

def coma(x, d=1):
    return f"{x:.{d}f}".replace(".", ",")

# == bloque: figura arbol (oculto)
if F is not None:
    guardar(F.arbol_decision(ident="ejercicio-10-arbol"), "ejercicio-10-arbol.svg")

# == bloque: fuerza bruta (oculto)
def delta(X):
    # la distancia mínima, por fuerza bruta sobre la lista ordenada
    Y = sorted(X)
    return min(b - a for a, b in zip(Y, Y[1:]))


# == bloque: figura reduccion (oculto)
if F is not None:
    xs = [1.0, 2.5, 3.6, 5.0, 5.0, 7.3, 8.6]
    ancho = 300.0
    px = lambda x: (x - min(xs)) / (max(xs) - min(xs)) * ancho
    with F.Canvas() as canvas:
        F._txt("distinción de elementos: ¿hay dos xᵢ iguales?",
               F.Point(ancho / 2, -36), color=F.TINTA, size=F.CUERPO)
        F.Line(F.Point(-14, 0), F.Point(ancho + 14, 0), stroke=F.APAGADO, width=1.0)
        for x in xs:
            F._punto(F.Point(px(x), 0), F.TINTA, r=2.8)
        rep = [x for x in set(xs) if xs.count(x) > 1][0]
        F._txt(f"{coma(rep)} dos veces", F.Point(px(rep), -14), color=F.TINTA, size=F.PIE)
        for x in set(xs):
            flecha(F.Point(px(x), 14), F.Point(px(x), 54), color=F.ACENTO, ancho=0.9)
        F._txt("xᵢ ↦ xᵢ", F.Point(ancho + 22, 33), color=F.ACENTO, size=F.PIE,
               anchor="start")
        F.Rect(ancho + 40, 40, stroke=F.REGLA, width=1.0).move_to(F.Point(ancho / 2, 78))
        F.Line(F.Point(-14, 78), F.Point(ancho + 14, 78), stroke=F.APAGADO, width=1.0)
        for x in xs:
            F._punto(F.Point(px(x), 78), F.OSCURO, r=2.8)
        F.Circle(11, stroke=F.ALARMA, width=1.3).move_to(F.Point(px(rep), 78))
        F._txt("distancia 0", F.Point(px(rep), 92), color=F.ALARMA, size=F.PIE)
        F._txt("par más cercano: ¿es 0 la distancia mínima?",
               F.Point(ancho / 2, 118), color=F.TINTA, size=F.CUERPO)
        F._txt("la construcción es la identidad y no prueba el signo de ningún polinomio",
               F.Point(ancho / 2, 134), color=F.APAGADO, size=F.PIE)
    guardar(F._figura(canvas, "ejercicio-10-reduccion", ""), "ejercicio-10-reduccion.svg")

# == bloque: figura composicion (oculto)
if F is not None:
    with F.Canvas() as canvas:
        ancho, alto = 280.0, 74.0
        F.Polyline([F.Point(0, alto), F.Point(ancho / 2, 0), F.Point(ancho, alto),
                    F.Point(0, alto)], stroke=F.CALIDO, width=1.2,
                   fill=F.CALIDO.transparent(0.14))
        F._txt("árbol para par más cercano", F.Point(ancho / 2, alto - 26),
               color=F.TINTA, size=F.CUERPO)
        F._txt("sobre la misma lista", F.Point(ancho / 2, alto - 12), color=F.APAGADO,
               size=F.PIE)
        pruebas = [("x₁ − x₄", 40), ("x₂ − x₅", 120), ("x₃ − x₇", 240)]
        for texto, x in pruebas:
            F.Line(F.Point(x, alto), F.Point(x, alto + 14), stroke=F.APAGADO, width=0.9)
            F.Rect(70, 16, fill=F.ACENTO.transparent(0.14), stroke=F.OSCURO,
                   width=0.9).move_to(F.Point(x, alto + 22))
            F._txt(f"signo de {texto}", F.Point(x, alto + 22), color=F.TINTA, size=F.PIE)
            for dx, etq, color in ((-16, "= 0: sí", F.ALARMA), (16, "≠ 0: no", F.OSCURO)):
                F.Line(F.Point(x, alto + 30), F.Point(x + dx, alto + 46),
                       stroke=F.APAGADO, width=0.8)
                F._txt(etq, F.Point(x + dx, alto + 54), color=color, size=F.PIE)
        F._txt("···", F.Point(180, alto + 22), color=F.APAGADO, size=F.CUERPO)
        F.Line(F.Point(ancho + 18, 0), F.Point(ancho + 18, alto), stroke=F.APAGADO, width=0.9)
        F._txt("T(n)", F.Point(ancho + 24, alto / 2), color=F.CALIDO, size=F.CUERPO,
               anchor="start")
        F.Line(F.Point(ancho + 18, alto + 14), F.Point(ancho + 18, alto + 30),
               stroke=F.APAGADO, width=0.9)
        F._txt("+1", F.Point(ancho + 24, alto + 22), color=F.OSCURO, size=F.CUERPO,
               anchor="start")
    guardar(F._figura(canvas, "ejercicio-10-composicion", ""),
            "ejercicio-10-composicion.svg")

# == bloque: algoritmo
def par_mas_cercano_1d_aleatorio(X, semilla=0):
    pts = list(X)
    random.Random(semilla).shuffle(pts)
    d, par = abs(pts[0] - pts[1]), (pts[0], pts[1])
    if d == 0:                                 # repetidos: la respuesta es 0
        return 0, par
    lado = d / 2
    celda = lambda q: int(q // lado)
    rejilla = {celda(q): q for q in pts[:2]}
    for i in range(2, len(pts)):
        p = pts[i]
        antes, c = d, celda(p)
        for dc in (-2, -1, 0, 1, 2):           # las 5 celdas vecinas
            q = rejilla.get(c + dc)
            if q is not None and abs(p - q) < d:
                d, par = abs(p - q), (p, q)
        if d == 0:                             # p repite un valor
            return 0, par
        if d < antes:                          # delta bajó: reconstruir
            lado = d / 2                       # `celda` lee el nuevo lado
            rejilla = {celda(q): q for q in pts[:i + 1]}
        else:
            rejilla[c] = p
    return d, par

# == bloque: comprobacion
random.seed(11)
casos, fallos = 0, 0
for _ in range(20_000):
    n = random.randint(2, 40)
    if random.random() < 0.5:
        X = [random.uniform(-100, 100) for _ in range(n)]          # sin repetidos
    else:
        X = [random.randint(0, 60) for _ in range(n)]              # con repetidos
    d, (p, q) = par_mas_cercano_1d_aleatorio(X, semilla=casos)
    fallos += d != delta(X) or abs(p - q) != d
    casos += 1
print(f"{casos:,} listas de 2 a 40 números, con y sin repetidos:"
      f" {fallos} fallos contra la fuerza bruta")

# == bloque: figura rejilla (oculto)
def rejilla_en_paso(pts, paso):
    # el algoritmo con el orden ya fijado, detenido justo antes de insertar pts[paso]
    d = abs(pts[0] - pts[1])
    lado = d / 2
    celda = lambda q: int(q // lado)
    g = {celda(q): q for q in pts[:2]}
    for i in range(2, paso):
        p, antes, c = pts[i], d, celda(pts[i])
        for dc in (-2, -1, 0, 1, 2):
            q = g.get(c + dc)
            if q is not None and abs(p - q) < d:
                d = abs(p - q)
        if d < antes:
            lado = d / 2
            g = {celda(q): q for q in pts[:i + 1]}
        else:
            g[c] = p
    return g, d, lado

ejemplo = [3.1, 9.4, 0.4, 7.9, 5.2, 1.0, 12.6, 6.0]
g, d, lado = rejilla_en_paso(ejemplo, 3)
p4 = ejemplo[3]
c4 = int(p4 // lado)
cerca = [q for q in g.values() if abs(q - p4) < d]
assert math.isclose(d, 2.7) and math.isclose(lado, 1.35) and c4 == 5
assert cerca == [9.4] and math.isclose(abs(9.4 - p4), 1.5) and len(g) == 3
if F is not None:
    paso = 34.0
    x = lambda v: v / lado * paso
    with F.Canvas() as canvas:
        for k in range(0, 9):
            F.Rect(paso, 20, stroke=F.REGLA.darker(0.12), width=0.7).move_to(
                F.Point(k * paso, 0), anchor="topleft")
            F._txt(str(k), F.Point((k + 0.5) * paso, 30), color=F.APAGADO, size=F.PIE)
        F.Rect(5 * paso, 20, fill=F.ACENTO.transparent(0.14), stroke=F.ACENTO,
               width=1.5).move_to(F.Point((c4 - 2) * paso, 0), anchor="topleft")
        for q in g.values():
            F._punto(F.Point(x(q), 10), F.APAGADO, r=2.5)
            F._txt(coma(q), F.Point(x(q), -10), color=F.TINTA, size=F.PIE)
        F._punto(F.Point(x(p4), 10), F.ALARMA, r=3.4)
        F._txt(f"p₄ = {coma(p4)}", F.Point(x(p4), -10), color=F.ALARMA, size=F.PIE,
               anchor="end")
        tope(x(p4 - d), x(p4 + d), -26, f"a menos de δ = {coma(d)} de p₄", F.ALARMA,
             dy=-10)
        tope(0, paso, 46, f"δ/2 = {coma(lado, 2)}", F.CALIDO, dy=12)
        F._txt(f"celda de p₄: ⌊{coma(p4)}/{coma(lado, 2)}⌋ = {c4};"
               f" se consultan las celdas {c4 - 2}, …, {c4 + 2}",
               F.Point(5.5 * paso, 58), color=F.APAGADO, size=F.PIE)
    guardar(F._figura(canvas, "ejercicio-10-rejilla", ""), "ejercicio-10-rejilla.svg")
