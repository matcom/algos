"""Ejercicio 3 del Tema 1: una pila con mínimo en O(1) en el peor caso.

Los bloques van en el orden de ejercicio-03.md, y cada uno imprime lo que el .md
muestra debajo de él. Ejecutarlo desde Soluciones/tema-1/alinadelanoval/:

    pip install tesserax        # para la figura
    python codigo/ejercicio-03.py
"""

# == bloque: imports (oculto)
import random
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[3] / "Lectures" / "2026"))   # donde vive figuras.py

# == bloque: algoritmo
class PilaMin:
    def __init__(self):
        self.S, self.M = [], []

    def push(self, x):
        self.M.append(x if not self.M else min(self.M[-1], x))
        self.S.append(x)

    def pop(self):
        self.M.pop()
        return self.S.pop()

    def minimo(self):
        return self.M[-1]

# == bloque: traza (oculto)
operaciones = [("push", 5), ("push", 3), ("push", 7), ("push", 3), ("pop",), ("pop",),
               ("pop",)]
traza, p = [], PilaMin()
for op in operaciones:
    getattr(p, op[0])(*op[1:])
    traza.append((" ".join(map(str, op)), list(p.S), list(p.M), p.minimo()))

try:
    import figuras as F
except ImportError:
    print("sin tesserax no se regenera la figura")
else:
    paso, lado, alto_fila = 30.0, 22.0, 26.0
    with F.Canvas() as canvas:
        for t, (op, S, M, minimo) in enumerate(traza):
            y = t * (2 * alto_fila + 16)
            F._txt(op, F.Point(-28, y + alto_fila / 2), color=F.TINTA, size=F.CUERPO,
                   anchor="end")
            for fila, (nombre, pila) in enumerate((("S", S), ("M", M))):
                yy = y + fila * alto_fila
                F._txt(nombre, F.Point(-8, yy), color=F.APAGADO, size=F.PIE, anchor="end")
                for i, v in enumerate(pila):
                    cima = i == len(pila) - 1
                    tintada = nombre == "M"
                    F.Rect(lado, lado,
                           fill=F.ACENTO.transparent(0.16) if tintada else F.Colors.White,
                           stroke=F.OSCURO if (tintada and cima) else F.APAGADO,
                           width=1.5 if (tintada and cima) else 0.9
                           ).move_to(F.Point(10 + i * paso, yy))
                    F._txt(str(v), F.Point(10 + i * paso, yy),
                           color=F.TINTA, size=F.CUERPO)
            F._txt(f"minimo = {minimo}", F.Point(10 + 4 * paso + 12, y + alto_fila),
                   color=F.CALIDO, size=F.PIE, anchor="start")
    figura = F._figura(canvas, "ejercicio-03-traza", "")
    svg = figura[figura.index("<svg"):figura.index("</svg>") + len("</svg>")]
    vb = svg.split('viewBox="')[1].split('"')[0].split()   # fondo blanco para GitHub
    fondo = f'<rect x="{vb[0]}" y="{vb[1]}" width="{vb[2]}" height="{vb[3]}" fill="white"/>'
    (AQUI.parent / "figuras" / "ejercicio-03-traza.svg").write_text(
        svg.replace(">", ">" + fondo, 1), encoding="utf-8")

# == bloque: vigilada
def comprobar_invariante(p):
    # M[i] es el mínimo de S[0..i], para cada i
    assert len(p.M) == len(p.S)
    assert all(p.M[i] == min(p.S[:i + 1]) for i in range(len(p.S)))

random.seed(1)
operaciones = 0
for _ in range(3000):
    p, modelo = PilaMin(), []                   # modelo: una lista sin trucos
    for _ in range(random.randint(1, 30)):
        if modelo and random.random() < 0.4:
            assert p.pop() == modelo.pop()
        else:
            x = random.randint(0, 4)            # valores pequeños: muchos repetidos
            p.push(x)
            modelo.append(x)
        comprobar_invariante(p)
        if modelo:
            assert p.minimo() == min(modelo)
        operaciones += 1
print(f"invariante y minimo comprobados tras {operaciones:,} operaciones, sin fallos")
