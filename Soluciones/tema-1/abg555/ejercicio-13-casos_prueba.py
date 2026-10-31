import importlib
import math
import random

sp = importlib.import_module("ejercicio-13-splay")
splay, move_to_root, find, path, is_bst, access_sequence = (
    sp.splay, sp.move_to_root, sp.find, sp.path, sp.is_bst, sp.access_sequence)


def cota(n, m):
    # la cuenta de la seccion 5 de la conferencia 4: m (3 log2 n + 1) + Phi_0,
    # con Phi_0 = log2 n! (el potencial del camino)
    return m * (3 * math.log2(n) + 1) + math.lgamma(n + 1) / math.log(2)


# ===============================================================
print("Prueba 1: el costo de cada acceso, n = 16")
costs = access_sequence(16, range(1, 17))
print("  claves:", " ".join(f"{k:>2}" for k in range(1, 17)))
print("  costos:", " ".join(f"{c:>2}" for c in costs))
print("  total:", sum(costs))
assert costs[0] == 15
print("OK\n")

# ===============================================================
print("Prueba 2: despues de cada acceso, el arbol sigue siendo de busqueda y la clave esta en la raiz")
rng = random.Random(2)
accesos = 0
for _ in range(200):
    n = rng.randint(1, 60)
    root = path(n)
    for _ in range(3 * n):
        k = rng.randint(1, n)
        x = find(root, k)
        splay(x)
        root = x
        assert root.parent is None and root.key == k and is_bst(root)
        accesos += 1
print(f"{accesos:,} accesos al azar, siempre bien")
print("OK\n")

# ===============================================================
print("Prueba 3: el lema de acceso vigilado")
# costo amortizado c + Phi' - Phi <= 3 (r(t) - r(x)) + 1, con r(t) = log2 n
rng = random.Random(3)
revisados, peor = 0, -1e9
for n, orden in [(200, "en orden"), (200, "al azar"), (60, "en orden")]:
    claves = list(range(1, n + 1)) * 3 if orden == "en orden" else [rng.randint(1, n) for _ in range(3 * n)]
    watch = []
    access_sequence(n, claves, watch=watch)
    for c, antes, despues, r_x in watch:
        exceso = (c + despues - antes) - (3 * (math.log2(n) - r_x) + 1)
        assert exceso <= 1e-9
        peor = max(peor, exceso)
        revisados += 1
print(f"lema comprobado en {revisados:,} accesos; el costo amortizado nunca pasa la cota "
      f"(la mayor diferencia es {peor:.2f})")
print("OK\n")

# ===============================================================
print("Prueba 4: accesos 1, 2, ..., n en orden: costo real contra la cota")
print(f"{'n':>6} {'costo real':>11} {'real / n':>9} {'cota':>10} {'cota / real':>12} {'Phi_0 = log2 n!':>16}")
for n in [100, 200, 400, 800, 1600]:
    total = sum(access_sequence(n, range(1, n + 1)))
    c = cota(n, n)
    print(f"{n:>6,} {total:>11,} {total / n:>9.2f} {c:>10,.0f} {c / total:>12.1f} "
          f"{math.lgamma(n + 1) / math.log(2):>16,.0f}")
    assert total <= c
print("OK\n")

# ===============================================================
print("Prueba 4b: donde se pierde la cota")
print(f"{'n':>6} {'costo real':>11} {'suma de cotas del lema':>23} {'Phi_0':>8} {'Phi_final':>10}")
for n in [100, 400, 1600]:
    watch = []
    access_sequence(n, range(1, n + 1), watch=watch)
    real = sum(c for c, _, _, _ in watch)
    lema = sum(3 * (math.log2(n) - r) + 1 for _, _, _, r in watch)
    phi0, phim = watch[0][1], watch[-1][2]
    print(f"{n:>6,} {real:>11,} {lema:>23,.0f} {phi0:>8,.0f} {phim:>10,.0f}")
    assert abs(phi0 - phim) < 1e-6                 # al final el arbol vuelve a ser un camino
    amortizado = sum(c + d - a for c, a, d, _ in watch)
    assert abs(amortizado - real) < 1e-6           # entonces real = suma de los amortizados
print("OK\n")

# ===============================================================
print("Prueba 5: tres rondas seguidas (como la seccion 6 de la conferencia 4)")
print(f"{'n':>6} {'costo por acceso':>17} {'cota por acceso':>16}")
for n in [100, 200, 400, 800]:
    total = sum(access_sequence(n, list(range(1, n + 1)) * 3))
    print(f"{n:>6} {total / (3 * n):>17.2f} {cota(n, 3 * n) / (3 * n):>16.2f}")
print("OK\n")

# ===============================================================
print("Prueba 6: la cota no es mala para cualquier secuencia: accesos al azar")
rng = random.Random(6)
print(f"{'n':>6} {'en orden: real / n':>19} {'al azar: real / n':>18} {'log2 n':>7}")
for n in [100, 400, 1600]:
    orden = sum(access_sequence(n, range(1, n + 1))) / n
    azar = sum(access_sequence(n, [rng.randint(1, n) for _ in range(4 * n)])) / (4 * n)
    print(f"{n:>6} {orden:>19.2f} {azar:>18.2f} {math.log2(n):>7.1f}")
print("OK\n")

# ===============================================================
print("Prueba 7: subir a la raiz con la misma secuencia")
print(f"{'n':>6} {'splay':>9} {'subir a la raiz':>16} {'n^2 / 2':>9}")
for n in [100, 200, 400]:
    s = sum(access_sequence(n, range(1, n + 1)))
    r = sum(access_sequence(n, list(range(1, n + 1)) * 2, reorganize=move_to_root)[n:])
    print(f"{n:>6} {s:>9,} {r:>16,} {n * n // 2:>9,}")
print("(subir a la raiz: segunda ronda, cuando ya se ve el comportamiento estable)")
print("OK")
