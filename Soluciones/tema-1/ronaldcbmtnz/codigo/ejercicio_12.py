"""Ejercicio 12 del Tema 1: Gale-Shapley con listas incompletas.

pref_a[a] es la lista (en orden de preferencia) de los receptores que el
proponente a acepta; pref_b[b], la de los proponentes que el receptor b acepta.
Un par (a, b) es aceptable si cada uno está en la lista del otro. En el caso del
enunciado, los receptores tienen listas completas y solo las de los proponentes
son incompletas.

Uso:
    python ejercicio_12.py             imprime las tablas del informe
    python ejercicio_12.py --figuras   además regenera las figuras

Las pruebas están en test_ejercicio_12.py.
"""

import random
import sys
from collections import deque
from pathlib import Path


# ---------------------------------------------------------------------------
# 1. El algoritmo adaptado
# ---------------------------------------------------------------------------

def gale_shapley(pref_a, pref_b, orden="cola", semilla=0, traza=None):
    """Aceptación diferida con listas incompletas.

    Devuelve (M, propuestas), con M[a] = receptor de a, o None si a queda solo.
    Mientras haya un proponente libre al que le queden receptores en su lista,
    le propone al siguiente. El receptor acepta si a está en su lista y está
    libre o prefiere a a su pareja actual.
    """
    rango = [{a: lugar for lugar, a in enumerate(lista)} for lista in pref_b]
    siguiente = [0] * len(pref_a)
    pareja_de_b = [None] * len(pref_b)
    libres = deque(a for a in range(len(pref_a)) if pref_a[a])
    azar = random.Random(semilla)
    propuestas = 0

    while libres:
        if orden == "azar":
            libres.rotate(azar.randrange(len(libres)))
        a = libres.popleft() if orden != "pila" else libres.pop()
        b = pref_a[a][siguiente[a]]
        siguiente[a] += 1
        propuestas += 1
        actual = pareja_de_b[b]
        if a not in rango[b]:
            rechazado = a                                  # b no acepta a a
        elif actual is None:
            pareja_de_b[b], rechazado = a, None
        elif rango[b][a] < rango[b][actual]:
            pareja_de_b[b], rechazado = a, actual
        else:
            rechazado = a
        if rechazado is not None and siguiente[rechazado] < len(pref_a[rechazado]):
            libres.append(rechazado)                       # si agotó su lista, queda solo
        if traza is not None:
            traza.append((a, b, actual, pareja_de_b[b]))

    M = [None] * len(pref_a)
    for b, a in enumerate(pareja_de_b):
        if a is not None:
            M[a] = b
    return M, propuestas


def gale_shapley_ingenuo(pref_a, pref_b):
    """La adaptación que no cambia la condición del ciclo: revienta si alguien agota su lista."""
    rango = [{a: lugar for lugar, a in enumerate(lista)} for lista in pref_b]
    siguiente = [0] * len(pref_a)
    pareja_de_b = [None] * len(pref_b)
    libres = deque(range(len(pref_a)))
    while libres:
        a = libres.popleft()
        b = pref_a[a][siguiente[a]]                        # IndexError al agotar la lista
        siguiente[a] += 1
        actual = pareja_de_b[b]
        if a in rango[b] and (actual is None or rango[b][a] < rango[b][actual]):
            pareja_de_b[b] = a
            if actual is not None:
                libres.append(actual)
        else:
            libres.append(a)
    M = [None] * len(pref_a)
    for b, a in enumerate(pareja_de_b):
        if a is not None:
            M[a] = b
    return M


def gale_shapley_sin_mirar_b(pref_a, pref_b):
    """Otro error: el receptor no mira si a está en su lista (acepta a cualquiera)."""
    completas = [lista + [a for a in range(len(pref_a)) if a not in lista] for lista in pref_b]
    return gale_shapley(pref_a, completas)[0]


# ---------------------------------------------------------------------------
# 2. Estabilidad, por fuerza bruta
# ---------------------------------------------------------------------------

def aceptable(a, b, pref_a, pref_b):
    return b in pref_a[a] and a in pref_b[b]


def prefiere(lista, nuevo, actual):
    """True si en `lista` nuevo está antes que actual (o actual es None: estar solo)."""
    return actual is None or lista.index(nuevo) < lista.index(actual)


def pareja_de_b(M, n_b):
    inversa = [None] * n_b
    for a, b in enumerate(M):
        if b is not None:
            inversa[b] = a
    return inversa


def es_emparejamiento(M, pref_a, pref_b):
    """Cada receptor a lo sumo una vez y solo pares aceptables (racionalidad individual)."""
    usados = [b for b in M if b is not None]
    return len(usados) == len(set(usados)) and all(
        b is None or aceptable(a, b, pref_a, pref_b) for a, b in enumerate(M))


def pares_bloqueantes(M, pref_a, pref_b):
    """(a, b) aceptable, no juntos, y cada uno solo o prefiriendo al otro."""
    inversa = pareja_de_b(M, len(pref_b))
    return [(a, b) for a in range(len(pref_a)) for b in pref_a[a]
            if M[a] != b and a in pref_b[b]
            and prefiere(pref_a[a], b, M[a]) and prefiere(pref_b[b], a, inversa[b])]


def es_estable(M, pref_a, pref_b):
    return es_emparejamiento(M, pref_a, pref_b) and not pares_bloqueantes(M, pref_a, pref_b)


def todos_los_emparejamientos(pref_a, pref_b):
    """Todos los emparejamientos de pares aceptables (incluidos los que dejan gente sola)."""
    n_a = len(pref_a)
    actual = [None] * n_a
    usados = set()

    def extender(a):
        if a == n_a:
            yield list(actual)
            return
        actual[a] = None
        yield from extender(a + 1)
        for b in pref_a[a]:
            if b not in usados and a in pref_b[b]:
                usados.add(b)
                actual[a] = b
                yield from extender(a + 1)
                usados.discard(b)
        actual[a] = None

    yield from extender(0)


def todos_los_estables(pref_a, pref_b):
    return [M for M in todos_los_emparejamientos(pref_a, pref_b)
            if not pares_bloqueantes(M, pref_a, pref_b)]


# ---------------------------------------------------------------------------
# 3. Instancias
# ---------------------------------------------------------------------------

def instancia(n_a, n_b, p, rng, receptores_completos=True):
    """Cada proponente lista cada receptor con probabilidad p, en orden al azar.

    Con receptores_completos=True (el caso del enunciado) los receptores listan a
    todos; si no, también con probabilidad p.
    """
    pref_a = []
    for _ in range(n_a):
        lista = [b for b in range(n_b) if rng.random() < p]
        rng.shuffle(lista)
        pref_a.append(lista)
    pref_b = []
    for _ in range(n_b):
        lista = [a for a in range(n_a) if receptores_completos or rng.random() < p]
        rng.shuffle(lista)
        pref_b.append(lista)
    return pref_a, pref_b


def instancia_largo(n, k, rng):
    """Cada proponente lista exactamente k receptores al azar; receptores completos."""
    pref_a = [rng.sample(range(n), k) for _ in range(n)]
    pref_b = [rng.sample(range(n), n) for _ in range(n)]
    return pref_a, pref_b


EJEMPLO = (
    # proponentes a0..a3 (listas incompletas)
    [[0, 1], [0], [1, 2, 0], [2]],
    # receptores b0..b2 (listas completas)
    [[2, 1, 0, 3], [0, 2, 1, 3], [2, 3, 0, 1]],
)


# ---------------------------------------------------------------------------
# 4. Tablas
# ---------------------------------------------------------------------------

def _nombre(M):
    return "  ".join(f"a{a}–b{b}" if b is not None else f"a{a} solo" for a, b in enumerate(M))


def tabla_ejemplo():
    pref_a, pref_b = EJEMPLO
    print("Tabla 1. El ejemplo del informe")
    traza = []
    M, propuestas = gale_shapley(pref_a, pref_b, traza=traza)
    for paso, (a, b, antes, despues) in enumerate(traza, 1):
        if despues == a and antes is None:
            que = "acepta"
        elif despues == a:
            que = f"cambia; a{antes} queda libre"
        else:
            que = "rechaza"
        print(f"  {paso}: a{a} -> b{b}  tenía {'—' if antes is None else 'a' + str(antes)}: {que}")
    print(f"  resultado: {_nombre(M)}  ({propuestas} propuestas)")
    print(f"  estables: {[_nombre(E) for E in todos_los_estables(pref_a, pref_b)]}")
    try:
        gale_shapley_ingenuo(pref_a, pref_b)
        print("  versión ingenua: terminó")
    except IndexError:
        print("  versión ingenua: IndexError (un proponente agotó su lista)")
    print()


def experimento_verificacion(casos=1500, semilla=12):
    """Estabilidad, optimalidad, independencia del orden y hospitales rurales."""
    rng = random.Random(semilla)
    cuentas = dict(instancias=0, estables=0, iguales=0, optimo=0, rurales=0, propuestas_ok=0)
    for _ in range(casos):
        n_a, n_b = rng.randint(1, 5), rng.randint(1, 5)
        pref_a, pref_b = instancia(n_a, n_b, rng.choice([0.3, 0.6, 0.9]), rng,
                                   receptores_completos=rng.random() < 0.5)
        resultados = [gale_shapley(pref_a, pref_b, orden=o, semilla=s)
                      for o, s in [("cola", 0), ("pila", 0), ("azar", 1), ("azar", 2)]]
        M, propuestas = resultados[0]
        estables = todos_los_estables(pref_a, pref_b)
        cuentas["instancias"] += 1
        cuentas["estables"] += es_estable(M, pref_a, pref_b)
        cuentas["iguales"] += all(R[0] == M for R in resultados)
        cuentas["propuestas_ok"] += propuestas <= sum(map(len, pref_a))
        mejor = all(
            (M[a] is None and all(E[a] is None for E in estables)) or
            (M[a] is not None and all(E[a] is None or pref_a[a].index(M[a]) <= pref_a[a].index(E[a])
                                      for E in estables))
            for a in range(n_a))
        cuentas["optimo"] += mejor
        emparejados = {frozenset(a for a in range(n_a) if E[a] is not None) for E in estables}
        receptores = {frozenset(b for b in E if b is not None) for E in estables}
        cuentas["rurales"] += len(emparejados) == 1 and len(receptores) == 1
    return cuentas


def tabla_verificacion(cuentas):
    print("Tabla 2. Verificación contra la enumeración de todos los emparejamientos estables")
    n = cuentas["instancias"]
    print(f"  instancias (hasta 5 x 5, listas incompletas): {n}")
    print(f"  el resultado es estable:                           {cuentas['estables']} de {n}")
    print(f"  mismo resultado con cola, pila y dos azares:       {cuentas['iguales']} de {n}")
    print(f"  cada proponente con su mejor pareja válida:        {cuentas['optimo']} de {n}")
    print(f"  todos los estables emparejan a las mismas personas: {cuentas['rurales']} de {n}")
    print(f"  propuestas <= suma de los largos de las listas:    {cuentas['propuestas_ok']} de {n}")
    print()


def experimento_largo(n=50, repeticiones=200, semilla=13):
    rng = random.Random(semilla)
    filas = []
    for k in [1, 2, 3, 4, 5, 6, 8, 10, 15, 20, 30, 50]:
        solos = propuestas = 0
        for _ in range(repeticiones):
            pref_a, pref_b = instancia_largo(n, k, rng)
            M, p = gale_shapley(pref_a, pref_b)
            solos += sum(b is None for b in M)
            propuestas += p
        filas.append((k, solos / (n * repeticiones), propuestas / repeticiones, n * k))
    return filas


def tabla_largo(filas, n=50):
    print(f"Tabla 3. n = {n} proponentes y receptores; cada proponente lista k receptores al azar")
    print(f"{'k':>4} {'fracción sola':>14} {'propuestas':>11} {'n·k (cota)':>11}")
    for k, solos, propuestas, cota in filas:
        print(f"{k:>4} {solos:>14.3f} {propuestas:>11.1f} {cota:>11}")
    print()


def tabla_errores(casos=3000, semilla=14):
    print("Tabla 4. Los dos errores plantados, según cómo se generan las instancias")
    rng = random.Random(semilla)
    for receptores_completos in (True, False):
        revienta = intruso = 0
        for _ in range(casos):
            pref_a, pref_b = instancia(rng.randint(1, 6), rng.randint(1, 6), rng.choice([0.3, 0.6]),
                                       rng, receptores_completos)
            try:
                gale_shapley_ingenuo(pref_a, pref_b)
            except IndexError:
                revienta += 1
            intruso += not es_estable(gale_shapley_sin_mirar_b(pref_a, pref_b), pref_a, pref_b)
        tipo = "receptores completos (el enunciado)" if receptores_completos else "las dos listas incompletas"
        print(f"  {tipo:>36}: ingenua revienta {100 * revienta / casos:5.1f}%,"
              f" receptor que no mira su lista {100 * intruso / casos:5.1f}%")
    print()


# ---------------------------------------------------------------------------
# 5. Figura
# ---------------------------------------------------------------------------

AZUL, NARANJA = "#2a78d6", "#eb6834"
TINTA, TINTA_2, TENUE, REJILLA, SUPERFICIE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"


def figura_largo(destino, filas, n=50):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

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
    fig, (izq, der) = plt.subplots(1, 2, figsize=(10, 4))
    ks = [f[0] for f in filas]
    izq.plot(ks, [f[1] for f in filas], "o-", color=AZUL, markersize=5)
    izq.set_xscale("log")
    izq.set_xlabel("receptores en cada lista (k)")
    izq.set_ylabel("fracción de proponentes solos")
    izq.set_title("Con listas cortas, muchos quedan solos")
    izq.set_ylim(0, 0.4)
    der.plot(ks, [f[3] for f in filas], color=TENUE, linestyle=(0, (4, 3)), linewidth=1.4,
             label="cota del potencial: n·k")
    der.plot(ks, [f[2] for f in filas], "o-", color=NARANJA, markersize=5,
             label="propuestas medidas")
    der.set_xscale("log")
    der.set_yscale("log")
    der.set_xlabel("receptores en cada lista (k)")
    der.set_ylabel("propuestas")
    der.set_title("Propuestas contra la cota Σ|L(a)|")
    der.legend(loc="upper left")
    fig.suptitle(f"Gale-Shapley con listas incompletas, n = {n}, media de 200 instancias",
                 x=0.01, ha="left", fontsize=10, color=TINTA_2)
    fig.tight_layout()
    fig.savefig(destino / "ejercicio-12-largo-de-listas.png")
    plt.close(fig)
    print(f"figura escrita en {destino}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    tabla_ejemplo()
    tabla_verificacion(experimento_verificacion())
    filas = experimento_largo()
    tabla_largo(filas)
    tabla_errores()
    if "--figuras" in sys.argv:
        figura_largo(Path(__file__).resolve().parent.parent / "figuras", filas)
