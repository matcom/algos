"""Ejercicio 2: busqueda binaria. Invariante, potencial y cota de informacion (C3 sec.1, C5 sec.3)."""
import math
import random
from collections import Counter

random.seed(2)


def busqueda_binaria(A, x, traza=None, vigilar=False):
    """Devuelve (resultado, numero de comparaciones). Comparacion de 3 vias = 1 comparacion.
    resultado = ("esta", m) o ("hueco", lo). Con vigilar=True comprueba invariante y potencial."""
    n = len(A)
    lo, hi, comps = 0, n, 0
    while lo < hi:
        if vigilar:
            assert 0 <= lo <= hi <= n
            assert all(a < x for a in A[:lo]) and all(a > x for a in A[hi:])   # invariante I
        phi = hi - lo
        m = (lo + hi) // 2
        comps += 1
        if x == A[m]:
            if traza is not None:
                traza.append((lo, hi, phi, m, "="))
            return ("esta", m), comps
        if traza is not None:
            traza.append((lo, hi, phi, m, "<" if x < A[m] else ">"))
        if x < A[m]:
            hi = m
        else:
            lo = m + 1
        if vigilar:
            assert hi - lo <= phi // 2            # potencial: Phi' <= floor(Phi/2) < Phi
    if vigilar:
        assert all(a < x for a in A[:lo]) and all(a > x for a in A[lo:])      # postcondicion
    return ("hueco", lo), comps


def variante(A, x, tipo, tope=60, traza=None):
    """Variantes con un error de una unidad. Devuelve pasos, o None si pasa del tope (no termina).
    'semi' : intervalo [lo,hi), con lo = m en lugar de lo = m + 1   (C3 ej. 7)
    'cerr' : intervalo cerrado [lo,hi], con hi = m en lugar de hi = m - 1"""
    if tipo == "semi":
        lo, hi = 0, len(A)
        cond = lambda: lo < hi
        pot = lambda: hi - lo
    else:
        lo, hi = 0, len(A) - 1
        cond = lambda: lo <= hi
        pot = lambda: hi - lo + 1
    pasos = 0
    while cond():
        if traza is not None:
            traza.append((lo, hi, pot()))
        pasos += 1
        if pasos > tope:
            return None
        m = (lo + hi) // 2
        if x == A[m]:
            return pasos
        if x < A[m]:
            hi = m
        else:
            lo = m if tipo == "semi" else m + 1
    return pasos


def cota(n):
    return math.ceil(math.log2(n + 1))


def lower_bound2(A, x):
    """Modelo de 2 vias: cada comparacion es una pregunta si/no (x <= A[m]? o x == A[g]?).
    Invariante: A[:lo] < x <= A[hi:]. Devuelve (resultado, comparaciones)."""
    n = len(A)
    lo, hi, comps = 0, n, 0
    while lo < hi:
        m = (lo + hi) // 2
        comps += 1
        if x <= A[m]:
            hi = m
        else:
            lo = m + 1
    if lo < n:
        comps += 1
        if A[lo] == x:
            return ("esta", lo), comps
    return ("hueco", lo), comps


def binaria_saltando(A, x, j):
    """Binaria de decision que NUNCA compara con A[j]: si cae en m == j usa m+1 (o m-1);
    si el intervalo es solo {j}, responde 'no' sin comparar. Devuelve (esta?, comparo_j?)."""
    lo, hi = 0, len(A)
    while lo < hi:
        m = (lo + hi) // 2
        if m == j:
            if hi - lo == 1:
                return False
            m = m + 1 if m + 1 < hi else m - 1
        if x == A[m]:
            return True
        if x < A[m]:
            hi = m
        else:
            lo = m + 1
    return False


def cuelga(A, x, tipo):
    return variante(A, x, tipo) is None


print("=== 1. Correctitud con invariante y potencial vigilados (aleatorio) ===")
casos = 0
for _ in range(20000):
    n = random.randint(0, 40)
    A = sorted(random.randint(0, 30) for _ in range(n))       # con duplicados
    x = random.randint(-1, 31)
    (r, p), _c = busqueda_binaria(A, x, vigilar=True)
    if r == "esta":
        assert A[p] == x
    else:
        assert x not in A
    casos += 1
print(f"  {casos} casos (arreglos con duplicados, x dentro y fuera): sin fallos de aserto")

print()
print("=== 2. Peor caso exacto sobre TODAS las entradas (2n+1 clases) = ceil(log2(n+1)) ===")
malos = []
for n in range(0, 3001):
    A = [2 * i + 1 for i in range(n)]                   # impares; los pares son los huecos
    pc = max(busqueda_binaria(A, x)[1] for x in range(0, 2 * n + 1))
    if pc != cota(n):
        malos.append((n, pc, cota(n)))
print(f"  n = 0..3000: peor caso == ceil(log2(n+1)) en todos salvo {len(malos)}: {malos}")
print("  borde y tipicos:  n  peor  cota")
for n in (0, 1, 2, 3, 7, 8, 15, 16, 1000, 1023, 1024):
    A = [2 * i + 1 for i in range(n)]
    pc = max(busqueda_binaria(A, x)[1] for x in range(0, 2 * n + 1))
    print(f"    {n:>12}  {pc:>3}  {cota(n):>3}")

print()
print("=== 3. Hojas: los n+1 huecos terminan en hojas distintas (lema 4 de C5) ===")
for n in (7, 8, 100, 1000):
    A = [2 * i + 1 for i in range(n)]
    caminos = set()
    for g in range(n + 1):
        x = 2 * g                                        # el hueco g
        tz = []
        busqueda_binaria(A, x, traza=tz)
        caminos.add(tuple((m, o) for (_, _, _, m, o) in tz))   # hoja = camino (comparacion, respuesta)
    print(f"  n={n:>5}: {len(caminos)} caminos distintos para {n+1} huecos")
    assert len(caminos) == n + 1

print()
print("=== 4. Comparaciones por entrada, n = 7 (arbol de la figura 7 de C5) ===")
A = list(range(1, 8))
print("  x en A  :", [(x, busqueda_binaria(A, x)[1]) for x in A])
print("  huecos  :", [(f"h{g}", busqueda_binaria(A, g + 0.5)[1]) for g in range(8)])
print("  histograma (comps -> entradas, 2n+1=15 entradas):",
      dict(sorted(Counter([busqueda_binaria(A, x)[1] for x in A] +
                          [busqueda_binaria(A, g + 0.5)[1] for g in range(8)]).items())))

print()
print("=== 5. Huecos vecinos: los caminos se separan exactamente en A[g] ===")
total = 0
for n in range(0, 201):
    A = [2 * i + 1 for i in range(n)]
    for g in range(n):
        t1, t2 = [], []
        busqueda_binaria(A, 2 * g, traza=t1)
        busqueda_binaria(A, 2 * g + 2, traza=t2)
        p1 = [(m, o) for (_, _, _, m, o) in t1]
        p2 = [(m, o) for (_, _, _, m, o) in t2]
        k = next(i for i in range(min(len(p1), len(p2))) if p1[i] != p2[i])
        assert p1[k][0] == p2[k][0] == g and p1[k][1] != p2[k][1]
        total += 1
print(f"  n = 0..200, {total} pares de huecos vecinos (g, g+1): el primer desacuerdo es la comparacion con A[g]")
print("  Algoritmo que de verdad se salta el indice j (decision: esta x?):")
for n in (7, 8, 15, 50):
    A = [2 * i + 1 for i in range(n)]
    fallos = []
    for j in range(n):
        for x in range(0, 2 * n + 1):
            if binaria_saltando(A, x, j) != (x % 2 == 1):
                fallos.append((j, x))
    assert all(x == A[j] for j, x in fallos) and len(fallos) == n
    print(f"    n={n:>2}: falla solo en x = A[j] para cada j  ({len(fallos)} fallos en {n * (2 * n + 1)} pruebas)")

print()
print("=== 6. Variantes con un error de una unidad: el potencial las atrapa ===")
for tipo, desc in (("semi", "[lo,hi) con lo = m"), ("cerr", "[lo,hi] con hi = m")):
    total = cuelgan = 0
    minimo = None
    for n in range(0, 7):
        A = [2 * i + 1 for i in range(n)]
        for x in range(0, 2 * n + 1):
            total += 1
            if variante(A, x, tipo) is None:
                cuelgan += 1
                if minimo is None:
                    minimo = (A, x)
    print(f"  {desc}: cuelga en {cuelgan} de {total} entradas (n <= 6); la primera: A={minimo[0]}, x={minimo[1]}")
    tz = []
    variante(*minimo, tipo, tope=4, traza=tz)
    print("    traza (lo, hi, Phi):", tz[:4], "... el potencial se queda en", tz[-1][2])
ok = all(busqueda_binaria([2 * i + 1 for i in range(n)], x)[1] <= cota(n)
         for n in range(0, 7) for x in range(0, 2 * n + 1))
print(f"  la version correcta termina en <= ceil(log2(n+1)) pasos en las mismas entradas: {ok}")
print("  Caracterizacion (assert para n = 0..12, A distintos, x en 0..2n):")
print("    semi: cuelga <=> n>=1, x no esta y x > A[0];  cerr: cuelga <=> n>=1, x no esta y x < A[n-1]")
print("    con x presente nunca cuelga")
cont = {"semi": 0, "cerr": 0}
for n in range(0, 13):
    A = [2 * i + 1 for i in range(n)]
    for x in range(0, 2 * n + 1):
        esta = x in A
        assert cuelga(A, x, "semi") == (n >= 1 and not esta and x > A[0])
        assert cuelga(A, x, "cerr") == (n >= 1 and not esta and x < A[n - 1])
        if esta:
            assert not cuelga(A, x, "semi") and not cuelga(A, x, "cerr")
        for t in cont:
            cont[t] += cuelga(A, x, t)
tot = sum(2 * n + 1 for n in range(13))
print(f"    verificado en {tot} entradas; cuelgan {cont['semi']} (semi) y {cont['cerr']} (cerr); "
      f"por formula: sum_(n=1..12) n = {sum(range(1, 13))}")
print("    n <= 6: entradas = 49, x ausente = 28, de ellas en el hueco 0 (o n-1) = 7, cuelgan 28 - 7 = 21")

print()
print("=== 6b. Modelo de 2 vias: lower_bound + comparacion de igualdad ===")
malos = []
for n in range(1, 3001):
    A = [2 * i + 1 for i in range(n)]
    pc = max(lower_bound2(A, x)[1] for x in range(0, 2 * n + 1))
    c1 = cota(n) + 1
    c2 = math.ceil(math.log2(2 * n + 1))
    assert c1 == c2
    if pc != c1:
        malos.append((n, pc, c1))
print(f"  n = 1..3000: peor caso == ceil(log2(n+1)) + 1 == ceil(log2(2n+1)) salvo {len(malos)}: {malos}")
for n in (1, 2, 3, 7, 8, 1000, 1023, 1024):
    A = [2 * i + 1 for i in range(n)]
    pc = max(lower_bound2(A, x)[1] for x in range(0, 2 * n + 1))
    print(f"    n={n:>5}  peor={pc:>3}  ceil(log2(2n+1))={math.ceil(math.log2(2*n+1)):>3}")
for _ in range(5000):
    n = random.randint(0, 30)
    A = sorted(random.sample(range(0, 80), n))
    x = random.randint(-1, 81)
    r, _c = lower_bound2(A, x)
    assert r == busqueda_binaria(A, x)[0] or r[0] == busqueda_binaria(A, x)[0][0]
print("  5000 pruebas aleatorias: mismo veredicto que la binaria de 3 vias")
print()
print("=== 7. Traza con el potencial, n = 20, x = 13 (hueco entre 12 y 14) ===")
A = [2 * i for i in range(20)]
tz = []
res, c = busqueda_binaria(A, 13, traza=tz)
print("  paso   lo   hi  Phi=hi-lo   m  A[m] x?")
for k, (lo, hi, phi, m, o) in enumerate(tz, 1):
    print(f"  {k:>4} {lo:>4} {hi:>4} {phi:>10} {m:>3} {A[m]:>5}  x{o}A[m]")
print(f"  resultado {res}, comparaciones {c}, cota ceil(log2 21) = {cota(20)}")
