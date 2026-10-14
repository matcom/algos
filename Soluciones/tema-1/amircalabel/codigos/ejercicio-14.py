# Quickselect: k-ésimo menor en O(n) esperado.
# Uso: python ejercicio-14.py
# Salida: comparación contra un oráculo de fuerza bruta.

import random

def quickselect(A, k):
    """Devuelve el k-ésimo menor de A (k empieza en 1)."""
    if len(A) == 1:
        return A[0]
    pivote = A[len(A) // 2]
    menores = [x for x in A if x < pivote]
    iguales = [x for x in A if x == pivote]
    mayores = [x for x in A if x > pivote]
    if k <= len(menores):
        return quickselect(menores, k)
    elif k <= len(menores) + len(iguales):
        return pivote
    else:
        return quickselect(mayores, k - len(menores) - len(iguales))

def oraculo(A, k):
    return sorted(A)[k - 1]

def main():
    random.seed(2)
    print(f"{'n':>6} {'k':>4} {'quickselect':>12} {'oráculo':>10} {'ok':>4}")
    for n in [10, 100, 1000]:
        for k in [1, n // 2, n]:
            A = [random.randint(0, 1000) for _ in range(n)]
            res = quickselect(A, k)
            esp = oraculo(A, k)
            ok = "✓" if res == esp else "✗"
            print(f"{n:>6} {k:>4} {res:>12} {esp:>10} {ok:>4}")

if __name__ == "__main__":
    main()
