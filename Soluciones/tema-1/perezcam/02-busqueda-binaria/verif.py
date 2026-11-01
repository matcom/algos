import math

def busqueda_binaria(A, x, contador=None):
    lo, hi = 0, len(A)
    potenciales = [hi - lo]
    while lo < hi:
        m = (lo + hi) // 2
        if contador is not None:
            contador[0] += 1
        if x == A[m]:
            return ("esta", m), potenciales
        elif x < A[m]:
            hi = m
        else:
            lo = m + 1
        potenciales.append(hi - lo)
    return ("hueco", lo), potenciales

# 1) El potencial hi-lo baja estrictamente en cada vuelta, nunca sube, y es siempre >= 0
fallos_potencial = 0
for n in range(1, 400):
    A = list(range(0, 2*n, 2))  # pares 0,2,4,...
    for x in range(-1, 2*n + 2):
        _, pot = busqueda_binaria(A, x)
        for i in range(1, len(pot)):
            if not (pot[i] < pot[i-1]) or pot[i] < 0:
                fallos_potencial += 1
print("fallos del potencial (deberia ser 0):", fallos_potencial)

# 2) El peor caso de comparaciones es exactamente ceil(log2(n+1))
print(f"{'n':>6} {'max comparaciones':>18} {'techo(log2(n+1))':>18}")
for n in [1, 2, 3, 4, 7, 8, 15, 16, 100, 1000, 1_000_000]:
    A = list(range(0, 2*n, 2))
    peor = 0
    # probamos los n+1 huecos: x impar en cada hueco interior, y x fuera de rango en los extremos
    candidatos = [-1] + [2*i + 1 for i in range(n)] + [2*n]
    for x in candidatos:
        contador = [0]
        busqueda_binaria(A, x, contador)
        peor = max(peor, contador[0])
    print(f"{n:>6} {peor:>18} {math.ceil(math.log2(n+1)):>18}")
