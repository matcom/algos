"""Ejercicio 11 — ¿Es polinomial la mochila en $O(nW)$?

Código extraído de ejercicio-11.md, en el mismo orden en que aparece allí.
Ejecutar con:  python ejercicio-11.py
La salida esperada es la de la sección "Salida" de ejercicio-11.md.
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")   # para que la consola de Windows imprima δ, ≤, ⌈⌉...

# ----------------------------------------------------------------------
# Del md, sección: 1. El problema y el algoritmo
# ----------------------------------------------------------------------

def mochila_dp(pesos, valores, W, contador=None):
    """Programación dinámica O(nW), con una sola fila (se recorre c hacia atrás)."""
    M = [0] * (W + 1)
    for w, v in zip(pesos, valores):
        for c in range(W, w - 1, -1):
            M[c] = max(M[c], v + M[c - w])
        if contador is not None:
            contador[0] += W + 1            # celdas tocadas en esta fila
    return M[W]


# ----------------------------------------------------------------------
# Del md, sección: 5. Casos de prueba
# ----------------------------------------------------------------------

import itertools, random, math

def mochila_bruta(pesos, valores, W, contador=None):
    n, mejor = len(pesos), 0
    for S in itertools.product([0, 1], repeat=n):
        if contador is not None: contador[0] += 1
        if sum(p for p, s in zip(pesos, S) if s) <= W:
            mejor = max(mejor, sum(v for v, s in zip(valores, S) if s))
    return mejor

def bits(x):
    return max(1, x.bit_length())

def bits_instancia(pesos, valores, W):
    return sum(bits(p) for p in pesos) + sum(bits(v) for v in valores) + bits(W)

random.seed(11)
# 1) correctitud
for _ in range(400):
    n = random.randint(0, 10)
    pesos = [random.randint(1, 20) for _ in range(n)]
    valores = [random.randint(1, 30) for _ in range(n)]
    W = random.randint(0, 60)
    assert mochila_dp(pesos, valores, W) == mochila_bruta(pesos, valores, W)
print("DP == fuerza bruta en 400 instancias aleatorias")

# 2) escalado por 2^k
pesos, valores, W = [3, 4, 5, 9, 11, 13], [4, 5, 7, 12, 14, 17], 23
base = mochila_dp(pesos, valores, W)
print(f"\ninstancia: pesos={pesos} valores={valores} W={W} -> óptimo {base}")
print(f"{'k':>3} {'bits de la entrada':>19} {'celdas DP':>14} {'subconjuntos (bruta)':>21}")
for k in [0, 2, 4, 6, 8, 10, 12, 14, 16]:
    P = [p << k for p in pesos]; Wk = W << k
    c_dp, c_br = [0], [0]
    r1 = mochila_dp(P, valores, Wk, c_dp)
    r2 = mochila_bruta(P, valores, Wk, c_br)
    assert r1 == r2 == base                      # la respuesta no cambia
    print(f"{k:3} {bits_instancia(P, valores, Wk):19} {c_dp[0]:14,} {c_br[0]:21,}")

# 3) primalidad por división, medida en bits
def primo_division(N, contador):
    if N < 2: return False
    d = 2
    while d * d <= N:
        contador[0] += 1
        if N % d == 0: return False
        d += 1
    return True

def anterior_primo(x):
    while not primo_division(x, [0]):
        x -= 1
    return x

print(f"\n{'bits de N':>10} {'divisiones (N primo)':>21} {'2^(b/2)':>10}")
for b in [8, 12, 16, 20, 24, 28, 32, 36]:
    N = anterior_primo(2 ** b - 1)               # el mayor primo de b bits: N ≈ 2^b
    c = [0]
    assert primo_division(N, c)
    print(f"{N.bit_length():10} {c[0]:21,} {2 ** (b // 2):10,}")
