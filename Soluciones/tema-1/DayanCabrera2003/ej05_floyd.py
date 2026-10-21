"""Ejercicio 5: deteccion de ciclos de Floyd (liebre y tortuga). C3: invariante y potencial.
mu = nodos antes del ciclo, lam = largo del ciclo. Sin ciclo: n nodos y luego None.
Cada lectura del puntero .next se cuenta (Nodo.lecturas)."""
import math
import tracemalloc


class Nodo:
    __slots__ = ("_next", "id")
    lecturas = 0

    def __init__(self, i):
        self._next = None
        self.id = i

    @property
    def next(self):
        Nodo.lecturas += 1
        return self._next


def con_ciclo(mu, lam):
    """Nodos 0..mu+lam-1; el ultimo apunta al nodo mu. Requiere lam >= 1."""
    ns = [Nodo(i) for i in range(mu + lam)]
    for i in range(mu + lam - 1):
        ns[i]._next = ns[i + 1]
    ns[-1]._next = ns[mu]
    return ns[0]


def sin_ciclo(n):
    ns = [Nodo(i) for i in range(n)]
    for i in range(n - 1):
        ns[i]._next = ns[i + 1]
    return ns[0] if n else None


def f(s, mu, lam):
    """Indice del nodo tras s pasos desde la cabeza."""
    return s if s < mu + lam else mu + (s - mu) % lam


def floyd(head):
    """Devuelve (hay_ciclo, pasos, nodo_de_encuentro). pasos = iteraciones iniciadas."""
    if head is None:
        return False, 0, None
    t = h = head
    pasos = 0
    while True:
        t = t.next                       # lectura 1
        h = h.next                       # lectura 2
        pasos += 1
        if h is None:
            return False, pasos, None
        h = h.next                       # lectura 3
        if h is None:
            return False, pasos, None
        if t is h:
            return True, pasos, t


def floyd_vigilado(head, mu, lam):
    """Floyd con invariante t=f(s), h=f(2s) y potenciales vigilados con assert. Devuelve pasos."""
    t = h = head
    s = 0
    ant = None
    while True:
        # potencial lexicografico (fase 1, fase 2) como pares de enteros
        fase1 = max(mu - s, 0)
        fase2 = lam * math.ceil((s + 1) / lam) - s          # pasos hasta el proximo multiplo de lam
        pot = (fase1, fase2)
        if ant is not None and ant[0] > 0:
            assert pot[0] == ant[0] - 1                       # baja 1 en la fase 1
        if ant is not None and ant[0] == 0:
            assert pot[0] == 0 and pot[1] == ant[1] - 1       # baja 1 en la fase 2
        ant = pot
        assert t.id == f(s, mu, lam) and h.id == f(2 * s, mu, lam)   # invariante
        t = t.next
        h = h.next.next
        s += 1
        if t is h:
            return s


def pasos_formula(mu, lam):
    return lam if mu == 0 else lam * math.ceil(mu / lam)


def inicio_y_largo(head):
    """Fase 2 de Floyd. Devuelve (mu, lam, pasos_fase1, pasos_fase2, pasos_largo) o None."""
    hay, p1, m = floyd(head)
    if not hay:
        return None
    p, q, mu = head, m, 0
    while p is not q:
        p, q = p.next, q.next
        mu += 1
    lam, q = 1, p.next
    while q is not p:
        q = q.next
        lam += 1
    return mu, lam, p1, mu, lam


print("=== 1. Casos limite ===")
r = floyd(None)
print(f"  lista vacia:                 hay_ciclo={r[0]}, pasos={r[1]}")
r = floyd(sin_ciclo(1))
print(f"  un nodo sin ciclo (n=1):     hay_ciclo={r[0]}, pasos={r[1]}")
Nodo.lecturas = 0
r = floyd(con_ciclo(0, 1))
print(f"  un nodo con autolazo (0,1):  hay_ciclo={r[0]}, pasos={r[1]}, lecturas={Nodo.lecturas}")
for mu, lam in ((0, 2), (1, 1), (3, 4), (5, 3)):
    Nodo.lecturas = 0
    r = floyd(con_ciclo(mu, lam))
    print(f"  mu={mu}, lam={lam}: hay_ciclo={r[0]}, pasos={r[1]} (formula {pasos_formula(mu, lam)}), "
          f"encuentro en el nodo {r[2].id}")

print()
print("=== 2. Con ciclo: pasos exactos, lecturas y nodo de encuentro, mu en 0..60, lam en 1..60 ===")
malos = 0
maxpasos_extra = 0
for mu in range(0, 61):
    for lam in range(1, 61):
        head = con_ciclo(mu, lam)
        Nodo.lecturas = 0
        hay, pasos, m = floyd(head)
        ok = (hay and pasos == pasos_formula(mu, lam) and Nodo.lecturas == 3 * pasos
              and m.id == mu + ((-mu) % lam) and pasos <= mu + lam)
        malos += not ok
        maxpasos_extra = max(maxpasos_extra, pasos - (mu + lam))
print(f"  3600 listas; casos donde falla alguna comprobacion: {malos}")
print(f"  max(pasos - (mu+lam)) = {maxpasos_extra}  (cota pasos <= mu+lam; igualdad solo con mu=0)")
iguales = [(mu, lam) for mu in range(0, 61) for lam in range(1, 61)
           if pasos_formula(mu, lam) == mu + lam]
print(f"  igualdad pasos = mu+lam solo cuando mu = 0: {all(m == 0 for m, _ in iguales)}  ({len(iguales)} casos)")
tot = 0
for mu in range(0, 31):
    for lam in range(1, 31):
        tot += floyd_vigilado(con_ciclo(mu, lam), mu, lam)
print(f"  invariante t=f(s), h=f(2s) y potenciales (fase1, fase2) vigilados en {tot} pasos, mu,lam <= 30: sin fallos")

print()
print("=== 3. Sin ciclo: pasos y lecturas exactos para n = 0..300 ===")
malos = 0
for n in range(0, 301):
    Nodo.lecturas = 0
    hay, pasos, _ = floyd(sin_ciclo(n))
    lect_esp = 0 if n == 0 else (3 * n // 2 if n % 2 == 0 else (3 * n + 1) // 2)
    if hay or pasos != math.ceil(n / 2) or Nodo.lecturas != lect_esp:
        malos += 1
print(f"  n=0..300: fallos = {malos}  (pasos = ceil(n/2); lecturas = 3n/2 si n par, (3n+1)/2 si impar)")
for n in (0, 1, 2, 3, 4, 5, 100, 101):
    Nodo.lecturas = 0
    hay, pasos, _ = floyd(sin_ciclo(n))
    print(f"    n={n:>3}: pasos={pasos:>3}, lecturas={Nodo.lecturas:>3}")

print()
print("=== 4. Traza: mu=3, lam=4  (nodos v0 v1 v2 | v3 v4 v5 v6 -> v3) ===")
mu, lam = 3, 4
print("  paso s   t=f(s)   h=f(2s)   t==h")
for s in range(0, 5):
    print(f"  {s:>6}   v{f(s, mu, lam):<6}  v{f(2 * s, mu, lam):<7}  {f(s, mu, lam) == f(2 * s, mu, lam)}")
hay, pasos, m = floyd(con_ciclo(mu, lam))
print(f"  Floyd: hay_ciclo={hay}, pasos={pasos}, encuentro en v{m.id}")
head = con_ciclo(mu, lam)
_, _, m = floyd(head)
p, q = head, m
print("  fase 2: p desde la cabeza, q desde el encuentro, avanzan de a 1")
print("     j   p    q")
j = 0
print(f"  {j:>4}  v{p.id}  v{q.id}")
while p is not q:
    p, q = p.next, q.next
    j += 1
    print(f"  {j:>4}  v{p.id}  v{q.id}")
print(f"  se encuentran en v{p.id} tras {j} pasos = mu; luego se recorre el ciclo desde v{p.id}")

print()
print("=== 5. Fase 2: mu y lam, mu en 0..60, lam en 1..60 ===")
malos = 0
for mu in range(0, 61):
    for lam in range(1, 61):
        r = inicio_y_largo(con_ciclo(mu, lam))
        if r is None or r[0] != mu or r[1] != lam:
            malos += 1
print(f"  3600 listas; fallos al recuperar (mu, lam): {malos}")
Nodo.lecturas = 0
inicio_y_largo(con_ciclo(1000, 70))
print(f"  mu=1000, lam=70: lecturas totales = {Nodo.lecturas} "
      f"(= 3*{pasos_formula(1000, 70)} + 2*1000 + 70 = {3 * pasos_formula(1000, 70) + 2000 + 70})")

print()
print("=== 6. Memoria: Floyd (2 punteros) contra conjunto de visitados ===")


def visitados(head):
    vis, p = set(), head
    while p is not None and id(p) not in vis:
        vis.add(id(p))
        p = p._next
    return p is not None, len(vis)


for mu, lam in ((100000, 100000),):
    head = con_ciclo(mu, lam)
    tracemalloc.start()
    r1 = floyd(head)
    _, pico_floyd = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    tracemalloc.start()
    r2 = visitados(head)
    _, pico_vis = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"  mu={mu}, lam={lam} ({mu + lam} nodos): Floyd hay_ciclo={r1[0]} en {r1[1]} pasos, pico de memoria {pico_floyd} bytes;")
    print(f"  visitados hay_ciclo={r2[0]}, {r2[1]} nodos guardados, pico de memoria {pico_vis} bytes (x{pico_vis // max(pico_floyd, 1)})")

print()
print("=== 7. Velocidades (1, k): siempre se encuentran, con la misma salida de partida ===")
from math import gcd


def floyd_k(head, k, desfase=0, tope=100000):
    t = h = head
    for _ in range(desfase):
        h = h.next
    pasos = 0
    while pasos < tope:
        t = t.next
        for _ in range(k):
            h = h.next
            if h is None:
                return False, pasos + 1
        pasos += 1
        if t is h:
            return True, pasos
    return None, pasos


def pasos_k(mu, lam, k):
    per = lam // gcd(k - 1, lam)            # periodo de coincidencia de las posiciones
    base = max(mu, 1)
    return per * math.ceil(base / per)


for k in range(2, 8):
    malos = 0
    for mu in range(0, 41):
        for lam in range(1, 41):
            hay, p = floyd_k(con_ciclo(mu, lam), k)
            if not hay or p != pasos_k(mu, lam, k):
                malos += 1
    print(f"  k={k}: mu,lam <= 40 (1600 listas): se encuentran siempre y pasos = (lam/g)*ceil(max(mu,1)/(lam/g)), "
          f"g=gcd(k-1,lam): fallos = {malos}")

print("  Lecturas de puntero hasta el encuentro, (k+1) * pasos:")
print(f"  {'mu':>4} {'lam':>4} | " + " ".join(f"{'k='+str(k):>9}" for k in (2, 3, 4, 5)))
for mu, lam in ((0, 12), (0, 7), (5, 12), (100, 30), (100, 31), (0, 1000), (1000, 1000)):
    print(f"  {mu:>4} {lam:>4} | " + " ".join(f"{(k + 1) * pasos_k(mu, lam, k):>9}" for k in (2, 3, 4, 5)))

print("  Quien gana en lecturas (assert en mu,lam <= 60):")
for lam in range(1, 61):
    lec = {k: (k + 1) * pasos_k(0, lam, k) for k in (2, 3)}
    assert (lec[3] < lec[2]) == (lam % 2 == 0)
print("    mu = 0: k=3 gana a k=2 si y solo si lam es par (4*lam/g < 3*lam  <=>  g = gcd(2,lam) = 2)")
bien = 0
for mu in range(1, 61):
    for lam in range(1, 61):
        if mu >= 3 * lam - 2:
            assert all(3 * pasos_k(mu, lam, 2) < (k + 1) * pasos_k(mu, lam, k) for k in range(3, 8))
            bien += 1
print(f"    mu >= 3*lam - 2: k=2 gana estrictamente a todo k=3..7 ({bien} pares): 3(mu+lam-1) < 4mu <= (k+1)*s_k")
print("    mu=100, lam=30: k=2: s=120, lecturas 360;  k=3: g=2, s=105, lecturas 420  (mu >= 88)")
print("    mu=100, lam=31: k=2: s=124, lecturas 372;  k=3: g=1, s=124, lecturas 496")

print()
print("=== 8. La variante que parece correcta: la liebre sale delta nodos adelantada ===")
print("  (al entrar al ciclo, la distancia d de h a t cumple d = -delta (mod g), g = gcd(k-1, lam);")
print("   se encuentran  sii  g divide a delta)")
for k in (2, 3, 4, 5):
    resumen = []
    for delta in (0, 1, 2, 3, 4):
        nunca = 0
        for mu in range(0, 13):
            for lam in range(1, 13):
                hay, _ = floyd_k(con_ciclo(mu, lam), k, desfase=delta, tope=3000)
                teoria = delta % gcd(k - 1, lam) == 0
                assert (hay is True) == teoria, (k, delta, mu, lam)
                nunca += (not hay)
        resumen.append(f"delta={delta}: {nunca}")
    print(f"  k={k}: listas (de 156) donde NO se encuentran:  " + ",  ".join(resumen))
print("  (assert: en cada una de las 4*5*156 pruebas, se encuentran  <=>  gcd(k-1, lam) | delta)")
print("  Ejemplos ejecutados:")
for k, mu, lam, delta in ((3, 0, 2, 1), (4, 0, 3, 2), (4, 0, 3, 3), (5, 0, 4, 2)):
    hay, p = floyd_k(con_ciclo(mu, lam), k, desfase=delta, tope=3000)
    print(f"    k={k}, mu={mu}, lam={lam}, delta={delta}: gcd(k-1,lam)={gcd(k - 1, lam)}, "
          f"encuentro={hay}" + (f" en {p} pasos" if hay else " (sin encuentro en 3000 pasos)"))

print()
print("=== 9. Contraejemplo minimo real (ciclo de largo 2, k=3, liebre adelantada 1 nodo) ===")
cands = [(mu + lam, mu, lam) for mu in range(0, 8) for lam in range(1, 8)]
cands.sort()
for tam, mu, lam in cands:
    hay, p = floyd_k(con_ciclo(mu, lam), 3, desfase=1, tope=2000)
    if not hay:
        print(f"  la lista mas pequena (menos nodos) que rompe (1,3) con desfase 1: mu={mu}, lam={lam} ({tam} nodos)")
        break
head = con_ciclo(0, 2)
t = head
h = head.next
tr = []
for s in range(0, 6):
    tr.append((t.id, h.id))
    t = t.next
    h = h.next.next.next
print(f"  posiciones (t, h) en el ciclo de 2 nodos, k=3: {tr}  -> la distancia h-t vale siempre 1 (impar), nunca 0")
print(f"  con salida comun (desfase 0): encuentro en {floyd_k(con_ciclo(0, 2), 3)[1]} paso;  (1,2) con desfase 1: {floyd_k(con_ciclo(0, 2), 2, desfase=1)}")
