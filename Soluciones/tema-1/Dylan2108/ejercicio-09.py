"""Ejercicio 9: la mezcla "optimizada" que deja de comparar cuando a A le queda un elemento.

Corre: python ejercicio-09.py
"""
import itertools, random

def mezcla(A, B, cmp):
    """Mezcla clásica (sección 6 de la conferencia 5). cmp(a, b) -> True si a < b; cuenta por fuera."""
    i = j = 0
    salida = []
    while i < len(A) and j < len(B):
        if cmp(A[i], B[j]):
            salida.append(A[i]); i += 1
        else:
            salida.append(B[j]); j += 1
    return salida + A[i:] + B[j:]


def mezcla_optimizada(A, B, cmp):
    """Igual, pero cuando a A le queda un solo elemento deja de comparar:
    pone lo que queda de B y al final ese último elemento de A."""
    i = j = 0
    salida = []
    while len(A) - i >= 2 and j < len(B):
        if cmp(A[i], B[j]):
            salida.append(A[i]); i += 1
        else:
            salida.append(B[j]); j += 1
    if j == len(B):                     # B se acabó antes: termina como la mezcla normal
        return salida + A[i:]
    return salida + B[j:] + A[i:]       # A tiene exactamente 1: "lo pone al final"


def contar(alg, A, B):
    pares = []
    def cmp(a, b):
        pares.append((a, b))
        return a < b
    return alg(A, B, cmp), pares


def todas_las_entradas(n):
    """Las C(2n, n) formas de repartir 0..2n-1 entre A y B (todas las intercalaciones)."""
    for S in itertools.combinations(range(2 * n), n):
        A = list(S)
        B = [v for v in range(2 * n) if v not in S]
        yield A, B


if __name__ == "__main__":
    # 1. Peor caso de comparaciones, exhaustivo
    print(f"{'n':>3} {'entradas':>9} {'peor mezcla':>12} {'peor optimizada':>16} {'cota 2n-1':>10} {'fallos optimizada':>18}")
    for n in range(1, 9):
        peor_m = peor_o = fallos = total = 0
        for A, B in todas_las_entradas(n):
            total += 1
            s, p = contar(mezcla, A, B)
            assert s == sorted(A + B)
            peor_m = max(peor_m, len(p))
            s, p = contar(mezcla_optimizada, A, B)
            peor_o = max(peor_o, len(p))
            fallos += s != sorted(A + B)
            # caracterización: falla exactamente cuando el máximo de todo está en B
            assert (s != sorted(A + B)) == (max(B) > max(A))
        assert peor_m == 2 * n - 1
        assert peor_o == 2 * n - 2
        print(f"{n:>3} {total:>9} {peor_m:>12} {peor_o:>16} {2 * n - 1:>10} {100 * fallos / total:>17.1f}%")

    # 2. El adversario de la sección 6 de la conferencia 5: la entrada intercalada a1 < b1 < a2 < b2 < ... < an < bn
    n = 5
    A = [2 * k for k in range(n)]          # a_k = 2(k-1)
    B = [2 * k + 1 for k in range(n)]      # b_k = 2(k-1) + 1
    nombre = lambda v: f"{'ab'[v % 2]}{v // 2 + 1}"
    s, pares = contar(mezcla_optimizada, A, B)
    comparados = {frozenset(p) for p in pares}
    vecinos = [frozenset((v, v + 1)) for v in range(2 * n - 1)]
    sin_comparar = [tuple(sorted(p)) for p in vecinos if p not in comparados]
    print(f"\nn = {n}, entrada intercalada del adversario: A = {A}, B = {B}")
    print("  comparaciones:", " ".join(f"{nombre(a)}:{nombre(b)}" for a, b in pares), f"({len(pares)})")
    print("  pares de vecinos sin comparar:", [f"{nombre(a)}-{nombre(b)}" for a, b in sin_comparar])
    print("  salida:   ", " ".join(nombre(v) for v in s))
    print("  correcta: ", " ".join(nombre(v) for v in sorted(A + B)))
    assert len(pares) == 2 * n - 3
    assert sin_comparar == [(2 * n - 3, 2 * n - 2), (2 * n - 2, 2 * n - 1)]   # b_{n-1}-a_n y a_n-b_n
    assert s != sorted(A + B)                             # ya falla en la propia entrada del adversario

    # 3. El intercambio del par sin comparar: mismas respuestas, salida correcta distinta
    v, w = sin_comparar[-1]                # el par a_n - b_n
    swap = lambda L: [w if x == v else v if x == w else x for x in L]
    A2, B2 = swap(A), swap(B)
    assert A2 == sorted(A2) and B2 == sorted(B2)
    s2, pares2 = contar(mezcla_optimizada, A2, B2)
    assert [(a < b) for a, b in pares] == [(a < b) for a, b in pares2]   # mismas respuestas
    pos = lambda S, AA: ["A" if x in AA else "B" for x in S]             # la salida como etiquetas
    assert pos(s, A) == pos(s2, A2)                                      # misma salida
    print(f"\n  intercambiando a{n} y b{n}: A' = {A2}, B' = {B2}")
    print("  las", len(pares2), "respuestas son las mismas y la salida (en posiciones) también;")
    print("  con A', B' es correcta:", s2 == sorted(A2 + B2), " con A, B es correcta:", s == sorted(A + B))

    # 4. Cuánto lo ven las pruebas
    rng = random.Random(2026)
    print(f"\n{'generador':>40} {'fallos':>8}")
    gens = {
        "aleatorio (reparto al azar de 2n valores)": lambda n: (lambda S: (sorted(S[:n]), sorted(S[n:])))(rng.sample(range(10**6), 2 * n)),
        "A toda menor que B": lambda n: (list(range(n)), list(range(n, 2 * n))),
        "B toda menor que A": lambda n: (list(range(n, 2 * n)), list(range(n))),
        "intercalada, A empieza": lambda n: (list(range(0, 2 * n, 2)), list(range(1, 2 * n, 2))),
        "intercalada, B empieza": lambda n: (list(range(1, 2 * n, 2)), list(range(0, 2 * n, 2))),
    }
    for nombre_g, g in gens.items():
        N = 2000
        f = 0
        for _ in range(N):
            A, B = g(rng.randint(2, 50))
            f += mezcla_optimizada(A, B, lambda a, b: a < b) != sorted(A + B)
        print(f"{nombre_g:>40} {100 * f / N:>7.1f}%")
