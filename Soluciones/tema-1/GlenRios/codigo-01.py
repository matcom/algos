import math
import os
RUTA = os.path.join("Soluciones", "tema-1", "GlenRios")
os.makedirs(RUTA, exist_ok=True)  # crea la carpeta si no existe

def max_n(costo, presupuesto):
    """Mayor n tal que costo(n) <= presupuesto."""
    alto = 2
    while costo(alto) <= presupuesto:
        alto *= 2
    bajo = alto // 2
    while bajo + 1 < alto:
        medio = (bajo + alto) // 2
        if costo(medio) <= presupuesto:
            bajo = medio
        else:
            alto = medio
    return bajo

H = 3600 * 10**9  # 1 hora a 10^9 ops/s

print(f"{'costo':>10} {'n actual':>12} {'n con 1000x':>14} {'factor':>8}")
for nombre, f in [("n^2", lambda n: n**2),
                  ("n log n", lambda n: n * math.log2(n))]:
    n0 = max_n(f, H)
    n1 = max_n(f, 1000 * H)
    print(f"{nombre:>10} {n0:>12.3g} {n1:>14.3g} {n1/n0:>8.2f}")