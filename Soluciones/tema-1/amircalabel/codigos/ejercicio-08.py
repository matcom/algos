
import random
from collections import Counter

def mayoria_n_tercios(A):
    cand1, cand2 = None, None
    c1, c2 = 0, 0
    for x in A:
        if c1 > 0 and x == cand1:
            c1 += 1
        elif c2 > 0 and x == cand2:
            c2 += 1
        elif c1 == 0:
            cand1, c1 = x, 1
        elif c2 == 0:
            cand2, c2 = x, 1
        else:
            c1 -= 1
            c2 -= 1
    resultado = []
    for cand in (cand1, cand2):
        if cand is not None and A.count(cand) > len(A) // 3:
            resultado.append(cand)
    return resultado

def mayoria_n_tercios_atajo(A):
    cand1, cand2 = None, None
    c1, c2 = 0, 0
    for x in A:
        if c1 > 0 and x == cand1:
            c1 += 1
        elif c2 > 0 and x == cand2:
            c2 += 1
        elif c1 == 0:
            cand1, c1 = x, 1
        elif c2 == 0:
            cand2, c2 = x, 1
        else:
            c1 -= 1
            c2 -= 1
    return [c for c, cnt in [(cand1, c1), (cand2, c2)] if cnt > 0]

def oraculo(A):
    return [x for x, k in Counter(A).items() if k > len(A) // 3]

def plantada(n):
    m = random.choice("ABCDE")
    A = [m] * (n // 3 + 1) + [random.choice("ABCDE") for _ in range(n - n // 3 - 1)]
    random.shuffle(A)
    return A

def main():
    generadores = {
        "mayoría plantada": plantada,
        "binario": lambda n: [random.choice("AB") for _ in range(n)],
        "3 símbolos": lambda n: [random.choice("ABC") for _ in range(n)],
        "5 símbolos": lambda n: [random.choice("ABCDE") for _ in range(n)],
    }
    random.seed(5)
    print(f"{'generador':>20} {'atajo':>8} {'dos pasadas':>12}")
    for nombre, gen in generadores.items():
        casos = [gen(random.randint(1, 15)) for _ in range(4000)]
        f_atajo = sum(set(mayoria_n_tercios_atajo(A)) != set(oraculo(A)) for A in casos) / len(casos)
        f_bm = sum(set(mayoria_n_tercios(A)) != set(oraculo(A)) for A in casos) / len(casos)
        print(f"{nombre:>20} {100*f_atajo:>7.1f}% {100*f_bm:>11.1f}%")

if __name__ == "__main__":
    main()
