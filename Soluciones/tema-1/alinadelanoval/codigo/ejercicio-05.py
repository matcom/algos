"""Ejercicio 5 del Tema 1: detección de ciclos con dos punteros (algoritmo de Floyd).

Los bloques van en el orden de ejercicio-05.md, y cada uno imprime lo que el .md
muestra debajo de él. Ejecutarlo desde Soluciones/tema-1/alinadelanoval/:

    pip install tesserax        # para las figuras
    python codigo/ejercicio-05.py
"""

# == bloque: imports (oculto)
import math
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

# == bloque: dibujo (oculto)
def flecha(p, q, color=None, ancho=0.8, punta=3.0):
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
# Un nodo: una casilla para el nombre y otra para next.
ANCHO_NOMBRE, ANCHO_NEXT, ALTO = 30.0, 12.0, 18.0

def nodo(c, nombre, nil=False, marco=None, campo=None):
    """c es el centro del nodo entero. `marco` colorea el nodo; `campo`, la casilla next."""
    if F is None:
        return
    k = c.x - (ANCHO_NOMBRE + ANCHO_NEXT) / 2 + ANCHO_NOMBRE / 2
    n = k + ANCHO_NOMBRE / 2 + ANCHO_NEXT / 2
    color = marco or F.APAGADO
    F.Rect(ANCHO_NOMBRE, ALTO, fill=color.transparent(0.14) if marco else F.Colors.White,
           stroke=color, width=1.6 if marco else 0.9).move_to(F.Point(k, c.y))
    F.Rect(ANCHO_NEXT, ALTO, fill=campo.transparent(0.2) if campo else F.Colors.White,
           stroke=color, width=1.6 if marco else 0.9).move_to(F.Point(n, c.y))
    F._txt(nombre, F.Point(k, c.y), color=F.TINTA, size=F.PIE)
    if nil:
        F.Line(F.Point(n - ANCHO_NEXT / 2, c.y + ALTO / 2),
               F.Point(n + ANCHO_NEXT / 2, c.y - ALTO / 2), stroke=F.TINTA, width=0.9)

def campo_next(c):
    return F.Point(c.x + ANCHO_NOMBRE / 2, c.y)

def unir(a, b):
    # flecha del centro de a al borde de b, recortada contra los dos rectángulos
    dx, dy = b.x - a.x, b.y - a.y
    d = math.hypot(dx, dy)
    ux, uy = dx / d, dy / d
    w, h = (ANCHO_NOMBRE + ANCHO_NEXT) / 2 + 3, ALTO / 2 + 3
    k = min(w / abs(ux) if ux else 1e9, h / abs(uy) if uy else 1e9)
    flecha(F.Point(a.x + ux * k, a.y + uy * k), F.Point(b.x - ux * k, b.y - uy * k))

def fila(n, y, x0=0.0, paso=70.0, ultimo_nil=True, campo_ultimo=None):
    """n nodos en línea, con L.head delante; devuelve los centros."""
    centros = [F.Point(x0 + i * paso, y) for i in range(n)]
    F._txt("L.head", F.Point(x0 - 62, y), color=F.TINTA, size=F.PIE, anchor="end")
    flecha(F.Point(x0 - 58, y), F.Point(x0 - 24, y))
    for i, c in enumerate(centros):
        ult = i == n - 1
        nodo(c, f"x{F.sub(i)}", nil=ult and ultimo_nil, campo=campo_ultimo if ult else None)
        if not ult:
            F._punto(campo_next(c), F.TINTA, r=1.4)
            flecha(campo_next(c), F.Point(centros[i + 1].x - 23, y))
    return centros

def anillo(centro, C, primero, r=58.0):
    """los C nodos del ciclo en un círculo, x_primero a la izquierda y en el orden de next."""
    return [F.Point(centro.x + r * math.cos(math.pi + 2 * math.pi * i / C),
                    centro.y + r * math.sin(math.pi + 2 * math.pi * i / C))
            for i in range(C)]

# == bloque: figura entrada (oculto)
if F is not None:
    with F.Canvas() as canvas:
        fila(5, 0)
        F._txt(f"sin ciclo: n = 5, x{F.sub(5)} = NIL", F.Point(5 * 70 - 20, 0),
               color=F.APAGADO, size=F.PIE, anchor="start")
        a, C, y = 3, 5, 120
        centros = fila(a, y, ultimo_nil=False)
        ciclo = anillo(F.Point(a * 70 + 58, y), C, a)
        F._punto(campo_next(centros[-1]), F.TINTA, r=1.4)
        flecha(campo_next(centros[-1]), F.Point(ciclo[0].x - 23, y))
        for i, c in enumerate(ciclo):
            nodo(c, f"x{F.sub(a + i)}")
            unir(c, ciclo[(i + 1) % C])
        F._txt("C = 5", F.Point(a * 70 + 58, y), color=F.ACENTO, size=F.CUERPO)
        x0 = a * 70 + 58 + 100                  # "x con subíndice i+C = x con subíndice i si i ≥ a"
        for dx, texto, dy, tam in ((0, "x", 0, F.CUERPO), (5, "i+C", 3, 6.0),
                                   (17, "= x", 0, F.CUERPO), (30, "i", 3, 6.0),
                                   (35, "si i ≥ a", 0, F.CUERPO)):
            F._txt(texto, F.Point(x0 + dx, y + dy), color=F.APAGADO, size=tam,
                   anchor="start")
        F.Line(F.Point(-21, y + 20), F.Point((a - 1) * 70 + 21, y + 20),
               stroke=F.CALIDO, width=1.0)
        F._txt("a = 3 nodos antes del ciclo", F.Point((a - 1) * 35, y + 33),
               color=F.CALIDO, size=F.PIE)
    guardar(F._figura(canvas, "ejercicio-05-entrada", ""), "ejercicio-05-entrada.svg")

# == bloque: algoritmo
class Nodo:
    def __init__(self):
        self.next = None

def floyd(cabeza):
    t = h = cabeza
    while h is not None and h.next is not None:
        t = t.next
        h = h.next.next
        if t is h:
            return True
    return False

# == bloque: vigilada
def lista(a, C):
    # a nodos antes del ciclo y C en el ciclo; con C = 0, una lista sin ciclo de a nodos
    x = [Nodo() for _ in range(a + C)]
    for i in range(len(x) - 1):
        x[i].next = x[i + 1]
    if C:
        x[-1].next = x[a]
    return x

def floyd_vigilado(x, a, C):
    # el mismo algoritmo, comprobando el invariante y el potencial en cada vuelta
    def nodo_x(i):                              # x_i, o None (NIL) si la lista se acaba
        if C == 0:
            return x[i] if i < len(x) else None
        return x[i] if i < a else x[a + (i - a) % C]
    pos = {id(v): i for i, v in enumerate(x)}
    t = h = (x[0] if x else None)
    k, phi = 0, None
    while h is not None and h.next is not None:
        t = t.next
        h = h.next.next
        k += 1
        assert t is nodo_x(k) and h is nodo_x(2 * k)              # invariante
        if C == 0:
            assert len(x) - 2 * k >= 0                            # Φ = n - 2k >= 0
        elif k >= max(a, 1):
            nuevo = (pos[id(t)] - pos[id(h)]) % C                 # pasos de h hasta t
            assert phi is None or nuevo == phi - 1                # Φ baja en 1
            phi = nuevo
        if t is h:
            return True, k
    return False, k

sin_ciclo = 0
for n in range(0, 201):
    x = lista(n, 0)
    r, vueltas = floyd_vigilado(x, n, 0)
    assert r is False is floyd(x[0] if x else None) and vueltas <= n // 2
    sin_ciclo += 1

con_ciclo = 0
for a in range(0, 41):
    for C in range(1, 41):
        x = lista(a, C)
        r, vueltas = floyd_vigilado(x, a, C)
        assert r is True is floyd(x[0]) and vueltas <= max(a, 1) + C - 1 <= a + C
        con_ciclo += 1
print(f"sin ciclo, n de 0 a 200: {sin_ciclo} listas, False en todas,"
      f" a lo sumo ⌊n/2⌋ vueltas")
print(f"con ciclo, a de 0 a 40 y C de 1 a 40: {con_ciclo:,} listas, True en todas,"
      f" a lo sumo n vueltas")
print("invariante t = xₖ, h = x₂ₖ y los dos potenciales comprobados en cada vuelta")

# == bloque: traza (asis)
SUB = "₀₁₂₃₄₅₆₇₈₉"
x_ = lambda i: "x" + "".join(SUB[int(c)] for c in str(i))
a, C = 3, 5
x = lista(a, C)
pos = {id(v): i for i, v in enumerate(x)}
t = h = x[0]
k = 0
print("| vueltas | tortuga | liebre | Φ |")
print("|---|---|---|---|")
while True:
    it, ih = pos[id(t)], pos[id(h)]
    h_txt = x_(2 * k) + ("" if ih == 2 * k else f" = {x_(ih)}")
    phi = (it - ih) % C if k >= max(a, 1) else "—"
    print(f"| {k} | {x_(k)} | {h_txt} | {phi} |")
    if k and t is h:
        break
    t, h, k = t.next, h.next.next, k + 1
assert floyd(x[0]) is True and k == 5

# == bloque: figura potencial (oculto)
if F is not None:
    a, C = 3, 5
    x = lista(a, C)
    pos = {id(v): i for i, v in enumerate(x)}
    estados, t, h, k = [], x[0], x[0], 0
    while True:                                 # la misma vuelta de floyd, guardando el estado
        t, h, k = t.next, h.next.next, k + 1
        if k >= max(a, 1):
            estados.append((k, pos[id(t)], pos[id(h)], (pos[id(t)] - pos[id(h)]) % C))
        if t is h:
            break
    with F.Canvas() as canvas:
        for panel, (k, it, ih, phi) in enumerate(estados):
            centro = F.Point(panel * 190, 0)
            ciclo = anillo(centro, C, a)
            for i, c in enumerate(ciclo):
                j = a + i
                marco = (F.ALARMA if j == it == ih else F.OSCURO if j == it
                         else F.CALIDO if j == ih else None)
                nodo(c, f"x{F.sub(j)}", marco=marco)
                unir(c, ciclo[(i + 1) % C])
            if phi:                             # el arco: los Φ pasos que le faltan a h
                p, q = ciclo[ih - a], ciclo[it - a]
                medio = F.Point((p.x + q.x) / 2, (p.y + q.y) / 2)
                if phi > 1:                     # se curva hacia el camino que recorre h
                    ang = math.pi + 2 * math.pi * ((ih - a) + phi / 2) / C
                    hacia = F.Point(centro.x + 58 * math.cos(ang), centro.y + 58 * math.sin(ang))
                    f = 0.45
                else:                           # Φ = 1: hacia dentro, para no tapar la flecha
                    hacia, f = centro, 0.55
                ctrl = F.Point(medio.x + (hacia.x - medio.x) * f, medio.y + (hacia.y - medio.y) * f)
                def recortar(a_, b_, r):        # avanza r desde a_ hacia b_
                    d = math.hypot(b_.x - a_.x, b_.y - a_.y)
                    return F.Point(a_.x + (b_.x - a_.x) * r / d, a_.y + (b_.y - a_.y) * r / d)
                arco(recortar(p, ctrl, 24), recortar(q, ctrl, 24), ctrl, F.ALARMA)
            h_txt = f"x{F.sub(2 * k)}" + (f" = x{F.sub(ih)}" if ih != 2 * k else "")
            F._txt(f"k = {k}: t = x{F.sub(it)}, h = {h_txt}", F.Point(centro.x, 84),
                   color=F.TINTA, size=F.PIE)
            F._txt(f"Φ = {phi}", F.Point(centro.x, 100), color=F.ALARMA, size=F.PIE)
    guardar(F._figura(canvas, "ejercicio-05-potencial", ""), "ejercicio-05-potencial.svg")
