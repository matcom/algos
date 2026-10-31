"""Ejercicio 9 ★★ — Una mezcla "optimizada" (C5)

Código de validación de ejercicio-09.md.
Ejecutar con: python ejercicio-09.py
"""


# -------------------- Parte 1 --------------------

def mezcla_optimizada(I, D, cuenta, registro=None):
    R, i, j = [], 0, 0
    while len(I) - i > 1 and j < len(D):        # se detiene si a I le queda uno solo
        cuenta[0] += 1
        if registro is not None:
            registro.append((I[i], D[j]))
        if I[i] <= D[j]:
            R.append(I[i])
            i += 1
        else:
            R.append(D[j])
            j += 1
    return R + D[j:] + I[i:]                    # lo que queda de D y, "al final", el último de I

# -------------------- Parte 2 --------------------

import random
from itertools import combinations

def correcta(I, D):
    return sorted(I + D)

def todas_las_entradas(n):
    """Todas las formas de intercalar dos listas de n (valores 0..2n-1)."""
    for idx in combinations(range(2 * n), n):
        I = list(idx)
        D = [v for v in range(2 * n) if v not in idx]
        yield I, D

# -------------------- Parte 3 --------------------

print(f"{'n':>3} {'peor caso':>10} {'2n-2':>5} {'cota 2n-1':>10} {'entradas':>9} {'fallan':>7}")
for n in range(1, 10):
    peor, fallan, total = 0, 0, 0
    for I, D in todas_las_entradas(n):
        cuenta = [0]
        R = mezcla_optimizada(I, D, cuenta)
        peor = max(peor, cuenta[0])
        malo = R != correcta(I, D)
        assert malo == (I[-1] < D[-1])          # falla exactamente cuando a_n < b_n
        fallan += malo
        total += 1
    assert peor == max(0, 2 * n - 2)
    print(f"{n:>3} {peor:>10} {2 * n - 2:>5} {2 * n - 1:>10} {total:>9} {fallan:>7}")

# -------------------- Parte 4 --------------------

for n in [4, 8]:
    I, D = list(range(0, 2 * n, 2)), list(range(1, 2 * n, 2))    # intercalada perfecta
    cuenta, registro = [0], []
    R = mezcla_optimizada(I, D, cuenta, registro)
    vecinos = [tuple(sorted((v, v + 1))) for v in range(2 * n - 1)]
    comparados = {tuple(sorted(p)) for p in registro}
    faltan = [p for p in vecinos if p not in comparados]
    print(f"n = {n}: {cuenta[0]} comparaciones; pares de vecinos sin comparar: {faltan}")
    print(f"   salida:   {R}")
    print(f"   correcta: {correcta(I, D)}")
    assert R != correcta(I, D)

# -------------------- Parte 5 --------------------

random.seed(9)
fallos = 0
for _ in range(10000):
    n = random.randint(1, 20)
    valores = random.sample(range(1000), 2 * n)
    I, D = sorted(valores[:n]), sorted(valores[n:])
    fallos += mezcla_optimizada(I, D, [0]) != correcta(I, D)
print(f"falla en {100 * fallos / 10000:.1f}% de 10000 entradas al azar")
