"""Ejercicio 1 del Tema 1: una computadora mil veces más rápida.

¿Cuánto crece el tamaño de entrada que se resuelve en una hora cuando la
computadora es M = 1000 veces más rápida, con un costo Θ(n²) y con uno
Θ(n log n)?

Uso:
    python ejercicio_01.py             imprime todas las tablas del informe
    python ejercicio_01.py --figuras   además regenera las figuras en ../figuras/

Las pruebas están en test_ejercicio_01.py.
"""

import itertools
import math
import sys
from pathlib import Path

HORA = 3600 * 10**9  # operaciones en una hora a 10^9 op/s (conferencia 1, §7)
M = 1000             # cuántas veces más rápida es la computadora nueva


# ---------------------------------------------------------------------------
# 1. Búsqueda exacta del mayor n que cabe en un presupuesto
# ---------------------------------------------------------------------------

def mayor_n(costo, presupuesto):
    """El mayor n con costo(n) <= presupuesto, para un costo no decreciente.

    Es la función de la conferencia 1, §7: duplica hasta pasarse y después hace
    búsqueda binaria manteniendo costo(bajo) <= presupuesto < costo(alto).
    """
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


def factor_medido(costo, presupuesto, m=M):
    """n'/n: cuánto crece el mayor n resoluble al multiplicar el presupuesto por m."""
    return mayor_n(costo, m * presupuesto) / mayor_n(costo, presupuesto)


# ---------------------------------------------------------------------------
# 2. Fórmulas del informe
# ---------------------------------------------------------------------------

def factor_potencia(a, m=M):
    """Costo c·n^a: el factor es m^(1/a), sin importar c ni el presupuesto."""
    return m ** (1 / a)


def iterados_nlogn(n, m=M, pasos=8):
    """Iterados de k <- m·L / (L + log2 k), con L = log2 n, empezando en k = m.

    El punto fijo es el factor de un costo c·n·log n cuando hoy se resuelve
    tamaño n. El lado derecho decrece en k, así que los iterados alternan
    alrededor del factor: los de índice impar quedan debajo y los pares encima.
    """
    L = math.log2(n)
    k = float(m)
    iterados = [k]
    for _ in range(pasos):
        k = m * L / (L + math.log2(k))
        iterados.append(k)
    return iterados


def factor_nlogn(n, m=M):
    """Solución de k·(L + log2 k) = m·L en [1, m], por bisección (L = log2 n)."""
    L = math.log2(n)
    bajo, alto = 1.0, float(m)
    for _ in range(200):
        medio = (bajo + alto) / 2
        if medio * (L + math.log2(medio)) < m * L:
            bajo = medio
        else:
            alto = medio
    return (bajo + alto) / 2


def cota_inferior_nlogn(n, m=M):
    """m·L / (L + log2 m): el primer iterado, siempre por debajo del factor."""
    L = math.log2(n)
    return m * L / (L + math.log2(m))


def contraccion_nlogn(n, m=M):
    """Cota q de |g'| en [cota inferior, m] para g(k) = m·L / (L + log2 k).

    Cada iterado está a lo sumo q veces la distancia del anterior al factor.
    """
    L = math.log2(n)
    piso = cota_inferior_nlogn(n, m)
    return (L + math.log2(m)) / ((L + math.log2(piso)) ** 2 * math.log(2))


def factor_lambert(presupuesto, m=M):
    """Forma cerrada con la W de Lambert para el costo exacto n·log2 n.

    n·ln n = x  <=>  n = x / W(x), con x = presupuesto·ln 2.
    """
    from scipy.special import lambertw

    x = presupuesto * math.log(2)
    return m * lambertw(x).real / lambertw(m * x).real


def tamano_lambert(presupuesto):
    """El n real con n·log2 n = presupuesto."""
    from scipy.special import lambertw

    x = presupuesto * math.log(2)
    return x / lambertw(x).real


# ---------------------------------------------------------------------------
# 3. Algoritmos reales y su costo exacto de peor caso (en comparaciones)
# ---------------------------------------------------------------------------

def insercion(A):
    """Ordena por inserción. Devuelve (ordenado, comparaciones)."""
    A = list(A)
    comparaciones = 0
    for i in range(1, len(A)):
        x = A[i]
        j = i - 1
        while j >= 0:
            comparaciones += 1
            if A[j] <= x:
                break
            A[j + 1] = A[j]
            j -= 1
        A[j + 1] = x
    return A, comparaciones


def mezcla(A):
    """Merge sort de arriba hacia abajo. Devuelve (ordenado, comparaciones)."""
    if len(A) <= 1:
        return list(A), 0
    medio = (len(A) + 1) // 2
    izq, ci = mezcla(A[:medio])
    der, cd = mezcla(A[medio:])
    res = []
    i = j = 0
    comparaciones = ci + cd
    while i < len(izq) and j < len(der):
        comparaciones += 1
        if izq[i] <= der[j]:
            res.append(izq[i])
            i += 1
        else:
            res.append(der[j])
            j += 1
    res.extend(izq[i:])
    res.extend(der[j:])
    return res, comparaciones


def peor_caso(algoritmo, n):
    """Máximo de comparaciones sobre las n! permutaciones de 0..n-1."""
    return max(algoritmo(p)[1] for p in itertools.permutations(range(n)))


def costo_insercion(n):
    """Peor caso exacto de insercion: el arreglo invertido, n(n-1)/2."""
    return n * (n - 1) // 2


def costo_mezcla(n):
    """Peor caso exacto de mezcla: n·⌈lg n⌉ - 2^⌈lg n⌉ + 1, en enteros."""
    if n <= 1:
        return 0
    t = (n - 1).bit_length()  # ⌈log2 n⌉ sin errores de punto flotante
    return n * t - 2**t + 1


# ---------------------------------------------------------------------------
# 4. Θ(n²) no basta para fijar el factor
# ---------------------------------------------------------------------------

def costo_patologico(n):
    """n² <= T(n) <= 2n², creciente, pero T(n)/n² oscila sin límite."""
    return n * n * (3 + math.sin(math.log(n))) / 2


def costo_orden_menor(n):
    """Θ(n²) con un término lineal que domina mientras n < 10^6."""
    return n * n + 10**6 * n


# ---------------------------------------------------------------------------
# 5. Tablas del informe
# ---------------------------------------------------------------------------

def nlogn(n):
    return n * math.log2(n)


COSTOS = {
    "n": lambda n: n,
    "n log n": nlogn,
    "n^2": lambda n: n**2,
    "n^3": lambda n: n**3,
    "2^n": lambda n: 2**n,
}


def tabla_conferencia():
    print("Tabla 1. La tabla de la conferencia 1, §7, con la columna del factor")
    print(f"{'costo':>8} {'n hoy':>18} {'n con 1000x':>20} {'factor':>10}")
    for nombre, costo in COSTOS.items():
        hoy = mayor_n(costo, HORA)
        nuevo = mayor_n(costo, M * HORA)
        print(f"{nombre:>8} {hoy:>18,} {nuevo:>20,} {nuevo / hoy:>10.4f}")
    print()


def tabla_iterados():
    n = mayor_n(nlogn, HORA)
    k = factor_nlogn(n)
    print(f"Tabla 2. Iterados de k <- M·L/(L + log2 k), n = {n:,}, L = {math.log2(n):.4f}")
    print(f"{'t':>3} {'k_t':>14} {'k_t - k':>14}  lado")
    for t, x in enumerate(iterados_nlogn(n, pasos=6)):
        lado = "encima" if x > k else "debajo"
        print(f"{t:>3} {x:>14.8f} {x - k:>14.2e}  {lado}")
    print(f"factor medido con mayor_n: {factor_medido(nlogn, HORA):.8f}")
    try:
        print(f"factor con la W de Lambert: {factor_lambert(HORA):.8f}")
    except ImportError:
        print("factor con la W de Lambert: (hace falta scipy)")
    print()


def tabla_por_tamano():
    print("Tabla 3. Factor de n log n según el tamaño n que se resuelve hoy")
    print(f"{'n hoy':>8} {'L':>8} {'cota inf':>10} {'factor':>10} {'1000 - k':>10}")
    for e in [3, 6, 9, 12, 18, 30, 100]:
        n = 10.0**e
        k = factor_nlogn(n)
        print(f"{'1e' + str(e):>8} {math.log2(n):>8.2f} {cota_inferior_nlogn(n):>10.2f}"
              f" {k:>10.2f} {M - k:>10.2f}")
    print()


def tabla_algoritmos():
    print("Tabla 4. Algoritmos reales, una comparación = una operación")
    print(f"{'algoritmo':>10} {'n hoy':>18} {'n con 1000x':>20} {'factor':>10}")
    for nombre, costo in [("insercion", costo_insercion), ("mezcla", costo_mezcla)]:
        hoy = mayor_n(costo, HORA)
        nuevo = mayor_n(costo, M * HORA)
        print(f"{nombre:>10} {hoy:>18,} {nuevo:>20,} {nuevo / hoy:>10.4f}")
    print()


def tabla_theta():
    print("Tabla 5. Dos costos Θ(n²) cuyo factor no es √1000")
    print(f"{'presupuesto':>12} {'n²+10^6 n':>12} {'patologico':>12}")
    for e in [8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]:
        B = 10**e
        print(f"{'1e' + str(e):>12} {factor_medido(costo_orden_menor, B):>12.4f}"
              f" {factor_medido(costo_patologico, B):>12.4f}")
    factores = [factor_medido(costo_patologico, 10 ** (e / 8)) for e in range(64, 241)]
    print(f"patológico, 1e8..1e30: mínimo {min(factores):.4f}, máximo {max(factores):.4f}")
    print(f"cotas de la Proposición 3: √500 = {math.sqrt(500):.4f}, √2000 = {math.sqrt(2000):.4f}")
    print()


# ---------------------------------------------------------------------------
# 6. Figuras
# ---------------------------------------------------------------------------

# Paleta categórica validada (slots 1-4) y tinta neutra.
AZUL, NARANJA, AQUA, AMARILLO = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
TINTA, TINTA_2, TENUE, REJILLA, SUPERFICIE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"


def _estilo(plt):
    plt.rcParams.update({
        "font.family": ["Segoe UI", "DejaVu Sans"],
        "font.size": 10,
        "axes.edgecolor": "#c3c2b7",
        "axes.labelcolor": TINTA_2,
        "axes.titlecolor": TINTA,
        "axes.titlesize": 12,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.facecolor": SUPERFICIE,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": REJILLA,
        "grid.linewidth": 0.6,
        "xtick.color": TENUE,
        "ytick.color": TENUE,
        "xtick.labelcolor": TINTA_2,
        "ytick.labelcolor": TINTA_2,
        "figure.facecolor": SUPERFICIE,
        "legend.frameon": False,
        "legend.labelcolor": TINTA_2,
        "lines.linewidth": 2,
        "savefig.dpi": 150,
        "savefig.bbox": "tight",
    })


def figura_factor_vs_n(plt, destino):
    exponentes = [e / 10 for e in range(10, 401)]
    ns = [10**e for e in exponentes]
    fig, ax = plt.subplots(figsize=(8, 4.6))
    ax.plot(ns, [factor_nlogn(n) for n in ns], color=AZUL, label="n log n (factor exacto)")
    ax.plot(ns, [cota_inferior_nlogn(n) for n in ns], color=AZUL, linestyle=(0, (4, 3)),
            linewidth=1.4, label="n log n (cota inferior M·L/(L+log₂M))")
    ax.plot(ns, [math.sqrt(M)] * len(ns), color=NARANJA, label="n² (√1000, constante)")
    ax.axhline(M, color=TENUE, linewidth=1, linestyle=(0, (2, 2)))
    ax.text(1.4e1, M * 1.06, "M = 1000: lo que gana un algoritmo lineal", color=TINTA_2, fontsize=9)

    n_ref = mayor_n(nlogn, HORA)
    k_ref = factor_medido(nlogn, HORA)
    ax.plot([n_ref], [k_ref], "o", color=AZUL, markersize=8, markeredgecolor=SUPERFICIE,
            markeredgewidth=2)
    ax.annotate(f"máquina de la C1: n ≈ 9,86·10¹⁰\nfactor ≈ {k_ref:.1f}".replace(".", ","),
                (n_ref, k_ref), xytext=(n_ref * 3e3, 330), color=TINTA, fontsize=9,
                arrowprops=dict(arrowstyle="-", color=TENUE, linewidth=1))
    n2_ref = mayor_n(COSTOS["n^2"], HORA)
    ax.plot([n2_ref], [math.sqrt(M)], "o", color=NARANJA, markersize=8,
            markeredgecolor=SUPERFICIE, markeredgewidth=2)
    ax.annotate("máquina de la C1: n ≈ 1,9·10⁶\nfactor ≈ 31,6", (n2_ref, math.sqrt(M)),
                xytext=(n2_ref * 1e4, 60), color=TINTA, fontsize=9,
                arrowprops=dict(arrowstyle="-", color=TENUE, linewidth=1))

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_ylim(15, 1500)
    ax.set_xlabel("tamaño n que se resuelve hoy en una hora")
    ax.set_ylabel("factor n'/n con una máquina 1000× más rápida")
    ax.set_title("El factor de n log n depende de n y tiende a 1000; el de n² no depende de nada")
    ax.legend(loc="center right", bbox_to_anchor=(1.0, 0.33))
    fig.savefig(destino / "ejercicio-01-factor-vs-n.png")
    plt.close(fig)


def figura_factor_vs_m(plt, destino):
    ms = [10 ** (e / 20) for e in range(0, 121)]
    n_ref = mayor_n(nlogn, HORA)
    n_exp = math.log2(HORA)  # tamaño real con 2^n = presupuesto
    series = [
        ("n", AZUL, [m for m in ms]),
        ("n log n", NARANJA, [factor_nlogn(n_ref, m) if m > 1 else 1.0 for m in ms]),
        ("n²", AQUA, [factor_potencia(2, m) for m in ms]),
        ("n³", AMARILLO, [factor_potencia(3, m) for m in ms]),
        ("2ⁿ", TINTA_2, [(n_exp + math.log2(m)) / n_exp for m in ms]),
    ]
    fig, ax = plt.subplots(figsize=(8, 4.6))
    for nombre, color, ys in series:
        ax.plot(ms, ys, color=color, label=nombre)
        ax.text(ms[-1] * 1.15, ys[-1], nombre, color=TINTA, fontsize=10, va="center")
    ax.axvline(M, color=TENUE, linewidth=1, linestyle=(0, (2, 2)))
    ax.text(M * 1.15, 1.25e5, "M = 1000", color=TINTA_2, fontsize=9)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1, 1e6 * 8)
    ax.set_xlabel("cuántas veces más rápida es la máquina (M)")
    ax.set_ylabel("factor n'/n del tamaño resoluble")
    ax.set_title("Lo que compra el hardware: M, casi M, √M, ∛M y casi nada")
    ax.legend(loc="upper left")
    fig.savefig(destino / "ejercicio-01-factor-vs-M.png")
    plt.close(fig)


def figura_theta(plt, destino):
    # Desde 10^8: con presupuestos menores n² + 10^6·n deja resolver n < 100 y
    # el redondeo a enteros domina el factor.
    exponentes = [e / 16 for e in range(8 * 16, 32 * 16 + 1)]
    presupuestos = [10**e for e in exponentes]
    fig, ax = plt.subplots(figsize=(8, 4.6))
    ax.axhspan(math.sqrt(M / 2), math.sqrt(2 * M), color=REJILLA, alpha=0.6, linewidth=0)
    ax.text(presupuestos[0] * 1.5, math.sqrt(2 * M) * 1.05,
            "banda de la Proposición 3: [√500, √2000]", color=TINTA_2, fontsize=9)
    ax.plot(presupuestos, [factor_medido(costo_patologico, B) for B in presupuestos],
            color=AZUL, label="T(n) = n²(3 + sen ln n)/2, entre n² y 2n²")
    ax.plot(presupuestos, [factor_medido(costo_orden_menor, B) for B in presupuestos],
            color=NARANJA, label="T(n) = n² + 10⁶·n")
    ax.axhline(math.sqrt(M), color=TINTA_2, linewidth=1, linestyle=(0, (4, 3)),
               label="√1000 ≈ 31,6 (costo exactamente c·n²)")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_ylim(15, 1500)
    ax.set_xlabel("presupuesto de operaciones de la máquina vieja")
    ax.set_ylabel("factor n'/n con 1000× más presupuesto")
    ax.set_title("Dos costos Θ(n²) cuyo factor no es √1000")
    ax.legend(loc="upper right")
    fig.savefig(destino / "ejercicio-01-theta-no-basta.png")
    plt.close(fig)


def figuras():
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    _estilo(plt)
    destino = Path(__file__).resolve().parent.parent / "figuras"
    destino.mkdir(exist_ok=True)
    figura_factor_vs_n(plt, destino)
    figura_factor_vs_m(plt, destino)
    figura_theta(plt, destino)
    print(f"figuras escritas en {destino}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # la consola de Windows no es UTF-8
    tabla_conferencia()
    tabla_iterados()
    tabla_por_tamano()
    tabla_algoritmos()
    tabla_theta()
    if "--figuras" in sys.argv:
        figuras()
