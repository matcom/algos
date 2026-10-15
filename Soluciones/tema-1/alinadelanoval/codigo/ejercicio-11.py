"""Ejercicio 11 del Tema 1: la mochila entera, medida en bits.

Los bloques van en el orden de ejercicio-11.md, y cada uno imprime lo que el .md
muestra debajo de él. Ejecutarlo desde Soluciones/tema-1/alinadelanoval/:

    pip install tesserax        # para la figura
    python codigo/ejercicio-11.py
"""

# == bloque: imports (oculto)
import math
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[3] / "Lectures" / "2026"))   # donde vive figuras.py

# == bloque: algoritmo
def mochila(v, w, n, W):
    celdas = 0
    c = [[0] * (W + 1) for _ in range(n + 1)]       # fila 0 y columna 0 valen 0
    for i in range(1, n + 1):
        for x in range(1, W + 1):
            celdas += 1
            if w[i - 1] <= x:
                if v[i - 1] + c[i - 1][x - w[i - 1]] > c[i - 1][x]:
                    c[i][x] = v[i - 1] + c[i - 1][x - w[i - 1]]
                else:
                    c[i][x] = c[i - 1][x]
            else:
                c[i][x] = c[i - 1][x]
    return c[n][W], celdas

v, w = [4, 6, 9], [3, 5, 7]
for W in [100, 10_000, 1_000_000]:
    optimo, celdas = mochila(v, w, 3, W)
    print(f"W = {W:>9,}   óptimo: {optimo}   celdas: {celdas:>9,}")

# == bloque: bits
segundos_por_año = 3600 * 24 * 365
n = 100

for bits in [16, 32, 64, 128, 256]:
    celdas = (n + 1) * 2 ** bits
    segundos = celdas / 10**9
    if segundos < 60:
        tiempo = f"{segundos:.3g} segundos"
    elif segundos < 3600:
        tiempo = f"{segundos / 60:.3g} minutos"
    else:
        tiempo = f"{segundos / segundos_por_año:.3g} años"
    print(f"{bits:>5} bits   {float(celdas):>9.3g} celdas   {tiempo}")

# == bloque: primalidad
def es_primo(n):
    divisiones = 0
    d = 2
    while d * d <= n:
        divisiones += 1
        if n % d == 0:
            return False, divisiones
        d += 1
    return n >= 2, divisiones

def primo_de(b):
    # el mayor primo de b bits
    p = 2 ** b - 1
    while not es_primo(p)[0]:
        p -= 1
    return p

print(f"{'b':>3} {'primo de b bits':>16} {'divisiones':>11} {'2^(b/2)':>9}")
for b in [10, 20, 30, 40]:
    p = primo_de(b)
    _, divisiones = es_primo(p)
    print(f"{b:>3} {p:>16,} {divisiones:>11,} {2 ** (b / 2):>9,.0f}")
for W in [100, 10_000, 1_000_000]:
    b = W.bit_length()
    assert mochila(v, w, 3, W)[1] == 3 * W and W < 2 ** b    # n·W celdas, W < 2^b

# == bloque: figura (oculto)
try:
    import figuras as F
except ImportError:
    print("sin tesserax no se regenera la figura")
else:
    bs = list(range(8, 129, 8))
    mochila_log = [math.log10((n + 1) * 2 ** b) for b in bs]       # n = 100 objetos
    primo_log = [math.log10(2 ** (b / 2)) for b in bs]
    año = math.log10(10**9 * segundos_por_año)                    # un año a 10^9 op/s
    ancho, alto = 320.0, 170.0
    y1 = math.ceil(max(mochila_log) / 10) * 10
    px = lambda b: (b - bs[0]) / (bs[-1] - bs[0]) * ancho
    py = lambda e: alto - e / y1 * alto
    with F.Canvas() as canvas:
        for e in range(0, y1 + 1, 10):
            F.Line(F.Point(0, py(e)), F.Point(ancho, py(e)), stroke=F.REGLA, width=0.7)
            F._txt(f"10{F.sup(e)}", F.Point(-8, py(e)), color=F.APAGADO, size=F.PIE,
                   anchor="end")
        for b in range(16, 129, 16):
            F._txt(str(b), F.Point(px(b), alto + 12), color=F.APAGADO, size=F.PIE)
        F.Line(F.Point(0, py(año)), F.Point(ancho, py(año)), stroke=F.ALARMA, width=1.0)
        F._txt("un año a 10⁹ por segundo", F.Point(4, py(año) - 7), color=F.ALARMA,
               size=F.PIE, anchor="start")
        for serie, color, nombre in ((mochila_log, F.CALIDO, "mochila: (n + 1)·2^b celdas"),
                                     (primo_log, F.OSCURO, "primalidad: 2^(b/2) divisiones")):
            F.Polyline([F.Point(px(b), py(e)) for b, e in zip(bs, serie)], stroke=color,
                       width=1.7)
            F._txt(nombre, F.Point(ancho + 8, py(serie[-1])), color=color, size=F.PIE,
                   anchor="start")
        F._txt("b, bits del número", F.Point(ancho / 2, alto + 30), color=F.APAGADO,
               size=F.PIE)
        F._txt("operaciones", F.Point(-8, -12), color=F.APAGADO, size=F.PIE, anchor="end")
    figura = F._figura(canvas, "ejercicio-11-bits", "")
    svg = figura[figura.index("<svg"):figura.index("</svg>") + len("</svg>")]
    vb = svg.split('viewBox="')[1].split('"')[0].split()   # fondo blanco para GitHub
    fondo = f'<rect x="{vb[0]}" y="{vb[1]}" width="{vb[2]}" height="{vb[3]}" fill="white"/>'
    (AQUI.parent / "figuras" / "ejercicio-11-bits.svg").write_text(
        svg.replace(">", ">" + fondo, 1), encoding="utf-8")
