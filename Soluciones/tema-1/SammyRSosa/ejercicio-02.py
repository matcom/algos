import math
import random
from pathlib import Path
import matplotlib.pyplot as plt


def busqueda_binaria(A, x, vigilar=False, guardar_traza=False):
    """
    Busca x en el arreglo estrictamente creciente A[0..n).
    Devuelve (indice o None, numero de comparaciones[, traza]).
    """
    lo, hi = 0, len(A)
    comparaciones = 0
    traza = []

    while lo < hi:
        if vigilar:
            assert 0 <= lo < hi <= len(A)
            assert all(v < x for v in A[:lo])
            assert all(v > x for v in A[hi:])

        phi_antes = hi - lo
        m = (lo + hi) // 2
        comparaciones += 1
        val_m = A[m]

        if x == val_m:
            if guardar_traza:
                traza.append((comparaciones, lo, hi, m, val_m, "=", 0))
                return m, comparaciones, traza
            return m, comparaciones
        elif x < val_m:
            hi = m
            rel = "<"
        else:
            lo = m + 1
            rel = ">"

        phi_despues = hi - lo
        if vigilar:
            assert phi_despues <= phi_antes // 2

        if guardar_traza:
            traza.append((comparaciones, lo, hi, m, val_m, rel, phi_despues))

    if vigilar:
        assert lo == hi
        assert all(v < x for v in A[:lo]) and all(v > x for v in A[lo:])

    if guardar_traza:
        return None, comparaciones, traza
    return None, comparaciones


if __name__ == "__main__":
    # 1. Trazas de ejemplo sobre un arreglo de 10 elementos
    A_ej = [4, 9, 15, 22, 31, 38, 44, 57, 63, 70]
    print(f"Arreglo de ejemplo (n = {len(A_ej)}): {A_ej}\n")

    for objetivo, desc in [(22, "elemento presente"), (25, "ausente, cae en hueco")]:
        pos, comps, traza = busqueda_binaria(A_ej, objetivo, vigilar=True, guardar_traza=True)
        print(f"--- Busqueda de x = {objetivo} ({desc}) | Phi_0 = {len(A_ej)} ---")
        for paso, lo_d, hi_d, m, val_m, rel, phi_d in traza:
            print(f"Paso {paso}: m={m}, A[m]={val_m:>2} ({objetivo} {rel} {val_m}) "
                  f"-> nuevo [lo, hi) = [{lo_d}, {hi_d}), Phi = {phi_d}")
        print(f"Resultado: pos = {pos}, comparaciones = {comps}\n")

    # 2. Verificacion aleatoria del invariante y del potencial
    rng = random.Random(1042)
    pruebas = 3500
    for _ in range(pruebas):
        n = rng.randint(0, 50)
        A = sorted(rng.sample(range(300), n))
        x = rng.randrange(-10, 310)
        pos, _ = busqueda_binaria(A, x, vigilar=True)
        assert (pos is None and x not in A) or (pos is not None and A[pos] == x)
    print(f"Invariante y potencial verificados en {pruebas} busquedas aleatorias: 0 fallos.\n")

    # 3. Comparacion contra la cota de informacion ceil(log2(n + 1))
    print(f"{'n':>5} | {'Peor caso':>10} | {'Prom. huecos':>13} | {'Prom. exito':>12} | {'ceil(log2(n+1))':>16}")
    print("-" * 68)
    for n in [1, 3, 7, 8, 15, 16, 31, 32, 64, 100, 150]:
        A = [2 * i + 1 for i in range(n)]
        costos_huecos = [busqueda_binaria(A, 2 * i)[1] for i in range(n + 1)]
        costos_exito = [busqueda_binaria(A, 2 * i + 1)[1] for i in range(n)]
        peor = max(costos_huecos + costos_exito)
        cota = math.ceil(math.log2(n + 1))
        assert peor == cota
        prom_h = sum(costos_huecos) / len(costos_huecos)
        prom_e = sum(costos_exito) / len(costos_exito)
        print(f"{n:>5} | {peor:>10} | {prom_h:>13.2f} | {prom_e:>12.2f} | {cota:>16}")

    # 4. Generacion de la grafica en 2 paneles
    ns = list(range(1, 151))
    peores, prom_huecos, prom_exitos, cotas = [], [], [], []
    for n in ns:
        A = [2 * i + 1 for i in range(n)]
        ch = [busqueda_binaria(A, 2 * i)[1] for i in range(n + 1)]
        ce = [busqueda_binaria(A, 2 * i + 1)[1] for i in range(n)]
        peores.append(max(ch + ce))
        prom_huecos.append(sum(ch) / len(ch))
        prom_exitos.append(sum(ce) / len(ce))
        cotas.append(math.ceil(math.log2(n + 1)))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.4))

    # Panel 1: Escalera de peor caso y promedios vs ceil(log2(n+1))
    ax1.step(ns, cotas, where="post", color="#1f77b4", lw=2.2,
             label="Cota teorica y peor caso: ceil(log2(n+1))")
    ax1.plot(ns, prom_huecos, "-", color="#ff7f0e", lw=1.6,
             label="Promedio en los n+1 huecos (sin exito)")
    ax1.plot(ns, prom_exitos, "--", color="#2ca02c", lw=1.6,
             label="Promedio en los n elementos (con exito)")
    ax1.set_title("Comparaciones en busqueda binaria para n en [1, 150]")
    ax1.set_xlabel("Tamano del arreglo n")
    ax1.set_ylabel("Numero de comparaciones")
    ax1.set_yticks(range(1, 9))
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc="lower right", fontsize=8.5)

    # Panel 2: Caida del potencial Phi_k = hi - lo paso a paso para n = 100
    n_pot = 100
    A_pot = [2 * i + 1 for i in range(n_pot)]
    max_k = math.ceil(math.log2(n_pot + 1))
    pasos_k = list(range(0, max_k + 1))
    cota_pot = [n_pot // (2 ** k) for k in pasos_k]

    _, _, traza_der = busqueda_binaria(A_pot, 2 * n_pot, guardar_traza=True)
    phis_der = [n_pot] + [t[6] for t in traza_der]

    _, _, traza_izq = busqueda_binaria(A_pot, 0, guardar_traza=True)
    phis_izq = [n_pot] + [t[6] for t in traza_izq]

    _, _, traza_exito = busqueda_binaria(A_pot, A_pot[74], guardar_traza=True)
    phis_exito = [n_pot] + [t[6] for t in traza_exito]

    ax2.plot(pasos_k, cota_pot, "s--", color="#555555", lw=1.8, markersize=5,
             label="Cota superior floor(n / 2^k)")
    ax2.plot(range(len(phis_izq)), phis_izq, "o-", color="#1f77b4", lw=2, markersize=4.5,
             label="Hueco extremo izquierdo (x < A[0])")
    ax2.plot(range(len(phis_der)), phis_der, "^-", color="#d62728", lw=1.8, markersize=4.5,
             label="Hueco extremo derecho (x > A[n-1])")
    ax2.plot(range(len(phis_exito)), phis_exito, "d-", color="#2ca02c", lw=1.8, markersize=4.5,
             label="Elemento encontrado en m (x = A[74])")
    ax2.set_title("Caida del potencial Phi_k = hi - lo (n = 100)")
    ax2.set_xlabel("Iteracion k")
    ax2.set_ylabel("Potencial Phi_k = hi - lo")
    ax2.set_xticks(pasos_k)
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc="upper right", fontsize=8.5)

    plt.tight_layout()
    salida_png = Path(__file__).with_name("ejercicio-02.png")
    plt.savefig(salida_png, dpi=150)
    print(f"\nGrafica guardada en {salida_png.name}")
