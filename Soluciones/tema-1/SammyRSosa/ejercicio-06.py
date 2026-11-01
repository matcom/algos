import random
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np


def escalera(M, x, comparar=None, columna_inicial=None, guardar_camino=False):
    """
    Busca el valor x en una matriz n x n con filas y columnas crecientes,
    partiendo de la esquina superior derecha (0, n - 1).
    """
    n = len(M)
    i = 0
    j = (n - 1) if columna_inicial is None else columna_inicial
    camino = []

    if comparar is None:
        def comparar(f, c):
            return (x > M[f][c]) - (x < M[f][c])

    while i < n and j >= 0:
        phi = (n - i) + (j + 1)
        r = comparar(i, j)
        if guardar_camino:
            camino.append((i, j, M[i][j], phi, r))
        if r == 0:
            return (True, camino) if guardar_camino else True
        elif r < 0:
            j -= 1
        else:
            i += 1

    return (False, camino) if guardar_camino else False


def matriz_ordenada_azar(n, rng):
    """Genera una matriz n x n con filas y columnas crecientes (con posibles repeticiones)."""
    filas = sorted(rng.randrange(3 * n) for _ in range(n))
    cols = sorted(rng.randrange(3 * n) for _ in range(n))
    return [[filas[i] + cols[j] for j in range(n)] for i in range(n)]


def matriz_adversario(n):
    """
    Construye la matriz base B del adversario para x = n - 1:
    B[i][j] = n - 1.5 en la antidiagonal (i + j == n - 1), e i + j en el resto.
    """
    return [[(n - 1.5) if i + j == n - 1 else float(i + j) for j in range(n)] for i in range(n)]


def es_estrictamente_creciente(M):
    n = len(M)
    filas_ok = all(M[i][j] < M[i][j + 1] for i in range(n) for j in range(n - 1))
    cols_ok = all(M[i][j] < M[i + 1][j] for i in range(n - 1) for j in range(n))
    return filas_ok and cols_ok


def celdas_libres(n):
    """Las 2n - 1 celdas que pueden valer x = n - 1 sin romper el orden de B: la
    antidiagonal (i + j = n - 1) y la diagonal justo debajo (i + j = n)."""
    return [(k, n - 1 - k) for k in range(n)] + [(k, n - k) for k in range(1, n)]


def auditar_contra_adversario(algoritmo, n):
    """Ejecuta el algoritmo frente a B y devuelve (respuesta, celdas libres no vistas)."""
    x = n - 1
    B = matriz_adversario(n)
    vistas = set()

    def comparar(i, j):
        vistas.add((i, j))
        return (x > B[i][j]) - (x < B[i][j])

    resp = algoritmo(B, x, comparar)
    no_vistas = [c for c in celdas_libres(n) if c not in vistas]
    return resp, no_vistas


if __name__ == "__main__":
    # 1. Traza paso a paso sobre la matriz 4x4 del adversario con x = 3
    n_ej = 4
    x_ej = n_ej - 1
    B4 = matriz_adversario(n_ej)
    hallado, traza = escalera(B4, x_ej, guardar_camino=True)
    print(f"=== Traza en la matriz 4x4 del adversario (antidiagonal = 2.5, x = {x_ej}) ===")
    for fila in B4:
        print("  ", [f"{v:4.1f}" for v in fila])
    print(f"\n{'Paso':>4} | {'Celda (i, j)':>12} | {'M[i][j]':>7} | {'Comparacion':>13} | {'Accion':>16} | {'Phi':>4}")
    print("-" * 70)
    for idx, (i, j, val, phi, r) in enumerate(traza, 1):
        comp_str = "x < M[i][j]" if r < 0 else ("x > M[i][j]" if r > 0 else "x == M[i][j]")
        acc_str = "j <- j - 1 (izq)" if r < 0 else ("i <- i + 1 (abajo)" if r > 0 else "encontrado")
        print(f"{idx:>4} | ({i}, {j}){'':>6} | {val:>7.1f} | {comp_str:>13} | {acc_str:>16} | {phi:>4}")
    print(f"Resultado final: {hallado} en {len(traza)} comparaciones (2n - 1 = {2 * n_ej - 1}).\n")

    # 2. Verificacion contra oraculo en 20 000 matrices aleatorias
    rng = random.Random(106)
    peor_por_n = {}
    for _ in range(20_000):
        n = rng.randint(1, 12)
        M = matriz_ordenada_azar(n, rng)
        x = rng.randrange(-2, 6 * n + 2)
        pasos = [0]

        def comp(i, j):
            pasos[0] += 1
            return (x > M[i][j]) - (x < M[i][j])

        res = escalera(M, x, comparar=comp)
        esperado = any(x in fila for fila in M)
        assert res == esperado
        assert pasos[0] <= 2 * n - 1
        peor_por_n[n] = max(peor_por_n.get(n, 0), pasos[0])

    print("Verificadas 20 000 busquedas contra fuerza bruta: 0 fallos.")
    print("Peor caso medido por n:", {k: peor_por_n[k] for k in sorted(peor_por_n)})

    # 3. Verificacion del adversario y de las 2n - 1 matrices perturbadas B_c
    for n in [1, 2, 4, 8, 25]:
        B = matriz_adversario(n)
        assert es_estrictamente_creciente(B)
        assert not any(v == n - 1 for fila in B for v in fila)
        for (i, j) in celdas_libres(n):
            Bc = [fila[:] for fila in B]
            Bc[i][j] = float(n - 1)
            assert es_estrictamente_creciente(Bc)
    print("Verificado: B y las 2n - 1 matrices perturbadas B_c (antidiagonal y diagonal de abajo) "
          "mantienen filas y columnas estrictamente crecientes.")

    def escalera_incompleta(M, x, comparar):
        return escalera(M, x, comparar=comparar, columna_inicial=len(M) - 2)

    print(f"\n{'n':>4} | {'celdas libres':>13} | {'escalera: libres sin mirar':>26} | {'incompleta: libres sin mirar':>28}")
    for n in [4, 16, 64]:
        _, sin_mirar_ok = auditar_contra_adversario(escalera, n)
        _, sin_mirar_mal = auditar_contra_adversario(escalera_incompleta, n)
        print(f"{n:>4} | {2 * n - 1:>13} | {len(sin_mirar_ok):>26} | {len(sin_mirar_mal):>28}")
        assert len(sin_mirar_ok) == 0
        if sin_mirar_mal:
            i, j = sin_mirar_mal[0]
            Bc = matriz_adversario(n)
            Bc[i][j] = float(n - 1)
            assert escalera_incompleta(Bc, n - 1, None) is False

    # 4. Generacion de la figura con 2 paneles
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8))

    # Panel 1: cuadricula 8x8 mostrando el zigzag de 2n - 1 pasos frente al adversario
    n_grid = 8
    B8 = matriz_adversario(n_grid)
    _, cam_peor = escalera(B8, n_grid - 1, guardar_camino=True)

    # Segundo camino sobre la misma B8: buscar x = 9.0 (aparece en (3,6), (4,5), (5,4), (6,3)...)
    # o en B_k con k = 3 (donde B_3[3][4] = 7.0) buscando x = 7: se detiene al hallarlo en (3, 4)
    B8_k3 = [fila[:] for fila in B8]
    B8_k3[3][4] = 7.0
    _, cam_exito = escalera(B8_k3, 7.0, guardar_camino=True)

    matriz_color = np.zeros((n_grid, n_grid))
    for i in range(n_grid):
        for j in range(n_grid):
            if i + j == n_grid - 1:
                matriz_color[i, j] = 1.0  # antidiagonal del adversario

    ax1.imshow(matriz_color, cmap="YlOrBr", alpha=0.35, vmin=0, vmax=1.5)
    for i in range(n_grid):
        for j in range(n_grid):
            val_txt = f"{B8[i][j]:.1f}" if i + j == n_grid - 1 else f"{int(B8[i][j])}"
            ax1.text(j, i, val_txt, ha="center", va="center", fontsize=8, color="#333333")

    # Trazar camino del peor caso en B (x = 7 no esta)
    ys_p = [c[0] for c in cam_peor]
    xs_p = [c[1] for c in cam_peor]
    ax1.plot(xs_p, ys_p, "o-", color="#d62728", lw=2.2, markersize=5.5,
             label=f"En B (x=7 no esta): {len(cam_peor)} pasos")

    # Trazar camino cuando x = 7 esta en (3, 4) (matriz B_3)
    ys_e = [c[0] for c in cam_exito]
    xs_e = [c[1] for c in cam_exito]
    ax1.plot([x + 0.08 for x in xs_e], [y - 0.08 for y in ys_e], "s--", color="#1f77b4", lw=2.0, markersize=5,
             label=f"En B_3 (x=7 en (3,4)): {len(cam_exito)} pasos")

    ax1.set_title("Recorrido en escalera sobre matriz 8x8 del adversario")
    ax1.set_xlabel("Columna j")
    ax1.set_ylabel("Fila i")
    ax1.set_xticks(range(n_grid))
    ax1.set_yticks(range(n_grid))
    ax1.legend(loc="lower right", fontsize=8.5)

    # Panel 2: comparaciones al crecer n (peor caso 2n-1, promedio aleatorio, cota inferior 2n-1)
    ns = list(range(2, 31, 2))
    cota_sup = [2 * n - 1 for n in ns]
    cota_inf = [2 * n - 1 for n in ns]
    prom_azar = []
    peor_emp = []

    for n in ns:
        # El adversario alcanza siempre 2n - 1
        _, cam_adv = escalera(matriz_adversario(n), n - 1, guardar_camino=True)
        peor_emp.append(len(cam_adv))
        # Promedio en matrices aleatorias
        total_p = 0
        rep = 300
        for _ in range(rep):
            M_r = matriz_ordenada_azar(n, rng)
            x_r = rng.randrange(-2, 6 * n + 2)
            _, cam_r = escalera(M_r, x_r, guardar_camino=True)
            total_p += len(cam_r)
        prom_azar.append(total_p / rep)

    ax2.plot(ns, cota_sup, "-", color="#d62728", lw=2, label="Cota superior: 2n - 1")
    ax2.plot(ns, peor_emp, "o", color="#d62728", markersize=5, label="Peor caso medido (adversario)")
    ax2.plot(ns, prom_azar, "s-", color="#1f77b4", lw=1.8, markersize=4, label="Promedio en busquedas al azar")
    ax2.plot(ns, cota_inf, "--", color="#2ca02c", lw=2, label="Cota inferior del adversario: 2n - 1 (coincide)")
    ax2.plot(ns, ns, ":", color="#888888", lw=1.4, label="Referencia: n")

    ax2.set_title("Costo en comparaciones segun el tamano n")
    ax2.set_xlabel("Dimension de la matriz (n)")
    ax2.set_ylabel("Numero de comparaciones")
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=8.5)

    plt.tight_layout()
    salida_png = Path(__file__).with_name("ejercicio-06.png")
    plt.savefig(salida_png, dpi=150)
    print(f"\nGrafica guardada en {salida_png.name}")
