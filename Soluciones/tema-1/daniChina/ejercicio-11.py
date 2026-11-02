"""
Tema 1, ejercicio 11: la mochila entera con programacion dinamica, O(nW).
Medimos el tamano de la entrada en bits y preguntamos: es polinomial?

Modelo: RAM con palabras. Las operaciones aritmeticas sobre numeros que
caben en una palabra (pesos, valores, indices) cuestan 1.
Uso:  python ejercicio11_mochila.py
"""
import itertools
import random
import time
from pathlib import Path


# ----------------------------------------------------------------------------
# El algoritmo: tabla dp[i][c]
#   dp[i][c] = mejor valor con los primeros i objetos y capacidad c
# ----------------------------------------------------------------------------
def mochila(pesos, valores, W):
    """Devuelve (mejor_valor, tabla, operaciones). operaciones = celdas calculadas."""
    n = len(pesos)
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    operaciones = 0
    for i in range(1, n + 1):
        p, v = pesos[i - 1], valores[i - 1]
        for c in range(W + 1):
            operaciones += 1
            dp[i][c] = dp[i - 1][c]                    # no lo llevo
            if c >= p and dp[i - 1][c - p] + v > dp[i][c]:
                dp[i][c] = dp[i - 1][c - p] + v        # lo llevo
    return dp[n][W], dp, operaciones


def mochila_1d(pesos, valores, W):
    """Misma idea con una sola fila. Se recorre c de mayor a menor para no
    usar el mismo objeto dos veces."""
    dp = [0] * (W + 1)
    for p, v in zip(pesos, valores):
        for c in range(W, p - 1, -1):
            dp[c] = max(dp[c], dp[c - p] + v)
    return dp[W]


def reconstruir(dp, pesos, W):
    """Vuelve por la tabla: devuelve (objetos elegidos, celdas recorridas)."""
    i, c = len(pesos), W
    elegidos, camino = [], [(i, c)]
    while i > 0:
        if dp[i][c] != dp[i - 1][c]:                   # lo llevo
            elegidos.append(i)
            c -= pesos[i - 1]
        i -= 1
        camino.append((i, c))
    return sorted(elegidos), camino


def fuerza_bruta(pesos, valores, W):
    mejor = 0
    for mascara in itertools.product((0, 1), repeat=len(pesos)):
        peso = sum(m * p for m, p in zip(mascara, pesos))
        if peso <= W:
            mejor = max(mejor, sum(m * v for m, v in zip(mascara, valores)))
    return mejor


# ----------------------------------------------------------------------------
# Tamano de la entrada en bits
# ----------------------------------------------------------------------------
def bits(k):
    return max(1, k.bit_length())


def tamano_entrada(pesos, valores, W):
    return sum(bits(p) for p in pesos) + sum(bits(v) for v in valores) + bits(W)


# ----------------------------------------------------------------------------
# La primalidad por division, para comparar
# ----------------------------------------------------------------------------
def divisiones_primalidad(n):
    divisiones, d = 0, 2
    while d * d <= n:
        divisiones += 1
        if n % d == 0:
            return divisiones
        d += 1
    return divisiones


def es_primo(k):
    d = 2
    while d * d <= k:
        if k % d == 0:
            return False
        d += 1
    return k >= 2


def primo_menor_que(tope):
    k = tope - 1
    while not es_primo(k):
        k -= 1
    return k


# ----------------------------------------------------------------------------
# Animaciones (opcionales, necesitan Pillow)
# ----------------------------------------------------------------------------
def _fuentes():
    from PIL import ImageFont
    try:
        return ImageFont.load_default(size=18), ImageFont.load_default(size=14)
    except TypeError:
        f = ImageFont.load_default()
        return f, f


def generar_gif_tabla(pesos, valores, W, ruta):
    """Como se llena la tabla fila por fila y como se recupera la solucion."""
    from PIL import Image, ImageDraw

    fuente, chica = _fuentes()
    n = len(pesos)
    mejor, dp, _ = mochila(pesos, valores, W)
    elegidos, camino = reconstruir(dp, pesos, W)
    C, X0, Y0 = 52, 150, 90
    ANCHO, ALTO = X0 + C * (W + 1) + 20, Y0 + C * (n + 1) + 90

    def cuadro(k, msg, final=False):
        im = Image.new("RGB", (ANCHO, ALTO), "white")
        d = ImageDraw.Draw(im)
        d.text((15, 10), f"capacidad W = {W}    objetos (peso, valor): "
               + "  ".join(f"({p},{v})" for p, v in zip(pesos, valores)),
               fill="black", font=chica)
        d.text((15, 40), "dp[i][c] = mejor valor con los primeros i objetos y capacidad c",
               fill="#444444", font=chica)
        for c in range(W + 1):
            d.text((X0 + c * C + C // 2 - 6, Y0 - 24), str(c), fill="#444444", font=chica)
        for i in range(n + 1):
            etiqueta = "i=0  sin objetos" if i == 0 else f"i={i}  p={pesos[i-1]} v={valores[i-1]}"
            d.text((10, Y0 + i * C + C // 2 - 7), etiqueta, fill="#444444", font=chica)
            for c in range(W + 1):
                x0, y0 = X0 + c * C, Y0 + i * C
                visible = i <= k
                fondo = "#ffffff" if visible else "#eeeeee"
                if visible and i == k and not final:
                    fondo = "#ffe27a"
                if final and (i, c) in camino:
                    fondo = "#7fd18b"
                d.rectangle([x0, y0, x0 + C, y0 + C], fill=fondo,
                            outline="#555555", width=2)
                if visible:
                    d.text((x0 + C // 2 - 6, y0 + C // 2 - 8), str(dp[i][c]),
                           fill="black", font=fuente)
        d.text((15, Y0 + C * (n + 1) + 15), msg, fill="#b00020", font=chica)
        return im

    frames = [cuadro(0, "sin objetos, toda capacidad vale 0")]
    for k in range(1, n + 1):
        p, v = pesos[k - 1], valores[k - 1]
        frames.append(cuadro(
            k, f"objeto {k} (peso {p}, valor {v}): dp[{k}][c] = max(no lo llevo, "
               f"lo llevo = dp[{k-1}][c-{p}] + {v})"))
    frames.append(cuadro(n, f"respuesta dp[{n}][{W}] = {mejor}; "
                            f"se llevan los objetos {elegidos}", final=True))
    frames += [frames[-1]]
    frames[0].save(ruta, save_all=True, append_images=frames[1:],
                   duration=1500, loop=0)


def generar_gif_bits(ruta, kmax=10):
    """Un bit mas en W duplica las celdas de la tabla."""
    from PIL import Image, ImageDraw

    fuente, chica = _fuentes()
    C, LADO, X0, Y0 = 9, 32, 20, 60
    ANCHO, ALTO = X0 + C * LADO + 330, Y0 + C * LADO + 40
    frames = []
    for k in range(1, kmax + 1):
        celdas = 2 ** k
        im = Image.new("RGB", (ANCHO, ALTO), "white")
        d = ImageDraw.Draw(im)
        d.text((15, 12), "una celda de la tabla por cada capacidad 0, 1, ..., W",
               fill="black", font=chica)
        d.text((15, 32), "(se dibuja con n = 1 objeto: la tabla tiene W + 1 celdas)",
               fill="#444444", font=chica)
        for idx in range(LADO * LADO):
            r, c = divmod(idx, LADO)
            x0, y0 = X0 + c * C, Y0 + r * C
            d.rectangle([x0, y0, x0 + C, y0 + C],
                        fill="#1f6feb" if idx < celdas else "#ffffff",
                        outline="#dddddd")
        xp = X0 + C * LADO + 25
        d.text((xp, Y0), f"bits de W:  {k}", fill="black", font=fuente)
        d.text((xp, Y0 + 32), f"W = 2^{k} - 1 = {2 ** k - 1}", fill="black", font=chica)
        for b in range(k):                                 # W en binario
            d.rectangle([xp + b * 22, Y0 + 66, xp + b * 22 + 18, Y0 + 90],
                        fill="#ffe27a", outline="#555555")
            d.text((xp + b * 22 + 5, Y0 + 69), "1", fill="black", font=chica)
        d.text((xp, Y0 + 110), f"celdas de la tabla:  {celdas}", fill="#b00020", font=fuente)
        d.text((xp, Y0 + 148), "un bit mas en W", fill="#444444", font=chica)
        d.text((xp, Y0 + 168), "= el doble de celdas", fill="#444444", font=chica)
        frames.append(im)
    frames += [frames[-1]]
    frames[0].save(ruta, save_all=True, append_images=frames[1:],
                   duration=900, loop=0)


# ----------------------------------------------------------------------------
# Experimentos
# ----------------------------------------------------------------------------
EJ_PESOS, EJ_VALORES, EJ_W = [1, 3, 4, 5], [1, 4, 5, 7], 7


def comprobar_algoritmo():
    rng = random.Random(11)
    casos = 0
    for _ in range(600):
        n = rng.randint(0, 9)
        pesos = [rng.randint(1, 8) for _ in range(n)]
        valores = [rng.randint(1, 20) for _ in range(n)]
        W = rng.randint(0, 25)
        mejor, dp, ops = mochila(pesos, valores, W)
        assert mejor == mochila_1d(pesos, valores, W) == fuerza_bruta(pesos, valores, W)
        assert ops == n * (W + 1)                    # exactamente n(W+1) celdas
        elegidos, _ = reconstruir(dp, pesos, W)
        assert sum(pesos[i - 1] for i in elegidos) <= W
        assert sum(valores[i - 1] for i in elegidos) == mejor
        casos += 1
    print(f"tabla, version de una fila y fuerza bruta coinciden en {casos} instancias; "
          f"las operaciones son exactamente n(W+1)")


def tabla_en_bits():
    """n fijo; W con b bits (el mayor posible, 2^b - 1): el costo se duplica por bit."""
    rng = random.Random(5)
    n = 10
    pesos = [rng.randint(1, 8) for _ in range(n)]
    valores = [rng.randint(1, 20) for _ in range(n)]
    print(f"n = {n} objetos; W = 2^b - 1 (el mayor numero de b bits)")
    print(f"{'b':>3} {'N (bits)':>9} {'W':>8} {'operaciones':>12} {'ops / N^2':>10} "
          f"{'tiempo (s)':>11} {'x anterior':>11}")
    anterior = None
    for b in range(4, 18):
        W = 2 ** b - 1
        N = tamano_entrada(pesos, valores, W)
        t0 = time.perf_counter()
        _, _, ops = mochila(pesos, valores, W)
        t = time.perf_counter() - t0
        razon = f"{t / anterior:>10.2f}" if anterior and anterior > 0.02 else f"{'':>10}"
        print(f"{b:>3} {N:>9} {W:>8} {ops:>12,} {ops / N ** 2:>10.1f} {t:>11.3f} {razon}")
        anterior = t


def a_escala_real():
    n, ritmo = 100, 10 ** 9
    print(f"n = {n} objetos, {ritmo:.0e} operaciones por segundo")
    print(f"{'bits de W':>10} {'operaciones':>12} {'tiempo':>16} {'memoria (1 fila)':>18}")
    for b in (20, 32, 40, 50, 64):
        W = 2 ** b - 1
        ops = n * (W + 1)
        seg = ops / ritmo
        if seg < 60:
            tiempo = f"{seg:.3g} s"
        elif seg < 86400:
            tiempo = f"{seg / 3600:.3g} horas"
        elif seg < 86400 * 365:
            tiempo = f"{seg / 86400:.3g} dias"
        else:
            tiempo = f"{seg / (86400 * 365):.3g} anios"
        mem = 8 * (W + 1)
        if mem < 2 ** 30:
            memoria = f"{mem / 2 ** 20:.3g} MB"
        elif mem < 2 ** 40:
            memoria = f"{mem / 2 ** 30:.3g} GB"
        else:
            memoria = f"{mem / 2 ** 40:.3g} TB"
        print(f"{b:>10} {ops:>12.3g} {tiempo:>16} {memoria:>18}")


def comparar_con_primalidad():
    print(f"{'bits':>5} {'divisiones (primo)':>19} {'x (2 bits)':>11} "
          f"{'celdas mochila (n=1)':>21} {'x (2 bits)':>11}")
    ant_p = ant_m = None
    for b in range(10, 31, 2):
        p = primo_menor_que(2 ** b)
        divs = divisiones_primalidad(p)
        celdas = 2 ** b
        rp = f"{divs / ant_p:>10.2f}" if ant_p else f"{'':>10}"
        rm = f"{celdas / ant_m:>10.2f}" if ant_m else f"{'':>10}"
        print(f"{b:>5} {divs:>19,} {rp} {celdas:>21,} {rm}")
        ant_p, ant_m = divs, celdas


def main():
    mejor, dp, ops = mochila(EJ_PESOS, EJ_VALORES, EJ_W)
    elegidos, _ = reconstruir(dp, EJ_PESOS, EJ_W)
    print(f"Ejemplo: pesos {EJ_PESOS}, valores {EJ_VALORES}, W = {EJ_W}")
    print(f"mejor valor = {mejor}, objetos {elegidos}, celdas calculadas = {ops}")
    for fila in dp:
        print("  ", fila)
    print()
    comprobar_algoritmo()
    print()
    tabla_en_bits()
    print()
    a_escala_real()
    print()
    comparar_con_primalidad()
    print()
    try:
        base = Path(__file__).parent
        generar_gif_tabla(EJ_PESOS, EJ_VALORES, EJ_W, base / "mochila_tabla.gif")
        generar_gif_bits(base / "mochila_bits.gif")
        print("animaciones guardadas: mochila_tabla.gif y mochila_bits.gif")
    except ImportError:
        print("(sin Pillow: se omiten las animaciones)")


if __name__ == "__main__":
    main()
