
import random

def mediana_dos_arreglos(A, B):
    """Devuelve el n-ésimo menor de los 2n elementos de A y B."""
    n = len(A)
    lo, hi = 0, n
    while lo <= hi:
        i = (lo + hi) // 2
        j = n - i
        A_izq = A[i-1] if i > 0 else float('-inf')
        A_der = A[i] if i < n else float('inf')
        B_izq = B[j-1] if j > 0 else float('-inf')
        B_der = B[j] if j < n else float('inf')
        if A_izq <= B_der and B_izq <= A_der:
            return max(A_izq, B_izq)
        elif A_izq > B_der:
            hi = i - 1
        else:
            lo = i + 1
    raise ValueError("No se encontró la mediana")

def oraculo(A, B):
    """Fuerza bruta: junta, ordena y toma el n-ésimo menor."""
    C = sorted(A + B)
    return C[len(A) - 1]

def main():
    random.seed(1)
    print(f"{'n':>4} {'algoritmo':>10} {'oráculo':>10} {'ok':>4}")
    for n in [1, 2, 3, 5, 10, 100]:
        for _ in range(5):
            A = sorted(random.sample(range(1000), n))
            B = sorted(random.sample(range(1000), n))
            res = mediana_dos_arreglos(A, B)
            esp = oraculo(A, B)
            ok = "✓" if res == esp else "✗"
            print(f"{n:>4} {res:>10} {esp:>10} {ok:>4}")

if __name__ == "__main__":
    main()
