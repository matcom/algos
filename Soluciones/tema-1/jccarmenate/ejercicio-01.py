"""Ejercicio 1 del Tema 1: una computadora mil veces más rápida.

    python ejercicio-01.py

Imprime todas las tablas que cita ejercicio-01.md, corre las pruebas y regenera
las dos figuras (ejercicio-01-factor.svg y ejercicio-01-theta.svg). Cada número
que aparece en la prosa sale de aquí. Solo necesita matplotlib.
"""

import math

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt

VELOCIDAD = 10**9              # operaciones por segundo
HORA = 3600 * VELOCIDAD        # el presupuesto: una hora
S = 1000                       # cuántas veces más rápida es la computadora nueva


# --------------------------------------------------------------------------
# 1. El mayor n que cabe en un presupuesto
# --------------------------------------------------------------------------

def mayor_n(costo, presupuesto):
    # búsqueda binaria sobre n: duplicar hasta pasarse, después bisecar
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


def mayor_n_oraculo(costo, presupuesto):
    # el oráculo: probar n = 1, 2, 3, ... hasta pasarse. Obvio y lento.
    n = 1
    while costo(n + 1) <= presupuesto:
        n += 1
    return n


def tamano_real(costo, presupuesto):
    """La solución real x >= 1 de costo(x) = presupuesto, por bisección.
    Supone que costo es creciente en [1, oo)."""
    bajo, alto = 1.0, 2.0
    while costo(alto) < presupuesto:
        alto *= 2
    for _ in range(200):
        medio = (bajo + alto) / 2
        if costo(medio) < presupuesto:
            bajo = medio
        else:
            alto = medio
    return (bajo + alto) / 2


def factor_real(costo, n0, s=S):
    """Cuánto crece el tamaño resoluble si hoy se resuelve n0 y el presupuesto se
    multiplica por s: la solución x de costo(x) = s * costo(n0), dividida por n0."""
    return tamano_real(costo, s * costo(n0)) / n0


# --------------------------------------------------------------------------
# 2. El factor de n log n como punto fijo
# --------------------------------------------------------------------------

def phi(k, L, s=S):
    # la ecuación (★) de la sección 4: k = s / (1 + log2 k / log2 n0)
    return s / (1 + math.log2(k) / L)


def factor_nlogn(L, s=S, traza=None):
    """El factor k de un algoritmo c·n·log n, dado L = log2 n0. Se itera phi desde
    k = s. Con s = 1000, la sección 4 demuestra que converge en el escenario de una
    hora, y la prueba (b) comprueba que el resultado satisface (★) para L de 2 a 60.
    Trabajar con L y no con n0 permite n0 = 2^1000 sin desbordar."""
    k = s
    for _ in range(200):
        k_nuevo = phi(k, L, s)
        if traza is not None:
            traza.append(k_nuevo)
        if abs(k_nuevo - k) < 1e-12:
            return k_nuevo
        k = k_nuevo
    return k


def cota_inferior_nlogn(L, s=S):
    # las cotas de la sección 4: s / (1 + log2 s / log2 n0) <= k < s
    return s / (1 + math.log2(s) / L)


cuadratico = lambda n: n * n
nlogn = lambda n: n * math.log2(n)


def fmt(x):
    # 7.8e+13 -> 7,80·10^13, para pegar en la prosa sin retocar
    m, e = f"{x:.2e}".split("e")
    return f"{m.replace('.', ',')}·10^{int(e)}"


def coma(x, d=1):
    return f"{x:.{d}f}".replace(".", ",")


def miles(x):
    # 1643 -> "1 643", con espacio de miles
    return f"{x:,.0f}".replace(",", " ")


# --------------------------------------------------------------------------
# 3. Las tablas que cita la prosa
# --------------------------------------------------------------------------

def seccion(titulo):
    print()
    print(titulo)
    print("-" * len(titulo))


def ejemplo_chico():
    seccion("§2. Ejemplo chico: hoy se resuelve n0 = 1024 en una hora")
    n0 = 1024
    print(f"{'costo':>8} {'ops hoy':>12} {'ops 1000x':>14} {'n nuevo':>10} {'factor':>8}")
    for nombre, f in [("n^2", cuadratico), ("n log n", nlogn)]:
        hoy = f(n0)
        n1 = mayor_n(f, S * hoy)
        print(f"{nombre:>8} {hoy:>12,.0f} {S * hoy:>14,.0f} {n1:>10,} {n1 / n0:>8.1f}")
    n1 = mayor_n(nlogn, S * nlogn(n0))
    print(f"log2 del n nuevo de n log n: {math.log2(n1):.1f}  (el de n0 es 10)")


def escenario_una_hora():
    seccion("§3 y §4. El escenario de referencia: 10^9 op/s, una hora")
    print(f"{'costo':>8} {'hoy':>12} {'1000x':>12} {'factor':>8}")
    for nombre, f in [("n^2", cuadratico), ("n log n", nlogn)]:
        n0, n1 = mayor_n(f, HORA), mayor_n(f, S * HORA)
        print(f"{nombre:>8} {fmt(n0):>12} {fmt(n1):>12} {n1 / n0:>8.2f}")
    print(f"raíz de 1000 = {math.sqrt(S):.4f}")


def punto_fijo():
    seccion("§4. La iteración de punto fijo, en el escenario de una hora")
    n0 = mayor_n(nlogn, HORA)
    L = math.log2(n0)
    traza = []
    k = factor_nlogn(L, traza=traza)
    print(f"n0 = {fmt(n0)},  L = log2 n0 = {L:.2f}")
    print("k:  1000 -> " + " -> ".join(f"{x:.2f}" for x in traza[:5]) + " -> ...")
    print(f"punto fijo: k = {k:.2f}")
    print(f"cota inferior: {cota_inferior_nlogn(L):.1f}")
    print(f"|phi'(k)| = k / (1000 · L · ln 2) = {k / (S * L * math.log(2)):.4f}")
    cota = cota_inferior_nlogn(L)
    print(f"en [cota inferior, 1000]: |phi'| <= 1000 / (cota · L · ln 2) = "
          f"{S / (cota * L * math.log(2)):.4f}")
    n1 = mayor_n(nlogn, S * HORA)
    print(f"comparación con la búsqueda binaria: n1 / n0 = {n1 / n0:.2f}")


def factor_contra_presupuesto():
    seccion("§4. El factor de n log n depende del presupuesto; el de n^2, no")
    presupuestos = [("1 segundo", 1), ("1 minuto", 60), ("1 hora", 3600),
                    ("1 día", 86400), ("1 año", 86400 * 365),
                    ("1 siglo", 86400 * 365 * 100)]
    print(f"{'presupuesto':>12} {'n0 de n log n':>14} {'log2 n0':>8} "
          f"{'cota inf.':>10} {'factor n log n':>15} {'factor n^2':>11}")
    for nombre, seg in presupuestos:
        T = seg * VELOCIDAD
        n0 = tamano_real(nlogn, T)
        L = math.log2(n0)
        k = factor_nlogn(L)
        k2 = factor_real(cuadratico, tamano_real(cuadratico, T))
        print(f"{nombre:>12} {fmt(n0):>14} {L:>8.1f} {cota_inferior_nlogn(L):>10.1f} "
              f"{k:>15.1f} {k2:>11.2f}")


def umbrales():
    seccion("§4. Qué tan grande tiene que ser n0 para acercarse a 1000")
    for objetivo in [900, 950, 990]:
        # k >= objetivo  <=>  log2 k / L <= S/objetivo - 1, con k = objetivo
        L = math.log2(objetivo) / (S / objetivo - 1)
        print(f"factor >= {objetivo}: hace falta log2 n0 >= {L:.1f}, "
              f"o sea n0 con unas {L * math.log10(2):.0f} cifras decimales")


def oscilante(n):
    # Θ(n²) con c1 = 1 y c2 = 2, pero f(n)/n² no tiene límite. Es creciente:
    # (ln f)' = 2/n + h'/h >= 2/n - 0,5/n > 0.
    return n * n * (1.5 + 0.5 * math.sin(math.log(n)))


def lo_que_theta_no_dice():
    seccion("§5. Cuatro funciones Θ(n²) y sus factores, en el escenario de una hora")
    casos = [
        ("n^2", cuadratico),
        ("7 n^2", lambda n: 7 * n * n),
        ("3n^2 + 10 n log n + 7", lambda n: 3 * n * n + 10 * n * math.log2(n) + 7),
        ("n^2 + 10^7 n", lambda n: n * n + 10**7 * n),
    ]
    print(f"{'costo':>22} {'hoy':>12} {'1000x':>12} {'factor':>8}")
    for nombre, f in casos:
        n0, n1 = mayor_n(f, HORA), mayor_n(f, S * HORA)
        print(f"{nombre:>22} {fmt(n0):>12} {fmt(n1):>12} {n1 / n0:>8.2f}")
    n0 = mayor_n(casos[2][1], HORA)
    print(f"con 3n^2 + 10 n log n + 7 y n0 = {fmt(n0)}: "
          f"3 n0^2 / (10 n0 log2 n0) = {miles(3 * n0 / (10 * math.log2(n0)))}")
    n0 = mayor_n(casos[3][1], HORA)
    print(f"con n^2 + 10^7 n y n0 = {fmt(n0)}: 10^7 n0 / n0^2 = {10**7 / n0:.1f}")

    # la función oscilante: barrer n0 sobre doce órdenes de magnitud
    factores = [factor_real(oscilante, 10 ** (2 + i * 0.006)) for i in range(2001)]
    print(f"n^2 (1,5 + 0,5 sen ln n), n0 entre 10^2 y 10^14: factor entre "
          f"{min(factores):.1f} y {max(factores):.1f}")
    print(f"la cota de la sección 5 con c1 = 1, c2 = 2: entre raíz(500) = "
          f"{math.sqrt(500):.1f} y raíz(2000) = {math.sqrt(2000):.1f}")


def cambiar_de_algoritmo():
    seccion("§6. Cambiar de máquina contra cambiar de algoritmo")
    n2_rapida = mayor_n(cuadratico, S * HORA)
    nlogn_lenta = mayor_n(nlogn, HORA)
    print(f"n^2 en la máquina 1000 veces más rápida: {fmt(n2_rapida)}")
    print(f"n log n en la máquina de siempre:        {fmt(nlogn_lenta)}")
    print(f"cociente: {miles(nlogn_lenta / n2_rapida)}")
    print()
    print(f"{'costo':>8} {'qué compra la máquina 1000 veces más rápida':>45}")
    for nombre, f in [("n", lambda n: n), ("n log n", nlogn), ("n^2", cuadratico),
                      ("n^3", lambda n: n ** 3)]:
        n0, n1 = mayor_n(f, HORA), mayor_n(f, S * HORA)
        print(f"{nombre:>8} {'multiplica n por ' + coma(n1 / n0):>45}")
    for nombre, f in [("2^n", lambda n: 2 ** n), ("2^(n/2)", lambda n: 2 ** (n / 2))]:
        n0, n1 = mayor_n(f, HORA), mayor_n(f, S * HORA)
        print(f"{nombre:>8} {f'le suma {n1 - n0} a n':>45}")
    print(f"log2 1000 = {math.log2(S):.2f}")


# --------------------------------------------------------------------------
# 4. Pruebas
# --------------------------------------------------------------------------

def pruebas():
    seccion("Pruebas")
    comprobaciones = 0

    # (a) mayor_n contra el oráculo, en todos los presupuestos chicos
    costos = {"n": lambda n: n, "n log n": nlogn, "n^2": cuadratico,
              "n^3": lambda n: n ** 3, "2^n": lambda n: 2 ** n,
              "oscilante": oscilante}
    for nombre, f in costos.items():
        for presupuesto in range(2, 2001):
            if f(2) > presupuesto:
                continue
            assert mayor_n(f, presupuesto) == mayor_n_oraculo(f, presupuesto), \
                (nombre, presupuesto)
            comprobaciones += 1

    # (b) el punto fijo resuelve la ecuación y coincide con la bisección directa
    for e in range(2, 61):
        n0 = 2.0 ** e
        k = factor_nlogn(e)
        assert abs(k - phi(k, e)) < 1e-9
        directo = factor_real(nlogn, n0)
        assert abs(k - directo) / directo < 1e-9, (e, k, directo)
        comprobaciones += 2

    # (c) las cotas de la sección 4: cota inferior <= k < 1000, para L de 1 a 3000
    for L in range(1, 3001):
        k = factor_nlogn(L)
        assert cota_inferior_nlogn(L) <= k < S, L
        comprobaciones += 1

    # (d) n^2: el factor entero tiende a raíz de 1000 (el límite de la sección 3)
    for e in range(12, 31):
        T = 10**e
        k = mayor_n(cuadratico, S * T) / mayor_n(cuadratico, T)
        assert abs(k - math.sqrt(S)) < 10 ** (-(e // 2 - 2)), (e, k)
        comprobaciones += 1

    # (e) la función oscilante es creciente (la sección 5 lo necesita)
    for i in range(1, 200_000):
        assert oscilante(i + 1) > oscilante(i)
    comprobaciones += 1

    print(f"{miles(comprobaciones)} comprobaciones, 0 fallos")


# --------------------------------------------------------------------------
# 5. Figuras
# --------------------------------------------------------------------------

# Paleta de colores de las figuras.
TINTA, APAGADO, REGLA = "#1a1a1a", "#6b7280", "#d8dce3"
ACENTO, OSCURO, CALIDO, ALARMA = "#0891b2", "#0e7490", "#b45309", "#be123c"


def _estilo():
    plt.rcParams.update({
        "font.size": 9, "axes.edgecolor": APAGADO, "axes.labelcolor": TINTA,
        "xtick.color": APAGADO, "ytick.color": APAGADO, "axes.grid": True,
        "grid.color": REGLA, "grid.linewidth": 0.6, "axes.spines.top": False,
        "axes.spines.right": False, "figure.facecolor": "white",
        "svg.hashsalt": "ejercicio-01",           # SVG reproducible byte a byte
    })


def _guardar(fig, nombre):
    fig.tight_layout()
    fig.savefig(nombre, metadata={"Date": None})
    plt.close(fig)


def figura_factor():
    Ls = [2 ** (i / 40) for i in range(int(40 * math.log2(1100)) + 1) if 2 ** (i / 40) >= 4]
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    ax.axhline(S, color=APAGADO, ls=":", lw=1)
    ax.text(4.3, S + 18, "1000", color=APAGADO)
    ax.plot(Ls, [cota_inferior_nlogn(L) for L in Ls], color=ACENTO, ls="--", lw=1,
            label="cota inferior: 1000 / (1 + log₂1000 / log₂n₀)")
    ax.plot(Ls, [factor_nlogn(L) for L in Ls], color=OSCURO, lw=2,
            label="factor de n log n")
    ax.plot(Ls, [math.sqrt(S)] * len(Ls), color=CALIDO, lw=2,
            label="factor de n²: √1000 ≈ 31,6")
    marcas = [(10, "n₀ = 1024\n(sección 2)"),
              (math.log2(mayor_n(nlogn, HORA)), "una hora\na 10⁹ op/s")]
    for L, texto in marcas:
        k = factor_nlogn(L)
        ax.plot([L], [k], "o", color=ALARMA, ms=4, zorder=5)
        ax.annotate(f"{texto}\nk ≈ {k:.0f}", (L, k), xytext=(8, -34),
                    textcoords="offset points", color=ALARMA, fontsize=8)
    ax.set_xscale("log", base=2)
    ax.set_xticks([4, 16, 64, 256, 1024])
    ax.set_xticklabels(["2⁴", "2¹⁶", "2⁶⁴", "2²⁵⁶", "2¹⁰²⁴"])
    ax.set_xlabel("n₀, el tamaño que se resuelve hoy (eje en log log)")
    ax.set_ylabel("factor de crecimiento con 1000×")
    ax.set_ylim(0, 1080)
    ax.legend(loc="lower right", fontsize=7.5, frameon=False, bbox_to_anchor=(1, 0.08))
    _guardar(fig, "ejercicio-01-factor.svg")


def figura_theta():
    n0s = [10 ** (2 + i * 0.01) for i in range(1201)]
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    series = [
        ("n²", cuadratico, CALIDO, "-"),
        ("n² + 10⁷ n", lambda n: n * n + 10**7 * n, OSCURO, "-"),
        ("n² (1,5 + 0,5 sen ln n)", oscilante, ALARMA, "-"),
    ]
    for nombre, f, color, ls in series:
        ax.plot(n0s, [factor_real(f, n0) for n0 in n0s], color=color, ls=ls, lw=1.6,
                label=nombre)
    fondo = {"facecolor": "white", "edgecolor": "none", "pad": 1}
    for v, txt in [(math.sqrt(500), "√500"), (math.sqrt(2000), "√2000")]:
        ax.axhline(v, color=ALARMA, ls="--", lw=0.8, alpha=0.6)
        ax.text(4e14, v, txt, color=ALARMA, va="center", fontsize=8, bbox=fondo)
    ax.axhline(S, color=APAGADO, ls=":", lw=1)
    ax.text(4e14, S, "1000", color=APAGADO, va="center", fontsize=8, bbox=fondo)
    ax.set_xlim(60, 1e16)
    n0_hora = mayor_n(series[1][1], HORA)
    ax.axvline(n0_hora, color=APAGADO, lw=0.8)
    ax.text(n0_hora * 1.3, 400, "una hora,\npara n² + 10⁷ n", color=APAGADO, fontsize=8)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_yticks([20, 31.6, 50, 100, 200, 500, 1000])
    ax.set_yticklabels(["20", "31,6", "50", "100", "200", "500", "1000"])
    ax.set_xlabel("n₀, el tamaño que se resuelve hoy")
    ax.set_ylabel("factor de crecimiento con 1000×")
    ax.legend(loc="upper right", fontsize=7.5, frameon=False, bbox_to_anchor=(0.97, 0.9))
    _guardar(fig, "ejercicio-01-theta.svg")


if __name__ == "__main__":
    ejemplo_chico()
    escenario_una_hora()
    punto_fijo()
    factor_contra_presupuesto()
    umbrales()
    lo_que_theta_no_dice()
    cambiar_de_algoritmo()
    pruebas()
    _estilo()
    figura_factor()
    figura_theta()
    print("\nfiguras: ejercicio-01-factor.svg, ejercicio-01-theta.svg")
