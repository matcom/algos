"""
Mezcla "optimizada" de dos listas ordenadas.

La versión optimizada deja de comparar cuando a A le queda un solo elemento,
y lo pone al final. Este script:
  - Implementa la mezcla estándar (correcta) y la optimizada (incorrecta).
  - Cuenta comparaciones.
  - Detecta fallos contra la mezcla estándar.
  - Genera figuras:
      fig_p9_comparaciones.png : comparaciones vs n para ambas versiones.
      fig_p9_fallos.png        : tasa de fallo de la optimizada según generador.
"""
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
RUTA = os.path.join("Soluciones", "tema-1", "GlenRios")
os.makedirs(RUTA, exist_ok=True)  # crea la carpeta si no existe


def mezcla_estandar(A, B):
    """Mezcla correcta. Devuelve (resultado, comparaciones)."""
    i = j = 0
    R = []
    comps = 0
    while i < len(A) and j < len(B):
        comps += 1
        if A[i] <= B[j]:
            R.append(A[i]); i += 1
        else:
            R.append(B[j]); j += 1
    R.extend(A[i:])
    R.extend(B[j:])
    return R, comps


def mezcla_optimizada(A, B):
    """
    Mezcla 'optimizada': para cuando a A le queda 1 elemento.
    Devuelve (resultado, comparaciones).
    """
    n = len(A)
    i = j = 0
    R = []
    comps = 0
    while i < n - 1 and j < n:
        comps += 1
        if A[i] <= B[j]:
            R.append(A[i]); i += 1
        else:
            R.append(B[j]); j += 1
    # Copiar lo que quede de B
    R.extend(B[j:])
    # Poner el último de A al final
    if i < n:
        R.append(A[i])
    return R, comps


def generar_entrada_adversaria(n, rng):
    """
    Intercalada perfecta: a0 < b0 < a1 < b1 < ... < a_{n-1} < b_{n-1}.
    """
    todos = sorted(rng.sample(range(0, 10 * n), 2 * n))
    A = todos[0::2]
    B = todos[1::2]
    return A, B


def generar_entrada_aleatoria(n, rng):
    A = sorted(rng.randint(0, 10 * n) for _ in range(n))
    B = sorted(rng.randint(0, 10 * n) for _ in range(n))
    return A, B


def generar_entrada_B_pequenos(n, rng):
    """Todos los de B menores que los de A."""
    todos = sorted(rng.sample(range(0, 10 * n), 2 * n))
    return todos[n:], todos[:n]


def experimento_comparaciones():
    rng = random.Random(42)
    ns, comps_est, comps_opt = [], [], []
    print(f"{'n':>6} {'estándar':>10} {'optimizada':>12} {'2n-1':>8}")
    for n in [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]:
        A, B = generar_entrada_adversaria(n, rng)
        _, c_est = mezcla_estandar(A, B)
        _, c_opt = mezcla_optimizada(A, B)
        ns.append(n); comps_est.append(c_est); comps_opt.append(c_opt)
        print(f"{n:>6} {c_est:>10} {c_opt:>12} {2*n-1:>8}")

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(ns, comps_est, "o-", label="mezcla estándar", color="tab:blue")
    ax.plot(ns, comps_opt, "s-", label="mezcla optimizada", color="tab:red")
    ax.plot(ns, [2 * n - 1 for n in ns], "--", label="$2n-1$ (cota)",
            color="tab:orange")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("$n$"); ax.set_ylabel("comparaciones")
    ax.set_title("Mezcla estándar vs optimizada (entrada intercalada)")
    ax.legend(); ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(RUTA, "fig_p9_comparaciones.png"), dpi=150)
    plt.close(fig)
    print("  guardada fig_p9_comparaciones.png")


def experimento_fallos():
    rng = random.Random(7)
    generadores = {
        "intercalada":  generar_entrada_adversaria,
        "aleatoria":    generar_entrada_aleatoria,
        "B pequeños":   generar_entrada_B_pequenos,
    }
    nombres = list(generadores.keys())
    tasas = []
    print(f"\n{'generador':>14} {'fallos':>8}")
    for nombre, gen in generadores.items():
        fallos = 0
        total = 5000
        for _ in range(total):
            n = rng.randint(1, 10)
            A, B = gen(n, rng)
            correcto, _ = mezcla_estandar(A, B)
            optimo, _ = mezcla_optimizada(A, B)
            if correcto != optimo:
                fallos += 1
        tasa = 100 * fallos / total
        tasas.append(tasa)
        print(f"{nombre:>14} {tasa:>7.2f}%")

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.bar(nombres, tasas, color=["tab:red", "tab:blue", "tab:green"])
    ax.set_ylabel("% de fallos")
    ax.set_title("Tasa de fallo de la mezcla optimizada")
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(RUTA, "fig_p9_fallos.png"), dpi=150)
    plt.close(fig)
    print("  guardada fig_p9_fallos.png")


if __name__ == "__main__":
    experimento_comparaciones()
    experimento_fallos()
    print("\nFiguras generadas.")