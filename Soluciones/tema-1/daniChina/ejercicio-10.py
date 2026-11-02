"""
Ejercicio 10: par mas cercano en una dimension.

Dados n numeros reales (una lista, puede haber repetidos), hallar dos que
minimicen |x_i - x_j|.

  1. Ordenar y mirar vecinos: O(n log n), optimo en arboles de decision algebraicos
     (por reduccion desde distincion de elementos).
  2. Rejilla aleatoria incremental: O(n) esperado. Rompe la cota porque usa la parte
     entera y una tabla hash, que ese modelo no tiene.

Uso:
    python ejercicio10_par_cercano_1d.py             # corre los experimentos
    python ejercicio10_par_cercano_1d.py --figuras   # ademas genera png y gif
"""
import math
import random
import sys
import time
from functools import cmp_to_key
from itertools import combinations


# --------------------------------------------------------------------------
# 1. Los algoritmos
# --------------------------------------------------------------------------
def fuerza_bruta(xs):
    """El oraculo: mira todos los pares. O(n^2)."""
    a, b = min(combinations(xs, 2), key=lambda par: abs(par[0] - par[1]))
    return abs(a - b), (a, b)


def ordenando(xs, cuenta=None):
    """Ordenar y mirar solo los pares de vecinos. O(n log n)."""
    def cmp(a, b):
        if cuenta is not None:
            cuenta[0] += 1
        return (a > b) - (a < b)
    ys = sorted(xs, key=cmp_to_key(cmp))
    mejor = (ys[1] - ys[0], (ys[0], ys[1]))
    for k in range(1, len(ys) - 1):
        if cuenta is not None:
            cuenta[0] += 1                       # comparar dos huecos
        if ys[k + 1] - ys[k] < mejor[0]:
            mejor = (ys[k + 1] - ys[k], (ys[k], ys[k + 1]))
    return mejor


def rejilla(xs, semilla=0, traza=None):
    """Incremental y aleatorio. Devuelve (distancia, par, info).

    info: reconstrucciones y operaciones sobre la tabla (consultas + inserciones).
    Cajas de largo delta (la mejor distancia hasta ahora), en una tabla hash.
    """
    pts = list(xs)
    random.Random(semilla).shuffle(pts)
    delta = abs(pts[0] - pts[1])
    par = (pts[0], pts[1])
    info = {"reconstrucciones": 0, "operaciones": 0}
    if delta == 0:
        return 0, par, info

    celda = lambda x: x // delta                  # la parte entera: lo que el modelo no tiene
    tabla = {}
    for x in pts[:2]:
        tabla.setdefault(celda(x), []).append(x)
        info["operaciones"] += 1

    for i in range(2, len(pts)):
        p = pts[i]
        c = celda(p)
        mejor, mejor_q = delta, None
        for dc in (-1, 0, 1):                     # las 3 cajas cercanas
            info["operaciones"] += 1
            for q in tabla.get(c + dc, ()):
                if abs(p - q) < mejor:
                    mejor, mejor_q = abs(p - q), q
        if traza is not None:
            traza.append(dict(i=i, p=p, delta=delta, q=mejor_q, d=mejor, previos=pts[:i],
                              par=par))
        if mejor < delta:                         # delta bajo: reconstruir
            delta, par = mejor, (p, mejor_q)
            info["reconstrucciones"] += 1
            if delta == 0:                        # dos valores iguales
                return 0, par, info
            tabla = {}
            for x in pts[:i + 1]:
                tabla.setdefault(x // delta, []).append(x)
                info["operaciones"] += 1
        else:
            tabla.setdefault(c, []).append(p)
            info["operaciones"] += 1
    return delta, par, info


def hay_repetidos_via_par_cercano(xs, algoritmo):
    """La reduccion: los numeros de la lista son los puntos. Hay repetidos si y solo
    si la distancia minima es 0."""
    return algoritmo(xs)[0] == 0


# --------------------------------------------------------------------------
# 2. Experimentos
# --------------------------------------------------------------------------
def exp_correctitud():
    print("== Correctitud contra la fuerza bruta ==")
    rng = random.Random(1)
    malos = {"ordenando": 0, "rejilla": 0}
    pruebas = 0
    for _ in range(3000):
        n = rng.randint(2, 30)
        if rng.random() < 0.5:
            xs = rng.sample(range(1000), n)                        # enteros distintos
        else:
            xs = [rng.random() * 100 for _ in range(n)]            # reales
        d0 = fuerza_bruta(xs)[0]
        malos["ordenando"] += abs(ordenando(xs)[0] - d0) > 1e-12
        malos["rejilla"] += abs(rejilla(xs, semilla=rng.randrange(10**6))[0] - d0) > 1e-12
        pruebas += 1
    print(f"  {pruebas} pruebas. fallos: ordenando = {malos['ordenando']}, rejilla = {malos['rejilla']}\n")


def exp_reduccion():
    print("== La reduccion: distincion de elementos usando el par mas cercano ==")
    rng = random.Random(2)
    bien = {"ordenando": 0, "rejilla": 0}
    total = 4000
    for _ in range(total):
        n = rng.randint(2, 20)
        xs = [rng.randrange(60) for _ in range(n)]                 # a veces hay repetidos
        verdad = len(set(xs)) < len(xs)
        bien["ordenando"] += hay_repetidos_via_par_cercano(xs, ordenando) == verdad
        bien["rejilla"] += hay_repetidos_via_par_cercano(xs, lambda v: rejilla(v, semilla=7)) == verdad
    print(f"  aciertos de 'hay repetidos?' sobre {total} listas: "
          f"ordenando = {bien['ordenando']}, rejilla = {bien['rejilla']}\n")


def exp_costo():
    print("== Costo: operaciones, no segundos ==")
    print("  ordenando: comparaciones.  rejilla: consultas e inserciones en la tabla.")
    print(f"{'n':>8} {'comparaciones':>14} {'comp. / n':>10} {'ops tabla':>11} {'ops / n':>8} "
          f"{'reconstr.':>10} {'2 ln n':>7}")
    rng = random.Random(3)
    for n in [1_000, 10_000, 100_000]:
        xs = rng.sample(range(100 * n), n)
        cuenta = [0]
        ordenando(xs, cuenta)
        ops, rec, veces = 0, 0, 5
        for s in range(veces):
            _, _, info = rejilla(xs, semilla=s)
            ops += info["operaciones"]
            rec += info["reconstrucciones"]
        print(f"{n:>8,} {cuenta[0]:>14,} {cuenta[0] / n:>10.1f} {ops // veces:>11,} {ops / veces / n:>8.1f} "
              f"{rec / veces:>10.1f} {2 * math.log(n):>7.1f}")
    print()


def exp_tiempos():
    print("== Tiempos (ojo: sorted de Python esta escrito en C, la rejilla no) ==")
    print(f"{'n':>9} {'ordenando':>11} {'rejilla':>9}")
    rng = random.Random(4)
    for n in [10_000, 100_000, 1_000_000]:
        xs = rng.sample(range(100 * n), n)
        t = time.perf_counter(); ys = sorted(xs); min(b - a for a, b in zip(ys, ys[1:])); t1 = time.perf_counter() - t
        t = time.perf_counter(); rejilla(xs); t2 = time.perf_counter() - t
        print(f"{n:>9,} {t1:>10.3f}s {t2:>8.3f}s")
    print()


# --------------------------------------------------------------------------
# 3. Figuras: png y gif (necesita matplotlib y pillow)
# --------------------------------------------------------------------------
def figuras():
    import io
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from PIL import Image

    # ---- png: la reduccion
    xs = [12, 47, 5, 33, 47, 80, 21]
    fig, ax = plt.subplots(figsize=(9, 2.6))
    ax.set_xlim(-3, 88); ax.set_ylim(-1.2, 1.6); ax.axis("off")
    ax.plot([0, 85], [0, 0], color="#555", lw=1.5)
    for x in xs:
        rep = xs.count(x) > 1
        ax.scatter([x], [0], s=160 if not rep else 220, zorder=3,
                   color="#d62728" if rep else "#1f77b4", edgecolor="black")
        ax.text(x, -0.55, str(x), ha="center", fontsize=11)
    ax.annotate("dos valores iguales =\ndos puntos a distancia 0", xy=(47, 0.15), xytext=(47, 1.0),
                ha="center", fontsize=10, color="#d62728", arrowprops=dict(arrowstyle="->", color="#d62728"))
    ax.set_title("La reducción: los números de la lista son los puntos de la recta", loc="left", fontsize=11)
    ax.text(-2, -1.1, "hay repetidos  <=>  la distancia del par más cercano es 0", fontsize=10, color="#444")
    fig.tight_layout(); fig.savefig("par1d_reduccion.png", dpi=110); plt.close(fig)

    # ---- gif: la rejilla paso a paso. Se busca un orden con unas pocas reconstrucciones
    base = [7, 91, 40, 62, 15, 78, 33, 54, 22, 85, 3, 68]
    semilla = next(s for s in range(500) if 2 <= rejilla(base, s)[2]["reconstrucciones"] <= 4)
    traza = []
    rejilla(base, semilla, traza)
    pts = list(base)
    random.Random(semilla).shuffle(pts)

    def dibujar(titulo, insertados, delta, p=None, bloque=None, par=None, lineas=()):
        fig, ax = plt.subplots(figsize=(9, 3.6))
        ax.set_xlim(-2, 102); ax.set_ylim(-1.6, 2.0); ax.axis("off")
        ax.set_title(titulo, loc="left", fontsize=10, family="monospace")
        if bloque is not None:
            ax.fill_between([bloque[0], bloque[1]], -0.45, 0.65, color="#d9ecf5", zorder=0)
        k = 0
        while k * delta <= 101:
            ax.plot([k * delta] * 2, [-0.35, 0.55], color="#999", lw=0.9, zorder=1)
            k += 1
        ax.plot([0, 100], [0, 0], color="#555", lw=1.4, zorder=1)
        for x in insertados:
            enpar = par is not None and x in par
            ax.scatter([x], [0.1], s=120, zorder=3, color="#d62728" if enpar else "#1f77b4", edgecolor="black")
            ax.text(x, -0.75, str(x), ha="center", fontsize=8)
        if p is not None:
            ax.scatter([p], [0.1], s=170, zorder=4, color="#ff9f1c", edgecolor="black")
            ax.text(p, 0.8, f"p = {p}", ha="center", fontsize=10, color="#b35c00")
        ax.text(0, 1.5, f"delta = {delta}   (largo de cada caja)", fontsize=10, family="monospace")
        for t, l in enumerate(lineas):
            ax.text(0, -1.2 - 0.35 * t, l, fontsize=9, family="monospace")
        fig.tight_layout()
        buf = io.BytesIO(); fig.savefig(buf, format="png", dpi=90); plt.close(fig)
        buf.seek(0)
        return Image.open(buf).convert("P", palette=Image.ADAPTIVE)

    d0 = abs(pts[0] - pts[1])
    cuadros = [dibujar(f"Empiezo con los dos primeros puntos ({pts[0]} y {pts[1]}): delta = {d0}",
                       pts[:2], d0, par=(pts[0], pts[1]))]
    for t in traza:
        delta = t["delta"]
        c = t["p"] // delta
        bloque = ((c - 1) * delta, (c + 2) * delta)
        cuadros.append(dibujar(f"llega p = {t['p']}: miro solo las 3 cajas de alrededor", t["previos"], delta,
                               p=t["p"], bloque=bloque, par=t["par"],
                               lineas=[f"cajas consultadas: {c - 1}, {c}, {c + 1}"]))
        if t["d"] < delta:
            nuevo = t["d"]
            cuadros.append(dibujar(f"{t['p']} está a {nuevo} de {t['q']}: delta baja de {delta} a {nuevo}",
                                   t["previos"] + [t["p"]], nuevo, par=(t["p"], t["q"]),
                                   lineas=["hay que reconstruir la rejilla con cajas más chicas",
                                           "(pasa pocas veces: con orden al azar, unas 2 ln n)"]))
        else:
            cuadros.append(dibujar(f"no hay nadie a menos de {delta} de {t['p']}: delta no cambia, lo guardo",
                                   t["previos"] + [t["p"]], delta, par=t["par"],
                                   lineas=["costo: 3 consultas a la tabla"]))
    cuadros[0].save("par1d_rejilla.gif", save_all=True, append_images=cuadros[1:], duration=1700, loop=0)
    print("figuras escritas: par1d_reduccion.png, par1d_rejilla.gif")


if __name__ == "__main__":
    exp_correctitud()
    exp_reduccion()
    exp_costo()
    exp_tiempos()
    if "--figuras" in sys.argv:
        figuras()
