"""Ejercicio 12 - Gale-Shapley con listas incompletas.

Las secciones siguen el orden del texto, salvo la 2 (que el texto usa en la seccion 5). El .tex incluye
con \\lstinputlisting dos de las funciones marcadas inicio/fin (la version vigilada y la pareja bloqueante);
el algoritmo va como pseudocodigo con su rango de lineas. Todo lo que se imprime es ASCII (el .tex lo pega).

Convenciones: los proponentes son 0..n_a-1 y los receptores 0..n_b-1 (se imprimen como a1.., b1..).
L[a] = receptores aceptables para a, de mejor a peor. R[b][a] = lugar de a en la lista de b, definido
solo para los a que listan a b (menor numero = mejor).
"""
import itertools
import random
from collections import deque


# ---- inicio del algoritmo
def gale_shapley_incompleto(L, R, orden="cola", semilla=0, traza=None):
    """Devuelve (M, propuestas), con M = {proponente: receptor}."""
    siguiente = [0] * len(L)          # siguiente[a]: propuestas que a ya hizo
    pareja_de_b = {}
    libres = deque(a for a in range(len(L)) if L[a])    # libres con pendientes
    azar = random.Random(semilla)
    propuestas = 0
    while libres:
        if orden == "azar":
            libres.rotate(azar.randrange(len(libres)))
        a = libres.popleft() if orden == "cola" else libres.pop()
        b = L[a][siguiente[a]]
        siguiente[a] += 1
        propuestas += 1
        actual = pareja_de_b.get(b)
        if actual is None:                  # b libre: acepta
            pareja_de_b[b], perdedor = a, None
        elif R[b][a] < R[b][actual]:        # b prefiere a: desplaza a su pareja
            pareja_de_b[b], perdedor = a, actual
        else:                               # b rechaza a
            perdedor = a
        if perdedor is not None and siguiente[perdedor] < len(L[perdedor]):
            libres.append(perdedor)         # sigue libre, con pendientes
        if traza is not None:
            traza.append((a, b, actual, pareja_de_b[b]))
    return {a: b for b, a in pareja_de_b.items()}, propuestas
# ---- fin del algoritmo


# ---- inicio de la pareja bloqueante
def pares_bloqueantes(M, L, R):
    """(a, b) mutuamente aceptables tales que (a libre o a prefiere b a M[a])
    y (b libre o b prefiere a a su pareja en M)."""
    pareja_de_b = {b: a for a, b in M.items()}
    bloqueantes = []
    for a in range(len(L)):
        for lugar, b in enumerate(L[a]):                # b es aceptable para a
            a_quiere = a not in M or lugar < L[a].index(M[a])
            actual = pareja_de_b.get(b)
            b_quiere = actual is None or R[b][a] < R[b][actual]
            if a_quiere and b_quiere:
                bloqueantes.append((a, b))
    return bloqueantes
# ---- fin de la pareja bloqueante


# ---- inicio de la version vigilada
def gs_vigilado(L, R):
    """GS comprobando en cada vuelta el potencial y los invariantes.
    Devuelve (vueltas, violaciones)."""
    sig = [0] * len(L)
    pareja_de_b = {}
    libres = deque(a for a in range(len(L)) if L[a])
    phi = sum(map(len, L))
    rango_previo = {}                   # rango de la pareja de b, vuelta anterior
    vueltas = viol = 0
    while libres:
        a = libres.popleft()
        b = L[a][sig[a]]
        sig[a] += 1
        vueltas += 1
        actual = pareja_de_b.get(b)
        perdedor = a
        if actual is None or R[b][a] < R[b][actual]:
            pareja_de_b[b], perdedor = a, actual
        if perdedor is not None and sig[perdedor] < len(L[perdedor]):
            libres.append(perdedor)
        nuevo = sum(len(L[x]) - sig[x] for x in range(len(L)))
        viol += nuevo != phi - 1                    # el potencial baja 1
        phi = nuevo
        r = R[b][pareja_de_b[b]]
        viol += b in rango_previo and r > rango_previo[b]   # I1
        viol += r > R[b][a]                         # Lema 2: a o algo mejor
        rango_previo[b] = r
        viol += any(L[x][sig[x] - 1] != y           # I2: el ultimo al que
                    for y, x in pareja_de_b.items())    # le propuso
        emparejados = set(pareja_de_b.values())
        pendientes = {x for x in range(len(L))
                      if x not in emparejados and sig[x] < len(L[x])}
        viol += sorted(libres) != sorted(pendientes)    # I3: la cola
    return vueltas, viol
# ---- fin de la version vigilada


def gs_con_descarte(L, R):
    """La variante donde la cola guarda a todos y se descarta al agotado al sacarlo.
    Devuelve (M, propuestas, vueltas): una vuelta de descarte no es una propuesta."""
    siguiente = [0] * len(L)
    pareja_de_b = {}
    libres = deque(range(len(L)))
    propuestas = vueltas = 0
    while libres:
        vueltas += 1
        a = libres.popleft()
        if siguiente[a] >= len(L[a]):
            continue
        b = L[a][siguiente[a]]
        siguiente[a] += 1
        propuestas += 1
        actual = pareja_de_b.get(b)
        if actual is None:
            pareja_de_b[b] = a
        elif R[b][a] < R[b][actual]:
            pareja_de_b[b] = a
            libres.append(actual)
        else:
            libres.append(a)
    return {a: b for b, a in pareja_de_b.items()}, propuestas, vueltas


def pares_bloqueantes_ingenuo(M, L, R):
    """Error tipico: solo compara preferencias cuando los dos tienen pareja."""
    pareja_de_b = {b: a for a, b in M.items()}
    return [(a, b) for a in M for b in L[a]
            if b in pareja_de_b and L[a].index(b) < L[a].index(M[a]) and R[b][a] < R[b][pareja_de_b[b]]]


def pares_bloqueantes_con_vacio(M, L, R):
    """La misma definicion con el vacio en las listas: lista(a) > vacio > no listados."""
    tope = 10 ** 6
    pareja_de_b = {b: a for a, b in M.items()}
    bloq = []
    for a in range(len(L)):
        for b in range(len(R)):
            rango_a = lambda x: L[a].index(x) if x in L[a] else tope + 1 if x is not None else tope
            rango_b = lambda x: R[b].get(x, tope + 1) if x is not None else tope
            if rango_a(b) < rango_a(M.get(a)) and rango_b(a) < rango_b(pareja_de_b.get(b)):
                bloq.append((a, b))
    return bloq


def todos_los_emparejamientos(L):
    """Todos los emparejamientos M contenidos en las parejas aceptables (parciales incluidos)."""
    def rec(a):
        if a == len(L):
            yield {}
            return
        for resto in rec(a + 1):
            yield dict(resto)
            for b in L[a]:
                if b not in resto.values():
                    m = dict(resto)
                    m[a] = b
                    yield m
    return rec(0)


def estables(L, R):
    return [M for M in todos_los_emparejamientos(L) if not pares_bloqueantes(M, L, R)]


def instancia_aleatoria(n_a, n_b, rng, p=0.6):
    """Cada receptor es aceptable para cada proponente con probabilidad p; cada receptor ordena
    al azar a los proponentes que lo listan."""
    L = []
    for a in range(n_a):
        aceptables = [b for b in range(n_b) if rng.random() < p]
        rng.shuffle(aceptables)
        L.append(aceptables)
    R = [dict() for _ in range(n_b)]
    for b in range(n_b):
        quienes = [a for a in range(n_a) if b in L[a]]
        rng.shuffle(quienes)
        for lugar, a in enumerate(quienes):
            R[b][a] = lugar
    return L, R


def nombre(M):
    return "{" + ", ".join(f"a{a + 1}-b{b + 1}" for a, b in sorted(M.items())) + "}"


# ================================================================== 1. el ejemplo que atraviesa el ejercicio
print("== 1. el ejemplo que usamos en todo el ejercicio ==")
EL = [[1, 0], [0, 1], [0], [1, 2]]
ER = [{2: 0, 1: 1, 0: 2}, {0: 0, 3: 1, 1: 2}, {3: 0}]
for a, lista in enumerate(EL):
    print(f"a{a + 1}: " + " > ".join(f"b{b + 1}" for b in lista))
for b, rango in enumerate(ER):
    print(f"b{b + 1} (lo listan " + ",".join(f"a{a + 1}" for a in sorted(rango)) + "): "
          + " > ".join(f"a{a + 1}" for a in sorted(rango, key=rango.get)))
traza = []
EM, eprop = gale_shapley_incompleto(EL, ER, traza=traza)
print()
print(f"{'paso':>4} {'propone':>8} {'a':>3} {'tenia':>6} {'queda con':>10} {'phi':>4}  que pasa")
phi = sum(len(l) for l in EL)
for k, (a, b, actual, queda) in enumerate(traza, start=1):
    phi -= 1
    if actual is None:
        que = "acepta"
    elif queda == a:
        que = f"cambia; a{actual + 1} queda libre"
    else:
        que = f"rechaza a a{a + 1}"
    print(f"{k:>4} {'a' + str(a + 1):>8} {'b' + str(b + 1):>3} {('a' + str(actual + 1)) if actual is not None else '-':>6} "
          f"{'a' + str(queda + 1):>10} {phi:>4}  {que}")
print(f"resultado: {nombre(EM)} en {eprop} propuestas")
print("libres: " + ", ".join(f"a{a + 1}" for a in range(len(EL)) if a not in EM)
      + " (agoto su lista: " + " > ".join(f"b{b + 1}" for b in EL[1]) + ")")
print(f"parejas bloqueantes de ese resultado: {pares_bloqueantes(EM, EL, ER)}")

print()
print("las cuatro clausulas de la pareja bloqueante, en emparejamientos del ejemplo:")
etiquetas = {(False, False): "a y b con pareja", (True, False): "a libre, b con pareja",
             (False, True): "a con pareja, b libre", (True, True): "a y b libres"}
vistos = {}
for M in sorted(todos_los_emparejamientos(EL), key=lambda m: (len(m), sorted(m.items()))):
    pb = {b: a for a, b in M.items()}
    for (a, b) in pares_bloqueantes(M, EL, ER):
        clave = (a not in M, b not in pb)
        if clave not in vistos:
            vistos[clave] = (M, (a, b))
for clave in [(False, False), (True, False), (False, True), (True, True)]:
    M, (a, b) = vistos[clave]
    print(f"  {etiquetas[clave]:<22} M = {nombre(M) if M else '{}':<22} bloquea (a{a + 1}, b{b + 1})")

# ================================================================== 2. la definicion con el vacio
print()
print("== 2. la definicion con el vacio en las listas ==")
rng = random.Random(5)
dif = tot = 0
for _ in range(300):
    n_a, n_b = rng.randint(1, 6), rng.randint(1, 6)
    L, R = instancia_aleatoria(n_a, n_b, random.Random(rng.randint(0, 10 ** 9)))
    for M in itertools.islice(todos_los_emparejamientos(L), 40):
        tot += 1
        dif += set(pares_bloqueantes(M, L, R)) != set(pares_bloqueantes_con_vacio(M, L, R))
print(f"vacio en las listas vs cuatro clausulas: {dif} diferencias en {tot} emparejamientos")

# ================================================================== 3. potencial e invariantes, ejecutados
print()
print("== 3. el potencial y los invariantes, ejecutados vuelta a vuelta ==")
rng = random.Random(0)
vueltas_tot = viol = 0
inst = []
for _ in range(3000):
    n_a, n_b = rng.randint(1, 15), rng.randint(1, 15)
    L, R = instancia_aleatoria(n_a, n_b, random.Random(rng.randint(0, 10 ** 9)))
    inst.append((L, R))
    v, k = gs_vigilado(L, R)
    vueltas_tot += v
    viol += k
print(f"3000 instancias: {vueltas_tot} vueltas comprobadas, violaciones (deberia ser 0): {viol}")
dentro = sum(gale_shapley_incompleto(L, R)[1] <= sum(map(len, L)) for L, R in inst)
print(f"propuestas <= suma de los largos de las listas: {dentro} de 3000")

# ================================================================== 4. el costo exacto
print()
print("== 4. cuantas propuestas hace: una formula exacta ==")
ok = 0
for L, R in inst:
    M, prop = gale_shapley_incompleto(L, R)
    formula = sum(L[a].index(M[a]) + 1 if a in M else len(L[a]) for a in range(len(L)))
    ok += prop == formula
print("propuestas = suma pos(M(a)) (emparejados) + suma |L(a)| (libres):")
print(f"   coincide en {ok} de 3000 instancias")
excede = peor = 0
for L, R in inst:
    _, prop, vueltas = gs_con_descarte(L, R)
    excede += vueltas > sum(map(len, L))
    peor = max(peor, vueltas - sum(map(len, L)))
print(f"cola con agotados: vueltas > suma|L| en {excede} de 3000 instancias")
print(f"   (exceso maximo {peor}); con 3 listas vacias: suma = 0, vueltas = "
      f"{gs_con_descarte([[], [], []], [dict()])[2]}")

# ================================================================== 5. estabilidad
print()
print("== 5. estabilidad ==")
parejas_ok = estable = 0
for L, R in inst:
    M, _ = gale_shapley_incompleto(L, R)
    parejas_ok += all(b in L[a] for a, b in M.items()) and len(set(M.values())) == len(M)
    estable += not pares_bloqueantes(M, L, R)
print(f"emparejamiento valido (M en E, sin repetir receptor): {parejas_ok} de 3000")
print(f"sin parejas bloqueantes (deberia ser 3000 de 3000): {estable} de 3000")
rng = random.Random(4)
casos = ingenuo = correcto = 0
for _ in range(1000):
    n_a, n_b = rng.randint(2, 12), rng.randint(2, 12)
    L, R = instancia_aleatoria(n_a, n_b, random.Random(rng.randint(0, 10 ** 9)))
    M, _ = gale_shapley_incompleto(L, R)
    if not M:
        continue
    a = rng.choice(sorted(M))
    roto = {x: y for x, y in M.items() if x != a}                 # a y su pareja quedan libres
    casos += 1
    ingenuo += not pares_bloqueantes_ingenuo(roto, L, R)
    correcto += bool(pares_bloqueantes(roto, L, R))
print(f"romper una pareja ({casos} casos): el chequeo ingenuo dice 'estable' en {ingenuo};")
print(f"   el chequeo con las cuatro clausulas encuentra la pareja bloqueante en {correcto}")

# ================================================================== 6. lo que se hereda de C3
print()
print("== 6. lo que se hereda de C3, con todos los emparejamientos enumerados ==")
rng = random.Random(3)
n_inst = 600
cuenta = dict(estable=0, optimo=0, peor=0, mismos=0, ordenes=0, varios=0, libres=0,
              varios_mismos=0, varios_optimo=0)
for _ in range(n_inst):
    n_a, n_b = rng.randint(3, 5), rng.randint(3, 5)
    L, R = instancia_aleatoria(n_a, n_b, random.Random(rng.randint(0, 10 ** 9)), p=0.85)
    E = estables(L, R)
    M, _ = gale_shapley_incompleto(L, R)
    cuenta["estable"] += M in E
    mejor = lambda a: min((e[a] for e in E if a in e), key=L[a].index, default=None)
    cuenta["optimo"] += all(M.get(a) == mejor(a) for a in range(n_a))
    par = lambda e, b: {v: k for k, v in e.items()}.get(b)
    peor = lambda b: max((par(e, b) for e in E if par(e, b) is not None), key=lambda a: R[b][a], default=None)
    cuenta["peor"] += all(par(M, b) == peor(b) for b in range(n_b))
    cuenta["mismos"] += len({(frozenset(e), frozenset(e.values())) for e in E}) == 1
    resultados = [gale_shapley_incompleto(L, R, o, s)[0] for o, s in (("cola", 0), ("pila", 0), ("azar", 1), ("azar", 2))]
    cuenta["ordenes"] += all(r == resultados[0] for r in resultados)
    cuenta["varios"] += len(E) > 1
    cuenta["libres"] += len(M) < n_a
    if len(E) > 1:
        cuenta["varios_mismos"] += len({(frozenset(e), frozenset(e.values())) for e in E}) == 1
        cuenta["varios_optimo"] += all(M.get(a) == mejor(a) for a in range(n_a))
print(f"{n_inst} instancias de 3 a 5 por lado: {cuenta['varios']} con mas de un estable,")
print(f"   {cuenta['libres']} con algun proponente libre:")
print(f"  el resultado de GS es uno de los estables: {cuenta['estable']} de {n_inst}")
print(f"  cada proponente obtiene su mejor pareja valida: {cuenta['optimo']} de {n_inst}")
print(f"  cada receptor emparejado obtiene su peor pareja valida: {cuenta['peor']} de {n_inst}")
print(f"  todos los estables emparejan a los mismos agentes: {cuenta['mismos']} de {n_inst}")
print(f"  mismo resultado con cuatro ordenes de ejecucion: {cuenta['ordenes']} de {n_inst}")
print(f"  solo en las {cuenta['varios']} con varios estables: optimo {cuenta['varios_optimo']}, mismos agentes {cuenta['varios_mismos']}")

# ================================================================== 7. cuanto cuesta en promedio
print()
print("== 7. n_a = n_b = 12: libres y propuestas segun la probabilidad de aceptabilidad p ==")
print(f"{'p':>5} {'proponentes libres':>19} {'propuestas / suma|L|':>21}")
rng = random.Random(6)
for p in (0.2, 0.4, 0.6, 0.8, 1.0):
    libres_f = razon = 0.0
    for _ in range(300):
        L, R = instancia_aleatoria(12, 12, random.Random(rng.randint(0, 10 ** 9)), p)
        M, prop = gale_shapley_incompleto(L, R)
        libres_f += (12 - len(M)) / 12
        razon += prop / sum(map(len, L)) if sum(map(len, L)) else 0
    print(f"{p:>5} {libres_f / 300:>19.3f} {razon / 300:>21.3f}")
