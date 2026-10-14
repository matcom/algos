"""Ejercicio 3 del Tema 1: una pila con mínimo en O(1) en el peor caso.

Uso:
    python ejercicio_03.py             imprime las tablas del informe
    python ejercicio_03.py --figuras   además regenera las figuras

Las pruebas están en test_ejercicio_03.py.
"""

import math
import random
import sys
from pathlib import Path


class Contador:
    """Cuenta comparaciones entre elementos, para medir el costo por operación."""

    def __init__(self):
        self.total = 0

    def menor_o_igual(self, a, b):
        self.total += 1
        return a <= b

    def igual(self, a, b):
        self.total += 1
        return a == b


# ---------------------------------------------------------------------------
# 1. La estructura: cada entrada guarda su valor y el mínimo del prefijo
# ---------------------------------------------------------------------------

class PilaMin:
    """Pila de pares (x, m), donde m es el mínimo de los elementos hasta x inclusive."""

    def __init__(self, contador=None):
        self.datos = []
        self.contador = contador or Contador()

    def apilar(self, x):
        if not self.datos or self.contador.menor_o_igual(x, self.datos[-1][1]):
            self.datos.append((x, x))
        else:
            self.datos.append((x, self.datos[-1][1]))

    def desapilar(self):
        if not self.datos:
            raise IndexError("desapilar de una pila vacía")
        return self.datos.pop()[0]

    def tope(self):
        if not self.datos:
            raise IndexError("tope de una pila vacía")
        return self.datos[-1][0]

    def minimo(self):
        if not self.datos:
            raise IndexError("mínimo de una pila vacía")
        return self.datos[-1][1]

    def __len__(self):
        return len(self.datos)

    def vigilar(self):
        """El invariante: m_k = min(x_1, ..., x_k) para toda posición k."""
        prefijo = None
        for x, m in self.datos:
            prefijo = x if prefijo is None else min(prefijo, x)
            assert m == prefijo


class PilaMinCompacta:
    """Dos pilas: los datos y los récords (débiles) del mínimo.

    `minimos` guarda, en orden, los x que al apilarse eran <= que todos los de
    debajo. Con estricta=True usa < en lugar de <=: es el error plantado.
    """

    def __init__(self, estricta=False, contador=None):
        self.datos = []
        self.minimos = []
        self.estricta = estricta
        self.contador = contador or Contador()

    def apilar(self, x):
        self.datos.append(x)
        if not self.minimos:
            self.minimos.append(x)
        elif self.estricta:
            self.contador.total += 1
            if x < self.minimos[-1]:
                self.minimos.append(x)
        elif self.contador.menor_o_igual(x, self.minimos[-1]):
            self.minimos.append(x)

    def desapilar(self):
        if not self.datos:
            raise IndexError("desapilar de una pila vacía")
        x = self.datos.pop()
        if self.contador.igual(x, self.minimos[-1]):     # una comparación por desapilar
            self.minimos.pop()
        return x

    def tope(self):
        if not self.datos:
            raise IndexError("tope de una pila vacía")
        return self.datos[-1]

    def minimo(self):
        if not self.datos:
            raise IndexError("mínimo de una pila vacía")
        return self.minimos[-1]

    def __len__(self):
        return len(self.datos)

    def memoria(self):
        return len(self.datos) + len(self.minimos)

    def vigilar(self):
        """minimos = los récords débiles de datos, en orden."""
        records = []
        for x in self.datos:
            if not records or x <= records[-1]:
                records.append(x)
        assert self.minimos == records


class PilaMinCodificada:
    """Variante con O(1) memoria extra para enteros: guarda 2x - min cuando x es un récord.

    No es del modelo de comparaciones (usa aritmética), y 2x - min puede necesitar
    un bit más que x.
    """

    def __init__(self):
        self.datos = []
        self.min = None

    def apilar(self, x):
        if not self.datos:
            self.datos.append(x)
            self.min = x
        elif x < self.min:
            self.datos.append(2 * x - self.min)   # menor que el x nuevo: marca un récord
            self.min = x
        else:
            self.datos.append(x)

    def desapilar(self):
        y = self.datos.pop()
        if y < self.min:                           # era un récord: recuperar el mínimo anterior
            x, self.min = self.min, 2 * self.min - y
            return x
        if not self.datos:
            self.min = None
        return y

    def tope(self):
        y = self.datos[-1]
        return self.min if y < self.min else y

    def minimo(self):
        return self.min

    def __len__(self):
        return len(self.datos)


class ColaMin:
    """Cola con mínimo hecha con dos PilaMin: O(1) amortizado (conferencia 4)."""

    def __init__(self):
        self.entrada = PilaMin()
        self.salida = PilaMin()
        self.mudanzas = 0

    def encolar(self, x):
        self.entrada.apilar(x)

    def desencolar(self):
        if not len(self.salida):
            while len(self.entrada):
                self.salida.apilar(self.entrada.desapilar())
                self.mudanzas += 1
        return self.salida.desapilar()

    def minimo(self):
        candidatos = [p.minimo() for p in (self.entrada, self.salida) if len(p)]
        if not candidatos:
            raise IndexError("mínimo de una cola vacía")
        return min(candidatos)

    def __len__(self):
        return len(self.entrada) + len(self.salida)


# ---------------------------------------------------------------------------
# 2. Oráculo y secuencias de operaciones
# ---------------------------------------------------------------------------

def secuencia(rng, largo, valores):
    """Operaciones al azar: apilar con valores de `valores`, desapilar o consultar."""
    ops = []
    tamano = 0
    for _ in range(largo):
        r = rng.random()
        if tamano == 0 or r < 0.45:
            ops.append(("apilar", valores(rng)))
            tamano += 1
        elif r < 0.75:
            ops.append(("desapilar", None))
            tamano -= 1
        elif r < 0.9:
            ops.append(("minimo", None))
        else:
            ops.append(("tope", None))
    return ops


def ejecutar(pila, ops, vigilar=False):
    """Ejecuta las operaciones y devuelve la lista de respuestas.

    Si la estructura revienta (la versión con error puede vaciar `minimos`
    antes de tiempo), la respuesta termina en "excepción".
    """
    salida = []
    for op, x in ops:
        try:
            if op == "apilar":
                pila.apilar(x)
                salida.append(None)
            else:
                salida.append(getattr(pila, op)())
        except IndexError:
            salida.append("excepción")
            return salida
        if vigilar and hasattr(pila, "vigilar"):
            pila.vigilar()
    return salida


class Oraculo:
    """Una lista y min(): obviamente correcta, O(n) por mínimo."""

    def __init__(self):
        self.datos = []

    def apilar(self, x):
        self.datos.append(x)

    def desapilar(self):
        return self.datos.pop()

    def tope(self):
        return self.datos[-1]

    def minimo(self):
        return min(self.datos)


GENERADORES = {
    "distintos": lambda rng: rng.random(),
    "enteros de 0 a 10⁶": lambda rng: rng.randrange(10**6),
    "enteros de 0 a 100": lambda rng: rng.randrange(100),
    "enteros de 0 a 4": lambda rng: rng.randrange(5),
}


def tasas_de_fallo(casos=3000, largo=40, semilla=3):
    rng = random.Random(semilla)
    filas = []
    for nombre, valores in GENERADORES.items():
        fallos_estricta = fallos_correcta = 0
        for _ in range(casos):
            ops = secuencia(rng, largo, valores)
            esperado = ejecutar(Oraculo(), ops)
            fallos_estricta += ejecutar(PilaMinCompacta(estricta=True), ops) != esperado
            fallos_correcta += ejecutar(PilaMinCompacta(), ops) != esperado
        filas.append((nombre, 100 * fallos_estricta / casos, 100 * fallos_correcta / casos))
    return filas


def contraejemplo_minimo():
    """La secuencia más corta que distingue < de <=, por búsqueda exhaustiva."""
    for largo in range(1, 7):
        for ops in _todas_las_secuencias(largo, valores=[1, 2]):
            if ejecutar(PilaMinCompacta(estricta=True), ops) != ejecutar(Oraculo(), ops):
                return ops
    return None


def _todas_las_secuencias(largo, valores):
    def extender(prefijo, tamano):
        if len(prefijo) == largo:
            yield list(prefijo)
            return
        for v in valores:
            yield from extender(prefijo + [("apilar", v)], tamano + 1)
        if tamano:
            for op in ("desapilar", "minimo"):
                yield from extender(prefijo + [(op, None)], tamano - 1 if op == "desapilar" else tamano)
    yield from extender([], 0)


def records_esperados(n):
    """H_n: récords esperados de una permutación al azar."""
    return sum(1 / k for k in range(1, n + 1))


# ---------------------------------------------------------------------------
# 3. Tablas
# ---------------------------------------------------------------------------

def tabla_traza():
    print("Tabla 1. Traza de PilaMin")
    pila = PilaMin()
    ops = [("apilar", 5), ("apilar", 7), ("apilar", 3), ("apilar", 3), ("apilar", 8),
           ("minimo", None), ("desapilar", None), ("desapilar", None), ("minimo", None),
           ("desapilar", None), ("minimo", None)]
    for op, x in ops:
        r = pila.apilar(x) if op == "apilar" else getattr(pila, op)()
        print(f"  {op:>10} {'' if x is None else x:>3} -> {'' if r is None else r:>3}   pila: {pila.datos}")
    print()


def tabla_costo():
    print("Tabla 2. Comparaciones en la peor llamada de cada operación, en 10^5 operaciones al azar")
    rng = random.Random(4)
    for nombre, clase in [("PilaMin", PilaMin), ("PilaMinCompacta", PilaMinCompacta)]:
        contador = Contador()
        pila = clase(contador=contador)
        peor = dict.fromkeys(["apilar", "desapilar", "tope", "minimo"], 0)
        for op, x in secuencia(rng, 10**5, GENERADORES["enteros de 0 a 100"]):
            antes = contador.total
            if op == "apilar":
                pila.apilar(x)
            else:
                getattr(pila, op)()
            peor[op] = max(peor[op], contador.total - antes)
        print(f"  {nombre:>16}: " + ", ".join(f"{op} {k}" for op, k in peor.items()))
    print()


def tabla_memoria():
    print("Tabla 3. Memoria de la versión compacta tras apilar n distintos al azar")
    print(f"{'n':>8} {'récords (media de 200)':>23} {'H_n':>7} {'memoria / n':>12}")
    rng = random.Random(5)
    for n in [10, 100, 1000, 10000]:
        total = 0
        for _ in range(200):
            pila = PilaMinCompacta()
            for x in rng.sample(range(10 * n), n):
                pila.apilar(x)
            total += len(pila.minimos)
        media = total / 200
        print(f"{n:>8} {media:>23.2f} {records_esperados(n):>7.2f} {(n + media) / n:>12.4f}")
    print("  peor caso (apilar n, n-1, ..., 1): memoria 2n")
    print()


def tabla_fallos(filas):
    print("Tabla 4. Porcentaje de secuencias de 40 operaciones donde la versión falla")
    print(f"{'generador':>22} {'< (error)':>10} {'<= (correcta)':>14}")
    for nombre, mal, bien in filas:
        print(f"{nombre:>22} {mal:>9.1f}% {bien:>13.1f}%")
    print()


# ---------------------------------------------------------------------------
# 4. Figuras
# ---------------------------------------------------------------------------

AZUL, NARANJA, AQUA, AMARILLO = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
TINTA, TINTA_2, TENUE, REJILLA, SUPERFICIE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"


def _estilo(plt):
    plt.rcParams.update({
        "font.family": ["Segoe UI", "DejaVu Sans"], "font.size": 10,
        "axes.edgecolor": "#c3c2b7", "axes.labelcolor": TINTA_2, "axes.titlecolor": TINTA,
        "axes.titlesize": 12, "axes.titleweight": "bold", "axes.titlelocation": "left",
        "axes.facecolor": SUPERFICIE, "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.color": REJILLA, "grid.linewidth": 0.6,
        "xtick.color": TENUE, "ytick.color": TENUE, "xtick.labelcolor": TINTA_2,
        "ytick.labelcolor": TINTA_2, "figure.facecolor": SUPERFICIE, "legend.frameon": False,
        "legend.labelcolor": TINTA_2, "lines.linewidth": 2, "savefig.dpi": 150,
        "savefig.bbox": "tight",
    })


def figura_traza(plt, destino):
    import matplotlib.patches as patches

    ops = [("apilar", 5), ("apilar", 7), ("apilar", 3), ("apilar", 3), ("apilar", 8),
           ("desapilar", None), ("desapilar", None), ("desapilar", None)]
    pila = PilaMin()
    compacta = PilaMinCompacta(estricta=True)
    estados = []
    for op, x in ops:
        if op == "apilar":
            pila.apilar(x)
            compacta.apilar(x)
        else:
            pila.desapilar()
            compacta.desapilar()
        estados.append((op, x, list(pila.datos), compacta.minimo() if len(compacta) else None))
    fig, ax = plt.subplots(figsize=(9.4, 4.0))
    ax.axis("off")
    for col, (op, x, datos, min_mal) in enumerate(estados):
        cx = col * 1.15
        ax.text(cx + 0.45, -0.75, f"{op}\n{x if x is not None else ''}", ha="center", va="top",
                fontsize=8.5, color=TINTA_2)
        for fila, (v, m) in enumerate(datos):
            ax.add_patch(patches.Rectangle((cx, fila * 0.62), 0.9, 0.55, facecolor=SUPERFICIE,
                                           edgecolor="#c3c2b7", linewidth=0.8))
            ax.text(cx + 0.25, fila * 0.62 + 0.27, str(v), ha="center", va="center", fontsize=10,
                    color=TINTA)
            ax.text(cx + 0.66, fila * 0.62 + 0.27, str(m), ha="center", va="center", fontsize=10,
                    color=AZUL, fontweight="bold")
        if datos:
            correcto = datos[-1][1]
            ax.text(cx + 0.45, 3.45, f"mín {correcto}", ha="center", fontsize=9, color=AZUL)
            color = NARANJA if min_mal != correcto else TINTA_2
            ax.text(cx + 0.45, 3.15, f"con <: {min_mal}", ha="center", fontsize=9, color=color,
                    fontweight="bold" if min_mal != correcto else "normal")
    ax.text(-0.1, 3.85, "Cada caja: valor (negro) y mínimo del prefijo (azul). Abajo, la operación.",
            fontsize=9, color=TINTA_2)
    ax.set_xlim(-0.2, len(estados) * 1.15)
    ax.set_ylim(-1.5, 4.1)
    ax.set_title("La pila de pares, y la versión compacta con < que pierde el 3 repetido")
    fig.savefig(destino / "ejercicio-03-traza.png")
    plt.close(fig)


def figura_fallos(plt, destino, filas):
    fig, ax = plt.subplots(figsize=(8, 3.8))
    nombres = [f[0] for f in filas]
    vals = [f[1] for f in filas]
    barras = ax.bar(range(len(filas)), vals, 0.55, color=NARANJA, label="compacta con < (error)")
    for b, v in zip(barras, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 1.5, f"{v:.1f} %", ha="center", fontsize=9,
                color=TINTA_2)
    ax.set_xticks(range(len(filas)))
    ax.set_xticklabels(nombres)
    ax.set_ylim(0, 100)
    ax.set_ylabel("% de secuencias que fallan")
    ax.set_title("El error solo aparece cuando el mínimo se repite")
    fig.savefig(destino / "ejercicio-03-fallos.png")
    plt.close(fig)


def figuras(filas):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    _estilo(plt)
    destino = Path(__file__).resolve().parent.parent / "figuras"
    destino.mkdir(exist_ok=True)
    figura_traza(plt, destino)
    figura_fallos(plt, destino, filas)
    print(f"figuras escritas en {destino}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    tabla_traza()
    tabla_costo()
    tabla_memoria()
    filas = tasas_de_fallo()
    tabla_fallos(filas)
    print("Contraejemplo mínimo para la versión con <:", contraejemplo_minimo())
    if "--figuras" in sys.argv:
        figuras(filas)
