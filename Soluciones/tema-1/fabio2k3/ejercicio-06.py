import random

def search(M, x, check = False):
    n = len(M)
    i = 0
    j = n-1

    comparaciones = 0
    consultadas = []

    phi_ant = None
    while i < n and j >= 0:
        if check:
            assert all(M[a][b] != x for a in range(i) for b in range(n))
            assert all(M[a][b] != x for a in range(n) for b in range(j+1, n))

            phi = (n-i) + (j+1)
            assert phi_ant is None or phi == phi_ant - 1
            phi_ant = phi

        comparaciones += 1
        consultadas.append((i,j))

        if M[i][j] == x:
            return(i,j), comparaciones, consultadas
        if M[i][j] > x:
            j -= 1
        else:
            i += 1

    return None, comparaciones, consultadas

def matriz_ordenada(n, rng):
    M = [[0] * n for _ in range(n)]
    for i in range (n):
        for j  in range(n):
            base = max(M[i-1][j] if i else 0, M[i][j-1] if j else 0)
            M[i][j] = base + rng.randint(0,3)

    return M

def adversario(n):
    M0 = [[10 * (i+j) for j in range (n)] for i in range(n)]
    x = 10 * (n-1) + 5
    return M0, x

if __name__ == "__main__":
    rng = random.Random(0)
    print(f"{'n':>3} {'instancias':>11} {'presentes':>10} {'ausentes':>9} "
          f"{'desacuerdos':>12} {'max comp.':>10} {'2n-1':>6}")
    for n in range(1, 9):
        total = presentes = desacuerdos = peor = 0
        for _ in range(3000):
            M = matriz_ordenada(n, rng)
            todas = [v for fila in M for v in fila]
            x = rng.choice(todas) if rng.random() < 0.5 else rng.randint(-1, max(todas) + 1)
            pos, c, _ = search(M, x, check=True)
            esta = x in todas
            total += 1
            presentes += esta
            desacuerdos += (pos is not None) != esta
            assert pos is None or M[pos[0]][pos[1]] == x
            peor = max(peor, c)
        assert peor <= 2 * n - 1
        print(f"{n:>3} {total:>11} {presentes:>10} {total - presentes:>9} "
              f"{desacuerdos:>12} {peor:>10} {2 * n - 1:>6}")

    print()
    print(f"{'n':>3} {'comp. en M0':>12} {'2n-1':>6} {'antidiag. consultadas':>22} "
          f"{'k donde M1_k halla x':>21}")
    for n in [2, 4, 8, 16, 32]:
        M0, x = adversario(n)
        pos, c, cons = search(M0, x)
        assert pos is None
        antidiag = {(k, n - 1 - k) for k in range(n)}
        consultadas = len(antidiag & set(cons))
        halla = 0
        for k in range(n):
            M1 = [fila[:] for fila in M0]
            M1[k][n - 1 - k] = x          
            pos1, _, _ = search(M1, x)
            halla += pos1 == (k, n - 1 - k)
        print(f"{n:>3} {c:>12} {2 * n - 1:>6} {consultadas:>22} {halla:>21}")