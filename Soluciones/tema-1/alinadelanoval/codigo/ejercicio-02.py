"""Ejercicio 2 del Tema 1: invariante, potencial y cota de información de la búsqueda binaria.

Los bloques van en el orden de ejercicio-02.md, y cada uno imprime lo que el .md
muestra debajo de él. Ejecutarlo desde Soluciones/tema-1/alinadelanoval/:

    pip install tesserax        # para la figura
    python codigo/ejercicio-02.py
"""

# == bloque: imports (oculto)
import math
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[3] / "Lectures" / "2026"))   # donde vive figuras.py

# == bloque: algoritmo
def busqueda_binaria(A, x):
    lo, hi = 0, len(A)                              # ventana A[lo:hi], hi excluido
    while lo < hi:
        m = (lo + hi) // 2
        if A[m] == x:
            return m
        if x < A[m]:
            hi = m                                  # x < A[m]: fuera m y su derecha
        else:
            lo = m + 1                              # x > A[m]: fuera m y su izquierda
    return -1

# == bloque: vigilada
def busqueda_binaria_vigilada(A, x):
    # la misma búsqueda, comprobando el invariante y el potencial en cada vuelta
    lo, hi = 0, len(A)
    vueltas = 0
    while lo < hi:
        assert all(A[j] != x for j in range(len(A)) if not lo <= j < hi)   # invariante
        phi = hi - lo
        vueltas += 1
        m = (lo + hi) // 2
        if A[m] == x:
            return m, vueltas
        if x < A[m]:
            hi = m
        else:
            lo = m + 1
        assert 0 <= hi - lo <= phi // 2                                          # potencial
    return -1, vueltas

def busqueda_lineal(A, x):
    return next((j for j, a in enumerate(A) if a == x), -1)

busquedas = 0
for n in range(1, 400):
    A = list(range(2, 2 * n + 1, 2))                # 2, 4, ..., 2n
    peor = 0
    for x in range(1, 2 * n + 2):                   # pares: están; impares: un valor por hueco
        r, vueltas = busqueda_binaria_vigilada(A, x)
        assert r == busqueda_lineal(A, x) == busqueda_binaria(A, x)
        peor = max(peor, vueltas)
        busquedas += 1
    assert peor == math.ceil(math.log2(n + 1))
print(f"n de 1 a 399: {busquedas:,} búsquedas, 0 fallos")
print("invariante y Φ ≤ ⌊Φ/2⌋ comprobados en cada vuelta")
print("peor caso = ⌈log2(n + 1)⌉ comparaciones para todo n")

# == bloque: arbol (oculto)
class Consulta:
    """Un valor x que anota cada pregunta «x < a» que le hace la búsqueda."""
    def __init__(self, valor):
        self.valor, self.preguntas = valor, []
    def __eq__(self, otro):
        return self.valor == otro
    def __lt__(self, otro):
        r = self.valor < otro
        self.preguntas.append((otro, r))
        return r

def arbol_de_decision(A, hoja=lambda g: f"h{g}"):
    # corre busqueda_binaria con un valor de cada hueco y junta los caminos en un árbol
    raiz = {}
    huecos = [A[0] - 1] + [(a + b) / 2 for a, b in zip(A, A[1:])] + [A[-1] + 1]
    for g, v in enumerate(huecos):
        x = Consulta(v)
        assert busqueda_binaria(A, x) == -1
        nodo = raiz
        for a, r in x.preguntas:
            assert nodo.setdefault("pregunta", f"x < {a}") == f"x < {a}"
            nodo = nodo.setdefault(r, {})
        nodo["hoja"] = hoja(g)

    def a_tupla(nodo):
        if "hoja" in nodo:
            return ("hoja", nodo["hoja"])
        return (nodo["pregunta"], a_tupla(nodo[True]), a_tupla(nodo[False]))
    return a_tupla(raiz)

try:
    import figuras as F
except ImportError:
    print("sin tesserax no se regenera la figura")
else:
    arbol = arbol_de_decision([3, 8, 12, 17, 21, 26, 30], hoja=lambda g: "h" + F.sub(g))
    figura = F.arbol_comparaciones(arbol, ident="ejercicio-02-arbol")
    svg = figura[figura.index("<svg"):figura.index("</svg>") + len("</svg>")]
    vb = svg.split('viewBox="')[1].split('"')[0].split()   # fondo blanco para GitHub
    fondo = f'<rect x="{vb[0]}" y="{vb[1]}" width="{vb[2]}" height="{vb[3]}" fill="white"/>'
    (AQUI.parent / "figuras" / "ejercicio-02-arbol.svg").write_text(
        svg.replace(">", ">" + fondo, 1), encoding="utf-8")
