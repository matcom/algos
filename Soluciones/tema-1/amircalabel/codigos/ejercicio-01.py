

import math

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

def main():
    hora = 3600 * 10**9
    costos = {
        "n": lambda n: n,
        "n log n": lambda n: n * math.log2(n),
        "n^2": lambda n: n ** 2,
        "n^3": lambda n: n ** 3,
        "2^n": lambda n: 2 ** n,
    }
    print(f"{'costo':>8} {'actual':>14} {'1000x':>14} {'factor':>10}")
    for nombre, costo in costos.items():
        n0 = mayor_n(costo, hora)
        n1 = mayor_n(costo, 1000 * hora)
        print(f"{nombre:>8} {n0:>14.4g} {n1:>14.4g} {n1/n0:>10.2f}")

if __name__ == "__main__":
    main()
