import math

# Ejercicio 1, Tema 1: maquina 1000 veces mas rapida.
# Para n log n hay que resolver:  k * (1 + log2(k)/log2(n)) = 1000
# Despejando k:                   k = 1000 / (1 + log2(k)/log2(n))
# Idea: empezar con k = 1000, meterlo en el lado derecho para sacar un k
# mejor, y repetir hasta que k casi no cambie.


def estimacion(n):
    # un solo paso, se puede hacer a mano (usa log2(k) < log2(1000))
    L = math.log2(n)
    return 1000 * L / (L + math.log2(1000))


def factor(n):
    L = math.log2(n)
    k = 1000.0
    for _ in range(50):
        k = 1000 / (1 + math.log2(k) / L)
    return k


if __name__ == "__main__":
    # ejemplo paso a paso con n = 10^6
    n = 10 ** 6
    L = math.log2(n)
    k = 1000.0
    print("Pasos para n = 10^6:")
    for i in range(1, 5):
        k = 1000 / (1 + math.log2(k) / L)
        print(f"  paso {i}: k = {k:.2f}")
    print()

    print(f"{'n':>6} {'estimacion':>11} {'k':>9} {'n nuevo':>10}")
    for exp in range(3, 10):
        n = 10 ** exp
        k = factor(n)
        print(f"{'10^' + str(exp):>6} {estimacion(n):11.1f} {k:9.1f} {k * n:10.3e}")
