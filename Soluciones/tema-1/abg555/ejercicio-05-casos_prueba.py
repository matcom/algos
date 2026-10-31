import importlib
import random

floyd = importlib.import_module("ejercicio-05-floyd")
has_cycle, has_cycle_set, has_cycle_bug = floyd.has_cycle, floyd.has_cycle_set, floyd.has_cycle_bug
make_list, node_at = floyd.make_list, floyd.node_at


def vueltas(head):
    trace = []
    has_cycle(head, trace)
    return len(trace)


def vueltas_esperadas(mu, lam):
    # Lo que dice la demostracion:
    #   sin ciclo: floor(n / 2) vueltas
    #   con ciclo: el primer multiplo de lam que sea >= mu y >= 1
    if lam == 0:
        return mu // 2
    t = lam
    while t < mu:
        t += lam
    return t


# ===============================================================
print("Prueba 1: la traza del ejemplo (mu = 3, lam = 5)")
head, nodes = make_list(3, 5)
trace = []
assert has_cycle(head, trace)
print(f"{'vuelta':>7} {'pos slow':>9} {'pos fast':>9} {'nodo slow':>10} {'nodo fast':>10}")
for t, (slow, fast) in enumerate(trace, start=1):
    marca = "  <- se encuentran" if slow is fast else ""
    print(f"{t:>7} {t:>9} {2 * t:>9} {slow.value:>10} {fast.value:>10}{marca}")
assert len(trace) == 5 and trace[-1][0].value == 5
print("OK\n")

# ===============================================================
print("Prueba 2: casos borde")
assert has_cycle(None) is False
print(f"  {'lista vacia: no hay ciclo':<52}OK")
assert has_cycle(make_list(1, 0)[0]) is False
print(f"  {'un nodo sin ciclo':<52}OK")
assert has_cycle(make_list(0, 1)[0]) is True
print(f"  {'un nodo que apunta a si mismo: hay ciclo':<52}OK")
assert has_cycle(make_list(0, 2)[0]) is True
print(f"  {'dos nodos que se apuntan entre si: hay ciclo':<52}OK")
assert has_cycle(make_list(2, 0)[0]) is False and has_cycle(make_list(3, 0)[0]) is False
print(f"  {'listas de 2 y 3 nodos sin ciclo (largo par e impar)':<52}OK")
assert has_cycle(make_list(50, 1)[0]) is True
print(f"  {'cola de 50 nodos y el ultimo apunta a si mismo':<52}OK")
assert has_cycle(make_list(0, 50)[0]) is True
print(f"  {'ciclo de 50 nodos sin cola (la lista es un anillo)':<52}OK\n")

# ===============================================================
print("Prueba 3: el invariante vigilado")
# despues de la vuelta t: slow es el nodo de la posicion t, fast el de la posicion 2t
random.seed(5)
revisados = 0
for _ in range(2000):
    mu, lam = random.randint(0, 20), random.randint(0, 20)
    head, _ = make_list(mu, lam)
    trace = []
    has_cycle(head, trace)
    for t, (slow, fast) in enumerate(trace, start=1):
        assert slow is node_at(head, t)
        assert fast is node_at(head, 2 * t)
        revisados += 1
print(f"invariante comprobado en {revisados:,} vueltas, sin fallos")
print("OK\n")

# ===============================================================
print("Prueba 4: contra el oraculo (la version con conjunto)")
random.seed(6)
print(f"{'listas':>18} {'casos':>7} {'fallos':>7}")
for nombre, lam_min, lam_max in [("sin ciclo", 0, 0), ("con ciclo", 1, 60), ("mezcladas", 0, 60)]:
    malos = 0
    for _ in range(3000):
        head, _ = make_list(random.randint(0, 60), random.randint(lam_min, lam_max))
        malos += has_cycle(head) != has_cycle_set(head)
    print(f"{nombre:>18} {3000:>7} {malos:>7}")
    assert malos == 0
print("OK\n")

# ===============================================================
print("Prueba 5: cuantas vueltas da, contra la formula de la demostracion")
casos = 0
for mu in range(0, 41):
    for lam in range(0, 41):
        if mu + lam == 0:
            continue
        head, _ = make_list(mu, lam)
        v = vueltas(head)
        assert v == vueltas_esperadas(mu, lam)
        assert v <= mu + lam                   # nunca mas de n vueltas
        casos += 1
print(f"{casos:,} listas (mu y lam de 0 a 40): las vueltas coinciden siempre con la formula")
print("y nunca pasan de n")
print("OK\n")

# ===============================================================
print("Prueba 6: memoria, Floyd contra la version con conjunto")
print(f"{'n':>8} {'vueltas Floyd':>14} {'nodos que guarda Floyd':>23} {'nodos que guarda el conjunto':>29}")
for n in [10, 100, 1_000, 10_000, 100_000]:
    head, _ = make_list(n // 2, n - n // 2)
    seen = set()
    assert has_cycle(head) and has_cycle_set(head, seen)
    print(f"{n:>8,} {vueltas(head):>14,} {2:>23} {len(seen):>29,}")
    assert len(seen) == n
print("OK\n")

# ===============================================================
print("Prueba 7: la version que solo revisa fast.next")


def falla(head):
    try:
        return has_cycle_bug(head) != has_cycle(head)
    except AttributeError:                     # 'NoneType' object has no attribute 'next'
        return True


random.seed(7)
generadores = {
    "con ciclo": lambda: make_list(random.randint(0, 60), random.randint(1, 60)),
    "sin ciclo, largo impar": lambda: make_list(2 * random.randint(0, 30) + 1, 0),
    "sin ciclo, largo par": lambda: make_list(2 * random.randint(1, 30), 0),
    "mezcladas": lambda: make_list(random.randint(1, 60), random.choice([0, random.randint(1, 60)])),
}
print(f"{'listas':>24} {'fallos':>8}")
for nombre, generar in generadores.items():
    f = sum(falla(generar()[0]) for _ in range(3000)) / 3000
    print(f"{nombre:>24} {100 * f:>7.1f}%")
assert falla(make_list(2, 0)[0]) and not falla(make_list(3, 0)[0])
print("OK")
