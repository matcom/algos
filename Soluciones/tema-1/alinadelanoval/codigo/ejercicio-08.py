"""Ejercicio 8 del Tema 1: el elemento que aparece más de n/3 veces.

Los bloques van en el orden de ejercicio-08.md, y cada uno imprime lo que el .md
muestra debajo de él. Ejecutarlo desde Soluciones/tema-1/alinadelanoval/:

    pip install tesserax        # para la figura
    python codigo/ejercicio-08.py
"""

# == bloque: imports (oculto)
import random
import sys
from collections import Counter
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[3] / "Lectures" / "2026"))   # donde vive figuras.py

# == bloque: algoritmo
def mayoria_tercio(A):
    candidato1, c1, candidato2, c2 = None, 0, None, 0
    for x in A:                      # primera pasada: cancelar
        if x == candidato1:
            c1 += 1
        elif x == candidato2:
            c2 += 1
        elif c1 == 0:
            candidato1, c1 = x, 1
        elif c2 == 0:
            candidato2, c2 = x, 1
        else:
            c1 -= 1
            c2 -= 1
    # segunda pasada: verificar
    return [m for m, c in ((candidato1, c1), (candidato2, c2))
            if c > 0 and 3 * A.count(m) > len(A)]

# == bloque: vigilada
def se_parte_en_trios(S):
    # un multiconjunto se parte en tríos de distintos si y solo si su tamaño es
    # múltiplo de 3 y ningún elemento aparece más de un tercio de las veces
    return len(S) % 3 == 0 and all(3 * k <= len(S) for k in Counter(S).values())

def primera_pasada_vigilada(A):
    candidato1, c1, candidato2, c2 = None, 0, None, 0
    for i, x in enumerate(A):
        if x == candidato1:
            c1 += 1
        elif x == candidato2:
            c2 += 1
        elif c1 == 0:
            candidato1, c1 = x, 1
        elif c2 == 0:
            candidato2, c2 = x, 1
        else:
            c1 -= 1
            c2 -= 1
        resto = Counter(A[:i + 1])
        resto[candidato1] -= c1       # quitar las c1 copias del primer candidato
        resto[candidato2] -= c2       # y las c2 del segundo
        assert min(resto.values()) >= 0 and se_parte_en_trios(list(resto.elements()))
        assert c2 == 0 or candidato1 != candidato2
    return (candidato1, c1), (candidato2, c2)

random.seed(8)
prefijos = 0
for _ in range(3000):
    A = [random.choice("ABCDE") for _ in range(random.randint(1, 15))]
    primera_pasada_vigilada(A)
    prefijos += len(A)
print(f"invariante comprobado en {prefijos:,} prefijos, sin fallos")

# == bloque: sin_verificar
def mayoria_tercio_sin_verificar(A):
    (candidato1, c1), (candidato2, c2) = primera_pasada_vigilada(A)
    return [m for m, c in ((candidato1, c1), (candidato2, c2)) if c > 0]

def oraculo(A):
    return [x for x, k in Counter(A).items() if 3 * k > len(A)]

A = list("AAB")
print(f"A A B: sin verificar {mayoria_tercio_sin_verificar(A)}, oráculo {oraculo(A)}")

# == bloque: generadores
def dos_plantados(n):         # el generador que no la atrapa
    p, q = random.sample("ABCDE", 2)
    k = n // 3 + 1
    A = [p] * k + [q] * k + [random.choice("ABCDE") for _ in range(n - 2 * k)]
    random.shuffle(A)
    return A

generadores = {
    "dos plantados": (dos_plantados, 4),            # necesita 2(⌊n/3⌋ + 1) <= n
    "binario": (lambda n: [random.choice("AB") for _ in range(n)], 1),
}

random.seed(5)
fallos = {}
print(f"{'generador':>14} {'sin verificar':>14} {'dos pasadas':>12}")
for nombre, (generar, minimo) in generadores.items():
    casos = [generar(random.randint(minimo, 15)) for _ in range(4000)]
    f_sin = sum(set(mayoria_tercio_sin_verificar(A)) != set(oraculo(A)) for A in casos)
    f_bm = sum(set(mayoria_tercio(A)) != set(oraculo(A)) for A in casos)
    fallos[nombre] = (100 * f_sin / len(casos), 100 * f_bm / len(casos))
    print(f"{nombre:>14} {fallos[nombre][0]:>13.1f}% {fallos[nombre][1]:>11.1f}%")

# == bloque: figura (oculto)
try:
    import figuras as F
except ImportError:
    print("sin tesserax no se regenera la figura")
else:
    figura = F.grafica_barras(list(fallos),
                              {"sin verificar": [s for s, _ in fallos.values()],
                               "dos pasadas": [b for _, b in fallos.values()]},
                              titulo_y="% de fallos", ident="ejercicio-08-generadores")
    svg = figura[figura.index("<svg"):figura.index("</svg>") + len("</svg>")]
    vb = svg.split('viewBox="')[1].split('"')[0].split()   # fondo blanco para GitHub
    fondo = f'<rect x="{vb[0]}" y="{vb[1]}" width="{vb[2]}" height="{vb[3]}" fill="white"/>'
    (AQUI.parent / "figuras" / "ejercicio-08-generadores.svg").write_text(
        svg.replace(">", ">" + fondo, 1), encoding="utf-8")
