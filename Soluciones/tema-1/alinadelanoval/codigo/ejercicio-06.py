"""Ejercicio 6 del Tema 1: búsqueda en una matriz ordenada por filas y por columnas.

Los bloques van en el orden de ejercicio-06.md, y cada uno imprime lo que el .md
muestra debajo de él. Ejecutarlo desde Soluciones/tema-1/alinadelanoval/:

    pip install tesserax        # para las figuras
    python codigo/ejercicio-06.py
"""

# == bloque: imports (oculto)
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

LADO = 26.0

def matriz(M, origen, color=lambda a, b: None, marco=lambda a, b: None, titulo=""):
    # dibuja M con la casilla (a, b) en la fila a y la columna b
    x0, y0 = origen
    casillas = [(a, b) for a in range(len(M)) for b in range(len(M))]
    # las casillas con marco al final, para que su borde no quede tapado
    for a, b in sorted(casillas, key=lambda ab: marco(*ab) is not None):
        c, m = color(a, b), marco(a, b)
        F.Rect(LADO, LADO, fill=c.transparent(0.2) if c else F.Colors.White,
               stroke=m or F.REGLA.darker(0.2), width=1.6 if m else 0.7).move_to(
            F.Point(x0 + b * LADO, y0 + a * LADO), anchor="topleft")
        F._txt(str(M[a][b]), F.Point(x0 + (b + 0.5) * LADO, y0 + (a + 0.5) * LADO),
               color=F.TINTA, size=F.PIE)
    if titulo:
        F._txt(titulo, F.Point(x0 + len(M) * LADO / 2, y0 - 12), color=F.TINTA, size=F.PIE)

def centro(origen, a, b):
    return F.Point(origen[0] + (b + 0.5) * LADO, origen[1] + (a + 0.5) * LADO)

# == bloque: algoritmo
def buscar_en_matriz(M, x, comparar):
    """Devuelve ("está", (i, j)) o ("no está", None)."""
    n = len(M)
    i, j = 0, n - 1              # invariante: si x está, está en M[i..n-1][0..j]
    while i < n and j >= 0:
        r = comparar(x, M[i][j])        # -1, 0 o 1
        if r == 0:
            return ("está", (i, j))
        if r < 0:
            j -= 1               # x es menor que toda la columna j, desde la fila i
        else:
            i += 1               # x es mayor que toda la fila i, hasta la columna j
    return ("no está", None)

# == bloque: ejemplo
def contando(registro):
    # una función comparar que anota con qué casilla se comparó
    def comparar(x, y):
        registro.append(y)
        return (x > y) - (x < y)
    return comparar

M = [[1, 4, 7, 11],
     [2, 5, 8, 12],
     [3, 6, 9, 16],
     [10, 13, 14, 17]]
for x in (9, 10):
    registro = []
    resultado = buscar_en_matriz(M, x, contando(registro))
    print(f"x = {x:>2}: compara con {', '.join(map(str, registro))}"
          f"  ({len(registro)} comparaciones) -> {resultado}")

# == bloque: figura caminos (oculto)
def camino_de(M, x):
    # corre buscar_en_matriz sobre casillas (valor, posición) y anota las que compara
    casillas = [[(v, (a, b)) for b, v in enumerate(fila)] for a, fila in enumerate(M)]
    pasos = []
    def comparar(x, casilla):
        valor, posicion = casilla
        pasos.append(posicion)
        return (x > valor) - (x < valor)
    buscar_en_matriz(casillas, x, comparar)
    return pasos

if F is not None:
    with F.Canvas() as canvas:
        for panel, x in enumerate((9, 10)):
            o = (panel * 160.0, 0.0)
            pasos = camino_de(M, x)
            matriz(M, o, color=lambda a, b, p=pasos: F.ACENTO if (a, b) in p else None,
                   marco=lambda a, b, p=pasos: F.ALARMA if (a, b) == p[-1] else None,
                   titulo=f"x = {x}: {len(pasos)} comparaciones")
            for k, (a, b) in enumerate(pasos, start=1):   # el orden de las comparaciones
                F._txt(str(k), F.Point(o[0] + b * LADO + 5, o[1] + a * LADO + 6),
                       color=F.OSCURO, size=6.0)
    guardar(F._figura(canvas, "ejercicio-06-caminos", ""), "ejercicio-06-caminos.svg")

# == bloque: figura invariante (oculto)
if F is not None:
    # estado tras dos vueltas con x = 9, y las dos vueltas que lo produjeron
    estados = [(0, 3, "x < M[0][3] = 11: sale la columna 3"),
               (0, 2, "x > M[0][2] = 7: sale la fila 0")]
    with F.Canvas() as canvas:
        for panel, (i, j, texto) in enumerate(estados):
            o = (panel * 170.0, 0.0)
            r = lambda a, b, i=i, j=j: i <= a and b <= j
            fuera = (lambda a, b, i=i, j=j: b == j and a >= i) if panel == 0 else \
                    (lambda a, b, i=i, j=j: a == i and b <= j)
            matriz(M, o, color=lambda a, b, r=r, f=fuera: F.ALARMA if f(a, b) else
                   (F.ACENTO if r(a, b) else None),
                   marco=lambda a, b, i=i, j=j: F.OSCURO if (a, b) == (i, j) else None,
                   titulo=f"R({i}, {j}), comparando con ({i}, {j})")
            F._txt(texto, F.Point(o[0] + 2 * LADO, 4 * LADO + 14), color=F.ALARMA,
                   size=F.PIE)
        o = (340.0, 0.0)
        matriz(M, o, color=lambda a, b: F.ACENTO if a >= 1 and b <= 2 else None,
               marco=lambda a, b: F.OSCURO if (a, b) == (1, 2) else None,
               titulo="después: R(1, 2)")
    guardar(F._figura(canvas, "ejercicio-06-invariante", ""),
            "ejercicio-06-invariante.svg")

# == bloque: vigilada
def matriz_al_azar(n, rng):
    # filas y columnas crecientes (no estrictamente), con valores repetidos
    A = [[0] * n for _ in range(n)]
    for a in range(n):
        for b in range(n):
            A[a][b] = max(A[a - 1][b] if a else 0, A[a][b - 1] if b else 0) + rng.randint(0, 2)
    return A

def buscar_vigilado(M, x):
    # el mismo algoritmo, comprobando el invariante al comienzo de cada vuelta y al salir
    n = len(M)
    i, j, comparaciones = 0, n - 1, 0
    esta = any(x in fila for fila in M)
    while True:
        en_R = any(M[a][b] == x for a in range(i, n) for b in range(0, j + 1))
        assert en_R or not esta                 # si x está en M, está en R(i, j)
        if not (i < n and j >= 0):
            return ("no está", None), comparaciones
        comparaciones += 1
        if M[i][j] == x:
            return ("está", (i, j)), comparaciones
        if x < M[i][j]:
            j -= 1
        else:
            i += 1

rng = random.Random(6)
casos = 0
peor = {}
for _ in range(4000):
    n = rng.randint(1, 9)
    A = matriz_al_azar(n, rng)
    for x in range(-1, A[-1][-1] + 2):
        (respuesta, p), c = buscar_vigilado(A, x)
        assert (respuesta == "está") == any(x in fila for fila in A)
        assert respuesta == "no está" or A[p[0]][p[1]] == x
        assert c <= 2 * n - 1
        peor[n] = max(peor.get(n, 0), c)
        casos += 1
print(f"{casos:,} búsquedas en matrices al azar con repetidos, n de 1 a 9: 0 fallos")
print("invariante comprobado al comienzo de cada vuelta y al salir")
print("peor caso medido:", ", ".join(f"n = {n}: {peor[n]}" for n in sorted(peor)))
assert all(peor[n] == 2 * n - 1 for n in peor)

# == bloque: adversario
def A0(n):
    return [[2 * (a + b) if a + b != n - 1 else 2 * n - 3 for b in range(n)]
            for a in range(n)]

def valida(A):
    n = len(A)
    return all(A[a][b] <= A[a][b + 1] for a in range(n) for b in range(n - 1)) and \
           all(A[a][b] <= A[a + 1][b] for a in range(n - 1) for b in range(n))

def criticas(A, x):
    # las casillas que, cambiadas a x, dan una matriz válida que contiene x
    out = []
    for a in range(len(A)):
        for b in range(len(A)):
            B = [fila[:] for fila in A]
            B[a][b] = x
            if valida(B):
                out.append((a, b))
    return out

print(f"{'n':>3} {'casillas críticas':>18} {'antidiagonal':>13} {'nivel n':>8}"
      f" {'comparaciones sobre A₀':>23}")
for n in range(2, 11):
    A, x = A0(n), 2 * n - 2
    assert valida(A) and not any(x in fila for fila in A)
    crit = criticas(A, x)
    anti = [(a, b) for a, b in crit if a + b == n - 1]
    nivel = [(a, b) for a, b in crit if a + b == n]
    assert len(anti) == n and len(nivel) == n - 1 and len(crit) == 2 * n - 1
    camino = camino_de(A, x)                   # las casillas que compara el algoritmo
    assert set(crit) <= set(camino)            # las compara todas
    print(f"{n:>3} {len(crit):>18} {len(anti):>13} {len(nivel):>8} {len(camino):>23}")

# == bloque: figura adversario (oculto)
if F is not None:
    n = 4
    A, x = A0(n), 2 * n - 2
    B = [fila[:] for fila in A]
    B[2][1] = x
    with F.Canvas() as canvas:
        for panel, (Mx, titulo) in enumerate([(A, f"A₀: x = {x} no está"),
                                              (B, f"A′₂: x = {x} sí está")]):
            o = (panel * 150.0, 0.0)
            matriz(Mx, o, color=lambda a, b: F.CALIDO if a + b == n - 1 else None,
                   marco=lambda a, b, p=panel: F.ALARMA if p == 1 and (a, b) == (2, 1)
                   else None, titulo=titulo)
        F._txt("solo difieren en la casilla (2, 1)", F.Point(150.0 + 2 * LADO, 4 * LADO + 14),
               color=F.ALARMA, size=F.PIE)
    guardar(F._figura(canvas, "ejercicio-06-adversario", ""), "ejercicio-06-adversario.svg")
