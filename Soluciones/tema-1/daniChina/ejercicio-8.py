"""
Ejercicio 8: elementos que aparecen mas de n/3 veces.

Problema: arreglo A de n elementos que solo se pueden comparar por igualdad.
Devolver todos los elementos que aparecen mas de n/3 veces (a lo sumo dos).
Se pide tiempo O(n) y memoria extra O(1).

Uso:
    python ejercicio8_un_tercio.py             # corre los experimentos
    python ejercicio8_un_tercio.py --figuras   # ademas genera png y gif
"""
import itertools
import random
import sys
from collections import Counter


# --------------------------------------------------------------------------
# 1. El algoritmo: Boyer-Moore con dos candidatos
# --------------------------------------------------------------------------
def primera_pasada(A):
    """Cancelar. Devuelve (c1, k1, c2, k2)."""
    c1, k1 = object(), 0        # centinelas distintos: c1 != c2 desde el principio
    c2, k2 = object(), 0
    for x in A:
        if x == c1:
            k1 += 1
        elif x == c2:
            k2 += 1
        elif k1 == 0:
            c1, k1 = x, 1
        elif k2 == 0:
            c2, k2 = x, 1
        else:                   # x distinto de c1 y de c2, y los dos contadores > 0
            k1 -= 1
            k2 -= 1
    return c1, k1, c2, k2


def mas_de_un_tercio(A):
    c1, k1, c2, k2 = primera_pasada(A)
    # segunda pasada: verificar
    return [c for c in (c1, c2) if 3 * A.count(c) > len(A)]


def mas_de_un_tercio_atajo(A):
    """El atajo: devolver los candidatos con contador positivo, sin verificar."""
    c1, k1, c2, k2 = primera_pasada(A)
    return [c for c, k in ((c1, k1), (c2, k2)) if k > 0]


def oraculo(A):
    """Cuenta todo (fuerza bruta)."""
    return sorted(x for x, k in Counter(A).items() if 3 * k > len(A))


# --------------------------------------------------------------------------
# 3. Experimentos
# --------------------------------------------------------------------------
def exp_traza():
    print("== Traza sobre el ejemplo del .md ==")
    A = list("BACBADBABC")
    c1, k1 = object(), 0
    c2, k2 = object(), 0
    nombre = lambda c, k: "-" if c is not None and not isinstance(c, str) else c
    print(f"A = {''.join(A)}, n = {len(A)}, n/3 = {len(A)/3:.2f}")
    print(f"{'i':>2} {'x':>2}  {'c1':>2} {'k1':>2} {'c2':>2} {'k2':>2}  que paso")
    for i, x in enumerate(A, start=1):
        if x == c1:
            k1 += 1; que = "x = c1: k1 sube"
        elif x == c2:
            k2 += 1; que = "x = c2: k2 sube"
        elif k1 == 0:
            c1, k1 = x, 1; que = "k1 = 0: x pasa a ser c1"
        elif k2 == 0:
            c2, k2 = x, 1; que = "k2 = 0: x pasa a ser c2"
        else:
            k1 -= 1; k2 -= 1; que = "trio (x, c1, c2): los dos bajan"
        print(f"{i:>2} {x:>2}  {nombre(c1, k1):>2} {k1:>2} {nombre(c2, k2):>2} {k2:>2}  {que}")
    print("resultado:", mas_de_un_tercio(A), " oraculo:", oraculo(A), "\n")


def exp_exhaustivo():
    print("== Todas las entradas de largo <= 8 sobre {A,B,C,D}: comparar con el oraculo ==")
    total = malos = mitad = 0
    for n in range(1, 9):
        for A in itertools.product("ABCD", repeat=n):
            A = list(A)
            total += 1
            malos += sorted(mas_de_un_tercio(A)) != oraculo(A)
            # la mitad buena del atajo: todo elemento > n/3 tiene contador positivo
            devueltos = mas_de_un_tercio_atajo(A)
            mitad += all(x in devueltos for x in oraculo(A))
    print(f"  entradas: {total}, fallos del algoritmo de dos pasadas: {malos}")
    print(f"  entradas donde todo elemento > n/3 tiene contador positivo: {mitad} de {total}\n")


def exp_atajo():
    print("== El atajo contra distintos generadores de pruebas (4000 arreglos de largo 1..15 cada uno) ==")

    def plantada(n):
        m = random.choice("ABCDE")
        A = [m] * (n // 3 + 1) + [random.choice("ABCDE") for _ in range(n - n // 3 - 1)]
        random.shuffle(A)
        return A

    def balanceados(n):                  # todo simbolo presente aparece mas de n/3 veces
        if n < 4:                        # con n < 4 no caben dos simbolos asi
            return ["A"] * n
        A = ["A"] * (n // 2) + ["B"] * (n - n // 2)
        random.shuffle(A)
        return A

    generadores = {
        "mayoria plantada":        plantada,
        "binario al azar":         lambda n: [random.choice("AB") for _ in range(n)],
        "3 simbolos":              lambda n: [random.choice("ABC") for _ in range(n)],
        "5 simbolos":              lambda n: [random.choice("ABCDE") for _ in range(n)],
        "un solo simbolo":         lambda n: ["A"] * n,
        "dos simbolos frecuentes":  balanceados,
    }
    random.seed(5)
    print(f"{'generador':>26} {'atajo':>8} {'dos pasadas':>12}")
    for nombre, generar in generadores.items():
        casos = [generar(random.randint(1, 15)) for _ in range(4000)]
        f_atajo = sum(sorted(mas_de_un_tercio_atajo(A)) != oraculo(A) for A in casos) / len(casos)
        f_bm = sum(sorted(mas_de_un_tercio(A)) != oraculo(A) for A in casos) / len(casos)
        print(f"{nombre:>26} {100 * f_atajo:>7.1f}% {100 * f_bm:>11.1f}%")
    print()
    print("  contraejemplo minimo del atajo: A B C D")
    A = list("ABCD")
    print(f"    atajo: {mas_de_un_tercio_atajo(A)}   verdad: {oraculo(A)}   (n/3 = {len(A)/3:.2f}, D aparece 1 vez)\n")


# --------------------------------------------------------------------------
# 4. Figuras: png y gif (necesita matplotlib y pillow)
# --------------------------------------------------------------------------
def traza_para_dibujar(A):
    """Devuelve una lista de estados, uno por paso, con los indices de cada grupo."""
    c1, k1, c2, k2 = None, 0, None, 0
    s1, s2, trios, estados = [], [], [], []
    for i, x in enumerate(A):
        if x == c1 and c1 is not None:
            k1 += 1; s1.append(i); que = f"x = {x} es c1: k1 sube a {k1}"
        elif x == c2 and c2 is not None:
            k2 += 1; s2.append(i); que = f"x = {x} es c2: k2 sube a {k2}"
        elif k1 == 0:
            c1, k1 = x, 1; s1 = [i]; que = f"k1 = 0: {x} pasa a ser c1"
        elif k2 == 0:
            c2, k2 = x, 1; s2 = [i]; que = f"k2 = 0: {x} pasa a ser c2"
        else:
            j1, j2 = s1.pop(), s2.pop()
            k1 -= 1; k2 -= 1
            trios.append((i, j1, j2)); que = f"{x} distinto de c1={c1} y c2={c2}: trio, k1={k1}, k2={k2}"
        estados.append(dict(i=i, que=que, c1=c1, k1=k1, c2=c2, k2=k2,
                            s1=list(s1), s2=list(s2), trios=list(trios)))
    return estados


def figuras():
    import io
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    from PIL import Image

    A = list("BACBADBABC")
    n = len(A)
    estados = traza_para_dibujar(A)
    PAL = ["#f4b183", "#ffd966", "#c5a3d9", "#f8cbad", "#b4c7e7"]
    AZUL, VERDE, VACIO = "#9dc3e6", "#a9d18e", "#f2f2f2"

    def dibujar(ax, est, inicio=False):
        ax.set_xlim(-0.2, n + 0.2); ax.set_ylim(-1.6, 1.6); ax.axis("off")
        color = {}
        if est:
            for j in est["s1"]: color[j] = AZUL
            for j in est["s2"]: color[j] = VERDE
            for t, tr in enumerate(est["trios"]):
                for j in tr: color[j] = PAL[t % len(PAL)]
        for j, x in enumerate(A):
            hecho = est is not None and j <= est["i"]
            c = color.get(j, VACIO) if hecho else "white"
            actual = est is not None and j == est["i"]
            ax.add_patch(Rectangle((j + 0.05, 0.0), 0.9, 0.9, fc=c, ec="#d95f02" if actual else "#333",
                                   lw=3 if actual else 1.2))
            ax.text(j + 0.5, 0.45, x, ha="center", va="center", fontsize=15)
            ax.text(j + 0.5, -0.2, str(j + 1), ha="center", fontsize=8, color="#777")
        if est is None:
            ax.set_title("Antes de empezar: c1 = -, k1 = 0, c2 = -, k2 = 0", loc="left", fontsize=11, family="monospace")
            return
        f = lambda c: "-" if c is None else c
        ax.set_title(est["que"], loc="left", fontsize=11, family="monospace")
        ax.text(0, -0.9, f"c1 = {f(est['c1'])}, k1 = {est['k1']}      c2 = {f(est['c2'])}, k2 = {est['k2']}",
                fontsize=12, family="monospace")
        ax.text(0, -1.35, f"ternas formadas: {len(est['trios'])}", fontsize=10, color="#444")

    leyenda = "azul: copias de c1  |  verde: copias de c2  |  otros colores: ternas de distintos  |  borde naranja: x actual"

    fig, ax = plt.subplots(figsize=(9, 3))
    dibujar(ax, estados[-1])
    ax.set_title("Final de la primera pasada sobre B A C B A D B A B C:  " + estados[-1]["que"], loc="left", fontsize=9, family="monospace")
    fig.text(0.5, 0.02, leyenda, ha="center", fontsize=8, color="#444")
    fig.tight_layout(rect=[0, 0.06, 1, 1])
    fig.savefig("un_tercio_final.png", dpi=110)
    plt.close(fig)

    frames = []
    for est in [None] + estados:
        fig, ax = plt.subplots(figsize=(9, 3))
        dibujar(ax, est)
        fig.text(0.5, 0.02, leyenda, ha="center", fontsize=8, color="#444")
        fig.tight_layout(rect=[0, 0.06, 1, 1])
        buf = io.BytesIO(); fig.savefig(buf, format="png", dpi=90); plt.close(fig)
        buf.seek(0); frames.append(Image.open(buf).convert("P", palette=Image.ADAPTIVE))
    frames[0].save("un_tercio_animacion.gif", save_all=True, append_images=frames[1:],
                   duration=1800, loop=0)
    print("figuras escritas: un_tercio_final.png, un_tercio_animacion.gif")


if __name__ == "__main__":
    exp_traza()
    exp_exhaustivo()
    exp_atajo()
    if "--figuras" in sys.argv:
        figuras()
