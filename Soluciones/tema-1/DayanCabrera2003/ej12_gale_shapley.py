"""Ejercicio 12: Gale-Shapley con listas incompletas (C3 sec. 6-9).
Proponentes a = 0..n-1, receptores b = 0..m-1. L_a: lista ordenada de receptores aceptables para a (mejor primero);
L_b: lista ordenada de proponentes aceptables para b. El par (a,b) es aceptable si b esta en L_a y a esta en L_b."""
import itertools
import random
from collections import deque

random.seed(12)


def gale_shapley(La, Lb, orden="cola", semilla=0, traza=None, defecto=None):
    """Devuelve (pareja_de_a, propuestas). 'defecto' activa variantes con error (para la seccion 8)."""
    n, m = len(La), len(Lb)
    rango = [{a: lugar for lugar, a in enumerate(Lb[b])} for b in range(m)]
    sig = [0] * n
    pareja_de_b = [None] * m
    libres = deque(a for a in range(n) if La[a])               # un proponente con lista vacia queda solo desde el principio
    azar = random.Random(semilla)
    propuestas = 0
    pasos = 0
    while libres:
        pasos += 1
        if defecto == "reinicia" and pasos > 5000:
            return None, propuestas                              # no termina
        if orden == "azar":
            libres.rotate(azar.randrange(len(libres)))
        a = libres.popleft() if orden == "cola" else libres.pop()
        if defecto == "reinicia" and sig[a] == len(La[a]):
            sig[a] = 0                                           # (variante) vuelve a empezar su lista
        b = La[a][sig[a]]
        sig[a] += 1
        propuestas += 1
        actual = pareja_de_b[b]
        if a not in rango[b] and defecto != "acepta_no_listado":
            acepta = False                                       # b rechaza a quien no lista
        elif actual is None:
            acepta = True
        elif a in rango[b] and actual in rango[b]:
            acepta = rango[b][a] < rango[b][actual]
        elif a not in rango[b]:                                  # (variante) a no esta listado: se acepta si 'es mejor que estar solo'
            acepta = False
        else:
            acepta = True
        if acepta:
            pareja_de_b[b] = a
            if actual is not None:
                if sig[actual] < len(La[actual]) or defecto == "reinicia":
                    libres.append(actual)
        else:
            if sig[a] < len(La[a]):
                libres.append(a)
            elif defecto == "reinicia":
                sig[a] = 0                                       # (variante) vuelve a empezar su lista
                libres.append(a)
        if traza is not None:
            traza.append((a, b, actual, pareja_de_b[b], acepta))
        # un proponente que agoto su lista y fue rechazado no vuelve a la cola: queda solo para siempre
    M = [None] * n
    for b, a in enumerate(pareja_de_b):
        if a is not None:
            M[a] = b
    return M, propuestas


def verificador(M, La, Lb):
    """Verificador independiente (fuerza bruta). Devuelve (racional, [pares bloqueantes])."""
    n, m = len(La), len(Lb)
    rank_a = [{b: r for r, b in enumerate(La[a])} for a in range(n)]
    rank_b = [{a: r for r, a in enumerate(Lb[b])} for b in range(m)]
    pareja_b = {}
    for a in range(n):
        if M[a] is not None:
            assert M[a] not in pareja_b
            pareja_b[M[a]] = a
    racional = all(M[a] is None or (M[a] in rank_a[a] and a in rank_b[M[a]]) for a in range(n))
    bloq = []
    for a in range(n):
        for b in range(m):
            if M[a] == b:
                continue
            if b not in rank_a[a] or a not in rank_b[b]:
                continue                                         # no es mutuamente aceptable
            a_quiere = M[a] is None or (M[a] in rank_a[a] and rank_a[a][b] < rank_a[a][M[a]]) or M[a] not in rank_a[a]
            actual = pareja_b.get(b)
            b_quiere = actual is None or (actual in rank_b[b] and rank_b[b][a] < rank_b[b][actual]) or actual not in rank_b[b]
            if a_quiere and b_quiere:
                bloq.append((a, b))
    return racional, bloq


def emparejamientos(n, m):
    """Todos los emparejamientos parciales: cada proponente, solo o con un receptor distinto."""
    def rec(a, usados, acum):
        if a == n:
            yield list(acum)
            return
        acum.append(None)
        yield from rec(a + 1, usados, acum)
        acum.pop()
        for b in range(m):
            if b not in usados:
                acum.append(b)
                yield from rec(a + 1, usados | {b}, acum)
                acum.pop()
    yield from rec(0, frozenset(), [])


def todos_estables(La, Lb):
    n, m = len(La), len(Lb)
    res = []
    for M in emparejamientos(n, m):
        rac, bloq = verificador(M, La, Lb)
        if rac and not bloq:
            res.append(M)
    return res


def instancia(n, m, pa, pb, rng, receptores_completos=False):
    """Listas incompletas aleatorias: a lista a b con prob. pa; b lista a a con prob. pb; ordenes al azar."""
    La = [[b for b in rng.sample(range(m), m) if rng.random() < pa] for _ in range(n)]
    if receptores_completos:
        Lb = [rng.sample(range(n), n) for _ in range(m)]
    else:
        Lb = [[a for a in rng.sample(range(n), n) if rng.random() < pb] for _ in range(m)]
    return La, Lb


def nombre(a): return f"a{a + 1}"
def nombreb(b): return f"b{b + 1}"


print("=== 1. Una instancia con n != m, listas incompletas, y su traza ===")
La = [[0, 1, 2], [0, 2], [0, 1], [1]]
Lb = [[1, 2, 0], [0, 3], [0]]
for a, l in enumerate(La):
    print(f"  {nombre(a)} lista: {' > '.join(nombreb(b) for b in l)}")
for b, l in enumerate(Lb):
    print(f"  {nombreb(b)} lista: {' > '.join(nombre(a) for a in l) if l else '(nadie)'}")
tz = []
M, prop = gale_shapley(La, Lb, traza=tz)
print("  paso  a  propone a  tenia   se queda con  que pasa")
for i, (a, b, actual, nuevo, acepta) in enumerate(tz, 1):
    print(f"  {i:>4}  {nombre(a)}  {nombreb(b):>9}  {nombre(actual) if actual is not None else '-':>5}  {nombre(nuevo) if nuevo is not None else '-':>11}  "
          f"{'acepta' if acepta else 'rechaza'}")
print("  resultado:", ", ".join(f"{nombre(a)}-{nombreb(M[a])}" if M[a] is not None else f"{nombre(a)} solo" for a in range(len(La))),
      f"({prop} propuestas; suma |L_a| = {sum(len(l) for l in La)})")
rac, bloq = verificador(M, La, Lb)
print(f"  verificador independiente: individualmente racional = {rac}, pares bloqueantes = {bloq}")
print(f"  emparejamientos estables (fuerza bruta, {sum(1 for _ in emparejamientos(4, 3))} emparejamientos posibles):",
      [[(nombre(a) + '-' + nombreb(x)) if x is not None else nombre(a) + ' solo' for a, x in enumerate(E)] for E in todos_estables(La, Lb)])

print()
print("=== 2. Por que hace falta la racionalidad individual (a) ===")
La0, Lb0 = [[]], [[0]]            # a no lista a nadie; b lista a a
M0 = [0]
print(f"  a lista: (nadie); b lista: a1. Emparejamiento {{a1-b1}}: racional = {verificador(M0, La0, Lb0)[0]}, "
      f"pares bloqueantes en el sentido ingenuo = {[p for p in verificador(M0, La0, Lb0)[1]]}")
print("  Sin pares bloqueantes, pero a1 queda con alguien que no lista: no es estable. El vacio {a1 solo, b1 solo} si lo es:",
      verificador([None], La0, Lb0))
print("  Algoritmo sobre esa instancia:", gale_shapley(La0, Lb0))

print()
print("=== 3. Experimento principal: instancias aleatorias pequenas (n, m <= 5), TODOS los emparejamientos enumerados ===")
rng = random.Random(1212)
tot = distintos_n_m = receptores_completos = 0
estable = igual_ordenes = optimo = rural = identidad = cota = pesimo = 0
vacios = 0
for it in range(4000):
    n, m = rng.randint(1, 5), rng.randint(1, 5)
    comp = (it % 4 == 0)
    pa, pb = rng.choice([0.4, 0.6, 0.8, 1.0]), rng.choice([0.4, 0.6, 0.8, 1.0])
    La, Lb = instancia(n, m, pa, pb, rng, receptores_completos=comp)
    tot += 1
    distintos_n_m += n != m
    receptores_completos += comp
    resultados = [gale_shapley(La, Lb, orden=o, semilla=s) for o, s in (("cola", 0), ("pila", 0), ("azar", 1), ("azar", 2))]
    M, prop = resultados[0]
    igual_ordenes += all(r[0] == M and r[1] == prop for r in resultados)
    rac, bloq = verificador(M, La, Lb)
    estable += rac and not bloq
    est = todos_estables(La, Lb)
    assert M in est
    # optimalidad para quien propone
    ok = True
    for a in range(n):
        mejores = [E[a] for E in est if E[a] is not None]
        if mejores:
            mejor = min(mejores, key=lambda b: La[a].index(b))
            ok &= M[a] == mejor
        else:
            ok &= M[a] is None
    optimo += ok
    # hospitales rurales: mismo conjunto de emparejados en todo estable
    ref_a = {a for a in range(n) if est[0][a] is not None}
    ref_b = {est[0][a] for a in ref_a}
    rural += all({a for a in range(n) if E[a] is not None} == ref_a and {E[a] for a in ref_a} == ref_b for E in est)
    # pesimalidad para receptores: todo b emparejado en M recibe en TODO estable E a alguien que prefiere (o iguala)
    pb0 = {M[a]: a for a in range(n) if M[a] is not None}
    ok_p = True
    for E in est:
        pbE = {E[a]: a for a in range(n) if E[a] is not None}
        for b, a0 in pb0.items():
            ok_p &= b in pbE and Lb[b].index(pbE[b]) <= Lb[b].index(a0)
    pesimo += ok_p
    # identidad de propuestas
    suma = sum(len(l) for l in La)
    esperado = sum(len(La[a]) if M[a] is None else La[a].index(M[a]) + 1 for a in range(n))
    identidad += prop == esperado
    cota += prop <= suma
    vacios += all(x is None for x in M)
print(f"  {tot} instancias ({distintos_n_m} con n != m, {receptores_completos} con receptores de lista completa, {vacios} con emparejamiento vacio)")
print(f"  (i)   el resultado de Gale-Shapley es estable (verificador independiente):                {estable} de {tot}")
print(f"  (ii)  el resultado no depende del orden (cola, pila, dos azares; mismo M y mismas propuestas): {igual_ordenes} de {tot}")
print(f"  (iii) optimo para quien propone (mejor pareja estable, o solo si no tiene ninguna):          {optimo} de {tot}")
print(f"  (iv)  hospitales rurales: mismo conjunto de emparejados en TODO emparejamiento estable:       {rural} de {tot}")
print(f"  (iv') pesimalidad: en M0 cada receptor emparejado queda con su PEOR pareja valida (en todo estable lo iguala o mejora): {pesimo} de {tot}")
print(f"  (v)   propuestas = sum_{{a solo}} |L_a| + sum_{{a emparejado}} lugar de su pareja:                {identidad} de {tot}")
print(f"  (vi)  propuestas <= sum |L_a|:                                                               {cota} de {tot}")
assert estable == igual_ordenes == optimo == rural == identidad == cota == pesimo == tot

print()
print("=== 4. Propuestas contra sum |L_a|: instancias grandes y la igualdad ===")
print(f"  {'n':>5} {'m':>5} {'sum |L_a|':>10} {'propuestas':>11} {'cociente':>9} {'proponentes solos':>18}")
rng = random.Random(44)
for n, m, pa, pb in ((50, 50, 1.0, 1.0), (50, 50, 0.3, 0.3), (200, 100, 0.5, 0.5), (100, 200, 0.5, 0.5), (400, 400, 0.1, 1.0), (400, 400, 0.1, 0.1)):
    La, Lb = instancia(n, m, pa, pb, rng)
    M, prop = gale_shapley(La, Lb, orden="azar", semilla=3)
    suma = sum(len(l) for l in La)
    assert verificador(M, La, Lb) == (True, [])
    print(f"  {n:>5} {m:>5} {suma:>10} {prop:>11} {prop / suma:>9.3f} {sum(x is None for x in M):>18}")
print("  Igualdad propuestas = sum |L_a|: sucede exactamente cuando todo proponente queda solo o con el ULTIMO de su lista.")
La, Lb = [[0, 1, 2], [0, 1], [2, 0]], [[], [], []]
print(f"  (a) receptores con listas vacias: nadie acepta; propuestas {gale_shapley(La, Lb)[1]} = sum |L_a| = {sum(map(len, La))}")
La, Lb = [[0, 1], [0]], [[1, 0], [0]]
M, prop = gale_shapley(La, Lb)
print(f"  (b) con emparejamientos: a1:[b1,b2], a2:[b1]; b1: a2>a1; b2: a1 -> M = {M}, propuestas {prop} = sum |L_a| = {sum(map(len, La))}"
      f" (a1 con el ultimo de su lista, a2 con el unico)")
print("  Complejidad con listas completas (n x n), peor caso sobre TODAS las instancias de n = 2, 3:")
for n in (2, 3):
    perms = list(itertools.permutations(range(n)))
    peor = 0
    for La in itertools.product(perms, repeat=n):
        for Lb in itertools.product(perms, repeat=n):
            peor = max(peor, gale_shapley([list(x) for x in La], [list(x) for x in Lb])[1])
    print(f"    n={n}: maximo de propuestas = {peor}  (n^2 - n + 1 = {n * n - n + 1}; la cota del potencial es n^2 = {n * n})")

print()
print("=== 5. Verificar el teorema de los hospitales rurales a mano: un ejemplo con varios estables ===")
La, Lb = [[0, 1], [1, 0]], [[1, 0], [0, 1]]
est = todos_estables(La, Lb)
print(f"  instancia 2x2 con dos estables: {[[(nombre(a) + '-' + nombreb(x)) for a, x in enumerate(E)] for E in est]}; Gale-Shapley: {gale_shapley(La, Lb)[0]}")

print()
print("=== 6. Variantes con error que parecen correctas ===")
# V1: el receptor acepta a quien no lista porque 'es mejor que estar solo'
hallado = None
for n in range(1, 4):
    for m in range(1, 4):
        for it in range(3000):
            rr = random.Random(it * 97 + n * 7 + m)
            La, Lb = instancia(n, m, 0.8, 0.5, rr)
            M, _ = gale_shapley(La, Lb, defecto="acepta_no_listado")
            rac, bloq = verificador(M, La, Lb)
            if not (rac and not bloq):
                if hallado is None or (n + m) < (hallado[0] + hallado[1]):
                    hallado = (n, m, La, Lb, M, rac, bloq)
        if hallado and n + m >= hallado[0] + hallado[1]:
            break
n, m, La, Lb, M, rac, bloq = hallado
print(f"  V1 (el receptor acepta a quien no lista 'porque es mejor que estar solo'): instancia mas chica hallada: n={n}, m={m}")
print(f"     listas a: {La}, listas b: {Lb}; resultado {M}: individualmente racional = {rac}, bloqueantes = {bloq}")
La, Lb = [[0]], [[]]
M, _ = gale_shapley(La, Lb, defecto="acepta_no_listado")
print(f"     instancia minima: a lista [b], b no lista a nadie: resultado {M} -> racional = {verificador(M, La, Lb)[0]} (b queda con un no listado)")
malas = 0
for it in range(3000):
    rr = random.Random(it)
    n, m = rr.randint(1, 5), rr.randint(1, 5)
    La, Lb = instancia(n, m, 0.7, 0.5, rr)
    M, _ = gale_shapley(La, Lb, defecto="acepta_no_listado")
    rac, bloq = verificador(M, La, Lb)
    malas += not (rac and not bloq)
print(f"     en 3000 instancias aleatorias, la variante no es estable en {malas} ({100 * malas / 3000:.1f} %)")
# V2: el proponente que agoto su lista vuelve a empezar
La, Lb = [[0]], [[]]
M, prop = gale_shapley(La, Lb, defecto="reinicia")
print(f"  V2 (el proponente que agoto su lista la reinicia): a lista [b], b no lista a nadie -> {'NO TERMINA' if M is None else M} (propuestas hechas: {prop}, tope de pasos 5000)")
La, Lb = [[0, 1], [0]], [[1, 0], [0]]
M, prop = gale_shapley(La, Lb, defecto="reinicia")
print(f"     con una instancia donde el original termina (M = {gale_shapley(La, Lb)[0]}), la variante: {'NO TERMINA' if M is None else M} ({prop} propuestas)")
malas = 0
for it in range(500):
    rr = random.Random(it)
    n, m = rr.randint(1, 4), rr.randint(1, 4)
    La, Lb = instancia(n, m, 0.7, 0.5, rr)
    M, _ = gale_shapley(La, Lb, defecto="reinicia")
    malas += M is None
print(f"     en 500 instancias aleatorias pequenas, la variante no termina en {malas} ({100 * malas / 500:.1f} %): el potencial ya no baja")
print("     con listas COMPLETAS (el caso de la conferencia) ningun proponente agota su lista y la variante nunca se activa:")
ok = 0
for it in range(500):
    rr = random.Random(it)
    n = rr.randint(1, 5)
    La = [rr.sample(range(n), n) for _ in range(n)]
    Lb = [rr.sample(range(n), n) for _ in range(n)]
    M, _ = gale_shapley(La, Lb, defecto="reinicia")
    ok += M is not None and M == gale_shapley(La, Lb)[0]
print(f"     {ok} de 500 instancias completas: la variante coincide con el original")
