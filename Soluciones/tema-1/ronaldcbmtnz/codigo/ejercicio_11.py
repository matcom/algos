"""Ejercicio 11 del Tema 1: la mochila entera en O(nW) no es polinomial.

Mide el costo de la programación dinámica de la mochila en función del tamaño
de la entrada en bits y lo compara con la primalidad por división.

Uso:
    python ejercicio_11.py             imprime todas las tablas del informe
    python ejercicio_11.py --figuras   además mide tiempos y regenera las figuras

Las pruebas están en test_ejercicio_11.py.
"""

import itertools
import math
import sys
import time
from pathlib import Path

POR_SEGUNDO = 10**9  # operaciones por segundo, como en la conferencia 1


# ---------------------------------------------------------------------------
# 1. La mochila: programación dinámica, fuerza bruta y tamaño de la entrada
# ---------------------------------------------------------------------------

def mochila(pesos, valores, W):
    """Programación dinámica clásica sobre la capacidad.

    Devuelve (mejor valor, índices elegidos, celdas calculadas). La tabla tiene
    n+1 filas y W+1 columnas; la fila 0 es la inicialización y cada una de las
    otras n·(W+1) celdas se calcula con la recurrencia.
    """
    n = len(pesos)
    tabla = [[0] * (W + 1)]
    celdas = 0
    for i in range(1, n + 1):
        w, v = pesos[i - 1], valores[i - 1]
        previa = tabla[i - 1]
        fila = [0] * (W + 1)
        for c in range(W + 1):
            celdas += 1
            fila[c] = previa[c]
            if w <= c and previa[c - w] + v > fila[c]:
                fila[c] = previa[c - w] + v
        tabla.append(fila)
    # Reconstrucción: el objeto i está en la solución si cambió el valor.
    elegidos = []
    c = W
    for i in range(n, 0, -1):
        if tabla[i][c] != tabla[i - 1][c]:
            elegidos.append(i - 1)
            c -= pesos[i - 1]
    return tabla[n][W], sorted(elegidos), celdas


def mochila_fuerza_bruta(pesos, valores, W):
    """Máximo valor probando los 2^n subconjuntos."""
    mejor = 0
    for eleccion in itertools.product([0, 1], repeat=len(pesos)):
        peso = sum(p for p, x in zip(pesos, eleccion) if x)
        if peso <= W:
            mejor = max(mejor, sum(v for v, x in zip(valores, eleccion) if x))
    return mejor


def mochila_rapida(pesos, valores, W, dtype="int64"):
    """La misma programación dinámica con una sola fila en numpy, para medir tiempos."""
    import numpy as np

    fila = np.zeros(W + 1, dtype=dtype)
    for w, v in zip(pesos, valores):
        if w <= W:
            # El lado derecho se evalúa entero antes de escribir: usa la fila vieja.
            np.maximum(fila[w:], fila[: W + 1 - w] + v, out=fila[w:])
    return int(fila[W])


def bits(x):
    """Bits de x en binario (al menos 1, para poder escribir el 0)."""
    return max(1, x.bit_length())


def tamano_entrada(pesos, valores, W):
    """Tamaño de la entrada en bits: n, cada peso, cada valor y la capacidad."""
    return bits(len(pesos)) + sum(bits(p) + bits(v) for p, v in zip(pesos, valores)) + bits(W)


def tamano_unario(pesos, valores, W):
    """Tamaño si los números se escribieran en unario (el número x ocupa x símbolos)."""
    return len(pesos) + sum(pesos) + sum(valores) + W


def celdas(n, W):
    """Celdas que calcula la programación dinámica: exactamente n·(W+1)."""
    return n * (W + 1)


# Familias de instancias -----------------------------------------------------

def familia_capacidad(b):
    """Un objeto de peso y valor 1, capacidad 2^b - 1: todos los bits están en W."""
    return [1], [1], 2**b - 1


def familia_dos_objetos(b):
    """Dos objetos de b bits que no caben juntos: sigue cara aunque se recorte W."""
    return [2 ** (b - 1), 2 ** (b - 1) + 1], [1, 1], 2**b


def familia_numeros(n, b):
    """n objetos con pesos y valores de b bits, capacidad la mitad del peso total."""
    pesos = [2 ** (b - 1) + (i * 2654435761) % 2 ** (b - 1) for i in range(n)]
    valores = [2 ** (b - 1) + (i * 40503) % 2 ** (b - 1) for i in range(n)]
    return pesos, valores, sum(pesos) // 2


# ---------------------------------------------------------------------------
# 2. Primalidad por división (conferencia 1, §1)
# ---------------------------------------------------------------------------

def es_primo(n):
    """El algoritmo de la conferencia 1. Devuelve (es primo, divisiones)."""
    divisiones = 0
    d = 2
    while d * d <= n:
        divisiones += 1
        if n % d == 0:
            return False, divisiones
        d += 1
    return n >= 2, divisiones


def es_primo_miller_rabin(n):
    """Miller-Rabin determinista para n < 3.3·10^24 (bases: los 13 primeros primos).

    Con los 13 primeros primos como bases no hay pseudoprimos fuertes por debajo
    de 3 317 044 064 679 887 385 961 981 (Sorenson y Webster, 2015); 2^81 está debajo.
    """
    if n < 2:
        return False
    bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
    for p in bases:
        if n % p == 0:
            return n == p
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in bases:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def mayor_primo(b):
    """El mayor primo de b bits (b <= 81, donde Miller-Rabin es determinista)."""
    assert 2 <= b <= 81
    p = 2**b - 1
    while not es_primo_miller_rabin(p):
        p -= 1
    return p


def divisiones_peor_caso(b):
    """Divisiones de es_primo con el mayor primo de b bits: ⌊√p⌋ - 1."""
    return math.isqrt(mayor_primo(b)) - 1


# ---------------------------------------------------------------------------
# 3. Tablas del informe
# ---------------------------------------------------------------------------

def _duracion(segundos):
    if segundos < 60:
        return f"{segundos:.3g} s"
    if segundos < 3600 * 24:
        return f"{segundos / 60:.3g} min"
    return f"{segundos / (3600 * 24 * 365):.3g} años"


def _bytes(b):
    for unidad in ["B", "KB", "MB", "GB", "TB", "PB", "EB"]:
        if b < 1000:
            return f"{b:.3g} {unidad}"
        b /= 1000
    return f"{b:.3g} ZB"


def tabla_como_la_conferencia():
    print("Tabla 1. Mochila con 100 objetos y capacidad de b bits, a 10^9 celdas por segundo")
    print(f"{'bits de W':>10} {'celdas':>10} {'tiempo':>14} {'una fila':>10} {'tabla':>10}"
          f" {'primalidad':>12}")
    for b in [16, 32, 48, 64, 128]:
        W = 2**b - 1
        c = celdas(100, W)
        print(f"{b:>10} {c:>10.3g} {_duracion(c / POR_SEGUNDO):>14} {_bytes(8 * (W + 1)):>10}"
              f" {_bytes(8 * 101 * (W + 1)):>10} {_duracion(2 ** (b // 2) / POR_SEGUNDO):>12}")
    print()


def tabla_familias():
    print("Tabla 2. Tamaño en bits contra celdas en las tres familias")
    print(f"{'familia':>16} {'b':>4} {'s':>6} {'celdas':>12} {'log2 celdas / s':>16}")
    for nombre, familia in [("capacidad", familia_capacidad), ("dos objetos", familia_dos_objetos),
                            ("8 números", lambda b: familia_numeros(8, b))]:
        for b in [8, 16, 32, 64]:
            p, v, W = familia(b)
            s = tamano_entrada(p, v, W)
            c = celdas(len(p), W)
            print(f"{nombre:>16} {b:>4} {s:>6} {c:>12.4g} {math.log2(c) / s:>16.3f}")
    print()


def tabla_reparto(s_objetivo=512):
    print(f"Tabla 3. El mismo tamaño (≈{s_objetivo} bits) repartido de distintas formas")
    print(f"{'objetos n':>10} {'bits b':>7} {'s':>6} {'celdas':>12} {'tiempo a 10^9/s':>16}")
    for n in [1, 2, 4, 8, 16, 32]:
        b = 1
        while tamano_entrada(*familia_numeros(n, b + 1)) <= s_objetivo:
            b += 1
        p, v, W = familia_numeros(n, b)
        c = celdas(n, W)
        print(f"{n:>10} {b:>7} {tamano_entrada(p, v, W):>6} {c:>12.3g}"
              f" {_duracion(c / POR_SEGUNDO):>16}")
    print()


def tabla_primalidad():
    print("Tabla 4. Primalidad por división, peor caso (el mayor primo de b bits)")
    print(f"{'bits':>5} {'mayor primo':>24} {'divisiones':>14} {'2^(b/2)':>12}")
    for b in [8, 16, 24, 32, 48, 64]:
        print(f"{b:>5} {mayor_primo(b):>24,} {divisiones_peor_caso(b):>14,} {2 ** (b / 2):>12.4g}")
    print()


def medir(funcion, *args, repeticiones=3):
    mejor = math.inf
    for _ in range(repeticiones):
        inicio = time.perf_counter()
        funcion(*args)
        mejor = min(mejor, time.perf_counter() - inicio)
    return mejor


def tiempos():
    """Tiempos reales: mochila con 20 objetos de b bits y primalidad con primos de b bits."""
    mochila_rapida(*familia_numeros(20, 10))  # calentar numpy
    filas_mochila = []
    for b in range(10, 22):
        filas_mochila.append((b, medir(mochila_rapida, *familia_numeros(20, b))))
    filas_primo = []
    for b in range(16, 47, 2):
        filas_primo.append((b, medir(es_primo, mayor_primo(b))))
    return filas_mochila, filas_primo


def pendiente(filas):
    """Pendiente de log2(tiempo) contra bits, por mínimos cuadrados."""
    xs = [b for b, _ in filas]
    ys = [math.log2(t) for _, t in filas]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)


# La pendiente de la mochila se ajusta desde b = 15 (filas_mochila[5:]): ahí la fila mide
# 1,8 MB, claramente más que la caché L2 de 1 MB. Con b = 14 mide 913 KB, justo en el borde,
# y según la corrida el salto de la caché cae entre 13 y 14 o entre 14 y 15 (Tabla 6).
DESDE_MOCHILA = 5


def salto_de_cache(filas_mochila):
    """Índice k del mayor cociente t(b_k) / t(b_{k-1}): dónde cayó el salto en esta corrida."""
    return max(range(1, len(filas_mochila)),
               key=lambda k: filas_mochila[k][1] / filas_mochila[k - 1][1])


def tabla_tiempos(filas_mochila, filas_primo):
    print("Tabla 5. Tiempos medidos (mínimo de 3 corridas)")
    print("mochila, 20 objetos, pesos y valores de b bits, W = mitad del peso total:")
    for b, t in filas_mochila:
        print(f"  b = {b:>2}   {t * 1000:>9.2f} ms")
    k = salto_de_cache(filas_mochila)
    print(f"  salto de la caché: entre b = {filas_mochila[k - 1][0]} y b = {filas_mochila[k][0]}")
    print(f"  pendiente de log2(tiempo) por bit, desde b = {filas_mochila[DESDE_MOCHILA][0]}:"
          f" {pendiente(filas_mochila[DESDE_MOCHILA:]):.3f}")
    print("primalidad por división, mayor primo de b bits:")
    for b, t in filas_primo:
        print(f"  b = {b:>2}   {t * 1000:>9.2f} ms")
    print(f"  pendiente de log2(tiempo) por bit: {pendiente(filas_primo[3:]):.3f}")
    print()


TAMANOS_FILA_KB = [128, 256, 384, 512, 640, 768, 896, 1024, 1280, 1536, 2048, 3072, 4096, 8192]


def experimento_cache(tamanos_kb=TAMANOS_FILA_KB, repeticiones=9):
    """Tiempo por celda según los bytes de la fila, con enteros de 64 y de 32 bits.

    Si el salto de la Figura 2 es de la caché, depende de los bytes de la fila y no de
    cuántas celdas tiene: con int32 la fila ocupa la mitad, así que el salto tiene que
    aparecer en los mismos bytes, que son el doble de celdas. Devuelve filas
    (KB de la fila, ns por celda con int64, ns por celda con int32).
    """
    import numpy as np

    mochila_rapida([1], [1], 1000)                      # calentar numpy
    filas = []
    for kb in tamanos_kb:
        fila = [kb]
        for dtype in ("int64", "int32"):
            W = kb * 1024 // np.dtype(dtype).itemsize - 1
            pesos = [W // 8 + 37 * i for i in range(20)]
            valores = [1000 + i for i in range(20)]
            actualizadas = sum(W + 1 - w for w in pesos)  # celdas que toca np.maximum
            t = medir(mochila_rapida, pesos, valores, W, dtype, repeticiones=repeticiones)
            fila.append(t / actualizadas * 1e9)
        filas.append(tuple(fila))
    return filas


def kb_de_la_fila(b, objetos=20):
    """KB de la fila int64 de la mochila con `objetos` objetos de b bits (la de la Figura 2)."""
    W = familia_numeros(objetos, b)[2]
    return 8 * (W + 1) / 1024


def tabla_cache(filas):
    print("Tabla 6. Tiempo por celda según los bytes de la fila (mínimo de 9 corridas)")
    print(f"{'fila (KB)':>10} {'int64 (ns)':>11} {'int32 (ns)':>11}")
    for kb, t64, t32 in filas:
        print(f"{kb:>10} {t64:>11.3f} {t32:>11.3f}")
    print("  la fila de la Figura 2 (20 objetos, int64): "
          + ", ".join(f"b = {b}: {kb_de_la_fila(b):.0f} KB" for b in (12, 13, 14, 15)))
    print()


# ---------------------------------------------------------------------------
# 4. Figuras
# ---------------------------------------------------------------------------

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


def _serie_mochila(instancias, limite):
    xs, ys = [], []
    for p, v, W in instancias:
        s = tamano_entrada(p, v, W)
        if s <= limite:
            xs.append(s)
            ys.append(math.log2(celdas(len(p), W)))
    return xs, ys


def figura_costo_vs_bits(plt, destino):
    limite, techo = 400, 60
    series = [
        ("mochila: los bits en W (1 objeto)", AZUL,
         *_serie_mochila((familia_capacidad(b) for b in range(1, techo + 2)), limite)),
        # Primalidad solo hasta 80 bits, donde mayor_primo es exacto.
        ("primalidad por división", NARANJA, list(range(4, 81, 2)),
         [math.log2(divisiones_peor_caso(b)) for b in range(4, 81, 2)]),
        ("mochila: 8 objetos de b bits", AQUA,
         *_serie_mochila((familia_numeros(8, b) for b in range(2, 40)), limite)),
        ("mochila: objetos de 4 bits, n crece", AMARILLO,
         *_serie_mochila((familia_numeros(n, 4) for n in range(1, 60)), limite)),
    ]

    fig, ax = plt.subplots(figsize=(8, 4.8))
    for nombre, color, xs, ys in series:
        ax.plot(xs, ys, color=color, label=nombre)
    ax.text(66, 52, "pendiente 1: un bit más de W\nduplica el costo", color=TINTA, fontsize=9)
    ax.text(84, 37, "pendiente ½", color=TINTA, fontsize=9)
    ax.text(300, 26.5, "pendiente ≈ 1/17", color=TINTA, fontsize=9)
    ax.text(300, 9.5, "polinomial: Θ(s²)", color=TINTA, fontsize=9)
    ax.set_xlim(0, limite)
    ax.set_ylim(0, techo)
    ax.set_xlabel("tamaño de la entrada s, en bits")
    ax.set_ylabel("log₂ de las operaciones")
    ax.set_title("Mismo algoritmo, mismo tamaño: el costo depende de dónde están los bits")
    ax.legend(loc="upper right")
    fig.savefig(destino / "ejercicio-11-costo-vs-bits.png")
    plt.close(fig)


def figura_tiempos(plt, destino, filas_mochila, filas_primo):
    fig, ax = plt.subplots(figsize=(8, 4.6))
    # La mochila se ajusta desde b = 15, ya fuera de la caché L2 (ver DESDE_MOCHILA).
    for nombre, color, filas, desde in [
            ("mochila: 20 objetos de b bits (numpy)", AZUL, filas_mochila, DESDE_MOCHILA),
            ("primalidad: mayor primo de b bits", NARANJA, filas_primo, 3)]:
        xs = [b for b, _ in filas]
        ys = [t * 1000 for _, t in filas]
        ax.plot(xs, ys, "o-", color=color, markersize=6, markeredgecolor=SUPERFICIE,
                markeredgewidth=1.5, label=f"{nombre}: ×{2 ** pendiente(filas[desde:]):.2f} por bit")
    # La etiqueta va donde cayó el salto en esta corrida, a media altura (geométrica) del salto.
    k = salto_de_cache(filas_mochila)
    (b0, t0), (_, t1) = filas_mochila[k - 1], filas_mochila[k]
    medio = (t0 * t1) ** 0.5 * 1000
    ax.annotate("la fila deja de caber\nen la caché L2", (b0 + 0.5, medio), color=TINTA,
                fontsize=9, xytext=(b0 - 3, medio * 16),
                arrowprops=dict(arrowstyle="-", color=TENUE, linewidth=1))
    ax.set_yscale("log", base=2)
    ax.set_xlabel("bits b de los números de la entrada")
    ax.set_ylabel("tiempo medido (ms, escala log₂)")
    ax.set_title("Medido: cada bit de W duplica el tiempo; cada bit de N lo multiplica por √2")
    ax.legend(loc="upper left")
    fig.savefig(destino / "ejercicio-11-tiempos.png")
    plt.close(fig)


def figura_cache(plt, destino, filas):
    fig, ax = plt.subplots(figsize=(8, 4.4))
    kbs = [f[0] for f in filas]
    ax.plot(kbs, [f[1] for f in filas], "o-", color=AZUL, markersize=6, markeredgecolor=SUPERFICIE,
            markeredgewidth=1.5, label="int64, como en la Figura 2")
    ax.plot(kbs, [f[2] for f in filas], "o-", color=NARANJA, markersize=6, markeredgecolor=SUPERFICIE,
            markeredgewidth=1.5, label="int32: el doble de celdas por byte")
    techo = max(max(f[1], f[2]) for f in filas) * 1.15
    ax.axvline(1024, color=TINTA_2, linewidth=1.2, linestyle=(0, (4, 3)))
    ax.text(1024 * 1.05, techo * 0.93, "1 MB: la caché L2\nde un núcleo", color=TINTA, fontsize=9,
            va="top")
    for b in (13, 14):
        kb = kb_de_la_fila(b)
        ax.axvline(kb, color=TENUE, linewidth=1, linestyle=(0, (1, 2)))
        ax.text(kb * 0.97, techo * 0.06, f"b = {b}", color=TINTA_2, fontsize=8.5, ha="right")
    ax.set_xscale("log", base=2)
    marcas = [128, 256, 512, 1024, 2048, 4096, 8192]
    ax.set_xticks(marcas)
    ax.set_xticklabels([f"{k} KB" if k < 1024 else f"{k // 1024} MB" for k in marcas])
    ax.minorticks_off()
    ax.set_ylim(0, techo)
    ax.set_xlabel("tamaño de la fila")
    ax.set_ylabel("ns por celda")
    ax.set_title("El salto lo decide el tamaño en bytes de la fila, no la cantidad de celdas")
    ax.legend(loc="upper left")
    fig.savefig(destino / "ejercicio-11-cache.png")
    plt.close(fig)


def figuras(filas_mochila, filas_primo, filas_cache):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    _estilo(plt)
    destino = Path(__file__).resolve().parent.parent / "figuras"
    destino.mkdir(exist_ok=True)
    figura_costo_vs_bits(plt, destino)
    figura_tiempos(plt, destino, filas_mochila, filas_primo)
    figura_cache(plt, destino, filas_cache)
    print(f"figuras escritas en {destino}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # la consola de Windows no es UTF-8
    tabla_como_la_conferencia()
    tabla_familias()
    tabla_reparto()
    tabla_primalidad()
    if "--figuras" in sys.argv:
        filas_mochila, filas_primo = tiempos()
        tabla_tiempos(filas_mochila, filas_primo)
        filas_cache = experimento_cache()
        tabla_cache(filas_cache)
        figuras(filas_mochila, filas_primo, filas_cache)
