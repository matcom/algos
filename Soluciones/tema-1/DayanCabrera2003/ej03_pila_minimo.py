"""Ejercicio 3: pila con minimo en O(1) en el peor caso (C3: invariantes).
Tres versiones: A (pares valor/minimo del prefijo), B (pila auxiliar solo con <=), C (codificada 2x-min).
Mas la variante defectuosa de B con '<'. Todas contra un oraculo min(S)."""
import itertools
import random
import statistics

random.seed(3)


# ---------------------------------------------------------------- versiones
class PilaA:
    """S[i] y M[i] = min(S[0..i]). Invariante IA."""
    def __init__(self):
        self.S, self.M = [], []
        self.cmp = 0            # comparaciones de la ultima operacion

    def push(self, x):
        self.cmp = 0
        if self.M:
            self.cmp = 1
            m = x if x < self.M[-1] else self.M[-1]
        else:
            m = x
        self.S.append(x)
        self.M.append(m)

    def pop(self):
        self.cmp = 0
        self.M.pop()
        return self.S.pop()

    def top(self):
        self.cmp = 0
        return self.S[-1]

    def minimo(self):
        self.cmp = 0
        return self.M[-1]

    def extra(self):
        return len(self.M)

    def invariante(self):
        return len(self.S) == len(self.M) and all(
            self.M[i] == min(self.S[:i + 1]) for i in range(len(self.S)))


class PilaB:
    """M guarda x solo si x <= minimo actual (estricto=False, correcta). Invariante IB:
    M = [S[i] : i = 0 o S[i] <= min(S[0..i-1])]."""
    def __init__(self, estricto=False):
        self.S, self.M = [], []
        self.estricto = estricto      # True: usa '<' en push (defectuosa con duplicados)
        self.cmp = 0

    def push(self, x):
        self.cmp = 0
        if self.M:
            self.cmp = 1
            guardar = x < self.M[-1] if self.estricto else x <= self.M[-1]
        else:
            guardar = True
        if guardar:
            self.M.append(x)
        self.S.append(x)

    def pop(self):
        y = self.S.pop()
        self.cmp = 1
        if y == self.M[-1]:           # y es un record  <=>  y == min(S)
            self.M.pop()
        return y

    def top(self):
        self.cmp = 0
        return self.S[-1]

    def minimo(self):
        self.cmp = 0
        return self.M[-1]

    def extra(self):
        return len(self.M)

    def invariante(self):
        esperado = [self.S[i] for i in range(len(self.S))
                    if i == 0 or self.S[i] <= min(self.S[:i])]
        return self.M == esperado


class PilaC:
    """Memoria extra O(1): una sola variable 'mn'. E[i] = S[i] si S[i] >= m_{i-1}, y 2 S[i] - m_{i-1] si no.
    w=None: enteros sin limite. w=k: aritmetica de k bits con complemento a dos (se envuelve)."""
    def __init__(self, w=None):
        self.E, self.mn, self.w = [], None, w

    def _ajusta(self, v):
        if self.w is None:
            return v
        m = 1 << self.w
        v %= m
        return v - m if v >= m // 2 else v

    def push(self, x):
        if not self.E:
            self.E.append(x)
            self.mn = x
        elif x >= self.mn:
            self.E.append(x)
        else:
            self.E.append(self._ajusta(2 * x - self.mn))
            self.mn = x

    def pop(self):
        y = self.E.pop()
        if y >= self.mn:
            return y
        real = self.mn
        self.mn = self._ajusta(2 * self.mn - y)
        return real

    def top(self):
        y = self.E[-1]
        return y if y >= self.mn else self.mn

    def minimo(self):
        if not self.E:
            raise IndexError("pila vacia")
        return self.mn


class Oraculo:
    def __init__(self):
        self.S = []

    def push(self, x):
        self.S.append(x)

    def pop(self):
        return self.S.pop()

    def top(self):
        return self.S[-1]

    def minimo(self):
        return min(self.S)


def ejecutar(P, ops):
    """Aplica ops (precondicion respetada) y devuelve la lista de salidas, o ('ERROR', e)."""
    sal = []
    try:
        for op in ops:
            if op[0] == "push":
                P.push(op[1])
            elif op[0] == "pop":
                sal.append(P.pop())
            elif op[0] == "top":
                sal.append(P.top())
            else:
                sal.append(P.minimo())
    except Exception as e:                   # noqa: BLE001
        return ("ERROR", type(e).__name__)
    return sal


def secuencias(alfabeto, largo):
    """Todas las secuencias de operaciones validas (sin pop/top/min sobre pila vacia)."""
    ops = [("push", v) for v in alfabeto] + [("pop",), ("top",), ("min",)]

    def rec(pref, tam):
        if len(pref) == largo:
            return
        for o in ops:
            if o[0] != "push" and tam == 0:
                continue
            nuevo = pref + [o]
            yield nuevo
            yield from rec(nuevo, tam + (1 if o[0] == "push" else -1 if o[0] == "pop" else 0))
    yield from rec([], 0)


def fabrica(nombre):
    return {"A": PilaA, "B(<=)": lambda: PilaB(False), "B(<)": lambda: PilaB(True),
            "C": PilaC}[nombre]


print("=== 1. Exhaustivo: toda secuencia valida hasta largo 7, valores {0,1,2}, contra el oraculo ===")
total = 0
fallos = {n: [] for n in ("A", "B(<=)", "B(<)", "C")}
for sec in secuencias((0, 1, 2), 7):
    total += 1
    esperado = ejecutar(Oraculo(), sec)
    for n in fallos:
        if ejecutar(fabrica(n)(), sec) != esperado:
            fallos[n].append(sec)
print(f"  {total} secuencias")
for n, f in fallos.items():
    print(f"  version {n:>6}: {len(f)} secuencias que difieren del oraculo")
assert not fallos["A"] and not fallos["B(<=)"] and not fallos["C"]
corta = min(len(s) for s in fallos["B(<)"])
minimas = [s for s in fallos["B(<)"] if len(s) == corta]
print(f"  B con '<': secuencias mas cortas que la rompen (largo {corta}): {len(minimas)}")
for s in minimas:
    print("   ", [o[0] + ("(" + str(o[1]) + ")" if len(o) > 1 else "") for o in s])
sec = minimas[0]
print("  ejecucion de la primera, B(<) contra el oraculo:",
      ejecutar(PilaB(True), sec), "vs", ejecutar(Oraculo(), sec))
print("  y con B(<=):", ejecutar(PilaB(False), sec))

print()
print("=== 1b. El ejemplo de la figura: push 5,3,3,7,2,2,9 y luego pop, pop, minimo ===")
ej = [("push", v) for v in (5, 3, 3, 7, 2, 2, 9)] + [("pop",), ("pop",), ("min",)]
for n in ("A", "B(<=)", "B(<)"):
    P = fabrica(n)()
    print(f"  {n:>6}: salidas {ejecutar(P, ej)}   M final = {getattr(P, 'M', None)}")
print(f"  oraculo: salidas {ejecutar(Oraculo(), ej)}")
P = PilaB(False)
for v in (5, 3, 3, 7, 2, 2, 9):
    P.push(v)
print(f"  tras los 7 pushes:  M_A = {[min([5,3,3,7,2,2,9][:i+1]) for i in range(7)]}  M_B(<=) = {P.M}", end="")
P = PilaB(True)
for v in (5, 3, 3, 7, 2, 2, 9):
    P.push(v)
print(f"  M_B(<) = {P.M}")

print()
print("=== 2. Aleatorio con invariante vigilado (A, B(<=)) y salidas contra el oraculo ===")
ops_totales = 0
for _ in range(3000):
    alfa = random.choice([2, 3, 5, 1000])
    A, B, Cc, O = PilaA(), PilaB(False), PilaC(), Oraculo()
    for _ in range(80):
        r = random.random()
        if r < 0.5 or not O.S:
            x = random.randrange(alfa)
            for P in (A, B, Cc, O):
                P.push(x)
        elif r < 0.8:
            sal = [P.pop() for P in (A, B, Cc, O)]
            assert len(set(sal)) == 1
        elif r < 0.9:
            sal = [P.top() for P in (A, B, Cc, O)]
            assert len(set(sal)) == 1
        else:
            sal = [P.minimo() for P in (A, B, Cc, O)]
            assert len(set(sal)) == 1
        assert A.invariante() and B.invariante()
        ops_totales += 1
print(f"  3000 secuencias de 80 operaciones (alfabetos de 2, 3, 5 y 1000 valores): {ops_totales} operaciones, sin fallos")

print()
print("=== 3. Casos borde: pila vacia (precondicion) ===")
for nombre in ("A", "B(<=)", "C"):
    P = fabrica(nombre)()
    res = []
    for op in ("pop", "top", "minimo"):
        try:
            getattr(P, op)()
            res.append(f"{op}: sin error")
        except IndexError:
            res.append(f"{op}: IndexError")
    print(f"  {nombre:>6}: {', '.join(res)}")

print()
print("=== 4. Memoria extra en el peor caso (|M| tras n pushes, n = 1000) ===")
n = 1000
casos = {"creciente": list(range(n)), "decreciente": list(range(n, 0, -1)), "todos iguales": [7] * n}
for nombre, xs in casos.items():
    A, B, Bs = PilaA(), PilaB(False), PilaB(True)
    for x in xs:
        A.push(x)
        B.push(x)
        Bs.push(x)
    print(f"  {nombre:>14}: |S|={n}  A: |M|={A.extra()}  B(<=): |M|={B.extra()}  B(<) [incorrecta]: |M|={Bs.extra()}")
for nombre, gen in (("permutacion", lambda: random.sample(range(n), n)),
                    ("alfabeto de 3", lambda: [random.randrange(3) for _ in range(n)]),
                    ("alfabeto de 100", lambda: [random.randrange(100) for _ in range(n)])):
    tam = []
    for _ in range(300):
        B = PilaB(False)
        for x in gen():
            B.push(x)
        tam.append(B.extra())
    H = sum(1 / k for k in range(1, n + 1))
    extra = f"  (H_n = {H:.2f})" if nombre == "permutacion" else ""
    print(f"  {nombre:>15}: media |M| = {statistics.mean(tam):7.2f}, maximo {max(tam):4d}{extra}")

print()
print("=== 5. Peor caso por operacion (comparaciones), 100000 operaciones aleatorias ===")
for nombre, F in (("A", PilaA), ("B(<=)", lambda: PilaB(False))):
    P, O = F(), Oraculo()
    mx = {"push": 0, "pop": 0, "min": 0}
    for _ in range(100000):
        r = random.random()
        if r < 0.5 or not O.S:
            x = random.randrange(50)
            P.push(x)
            O.push(x)
            mx["push"] = max(mx["push"], P.cmp)
        elif r < 0.9:
            P.pop()
            O.pop()
            mx["pop"] = max(mx["pop"], P.cmp)
        else:
            P.minimo()
            mx["min"] = max(mx["min"], P.cmp)
    print(f"  {nombre:>6}: maximo de comparaciones por operacion = {mx}")

print()
print("=== 6. Arreglo dinamico (duplicando): coste de un push suelto vs amortizado ===")
for k in (10, 14, 18):
    cap, tam, costes = 1, 0, []
    for _ in range(2 ** k + 1):
        c = 1
        if tam == cap:
            c += tam              # copiar al nuevo arreglo
            cap *= 2
        tam += 1
        costes.append(c)
    print(f"  {2**k+1:>7} pushes: peor push = {max(costes):>7}, media = {sum(costes)/len(costes):.3f}")

print()
print("=== 7. Version C (2x - min): memoria extra O(1) y desbordamiento en w bits ===")
w = 8
print(f"  enteros sin limite: ya verificada contra el oraculo en la seccion 1 y 2")
def busca_minima(w):
    """Busca por longitud (1, 2, 3) la secuencia mas corta que rompe PilaC(w): longitud 1 y 2
    exhaustivas sobre todo el alfabeto; longitud 3 con ultima operacion observable (pop/top/min):
    una secuencia minima no puede terminar en push, porque push no produce salida ni error."""
    lo, hi = -(1 << (w - 1)), (1 << (w - 1)) - 1
    vals = range(lo, hi + 1)
    nmin = {}
    for largo in (1, 2, 3):
        malas = []
        if largo == 1:
            cand = [[("push", v)] for v in vals]
        elif largo == 2:
            cand = [[("push", v), o] for v in vals for o in (("pop",), ("top",), ("min",))]
            cand += [[("push", v), ("push", u)] for v in vals for u in vals] if w <= 4 else []
        else:
            cand = []
            for v in vals:
                for seg in [[("push", u)] for u in vals] + [[o] for o in (("pop",), ("top",), ("min",))]:
                    for o in (("pop",), ("top",), ("min",)):
                        cand.append([("push", v)] + seg + [o])
        for sec in cand:
            if sec[0][0] != "push":
                continue
            try:
                esperado = ejecutar(Oraculo(), sec)
            except Exception:                         # noqa: BLE001
                continue                              # secuencia invalida (precondicion)
            if isinstance(esperado, tuple):
                continue
            if ejecutar(PilaC(w), sec) != esperado:
                malas.append(sec)
        nmin[largo] = malas
        if malas:
            break
    return nmin


for w in (4, 8):
    nm = busca_minima(w)
    largo = max(nm)
    print(f"  w={w}: secuencias que rompen, por largo: " +
          ", ".join(f"largo {k}: {len(v)}" for k, v in nm.items()))
    ej = nm[largo][0]
    print("    la primera de largo minimo:", [o[0] + ("(" + str(o[1]) + ")" if len(o) > 1 else "") for o in ej],
          "->", ejecutar(PilaC(w), ej), "(oraculo:", ejecutar(Oraculo(), ej), ")")
a, b = 100, -100
P = PilaC(w)
P.push(a); P.push(b)
print(f"    detalle: push(100), push(-100): E = {P.E}, mn = {P.mn}; 2*(-100)-100 = -300 -> {P._ajusta(-300)} en 8 bits")
print(f"    pop devuelve {P.pop()} (debia ser -100); pop devuelve {P.pop()} (debia ser 100)")
for w in (8, 16, 32):
    seguro = 2 ** (w - 3)
    malos = seguro_ok = 0
    for _ in range(20000):
        rango = 2 ** (w - 1)
        ops = [("push", random.randint(-rango, rango - 1)) for _ in range(6)] + [("pop",)] * 6
        esperado = ejecutar(Oraculo(), ops)
        if ejecutar(PilaC(w), ops) != esperado:
            malos += 1
        ops2 = [("push", random.randint(-seguro, seguro)) for _ in range(6)] + [("pop",)] * 6
        if ejecutar(PilaC(w), ops2) == ejecutar(Oraculo(), ops2):
            seguro_ok += 1
    print(f"  w={w:>2}: valores en todo el rango: fallan {malos}/20000; en |x| <= 2^(w-3)={seguro}: aciertan {seguro_ok}/20000")
    assert seguro_ok == 20000

print()
print("=== 8. Cola con minimo con dos pilas (A): contra un oraculo y coste amortizado ===")
from collections import deque


class ColaMin:
    """Dos pilas A: 'ent' (se encola) y 'sal' (se desencola). ops cuenta operaciones de pila."""
    def __init__(self):
        self.ent, self.sal = PilaA(), PilaA()
        self.n_ent = self.n_sal = 0
        self.ops = 0

    def encolar(self, x):
        self.ent.push(x)
        self.n_ent += 1
        self.ops += 1

    def desencolar(self):
        if not self.n_sal:
            while self.n_ent:
                self.sal.push(self.ent.pop())
                self.n_ent -= 1
                self.n_sal += 1
                self.ops += 2
        self.n_sal -= 1
        self.ops += 1
        return self.sal.pop()

    def minimo(self):
        c = []
        if self.n_ent:
            c.append(self.ent.minimo())
        if self.n_sal:
            c.append(self.sal.minimo())
        return min(c)


for _ in range(500):
    C, O = ColaMin(), deque()
    enc = des = 0
    for _ in range(300):
        r = random.random()
        if r < 0.5 or not O:
            x = random.randrange(10)
            C.encolar(x)
            O.append(x)
            enc += 1
        elif r < 0.85:
            assert C.desencolar() == O.popleft()
            des += 1
        else:
            assert C.minimo() == min(O)
        assert C.ops <= 3 * enc + 1 * des          # costo real <= suma de costos amortizados (3 y 1)
print("  500 secuencias de 300 operaciones: salidas iguales al oraculo (deque + min ingenuo);")
print("  en todos los prefijos: operaciones de pila reales <= 3*encolar + 1*desencolar (potencial 2|ent|)")
for m in (10**3, 10**5):
    C = ColaMin()
    for i in range(m):
        C.encolar(i)
    for i in range(m):
        C.desencolar()
    print(f"  {m} encolar + {m} desencolar: {C.ops} operaciones de pila = {C.ops / m:.0f}m "
          f"(cota amortizada 3m + m = 4m)")
single = ColaMin()
for i in range(10**5):
    single.encolar(i)
mv0 = single.ops
single.desencolar()
print(f"  un desencolar suelto con 10^5 elementos en la entrada cuesta {single.ops - mv0} operaciones de pila (O(n), no O(1))")
