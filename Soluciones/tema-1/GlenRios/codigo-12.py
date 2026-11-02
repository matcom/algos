"""
Problema 12: Gale-Shapley con listas incompletas.

Experimentos:
  - Verificación de estabilidad contra el oráculo (chequeo de parejas bloqueantes).
  - Número de propuestas vs n, comparado con el caso completo.
  - Fracción de agentes solteros en función de la densidad de la red.
  - Ejemplo de un emparejamiento en un grafo bipartito pequeño.

Genera:
  fig_p12_verificacion.png : confirmación de 0 fallos de estabilidad.
  fig_p12_propuestas.png   : propuestas vs n (incompletas vs completas).
  fig_p12_solteros.png     : fracción de solteros vs densidad.
  fig_p12_ejemplo.png      : visualización de un emparejamiento pequeño.
"""
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
RUTA = os.path.join("Soluciones", "tema-1", "GlenRios")
os.makedirs(RUTA, exist_ok=True)  # crea la carpeta si no existe


# ----------------------------------------------------------------------
# Generador de instancias con listas incompletas
# ----------------------------------------------------------------------

def generar_instancia(n, densidad, rng):
    """
    Genera listas incompletas con una probabilidad `densidad` de que un par
    (a, b) sea mutuamente aceptable.
    Devuelve pref_a, pref_b.
    """
    # Grafo bipartito subyacente
    aceptables = {(a, b) for a in range(n) for b in range(n)
                  if rng.random() < densidad}
    # Listas de preferencias: ordenar los vecinos al azar
    pref_a = [[] for _ in range(n)]
    pref_b = [[] for _ in range(n)]
    for a in range(n):
        vecinos = [b for b in range(n) if (a, b) in aceptables]
        rng.shuffle(vecinos)
        pref_a[a] = vecinos
    for b in range(n):
        vecinos = [a for a in range(n) if (a, b) in aceptables]
        rng.shuffle(vecinos)
        pref_b[b] = vecinos
    return pref_a, pref_b


def generar_instancia_completa(n, rng):
    """Listas completas (todas las permutaciones)."""
    pref_a = [rng.sample(range(n), n) for _ in range(n)]
    pref_b = [rng.sample(range(n), n) for _ in range(n)]
    return pref_a, pref_b


# ----------------------------------------------------------------------
# Algoritmo
# ----------------------------------------------------------------------

def gale_shapley_incompleto(pref_a, pref_b):
    """
    Gale-Shapley con listas incompletas.
    Devuelve match_a, match_b (con -1 si está solo) y el número de propuestas.
    """
    n = len(pref_a)
    # rank[b][a] = posición de a en la lista de b (para comparar rápido)
    rank_b = [dict() for _ in range(n)]
    for b in range(n):
        for lugar, a in enumerate(pref_b[b]):
            rank_b[b][a] = lugar

    match_a = [-1] * n
    match_b = [-1] * n
    siguiente = [0] * n  # a qué índice de su lista va a proponer
    propuestas = 0
    libres = list(range(n))

    while libres:
        a = libres.pop()
        if siguiente[a] == len(pref_a[a]):
            continue  # agotó su lista, queda solo
        b = pref_a[a][siguiente[a]]
        siguiente[a] += 1
        propuestas += 1

        # b acepta solo si a está en su lista
        if a not in rank_b[b]:
            libres.append(a)  # rechazado por no aceptable
            continue

        actual = match_b[b]
        if actual == -1:
            match_a[a] = b
            match_b[b] = a
        elif rank_b[b][a] < rank_b[b][actual]:
            # b prefiere a a su pareja actual
            match_a[actual] = -1
            libres.append(actual)
            match_a[a] = b
            match_b[b] = a
        else:
            libres.append(a)  # b prefiere a su actual

    return match_a, match_b, propuestas


# ----------------------------------------------------------------------
# Verificación de estabilidad
# ----------------------------------------------------------------------

def es_estable(match_a, match_b, pref_a, pref_b):
    """
    Verifica que no exista pareja bloqueante.
    Devuelve True si el emparejamiento es estable.
    """
    n = len(pref_a)
    rank_a = [dict() for _ in range(n)]
    for a in range(n):
        for lugar, b in enumerate(pref_a[a]):
            rank_a[a][b] = lugar
    rank_b = [dict() for _ in range(n)]
    for b in range(n):
        for lugar, a in enumerate(pref_b[b]):
            rank_b[b][a] = lugar

    for a in range(n):
        for b in pref_a[a]:  # solo mutuamente aceptables
            if b not in rank_b[b] and a not in rank_b[b]:
                continue
            if a not in rank_b[b]:
                continue

            # ¿a prefiere b a su pareja actual?
            if match_a[a] == -1:
                a_prefiere = True
            else:
                a_prefiere = rank_a[a][b] < rank_a[a][match_a[a]]

            # ¿b prefiere a a su pareja actual?
            if match_b[b] == -1:
                b_prefiere = True
            else:
                b_prefiere = rank_b[b][a] < rank_b[b][match_b[b]]

            if a_prefiere and b_prefiere:
                return False
    return True


# ----------------------------------------------------------------------
# Experimentos
# ----------------------------------------------------------------------

def experimento_verificacion(n_sims=2000):
    rng = random.Random(42)
    fallos = 0
    for _ in range(n_sims):
        n = rng.randint(2, 15)
        densidad = rng.uniform(0.2, 1.0)
        pref_a, pref_b = generar_instancia(n, densidad, rng)
        match_a, match_b, _ = gale_shapley_incompleto(pref_a, pref_b)
        if not es_estable(match_a, match_b, pref_a, pref_b):
            fallos += 1
    print(f"Verificación: {fallos} fallos de estabilidad en {n_sims} instancias.")

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(["fallos"], [fallos], color="tab:red" if fallos else "tab:green")
    ax.set_ylabel("número de fallos")
    ax.set_title(f"Estabilidad con listas incompletas ({n_sims} instancias)")
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(RUTA, "fig_p12_verificacion.png"), dpi=150)
    plt.close(fig)
    print("  guardada fig_p12_verificacion.png")


def experimento_propuestas():
    rng = random.Random(7)
    ns = [10, 20, 50, 100, 200, 500]
    prop_incomp, prop_comp = [], []

    print(f"\n{'n':>6} {'incompletas':>12} {'completas':>12} {'n ln n':>10}")
    import math
    for n in ns:
        # Incompletas con densidad 0.5
        total = 0
        for _ in range(30):
            pref_a, pref_b = generar_instancia(n, 0.5, rng)
            _, _, p = gale_shapley_incompleto(pref_a, pref_b)
            total += p
        prop_incomp.append(total / 30)

        # Completas
        total = 0
        for _ in range(30):
            pref_a, pref_b = generar_instancia_completa(n, rng)
            _, _, p = gale_shapley_incompleto(pref_a, pref_b)
            total += p
        prop_comp.append(total / 30)
        print(f"{n:>6} {prop_incomp[-1]:>12.1f} {prop_comp[-1]:>12.1f} {n*math.log(n):>10.1f}")

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(ns, prop_incomp, "o-", label="incompletas (densidad 0.5)", color="tab:blue")
    ax.plot(ns, prop_comp, "s-", label="completas", color="tab:orange")
    ax.plot(ns, [n * math.log(n) for n in ns], "--", label="$n \\ln n$", color="gray")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("$n$"); ax.set_ylabel("propuestas")
    ax.set_title("Propuestas totales: listas completas vs incompletas")
    ax.legend(); ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(RUTA, "fig_p12_propuestas.png"), dpi=150)
    plt.close(fig)
    print("  guardada fig_p12_propuestas.png")


def experimento_solteros():
    rng = random.Random(13)
    n = 100
    densidades = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    frac_solteros = []

    print(f"\n{'densidad':>10} {'% solteros':>12}")
    for d in densidades:
        solteros = 0
        for _ in range(50):
            pref_a, pref_b = generar_instancia(n, d, rng)
            match_a, _, _ = gale_shapley_incompleto(pref_a, pref_b)
            solteros += sum(1 for x in match_a if x == -1)
        frac = 100 * solteros / (50 * n)
        frac_solteros.append(frac)
        print(f"{d:>10.1f} {frac:>11.1f}%")

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(densidades, frac_solteros, "o-", color="tab:purple")
    ax.set_xlabel("densidad (probabilidad de ser aceptables)")
    ax.set_ylabel("% de proponentes solteros")
    ax.set_title(f"Solteros en función de la densidad ($n={n}$)")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(RUTA, "fig_p12_solteros.png"), dpi=150)
    plt.close(fig)
    print("  guardada fig_p12_solteros.png")


def experimento_ejemplo():
    rng = random.Random(2026)
    n = 6
    densidad = 0.4
    pref_a, pref_b = generar_instancia(n, densidad, rng)
    match_a, match_b, propuestas = gale_shapley_incompleto(pref_a, pref_b)

    # Dibujar el grafo bipartito
    fig, ax = plt.subplots(figsize=(8, 5))
    xs_a = [0] * n
    ys_a = list(range(n, 0, -1))
    xs_b = [1] * n
    ys_b = list(range(n, 0, -1))

    for a in range(n):
        ax.scatter(xs_a[a], ys_a[a], s=300, color="tab:blue", zorder=3)
        ax.text(xs_a[a], ys_a[a], f"$a_{a}$", ha="center", va="center",
                color="white", fontsize=10, zorder=4)
    for b in range(n):
        ax.scatter(xs_b[b], ys_b[b], s=300, color="tab:orange", zorder=3)
        ax.text(xs_b[b], ys_b[b], f"$b_{b}$", ha="center", va="center",
                color="white", fontsize=10, zorder=4)

    # Aristas aceptables
    for a in range(n):
        for b in pref_a[a]:
            ax.plot([xs_a[a], xs_b[b]], [ys_a[a], ys_b[b]], color="lightgray",
                    linestyle="--", alpha=0.5, zorder=1)

    # Aristas del emparejamiento
    for a in range(n):
        if match_a[a] != -1:
            b = match_a[a]
            ax.plot([xs_a[a], xs_b[b]], [ys_a[a], ys_b[b]], color="tab:green",
                    linewidth=2, zorder=2)

    ax.set_title(f"Emparejamiento estable con listas incompletas ($n={n}$, "
                 f"{propuestas} propuestas)")
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(os.path.join(RUTA, "fig_p12_ejemplo.png"), dpi=150)
    plt.close(fig)
    print("\n  guardada fig_p12_ejemplo.png")


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Verificación de estabilidad")
    print("=" * 60)
    experimento_verificacion(n_sims=2000)

    print("\n" + "=" * 60)
    print("Número de propuestas vs n")
    print("=" * 60)
    experimento_propuestas()

    print("\n" + "=" * 60)
    print("Fracción de solteros vs densidad")
    print("=" * 60)
    experimento_solteros()

    print("\n" + "=" * 60)
    print("Ejemplo visual")
    print("=" * 60)
    experimento_ejemplo()

    print("\nFiguras generadas: fig_p12_verificacion.png, fig_p12_propuestas.png, "
          "fig_p12_solteros.png, fig_p12_ejemplo.png")