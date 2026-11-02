"""Ejercicio 10: par más cercano en una dimensión. Cota Ω(n log n) y cómo romperla.

Corre: python ejercicio-10.py  (prueba los dos algoritmos y la reducción contra fuerza bruta,
mide comparaciones y trabajo por punto, cuenta las reconstrucciones y genera la figura)
"""
import functools
import math
import random


def fuerza_bruta(xs):
    return min(abs(a - b) for i, a in enumerate(xs) for b in xs[i + 1:])


def ordenando(xs):
    """Dentro del modelo: ordenar y mirar los consecutivos (sección 3 de la conferencia 2).
    Devuelve (distancia mínima, pruebas de signo)."""
    pruebas = 0
    def cmp(a, b):
        nonlocal pruebas
        pruebas += 1                       # una prueba de signo de a - b
        return (a > b) - (a < b)
    ys = sorted(xs, key=functools.cmp_to_key(cmp))
    mejor = ys[1] - ys[0]
    for a, b in zip(ys[1:], ys[2:]):
        pruebas += 1                       # una prueba de signo de (b - a) - mejor
        mejor = min(mejor, b - a)
    return mejor, pruebas


def rejilla(xs, rng):
    """Fuera del modelo: la rejilla de Rabin de la sección 9 de la conferencia 2, en una dimensión.
    Celdas de largo δ, celda(x) = ⌊x / δ⌋, guardadas en una tabla hash.
    Los puntos son enteros, así que la parte entera es exacta.
    Devuelve (distancia mínima, accesos a la tabla, reconstrucciones)."""
    pts = list(xs)
    rng.shuffle(pts)
    delta = abs(pts[1] - pts[0])
    if delta == 0:
        return 0, 0, 0
    tabla = {p // delta: p for p in pts[:2]}
    accesos, reconstrucciones = 2, 0
    for i in range(2, len(pts)):
        p, c = pts[i], pts[i] // delta
        nuevo = delta
        for d in (-1, 0, 1):               # un punto a distancia < δ está en la celda vecina o en la misma
            accesos += 1
            q = tabla.get(c + d)
            if q is not None:
                nuevo = min(nuevo, abs(p - q))
        if nuevo == 0:
            return 0, accesos, reconstrucciones      # dos iguales: no hay nada más que buscar
        if nuevo < delta:                            # δ bajó: la rejilla vieja ya no sirve
            delta = nuevo
            tabla = {q // delta: q for q in pts[:i + 1]}
            accesos += i + 1
            reconstrucciones += 1
        else:
            tabla[c] = p
            accesos += 1
        assert len(tabla) == (i + 1)                 # invariante: a lo sumo un punto por celda
    return delta, accesos, reconstrucciones


def hay_repetidos(xs, par_mas_cercano):
    """La reducción: distinción de elementos con un algoritmo de par más cercano y una prueba más."""
    return par_mas_cercano(xs) == 0


if __name__ == "__main__":
    rng = random.Random(2026)

    # 1. Los dos algoritmos son correctos, con y sin repetidos
    for _ in range(3000):
        n = rng.randint(2, 40)
        hasta = rng.choice([n, 10 * n, 10 ** 9])     # rango chico: muchos repetidos
        xs = [rng.randint(0, hasta) for _ in range(n)]
        d = fuerza_bruta(xs)
        assert ordenando(xs)[0] == d
        assert rejilla(xs, rng)[0] == d
        # la reducción responde distinción de elementos
        assert hay_repetidos(xs, lambda v: ordenando(v)[0]) == (len(set(xs)) < n)
        assert hay_repetidos(xs, lambda v: rejilla(v, rng)[0]) == (len(set(xs)) < n)
    print("3000 entradas (con y sin repetidos): los dos algoritmos y la reducción coinciden con fuerza bruta")

    # 2. Costo por punto: ordenando crece como log n, la rejilla se queda constante
    print(f"\n{'n':>8} {'pruebas/n (ordenando)':>22} {'log2 n':>7} {'accesos/n (rejilla)':>20} "
          f"{'reconstrucciones':>17} {'2 ln n':>7}")
    filas = []
    for n in [1_000, 10_000, 100_000, 300_000]:
        xs = rng.sample(range(10 ** 12), n)         # sin repetidos: el caso más caro
        _, pruebas = ordenando(xs)
        corridas = [rejilla(xs, random.Random(s)) for s in range(10)]
        acc = sum(c[1] for c in corridas) / len(corridas)
        rec = sum(c[2] for c in corridas) / len(corridas)
        filas.append((n, pruebas / n, acc / n))
        print(f"{n:>8,} {pruebas / n:>22.2f} {math.log2(n):>7.2f} {acc / n:>20.2f} {rec:>17.1f} {2 * math.log(n):>7.1f}")
        # esperado: 3 consultas + 1 inserción + a lo sumo 2 de reconstrucciones = 6 por punto;
        # el promedio de 10 corridas fluctúa, porque una reconstrucción tardía cuesta del orden de n
        assert acc / n < 8
    assert filas[-1][1] > filas[0][1] + 5          # ordenando: crece con log n
    assert filas[-1][2] < 8                        # rejilla: no crece

    # 3. Figura
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("\n(sin matplotlib: no se genera la figura)")
    else:
        ns = [int(10 ** (e / 2)) for e in range(6, 12)]
        orden, rej = [], []
        for n in ns:
            xs = rng.sample(range(10 ** 12), n)
            orden.append(ordenando(xs)[1] / n)
            rej.append(sum(rejilla(xs, random.Random(s))[1] for s in range(3)) / 3 / n)
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(ns, orden, "o-", c="#2563eb", label="ordenando: pruebas de signo por punto")
        ax.plot(ns, rej, "s-", c="#dc2626", label="rejilla: accesos a la tabla por punto")
        ax.set_xscale("log")
        ax.set_xlabel("n (escala logarítmica)"); ax.set_ylabel("operaciones por punto")
        ax.set_title("Par más cercano en una dimensión")
        ax.legend(); fig.tight_layout()
        fig.savefig("ejercicio-10-costo.png", dpi=150)
        print("\nfigura: ejercicio-10-costo.png")
