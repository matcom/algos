import random
import math

def par_mas_cercano_1d(P):
    P_ord = sorted(P)
    mejor = float('inf')
    par = None
    for i in range(len(P_ord) - 1):
        d = P_ord[i+1] - P_ord[i]
        if d < mejor:
            mejor = d
            par = (P_ord[i], P_ord[i+1])
    return mejor, par

def par_mas_cercano_1d_aleatorio(P, semilla=0):
    pts = list(P)
    random.Random(semilla).shuffle(pts)
    d = abs(pts[0] - pts[1])
    par = (pts[0], pts[1])
    lado = d / 2
    celda = lambda x: int(x // lado)
    rejilla = {celda(pts[0]): pts[0], celda(pts[1]): pts[1]}
    reconstrucciones = 0
    for i in range(2, len(pts)):
        x = pts[i]
        antes = d
        cx = celda(x)
        for dx in (-1, 0, 1):
            y = rejilla.get(cx + dx)
            if y is not None and abs(x - y) < d:
                d = abs(x - y)
                par = (x, y)
        if d < antes:
            lado = d / 2
            rejilla = {}
            for j in range(i + 1):
                rejilla[celda(pts[j])] = pts[j]
            reconstrucciones += 1
        else:
            rejilla[cx] = x
    return d, par, reconstrucciones

def main():
    random.seed(3)
    print(f"{'n':>8} {'determinista':>14} {'aleatorio':>14} {'2 ln n':>8}")
    for n in [1000, 10000, 100000]:
        P = [random.random() for _ in range(n)]
        d1, _ = par_mas_cercano_1d(P)
        rs = [par_mas_cercano_1d_aleatorio(P, semilla=s)[2] for s in range(3)]
        d2, _, _ = par_mas_cercano_1d_aleatorio(P)
        print(f"{n:>8} {d1:>14.2e} {d2:>14.2e} {sum(rs)/len(rs):>8.1f}")

if __name__ == "__main__":
    main()
