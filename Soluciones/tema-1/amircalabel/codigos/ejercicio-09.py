def mezclar(A, B):
    """Mezcla óptima. Devuelve (resultado, comparaciones)."""
    R = []
    i, j = 0, 0
    comparaciones = 0
    while i < len(A) and j < len(B):
        comparaciones += 1
        if A[i] <= B[j]:
            R.append(A[i]); i += 1
        else:
            R.append(B[j]); j += 1
    R.extend(A[i:])
    R.extend(B[j:])
    return R, comparaciones

def mezclar_optimizada(A, B):
    """Versión que deja de comparar cuando a A le queda un solo elemento."""
    R = []
    i, j = 0, 0
    comparaciones = 0
    while i < len(A) and j < len(B):
        if len(A) - i == 1:
            break
        comparaciones += 1
        if A[i] <= B[j]:
            R.append(A[i]); i += 1
        else:
            R.append(B[j]); j += 1
    R.extend(A[i:])
    R.extend(B[j:])
    return R, comparaciones

def main():
    # Entrada intercalada perfecta
    n = 3
    A = [1, 3, 5]
    B = [2, 4, 6]
    R_opt, c_opt = mezclar(A, B)
    R_atajo, c_atajo = mezclar_optimizada(A, B)
    print(f"A = {A}")
    print(f"B = {B}")
    print(f"Mezcla óptima:     {R_opt}  ({c_opt} comparaciones)")
    print(f"Mezcla optimizada: {R_atajo}  ({c_atajo} comparaciones)")
    print(f"¿Ordenada la optimizada? {R_atajo == sorted(R_atajo)}")
    print()

    # Tabla de comparaciones para varios n
    print(f"{'n':>4} {'óptima':>8} {'optimizada':>12} {'2n-1':>6}")
    for n in [2, 3, 5, 10, 100]:
        A = [2*i for i in range(n)]
        B = [2*i + 1 for i in range(n)]
        _, c1 = mezclar(A, B)
        _, c2 = mezclar_optimizada(A, B)
        print(f"{n:>4} {c1:>8} {c2:>12} {2*n-1:>6}")

if __name__ == "__main__":
    main()
