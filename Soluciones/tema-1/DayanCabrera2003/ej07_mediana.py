"""Ejercicio 7: el n-esimo menor de dos arreglos ordenados de largo n, en O(log n) (C2, C3, C5).
Busqueda binaria sobre la particion: i elementos de A y n-i de B a la izquierda."""
import itertools
import math
import random
from collections import Counter

random.seed(7)
NEG, POS = float("-inf"), float("inf")


class Cmp:
    def __init__(self):
        self.n = 0

    def le(self, a, b):             # a <= b, una comparacion
        self.n += 1
        return a <= b


def P(A, B, n, i):
    """P(i): A[i] >= B[n-i-1], con A[n] = +inf (i = n)."""
    return True if i >= n else A[i] >= B[n - i - 1]


def mediana(A, B, c=None, vigilar=False):
    """n-esimo menor de A u B (A, B ordenados, largo n >= 1). Devuelve (valor, i, iteraciones)."""
    n = len(A)
    c = c if c is not None else Cmp()
    lo, hi, iters = 0, n, 0
    if vigilar:
        istar = next(i for i in range(n + 1) if P(A, B, n, i))
    while lo < hi:
        if vigilar:
            assert lo <= istar <= hi                          # invariante: la i correcta esta en [lo, hi]
            s = hi - lo
        mid = (lo + hi) // 2
        iters += 1
        if c.le(B[n - mid - 1], A[mid]):                       # P(mid): A[mid] >= B[n-mid-1]
            hi = mid
        else:
            lo = mid + 1
        if vigilar:
            assert hi - lo <= s // 2 and hi - lo < s           # potencial hi - lo
    i = lo
    if vigilar:
        assert i == istar
        # particion correcta: max(A[:i] + B[:n-i]) <= min(A[i:] + B[n-i:])
        izq = A[:i] + B[:n - i]
        der = A[i:] + B[n - i:]
        assert max(izq) <= min(der)
    izq_a = A[i - 1] if i > 0 else NEG
    izq_b = B[n - i - 1] if n - i > 0 else NEG
    if i > 0 and n - i > 0:                                    # max de los dos, con centinelas -inf
        v = izq_a if c.le(izq_b, izq_a) else izq_b
    else:
        v = izq_a if i > 0 else izq_b
    return v, i, iters


def kesimo(A, B, k, c=None):
    """k-esimo menor (1 <= k <= m+n) de dos arreglos de largos distintos, en O(log min(m,n))."""
    if len(A) > len(B):
        A, B = B, A
    m, nb = len(A), len(B)
    c = c if c is not None else Cmp()
    lo, hi = max(0, k - nb), min(k, m)
    while lo < hi:
        mid = (lo + hi) // 2                                   # mid <= m-1 y 0 <= k-mid-1 <= nb-1
        if c.le(B[k - mid - 1], A[mid]):
            hi = mid
        else:
            lo = mid + 1
    i = lo
    a = A[i - 1] if i > 0 else NEG
    b = B[k - i - 1] if k - i > 0 else NEG
    if i > 0 and k - i > 0:
        return (a if c.le(b, a) else b)
    return a if i > 0 else b


def kesimo_descarte(A, B, k, c=None):
    """La version que descarta mitades: compara A[i-1] con B[j-1] y tira el prefijo del menor."""
    c = c if c is not None else Cmp()
    A, B = list(A), list(B)
    while True:
        if not A:
            return B[k - 1]
        if not B:
            return A[k - 1]
        if k == 1:
            return A[0] if c.le(A[0], B[0]) else B[0]
        i, j = min(len(A), k // 2), min(len(B), k // 2)
        if c.le(A[i - 1], B[j - 1]):
            A, k = A[i:], k - i
        else:
            B, k = B[j:], k - j


# ---- versiones equivocadas tipicas (errores de una unidad)
def mediana_mala(A, B, defecto):
    n = len(A)
    lo, hi = (1 if defecto == "lo=1" else 0), (n - 1 if defecto == "hi=n-1" else n)
    while lo < hi:
        mid = (lo + hi) // 2
        if B[n - mid - 1] <= A[mid]:
            hi = mid
        else:
            lo = mid + 1
    i = lo
    if defecto == "A[i-1] sin centinela":                       # en Python A[-1] es el ULTIMO elemento
        a = A[i - 1]
        b = B[n - i - 1] if n - i > 0 else NEG
        return max(a, b)
    if defecto == "indice de B corrido en el max final":
        a = A[i - 1] if i > 0 else NEG
        b = B[n - i] if n - i < n and n - i >= 0 else NEG
        return max(a, b)
    a = A[i - 1] if i > 0 else NEG
    b = B[n - i - 1] if n - i > 0 else NEG
    return max(a, b)


def verdad(A, B):
    return sorted(A + B)[len(A) - 1]


def todas_distintas(n):
    for sub in itertools.combinations(range(2 * n), n):
        A = list(sub)
        B = [v for v in range(2 * n) if v not in sub]
        yield A, B


def con_duplicados(n, V):
    """Todos los pares de arreglos ordenados de largo n con valores en 0..V-1."""
    arr = [list(t) for t in itertools.combinations_with_replacement(range(V), n)]
    for A in arr:
        for B in arr:
            yield A, B


print("=== 1. Correctitud contra sorted(A+B)[n-1] ===")
total = 0
for n, V in ((1, 6), (2, 5), (3, 4), (4, 4), (5, 3)):
    cnt = 0
    for A, B in con_duplicados(n, V):
        assert mediana(A, B, vigilar=True)[0] == verdad(A, B), (A, B)
        cnt += 1
    total += cnt
    print(f"  n={n}: todos los pares ordenados con valores en 0..{V - 1} (con duplicados): {cnt} entradas, correcto, invariante y potencial vigilados")
for n in range(1, 10):
    cnt = 0
    for A, B in todas_distintas(n):
        assert mediana(A, B, vigilar=True)[0] == verdad(A, B)
        cnt += 1
    total += cnt
print(f"  n = 1..9: todas las particiones de 0..2n-1 en dos arreglos (distintos): correcto y vigilado")
gens = {
    "aleatorios distintos": lambda n: (lambda v: (sorted(v[:n]), sorted(v[n:])))(random.sample(range(10 ** 6), 2 * n)),
    "aleatorios con muchos duplicados": lambda n: (sorted(random.randint(0, 4) for _ in range(n)), sorted(random.randint(0, 4) for _ in range(n))),
    "A toda menor que B": lambda n: (list(range(n)), list(range(n, 2 * n))),
    "B toda menor que A": lambda n: (list(range(n, 2 * n)), list(range(n))),
    "intercalados a1<b1<a2<...": lambda n: (list(range(0, 2 * n, 2)), list(range(1, 2 * n, 2))),
    "intercalados b1<a1<b2<...": lambda n: (list(range(1, 2 * n, 2)), list(range(0, 2 * n, 2))),
    "todos iguales": lambda n: ([7] * n, [7] * n),
}
for nombre, g in gens.items():
    cnt = 0
    for n in list(range(1, 80)) + [200, 1000, 4096, 5000]:
        for _ in range(3 if "aleatorios" in nombre else 1):
            A, B = g(n)
            assert mediana(A, B, vigilar=(n <= 200))[0] == verdad(A, B), (nombre, n)
            cnt += 1
    print(f"  {nombre:<34} {cnt:>4} entradas (n = 1..79, 200, 1000, 4096, 5000): correcto")
for _ in range(20000):
    n = random.randint(1, 60)
    A, B = gens[random.choice(list(gens))](n)
    assert mediana(A, B)[0] == verdad(A, B)
    total += 1
print(f"  {total + 20000} entradas en total hasta aqui (exhaustivas + aleatorias): sin fallos")

print()
print("=== 2. Costo: comparaciones del peor caso, contadas ===")
print(f"  {'n':>6} {'peor medido':>12} {'ceil(log2(n+1))+1':>18} {'cota inf: ceil(log2 2n)':>24} {'iteraciones max':>16}")
cota_alg = lambda n: math.ceil(math.log2(n + 1)) + 1
cota_inf = lambda n: math.ceil(math.log2(2 * n))
filas = []
for n in list(range(1, 11)) + [15, 16, 17, 31, 32, 63, 64, 100, 127, 128, 1000, 1023, 1024, 4096]:
    peor = 0
    it_max = 0

    def costo_istar(istar, n=n):
        """Comparaciones del algoritmo cuando la particion correcta es i*: P(mid) <=> mid >= i*."""
        lo, hi, it = 0, n, 0
        while lo < hi:
            mid = (lo + hi) // 2
            it += 1
            if mid >= istar:
                hi = mid
            else:
                lo = mid + 1
        return it + (1 if 0 < istar < n else 0), it

    def una(istar, n=n):
        """Entrada con particion correcta i*: A[:i*] y B[:n-i*] son los n menores; el resto, los n mayores."""
        izq_a = list(range(0, istar))
        izq_b = list(range(istar, n))
        der_a = list(range(n, n + (n - istar)))
        der_b = list(range(n + (n - istar), 2 * n))
        return izq_a + der_a, izq_b + der_b

    if n <= 10:
        for A, B in todas_distintas(n):
            c = Cmp()
            v, i, it = mediana(A, B, c)
            assert v == verdad(A, B) and (c.n, it) == costo_istar(i)       # el costo solo depende de i*
            peor = max(peor, c.n)
            it_max = max(it_max, it)
    else:
        for istar in range(n + 1):                                       # peor caso exacto: simulacion sobre todo i*
            cn, it = costo_istar(istar)
            peor = max(peor, cn)
            it_max = max(it_max, it)
        for istar in sorted(set([0, 1, n - 1, n] + random.sample(range(n + 1), min(40, n + 1)))):   # y comprobacion con entradas reales
            A, B = una(istar)
            assert len(A) == len(B) == n and A == sorted(A) and B == sorted(B)
            c = Cmp()
            v, i, it = mediana(A, B, c)
            assert v == verdad(A, B) and i == istar and (c.n, it) == costo_istar(istar)
    filas.append((n, peor))
    print(f"  {n:>6} {peor:>12} {cota_alg(n):>18} {cota_inf(n):>24} {it_max:>16}")
    assert peor <= cota_alg(n)
print("  (el costo solo depende de i*, la particion correcta: n <= 10, todas las C(2n,n) entradas; n mayor, simulacion sobre todo i* = 0..n y ~44 entradas reales por n que la confirman)")

print()
print("=== 3. Cota inferior: 2n posiciones distintas para la respuesta, y hojas distintas ===")
for n in range(1, 8):
    pos = set()
    hojas = set()
    prof = 0
    for A, B in todas_distintas(n):
        v = verdad(A, B)
        pos.add(("A", A.index(v)) if v in A else ("B", B.index(v)))
        # transcripcion de comparaciones y respuestas (la hoja), con el algoritmo
        traza = []

        class CmpT(Cmp):
            def le(self, a, b):
                r = a <= b
                traza.append(r)
                self.n += 1
                return r
        c = CmpT()
        val, i, _ = mediana(A, B, c)
        hojas.add((tuple(traza), ("A", A.index(val)) if val in A else ("B", B.index(val))))
        prof = max(prof, len(traza))
    print(f"  n={n}: posiciones distintas de la respuesta = {len(pos)} (= 2n = {2 * n}); hojas distintas del algoritmo = {len(hojas)} (>= 2n); "
          f"cota ceil(log2 2n) = {cota_inf(n)}; profundidad del algoritmo = {prof}")
    assert len(pos) == 2 * n and len(hojas) >= 2 * n

print()
print("=== 4. Versiones equivocadas (errores de una unidad) y quien las atrapa ===")
defectos = ["hi=n-1", "lo=1", "A[i-1] sin centinela", "indice de B corrido en el max final"]
print(f"  {'defecto':<30}" + "".join(f"{g[:18]:>20}" for g in list(gens)[:6]))
for d in defectos:
    fila = []
    for nombre, g in list(gens.items())[:6]:
        f = tot = 0
        for n in range(1, 40):
            for _ in range(3 if "aleatorios" in nombre else 1):
                A, B = g(n)
                tot += 1
                try:
                    f += mediana_mala(A, B, d) != verdad(A, B)
                except IndexError:
                    f += 1
        fila.append(100 * f / tot)
    print(f"  {d:<30}" + "".join(f"{x:>19.0f}%" for x in fila))
for d in defectos:
    hallado = None
    for n in range(1, 5):
        for A, B in con_duplicados(n, 4):
            try:
                mal = mediana_mala(A, B, d) != verdad(A, B)
            except IndexError:
                mal = True
            if mal:
                hallado = (A, B)
                break
        if hallado:
            break
    print(f"  entrada mas chica que rompe '{d}': A={hallado[0]}, B={hallado[1]}, correcto {verdad(*hallado)}")
    try:
        print(f"      devuelve {mediana_mala(hallado[0], hallado[1], d)}")
    except IndexError:
        print("      IndexError")

print()
print("=== 5. k-esimo menor con largos distintos m y n: O(log min(m,n)) ===")
errores = 0
casos = 0
for m in range(1, 5):
    for nb in range(1, 6):
        for V in (3, 4):
            arrA = [list(t) for t in itertools.combinations_with_replacement(range(V), m)]
            arrB = [list(t) for t in itertools.combinations_with_replacement(range(V), nb)]
            for A in arrA:
                for B in arrB:
                    for k in range(1, m + nb + 1):
                        if m == 0:
                            continue
                        casos += 1
                        e = sorted(A + B)[k - 1]
                        errores += kesimo(A, B, k) != e or kesimo_descarte(A, B, k) != e
print(f"  {casos} casos exhaustivos pequenos (m 1..4, n 1..5, valores con duplicados, todo k): errores = {errores}")
print(f"  {'m':>5} {'n':>7} {'k':>7} {'comp. particion (peor)':>23} {'ceil(log2(min+1))+1':>20} {'comp. descarte (peor)':>22}")
for m, nb in ((8, 8), (8, 1000), (64, 20000), (1000, 1000), (3, 50000)):
    pw = dw = 0
    for _ in range(100):
        A = sorted(random.sample(range(10 ** 7), m))
        B = sorted(random.sample(range(10 ** 7), nb))
        k = random.choice([1, m + nb, (m + nb) // 2, random.randint(1, m + nb)])
        e = sorted(A + B)[k - 1]
        c1, c2 = Cmp(), Cmp()
        assert kesimo(A, B, k, c1) == e == kesimo_descarte(A, B, k, c2)
        pw, dw = max(pw, c1.n), max(dw, c2.n)
    print(f"  {m:>5} {nb:>7} {'varios':>7} {pw:>23} {math.ceil(math.log2(min(m, nb) + 1)) + 1:>20} {dw:>22}")
print("  posiciones que pueden ser la respuesta (cota de informacion) con m=3, n=6, todos los k:")
for k in range(1, 10):
    pos = set()
    for sub in itertools.combinations(range(9), 3):
        A = list(sub)
        B = [v for v in range(9) if v not in sub]
        v = sorted(A + B)[k - 1]
        pos.add(("A", A.index(v)) if v in A else ("B", B.index(v)))
    print(f"    k={k}: {len(pos)} posiciones posibles -> al menos ceil(log2 {len(pos)}) = {math.ceil(math.log2(len(pos)))} comparaciones")


# ---- busqueda minimax del arbol de decision OPTIMO (entradas = intercalados consistentes)
import sys
import time

sys.setrecursionlimit(10000)


def peor_particion(n):
    """Peor caso exacto del algoritmo de la particion (simulacion sobre todo i*)."""
    peor = 0
    for istar in range(n + 1):
        lo, hi, it = 0, n, 0
        while lo < hi:
            mid = (lo + hi) // 2
            it += 1
            if mid >= istar:
                hi = mid
            else:
                lo = mid + 1
        peor = max(peor, it + (1 if 0 < istar < n else 0))
    return peor


def minimax(n):
    """Profundidad optima de un arbol de decision cuyas consultas son A[i] < B[j]? y cuyas hojas son una posicion de
    la respuesta. Estados = conjuntos de intercalados consistentes (bitmasks sobre las C(2n,n) entradas)."""
    subs = list(itertools.combinations(range(2 * n), n))     # rangos (en el orden total) ocupados por A
    C = len(subs)
    Ar, Br, pos_of = [], [], []
    for sub in subs:
        comp = [v for v in range(2 * n) if v not in sub]
        Ar.append(sub)
        Br.append(comp)
        pos_of.append(sub.index(n - 1) if (n - 1) in sub else n + comp.index(n - 1))   # 0..n-1: A[i]; n..2n-1: B[j]
    ans = [0] * (2 * n)
    for k, p in enumerate(pos_of):
        ans[p] |= 1 << k
    lt = {}
    for i in range(n):
        for j in range(n):
            m = 0
            for k in range(C):
                if Ar[k][i] < Br[k][j]:
                    m |= 1 << k
            lt[(i, j)] = m
    ALL = (1 << C) - 1
    memo = {}

    def nresp(S):
        return sum(1 for p in range(2 * n) if S & ans[p])

    def puede(S, d):
        key = (S, d)
        if key in memo:
            return memo[key]
        c = nresp(S)
        if c <= 1:
            memo[key] = True
        elif d == 0 or c > (1 << d):
            memo[key] = False
        else:
            res = False
            for q, m in lt.items():
                L = S & m
                if L == 0 or L == S:
                    continue
                R = S ^ L
                if nresp(L) > (1 << (d - 1)) or nresp(R) > (1 << (d - 1)):
                    continue
                if puede(L, d - 1) and puede(R, d - 1):
                    res = True
                    break
            memo[key] = res
        return memo[key]

    def arbol(S, d):
        """Extrae el arbol de profundidad <= d (existe si puede(S,d))."""
        c = nresp(S)
        if c <= 1:
            p = next(p for p in range(2 * n) if S & ans[p])
            return ("hoja", p)
        for q, m in lt.items():
            L = S & m
            if L == 0 or L == S:
                continue
            R = S ^ L
            if nresp(L) > (1 << (d - 1)) or nresp(R) > (1 << (d - 1)):
                continue
            if puede(L, d - 1) and puede(R, d - 1):
                return ("q", q, arbol(L, d - 1), arbol(R, d - 1))
        raise RuntimeError

    d = math.ceil(math.log2(2 * n))
    while not puede(ALL, d):
        d += 1
    T = arbol(ALL, d)
    # verificacion independiente del arbol extraido sobre TODAS las entradas
    prof = 0
    for k in range(C):
        nodo, pasos = T, 0
        while nodo[0] == "q":
            i, j = nodo[1]
            nodo = nodo[2] if Ar[k][i] < Br[k][j] else nodo[3]
            pasos += 1
        assert nodo[1] == pos_of[k], (n, k)
        prof = max(prof, pasos)
    assert prof <= d
    return d, T, C, prof


def mostrar(T, n, sangria=""):
    if T[0] == "hoja":
        p = T[1]
        print(f"{sangria}-> la respuesta es {'A[' + str(p) + ']' if p < n else 'B[' + str(p - n) + ']'}")
        return
    i, j = T[1]
    print(f"{sangria}A[{i}] < B[{j}]?  si:")
    mostrar(T[2], n, sangria + "    ")
    print(f"{sangria}                 no:")
    mostrar(T[3], n, sangria + "    ")


print()
print("=== 6. Busqueda minimax: el arbol de decision OPTIMO, n = 1..10 ===")
print("  Estados = conjuntos de intercalados consistentes; consultas = A[i] < B[j]?; hoja cuando todos dan la misma posicion de respuesta.")
print(f"  {'n':>3} {'entradas':>9} {'cota ceil(log2 2n)':>19} {'optimo (minimax)':>17} {'algoritmo de la particion':>26} {'arbol verificado en todas':>26} {'1a consulta del arbol':>22}")
arboles = {}
for n in range(1, 11):
    d, T, C, prof = minimax(n)
    arboles[n] = T
    raiz = f"A[{T[1][0]}] < B[{T[1][1]}]" if T[0] == "q" else "(sin consultas)"
    print(f"  {n:>3} {C:>9} {cota_inf(n):>19} {d:>17} {peor_particion(n):>26} {'si (profundidad ' + str(prof) + ')':>26} {raiz:>22}")
    assert d == cota_inf(n)
print("  El optimo coincide con la cota de informacion ceil(log2 2n) en todos los n calculados; el algoritmo de la particion pierde una")
print("  comparacion exactamente cuando n es potencia de 2 (n = 2, 4, 8).")
print()
print("  Arbol optimo para n = 2 (2 comparaciones):")
mostrar(arboles[2], 2, "    ")
print()
print("  Arbol optimo para n = 4 (3 comparaciones):")
mostrar(arboles[4], 4, "    ")
print()
print("  Reparto de las 2n posiciones de la respuesta que hace la primera consulta del algoritmo de la particion, A[mid] vs B[n-mid-1]:")
for n in (2, 4, 8, 16, 1024):
    mid = n // 2
    print(f"    n={n:>4}: mid={mid}: se parten en {2 * mid + 1} y {2 * n - 2 * mid - 1} (dos numeros IMPARES: nunca {n} y {n})")

# ---- figura: el camino de la mezcla y la antidiagonal
A, B = [1, 4, 5, 8, 9, 12], [2, 3, 6, 7, 10, 11]
n = len(A)
ruta = [(0, 0)]
x = y = 0
while x < n or y < n:
    if y == n or (x < n and A[x] <= B[y]):
        x += 1
    else:
        y += 1
    ruta.append((x, y))
sondas = []
lo, hi = 0, n
while lo < hi:
    mid = (lo + hi) // 2
    r = B[n - mid - 1] <= A[mid]
    sondas.append((mid, r))
    if r:
        hi = mid
    else:
        lo = mid + 1
v, istar, _ = mediana(A, B)
lineas = ["\\begin{tikzpicture}[x=0.9cm,y=0.9cm,every node/.style={font=\\scriptsize}]"]
for t in range(n + 1):
    lineas.append(f"\\draw[gray!35] ({t},0)--({t},{n}); \\draw[gray!35] (0,{t})--({n},{t});")
    lineas.append(f"\\node[below] at ({t},-0.05) {{{t}}}; \\node[left] at (-0.05,{t}) {{{t}}};")
lineas.append(f"\\draw[orange,dashed,very thick] (0,{n})--({n},0);")
lineas.append("\\draw[blue,very thick] " + " -- ".join(f"({a},{b})" for a, b in ruta) + ";")
for k, (mid, r) in enumerate(sondas, 1):
    col = "red" if r else "teal"
    lineas.append(f"\\fill[{col}] ({mid},{n - mid}) circle (2.6pt);")
    lineas.append(f"\\node[above right,{col}] at ({mid},{n - mid}) {{sonda {k}}};")
lineas.append(f"\\fill[blue] ({istar},{n - istar}) circle (3.4pt);")
lineas.append(f"\\node[below left,blue] at ({istar},{n - istar}) {{$i^*={istar}$}};")
lineas.append(f"\\node[below] at ({n / 2},-0.7) {{i = elementos de $A$ tomados}}; \\node[rotate=90,above] at (-0.7,{n / 2}) {{elementos de $B$ tomados}};")
lineas.append("\\end{tikzpicture}")
open("ej07_fig.tex", "w").write("\n".join(lineas) + "\n")
print()
print(f"=== 7. La figura: A={A}, B={B}: la mezcla pasa por la antidiagonal en i*={istar}; sondas (i, P(i)): {sondas}; mediana = {v} ===")
