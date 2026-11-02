def busqueda_binaria(A, x):
    lo, hi = 0, len(A)
    comps = 0
    while lo < hi:
        mid = (lo + hi) // 2
        comps += 1
        if A[mid] == x:
            return mid, comps
        elif A[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return None, comps

import math
import os
RUTA = os.path.join("Soluciones", "tema-1", "GlenRios")
os.makedirs(RUTA, exist_ok=True)  # crea la carpeta si no existe
print(f"{'n':>5} {'comparaciones':>15} {'log2(n+1)':>12}")
for k in range(1, 11):
    n = 2**k - 1
    A = list(range(n))
    _, comps = busqueda_binaria(A, n)  # x = n no está, peor caso
    print(f"{n:>5} {comps:>15} {math.log2(n+1):>12.0f}")