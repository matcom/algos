import math

OPS_POR_SEGUNDO = 10**9          # supuesto de la Conferencia 1
HORA = 3600 * OPS_POR_SEGUNDO    # presupuesto B = 3.6e12 operaciones


def mayor_n(costo, presupuesto):
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


COSTOS = {
    "n log n": lambda n: n * math.log2(n),
    "n^2":     lambda n: n ** 2,
}

def factor(costo, k, base=HORA):
    """Factor n(k*B)/n(B) calculado con enteros exactos."""
    n1 = mayor_n(costo, base)
    n2 = mayor_n(costo, base * k)
    return n1, n2, n2 / n1

if __name__ == "__main__":
    print(f"{'costo':>8} {'n actual':>14} {'n con 1000x':>16} {'factor':>10}")
    for nombre in ("n log n", "n^2"):
        n1, n2, f = factor(COSTOS[nombre], 1000)
        print(f"{nombre:>8} {n1:>14,} {n2:>16,} {f:>10.2f}")
