"""
Búsqueda en matriz n x n con filas y columnas crecientes.

Mezcla de consultas:
  - valores presentes en la matriz (elegidos al azar de celdas reales),
  - valores ausentes pero dentro del rango,
  - valores extremos (menor que todos, mayor que todos),
  - valores completamente aleatorios.

Reporta el máximo observado y el promedio de comparaciones.
"""
import random
import time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
RUTA = os.path.join("Soluciones", "tema-1", "GlenRios")
os.makedirs(RUTA, exist_ok=True)  # crea la carpeta si no existe

def matriz_ordenada(n, rng):
    """Genera una matriz n x n con filas y columnas crecientes."""
    A = [[rng.randint(0, 10 * n) for _ in range(n)] for _ in range(n)]
    for _ in range(n + 1):
        for i in range(n):
            A[i].sort()
        cambio = False
        for j in range(n):
            col_ord = sorted(A[i][j] for i in range(n))
            for i in range(n):
                if A[i][j] != col_ord[i]:
                    cambio = True
                A[i][j] = col_ord[i]
        if not cambio:
            break
    return A


def buscar_escalera(A, x):
    n = len(A)
    i, j = 0, n - 1
    comps = 0
    while i < n and j >= 0:
        comps += 1
        if A[i][j] == x:
            return True, comps
        elif A[i][j] > x:
            j -= 1
        else:
            i += 1
    return False, comps


def buscar_fuerza_bruta(A, x):
    for fila in A:
        for v in fila:
            if v == x:
                return True
    return False


def verificar_matriz_ordenada(A):
    n = len(A)
    for i in range(n):
        for j in range(1, n):
            if A[i][j - 1] > A[i][j]:
                return False
    for j in range(n):
        for i in range(1, n):
            if A[i - 1][j] > A[i][j]:
                return False
    return True


def generar_consultas(A, rng, cuantas=200):
    """
    Genera una mezcla de consultas:
      - 25% presentes en la matriz,
      - 25% ausentes pero dentro del rango,
      - 25% extremos (menor que todos / mayor que todos),
      - 25% completamente aleatorios.
    """
    n = len(A)
    lo, hi = A[0][0], A[n - 1][n - 1]
    consultas = []
    for _ in range(cuantas):
        r = rng.random()
        if r < 0.25:
            # Presente: elegir una celda al azar
            i = rng.randrange(n)
            j = rng.randrange(n)
            consultas.append(A[i][j])
        elif r < 0.50:
            # Ausente dentro del rango
            consultas.append(rng.randint(lo, hi))
        elif r < 0.75:
            # Extremo
            consultas.append(lo - 1 if rng.random() < 0.5 else hi + 1)
        else:
            # Completamente aleatorio (puede caer dentro o fuera)
            consultas.append(rng.randint(lo - 10, hi + 10))
    return consultas


def experimento():
    rng = random.Random(42)
    ns, maximos, promedios, tiempos = [], [], [], []

    print(f"{'n':>6} {'máx':>6} {'prom':>8} {'n':>6} {'2n':>6} {'tiempo (µs)':>12}")
    for n in [10, 25, 50, 100, 200, 400, 800, 1600]:
        A = matriz_ordenada(n, rng)
        assert verificar_matriz_ordenada(A), f"Matriz n={n} no ordenada"

        consultas = generar_consultas(A, rng, cuantas=300)
        comps_lista = []
        for x in consultas:
            _, c = buscar_escalera(A, x)
            comps_lista.append(c)

        maximo = max(comps_lista)
        promedio = sum(comps_lista) / len(comps_lista)

        # Tiempo con la misma mezcla
        inicio = time.perf_counter()
        reps = 100
        for _ in range(reps):
            for x in consultas[:50]:
                buscar_escalera(A, x)
        t = (time.perf_counter() - inicio) / (reps * 50) * 1e6  # µs

        ns.append(n)
        maximos.append(maximo)
        promedios.append(promedio)
        tiempos.append(t)
        print(f"{n:>6} {maximo:>6} {promedio:>8.1f} {n:>6} {2 * n:>6} {t:>12.2f}")

    # Verificación contra fuerza bruta
    fallos = 0
    for _ in range(200):
        n = rng.randint(1, 8)
        A = matriz_ordenada(n, rng)
        for _ in range(10):
            x = rng.randint(-2, 10 * n + 2)
            if buscar_escalera(A, x)[0] != buscar_fuerza_bruta(A, x):
                fallos += 1
    print(f"\nFallos contra fuerza bruta: {fallos}")

    # ---------- Figura 1: comparaciones ----------
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(ns, maximos, "o-", label="máximo observado", color="tab:red")
    ax.plot(ns, promedios, "s-", label="promedio observado", color="tab:blue")
    ax.plot(ns, [n for n in ns], "--", label="$n$ (cota superior real)", color="tab:orange")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("$n$")
    ax.set_ylabel("comparaciones")
    ax.set_title("Búsqueda en matriz ordenada: mezcla de consultas")
    ax.legend(); ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(RUTA,"fig_p6_comparaciones.png"), dpi=150)
    plt.close(fig)

    # ---------- Figura 2: tiempos ----------
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(ns, tiempos, "^-", color="tab:green")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("$n$")
    ax.set_ylabel("tiempo por búsqueda (µs)")
    ax.set_title("Tiempo de la búsqueda con mezcla de consultas")
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(RUTA,"fig_p6_tiempos.png"), dpi=150)
    plt.close(fig)

    # ---------- Figura 3: histograma de comparaciones para un n fijo ----------
    n_ejemplo = 200
    A = matriz_ordenada(n_ejemplo, rng)
    consultas = generar_consultas(A, rng, cuantas=2000)
    comps = [buscar_escalera(A, x)[1] for x in consultas]
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.hist(comps, bins=range(0, max(comps) + 2), color="tab:purple",
            edgecolor="black", alpha=0.8)
    ax.axvline(n_ejemplo, color="red", linestyle="--",
               label=f"$n = {n_ejemplo}$")
    ax.set_xlabel("comparaciones")
    ax.set_ylabel("frecuencia")
    ax.set_title(f"Distribución de comparaciones para $n = {n_ejemplo}$ "
                 f"(2000 consultas)")
    ax.legend(); ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(RUTA,"fig_p6_histograma.png"), dpi=150)
    plt.close(fig)

    print("\nFiguras generadas: fig_p6_comparaciones.png, "
          "fig_p6_tiempos.png, fig_p6_histograma.png")


if __name__ == "__main__":
    experimento()