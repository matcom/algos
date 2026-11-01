import math


def factor_nlogn(S, n0, iteraciones=50):
    """Resuelve k = S / (1 + log2(k)/log2(n0)) por punto fijo."""
    log2_n0 = math.log2(n0)
    k = S  # primera estimacion: ignorar el termino logaritmico
    for _ in range(iteraciones):
        k = S / (1 + math.log2(k) / log2_n0)
    return k


def mayor_n(costo, presupuesto):
    """El mayor n con costo(n) <= presupuesto, por busqueda binaria (C1, S7)."""
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


if __name__ == "__main__":
    # --- seccion 3: resolver el factor de n log n por punto fijo ---
    n0 = 9.857e10  # n0 real para una hora a 10^9 operaciones por segundo
    k = factor_nlogn(1000, n0)
    print(f"factor estimado para n log n: {k:.1f}")       # aprox 791.4
    print(f"factor exacto para n^2:        {1000 ** 0.5:.2f}")  # 31.62

    print()

    # --- seccion 4: verificacion exacta reutilizando mayor_n de la conferencia 1 ---
    costos = {
        "n^2":     lambda n: n ** 2,
        "n log n": lambda n: n * math.log2(n),
    }

    hora = 3600 * 10**9          # presupuesto a 10^9 operaciones/segundo, una hora
    S = 1000

    print(f"{'costo':>9} {'n0 (actual)':>14} {'n1 (1000x)':>14} "
          f"{'factor medido':>14} {'factor teorico':>14}")
    for nombre, costo in costos.items():
        n0 = mayor_n(costo, hora)
        n1 = mayor_n(costo, hora * S)
        medido = n1 / n0
        teorico = (S ** 0.5) if nombre == "n^2" else factor_nlogn(S, n0)
        print(f"{nombre:>9} {n0:>14.4g} {n1:>14.4g} {medido:>14.3f} {teorico:>14.3f}")

    print()

    # --- seccion 5: si hardware Y datos crecen por un factor F cada decada ---
    # para Theta(n^p), tiempo(k decadas) / tiempo(0) = F^(k*(p-1))
    F = 10
    print(f"{'decada':>7} {'+anios':>7} {'lineal (p=1)':>13} {'cuadratico (p=2)':>17} {'cubico (p=3)':>13}")
    for k in range(4):
        fila = [F ** (k * (p - 1)) for p in (1, 2, 3)]
        print(f"{k:>7} {10*k:>7} {fila[0]:>13} {fila[1]:>17} {fila[2]:>13}")
