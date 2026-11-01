import math
import random
import time
from itertools import permutations
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches


def es_pico(A, i):
    n = len(A)
    izq_ok = (i == 0) or (A[i] >= A[i - 1])
    der_ok = (i == n - 1) or (A[i] >= A[i + 1])
    return izq_ok and der_ok


def todos_los_picos(A):
    return [i for i in range(len(A)) if es_pico(A, i)]


def pico_1d(A, comparar_menor=None, guardar_traza=False):
    """
    Algoritmo de biseccion en exactamente <= ceil(log2 n) comparaciones.
    Mantiene el invariante de fronteras:
      (lo == 0 o A[lo-1] < A[lo]) y (hi == n-1 o A[hi] >= A[hi+1])
    """
    lo, hi = 0, len(A) - 1
    traza = []

    if comparar_menor is None:
        def comparar_menor(i, j):
            return A[i] < A[j]

    paso = 0
    while lo < hi:
        paso += 1
        m = (lo + hi) // 2
        sube_a_derecha = comparar_menor(m, m + 1)
        if guardar_traza:
            traza.append({
                "paso": paso,
                "lo": lo,
                "hi": hi,
                "m": m,
                "sube": sube_a_derecha,
                "nuevo_lo": (m + 1 if sube_a_derecha else lo),
                "nuevo_hi": (hi if sube_a_derecha else m),
                "phi_antes": hi - lo + 1,
                "phi_despues": (hi - m if sube_a_derecha else m - lo + 1),
            })
        if sube_a_derecha:
            lo = m + 1
        else:
            hi = m

    if guardar_traza:
        return lo, traza
    return lo


def pico_2d_divide_y_venceras(M):
    """
    Generalizacion a 2D (matriz n x n): encuentra un pico 2D aplicando la misma idea
    de frontera sobre la columna central. Solo parte las columnas, asi que en el peor
    caso cuesta T(n, c) = T(n, c/2) + Theta(n) = Theta(n log n) comparaciones, en lugar
    de las n^2 de la fuerza bruta. Alternando el corte entre filas y columnas se baja a
    Theta(n) (Llewellyn, Tovey y Trick); esa version no esta implementada aqui.
    """
    filas = len(M)
    cols = len(M[0])
    lo_c, hi_c = 0, cols - 1
    comparaciones = 0

    while lo_c <= hi_c:
        mid_c = (lo_c + hi_c) // 2
        # Hallar el maximo global de la columna mid_c en O(filas)
        mejor_f = 0
        for f in range(1, filas):
            comparaciones += 1
            if M[f][mid_c] > M[mejor_f][mid_c]:
                mejor_f = f

        # Comparar con los vecinos izquierdo y derecho de esa fila
        sube_izq = False
        sube_der = False
        if mid_c > lo_c:
            comparaciones += 1
            if M[mejor_f][mid_c - 1] > M[mejor_f][mid_c]:
                sube_izq = True
        if not sube_izq and mid_c < hi_c:
            comparaciones += 1
            if M[mejor_f][mid_c + 1] > M[mejor_f][mid_c]:
                sube_der = True

        if not sube_izq and not sube_der:
            return (mejor_f, mid_c), comparaciones
        elif sube_izq:
            hi_c = mid_c - 1
        else:
            lo_c = mid_c + 1

    return (0, 0), comparaciones


def es_pico_2d(M, f, c):
    filas, cols = len(M), len(M[0])
    v = M[f][c]
    if f > 0 and M[f - 1][c] > v:
        return False
    if f + 1 < filas and M[f + 1][c] > v:
        return False
    if c > 0 and M[f][c - 1] > v:
        return False
    if c + 1 < cols and M[f][c + 1] > v:
        return False
    return True


def instrumentar(A):
    cuenta = [0]

    def menor(i, j):
        cuenta[0] += 1
        return A[i] < A[j]

    return menor, cuenta


def unimodal(n, k):
    return [n - abs(i - k) for i in range(n)]


def generar_gif_pico(A, traza, idx_final, ruta_gif):
    n = len(A)
    fig, (ax_arr, ax_phi) = plt.subplots(
        1, 2, figsize=(11, 4.4), gridspec_kw={"width_ratios": [1.65, 1.0]}
    )

    frames = [None] + traza + ["FIN"]

    def actualizar(idx):
        ax_arr.clear()
        ax_phi.clear()

        estado = frames[idx]
        if estado is None:
            lo, hi = 0, n - 1
            m = None
            titulo = f"Inicio: intervalo activo [0..{n-1}], potencial Phi = {n}"
            pasos_hechos = 0
        elif estado == "FIN":
            lo = hi = idx_final
            m = None
            titulo = f"Fin en {len(traza)} comparaciones: lo = hi = {idx_final} es PICO (A[{idx_final}] = {A[idx_final]})"
            pasos_hechos = len(traza)
        else:
            lo, hi = estado["lo"], estado["hi"]
            m = estado["m"]
            dir_txt = f"A[{m}] < A[{m+1}] (sube -> derecha [{m+1}..{hi}])" if estado["sube"] else f"A[{m}] >= A[{m+1}] (baja -> izquierda [{lo}..{m}])"
            titulo = f"Paso {estado['paso']}: m = {m} | {dir_txt}"
            pasos_hechos = estado["paso"]

        colores = []
        for i in range(n):
            if estado == "FIN" and i == idx_final:
                colores.append("#2ca02c")
            elif m is not None and (i == m or i == m + 1):
                colores.append("#ff7f0e")
            elif lo <= i <= hi:
                colores.append("#1f77b4")
            else:
                colores.append("#d9d9d9")

        barras = ax_arr.bar(range(n), A, color=colores, edgecolor="#333333", width=0.72, zorder=3)
        for i, b in enumerate(barras):
            ax_arr.text(
                b.get_x() + b.get_width() / 2, b.get_height() + 0.5,
                str(A[i]), ha="center", va="bottom", fontsize=8.5, fontweight="bold"
            )

        # Sombrear el intervalo activo [lo, hi]
        rect = patches.Rectangle(
            (lo - 0.45, 0), (hi - lo + 0.9), max(A) + 4.5,
            linewidth=1.5, edgecolor="#1f77b4", facecolor="#1f77b4", alpha=0.08, zorder=1
        )
        ax_arr.add_patch(rect)

        # Mostrar las condiciones de frontera del invariante
        izq_txt = "lo=0 (borde)" if lo == 0 else f"A[{lo-1}]<A[{lo}] (sube)"
        der_txt = f"hi={n-1} (borde)" if hi == n - 1 else f"A[{hi}]>=A[{hi+1}] (baja)"
        ax_arr.text(
            (lo + hi) / 2, max(A) + 2.8,
            f"Invariante en [{lo}..{hi}]: izq [{izq_txt}] | der [{der_txt}]",
            ha="center", va="center", fontsize=8.8,
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#eef5fb", edgecolor="#1f77b4")
        )

        ax_arr.set_xticks(range(n))
        ax_arr.set_xticklabels([str(i) for i in range(n)], fontsize=8.5)
        ax_arr.set_ylim(0, max(A) + 5.5)
        ax_arr.set_xlabel("Indice i del arreglo A")
        ax_arr.set_ylabel("Valor A[i]")
        ax_arr.set_title(titulo, fontsize=10, fontweight="bold")
        ax_arr.grid(True, axis="y", alpha=0.25)

        # Panel derecho: caida exponencial del tamano del intervalo Phi
        xs_todos = list(range(len(traza) + 1))
        ys_todos = [n] + [t["phi_despues"] for t in traza]
        cota_teorica = [math.ceil(n / (2 ** k)) for k in xs_todos]

        ax_phi.plot(xs_todos, cota_teorica, "--", color="#888888", lw=1.6, label="Cota ceil(n / 2^k)")
        ax_phi.plot(xs_todos[:pasos_hechos + 1], ys_todos[:pasos_hechos + 1],
                    "o-", color="#d62728", lw=2.5, markersize=6, label="Tamano activo (hi - lo + 1)")
        ax_phi.axhline(1, color="#2ca02c", linestyle=":", lw=1.4, label="Meta Phi = 1 (pico hallado)")
        ax_phi.set_xlim(-0.2, len(traza) + 0.3)
        ax_phi.set_ylim(0, n + 1.5)
        ax_phi.set_xticks(xs_todos)
        ax_phi.set_xlabel("Comparaciones realizadas (k)")
        ax_phi.set_ylabel("Elementos candidatos en [lo..hi]")
        ax_phi.set_title("Reduccion a la mitad por biseccion", fontsize=10)
        ax_phi.grid(True, alpha=0.3)
        ax_phi.legend(loc="upper right", fontsize=8)

        plt.tight_layout()

    ani = animation.FuncAnimation(fig, actualizar, frames=len(frames), interval=1200, repeat=True)
    ani.save(ruta_gif, writer=animation.PillowWriter(fps=1))
    plt.close(fig)


if __name__ == "__main__":
    # 1. Traza detallada sobre un arreglo de 8 elementos y otro de 16 para el GIF
    A_ej8 = [3, 5, 8, 6, 12, 15, 11, 4]
    pos8, traza8 = pico_1d(A_ej8, guardar_traza=True)
    print(f"=== Traza paso a paso sobre A = {A_ej8} (n = 8) ===")
    for t in traza8:
        sentido = "sube -> derecha" if t["sube"] else "baja -> izquierda"
        print(f"Paso {t['paso']}: [{t['lo']}..{t['hi']}], m={t['m']} "
              f"(A[{t['m']}]={A_ej8[t['m']]} vs A[{t['m']+1}]={A_ej8[t['m']+1]}: {sentido}) "
              f"-> [{t['nuevo_lo']}..{t['nuevo_hi']}], tamano={t['phi_despues']}")
    print(f"Resultado devuelto: indice {pos8} (valor {A_ej8[pos8]}), es_pico={es_pico(A_ej8, pos8)}\n")

    A_gif = [4, 7, 11, 9, 6, 8, 13, 16, 19, 17, 14, 18, 22, 20, 15, 10]
    pos_gif, traza_gif = pico_1d(A_gif, guardar_traza=True)
    ruta_gif = Path(__file__).with_name("ejercicio-14-anim.gif")
    generar_gif_pico(A_gif, traza_gif, pos_gif, ruta_gif)
    print(f"GIF animado de 16 elementos guardado en {ruta_gif.name}")

    # 2. Verificacion contra fuerza bruta en 20,000 arreglos aleatorios
    rng = random.Random(503)
    for _ in range(20_000):
        n = rng.randint(1, 45)
        escala = rng.choice([2, 5, 100])
        A = [rng.randrange(escala) for _ in range(n)]
        menor, cuenta = instrumentar(A)
        idx = pico_1d(A, menor)
        assert es_pico(A, idx)
        cota = math.ceil(math.log2(n)) if n > 1 else 0
        assert cuenta[0] <= cota
    print("20,000 arreglos aleatorios verificados: siempre halla un pico en <= ceil(log2 n) comparaciones.")

    # 3. Peor caso y promedio exactos sobre todas las permutaciones (n <= 9)
    print(f"\n{'n':>3} {'peor caso (permutaciones)':>27} {'promedio':>10} {'ceil(log2 n)':>14} {'maximo (n-1)':>14}")
    datos_n = list(range(1, 17))
    peor_lista, prom_lista, cota_lista, max_lista = [], [], [], []

    for n in datos_n:
        cota = math.ceil(math.log2(n)) if n > 1 else 0
        if n <= 9:
            peor = 0
            suma = 0
            total = 0
            for P in permutations(range(n)):
                menor, cuenta = instrumentar(P)
                idx = pico_1d(P, menor)
                assert es_pico(P, idx)
                peor = max(peor, cuenta[0])
                suma += cuenta[0]
                total += 1
            prom = suma / total
            assert peor == cota
            if n in (1, 2, 3, 4, 5, 8, 9):
                print(f"{n:>3} {peor:>27} {prom:>10.2f} {cota:>14} {n - 1:>14}")
        else:
            peor = 0
            suma = 0
            muestras = 2000
            for _ in range(muestras):
                P = rng.sample(range(n), n)
                menor, cuenta = instrumentar(P)
                idx = pico_1d(P, menor)
                assert es_pico(P, idx)
                peor = max(peor, cuenta[0])
                suma += cuenta[0]
            prom = suma / muestras
        peor_lista.append(peor)
        prom_lista.append(prom)
        cota_lista.append(cota)
        max_lista.append(n - 1)

    # 4. Comprobacion de las entradas unimodales U_k de la cota inferior
    for n in [1, 2, 6, 15, 50]:
        for k in range(n):
            U = unimodal(n, k)
            assert todos_los_picos(U) == [k]
            menor, _ = instrumentar(U)
            assert pico_1d(U, menor) == k
    print("\nVerificada la familia unimodal U_k: cada posicion k es el unico pico de U_k.")

    # 5. Comparacion experimental con la generalizacion a 2D y tiempos reales
    print("\n=== Comparacion entre Pico 1D O(log n), Maximo 1D O(n) y Pico 2D por columnas ===")
    print(f"{'n':>6} {'comp Pico 1D':>14} {'comp Max 1D':>13} {'Pico 2D al azar':>16} "
          f"{'Pico 2D peor caso':>18} {'n log2 n':>9} {'celdas n^2':>12}")
    ns_2d = [8, 16, 32, 64, 128, 256]
    comp_1d_med, comp_2d_med, comp_2d_peor, comp_2d_fb = [], [], [], []
    for n_m in ns_2d:
        arr_1d = [rng.random() for _ in range(n_m)]
        menor, c1 = instrumentar(arr_1d)
        pico_1d(arr_1d, menor)

        mat_2d = [[rng.random() for _ in range(n_m)] for _ in range(n_m)]
        (f_p, c_p), c2 = pico_2d_divide_y_venceras(mat_2d)
        assert es_pico_2d(mat_2d, f_p, c_p)

        # peor caso: valores que crecen hacia la derecha, asi que siempre sigue por
        # la mitad derecha y recorre ~log2 n columnas enteras
        mat_peor = [[c * n_m + f for c in range(n_m)] for f in range(n_m)]
        (f_p, c_p), c3 = pico_2d_divide_y_venceras(mat_peor)
        assert es_pico_2d(mat_peor, f_p, c_p)

        comp_1d_med.append(c1[0])
        comp_2d_med.append(c2)
        comp_2d_peor.append(c3)
        comp_2d_fb.append(n_m * n_m)
        print(f"{n_m:>6} {c1[0]:>14} {n_m - 1:>13} {c2:>16} {c3:>18} "
              f"{round(n_m * math.log2(n_m)):>9} {n_m * n_m:>12}")

    # 6. Figura estatica de 3 paneles
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14.2, 4.3))

    n_uni = 6
    colores_u = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]
    xs = list(range(n_uni))
    for k in range(n_uni):
        uk = unimodal(n_uni, k)
        ax1.plot(xs, uk, "o--", color=colores_u[k], lw=1.5, markersize=5, alpha=0.8, label=f"U_{k} (pico={k})")
        ax1.plot([k], [uk[k]], "o", color=colores_u[k], markersize=9)
    ax1.set_title("Familia unimodal U_k (n = 6): n hojas distintas")
    ax1.set_xlabel("Indice i en el arreglo")
    ax1.set_ylabel("Valor U_k[i] = n - |i - k|")
    ax1.set_xticks(xs)
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=7.8, ncol=2)

    ax2.plot(datos_n, max_lista, "s--", color="#d62728", lw=1.6, markersize=4, label="Maximo global: n - 1")
    ax2.step(datos_n, cota_lista, where="post", color="#333333", lw=1.8, label="Cota exacta ceil(log2 n)")
    ax2.plot(datos_n, peor_lista, "o", color="#1f77b4", markersize=5, label="Pico 1D: peor caso")
    ax2.plot(datos_n, prom_lista, "^-", color="#2ca02c", lw=1.5, markersize=4, label="Pico 1D: promedio")
    ax2.set_title("Pico local 1D vs Maximo global")
    ax2.set_xlabel("Tamano del arreglo (n)")
    ax2.set_ylabel("Numero de comparaciones")
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=8)

    ax3.loglog(ns_2d, comp_2d_fb, "s--", color="#d62728", lw=1.6, label="Fuerza bruta 2D: n^2")
    ax3.loglog(ns_2d, comp_2d_peor, "o-", color="#9467bd", lw=2.0, label="Pico 2D por columnas, peor caso: Theta(n log n)")
    ax3.loglog(ns_2d, comp_2d_med, "x:", color="#9467bd", lw=1.2, label="Pico 2D por columnas, matriz al azar")
    ax3.loglog(ns_2d, [n_m - 1 for n_m in ns_2d], ":", color="#555555", lw=1.5, label="Maximo 1D: n - 1")
    ax3.loglog(ns_2d, comp_1d_med, "^-", color="#1f77b4", lw=2.0, label="Pico 1D biseccion: ceil(log2 n)")
    ax3.set_title("Escala log-log: 1D O(log n) vs 2D O(n log n) vs O(n^2)")
    ax3.set_xlabel("Lado n (arreglo de n o matriz de n x n)")
    ax3.set_ylabel("Comparaciones realizadas")
    ax3.grid(True, which="both", alpha=0.3)
    ax3.legend(fontsize=7.8)

    plt.tight_layout()
    salida = Path(__file__).with_name("ejercicio-14.png")
    plt.savefig(salida, dpi=150)
    plt.close(fig)
    print(f"\nGrafica guardada en {salida.name}")
