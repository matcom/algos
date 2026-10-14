
def busqueda_binaria_verificada(A, x):
    lo, hi = 0, len(A)
    comparaciones = 0
    while lo < hi:
        # Invariante: si x está, está en A[lo:hi]
        assert not (x in A and not (lo <= A.index(x) < hi)), \
            f"Invariante violado: x={x}, A[lo:hi]={A[lo:hi]}"
        phi_antes = hi - lo
        m = (lo + hi) // 2
        comparaciones += 1
        if x == A[m]:
            return ("está", m), comparaciones
        elif x < A[m]:
            hi = m
        else:
            lo = m + 1
        phi_despues = hi - lo
        if lo < hi:
            assert phi_despues < phi_antes, \
                f"Potencial no baja: {phi_antes} -> {phi_despues}"
    return ("hueco", lo), comparaciones

def main():
    casos = [
        ([1, 3, 5, 7, 9, 11, 13], 7),
        ([1, 3, 5, 7, 9, 11, 13], 4),
        ([1, 3, 5, 7, 9, 11, 13], 0),
        ([1, 3, 5, 7, 9, 11, 13], 14),
        ([1], 1),
        ([1], 0),
        ([], 5),
    ]
    print(f"{'A':>30} {'x':>4} {'resultado':>12} {'comparaciones':>14}")
    for A, x in casos:
        (res, pos), comp = busqueda_binaria_verificada(A, x)
        print(f"{str(A):>30} {x:>4} {res+' '+str(pos):>12} {comp:>14}")

if __name__ == "__main__":
    main()
