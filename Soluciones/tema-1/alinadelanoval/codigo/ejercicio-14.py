"""Ejercicio 14 del Tema 1: el siguiente mayor de cada elemento.

Los bloques van en el orden de ejercicio-14.md, y cada uno imprime lo que el .md
muestra debajo de él. Ejecutarlo desde Soluciones/tema-1/alinadelanoval/:

    pip install tesserax        # para las figuras
    python codigo/ejercicio-14.py
"""

# == bloque: imports (oculto)
import random
import sys
from itertools import permutations
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

# == bloque: fuerza bruta
def fuerza_bruta(A):
    n, comparaciones, sig = len(A), 0, []
    for i in range(n):
        s = None
        for j in range(i + 1, n):
            comparaciones += 1
            if A[j] > A[i]:
                s = j
                break
        sig.append(s)
    return sig, comparaciones

print(f"{'n':>6} {'comparaciones con A decreciente':>32} {'n(n − 1)/2':>11}")
for n in [10, 100, 1000]:
    _, c = fuerza_bruta(list(range(n, 0, -1)))
    assert c == n * (n - 1) // 2
    print(f"{n:>6} {c:>32,} {n * (n - 1) // 2:>11,}")

# == bloque: algoritmo
def siguiente_mayor(A):
    n = len(A)
    sig = [None] * n             # None: no tiene siguiente mayor
    pila = []                    # posiciones a la derecha, cima = la más cercana
    for i in range(n - 1, -1, -1):
        while pila and A[pila[-1]] <= A[i]:
            pila.pop()
        if pila:
            sig[i] = pila[-1]
        pila.append(i)
    return sig

random.seed(14)
casos = 0
for _ in range(20_000):
    A = [random.randint(0, 9) for _ in range(random.randint(1, 30))]   # con repetidos
    assert siguiente_mayor(A) == fuerza_bruta(A)[0]
    casos += 1
print(f"{casos:,} arreglos al azar, con repetidos: 0 fallos contra la fuerza bruta")

# == bloque: figura pila (oculto)
def pila_al_procesar(A, i):
    # la pila justo antes y justo después del while al procesar A[i] (índices desde 0)
    pila, sig = [], [None] * len(A)
    for k in range(len(A) - 1, -1, -1):
        antes = list(pila)
        while pila and A[pila[-1]] <= A[k]:
            pila.pop()
        if pila:
            sig[k] = pila[-1]
        if k == i:
            return antes, list(pila), sig
        pila.append(k)

A = [7, 3, 5, 2, 4, 1, 6]
antes, despues, sig = pila_al_procesar(A, 2)
assert [p + 1 for p in reversed(antes)] == [4, 5, 7] and [p + 1 for p in reversed(despues + [2])] == [3, 7]
assert sig[2] == 6
if F is not None:
    paso, unidad = 32.0, 12.0
    base = 0.0
    with F.Canvas() as canvas:
        for k, v in enumerate(A):
            h = v * unidad
            if k == 2:
                color, fill = F.CALIDO, F.CALIDO.transparent(0.25)
            elif k in antes and k not in despues:
                color, fill = F.ALARMA, F.ALARMA.transparent(0.2)
            elif k in antes:
                color, fill = F.OSCURO, F.ACENTO.transparent(0.25)
            else:
                color, fill = F.APAGADO, F.Colors.White
            F.Rect(paso * 0.7, h, fill=fill, stroke=color, width=1.1).move_to(
                F.Point(k * paso, base - h), anchor="topleft")
            F._txt(str(v), F.Point(k * paso + paso * 0.35, base - h - 8), color=F.TINTA,
                   size=F.PIE)
            F._txt(str(k + 1), F.Point(k * paso + paso * 0.35, base + 14), color=F.APAGADO,
                   size=F.PIE)
            marca = "?" if k < 2 else ("–" if sig[k] is None else str(sig[k] + 1))
            F._txt(marca, F.Point(k * paso + paso * 0.35, base + 30), color=F.TINTA,
                   size=F.PIE)
        F._txt("i", F.Point(-12, base + 14), color=F.APAGADO, size=F.PIE, anchor="end")
        F._txt("sig(i)", F.Point(-12, base + 30), color=F.APAGADO, size=F.PIE, anchor="end")
        F._txt("x = A[3]", F.Point(2 * paso + paso * 0.35, base - A[2] * unidad - 22),
               color=F.CALIDO, size=F.PIE)
        x0 = len(A) * paso + 8
        F._txt("pila antes: " + ", ".join(str(p + 1) for p in reversed(antes)),
               F.Point(x0, -50), color=F.TINTA, size=F.PIE, anchor="start")
        F._txt("pila después: " + ", ".join(str(p + 1) for p in reversed(despues + [2])),
               F.Point(x0, -36), color=F.TINTA, size=F.PIE, anchor="start")
        F._txt("(cima a la izquierda)", F.Point(x0, -22), color=F.APAGADO, size=F.PIE,
               anchor="start")
    guardar(F._figura(canvas, "ejercicio-14-pila", ""), "ejercicio-14-pila.svg")

# == bloque: vigilada
def siguiente_mayor_vigilado(A):
    # el mismo algoritmo, comprobando el invariante reforzado después de cada posición
    n = len(A)
    sig, pila = [None] * n, []
    correcto = fuerza_bruta(A)[0]
    for i in range(n - 1, -1, -1):
        while pila and A[pila[-1]] <= A[i]:
            pila.pop()
        if pila:
            sig[i] = pila[-1]
        pila.append(i)
        # sig correcto en A[i..n] y la pila = las k >= i mayores que todo A[i..k-1]
        assert all(sig[k] == correcto[k] for k in range(i, n))
        esperada = [k for k in range(i, n) if all(A[k] > A[j] for j in range(i, k))]
        assert pila == list(reversed(esperada))           # la menor en la cima
    return sig

random.seed(15)
prefijos = 0
for _ in range(5_000):
    A = [random.randint(0, 9) for _ in range(random.randint(1, 20))]
    siguiente_mayor_vigilado(A)
    prefijos += len(A)
print(f"invariante comprobado en {prefijos:,} sufijos, sin fallos")

# == bloque: costo
def comparaciones_pila(A):
    # el mismo algoritmo, contando las comparaciones A[cima] <= x
    pila, c = [], 0
    for i in range(len(A) - 1, -1, -1):
        while pila:
            c += 1
            if A[pila[-1]] <= A[i]:
                pila.pop()
            else:
                break
        pila.append(i)
    return c

print(f"{'n':>3} {'peor caso (todas las permutaciones)':>36} {'2n − 2':>7}")
for n in range(1, 9):
    peor = max(comparaciones_pila(list(p)) for p in permutations(range(n)))
    assert peor <= 2 * n - 2
    print(f"{n:>3} {peor:>36} {2 * n - 2:>7}")

# == bloque: cota
def intercambiar_vecinos(n, i):
    # la entrada creciente con A[i] y A[i+1] intercambiados (posiciones desde 1)
    A = list(range(1, n + 1))
    A[i - 1], A[i] = A[i], A[i - 1]
    return A

n = 6
creciente = list(range(1, n + 1))
print(f"{'entrada':>20}  sig")
for A in [creciente] + [intercambiar_vecinos(n, i) for i in range(1, n)]:
    s = [None if k is None else k + 1 for k in siguiente_mayor(A)]
    print(f"{str(A):>20}  {' '.join('–' if k is None else str(k) for k in s)}")
# cada intercambio de vecinos cambia la respuesta: hay que comparar los n − 1 pares
assert all(siguiente_mayor(intercambiar_vecinos(n, i)) != siguiente_mayor(creciente)
           for i in range(1, n))

# == bloque: figura cota (oculto)
if F is not None:
    paso, unidad, sep = 30.0, 10.0, 230.0
    with F.Canvas() as canvas:
        for panel, (titulo, A) in enumerate([("entrada creciente", creciente),
                                             ("intercambiando A[3] y A[4]",
                                              intercambiar_vecinos(n, 3))]):
            x0 = panel * sep
            s = siguiente_mayor(A)
            for k, v in enumerate(A):
                cambiado = panel == 1 and k in (2, 3)
                color = F.ALARMA if cambiado else F.OSCURO
                F.Rect(paso * 0.7, v * unidad,
                       fill=(F.ALARMA if cambiado else F.ACENTO).transparent(0.2),
                       stroke=color, width=1.1).move_to(
                    F.Point(x0 + k * paso, -v * unidad), anchor="topleft")
                F._txt(str(k + 1), F.Point(x0 + k * paso + paso * 0.35, 14),
                       color=F.APAGADO, size=F.PIE)
                F._txt("–" if s[k] is None else str(s[k] + 1),
                       F.Point(x0 + k * paso + paso * 0.35, 30),
                       color=F.ALARMA if (panel == 1 and k == 2) else F.TINTA, size=F.PIE)
            F._txt(titulo, F.Point(x0 + n * paso / 2, -n * unidad - 16), color=F.TINTA,
                   size=F.PIE)
        F._txt("i", F.Point(-12, 14), color=F.APAGADO, size=F.PIE, anchor="end")
        F._txt("sig(i)", F.Point(-12, 30), color=F.APAGADO, size=F.PIE, anchor="end")
    guardar(F._figura(canvas, "ejercicio-14-cota", ""), "ejercicio-14-cota.svg")
