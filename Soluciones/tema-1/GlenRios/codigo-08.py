"""
Problema 8: generalización de Boyer-Moore para elementos con frecuencia > n/3.

Experimentos:
  - Tasa de fallo de la versión sin verificar vs la versión con verificar,
    para varios generadores de entradas (50 000 simulaciones cada uno).
  - Tasa de fallo en función de n para generadores seleccionados.
  - Ejemplo concreto de fallo con las frecuencias dibujadas.

Genera:
  fig_p8_tasas.png    : barras con la tasa de fallo por generador.
  fig_p8_por_n.png    : curvas de fallo en función de n.
  fig_p8_ejemplo.png  : ejemplo de fallo con las frecuencias.
"""
import random
from collections import Counter
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
RUTA = os.path.join("Soluciones", "tema-1", "GlenRios")
os.makedirs(RUTA, exist_ok=True)  # crea la carpeta si no existe


# ----------------------------------------------------------------------
# Algoritmos
# ----------------------------------------------------------------------

def mayoria_n3(A):
    """Versión correcta: dos candidatos + verificación."""
    c1 = c2 = None
    k1 = k2 = 0
    for x in A:
        if c1 is not None and x == c1:
            k1 += 1
        elif c2 is not None and x == c2:
            k2 += 1
        elif k1 == 0:
            c1, k1 = x, 1
        elif k2 == 0:
            c2, k2 = x, 1
        else:
            k1 -= 1
            k2 -= 1
    n = len(A)
    res = []
    for c in (c1, c2):
        if c is not None and A.count(c) > n / 3:
            res.append(c)
    return sorted(res)


def mayoria_n3_sin_verificar(A):
    """Versión incorrecta: devuelve candidatos con contador positivo, sin verificar."""
    c1 = c2 = None
    k1 = k2 = 0
    for x in A:
        if c1 is not None and x == c1:
            k1 += 1
        elif c2 is not None and x == c2:
            k2 += 1
        elif k1 == 0:
            c1, k1 = x, 1
        elif k2 == 0:
            c2, k2 = x, 1
        else:
            k1 -= 1
            k2 -= 1
    res = []
    if c1 is not None and k1 > 0:
        res.append(c1)
    if c2 is not None and k2 > 0:
        res.append(c2)
    return sorted(res)


def oraculo(A):
    """Fuerza bruta: todos los elementos con frecuencia > n/3."""
    n = len(A)
    return sorted(x for x, k in Counter(A).items() if k > n / 3)


# ----------------------------------------------------------------------
# Generadores
# ----------------------------------------------------------------------

def gen_plantada(rng, n):
    """Un elemento > n/3 y el resto pares que cancelan (el generador 'obvio')."""
    m = rng.randint(0, 4)
    k = n // 3 + 1
    A = [m] * k
    while len(A) + 1 < n:
        a, b = rng.sample([x for x in range(5) if x != m], 2)
        A += [a, b]
    if len(A) < n:
        A.append(rng.choice([x for x in range(5) if x != m]))
    rng.shuffle(A)
    return A


def gen_binario(rng, n):
    return [rng.choice([0, 1]) for _ in range(n)]


def gen_tres(rng, n):
    return [rng.choice([0, 1, 2]) for _ in range(n)]


def gen_cinco(rng, n):
    return [rng.choice([0, 1, 2, 3, 4]) for _ in range(n)]


def gen_exacto_n3(rng, n):
    """Tres elementos con frecuencia exactamente n/3 (no > n/3)."""
    n = max(3, (n // 3) * 3)
    A = [0] * (n // 3) + [1] * (n // 3) + [2] * (n // 3)
    rng.shuffle(A)
    return A


def gen_cuatro_iguales(rng, n):
    """Cuatro elementos con la misma frecuencia (ninguno > n/3 para n >= 4)."""
    n = max(4, (n // 4) * 4)
    A = [0] * (n // 4) + [1] * (n // 4) + [2] * (n // 4) + [3] * (n // 4)
    rng.shuffle(A)
    return A


def gen_sin_mayoria(rng, n):
    """Muchos símbolos, frecuencias todas <= n/3."""
    k = max(4, n // 3 + 1)
    return [rng.randint(0, k - 1) for _ in range(n)]


def gen_bloques(rng, n):
    """Cada símbolo aparece en un bloque contiguo (orden correlacionado)."""
    A = []
    i = 0
    while len(A) < n:
        bloque = rng.randint(1, max(1, n // 5))
        A += [i] * bloque
        i += 1
    return A[:n]


GENERADORES = {
    "plantada":    gen_plantada,
    "binario":     gen_binario,
    "3 símbolos":  gen_tres,
    "5 símbolos":  gen_cinco,
    "exacto n/3":  gen_exacto_n3,
    "4 iguales":   gen_cuatro_iguales,
    "sin mayoría": gen_sin_mayoria,
    "bloques":     gen_bloques,
}


# ----------------------------------------------------------------------
# Experimentos
# ----------------------------------------------------------------------

def experimento_tasas(n_sims=50000, n_min=3, n_max=50):
    rng = random.Random(2026)
    nombres = list(GENERADORES.keys())
    tasas_sin, tasas_con = [], []

    print(f"{'generador':>16} {'sims':>8} {'sin verificar':>16} {'con verificar':>16}")
    print("-" * 62)
    for nombre in nombres:
        gen = GENERADORES[nombre]
        fallos_sin = fallos_con = 0
        for _ in range(n_sims):
            n = rng.randint(n_min, n_max)
            A = gen(rng, n)
            esperado = oraculo(A)
            if mayoria_n3_sin_verificar(A) != esperado:
                fallos_sin += 1
            if mayoria_n3(A) != esperado:
                fallos_con += 1
        t_sin = 100 * fallos_sin / n_sims
        t_con = 100 * fallos_con / n_sims
        tasas_sin.append(t_sin)
        tasas_con.append(t_con)
        print(f"{nombre:>16} {n_sims:>8} {t_sin:>15.3f}% {t_con:>15.3f}%")

    x = range(len(nombres))
    ancho = 0.38
    fig, ax = plt.subplots(figsize=(11, 5.5))
    barras_sin = ax.bar([i - ancho / 2 for i in x], tasas_sin, ancho,
                        label="sin verificar (incorrecta)", color="tab:red")
    barras_con = ax.bar([i + ancho / 2 for i in x], tasas_con, ancho,
                        label="con verificar (correcta)", color="tab:green")
    ax.set_xticks(list(x))
    ax.set_xticklabels(nombres, rotation=20, ha="right")
    ax.set_ylabel("% de fallos")
    ax.set_title(f"Tasa de fallo por generador "
                 f"({n_sims:,} simulaciones, $n \\in [{n_min},{n_max}]$)")
    ax.legend()
    ax.grid(True, axis="y", alpha=0.3)
    for b, t in zip(barras_sin, tasas_sin):
        if t > 0:
            ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.4,
                    f"{t:.2f}%", ha="center", va="bottom", fontsize=8,
                    color="tab:red")
    for b, t in zip(barras_con, tasas_con):
        if t > 0:
            ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.4,
                    f"{t:.2f}%", ha="center", va="bottom", fontsize=8,
                    color="tab:green")
    fig.tight_layout()
    fig.savefig(os.path.join(RUTA, "fig_p8_tasas.png"), dpi=150)
    plt.close(fig)
    print("\n  guardada fig_p8_tasas.png")

    return nombres, tasas_sin, tasas_con


def experimento_por_n(generadores_elegidos, n_vals, n_sims=10000):
    rng = random.Random(7)
    resultados = {nombre: [] for nombre in generadores_elegidos}

    print(f"\n{'n':>5}", end="")
    for nombre in generadores_elegidos:
        print(f" {nombre:>14}", end="")
    print()
    for n in n_vals:
        print(f"{n:>5}", end="")
        for nombre in generadores_elegidos:
            gen = GENERADORES[nombre]
            fallos = 0
            for _ in range(n_sims):
                A = gen(rng, n)
                if mayoria_n3_sin_verificar(A) != oraculo(A):
                    fallos += 1
            tasa = 100 * fallos / n_sims
            resultados[nombre].append(tasa)
            print(f" {tasa:>13.2f}%", end="")
        print()

    fig, ax = plt.subplots(figsize=(8, 5))
    marcadores = ["o-", "s-", "^-", "d-", "v-"]
    for i, nombre in enumerate(generadores_elegidos):
        ax.plot(n_vals, resultados[nombre], marcadores[i % len(marcadores)],
                label=nombre)
    ax.set_xlabel("$n$")
    ax.set_ylabel("% de fallos (sin verificar)")
    ax.set_title("Tasa de fallo de la versión sin verificar en función de $n$")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(RUTA, "fig_p8_por_n.png"), dpi=150)
    plt.close(fig)
    print("\n  guardada fig_p8_por_n.png")

    return resultados


def experimento_ejemplo():
    rng = random.Random(0)
    ejemplo = None
    for _ in range(200000):
        A = [rng.choice([0, 1, 2, 3]) for _ in range(rng.randint(6, 20))]
        sv = mayoria_n3_sin_verificar(A)
        or_ = oraculo(A)
        if sv != or_:
            ejemplo = (A, sv, or_)
            break

    fig, ax = plt.subplots(figsize=(10, 4.5))
    if ejemplo is not None:
        A, sv, or_ = ejemplo
        conteo = Counter(A)
        elementos = sorted(conteo.keys())
        frec = [conteo[e] for e in elementos]
        colores = ["tab:red" if e in sv and e not in or_ else "tab:blue"
                   for e in elementos]
        ax.bar([str(e) for e in elementos], frec, color=colores,
               edgecolor="black")
        ax.axhline(len(A) / 3, color="black", linestyle="--",
                   label=f"$n/3 = {len(A)/3:.2f}$")
        ax.set_xlabel("elemento")
        ax.set_ylabel("frecuencia")
        ax.set_title(f"Ejemplo de fallo  |  $A$ = {A}\n"
                     f"sin verificar devuelve {sv}  ·  correcto es {or_}")
        ax.legend()
    else:
        ax.text(0.5, 0.5, "No se encontró ejemplo de fallo",
                ha="center", va="center", transform=ax.transAxes)
        ax.axis("off")
    fig.tight_layout()
    fig.savefig(os.path.join(RUTA, "fig_p8_ejemplo.png"), dpi=150)
    plt.close(fig)
    print("  guardada fig_p8_ejemplo.png")


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 62)
    print("Tasa de fallo por generador")
    print("=" * 62)
    nombres, t_sin, t_con = experimento_tasas(n_sims=50000, n_min=3, n_max=50)

    print("\n" + "=" * 62)
    print("Tasa de fallo en función de n (solo versión sin verificar)")
    print("=" * 62)
    generadores_elegidos = ["plantada", "3 símbolos", "sin mayoría", "4 iguales"]
    n_vals = [3, 5, 8, 12, 20, 30, 50, 80, 120, 200]
    experimento_por_n(generadores_elegidos, n_vals, n_sims=10000)

    print("\n" + "=" * 62)
    print("Ejemplo de fallo")
    print("=" * 62)
    experimento_ejemplo()

    print("\nFiguras generadas: fig_p8_tasas.png, "
          "fig_p8_por_n.png, fig_p8_ejemplo.png")