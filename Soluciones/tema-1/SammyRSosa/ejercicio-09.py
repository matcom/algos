from collections import Counter
from itertools import combinations
from pathlib import Path
import matplotlib.pyplot as plt


def mezcla_optimizada(I, D, guardar_traza=False):
    R, i, j = [], 0, 0
    comparaciones = 0
    traza = []

    while len(I) - i > 1 and j < len(D):
        comparaciones += 1
        a_val, b_val = I[i], D[j]
        if a_val <= b_val:
            R.append(a_val)
            i += 1
            accion = f"I[{i-1}]={a_val} <= D[{j}]={b_val} -> sale {a_val} de I"
        else:
            R.append(b_val)
            j += 1
            accion = f"I[{i}]={a_val} > D[{j-1}]={b_val} -> sale {b_val} de D"
        if guardar_traza:
            traza.append((comparaciones, (a_val, b_val), accion, list(R), I[i:], D[j:]))

    if j < len(D):
        R_final = R + D[j:] + I[i:]
    else:
        R_final = R + I[i:]

    if guardar_traza:
        return R_final, comparaciones, traza
    return R_final, comparaciones


def mezcla_estandar(I, D):
    R, i, j = [], 0, 0
    comparaciones = 0
    while i < len(I) and j < len(D):
        comparaciones += 1
        if I[i] <= D[j]:
            R.append(I[i])
            i += 1
        else:
            R.append(D[j])
            j += 1
    return R + I[i:] + D[j:], comparaciones


def todas_las_intercalaciones(n):
    """Genera las C(2n, n) particiones de {1, ..., 2n} en dos listas ordenadas I y D."""
    universo = list(range(1, 2 * n + 1))
    for indices_i in combinations(range(2 * n), n):
        set_i = set(indices_i)
        I = [universo[k] for k in range(2 * n) if k in set_i]
        D = [universo[k] for k in range(2 * n) if k not in set_i]
        yield I, D


if __name__ == "__main__":
    # 1. Traza paso a paso contra el adversario intercalado para n = 3
    I_adv = [1, 3, 5]
    D_adv = [2, 4, 6]
    salida, comps, traza = mezcla_optimizada(I_adv, D_adv, guardar_traza=True)
    print("=== Traza frente al adversario intercalado (n = 3) ===")
    print(f"Entrada: I = {I_adv}, D = {D_adv}")
    for paso, par, accion, r_parcial, resto_i, resto_d in traza:
        print(f"Paso {paso}: compara {par} | {accion} | R={r_parcial}, resta I={resto_i}, D={resto_d}")
    print(f"Fin del bucle: a I le queda {I_adv[-1:]}; se concatena D restante {D_adv[1:]} y luego {I_adv[-1:]}")
    print(f"Salida obtenida: {salida} ({comps} comparaciones)")
    print(f"Salida correcta: {sorted(I_adv + D_adv)}\n")

    # 2. Tabla exhaustiva para n = 1..10 y recoleccion de datos para graficar
    print(f"{'n':>3} {'entradas':>9} {'peor_opt':>9} {'prom_opt':>9} {'peor_est':>9} {'fallos':>8} {'equiv_an<bn':>12}")
    ns = list(range(1, 11))
    peor_opt_lista, prom_opt_lista = [], []
    peor_est_lista, prom_est_lista = [], []

    hist_aciertos_n8 = Counter()
    hist_fallos_n8 = Counter()

    for n in ns:
        peor_opt, suma_opt = 0, 0
        peor_est, suma_est = 0, 0
        fallos, total = 0, 0
        caracterizacion_exacta = True

        for I, D in todas_las_intercalaciones(n):
            R_opt, c_opt = mezcla_optimizada(I, D)
            _, c_est = mezcla_estandar(I, D)

            peor_opt = max(peor_opt, c_opt)
            suma_opt += c_opt
            peor_est = max(peor_est, c_est)
            suma_est += c_est

            falla = (R_opt != sorted(I + D))
            fallos += int(falla)
            total += 1
            caracterizacion_exacta = caracterizacion_exacta and (falla == (I[-1] < D[-1]))

            if n == 8:
                if falla:
                    hist_fallos_n8[c_opt] += 1
                else:
                    hist_aciertos_n8[c_opt] += 1

        prom_opt = suma_opt / total
        prom_est = suma_est / total
        peor_opt_lista.append(peor_opt)
        prom_opt_lista.append(prom_opt)
        peor_est_lista.append(peor_est)
        prom_est_lista.append(prom_est)

        print(f"{n:>3} {total:>9} {peor_opt:>9} {prom_opt:>9.2f} {peor_est:>9} "
              f"{100 * fallos / total:>7.1f}% {'si' if caracterizacion_exacta else 'no':>12}")

    # Para n = 11 y 12 completamos las curvas teoricas / empiricas del panel 1
    # Sabemos que peor_opt = 2n - 2, peor_est = 2n - 1, y calculamos el promedio por conteo exacto:
    # En la mezcla estandar, E[C] = 2n - 2n / (n + 1).
    # En la mezcla optimizada, podemos evaluar o usar la formula exacta sobre C(2n, n).
    for n in (11, 12):
        ns.append(n)
        peor_opt_lista.append(2 * n - 2)
        peor_est_lista.append(2 * n - 1)
        # Calculo combinatorio rapido del promedio para n=11, 12:
        # El bucle termina con k elementos restantes: si se vacia D quedan k>=2 en I;
        # si queda 1 en I quedan k>=1 en D.
        total_combinaciones = math.comb(2 * n, n) if "math" in globals() else 1
        # Como C(22,11)=705432 y C(24,12)=2704156, usamos la suma combinatoria directa:
        from math import comb
        total_c = comb(2 * n, n)
        suma_c_est = 0
        suma_c_opt = 0
        # Si D se vacia cuando en I quedan r >= 1 elementos (el ultimo en salir de D fue el paso 2n - r):
        # hay C(2n - r - 1, n - 1) formas en que D se vacia primero, y en igual numero I se vacia primero.
        for r in range(1, n + 1):
            formas_d_vacia = comb(2 * n - r - 1, n - 1)
            formas_i_vacia = comb(2 * n - r - 1, n - 1)
            suma_c_est += (2 * n - r) * (formas_d_vacia + formas_i_vacia)
            # Para mezcla_optimizada:
            # - Si D se vacia quedando r >= 2 en I, hace 2n - r comparaciones (C(2n - r - 1, n - 1) casos)
            # - Si I llega a quedar con 1 elemento cuando en D quedan s >= 1 elementos:
            #   el elemento n-1 de I sale en el paso (n - 1) + (n - s) = 2n - 1 - s comparaciones.
            #   La cantidad de formas es C(2n - 1 - s - 1, n - 2) = C(2n - s - 2, n - 2).
        for r in range(2, n + 1):
            suma_c_opt += (2 * n - r) * comb(2 * n - r - 1, n - 1)
        for s in range(1, n + 1):
            suma_c_opt += (2 * n - 1 - s) * comb(2 * n - s - 2, n - 2)
        prom_opt_lista.append(suma_c_opt / total_c)
        prom_est_lista.append(suma_c_est / total_c)

    # 3. Generacion de la figura con 2 paneles
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.4))

    ax1.plot(ns, peor_est_lista, "s--", color="#d62728", lw=1.8, markersize=5,
             label="Cota / peor caso mezcla correcta (2n - 1)")
    ax1.plot(ns, peor_opt_lista, "o-", color="#1f77b4", lw=2, markersize=5,
             label="Peor caso mezcla optimizada (2n - 2)")
    ax1.plot(ns, prom_est_lista, "^:", color="#ff7f0e", lw=1.6, markersize=5,
             label="Promedio mezcla correcta")
    ax1.plot(ns, prom_opt_lista, "d-.", color="#2ca02c", lw=1.8, markersize=5,
             label="Promedio mezcla optimizada")
    ax1.set_title("Comparaciones: peor caso y promedio (n = 1..12)")
    ax1.set_xlabel("Tamano de cada lista (n)")
    ax1.set_ylabel("Numero de comparaciones")
    ax1.set_xticks(ns)
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=8.5)

    valores_c = sorted(set(hist_aciertos_n8.keys()) | set(hist_fallos_n8.keys()))
    aciertos_vals = [hist_aciertos_n8[c] for c in valores_c]
    fallos_vals = [hist_fallos_n8[c] for c in valores_c]

    ax2.bar(valores_c, aciertos_vals, width=0.6, color="#2ca02c", alpha=0.85,
            label="Entradas donde acierta (a_n > b_n, 50%)")
    ax2.bar(valores_c, fallos_vals, width=0.6, bottom=aciertos_vals, color="#d62728", alpha=0.85,
            label="Entradas donde falla (a_n < b_n, 50%)")
    ax2.axvline(2 * 8 - 1, color="#333333", linestyle="--", lw=1.5,
                label="Cota necesaria en peor caso (2n - 1 = 15)")
    ax2.set_title("Distribucion de las C(16, 8) = 12870 entradas (n = 8)")
    ax2.set_xlabel("Comparaciones realizadas por mezcla_optimizada")
    ax2.set_ylabel("Cantidad de intercalaciones")
    ax2.set_xticks(range(min(valores_c), 2 * 8))
    ax2.grid(True, axis="y", alpha=0.3)
    ax2.legend(fontsize=8.5)

    plt.tight_layout()
    salida_png = Path(__file__).with_name("ejercicio-09.png")
    plt.savefig(salida_png, dpi=150)
    print(f"\nGrafica guardada en {salida_png.name}")
