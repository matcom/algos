import random, math

INF = float('inf')

def n_esimo_menor(A, B, contador=None):
    """A y B ordenados, mismo largo n. Devuelve el n-esimo menor (1-indexado) de A+B,
    es decir, indice n-1 (0-indexado) del merge completo."""
    n = len(A)
    lo, hi = 0, n
    while True:
        i = (lo + hi) // 2         # tomamos i elementos de A
        j = n - i                  # y n-i de B
        Aleft  = A[i-1] if i > 0 else -INF
        Aright = A[i]   if i < n else INF
        Bleft  = B[j-1] if j > 0 else -INF
        Bright = B[j]   if j < n else INF
        if contador is not None:
            contador[0] += 1
        if Aleft <= Bright and Bleft <= Aright:
            return max(Aleft, Bleft)
        elif Aleft > Bright:
            hi = i - 1
        else:
            lo = i + 1

def fuerza_bruta(A, B):
    return sorted(A + B)[len(A) - 1]   # n-esimo menor, 1-indexado = indice n-1

random.seed(0)
fallos = 0
pruebas = 0
max_iters = 0
for n in [1, 2, 3, 5, 10, 50, 200, 1000, 5000]:
    for _ in range(30):
        A = sorted(random.sample(range(-10**6, 10**6), n))
        B = sorted(random.sample(range(-10**6, 10**6), n))
        esperado = fuerza_bruta(A, B)
        c = [0]
        obtenido = n_esimo_menor(A, B, c)
        max_iters = max(max_iters, c[0])
        pruebas += 1
        if obtenido != esperado:
            fallos += 1

print(f"pruebas: {pruebas}, fallos (deberia ser 0): {fallos}")

print()
print(f"{'n':>6} {'iteraciones (peor de 30 pruebas)':>34} {'techo(log2(n+1))':>18}")
for n in [1, 2, 3, 5, 10, 50, 200, 1000, 5000, 100000, 1000000]:
    peor = 0
    for _ in range(30):
        A = sorted(random.sample(range(-10**9, 10**9), n))
        B = sorted(random.sample(range(-10**9, 10**9), n))
        c = [0]
        n_esimo_menor(A, B, c)
        peor = max(peor, c[0])
    print(f"{n:>6} {peor:>34} {math.ceil(math.log2(n+1)):>18}")

# Verificacion de la "crossing lemma": con la particion hallada, todo elemento del lado
# izquierdo es <= todo elemento del lado derecho.
print()
fallos_cruce = 0
for _ in range(2000):
    n = random.randint(1, 60)
    A = sorted(random.sample(range(-1000, 1000), n))
    B = sorted(random.sample(range(-1000, 1000), n))
    lo, hi = 0, n
    while True:
        i = (lo + hi) // 2
        j = n - i
        Aleft  = A[i-1] if i > 0 else -INF
        Aright = A[i]   if i < n else INF
        Bleft  = B[j-1] if j > 0 else -INF
        Bright = B[j]   if j < n else INF
        if Aleft <= Bright and Bleft <= Aright:
            izquierda = A[:i] + B[:j]
            derecha = A[i:] + B[j:]
            if izquierda and derecha and max(izquierda) > min(derecha):
                fallos_cruce += 1
            break
        elif Aleft > Bright:
            hi = i - 1
        else:
            lo = i + 1
print(f"fallos del lema de cruce (max(izq) <= min(der), deberia ser 0): {fallos_cruce}")
