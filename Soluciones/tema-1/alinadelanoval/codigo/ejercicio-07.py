"""Ejercicio 7 del Tema 1: el n-ésimo menor de dos arreglos ordenados de largo n.

Los bloques van en el orden de ejercicio-07.md, y cada uno imprime lo que el .md
muestra debajo de él. Ejecutarlo desde Soluciones/tema-1/alinadelanoval/:

    pip install tesserax        # para la figura
    python codigo/ejercicio-07.py
"""

# == bloque: imports (oculto)
import math
import random
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[3] / "Lectures" / "2026"))   # donde vive figuras.py

# == bloque: algoritmo
def mediana(a, b):
    """Devuelve el n-ésimo menor de a y b, ordenados y de largo n."""
    n = len(a)
    lo, hi = 0, n                         # invariante: todo corte válido está en [lo, hi]
    while lo <= hi:
        mid1 = (lo + hi) // 2             # cuántos tomo de a
        mid2 = n - mid1                   # cuántos tomo de b
        l1 = a[mid1 - 1] if mid1 > 0 else float('-inf')    # último tomado de a
        r1 = a[mid1]      if mid1 < n else float('inf')    # primero dejado en a
        l2 = b[mid2 - 1] if mid2 > 0 else float('-inf')    # último tomado de b
        r2 = b[mid2]      if mid2 < n else float('inf')    # primero dejado en b
        if l1 <= r2 and l2 <= r1:         # corte válido
            return max(l1, l2)
        if l1 > r2:
            hi = mid1 - 1                 # falla el cruce 1: sobran de a
        else:
            lo = mid1 + 1                 # falla el cruce 2: faltan de a

# == bloque: ejemplo
def vueltas(a, b):
    # las mismas vueltas de mediana, devolviendo el estado de cada una
    n, lo, hi = len(a), 0, len(a)
    while lo <= hi:
        mid1 = (lo + hi) // 2
        mid2 = n - mid1
        l1 = a[mid1 - 1] if mid1 > 0 else -math.inf
        r1 = a[mid1] if mid1 < n else math.inf
        l2 = b[mid2 - 1] if mid2 > 0 else -math.inf
        r2 = b[mid2] if mid2 < n else math.inf
        valido = l1 <= r2 and l2 <= r1
        yield lo, hi, mid1, mid2, l1, r1, l2, r2
        if valido:
            return
        if l1 > r2:
            hi = mid1 - 1
        else:
            lo = mid1 + 1

a = [2, 5, 9, 14, 20, 23, 27, 31]
b = [1, 3, 4, 8, 11, 12, 17, 30]
print(f"{'lo':>2} {'hi':>2} {'Φ':>2} {'mid1':>4} {'mid2':>4}  {'l1, r1':>7}  {'l2, r2':>7}   qué hace")
for lo, hi, mid1, mid2, l1, r1, l2, r2 in vueltas(a, b):
    if l1 <= r2 and l2 <= r1:
        hace = f"return max({l1}, {l2}) = {max(l1, l2)}"
    elif l1 > r2:
        hace = f"{l1} > {r2}: hi = {mid1 - 1}"
    else:
        hace = f"{l2} > {r1}: lo = {mid1 + 1}"
    print(f"{lo:>2} {hi:>2} {hi - lo + 1:>2} {mid1:>4} {mid2:>4}  {f'{l1}, {r1}':>7}  {f'{l2}, {r2}':>7}   {hace}")
print(f"\nmediana(a, b) = {mediana(a, b)};  sorted(a + b)[n - 1] = {sorted(a + b)[len(a) - 1]}")

# == bloque: figura (oculto)
try:
    import figuras as F
except ImportError:
    print("sin tesserax no se regenera la figura")
else:
    *_, (lo, hi, mid1, mid2, l1, r1, l2, r2) = vueltas(a, b)     # la última vuelta
    paso, lado, sep = 32.0, 24.0, 52.0
    centro = lambda fila, i: F.Point(i * paso, fila * sep)
    with F.Canvas() as canvas:
        for fila, (nombre, arr, tomados, color) in enumerate(
                (("a", a, mid1, F.ACENTO), ("b", b, mid2, F.CALIDO))):
            F._txt(nombre, F.Point(-paso + 4, fila * sep), color=color, size=F.CUERPO)
            for i, v in enumerate(arr):
                respuesta = v == max(l1, l2) and i == tomados - 1
                F.Rect(lado, lado, fill=color.transparent(0.2) if i < tomados else F.Colors.White,
                       stroke=F.ALARMA if respuesta else (color if i < tomados else F.APAGADO),
                       width=1.8 if respuesta else 0.9).move_to(centro(fila, i))
                F._txt(str(v), centro(fila, i), color=F.TINTA, size=F.CUERPO)
            x = (tomados - 0.5) * paso                         # la barra del corte
            F.Line(F.Point(x, fila * sep - 16), F.Point(x, fila * sep + 16),
                   stroke=F.TINTA, width=2.2)
        # cruce 1: último tomado de a contra primero dejado de b; cruce 2, al revés
        F.Line(centro(0, mid1 - 1) + F.Point(0, 13), centro(1, mid2) - F.Point(0, 13),
               stroke=F.OSCURO, width=1.2)
        F.Line(centro(1, mid2 - 1) - F.Point(0, 13), centro(0, mid1) + F.Point(0, 13),
               stroke=F.CALIDO, width=1.2)
        F._txt(f"cruce 1: {l1} ≤ {r2}", F.Point(len(a) * paso, sep / 2 - 8),
               color=F.OSCURO, size=F.PIE, anchor="start")
        F._txt(f"cruce 2: {l2} ≤ {r1}", F.Point(len(a) * paso, sep / 2 + 8),
               color=F.CALIDO, size=F.PIE, anchor="start")
    figura = F._figura(canvas, "ejercicio-07-corte", "")
    svg = figura[figura.index("<svg"):figura.index("</svg>") + len("</svg>")]
    vb = svg.split('viewBox="')[1].split('"')[0].split()   # fondo blanco para GitHub
    fondo = f'<rect x="{vb[0]}" y="{vb[1]}" width="{vb[2]}" height="{vb[3]}" fill="white"/>'
    (AQUI.parent / "figuras" / "ejercicio-07-corte.svg").write_text(
        svg.replace(">", ">" + fondo, 1), encoding="utf-8")

# == bloque: vigilada
def cortes_validos(a, b):
    n = len(a)
    ext = lambda arr, i: -math.inf if i < 0 else math.inf if i >= n else arr[i]
    return [i for i in range(n + 1)
            if ext(a, i - 1) <= ext(b, n - i) and ext(b, n - i - 1) <= ext(a, i)]

random.seed(7)
pares = 0
for _ in range(50_000):
    n = random.randint(1, 20)
    a = sorted(random.randint(0, 9) for _ in range(n))       # valores pequeños: repetidos
    b = sorted(random.randint(0, 9) for _ in range(n))
    validos = cortes_validos(a, b)
    assert validos                                            # siempre hay un corte válido
    phi_antes, k = None, 0
    for lo, hi, *_ in vueltas(a, b):
        k += 1
        assert all(lo <= i <= hi for i in validos)            # invariante
        phi = hi - lo + 1
        assert phi >= 1 and (phi_antes is None or phi <= phi_antes // 2)   # potencial
        phi_antes = phi
    assert k <= math.floor(math.log2(n + 1)) + 1
    assert mediana(a, b) == sorted(a + b)[n - 1]
    pares += 1
print(f"{pares:,} pares al azar con repetidos, n de 1 a 20: 0 fallos")
print("invariante, Φ ≤ ⌊Φ/2⌋ y a lo sumo ⌊log2(n + 1)⌋ + 1 vueltas en todos")

# == bloque: familia
familia = [([3, 5, 6], [1, 2, 4], "a", 0), ([1, 3, 5], [2, 4, 6], "a", 1),
           ([1, 2, 3], [4, 5, 6], "a", 2), ([1, 2, 4], [3, 5, 6], "b", 0),
           ([2, 4, 6], [1, 3, 5], "b", 1), ([4, 5, 6], [1, 2, 3], "b", 2)]
n = 3
print(f"{'a':>10} {'b':>10}   3.º menor   valor")
for a, b, arreglo, k in familia:
    valor = (a if arreglo == "a" else b)[k]
    assert len(set(a + b)) == 2 * n and sorted(a + b)[n - 1] == valor   # valores distintos
    print(f"{str(a):>10} {str(b):>10}   {arreglo}[{k}]{valor:>10}")
posiciones = {(arreglo, k) for _, _, arreglo, k in familia}
print(f"{len(posiciones)} posiciones distintas = 2n; ⌈log2(2n)⌉ = {math.ceil(math.log2(2 * n))}")
