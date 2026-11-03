"""Ejercicio 13 del Tema 1: un splay tree que empieza como un camino, accedido en orden.

    python ejercicio-13.py

Imprime todas las tablas que cita ejercicio-13.md, corre las pruebas y regenera las
tres figuras (ejercicio-13-mitad.svg, ejercicio-13-acumulado.svg y
ejercicio-13-cota.svg). Cada número que aparece en la prosa sale de aquí. Solo
necesita matplotlib.
"""

import math
import random

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt


# --------------------------------------------------------------------------
# 1. El splay tree
# --------------------------------------------------------------------------

class Nodo:
    def __init__(self, clave):
        self.clave, self.izq, self.der, self.padre = clave, None, None, None


def rotar(x):
    """Sube x un nivel rotando la arista con su padre. Preserva el orden."""
    p, g = x.padre, x.padre.padre
    if p.izq is x:
        p.izq, x.der = x.der, p
        if p.izq:
            p.izq.padre = p
    else:
        p.der, x.izq = x.izq, p
        if p.der:
            p.der.padre = p
    p.padre, x.padre = x, g
    if g:
        if g.izq is p:
            g.izq = x
        else:
            g.der = x


def splay(x):
    rotaciones = 0
    while x.padre:
        p, g = x.padre, x.padre.padre
        if g is None:                                  # zig
            rotar(x)
            rotaciones += 1
        elif (g.izq is p) == (p.izq is x):             # zig-zig: primero el padre
            rotar(p)
            rotar(x)
            rotaciones += 2
        else:                                          # zig-zag
            rotar(x)
            rotar(x)
            rotaciones += 2
    return rotaciones


def buscar(raiz, clave):
    x = raiz
    while x.clave != clave:
        x = x.izq if clave < x.clave else x.der
    return x


def camino(n):
    """n en la raíz, cada clave hija izquierda de la siguiente."""
    nodos = [Nodo(k) for k in range(1, n + 1)]
    for k in range(1, n):
        nodos[k].izq, nodos[k - 1].padre = nodos[k - 1], nodos[k]
    return nodos[-1]


def tamanos(raiz):
    """s(x) de cada nodo, sin recursión (los caminos tienen miles de niveles)."""
    orden, pila = [], [raiz]
    while pila:
        x = pila.pop()
        if x:
            orden.append(x)
            pila += [x.izq, x.der]
    s = {}
    for x in reversed(orden):
        s[x] = 1 + s.get(x.izq, 0) + s.get(x.der, 0)
    return s


def potencial(raiz):
    return sum(math.log2(v) for v in tamanos(raiz).values())


def es_camino(raiz, n):
    x, k = raiz, n
    while x:
        if x.clave != k or x.der:
            return False
        x, k = x.izq, k - 1
    return k == 0


def rama_izquierda_ok(raiz):
    """El invariante (C): la raíz es i y su subárbol izquierdo es el camino i-1, ..., 1,
    sin hijos derechos."""
    x, k = raiz.izq, raiz.clave - 1
    while x:
        if x.clave != k or x.der:
            return False
        x, k = x.izq, k - 1
    return k == 0


def ronda(raiz, claves, vigilar=False, medir=False):
    """Accede a las claves en el orden dado. Devuelve la raíz final y, por acceso,
    (costo real, potencial antes, potencial después, rango de x antes)."""
    filas = []
    for clave in claves:
        x = buscar(raiz, clave)
        if medir:
            s = tamanos(raiz)
            antes, r_x = sum(math.log2(v) for v in s.values()), math.log2(s[x])
        costo = max(splay(x), 1)
        raiz = x
        if vigilar:
            assert rama_izquierda_ok(raiz)
        if medir:
            filas.append((costo, antes, potencial(raiz), r_x))
        else:
            filas.append((costo,))
    return raiz, filas


def cota_seccion_5(n, m):
    """La cuenta que suma los costos amortizados y paga el potencial inicial aparte:
    m (3 log2 n + 1) + log2 n!  (el potencial de un camino)."""
    return m * (3 * math.log2(n) + 1) + math.lgamma(n + 1) / math.log(2)


def seccion(titulo):
    print()
    print(titulo)
    print("-" * len(titulo))


def miles(x):
    return f"{x:,}".replace(",", " ")


# --------------------------------------------------------------------------
# 2. Las tablas que cita la prosa
# --------------------------------------------------------------------------

def ejemplo_chico():
    seccion("§2. Ejemplo chico: un camino de 16 nodos, claves 1 a 16 en orden")
    n = 16
    raiz, filas = ronda(camino(n), range(1, n + 1))
    costos = [f[0] for f in filas]
    print("costo de cada acceso:", " ".join(map(str, costos)))
    print(f"total {sum(costos)}, {sum(costos) / n:.2f} por acceso; "
          f"al terminar, el árbol es otra vez el camino: {es_camino(raiz, n)}")
    raiz, filas2 = ronda(raiz, range(1, n + 1))
    print(f"segunda ronda: {' '.join(str(f[0]) for f in filas2)}")


def cota_contra_medida():
    seccion("§3. La cota del lema de acceso contra lo que se mide")
    print(f"{'n':>6} {'medido':>9} {'cota':>9} {'cota / medido':>14} {'medido / n':>11}")
    for n in [100, 200, 400, 800, 1600, 3200]:
        _, filas = ronda(camino(n), range(1, n + 1))
        real = sum(f[0] for f in filas)
        cota = cota_seccion_5(n, n)
        print(f"{n:>6} {miles(real):>9} {miles(round(cota)):>9} {cota / real:>14.1f} "
              f"{real / n:>11.2f}")


def tres_rondas():
    seccion("§4. Tres rondas, como el experimento que recorre las claves en orden")
    print(f"{'n':>6} {'ronda 1':>8} {'ronda 2':>8} {'ronda 3':>8} {'por acceso':>11} "
          f"{'camino al final de cada ronda':>30}")
    for n in [100, 200, 400, 800]:
        raiz, totales, caminos = camino(n), [], []
        for _ in range(3):
            raiz, filas = ronda(raiz, range(1, n + 1), vigilar=True)
            totales.append(sum(f[0] for f in filas))
            caminos.append(es_camino(raiz, n))
        print(f"{n:>6} {totales[0]:>8} {totales[1]:>8} {totales[2]:>8} "
              f"{sum(totales) / (3 * n):>11.2f} {str(caminos):>30}")


def desglose():
    seccion("§5. Dónde pierde la cota, acceso por acceso")
    n = 64
    raiz, filas = ronda(camino(n), range(1, n + 1), medir=True)
    real = [c for c, _, _, _ in filas]
    amortizado = [c + despues - antes for c, antes, despues, _ in filas]
    lema = [3 * (math.log2(n) - r_x) + 1 for _, _, _, r_x in filas]
    violaciones = sum(a > l + 1e-9 for a, l in zip(amortizado, lema))
    phi0, phin = filas[0][1], filas[-1][2]
    print(f"n = {n}: potencial al empezar {phi0:.1f}, al terminar {phin:.1f}")
    print(f"primer acceso: real {real[0]}, amortizado {amortizado[0]:.1f}, "
          f"lema {lema[0]:.1f}")
    print(f"accesos 2 a {n}: real {sum(real[1:])}, amortizado {sum(amortizado[1:]):.1f}, "
          f"lema {sum(lema[1:]):.1f}")
    print(f"total: real {sum(real)}, amortizado {sum(amortizado):.1f}, "
          f"lema {sum(lema):.1f}; la cota del lema falla en {violaciones} de {n} accesos")
    pequenos = sum(1 for _, _, _, r_x in filas if 2 ** r_x <= 3 + 1e-9)
    print(f"accesos en que el nodo tenía un subárbol de a lo sumo 3 nodos: {pequenos} de {n}")
    print(f"a cada uno, el lema le cobra al menos 3 (log2 n - log2 3) + 1 = "
          f"{3 * (math.log2(n) - math.log2(3)) + 1:.1f}")
    print(f"la cuenta completa: n (3 log2 n + 1) + log2 n! = "
          f"{n * (3 * math.log2(n) + 1):.0f} + {phi0:.0f} = {cota_seccion_5(n, n):.0f}")
    phi = [phi0] + [despues for _, _, despues, _ in filas]
    return real, amortizado, lema, phi


def sin_potencial_inicial():
    seccion("§6. El error en la cuenta: olvidar el potencial inicial")
    n = 1024
    raiz = camino(n)
    print(f"{'accesos':>8} {'costo real':>11} {'i (3 log2 n + 1)':>17} "
          f"{'+ Φ0 - Φi':>10}")
    phi0 = potencial(raiz)
    acumulado = 0
    marcas = {1, 2, 4, 16, 64, 256, 1024}
    for i in range(1, n + 1):
        x = buscar(raiz, i)
        acumulado += max(splay(x), 1)
        raiz = x
        if i in marcas:
            sin = i * (3 * math.log2(n) + 1)
            con = sin + phi0 - potencial(raiz)
            print(f"{i:>8} {miles(acumulado):>11} {miles(round(sin)):>17} "
                  f"{miles(round(con)):>10}")


def otras_secuencias():
    seccion("§7. ¿Es ajustada? Otras secuencias de n accesos desde el mismo camino")
    rng = random.Random(8)
    print(f"{'n':>6} {'en orden':>9} {'al azar':>9} {'cota mínima al azar':>20} "
          f"{'cota del lema':>14}   (por acceso)")
    curvas = {"en orden": [], "al azar": [], "cota mínima al azar": [],
              "cota del lema": []}
    for n in [64, 256, 1024, 4096, 16384]:
        _, filas = ronda(camino(n), range(1, n + 1))
        orden = sum(f[0] for f in filas) / n
        azar = []
        for _ in range(3):
            _, filas = ronda(camino(n), [rng.randint(1, n) for _ in range(n)])
            azar.append(sum(f[0] for f in filas) / n)
        azar = sum(azar) / 3
        minima = (math.floor(math.log2(n)) - 1) / 2
        lema = cota_seccion_5(n, n) / n
        for k, v in zip(curvas, [orden, azar, minima, lema]):
            curvas[k].append((n, v))
        print(f"{n:>6} {orden:>9.2f} {azar:>9.2f} {minima:>20.1f} {lema:>14.1f}")
    return curvas


def pruebas():
    seccion("Pruebas")
    comprobaciones = 0
    rng = random.Random(2026)

    # (a) el lema de acceso, acceso por acceso, en orden y al azar
    for n in [5, 17, 50, 120]:
        for claves in [range(1, n + 1), [rng.randint(1, n) for _ in range(2 * n)]]:
            _, filas = ronda(camino(n), claves, medir=True)
            for c, antes, despues, r_x in filas:
                assert c + despues - antes <= 3 * (math.log2(n) - r_x) + 1 + 1e-9
                comprobaciones += 1

    # (b) el invariante (C) y el regreso al camino, para todo n hasta 300
    for n in range(1, 301):
        raiz, filas = ronda(camino(n), range(1, n + 1), vigilar=True)
        assert es_camino(raiz, n)
        assert sum(f[0] for f in filas) <= cota_seccion_5(n, n)
        comprobaciones += len(filas) + 2

    # (c) el splay preserva el orden: el recorrido en orden sigue siendo 1..n
    for _ in range(200):
        n = rng.randint(1, 60)
        raiz, _ = ronda(camino(n), [rng.randint(1, n) for _ in range(n)])
        claves, pila, x = [], [], raiz
        while pila or x:
            while x:
                pila.append(x)
                x = x.izq
            x = pila.pop()
            claves.append(x.clave)
            x = x.der
        assert claves == list(range(1, n + 1))
        comprobaciones += 1

    print(f"{miles(comprobaciones)} comprobaciones, 0 fallos")


# --------------------------------------------------------------------------
# 3. Figuras
# --------------------------------------------------------------------------

TINTA, APAGADO, REGLA = "#1a1a1a", "#6b7280", "#d8dce3"
ACENTO, OSCURO, CALIDO, ALARMA = "#0891b2", "#0e7490", "#b45309", "#be123c"


def _estilo():
    plt.rcParams.update({
        "font.size": 9, "axes.edgecolor": APAGADO, "axes.labelcolor": TINTA,
        "xtick.color": APAGADO, "ytick.color": APAGADO,
        "figure.facecolor": "white", "svg.hashsalt": "ejercicio-13",
    })


def _guardar(fig, nombre):
    fig.tight_layout()
    fig.savefig(nombre, metadata={"Date": None})
    plt.close(fig)


def _dibujar(ax, raiz, siguiente, titulo):
    """Cada nodo en x = clave, y = -profundidad. En rojo, el camino de acceso a la
    clave siguiente."""
    pos, pila = {}, [(raiz, 0)]
    while pila:
        x, d = pila.pop()
        if x:
            pos[x] = (x.clave, -d)
            pila += [(x.izq, d + 1), (x.der, d + 1)]
    en_camino = set()
    x = buscar(raiz, siguiente)
    while x:
        en_camino.add(x)
        x = x.padre
    for x, (px, py) in pos.items():
        for h in (x.izq, x.der):
            if h:
                rojo = x in en_camino and h in en_camino
                ax.plot([px, pos[h][0]], [py, pos[h][1]], color=ALARMA if rojo else REGLA,
                        lw=1.8 if rojo else 1.0, zorder=1)
    for x, (px, py) in pos.items():
        ax.scatter([px], [py], s=95, color="white", zorder=2,
                   edgecolors=ALARMA if x in en_camino else OSCURO, linewidths=1.2)
        ax.text(px, py, str(x.clave), ha="center", va="center", fontsize=6, zorder=3)
    ax.set_title(titulo, fontsize=8, color=TINTA)
    ax.set_ylim(-16, 1)
    ax.set_xlim(0, 17)
    ax.axis("off")


def figura_mitad():
    n = 16
    raiz = camino(n)
    fig, ejes = plt.subplots(1, 3, figsize=(7.2, 3.6))
    for k, eje in enumerate(ejes):
        siguiente = k + 1
        x, prof = buscar(raiz, siguiente), 0
        while x.padre:
            prof, x = prof + 1, x.padre
        estado = "el camino inicial" if k == 0 else f"después de acceder a {k}"
        _dibujar(eje, raiz, siguiente, f"{estado}\n{siguiente} está a profundidad {prof}")
        x = buscar(raiz, siguiente)
        splay(x)
        raiz = x
    _guardar(fig, "ejercicio-13-mitad.svg")


def figura_acumulado(real, amortizado, lema, phi):
    """Sumas acumuladas después de i accesos. phi[i] es el potencial después del
    acceso i, y phi[0] el del camino."""
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    i = list(range(1, len(real) + 1))

    def acumular(xs):
        total, res = 0, []
        for x in xs:
            total += x
            res.append(total)
        return res

    suma_lema = acumular(lema)
    ax.plot(i, acumular(real), color=OSCURO, lw=2, label="costo real")
    ax.plot(i, acumular(amortizado), color=CALIDO, lw=1.4, label="costo amortizado")
    ax.plot(i, suma_lema, color=ALARMA, lw=1.2, ls=":",
            label="suma de las cotas del lema")
    ax.plot(i, [s + phi[0] - phi[k] for k, s in zip(i, suma_lema)], color=ALARMA, lw=1.4,
            label="suma de las cotas + Φ₀ − Φᵢ")
    ax.axhline(0, color=APAGADO, lw=0.8)
    ax.set_xlabel("accesos hechos (claves 1 a i)")
    ax.set_ylabel("rotaciones acumuladas")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(color=REGLA, lw=0.6)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    _guardar(fig, "ejercicio-13-acumulado.svg")


def figura_cota(curvas):
    fig, ax = plt.subplots(figsize=(6.0, 3.0))
    estilos = {"en orden": (OSCURO, "o-"), "al azar": (CALIDO, "o-"),
               "cota mínima al azar": (CALIDO, ":"), "cota del lema": (ALARMA, "--")}
    for nombre, pts in curvas.items():
        color, est = estilos[nombre]
        ax.plot([n for n, _ in pts], [v for _, v in pts], est, color=color, lw=1.4,
                ms=3.5, label=nombre)
    ax.set_xscale("log", base=2)
    ax.set_xlabel("n")
    ax.set_ylabel("rotaciones por acceso")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(color=REGLA, lw=0.6)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    _guardar(fig, "ejercicio-13-cota.svg")


if __name__ == "__main__":
    ejemplo_chico()
    cota_contra_medida()
    tres_rondas()
    real, amortizado, lema, phi = desglose()
    sin_potencial_inicial()
    curvas = otras_secuencias()
    pruebas()
    _estilo()
    figura_mitad()
    figura_acumulado(real, amortizado, lema, phi)
    figura_cota(curvas)
    print("\nfiguras: ejercicio-13-mitad.svg, ejercicio-13-acumulado.svg, "
          "ejercicio-13-cota.svg")
