def buscar_en_matriz(A, x):
    n = len(A)
    i, j = 0, n - 1
    while i < n and j >= 0:
        if A[i][j] == x:
            return True
        elif A[i][j] > x:
            j -= 1
        else:
            i += 1
    return False

def oraculo(A, x):
    return any(x in fila for fila in A)

def main():
    A = [
        [1, 4, 7, 11],
        [2, 5, 8, 12],
        [3, 6, 9, 16],
        [10, 13, 14, 17],
    ]
    casos = [1, 4, 7, 11, 2, 5, 8, 12, 3, 6, 9, 16, 10, 13, 14, 17,
             0, 15, 18, 100]
    print(f"{'x':>5} {'algoritmo':>10} {'oráculo':>9}")
    for x in casos:
        print(f"{x:>5} {str(buscar_en_matriz(A, x)):>10} {str(oraculo(A, x)):>9}")

if __name__ == "__main__":
    main()
