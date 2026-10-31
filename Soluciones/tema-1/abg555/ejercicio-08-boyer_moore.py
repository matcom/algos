from collections import Counter


def first_pass(A, trace=None):
    # Primera pasada: cancelar de a tres. Devuelve los dos candidatos y sus contadores.
    # Si se pasa una lista en trace, guarda (cand1, count1, cand2, count2) en cada paso.
    cand1, count1 = None, 0
    cand2, count2 = None, 0
    for x in A:
        if x == cand1:
            count1 += 1
        elif x == cand2:
            count2 += 1
        elif count1 == 0:
            cand1, count1 = x, 1
        elif count2 == 0:
            cand2, count2 = x, 1
        else:                                  # x se cancela con una copia de cada candidato
            count1 -= 1
            count2 -= 1
        if trace is not None:
            trace.append((cand1, count1, cand2, count2))
    return cand1, count1, cand2, count2


def more_than_third(A):
    # Devuelve los elementos que aparecen mas de n/3 veces (0, 1 o 2 elementos).
    cand1, _, cand2, _ = first_pass(A)
    # segunda pasada: verificar
    return [c for c in (cand1, cand2) if c is not None and 3 * A.count(c) > len(A)]


def more_than_third_shortcut(A):
    # Atajo: devuelve los candidatos con contador positivo, sin verificar.
    cand1, count1, cand2, count2 = first_pass(A)
    return [c for c, k in ((cand1, count1), (cand2, count2)) if k > 0]


def oracle(A):
    # Cuenta todo: obviamente correcto, pero usa O(n) memoria.
    return [x for x, k in Counter(A).items() if 3 * k > len(A)]
