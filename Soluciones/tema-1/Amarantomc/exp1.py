import itertools
from math import ceil, comb, log2
import random
def mediana(A, B):
    """n-ésimo menor de A ∪ B (mediana inferior). Solo usa comparaciones entre elementos."""
    n = len(A)
    assert len(B) == n and n >= 1
    lo, hi = 0, n                       # invariante: g(i) falso si i < lo; g(i) cierto si i >= hi
    while lo < hi:                      # potencial: hi - lo
        mid = (lo + hi) // 2
        if A[mid] >= B[n - 1 - mid]:    # g(mid)
            hi = mid
        else:
            lo = mid + 1
    i, j = lo, n - lo                   # i elementos de A y j de B forman los n menores
    if i == 0:
        return B[j - 1]
    if j == 0:
        return A[i - 1]
    return A[i - 1] if A[i - 1] > B[j - 1] else B[j - 1]

class Contado:
    __slots__ = ("v",)
    cuenta = 0
    def __init__(self, v): self.v = v
    def __ge__(self, o): Contado.cuenta += 1; return self.v >= o.v
    def __gt__(self, o): Contado.cuenta += 1; return self.v > o.v

def mediana_contada(A, B):
    Contado.cuenta = 0
    r = mediana([Contado(x) for x in A], [Contado(x) for x in B])
    return r.v, Contado.cuenta

def oraculo(A, B):
    return sorted(A + B)[len(A) - 1]

def intercalaciones(n):
    """Todas las formas de intercalar dos arreglos de largo n con valores distintos 0..2n-1."""
    for pos in itertools.combinations(range(2 * n), n):
        s = set(pos)
        yield list(pos), [r for r in range(2 * n) if r not in s]

def optimo_exacto(n):
    """Mínimo, sobre todos los algoritmos de comparaciones, del peor caso para hallar la mediana.
    Estado = conjunto de intercalaciones aún consistentes con las respuestas (bitmask)."""
    from functools import lru_cache
    inter = list(itertools.combinations(range(2 * n), n))     # posiciones (rangos) de A
    # mediana = elemento de rango n-1; su identidad: ('A',k) o ('B',k)
    ident = []
    for pos in inter:
        s = set(pos)
        if (n - 1) in s: ident.append(("A", pos.index(n - 1)))
        else: ident.append(("B", [r for r in range(2 * n) if r not in s].index(n - 1)))
    preguntas = []
    for i in range(n):
        for j in range(n):
            m = 0
            for k, pos in enumerate(inter):
                s = set(pos); b = [r for r in range(2 * n) if r not in s]
                if pos[i] < b[j]: m |= 1 << k
            preguntas.append(m)
    ident_masks = {}
    for k, idn in enumerate(ident): ident_masks[idn] = ident_masks.get(idn, 0) | (1 << k)
    masks = list(ident_masks.values())
    @lru_cache(maxsize=None)
    def f(mask):
        if any(mask & m == mask for m in masks): return 0       # una sola respuesta posible
        mejor = 99
        for q in preguntas:
            si, no = mask & q, mask & ~q
            if si and no: mejor = min(mejor, 1 + max(f(si), f(no)))
        return mejor
    return f((1 << len(inter)) - 1)



 





