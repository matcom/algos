"""Ejercicio 9: la mezcla "optimizada" que deja de comparar cuando a A le queda un
elemento y lo pone al final. Peor caso 2n - 2, una menos que la cota 2n - 1 de la
conferencia 5, así que tiene que fallar."""
from itertools import combinations


def mezcla(A, B):
    """La mezcla normal. Devuelve (resultado, comparaciones, pares comparados)."""
    R, i, j, pares = [], 0, 0, []
    while i < len(A) and j < len(B):
        pares.append((A[i], B[j]))
        if A[i] <= B[j]:
            R.append(A[i]); i += 1
        else:
            R.append(B[j]); j += 1
    return R + A[i:] + B[j:], len(pares), pares


def mezcla_optimizada(A, B):
    """Para cuando a A le queda un solo elemento: pega lo que queda de B y pone ese
    elemento de A al final, sin compararlo."""
    R, i, j, pares = [], 0, 0, []
    while len(A) - i > 1 and j < len(B):
        pares.append((A[i], B[j]))
        if A[i] <= B[j]:
            R.append(A[i]); i += 1
        else:
            R.append(B[j]); j += 1
    return R + B[j:] + A[i:], len(pares), pares


# 1. Peor caso y fallos sobre todas las entradas: A y B son una partición de 0..2n-1
print(f"{'n':>3} {'peor normal':>12} {'peor optimizada':>16} {'cota 2n-1':>10} {'falla en':>14}")
for n in range(1, 8):
    peor_n = peor_o = fallos = total = 0
    for S in combinations(range(2 * n), n):
        A = list(S)
        B = [x for x in range(2 * n) if x not in S]
        Rn, cn, _ = mezcla(A, B)
        Ro, co, _ = mezcla_optimizada(A, B)
        assert Rn == sorted(A + B)
        peor_n, peor_o = max(peor_n, cn), max(peor_o, co)
        total += 1
        fallos += Ro != sorted(A + B)
        # falla exactamente cuando el máximo está en B
        assert (Ro != sorted(A + B)) == (2 * n - 1 in B)
    print(f"{n:>3} {peor_n:>12} {peor_o:>16} {2 * n - 1:>10} {fallos:>6}/{total:<7}")

# 2. La entrada del adversario: la intercalada, y el par de vecinos que no se compara
A, B = [1, 3, 5, 7], [2, 4, 6, 8]
R, c, pares = mezcla_optimizada(A, B)
orden = sorted(A + B)
vecinos = set(zip(orden, orden[1:]))
comparados = {tuple(sorted(p)) for p in pares}
print(f"\nintercalada A={A} B={B}")
print(f"  resultado {R} con {c} comparaciones: {'bien' if R == orden else 'MAL'}")
print(f"  pares de vecinos que nunca comparó: {sorted(vecinos - comparados)}")
A2, B2 = [1, 3, 5, 8], [2, 4, 6, 7]                     # intercambio el 7 y el 8
R2, c2, pares2 = mezcla_optimizada(A2, B2)
print(f"intercambiando 7 y 8: A={A2} B={B2}")
print(f"  mismas comparaciones: {pares2 == pares}; resultado {R2}: "
      f"{'bien' if R2 == sorted(A2 + B2) else 'MAL'}")
