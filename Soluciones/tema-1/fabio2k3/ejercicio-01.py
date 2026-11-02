import math

def factor(n, mejora = 1000):
    logn = math.log2(n)

    izq, der = 1.0, float(mejora)

    for _ in range(100):
        k = (izq + der) / 2

        if k * (1 + math.log2(k) / logn) < mejora:
            izq = k
        else:
            der = k

    return (izq + der) / 2


if __name__ == "__main__":
    print(f"{'n':>8} {'k':>9}  {'k*(1 + logk / log n)':>19} {'n_nuevo':>12}")

    for exp in range(3,10):
        n = 10 ** exp
        k = factor(n)
        check = k * (1 + math.log2(k) / math.log2(n))

        print(f"{'10^' + str(exp):>8} {k:9.1f} {check:19.6f} {k * n: 12.3e}")