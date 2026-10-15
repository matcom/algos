"""Ejercicio 12 del Tema 1: Gale-Shapley con listas incompletas.

Los bloques van en el orden de ejercicio-12.md, y cada uno imprime lo que el .md
muestra debajo de él. Ejecutarlo desde Soluciones/tema-1/alinadelanoval/:

    pip install tesserax        # para la figura
    python codigo/ejercicio-12.py
"""

# == bloque: imports (oculto)
import random
import sys
from collections import deque
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[3] / "Lectures" / "2026"))   # donde vive figuras.py

# la instancia de la figura 1 (índices desde 0: a1 es 0, b1 es 0)
pref_a = [[0, 1], [0], [1, 0, 2], [1]]
pref_b = [[2, 0, 1, 3], [3, 0, 2, 1], [0, 1, 2, 3], [0, 1, 2, 3]]

# == bloque: verificador (oculto)
def pares_bloqueantes(M, pref_a, pref_b):
    pareja_de_b = {b: a for a, b in enumerate(M) if b is not None}
    return [(a, b) for a in range(len(M)) for b in pref_a[a]
            if b != M[a]
            and (M[a] is None or pref_a[a].index(b) < pref_a[a].index(M[a]))
            and (b not in pareja_de_b
                 or pref_b[b].index(a) < pref_b[b].index(pareja_de_b[b]))]

# == bloque: figura (oculto)
inestable = [0, None, 1, None]                  # a1–b1 y a3–b2; a2 y a4 solos
assert pares_bloqueantes(inestable, pref_a, pref_b) == [(3, 1)]   # solo a4–b2
assert 2 not in pref_a[1]                       # a2–b3: los dos solos, pero no bloquea
try:
    import figuras as F
except ImportError:
    print("sin tesserax no se regenera la figura")
else:
    n = len(pref_a)
    paso_y, xa, xb = 34.0, 0.0, 190.0
    with F.Canvas() as canvas:
        pos_a = [F.Point(xa, k * paso_y) for k in range(n)]
        pos_b = [F.Point(xb, k * paso_y) for k in range(n)]
        F.Line(pos_a[1], pos_b[2], stroke=F.APAGADO, width=1.0)            # a2–b3
        for i, j in enumerate(inestable):
            if j is not None:
                F.Line(pos_a[i], pos_b[j], stroke=F.ACENTO, width=1.6)
        for i, j in pares_bloqueantes(inestable, pref_a, pref_b):
            F.Line(pos_a[i], pos_b[j], stroke=F.ALARMA, width=1.6)
        for k in range(n):
            for p, nombre, lista, lado in ((pos_a[k], f"a{F.sub(k + 1)}", pref_a[k], -1),
                                           (pos_b[k], f"b{F.sub(k + 1)}", pref_b[k], 1)):
                F.Circle(9, fill=F.Colors.White, stroke=F.TINTA, width=0.9).move_to(p)
                F._txt(nombre, p, color=F.TINTA, size=F.PIE)
                otro = "b" if lado < 0 else "a"
                texto = " > ".join(f"{otro}{F.sub(x + 1)}" for x in lista)
                F._txt(texto, F.Point(p.x + lado * 18, p.y), color=F.APAGADO, size=F.PIE,
                       anchor="end" if lado < 0 else "start")
        F._txt("proponentes y sus listas", F.Point(xa - 40, -24), color=F.APAGADO, size=F.PIE)
        F._txt("receptores y sus listas", F.Point(xb + 40, -24), color=F.APAGADO, size=F.PIE)
    figura = F._figura(canvas, "ejercicio-12-bloqueante", "")
    svg = figura[figura.index("<svg"):figura.index("</svg>") + len("</svg>")]
    vb = svg.split('viewBox="')[1].split('"')[0].split()   # fondo blanco para GitHub
    fondo = f'<rect x="{vb[0]}" y="{vb[1]}" width="{vb[2]}" height="{vb[3]}" fill="white"/>'
    (AQUI.parent / "figuras" / "ejercicio-12-bloqueante.svg").write_text(
        svg.replace(">", ">" + fondo, 1), encoding="utf-8")

# == bloque: algoritmo
def gale_shapley(pref_a, pref_b, orden="cola", semilla=0, traza=None):
    n = len(pref_a)
    rango = [[0] * n for _ in range(n)]           # rango[b][a]: lugar de a en la lista de b
    for b in range(n):
        for lugar, a in enumerate(pref_b[b]):
            rango[b][a] = lugar
    siguiente = [0] * n                           # a qué lugar de su lista va a proponer a
    pareja_de_b = [None] * n
    libres = deque(a for a in range(n) if pref_a[a])                  # nuevo
    azar = random.Random(semilla)
    propuestas = 0

    while libres:
        if orden == "azar":
            libres.rotate(azar.randrange(len(libres)))
        a = libres.popleft() if orden == "cola" else libres.pop()
        b = pref_a[a][siguiente[a]]
        siguiente[a] += 1
        propuestas += 1
        actual = pareja_de_b[b]
        suelto = None                                                 # nuevo
        if actual is None:
            pareja_de_b[b] = a
        elif rango[b][a] < rango[b][actual]:
            pareja_de_b[b] = a
            suelto = actual                                           # nuevo
        else:
            suelto = a                                                # nuevo
        if suelto is not None and siguiente[suelto] < len(pref_a[suelto]):   # nuevo
            libres.append(suelto)                                     # nuevo
        if traza is not None:
            traza.append((a, b, actual, pareja_de_b[b]))

    M = [None] * n                                # M[a] = None: a se queda solo
    for b, a in enumerate(pareja_de_b):
        if a is not None:                                             # nuevo
            M[a] = b
    return M, propuestas

# == bloque: traza (asis)
SUB = "₀₁₂₃₄₅₆₇₈₉"
n_ = lambda letra, i: letra + "".join(SUB[int(c)] for c in str(i + 1))
traza = []
M, propuestas = gale_shapley(pref_a, pref_b, traza=traza)
propuesto = set()
print("| paso | proponente | receptor | tenía | se queda con | qué pasa |")
print("|---|---|---|---|---|---|")
for paso, (a, b, actual, queda) in enumerate(traza, start=1):
    propuesto.add((a, b))
    if actual is None:
        pasa, suelto = "acepta", None
    elif queda == a:
        pasa, suelto = f"cambia; {n_('a', actual)} queda libre", actual
    else:
        pasa, suelto = f"rechaza a {n_('a', a)}", a
    if suelto is not None and all((suelto, x) in propuesto for x in pref_a[suelto]):
        pasa = pasa.replace(" queda libre", "") + f"; {n_('a', suelto)} se queda solo"
    print(f"| {paso} | {n_('a', a)} | {n_('b', b)} | "
          f"{'—' if actual is None else n_('a', actual)} | {n_('a', queda)} | {pasa} |")
pares = ", ".join(f"{n_('a', a)}–{n_('b', b)}" for a, b in enumerate(M) if b is not None)
solos = " y ".join(n_("a", a) for a, b in enumerate(M) if b is None)
print(f"\nResultado: {pares}; {solos} se quedan solos, en {propuestas} propuestas.")
assert pares_bloqueantes(M, pref_a, pref_b) == []
assert sum(len(l) for l in pref_a) - propuestas == 1           # Φ termina en 1

# == bloque: comprobacion
def instancia(n, rng):
    return ([rng.sample(range(n), rng.randint(0, n)) for _ in range(n)],
            [rng.sample(range(n), n) for _ in range(n)])

rng = random.Random(8)
print(f"{'n':>3} {'instancias':>11} {'bloqueantes':>12} {'propuestas':>11} {'suma de listas':>15}")
for n, veces in [(5, 400), (20, 100), (60, 20)]:
    bloqueantes, propuestas, cota = 0, 0, 0
    for _ in range(veces):
        pref_a, pref_b = instancia(n, rng)
        for orden in ("cola", "pila", "azar"):              # para cualquier orden
            assert not pares_bloqueantes(gale_shapley(pref_a, pref_b, orden, n)[0],
                                         pref_a, pref_b)
        M, k = gale_shapley(pref_a, pref_b, orden="azar", semilla=n)
        bloqueantes += len(pares_bloqueantes(M, pref_a, pref_b))
        assert k <= sum(len(lista) for lista in pref_a)   # la cota del potencial
        propuestas += k
        cota += sum(len(lista) for lista in pref_a)
    print(f"{n:>3} {veces:>11} {bloqueantes:>12} {propuestas / veces:>11.1f} {cota / veces:>15.1f}")
