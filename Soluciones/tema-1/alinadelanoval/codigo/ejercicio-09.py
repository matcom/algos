"""Ejercicio 9 del Tema 1: la mezcla "optimizada".

Los bloques van en el orden de ejercicio-09.md, y cada uno imprime lo que el .md
muestra debajo de él. Ejecutarlo desde Soluciones/tema-1/alinadelanoval/:

    pip install tesserax        # para la figura
    python codigo/ejercicio-09.py
"""

# == bloque: imports (oculto)
import sys
from itertools import combinations
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[3] / "Lectures" / "2026"))   # donde vive figuras.py

# == bloque: algoritmo
def mezcla_optimizada(A, B):
    R, i, j = [], 0, 0
    while len(A) - i > 1 and j < len(B):
        if A[i] <= B[j]:
            R.append(A[i]); i += 1
        else:
            R.append(B[j]); j += 1
    if len(A) - i == 1:
        return R + B[j:] + [A[i]]      # lo que queda de B, y a_n al final
    return R + A[i:]                   # B se vació

# == bloque: conteo
def mezcla_optimizada_contada(A, B):
    # la misma mezcla, guardando qué pares compara
    R, i, j, comparados = [], 0, 0, []
    while len(A) - i > 1 and j < len(B):
        comparados.append((A[i], B[j]))
        if A[i] <= B[j]:
            R.append(A[i]); i += 1
        else:
            R.append(B[j]); j += 1
    if len(A) - i == 1:
        return R + B[j:] + [A[i]], comparados
    return R + A[i:], comparados

print(f"{'n':>2} {'entradas':>9} {'peor caso medido':>17} {'2n - 2':>7}")
for n in range(1, 8):
    peor = 0
    for pos_a in combinations(range(2 * n), n):     # todas las formas de repartir 1..2n
        A = [v + 1 for v in pos_a]
        B = [v + 1 for v in range(2 * n) if v not in pos_a]
        R, comparados = mezcla_optimizada_contada(A, B)
        assert R == mezcla_optimizada(A, B)
        peor = max(peor, len(comparados))
    # la entrada de la sección 3: b1 < a1 < b2 < a2 < ... < b(n-1) < a(n-1) < a_n < b_n
    A = [2 * k for k in range(1, n)] + [2 * n - 1]
    B = [2 * k - 1 for k in range(1, n)] + [2 * n]
    assert len(mezcla_optimizada_contada(A, B)[1]) == peor == 2 * n - 2
    print(f"{n:>2} {len(list(combinations(range(2 * n), n))):>9} {peor:>17} {2 * n - 2:>7}")

# == bloque: contraejemplo
def intercalada(n):
    # a1 < b1 < a2 < b2 < ... < an < bn, con valores 1, 2, ..., 2n
    return [2 * k - 1 for k in range(1, n + 1)], [2 * k for k in range(1, n + 1)]

nombre = lambda v: f"a{(v + 1) // 2}" if v % 2 else f"b{v // 2}"
n = 5
A, B = intercalada(n)
R, comparados = mezcla_optimizada_contada(A, B)
vecinos = {(v, v + 1) for v in range(1, 2 * n)}
sin_comparar = vecinos - {tuple(sorted(p)) for p in comparados}
print(f"n = {n}: {len(comparados)} comparaciones (2n - 3 = {2 * n - 3})")
print("pares de vecinos sin comparar:",
      ", ".join(f"({nombre(x)}, {nombre(y)})" for x, y in sorted(sin_comparar)))
print("salida:  ", " ".join(nombre(v) for v in R))
print("correcta:", " ".join(nombre(v) for v in sorted(A + B)))

A, B = [1, 3, 5], [2, 4, 6]
R, comparados = mezcla_optimizada_contada(A, B)
print(f"\nA = {A}, B = {B}: {len(comparados)} comparaciones, devuelve {R}")

# == bloque: figura (oculto)
try:
    import figuras as F
except ImportError:
    print("sin tesserax no se regenera la figura")
else:
    n = 5
    A, B = intercalada(n)
    _, comparados = mezcla_optimizada_contada(A, B)
    comparados = {tuple(sorted(p)) for p in comparados}
    paso = 34.0                                       # la disposición de F.intercalado
    pos = {v: F.Point((v - 1) * paso, 0 if v % 2 else 46) for v in range(1, 2 * n + 1)}
    with F.Canvas() as canvas:
        for v in range(1, 2 * n):
            hecho = (v, v + 1) in comparados
            F.Line(pos[v], pos[v + 1], stroke=F.CALIDO if hecho else F.ALARMA,
                   width=1.4 if hecho else 1.0)
        for v, p in pos.items():
            F.Circle(10, fill=F.Colors.White, stroke=F.TINTA, width=0.9).move_to(p)
            letra, k = ("a", (v + 1) // 2) if v % 2 else ("b", v // 2)
            F._txt(f"{letra}{F.sub(k)}", p, color=F.TINTA, size=F.PIE)
        F._txt("lista A", F.Point(-20, 0), color=F.APAGADO, size=F.PIE, anchor="end")
        F._txt("lista B", F.Point(-20, 46), color=F.APAGADO, size=F.PIE, anchor="end")
        F._txt(f"{len(comparados)} comparaciones (ámbar); "
               f"{2 * n - 1 - len(comparados)} pares de vecinos sin comparar (rojo)",
               F.Point((2 * n - 1) * paso / 2, 76), color=F.APAGADO, size=F.PIE)
    figura = F._figura(canvas, "ejercicio-09-adversario", "")
    svg = figura[figura.index("<svg"):figura.index("</svg>") + len("</svg>")]
    vb = svg.split('viewBox="')[1].split('"')[0].split()   # fondo blanco para GitHub
    fondo = f'<rect x="{vb[0]}" y="{vb[1]}" width="{vb[2]}" height="{vb[3]}" fill="white"/>'
    (AQUI.parent / "figuras" / "ejercicio-09-adversario.svg").write_text(
        svg.replace(">", ">" + fondo, 1), encoding="utf-8")
