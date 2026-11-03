"""Ejercicio 5 del Tema 1: detección de ciclos con dos punteros (Floyd).

    python ejercicio-05.py

Imprime todas las tablas que cita ejercicio-05.md, corre las pruebas y regenera las
tres figuras (ejercicio-05-rho.svg, ejercicio-05-potencial.svg y
ejercicio-05-errores.svg). Cada número que aparece en la prosa sale de aquí. Solo
necesita matplotlib.
"""

import math
import random

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt


# --------------------------------------------------------------------------
# 1. Las listas y el algoritmo
# --------------------------------------------------------------------------

class Nodo:
    __slots__ = ("next", "indice", "value")

    def __init__(self, indice, value=None):
        self.next, self.indice, self.value = None, indice, value


def lista(mu, lam, valores=None):
    """Una lista de n = mu + lam nodos. Si lam = 0 no tiene ciclo y el último apunta a
    None. Si lam > 0, los mu primeros son la cola y el último apunta al nodo mu, así
    que el ciclo tiene lam nodos. Devuelve la cabeza (None si la lista es vacía)."""
    n = mu + lam
    nodos = [Nodo(i, None if valores is None else valores[i]) for i in range(n)]
    for i in range(n - 1):
        nodos[i].next = nodos[i + 1]
    if lam > 0:
        nodos[-1].next = nodos[mu]
    return nodos[0] if nodos else None


class Lector:
    """Sigue un puntero y cuenta cuántas veces se hizo: el costo en este modelo."""

    def __init__(self):
        self.lecturas = 0

    def __call__(self, nodo):
        self.lecturas += 1
        return nodo.next


def floyd(head, next_of):
    """Tortuga a velocidad 1, liebre a velocidad 2. Devuelve (respuesta, vueltas)."""
    t = h = head
    vueltas = 0
    while h is not None:
        h1 = next_of(h)
        if h1 is None:
            break
        h = next_of(h1)
        t = next_of(t)
        vueltas += 1
        if t is h:
            return "hay ciclo", vueltas
    return "no hay ciclo", vueltas


def k_estrella(mu, lam):
    # la primera vuelta k >= max(mu, 1) que es múltiplo de lam
    return lam * math.ceil(max(mu, 1) / lam)


def indice_real(i, mu, lam):
    # el nodo al que se llega después de i pasos desde la cabeza
    return i if i < mu + lam else mu + (i - mu) % lam


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
    seccion("§2. Ejemplo chico: cola de 3 nodos y ciclo de 5")
    mu, lam = 3, 5
    print(f"{'k':>2} {'tortuga en':>11} {'liebre en':>10} {'tortuga en el ciclo':>20} "
          f"{'D':>3} {'potencial':>10}")
    k = 0
    while True:
        t, h = indice_real(k, mu, lam), indice_real(2 * k, mu, lam)
        en_ciclo = k >= mu
        D = (-k) % lam if en_ciclo else None
        pot = (mu - k) + lam if not en_ciclo else D
        print(f"{k:>2} {f'x{t}':>11} {f'x{h}':>10} {'sí' if en_ciclo else 'no':>20} "
              f"{'—' if D is None else D:>3} {pot:>10}")
        if k >= 1 and t == h:
            break
        k += 1
    resultado, vueltas = floyd(lista(mu, lam), Lector())
    print(f"Floyd: {resultado} en {vueltas} vueltas; k* = {k_estrella(mu, lam)}, "
          f"n = {mu + lam}")


def sin_ciclo():
    seccion("§2. Sin ciclo: n = 7 y n = 8")
    for n in [7, 8]:
        next_of = Lector()
        resultado, vueltas = floyd(lista(n, 0), next_of)
        print(f"n = {n}: {resultado} en {vueltas} vueltas y {next_of.lecturas} lecturas; "
              f"3·floor(n/2) + (n mod 2) = {3 * (n // 2) + n % 2}")


def potencial(k, mu, lam):
    """El potencial de la vuelta k (antes de moverse)."""
    if lam == 0:
        return mu - 2 * k                    # sin ciclo, n = mu: nodos desde la liebre
    if k < mu or k == 0:
        return (mu - k) + lam                # la tortuga todavía no entró al ciclo
    return (-k) % lam                        # distancia de la liebre a la tortuga


def posiciones_vigiladas(mu, lam):
    """Floyd con el invariante de posiciones y el potencial vigilados por assert.
    Devuelve la cantidad de vueltas."""
    t = h = lista(mu, lam)
    k = 0
    previo = None
    while h is not None:
        # invariante: después de k vueltas, la tortuga está en x_k y la liebre en x_2k
        assert t.indice == indice_real(k, mu, lam)
        assert h.indice == indice_real(2 * k, mu, lam)
        pot = potencial(k, mu, lam)
        assert pot >= 0 and (previo is None or pot < previo)
        previo = pot
        h1 = h.next
        if h1 is None:
            break
        h, t = h1.next, t.next
        k += 1
        if t is h:
            # el encuentro: la tortuga en x_k y potencial 0, que bajó en esta vuelta
            assert t.indice == indice_real(k, mu, lam)
            assert potencial(k, mu, lam) == 0 < previo
            return k
    # sin ciclo, el estado final: la tortuga en x_k y potencial n - 2k = n mod 2
    assert (t is None or t.indice == k) and potencial(k, mu, lam) == mu % 2
    return k


def exhaustivo():
    seccion("§3 a §5. Todas las listas chicas")
    con, sin = 0, 0
    for mu in range(61):
        for lam in range(1, 61):
            next_of = Lector()
            resultado, vueltas = floyd(lista(mu, lam), next_of)
            assert resultado == "hay ciclo"
            assert vueltas == k_estrella(mu, lam) == posiciones_vigiladas(mu, lam)
            assert next_of.lecturas == 3 * vueltas and vueltas <= mu + lam
            con += 1
    for n in range(121):
        next_of = Lector()
        resultado, vueltas = floyd(lista(n, 0), next_of)
        assert resultado == "no hay ciclo" and vueltas == n // 2
        assert next_of.lecturas == 3 * (n // 2) + n % 2
        posiciones_vigiladas(n, 0)
        sin += 1
    print(f"{miles(con)} listas con ciclo (mu de 0 a 60, lambda de 1 a 60): todas "
          f"detectadas en k* = lambda·ceil(max(mu,1)/lambda) vueltas, 3 lecturas por vuelta")
    print(f"{sin} listas sin ciclo (n de 0 a 120): todas bien, en floor(n/2) vueltas y "
          f"3·floor(n/2) + (n mod 2) lecturas")
    print("invariante de posiciones y potencial vigilados en cada vuelta de cada lista")


def peor_caso():
    seccion("§5. Peor caso: lecturas de punteros entre todas las listas de n nodos")
    print(f"{'n':>6} {'peor con ciclo':>15} {'dónde (mu, lambda)':>19} {'sin ciclo':>10} "
          f"{'peor / n':>9}")
    for n in [1, 2, 10, 100, 1000]:
        peor, donde = 0, None
        for mu in range(n):
            lam = n - mu
            next_of = Lector()
            floyd(lista(mu, lam), next_of)
            if next_of.lecturas > peor:
                peor, donde = next_of.lecturas, (mu, lam)
        next_of = Lector()
        floyd(lista(n, 0), next_of)
        print(f"{n:>6} {peor:>15} {str(donde):>19} {next_of.lecturas:>10} {peor / n:>9.2f}")


def busqueda_con_conjunto(head, next_of, guardados=None):
    """La alternativa obvia: recordar todos los nodos vistos. Memoria Θ(n)."""
    vistos = set()
    x = head
    respuesta_ = "no hay ciclo"
    while x is not None:
        if id(x) in vistos:
            respuesta_ = "hay ciclo"
            break
        vistos.add(id(x))
        x = next_of(x)
    if guardados is not None:
        guardados.append(len(vistos))
    return respuesta_


def comparar_con_conjunto():
    seccion("§6. Floyd contra recordar los nodos vistos, n = 1000")
    print(f"{'lista':>20} {'Floyd: lecturas':>16} {'conjunto: lecturas':>19} "
          f"{'conjunto: nodos guardados':>26}")
    for mu, lam in [(0, 1000), (500, 500), (999, 1), (1000, 0)]:
        s1, s2, guardados = Lector(), Lector(), []
        floyd(lista(mu, lam), s1)
        busqueda_con_conjunto(lista(mu, lam), s2, guardados)
        nombre = f"mu = {mu}, lambda = {lam}" if lam else f"sin ciclo, n = {mu}"
        print(f"{nombre:>20} {s1.lecturas:>16} {s2.lecturas:>19} {guardados[0]:>26}")


def inicio_del_ciclo(head, next_of):
    """Floyd completo: si hay ciclo, devuelve (mu, lambda)."""
    t = h = head
    while True:                              # primera fase: hasta encontrarse en x_k*
        if h is None or next_of(h) is None:
            return None
        h = next_of(next_of(h))
        t = next_of(t)
        if t is h:
            break
    t, mu = head, 0
    while t is not h:                        # segunda fase: los dos a velocidad 1
        t, h, mu = next_of(t), next_of(h), mu + 1
    lam, x = 1, next_of(t)
    while x is not t:                        # tercera fase: una vuelta al ciclo
        x, lam = next_of(x), lam + 1
    return mu, lam


def de_regalo():
    seccion("§7. De regalo: dónde empieza el ciclo y cuánto mide")
    bien = 0
    for mu in range(41):
        for lam in range(1, 41):
            assert inicio_del_ciclo(lista(mu, lam), Lector()) == (mu, lam)
            bien += 1
    print(f"{miles(bien)} listas (mu de 0 a 40, lambda de 1 a 40): mu y lambda "
          f"recuperados en todas")


# --------------------------------------------------------------------------
# 3. Los errores plantados
# --------------------------------------------------------------------------

def floyd_un_paso(head):
    """La liebre solo mira que ella misma exista antes de dar dos pasos."""
    t = h = head
    while h is not None:
        h = h.next.next                        # revienta si h.next es None
        t = t.next
        if t is h:
            return "hay ciclo"
    return "no hay ciclo"


def floyd_por_valor(head):
    """Compara lo que guardan los nodos en vez de compararlos a ellos."""
    t = h = head
    while h is not None and h.next is not None:
        h = h.next.next
        t = t.next
        if h is not None and t.value == h.value:
            return "hay ciclo"
    return "no hay ciclo"


def respuesta(funcion, head):
    try:
        return funcion(head)
    except AttributeError:
        return "revienta"


def errores_plantados():
    seccion("§8. Dos errores plantados contra cuatro baterías de pruebas")
    rng = random.Random(8)

    def caso(mu, lam):
        return mu, lam, [rng.randrange(10) for _ in range(mu + lam)]

    baterias = {
        "con ciclo": [caso(rng.randint(0, 30), rng.randint(1, 30)) for _ in range(2000)],
        "sin ciclo, largo par": [caso(2 * rng.randint(0, 30), 0) for _ in range(2000)],
        "sin ciclo, largo al azar": [caso(rng.randint(0, 60), 0) for _ in range(2000)],
        "exhaustivo, n <= 12": ([caso(mu, lam) for mu in range(12)
                                 for lam in range(1, 12 - mu + 1)]
                                + [caso(n, 0) for n in range(13)]),
    }
    variantes = [("correcta", lambda c: floyd(c, lambda x: x.next)[0]),
                 ("liebre de un paso", floyd_un_paso),
                 ("compara valores", floyd_por_valor)]
    fallos = {}
    print("los nodos guardan valores al azar en 0..9")
    print(f"{'batería':>25} {'listas':>7} " + " ".join(f"{v:>18}" for v, _ in variantes))
    for nombre, casos in baterias.items():
        fila = []
        for _, f in variantes:
            malos = sum(respuesta(f, lista(mu, lam, valores))
                        != ("hay ciclo" if lam > 0 else "no hay ciclo")
                        for mu, lam, valores in casos)
            fila.append(100 * malos / len(casos))
        fallos[nombre] = fila
        print(f"{nombre:>25} {len(casos):>7} " + " ".join(f"{x:>17.1f}%" for x in fila))

    # cuándo falla cada una
    revienta = [n for n in range(1, 41)
                if respuesta(floyd_un_paso, lista(n, 0)) == "revienta"]
    impares = [n for n in range(1, 41) if n % 2 == 1]
    print(f"la liebre de un paso revienta, entre las listas sin ciclo de 1 a 40 nodos, "
          f"exactamente en las de largo impar: {revienta == impares}")
    distintos = sum(respuesta(floyd_por_valor, lista(n, 0, list(range(n)))) != "no hay ciclo"
                    for n in range(200))
    print(f"comparar valores, con valores todos distintos: {distintos} errores en 200 "
          f"listas sin ciclo")
    return fallos, [v for v, _ in variantes]


# --------------------------------------------------------------------------
# 4. Pruebas
# --------------------------------------------------------------------------

def pruebas():
    seccion("Pruebas")
    comprobaciones = 0
    rng = random.Random(2026)

    # (a) listas con ciclo y sin ciclo: respuesta, vueltas y lecturas exactas
    for mu in range(81):
        for lam in range(0, 81):
            next_of = Lector()
            resultado, vueltas = floyd(lista(mu, lam), next_of)
            if lam == 0:
                assert resultado == "no hay ciclo" and vueltas == mu // 2
                assert next_of.lecturas == 3 * (mu // 2) + mu % 2
            else:
                assert resultado == "hay ciclo" and vueltas == k_estrella(mu, lam)
                assert next_of.lecturas == 3 * vueltas <= 3 * (mu + lam)
            comprobaciones += 1

    # (b) invariante de posiciones y potencial vigilados
    for mu in range(41):
        for lam in range(0, 41):
            posiciones_vigiladas(mu, lam)
            comprobaciones += 1

    # (c) Floyd contra el oráculo (el conjunto de vistos) en listas grandes al azar
    for _ in range(300):
        mu, lam = rng.randint(0, 3000), rng.choice([0, rng.randint(1, 3000)])
        assert (floyd(lista(mu, lam), Lector())[0]
                == busqueda_con_conjunto(lista(mu, lam), Lector()))
        comprobaciones += 1

    # (d) dónde empieza el ciclo y cuánto mide; sin ciclo devuelve None
    for mu in range(61):
        for lam in range(0, 61):
            esperado = (mu, lam) if lam else None
            assert inicio_del_ciclo(lista(mu, lam), Lector()) == esperado
            comprobaciones += 1

    # (e) k* <= n siempre, con igualdad solo si mu = 0
    for mu in range(200):
        for lam in range(1, 200):
            k = k_estrella(mu, lam)
            assert k <= mu + lam and ((k == mu + lam) == (mu == 0))
            comprobaciones += 1

    print(f"{miles(comprobaciones)} comprobaciones, 0 fallos")


# --------------------------------------------------------------------------
# 5. Figuras
# --------------------------------------------------------------------------

TINTA, APAGADO, REGLA = "#1a1a1a", "#6b7280", "#d8dce3"
ACENTO, OSCURO, CALIDO, ALARMA = "#0891b2", "#0e7490", "#b45309", "#be123c"


def _estilo():
    plt.rcParams.update({
        "font.size": 9, "axes.edgecolor": APAGADO, "axes.labelcolor": TINTA,
        "xtick.color": APAGADO, "ytick.color": APAGADO,
        "figure.facecolor": "white", "svg.hashsalt": "ejercicio-05",
    })


def _guardar(fig, nombre):
    fig.tight_layout()
    fig.savefig(nombre, metadata={"Date": None})
    plt.close(fig)


def figura_rho(mu=3, lam=5):
    k = floyd(lista(mu, lam), Lector())[1]
    encuentro = indice_real(k, mu, lam)
    fig, ax = plt.subplots(figsize=(6.4, 3.0))
    radio = 1.35
    centro = (mu * 1.3 + radio, 0)
    pos = {}
    for i in range(mu):
        pos[i] = (i * 1.3, 0)
    for j in range(lam):
        ang = math.pi - 2 * math.pi * j / lam
        pos[mu + j] = (centro[0] + radio * math.cos(ang), centro[1] + radio * math.sin(ang))
    for i in range(mu + lam):
        siguiente = i + 1 if i + 1 < mu + lam else mu
        (x0, y0), (x1, y1) = pos[i], pos[siguiente]
        ax.annotate("", (x1, y1), (x0, y0),
                    arrowprops={"arrowstyle": "-|>", "color": APAGADO, "lw": 0.9,
                                "shrinkA": 11, "shrinkB": 11})
    for i, (x, y) in pos.items():
        color = ALARMA if i == encuentro else (CALIDO if i == mu else OSCURO)
        ax.add_patch(plt.Circle((x, y), 0.32, facecolor="white", edgecolor=color, lw=1.6))
        ax.text(x, y, f"x{i}", ha="center", va="center", fontsize=8, color=color)
    ax.text(pos[0][0], -0.65, "cabeza", ha="center", fontsize=8, color=APAGADO)
    ax.text(pos[mu][0] - 0.1, pos[mu][1] - 0.65, f"entrada al ciclo\n(μ = {mu})",
            ha="center", va="top", fontsize=8, color=CALIDO)
    xe, ye = pos[encuentro]
    ax.text(xe + 0.45, ye + 0.35, f"se encuentran aquí\nen la vuelta k = {k}",
            ha="left", fontsize=8, color=ALARMA)
    ax.text(centro[0], 0, f"λ = {lam}", ha="center", va="center", fontsize=9,
            color=APAGADO)
    ax.set_xlim(-0.6, centro[0] + radio + 2.6)
    ax.set_ylim(-1.9, 1.9)
    ax.set_aspect("equal")
    ax.axis("off")
    _guardar(fig, "ejercicio-05-rho.svg")


def figura_potencial():
    fig, ax = plt.subplots(figsize=(6.4, 3.0))
    for (mu, lam), color in [((3, 5), ALARMA), ((0, 8), OSCURO), ((9, 3), CALIDO),
                             ((12, 0), APAGADO)]:
        k_fin = mu // 2 if lam == 0 else k_estrella(mu, lam)
        v = [potencial(k, mu, lam) for k in range(k_fin + 1)]
        nombre = f"μ = {mu}, λ = {lam}" if lam else f"sin ciclo, n = {mu}"
        ax.plot(range(len(v)), v, "o-", color=color, ms=3.5, lw=1.4, label=nombre)
    ax.set_xlabel("vuelta k")
    ax.set_ylabel("potencial")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(color=REGLA, lw=0.6)
    ax.legend(frameon=False, fontsize=8)
    _guardar(fig, "ejercicio-05-potencial.svg")


def figura_errores(fallos, nombres):
    fig, ax = plt.subplots(figsize=(6.8, 3.0))
    baterias = list(fallos)
    colores = [OSCURO, ALARMA, CALIDO]
    ancho = 0.26
    for k, (v, color) in enumerate(zip(nombres, colores)):
        alturas = [fallos[b][k] for b in baterias]
        pos = [i + (k - 1) * ancho for i in range(len(baterias))]
        ax.bar(pos, alturas, ancho, color=color, label=v)
        for x, h in zip(pos, alturas):
            ax.text(x, h + 1.2, f"{h:.0f}", ha="center", fontsize=7, color=color)
    ax.set_xticks(range(len(baterias)))
    ax.set_xticklabels(baterias, fontsize=8)
    ax.set_ylabel("% de listas mal")
    ax.set_ylim(0, 105)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color=REGLA, lw=0.6)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    _guardar(fig, "ejercicio-05-errores.svg")


if __name__ == "__main__":
    ejemplo_chico()
    sin_ciclo()
    exhaustivo()
    peor_caso()
    comparar_con_conjunto()
    de_regalo()
    fallos, nombres = errores_plantados()
    pruebas()
    _estilo()
    figura_rho()
    figura_potencial()
    figura_errores(fallos, nombres)
    print("\nfiguras: ejercicio-05-rho.svg, ejercicio-05-potencial.svg, "
          "ejercicio-05-errores.svg")
