import importlib
import random

gs = importlib.import_module("ejercicio-12-gale_shapley")
gale_shapley, gale_shapley_bug = gs.gale_shapley, gs.gale_shapley_bug
blocking_pairs, blocking_pairs_old, unacceptable = gs.blocking_pairs, gs.blocking_pairs_old, gs.unacceptable
is_stable, all_matchings, random_instance = gs.is_stable, gs.all_matchings, gs.random_instance


def nombre_a(a):
    return f"a{a + 1}"


def nombre_b(b):
    return "solo" if b is None else f"b{b + 1}"


def texto(M):
    return "  ".join(f"{nombre_a(a)}-{nombre_b(b)}" for a, b in enumerate(M))


# El ejemplo del md: a2 solo lista a b1, y b3 no esta en la lista de nadie
pref_a = [[0, 1], [0], [0, 2]]                 # a1: b1 > b2   a2: b1   a3: b1 > b3
pref_b = [[2, 0, 1], [0, 1, 2], [0, 1, 2]]     # b1: a3 > a1 > a2   b2, b3: a1 > a2 > a3

# ===============================================================
print("Prueba 1: la traza del ejemplo")
trace = []
M, k = gale_shapley(pref_a, pref_b, trace=trace)
print(f"{'paso':>5} {'propone':>8} {'a':>4} {'tenia':>6} {'se queda con':>13}")
for i, (a, b, antes, despues) in enumerate(trace, start=1):
    tenia = "-" if antes is None else nombre_a(antes)
    print(f"{i:>5} {nombre_a(a):>8} {nombre_b(b):>4} {tenia:>6} {nombre_a(despues):>13}")
print("resultado:", texto(M), f"  ({k} propuestas)")
assert M == [1, None, 0] and k == 4
assert is_stable(M, pref_a, pref_b)
print("OK\n")

# ===============================================================
print("Prueba 2: casos borde")
casos = [
    (([[], []], [[0, 1], [0, 1]]), [None, None], "nadie lista a nadie: todos solos"),
    (([[0, 1, 2], [1, 2, 0], [2, 0, 1]], [[1, 2, 0], [2, 0, 1], [0, 1, 2]]),
     [0, 1, 2], "listas completas: igual que la conferencia 3"),
    (([[0], [0], [0]], [[2, 1, 0]]), [None, None, 0], "todos listan solo a b1: gana su favorito"),
    (([[0, 1], [0, 1], [0, 1], [0, 1]], [[3, 2, 1, 0], [0, 1, 2, 3]]),
     [1, None, None, 0], "4 proponentes y 2 receptores"),
    (([[0], [0, 1]], [[1], [0, 1]]), [None, 0], "b1 no lista a a1: lo rechaza"),
]
for (pa, pb), esperado, txt in casos:
    M, _ = gale_shapley(pa, pb)
    assert M == esperado, txt
    assert is_stable(M, pa, pb), txt
    print(f"  {txt:<48}OK")
print()

# ===============================================================
print("Prueba 3: los invariantes vigilados")
# (1) un receptor, una vez con pareja, no vuelve a quedar solo, y su pareja solo mejora
# (2) cada proponente propone en el orden de su lista, sin repetir
# (3) toda pareja que se forma esta en las dos listas
rng = random.Random(3)
pasos = 0
for _ in range(2000):
    na, nb = rng.randint(1, 8), rng.randint(1, 8)
    pa, pb = random_instance(na, nb, rng, complete_b=rng.random() < 0.5)
    trace = []
    gale_shapley(pa, pb, order=rng.choice(["queue", "stack", "random"]), seed=rng.random(), trace=trace)
    lugar_b = [None] * nb                       # lugar de la pareja actual en la lista de b
    siguiente = [0] * na
    for a, b, antes, despues in trace:
        assert pa[a][siguiente[a]] == b         # (2)
        siguiente[a] += 1
        if lugar_b[b] is not None:
            assert despues is not None and pb[b].index(despues) <= lugar_b[b]   # (1)
        if despues is not None:
            assert b in pa[despues] and despues in pb[b]                       # (3)
            lugar_b[b] = pb[b].index(despues)
        pasos += 1
print(f"invariantes comprobados en {pasos:,} propuestas, sin fallos")
print("OK\n")

# ===============================================================
print("Prueba 4: estabilidad contra el oraculo de fuerza bruta")
rng = random.Random(4)
print(f"{'receptores':>12} {'tamanos':>8} {'instancias':>11} {'bloqueantes':>12} {'inaceptables':>13}")
for completos in [True, False]:
    for na, nb, veces in [(3, 3, 500), (5, 8, 300), (20, 15, 100)]:
        bloq = inac = 0
        for _ in range(veces):
            pa, pb = random_instance(na, nb, rng, complete_b=completos)
            for orden in ["queue", "stack", "random"]:
                M, _ = gale_shapley(pa, pb, order=orden, seed=rng.random())
                bloq += len(blocking_pairs(M, pa, pb))
                inac += len(unacceptable(M, pa, pb))
        tipo = "completos" if completos else "incompletos"
        print(f"{tipo:>12} {f'{na}x{nb}':>8} {veces:>11} {bloq:>12} {inac:>13}")
        assert bloq == 0 and inac == 0
print("OK\n")

# ===============================================================
print("Prueba 5: el resultado no depende del orden, y es el mejor para los proponentes")
rng = random.Random(5)
iguales = optimo = 0
for _ in range(200):
    pa, pb = random_instance(4, 4, rng, complete_b=rng.random() < 0.5)
    res = [gale_shapley(pa, pb, order=o, seed=s)[0]
           for o, s in [("queue", 0), ("stack", 0), ("random", 1), ("random", 2)]]
    iguales += all(M == res[0] for M in res)
    estables = [E for E in all_matchings(4, 4) if is_stable(E, pa, pb)]
    M = res[0]
    lugar = lambda a, b: len(pa[a]) if b is None else pa[a].index(b)   # solo = ultimo
    optimo += all(lugar(a, M[a]) <= min(lugar(a, E[a]) for E in estables) for a in range(4))
print(f"mismo resultado con las cuatro ejecuciones: {iguales} de 200")
print(f"cada proponente con lo mejor que consigue en un emparejamiento estable: {optimo} de 200")
assert iguales == 200 and optimo == 200
print("OK\n")

# ===============================================================
print("Prueba 6: el potencial, propuestas contra el largo total de las listas")
rng = random.Random(6)
print(f"{'tamanos':>8} {'L promedio':>11} {'propuestas promedio':>20} {'propuestas maximo':>18}")
for na, nb in [(5, 5), (20, 20), (60, 60), (60, 20)]:
    total_L = total_k = maximo = 0
    for _ in range(100):
        pa, pb = random_instance(na, nb, rng)
        L = sum(len(lst) for lst in pa)
        _, k = gale_shapley(pa, pb, order="random", seed=rng.random())
        assert k <= L
        total_L += L
        total_k += k
        maximo = max(maximo, k / L if L else 0)
    print(f"{f'{na}x{nb}':>8} {total_L / 100:>11.1f} {total_k / 100:>20.1f} {f'{100 * maximo:.0f}% de L':>18}")
print("nunca hay mas propuestas que L")
print("OK\n")

# ===============================================================
print("Prueba 7: copiar el algoritmo de listas completas sin adaptarlo")


def falla(pa, pb):
    try:
        return gale_shapley_bug(pa, pb) != gale_shapley(pa, pb)[0]
    except IndexError:                          # se le acabo la lista a alguien
        return True


rng = random.Random(7)
generadores = {
    "completas, n x n": lambda: ([rng.sample(range(6), 6) for _ in range(6)],
                                 [rng.sample(range(6), 6) for _ in range(6)]),
    "completas, 6 x 4": lambda: ([rng.sample(range(4), 4) for _ in range(6)],
                                 [rng.sample(range(6), 6) for _ in range(4)]),
    "proponentes incompletos": lambda: random_instance(6, 6, rng),
    "los dos incompletos": lambda: random_instance(6, 6, rng, complete_b=False),
}
print(f"{'listas':>25} {'fallos':>8}")
for nombre, generar in generadores.items():
    f = sum(falla(*generar()) for _ in range(3000)) / 30
    print(f"{nombre:>25} {f:>7.1f}%")
    if nombre == "completas, n x n":
        assert f == 0
print("OK\n")

# ===============================================================
print("Prueba 8: la definicion vieja de pareja bloqueante")
todos_solos = [None, None, None]
print("emparejamiento con todos solos, en el ejemplo de la prueba 1:")
print("  bloqueantes con la definicion vieja:", blocking_pairs_old(todos_solos, pref_a, pref_b))
print("  bloqueantes con la definicion nueva:",
      [(nombre_a(a), nombre_b(b)) for a, b in blocking_pairs(todos_solos, pref_a, pref_b)])
assert blocking_pairs_old(todos_solos, pref_a, pref_b) == []
rng = random.Random(8)
viejos = nuevos = 0
for _ in range(200):
    pa, pb = random_instance(4, 4, rng)
    for E in all_matchings(4, 4):
        if not unacceptable(E, pa, pb):
            viejos += not blocking_pairs_old(E, pa, pb)
            nuevos += not blocking_pairs(E, pa, pb)
print(f"en 200 instancias de 4x4, emparejamientos 'estables' segun la vieja: {viejos:,}")
print(f"                          y estables de verdad (definicion nueva):   {nuevos:,}")
assert viejos > nuevos
print("OK")
