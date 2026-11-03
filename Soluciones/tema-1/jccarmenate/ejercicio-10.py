"""Ejercicio 10 del Tema 1: el par más cercano en una dimensión.

    python ejercicio-10.py

Imprime todas las tablas que cita ejercicio-10.md, corre las pruebas y regenera las
dos figuras (ejercicio-10-rejilla.svg y ejercicio-10-trabajo.svg). Cada número que
aparece en la prosa sale de aquí. Solo necesita matplotlib.
"""

import math
import random

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt


# --------------------------------------------------------------------------
# 1. Los algoritmos
# --------------------------------------------------------------------------
# Los puntos son enteros: así la celda de un punto, x // delta, se calcula sin
# redondeos, y ninguna celda puede recibir dos puntos por un error de coma flotante.

def ordenando(xs):
    """El oráculo: ordenar y mirar vecinos consecutivos."""
    ys = sorted(xs)
    return min(b - a for a, b in zip(ys, ys[1:]))


def distincion(xs):
    """Distinción de elementos resuelta con el par más cercano: hay dos iguales si y
    solo si la distancia mínima es 0."""
    return ordenando(xs) == 0


class Rejilla:
    """El algoritmo aleatorio incremental, en una dimensión. Celdas de ancho delta,
    guardadas en un diccionario (una tabla hash). Cuenta el trabajo: 3 consultas por
    punto insertado más el tamaño de cada reconstrucción."""

    def __init__(self, vecinas=(-1, 0, 1)):
        self.vecinas = vecinas                  # el error plantado mira menos celdas
        self.trabajo = self.reconstrucciones = 0

    def resolver(self, xs, semilla=0, permutar=True, foto_en=None):
        pts = list(xs)
        if permutar:
            random.Random(semilla).shuffle(pts)
        d = abs(pts[0] - pts[1])
        if d == 0:
            return 0
        tabla = {pts[0] // d: pts[0], pts[1] // d: pts[1]}
        self.foto = None
        for i in range(2, len(pts)):
            p = pts[i]
            c = p // d
            if foto_en == i:
                self.foto = (dict(tabla), d, p)
            mejor = d
            for k in self.vecinas:
                q = tabla.get(c + k)
                if q is not None:
                    mejor = min(mejor, abs(p - q))
            self.trabajo += len(self.vecinas)
            if mejor == 0:
                return 0
            if mejor < d:                       # delta bajó: reconstruir con celdas nuevas
                d = mejor
                tabla = {q // d: q for q in pts[:i + 1]}
                self.trabajo += i + 1
                self.reconstrucciones += 1
            else:
                assert c not in tabla           # cada celda tiene a lo sumo un punto
                tabla[c] = p
        return d


def adversaria(n):
    """Un orden de inserción en el que cada punto nuevo baja delta: los huecos van
    n - 1, n - 2, ..., 1."""
    xs, x = [0], 0
    for k in range(1, n):
        x += n - k
        xs.append(x)
    return xs


def seccion(titulo):
    print()
    print(titulo)
    print("-" * len(titulo))


def miles(x):
    return f"{x:,}".replace(",", " ")


# --------------------------------------------------------------------------
# 2. Las tablas que cita la prosa
# --------------------------------------------------------------------------

def reduccion():
    seccion("§2. La reducción, con números")
    for xs in [[31, 7, 19, 52, 7, 40], [31, 7, 19, 52, 8, 40]]:
        print(f"{xs}: par más cercano = {ordenando(xs)}; "
              f"{'hay repetidos' if distincion(xs) else 'todos distintos'}")


def correctitud():
    seccion("§4. La rejilla contra el oráculo")
    rng = random.Random(4)
    bien = total = 0
    for _ in range(3000):
        n = rng.randint(2, 200)
        xs = [rng.randrange(rng.choice([300, 10**6, 10**12])) for _ in range(n)]
        total += 1
        bien += Rejilla().resolver(xs, semilla=rng.randrange(10**9)) == ordenando(xs)
    print(f"{miles(total)} conjuntos al azar, con y sin repetidos: la rejilla acierta en "
          f"{miles(bien)}")


def reconstrucciones():
    seccion("§5. Reconstrucciones y trabajo, con la permutación al azar")
    rng = random.Random(5)
    medidas = []
    print(f"{'n':>8} {'corridas':>9} {'reconstrucciones':>17} {'2(H_n - 1.5)':>13} "
          f"{'trabajo / n':>12}")
    for n in [10**3, 10**4, 10**5]:
        xs = rng.sample(range(10**12), n)
        rs, ts = [], []
        for s in range(10 if n < 10**5 else 4):
            r = Rejilla()
            assert r.resolver(xs, semilla=s) == ordenando(xs)
            rs.append(r.reconstrucciones)
            ts.append(r.trabajo / n)
        esperado = 2 * (sum(1 / k for k in range(1, n + 1)) - 1.5)
        (mr, er), (mt, et) = media_y_error(rs), media_y_error(ts)
        medidas.append((n, mt))
        print(f"{miles(n):>8} {len(rs):>9} {mr:>11.1f} ± {er:.1f} {esperado:>13.1f} "
              f"{mt:>5.2f} ± {et:.2f}")
    return medidas


def media_y_error(v):
    """El promedio de las corridas y su error estándar."""
    m = sum(v) / len(v)
    return m, math.sqrt(sum((x - m) ** 2 for x in v) / (len(v) - 1) / len(v))


def sin_permutar():
    seccion("§6. Sin la permutación: el orden adversario")
    filas = []
    print(f"{'n':>6} {'trabajo, en orden':>18} {'trabajo, permutado':>19} "
          f"{'reconstrucciones en orden':>26}")
    for n in [100, 300, 1000, 3000]:
        xs = adversaria(n)
        a, b = Rejilla(), Rejilla()
        assert a.resolver(xs, permutar=False) == b.resolver(xs, semilla=1) == ordenando(xs)
        filas.append((n, a.trabajo / n, b.trabajo / n))
        print(f"{n:>6} {miles(a.trabajo):>18} {miles(b.trabajo):>19} "
              f"{a.reconstrucciones:>26}")
    return filas


def errores_plantados():
    seccion("§7. Mirar menos celdas")
    rng = random.Random(7)
    casos = []
    for _ in range(3000):
        n = rng.randint(2, 100)
        casos.append(rng.sample(range(10**6), n))
    print(f"{'celdas que mira':>26} {'conjuntos mal':>14}")
    for nombre, vec in [("las tres", (-1, 0, 1)), ("la suya y la de la derecha", (0, 1)),
                        ("solo la suya", (0,))]:
        mal = sum(Rejilla(vec).resolver(xs, semilla=k) != ordenando(xs)
                  for k, xs in enumerate(casos))
        print(f"{nombre:>26} {100 * mal / len(casos):>13.1f}%")


# --------------------------------------------------------------------------
# 3. Pruebas
# --------------------------------------------------------------------------

def pruebas():
    seccion("Pruebas")
    comprobaciones = 0
    rng = random.Random(2026)

    # (a) la rejilla contra el oráculo, con muchos repetidos, pocos y ninguno
    for _ in range(10_000):
        n = rng.randint(2, 120)
        xs = [rng.randrange(rng.choice([50, 10**4, 10**9])) for _ in range(n)]
        assert Rejilla().resolver(xs, semilla=rng.randrange(10**9)) == ordenando(xs)
        comprobaciones += 1

    # (b) la reducción: distinción de elementos sale del par más cercano
    for _ in range(10_000):
        xs = [rng.randrange(60) for _ in range(rng.randint(2, 12))]
        assert distincion(xs) == (len(set(xs)) < len(xs))
        comprobaciones += 1

    # (c) el orden adversario reconstruye en cada punto
    for n in range(3, 200):
        r = Rejilla()
        r.resolver(adversaria(n), permutar=False)
        assert r.reconstrucciones == n - 2
        comprobaciones += 1

    print(f"{miles(comprobaciones)} comprobaciones, 0 fallos")


# --------------------------------------------------------------------------
# 4. Figuras
# --------------------------------------------------------------------------

TINTA, APAGADO, REGLA = "#1a1a1a", "#6b7280", "#d8dce3"
ACENTO, OSCURO, CALIDO, ALARMA = "#0891b2", "#0e7490", "#b45309", "#be123c"


def _estilo():
    plt.rcParams.update({
        "font.size": 9, "axes.edgecolor": APAGADO, "axes.labelcolor": TINTA,
        "xtick.color": APAGADO, "ytick.color": APAGADO,
        "figure.facecolor": "white", "svg.hashsalt": "ejercicio-10",
    })


def _guardar(fig, nombre):
    fig.tight_layout()
    fig.savefig(nombre, metadata={"Date": None})
    plt.close(fig)


def figura_rejilla():
    # buscar una instantánea que ilustre: delta >= 8 y al menos tres celdas ocupadas
    # cerca del punto que se inserta (la búsqueda es determinista)
    rng = random.Random(10)
    xs = rng.sample(range(3000), 120)
    for semilla in range(500):
        for paso in range(10, len(xs), 7):
            r = Rejilla()
            r.resolver(xs, semilla=semilla, foto_en=paso)
            if r.foto is None:
                continue
            tabla, d, p = r.foto
            c = p // d
            cerca = sum(1 for k in range(c - 4, c + 5) if k in tabla)
            if d >= 8 and cerca >= 3:
                break
        else:
            continue
        break
    c = p // d
    lo, hi = (c - 4) * d, (c + 5) * d
    fig, ax = plt.subplots(figsize=(6.8, 1.9))
    for k in range(c - 4, c + 5):
        en_uso = k in (c - 1, c, c + 1)
        ax.add_patch(plt.Rectangle((k * d, -0.3), d, 0.6,
                                   facecolor="#ecfeff" if en_uso else "white",
                                   edgecolor=REGLA, lw=0.8))
    for k, q in tabla.items():
        if lo <= q < hi:
            ax.plot([q], [0], "o", color=OSCURO, ms=6)
    ax.plot([p], [0], "o", color=ALARMA, ms=7)
    ax.text(p, 0.45, "p", ha="center", color=ALARMA, fontsize=9)
    ax.annotate("", ((c - 1) * d, -0.5), ((c + 2) * d, -0.5),
                arrowprops={"arrowstyle": "<->", "color": ACENTO, "lw": 1})
    ax.text((c + 0.5) * d, -0.8, "las tres celdas que se consultan", ha="center",
            color=ACENTO, fontsize=8)
    ax.text(lo, 0.45, f"δ = {d}", color=APAGADO, fontsize=8)
    ax.set_xlim(lo - 2, hi + 2)
    ax.set_ylim(-1.0, 0.8)
    ax.axis("off")
    _guardar(fig, "ejercicio-10-rejilla.svg")
    return d, len(tabla)


def figura_trabajo(filas):
    fig, ax = plt.subplots(figsize=(6.4, 3.0))
    ns = [n for n, _, _ in filas]
    ax.plot(ns, [a for _, a, _ in filas], "o-", color=ALARMA, lw=1.5,
            label="en el orden adversario")
    ax.plot(ns, [b for _, _, b in filas], "o-", color=OSCURO, lw=1.5,
            label="permutado al azar")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("n")
    ax.set_ylabel("trabajo por punto")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(color=REGLA, lw=0.6)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    _guardar(fig, "ejercicio-10-trabajo.svg")


if __name__ == "__main__":
    reduccion()
    correctitud()
    reconstrucciones()
    filas = sin_permutar()
    errores_plantados()
    pruebas()
    _estilo()
    d, ocupadas = figura_rejilla()
    figura_trabajo(filas)
    print(f"\nla figura de la rejilla: delta = {d}, {ocupadas} celdas ocupadas")
    print("figuras: ejercicio-10-rejilla.svg, ejercicio-10-trabajo.svg")
