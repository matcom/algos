import math
import random
from pathlib import Path
import matplotlib.pyplot as plt

INF = float("inf")


def mediana_inferior(A, B, cuenta=None, guardar_pasos=False):
    """
    Calcula el n-esimo menor elemento de la union de dos arreglos ordenados
    A y B de tamano n mediante busqueda binaria sobre el corte i in [0, n].
    """
    n = len(A)

    def a(idx):
        return -INF if idx < 0 else (INF if idx >= n else A[idx])

    def b(idx):
        return -INF if idx < 0 else (INF if idx >= n else B[idx])

    def es_menor(u, v):
        if cuenta is not None:
            cuenta[0] += 1
        return u < v

    lo, hi = 0, n
    pasos = []
    while True:
        i = (lo + hi) // 2
        j = n - i
        phi = hi - lo + 1
        demasiados_a = es_menor(b(j), a(i - 1))
        muy_pocos_a = False if demasiados_a else es_menor(a(i), b(j - 1))

        if guardar_pasos:
            pasos.append((lo, hi, i, j, a(i - 1), b(j), b(j - 1), a(i), demasiados_a, muy_pocos_a, phi))

        if demasiados_a:
            hi = i - 1
        elif muy_pocos_a:
            lo = i + 1
        else:
            res = max(a(i - 1), b(j - 1))
            return (res, pasos) if guardar_pasos else res


def tabla_cortes(A, B):
    """Evalua todos los cortes i in [0, n] para inspeccion y grafica."""
    n = len(A)

    def a(idx):
        return -INF if idx < 0 else (INF if idx >= n else A[idx])

    def b(idx):
        return -INF if idx < 0 else (INF if idx >= n else B[idx])

    filas = []
    for i in range(n + 1):
        j = n - i
        ai_1, bj = a(i - 1), b(j)
        bj_1, ai = b(j - 1), a(i)
        g_i = ai_1 > bj
        h_i = bj_1 > ai
        filas.append((i, j, ai_1, bj, bj_1, ai, g_i, h_i))
    return filas


if __name__ == "__main__":
    # 1. Ejemplo paso a paso para n = 5
    A_ej = [2, 5, 8, 12, 16]
    B_ej = [1, 3, 9, 10, 14]
    print(f"=== Tabla completa de cortes para A = {A_ej}, B = {B_ej} (n = 5) ===")
    print(f"{'i':>2} | {'j=n-i':>5} | {'a(i-1)':>7} | {'b(n-i)':>7} | {'b(n-i-1)':>8} | {'a(i)':>7} | {'g(i)':>6} | {'h(i)':>6} | {'Estado':>12}")
    print("-" * 80)
    for i, j, ai_1, bj, bj_1, ai, gi, hi in tabla_cortes(A_ej, B_ej):
        est = "VALIDO" if (not gi and not hi) else ("sobra A" if gi else "falta A")
        print(f"{i:>2} | {j:>5} | {str(ai_1):>7} | {str(bj):>7} | {str(bj_1):>8} | {str(ai):>7} | {str(gi):>6} | {str(hi):>6} | {est:>12}")

    med, traza_b = mediana_inferior(A_ej, B_ej, guardar_pasos=True)
    print("\nPasos de la busqueda binaria:")
    for num, (lo, hi, i, j, ai_1, bj, bj_1, ai, gi, hi_pred, phi) in enumerate(traza_b, 1):
        print(f"  Iter {num}: [lo, hi] = [{lo}, {hi}] (Phi = {phi}) -> prueba i = {i}, j = {j} | g(i)={gi}, h(i)={hi_pred}")
    print(f"Mediana inferior obtenida: max(a(2), b(1)) = {med} (oraculo: {sorted(A_ej + B_ej)[len(A_ej) - 1]})\n")

    # 2. Verificacion en 30 000 instancias aleatorias contra sorted(A + B)[n - 1]
    rng = random.Random(207)
    peor_medido = {}
    suma_medido = {}
    conteo_por_n = {}

    for _ in range(30_000):
        n = rng.randint(1, 64)
        universo = rng.choice([3, 2 * n, 1000])
        A = sorted(rng.randrange(universo) for _ in range(n))
        B = sorted(rng.randrange(universo) for _ in range(n))
        c = [0]
        res = mediana_inferior(A, B, cuenta=c)
        assert res == sorted(A + B)[n - 1]
        peor_medido[n] = max(peor_medido.get(n, 0), c[0])
        suma_medido[n] = suma_medido.get(n, 0) + c[0]
        conteo_por_n[n] = conteo_por_n.get(n, 0) + 1

    print("Verificados 30 000 casos aleatorios (con y sin repeticiones): 0 fallos.")
    print(f"\n{'n':>5} | {'Peor medido':>12} | {'Promedio':>9} | {'Cota 2(floor(log2(n+1))+1)':>27} | {'Cota inf ceil(log2(2n))':>24}")
    print("-" * 88)
    for n in [1, 2, 4, 8, 16, 32, 64]:
        cota_sup = 2 * (math.floor(math.log2(n + 1)) + 1)
        cota_inf = math.ceil(math.log2(2 * n))
        prom = suma_medido[n] / conteo_por_n[n]
        assert peor_medido[n] <= cota_sup
        print(f"{n:>5} | {peor_medido[n]:>12} | {prom:>9.2f} | {cota_sup:>27} | {cota_inf:>24}")

    # 3. Verificacion de que las 2n posiciones son alcanzables (cota de informacion)
    for n in [1, 3, 10]:
        alcanzadas = set()
        for k in range(n):
            A = [2 * t + 1 for t in range(n)]
            B = [0] * (n - 1 - k) + [10 * n] * (k + 1)
            B = [v + t * 1e-3 for t, v in enumerate(B)]
            assert mediana_inferior(A, B) == A[k]
            alcanzadas.add(("A", k))
            assert mediana_inferior(B, A) == A[k]
            alcanzadas.add(("B", k))
        assert len(alcanzadas) == 2 * n
    print("\nComprobado para n = 1, 3, 10: las 2n posiciones posibles de salida son alcanzables.")

    # 4. Generacion de la figura con 2 paneles
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.6))

    # Panel 1: diferencias monotonas en una instancia de n = 12
    n_p1 = 12
    A12 = [3, 7, 11, 14, 19, 23, 28, 31, 36, 42, 47, 53]
    B12 = [2, 5, 9, 15, 18, 22, 25, 33, 38, 41, 49, 55]
    # Para i in [1, n-1], ambas diferencias son finitas:
    # d_g(i) = a(i-1) - b(n-i) (creciente, > 0 cuando g(i) es True)
    # d_h(i) = b(n-i-1) - a(i) (decreciente, > 0 cuando h(i) es True)
    cortes_int = list(range(1, n_p1))
    diff_g = [A12[i - 1] - B12[n_p1 - i] for i in cortes_int]
    diff_h = [B12[n_p1 - i - 1] - A12[i] for i in cortes_int]

    # Encontrar corte valido
    corte_valido = [i for i in range(n_p1 + 1) if not tabla_cortes(A12, B12)[i][6] and not tabla_cortes(A12, B12)[i][7]][0]

    ax1.axhline(0, color="#333333", lw=1.2, linestyle="-")
    ax1.axvspan(corte_valido - 0.45, corte_valido + 0.45, color="#2ca02c", alpha=0.22,
                label=f"Corte valido i* = {corte_valido} (ambas <= 0)")
    ax1.plot(cortes_int, diff_g, "o-", color="#d62728", lw=2, markersize=5,
             label="a(i-1) - b(n-i)  [> 0 si g(i) es cierto]")
    ax1.plot(cortes_int, diff_h, "s-", color="#1f77b4", lw=2, markersize=5,
             label="b(n-i-1) - a(i)  [> 0 si h(i) es cierto]")

    ax1.set_title("Monotonia de las diferencias en el corte (n = 12)")
    ax1.set_xlabel("Indice del corte i (elementos tomados de A)")
    ax1.set_ylabel("Diferencia en la frontera del corte")
    ax1.set_xticks(cortes_int)
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=8.5, loc="upper left")

    # Panel 2: comparaciones medidas vs cota superior e inferior para n in [1..64]
    ns_all = sorted(peor_medido.keys())
    peores = [peor_medido[n] for n in ns_all]
    promedios = [suma_medido[n] / conteo_por_n[n] for n in ns_all]
    cota_s = [2 * (math.floor(math.log2(n + 1)) + 1) for n in ns_all]
    cota_i = [math.ceil(math.log2(2 * n)) for n in ns_all]

    ax2.step(ns_all, cota_s, where="post", color="#d62728", linestyle="--", lw=1.8,
             label="Cota superior: 2(floor(log2(n+1)) + 1)")
    ax2.plot(ns_all, peores, "o", color="#d62728", markersize=3.5, alpha=0.85,
             label="Peor caso medido")
    ax2.plot(ns_all, promedios, "-", color="#1f77b4", lw=2,
             label="Caso promedio medido")
    ax2.step(ns_all, cota_i, where="post", color="#2ca02c", linestyle="-.", lw=1.8,
             label="Cota inferior info: ceil(log2(2n))")

    ax2.set_title("Numero de comparaciones vs cotas teoricas (1 <= n <= 64)")
    ax2.set_xlabel("Tamano de cada arreglo (n)")
    ax2.set_ylabel("Comparaciones de elementos")
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=8.5, loc="lower right")

    plt.tight_layout()
    salida_png = Path(__file__).with_name("ejercicio-07.png")
    plt.savefig(salida_png, dpi=150)
    print(f"\nGrafica guardada en {salida_png.name}")
