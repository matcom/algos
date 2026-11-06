"""Ejercicio 10: la mochila por programación dinámica cuesta Θ(n·W).
Fijamos n y vamos agregando bits a W: si el algoritmo fuera polinomial en el
tamaño de la entrada, un bit más no debería duplicar el trabajo."""
import random
import time

def mochila(pesos, valores, W):
    """Tabla de (n+1) filas por (W+1) columnas, guardando solo la fila anterior.
    Devuelve el mejor valor y cuántas casillas se llenaron."""
    anterior = [0] * (W + 1)
    casillas = 0
    for p, v in zip(pesos, valores):
        actual = anterior[:]
        for w in range(W + 1):
            casillas += 1
            if p <= w and anterior[w - p] + v > actual[w]:
                actual[w] = anterior[w - p] + v
        anterior = actual
    return anterior[W], casillas

def fuerza_bruta(pesos, valores, W):
    """Oráculo: prueba los 2^n subconjuntos."""
    n, mejor = len(pesos), 0
    for mask in range(1 << n):
        p = sum(pesos[i] for i in range(n) if mask >> i & 1)
        v = sum(valores[i] for i in range(n) if mask >> i & 1)
        if p <= W:
            mejor = max(mejor, v)
    return mejor

# 1. Correctitud contra el oráculo en instancias pequeñas
random.seed(10)
for _ in range(500):
    n = random.randint(1, 10)
    pesos = [random.randint(1, 20) for _ in range(n)]
    valores = [random.randint(1, 20) for _ in range(n)]
    W = random.randint(0, 60)
    assert mochila(pesos, valores, W)[0] == fuerza_bruta(pesos, valores, W)
print("500 instancias contra fuerza bruta: sin fallos\n")

# 2. n fijo, W con cada vez más bits
n = 20
pesos = [random.randint(1, 1000) for _ in range(n)]
valores = [random.randint(1, 1000) for _ in range(n)]
print(f"{'bits de W':>10} {'W':>10} {'casillas':>12} {'tiempo':>9}")
for b in range(10, 19):
    W = 2 ** b - 1
    inicio = time.perf_counter()
    _, casillas = mochila(pesos, valores, W)
    seg = time.perf_counter() - inicio
    print(f"{b:>10} {W:>10,} {casillas:>12,} {seg:>8.3f}s")
