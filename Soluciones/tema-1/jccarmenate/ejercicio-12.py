"""Ejercicio 12 del Tema 1: Gale-Shapley con listas incompletas.

    python ejercicio-12.py

Imprime todas las tablas que cita ejercicio-12.md, corre las pruebas y regenera las
tres figuras (ejercicio-12-instancia.svg, ejercicio-12-potencial.svg y
ejercicio-12-errores.svg). Cada número que aparece en la prosa sale de aquí. Solo
necesita matplotlib.
"""

import random
from collections import deque

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt


# --------------------------------------------------------------------------
# 1. El algoritmo, la versión de listas completas y el oráculo
# --------------------------------------------------------------------------

def gale_shapley(pref_a, pref_b, orden="cola", semilla=0, traza=None, uno_antes=False):
    """Aceptación diferida con listas incompletas.

    pref_a[a] es la lista de a, de mejor a peor, con solo los receptores que a acepta.
    pref_b[b] es la lista de b; un proponente que no aparece en ella es inaceptable
    para b (en el enunciado las listas de los receptores son completas). Devuelve
    (M, propuestas), con M[a] el receptor de a o None si a queda solo.

    Un proponente vuelve a la cola de libres solo si le queda alguien en la lista: si
    no, se queda solo para siempre. uno_antes = True es el error plantado de la
    sección 7: el proponente se rinde una propuesta antes de agotar la lista.
    """
    n_a, n_b = len(pref_a), len(pref_b)
    rank = [{a: pos for pos, a in enumerate(pref_b[b])} for b in range(n_b)]
    next_choice = [0] * n_a
    match_of_b = [None] * n_b
    corte = 1 if uno_antes else 0

    def has_more(a):
        return next_choice[a] < len(pref_a[a]) - corte

    free = deque(a for a in range(n_a) if has_more(a))
    azar = random.Random(semilla)
    propuestas = 0

    while free:
        if orden == "azar":
            free.rotate(azar.randrange(len(free)))
        a = free.popleft() if orden == "cola" else free.pop()
        b = pref_a[a][next_choice[a]]
        next_choice[a] += 1
        propuestas += 1
        current = match_of_b[b]
        if a not in rank[b]:                       # b no acepta a a
            rejected = a
        elif current is None:
            match_of_b[b], rejected = a, None
        elif rank[b][a] < rank[b][current]:
            match_of_b[b], rejected = a, current
        else:
            rejected = a
        if traza is not None:
            traza.append((a, b, current, match_of_b[b]))
        if rejected is not None and has_more(rejected):
            free.append(rejected)

    M = [None] * n_a
    for b, a in enumerate(match_of_b):
        if a is not None:
            M[a] = b
    return M, propuestas


def gale_shapley_completo(pref_a, pref_b):
    """La versión para listas completas, sin cambios: todo proponente rechazado vuelve
    a la cola, porque ahí siempre le queda alguien."""
    n = len(pref_a)
    rank = [{a: pos for pos, a in enumerate(pref_b[b])} for b in range(n)]
    next_choice, match_of_b, free = [0] * n, [None] * n, deque(range(n))
    while free:
        a = free.popleft()
        b = pref_a[a][next_choice[a]]                 # IndexError si a agotó su lista
        next_choice[a] += 1
        current = match_of_b[b]
        if current is None:
            match_of_b[b] = a
        elif rank[b][a] < rank[b][current]:
            match_of_b[b] = a
            free.append(current)
        else:
            free.append(a)
    return match_of_b


def aceptable(pref_a, pref_b, a, b):
    return b in pref_a[a] and a in pref_b[b]


def bloqueantes(M, pref_a, pref_b):
    """La definición nueva. (a, b) bloquea si se aceptan mutuamente, no están juntos, a
    está solo o prefiere b a su pareja, y b está solo o prefiere a a su pareja."""
    match_of_b = {b: a for a, b in enumerate(M) if b is not None}
    res = []
    for a in range(len(pref_a)):
        for b in pref_a[a]:
            if M[a] == b or a not in pref_b[b]:
                continue
            quiere_a = M[a] is None or pref_a[a].index(b) < pref_a[a].index(M[a])
            otro = match_of_b.get(b)
            quiere_b = otro is None or pref_b[b].index(a) < pref_b[b].index(otro)
            if quiere_a and quiere_b:
                res.append((a, b))
    return res


def bloqueantes_viejo(M, pref_a, pref_b):
    """La definición de listas completas, copiada sin pensar: solo mira pares en los
    que los dos tienen pareja, porque ahí nadie quedaba solo."""
    return [(a, b) for a, b in bloqueantes(M, pref_a, pref_b)
            if M[a] is not None and b in M]


def individualmente_racional(M, pref_a, pref_b):
    return all(b is None or aceptable(pref_a, pref_b, a, b) for a, b in enumerate(M))


def es_estable(M, pref_a, pref_b):
    return individualmente_racional(M, pref_a, pref_b) and not bloqueantes(M, pref_a, pref_b)


def todos_estables(pref_a, pref_b):
    """El oráculo: todos los emparejamientos (parciales) con pares aceptables, filtrados
    por estabilidad."""
    n_a = len(pref_a)
    res = []

    def extender(a, M, usados):
        if a == n_a:
            if es_estable(M, pref_a, pref_b):
                res.append(list(M))
            return
        M.append(None)
        extender(a + 1, M, usados)
        M.pop()
        for b in pref_a[a]:
            if b not in usados and a in pref_b[b]:
                M.append(b)
                usados.add(b)
                extender(a + 1, M, usados)
                usados.discard(b)
                M.pop()

    extender(0, [], set())
    return res


def instancia(n_a, n_b, rng, largo=None, receptores_tachan=False):
    """largo(rng) da el largo de la lista de cada proponente; None = lista completa."""
    pref_a = [rng.sample(range(n_b), n_b if largo is None else largo(rng))
              for _ in range(n_a)]
    if receptores_tachan:
        pref_b = [rng.sample(range(n_a), rng.randint(0, n_a)) for _ in range(n_b)]
    else:
        pref_b = [rng.sample(range(n_a), n_a) for _ in range(n_b)]
    return pref_a, pref_b


def seccion(titulo):
    print()
    print(titulo)
    print("-" * len(titulo))


def miles(x):
    return f"{x:,}".replace(",", " ")


def nombre(s, i):
    return f"{s}{i + 1}"


def pares(M):
    return ", ".join(f"a{a + 1}–b{b + 1}" if b is not None else f"a{a + 1} solo"
                     for a, b in enumerate(M))


EJEMPLO_A = [[3, 1], [0, 1], [0, 3], [0, 3]]
EJEMPLO_B = [[2, 0, 1, 3], [0, 3, 1, 2], [1, 2, 3, 0], [3, 0, 2, 1]]


# --------------------------------------------------------------------------
# 2. Las tablas que cita la prosa
# --------------------------------------------------------------------------

def ejemplo_chico():
    seccion("§2. Ejemplo chico: 4 proponentes y 4 receptores")
    pa, pb = EJEMPLO_A, EJEMPLO_B
    for i in range(4):
        print(f"a{i + 1}: {' > '.join(nombre('b', x) for x in pa[i]):<16}"
              f"b{i + 1}: {' > '.join(nombre('a', x) for x in pb[i])}")
    traza = []
    M, k = gale_shapley(pa, pb, traza=traza)
    print()
    print(f"{'paso':>4}  {'propone':<8}{'a':<4}{'tenía':<7}{'se queda con':<14}qué pasa")
    restantes = {a: len(pa[a]) for a in range(4)}
    for paso, (a, b, antes, despues) in enumerate(traza, 1):
        restantes[a] -= 1
        if antes is None:
            que = "acepta"
        elif despues == a:
            que = f"cambia; a{antes + 1} queda libre"
            if restantes[antes] == 0:
                que += " y sin nadie más en su lista: se queda solo"
        else:
            que = f"rechaza a a{a + 1}"
            if restantes[a] == 0:
                que += ", que agotó su lista: se queda solo"
        print(f"{paso:>4}  {nombre('a', a):<8}{nombre('b', b):<4}"
              f"{'—' if antes is None else nombre('a', antes):<7}"
              f"{nombre('a', despues):<14}{que}")
    sin_pareja = [nombre("b", b) for b in range(4) if b not in M]
    print(f"resultado: {pares(M)}; sin pareja: {', '.join(sin_pareja)}. {k} propuestas, "
          f"L = {sum(map(len, pa))} pares en las listas")
    print(f"pares bloqueantes: {len(bloqueantes(M, pa, pb))}; "
          f"emparejamientos estables de la instancia: {len(todos_estables(pa, pb))}")
    try:
        gale_shapley_completo(pa, pb)
        print("la versión de listas completas termina")
    except IndexError:
        print("la versión de listas completas: IndexError al buscar el siguiente "
              "receptor de un proponente que ya agotó su lista")
    return M


def version_vieja():
    seccion("§3. La versión de listas completas, con listas incompletas")
    rng = random.Random(3)
    print(f"{'n':>4} {'instancias':>11} {'IndexError':>11}")
    for n in [5, 20, 100]:
        errores = 0
        for _ in range(300):
            pa, pb = instancia(n, n, rng, largo=lambda r: r.randint(1, n))
            try:
                gale_shapley_completo(pa, pb)
            except IndexError:
                errores += 1
        print(f"{n:>4} {300:>11} {errores:>11}")


def potencial():
    seccion("§4. Propuestas contra L, el largo total de las listas")
    rng = random.Random(4)
    puntos = {"listas completas": [], "listas incompletas": []}
    print(f"{'listas':>20} {'n':>4} {'instancias':>11} {'propuestas / L, máx':>20} "
          f"{'promedio':>9}")
    for etiqueta in puntos:
        for n in [10, 40, 160]:
            razones = []
            for _ in range(60):
                if etiqueta == "listas completas":
                    pa, pb = instancia(n, n, rng)
                else:
                    pa, pb = instancia(n, n, rng,
                                       largo=lambda r: r.randint(1, max(1, n // 4)))
                L = sum(map(len, pa))
                M, k = gale_shapley(pa, pb, orden="azar", semilla=n)
                assert k <= L
                razones.append(k / L)
                puntos[etiqueta].append((L, k))
            print(f"{etiqueta:>20} {n:>4} {60:>11} {max(razones):>20.3f} "
                  f"{sum(razones) / len(razones):>9.3f}")
    # la cota se alcanza: todos listan al mismo receptor
    pa = [[0] for _ in range(6)]
    pb = [list(range(6))]
    _, k = gale_shapley(pa, pb)
    print(f"seis proponentes que solo listan a b1: {k} propuestas = L = "
          f"{sum(map(len, pa))}")
    return puntos


def estabilidad():
    seccion("§5. Estabilidad, contra el oráculo")
    rng = random.Random(5)
    casos = bloq = irracional = fuera = 0
    for _ in range(1500):
        n_a, n_b = rng.randint(1, 6), rng.randint(1, 6)
        pa, pb = instancia(n_a, n_b, rng, largo=lambda r: r.randint(0, n_b))
        estables = todos_estables(pa, pb)
        for orden, s in [("cola", 0), ("pila", 0), ("azar", 1)]:
            M, _ = gale_shapley(pa, pb, orden=orden, semilla=s)
            casos += 1
            bloq += bool(bloqueantes(M, pa, pb))
            irracional += not individualmente_racional(M, pa, pb)
            fuera += M not in estables
    print(f"{miles(casos)} ejecuciones (1500 instancias con hasta 6 por lado, "
          f"tres órdenes):")
    print(f"  con alguna pareja bloqueante: {bloq}")
    print(f"  con alguien emparejado con quien no listó: {irracional}")
    print(f"  resultado que no está entre los estables del oráculo: {fuera}")


def optimalidad():
    seccion("§6. Lo que sigue valiendo: optimalidad y los que quedan solos")
    rng = random.Random(6)
    varios = iguales = optimo = mismos = 0
    total = 0
    while varios < 300:
        # solo cuentan las instancias con más de un emparejamiento estable: con uno
        # solo, todo lo que se comprueba aquí es automático
        total += 1
        n_a, n_b = rng.randint(3, 6), rng.randint(3, 6)
        pa, pb = instancia(n_a, n_b, rng, largo=lambda r: r.randint(n_b // 2, n_b))
        estables = todos_estables(pa, pb)
        if len(estables) < 2:
            continue
        varios += 1
        resultados = [gale_shapley(pa, pb, orden=o, semilla=s)[0]
                      for o, s in [("cola", 0), ("pila", 0), ("azar", 1), ("azar", 2)]]
        iguales += all(M == resultados[0] for M in resultados)
        M = resultados[0]

        def lugar(a, b):
            return len(pa[a]) if b is None else pa[a].index(b)

        optimo += all(lugar(a, M[a]) <= min(lugar(a, E[a]) for E in estables)
                      for a in range(n_a))
        solos_a = {frozenset(a for a in range(n_a) if E[a] is None) for E in estables}
        solos_b = {frozenset(set(range(n_b)) - set(E)) for E in estables}
        mismos += len(solos_a) == 1 and len(solos_b) == 1
    print(f"300 instancias con más de un emparejamiento estable (de {total} generadas):")
    print(f"  mismo resultado con las cuatro ejecuciones: {iguales} de 300")
    print(f"  cada proponente con su mejor pareja válida: {optimo} de 300")
    print(f"  los mismos solos en todos los emparejamientos estables: {mismos} de 300")


def errores_plantados():
    seccion("§7. El error plantado: rendirse una propuesta antes")
    rng = random.Random(7)
    n = 8
    baterias = {
        "listas completas": lambda: instancia(n, n, rng),
        "listas al azar": lambda: instancia(n, n, rng, largo=lambda r: r.randint(1, n)),
        "listas cortas": lambda: instancia(n, n, rng, largo=lambda r: r.randint(1, 2)),
    }
    tabla = {}
    print(f"{'batería':>18} {'casos':>6} {'definición vieja':>17} {'definición nueva':>17}")
    for etiqueta, g in baterias.items():
        casos = [g() for _ in range(2000)]
        viejo = nuevo = 0
        for pa, pb in casos:
            M, _ = gale_shapley(pa, pb, uno_antes=True)
            viejo += bool(bloqueantes_viejo(M, pa, pb))
            nuevo += bool(bloqueantes(M, pa, pb))
        f = [100 * viejo / len(casos), 100 * nuevo / len(casos)]
        tabla[etiqueta] = f
        print(f"{etiqueta:>18} {len(casos):>6} {f[0]:>16.1f}% {f[1]:>16.1f}%")
    print(f"las tres baterías tienen {n} proponentes y {n} receptores")
    M, _ = gale_shapley(EJEMPLO_A, EJEMPLO_B, uno_antes=True)
    nuevos = [f"(a{a + 1}, b{b + 1})" for a, b in bloqueantes(M, EJEMPLO_A, EJEMPLO_B)]
    viejos = [f"(a{a + 1}, b{b + 1})" for a, b in bloqueantes_viejo(M, EJEMPLO_A, EJEMPLO_B)]
    print(f"en el ejemplo de la sección 2: {pares(M)}")
    print(f"  bloqueantes con la definición nueva: {', '.join(nuevos) or 'ninguna'}; "
          f"con la vieja: {', '.join(viejos) or 'ninguna'}")
    return tabla


def receptores_tachan():
    seccion("§8. Si los receptores también tachan")
    rng = random.Random(8)
    casos = malos = 0
    for _ in range(1500):
        n_a, n_b = rng.randint(1, 6), rng.randint(1, 6)
        pa, pb = instancia(n_a, n_b, rng, largo=lambda r: r.randint(0, n_b),
                           receptores_tachan=True)
        estables = todos_estables(pa, pb)
        M, _ = gale_shapley(pa, pb, orden="azar", semilla=3)
        casos += 1
        malos += not es_estable(M, pa, pb) or M not in estables
    print(f"{miles(casos)} instancias con listas incompletas en los dos lados: "
          f"{malos} resultados inestables o fuera del oráculo")


# --------------------------------------------------------------------------
# 3. Pruebas
# --------------------------------------------------------------------------

def pruebas():
    seccion("Pruebas")
    comprobaciones = 0
    rng = random.Random(2026)

    # (a) con listas completas y n = n, la versión nueva coincide con la de siempre
    for _ in range(500):
        n = rng.randint(1, 12)
        pa, pb = instancia(n, n, rng)
        M, k = gale_shapley(pa, pb)
        match_of_b = gale_shapley_completo(pa, pb)
        assert all(M[a] == b for b, a in enumerate(match_of_b))
        assert None not in M and k <= n * n
        comprobaciones += 2
    print("(a) 500 instancias con listas completas, contra la versión de listas "
          "completas")

    # (b) la cota del potencial y la estabilidad, con instancias grandes
    tachan = 0
    for _ in range(300):
        n_a, n_b = rng.randint(1, 60), rng.randint(1, 60)
        tacha = rng.random() < 0.5
        tachan += tacha
        pa, pb = instancia(n_a, n_b, rng, largo=lambda r: r.randint(0, n_b),
                           receptores_tachan=tacha)
        for orden in ("cola", "pila", "azar"):
            M, k = gale_shapley(pa, pb, orden=orden, semilla=1)
            assert k <= sum(map(len, pa)) and es_estable(M, pa, pb)
            comprobaciones += 2
    print(f"(b) 300 instancias de hasta 60 por lado, tres órdenes, {tachan} con "
          f"receptores que tachan")

    # (c) el oráculo: el resultado está entre los estables, y todos los estables
    #     dejan solos a los mismos
    for _ in range(500):
        n_a, n_b = rng.randint(1, 5), rng.randint(1, 5)
        pa, pb = instancia(n_a, n_b, rng, largo=lambda r: r.randint(0, n_b),
                           receptores_tachan=rng.random() < 0.5)
        estables = todos_estables(pa, pb)
        M, _ = gale_shapley(pa, pb, orden="azar", semilla=rng.randrange(99))
        assert M in estables
        assert len({frozenset(a for a, b in enumerate(E) if b is None)
                    for E in estables}) == 1
        comprobaciones += 2
    print("(c) 500 instancias de hasta 5 por lado, contra el oráculo")

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
        "figure.facecolor": "white", "svg.hashsalt": "ejercicio-12",
    })


def _guardar(fig, nombre_archivo):
    fig.tight_layout()
    fig.savefig(nombre_archivo, metadata={"Date": None})
    plt.close(fig)


def figura_instancia(M):
    pa, pb = EJEMPLO_A, EJEMPLO_B
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    y = {i: 3 - i for i in range(4)}
    for a in range(4):
        for b in pa[a]:
            junto = M[a] == b
            ax.plot([0, 1], [y[a], y[b]], color=OSCURO if junto else REGLA,
                    lw=2.6 if junto else 1.2, zorder=1)
    for lado, x, color, listas, etiqueta in [(0, 0, OSCURO, pa, "a"),
                                             (1, 1, CALIDO, pb, "b")]:
        for i in range(4):
            solo = (M[i] is None) if lado == 0 else (i not in M)
            ax.scatter([x], [y[i]], s=520, color="white", zorder=2,
                       edgecolors=ALARMA if solo else color, linewidths=1.6,
                       linestyle="--" if solo else "-")
            ax.text(x, y[i], f"{etiqueta}{i + 1}", ha="center", va="center", zorder=3)
            otra = "b" if etiqueta == "a" else "a"
            texto = " > ".join(f"{otra}{j + 1}" for j in listas[i])
            ax.text(x - 0.12 if lado == 0 else x + 0.12, y[i], texto,
                    ha="right" if lado == 0 else "left", va="center", fontsize=8,
                    color=ALARMA if solo else TINTA)
    ax.text(0, 3.75, "proponentes: solo los que aceptan", ha="center", fontsize=8,
            color=APAGADO)
    ax.text(1, 3.75, "receptores: listas completas", ha="center", fontsize=8,
            color=APAGADO)
    ax.set_xlim(-0.75, 1.75)
    ax.set_ylim(-0.5, 4.0)
    ax.axis("off")
    _guardar(fig, "ejercicio-12-instancia.svg")


def figura_potencial(puntos):
    fig, ax = plt.subplots(figsize=(6.0, 3.0))
    for (etiqueta, pts), color in zip(puntos.items(), [CALIDO, OSCURO]):
        ax.scatter([L for L, _ in pts], [k for _, k in pts], s=10, color=color,
                   alpha=0.75, label=etiqueta, lw=0)
    tope = max(L for pts in puntos.values() for L, _ in pts)
    ax.plot([10, tope], [10, tope], color=ALARMA, lw=1, ls="--")
    ax.text(14, 30, "propuestas = L", color=ALARMA, fontsize=8)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("L, pares en las listas de los proponentes")
    ax.set_ylabel("propuestas")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(color=REGLA, lw=0.6)
    ax.legend(frameon=False, fontsize=8, loc="lower right")
    _guardar(fig, "ejercicio-12-potencial.svg")


def figura_errores(tabla):
    fig, ax = plt.subplots(figsize=(6.0, 2.8))
    nombres = list(tabla)
    ancho = 0.36
    for k, (etiqueta, color) in enumerate([("definición vieja", APAGADO),
                                           ("definición nueva", ALARMA)]):
        alturas = [tabla[b][k] for b in nombres]
        pos = [i + (k - 0.5) * ancho for i in range(len(nombres))]
        ax.bar(pos, alturas, ancho, color=color, label=etiqueta)
        for xx, h in zip(pos, alturas):
            ax.text(xx, h + 1.5, f"{h:.0f}", ha="center", fontsize=7, color=color)
    ax.set_xticks(range(len(nombres)))
    ax.set_xticklabels(nombres, fontsize=8)
    ax.set_ylabel("% de instancias en que\nse ve el error")
    ax.set_ylim(0, 112)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color=REGLA, lw=0.6)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    _guardar(fig, "ejercicio-12-errores.svg")


if __name__ == "__main__":
    M = ejemplo_chico()
    version_vieja()
    puntos = potencial()
    estabilidad()
    optimalidad()
    tabla = errores_plantados()
    receptores_tachan()
    pruebas()
    _estilo()
    figura_instancia(M)
    figura_potencial(puntos)
    figura_errores(tabla)
    print("\nfiguras: ejercicio-12-instancia.svg, ejercicio-12-potencial.svg, "
          "ejercicio-12-errores.svg")
