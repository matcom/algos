import random

def mochila(w, v, W):
    Q = [0] * (W + 1)

    celdas = 0

    for wi, vi in zip(w,v):
        for c in range(W, wi-1, -1):
            Q[c] = max(Q[c], Q[c-wi] + vi)
            celdas += 1

    return Q[W], celdas

def fuerza_bruta(w, v, W):
    n = len(w)
    mejor = 0
    for mascara in range(1 << n):
        peso = 0
        valor = 0

        for i in range(n):
            if (mascara >> i) & 1:
                peso += w[i]
                valor += v[i]
        if peso <= W:
            mejor = max(mejor, valor)

    return mejor

def prueba_correctitud():
    random.seed(0)
    for _ in range(2000):
        n = random.randint(0,10)
        W = random.randint(1, 30)
        w = [random.randint(1, 15) for _ in range(n)]
        v = [random.randint(1, 20) for _ in range(n)]
        assert mochila(w, v, W)[0] == fuerza_bruta(w, v, W), (w, v, W)

    print("Feten => Correctitud")

def tabla_bits_contra_pasos():
    random.seed(1)
    n = 5
    print(f"{'W':>8} {'bits b':>7} {'n*W':>10} {'celdas':>10} {'celdas/(n*W)':>13}")
    for e in range(2, 7):
        W = 10 ** e
        w = [random.randint(1,3) for _ in range(n)]
        v = [random.randint(1,100) for _ in range(n)]
        _, celdas = mochila(w, v, W)
        
        print(f"{'10^' + str(e):>8} {W.bit_length():>7} {n * W :>10} {celdas:>10} {celdas / ( n * W):>13.4f}")

if __name__ == "__main__":
    prueba_correctitud()
    tabla_bits_contra_pasos()