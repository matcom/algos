"""Ejercicio 13 — Acceso secuencial en un splay tree que empieza como un camino

Código extraído de ejercicio-13.md, en el mismo orden en que aparece allí.
Ejecutar con:  python ejercicio-13.py
La salida esperada es la de la sección "Salida" de ejercicio-13.md.
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")   # para que la consola de Windows imprima δ, ≤, ⌈⌉...

# ----------------------------------------------------------------------
# Del md, sección: 6. Casos de prueba
# ----------------------------------------------------------------------

import math, random

class Nodo:
    __slots__ = ("k", "l", "r", "p", "s")
    def __init__(self, k):
        self.k, self.l, self.r, self.p, self.s = k, None, None, None, 1

def tam(x): return x.s if x else 0
def actualizar(x): x.s = 1 + tam(x.l) + tam(x.r)

def rotar(x):
    """Sube x un nivel (rotación simple)."""
    p, g = x.p, x.p.p
    if p.l is x:
        p.l = x.r
        if x.r: x.r.p = p
        x.r = p
    else:
        p.r = x.l
        if x.l: x.l.p = p
        x.l = p
    p.p, x.p = x, g
    if g:
        if g.l is p: g.l = x
        else: g.r = x
    actualizar(p); actualizar(x)

def splay(x):
    rot = 0
    while x.p:
        p, g = x.p, x.p.p
        if g is None:                              # zig
            rotar(x); rot += 1
        elif (g.l is p) == (p.l is x):             # zig-zig: primero el padre
            rotar(p); rotar(x); rot += 2
        else:                                      # zig-zag
            rotar(x); rotar(x); rot += 2
    return rot

def subir_a_la_raiz(x):
    rot = 0
    while x.p:
        rotar(x); rot += 1
    return rot

def camino_izquierdo(n):
    """Raíz n, hijo izquierdo n-1, ..., hoja 1. Devuelve la lista de nodos por clave."""
    nodos = [Nodo(k) for k in range(1, n + 1)]
    for k in range(1, n):
        nodos[k].l, nodos[k - 1].p = nodos[k - 1], nodos[k]
    for k in range(n):
        nodos[k].s = k + 1
    return nodos

def raiz(x):
    while x.p: x = x.p
    return x

def potencial(t):
    total, pila = 0.0, [t]
    while pila:
        x = pila.pop()
        if x:
            total += math.log2(x.s); pila += [x.l, x.r]
    return total

def es_abb(t):
    claves, pila, x = [], [], t
    while pila or x:                               # recorrido en orden iterativo
        while x: pila.append(x); x = x.l
        x = pila.pop(); claves.append(x.k)
        if x.s != 1 + tam(x.l) + tam(x.r): return False
        x = x.r
    return claves == sorted(claves)

def dibujar(t, pref=""):
    """Dibujo de lado (la raíz a la izquierda, el hijo derecho arriba)."""
    if t is None: return []
    return dibujar(t.r, pref + "    ") + [pref + str(t.k)] + dibujar(t.l, pref + "    ")

# Ilustración con n = 7
nodos = camino_izquierdo(7)
for k in [1, 2, 3]:
    r = splay(nodos[k - 1])
    print(f"después de acceder {k} ({r} rotaciones):")
    print("\n".join(dibujar(nodos[k - 1])))
    print()

# 1), 2) y 3)
print(f"{'n':>6} {'rot. splay':>11} {'por acceso':>11} {'Σ lema':>9} {'lema/real':>10}"
      f" {'n(3lg n+1)+Φ0-Φn':>18} {'Φ0':>9} {'Φn':>9}")
for n in [10, 100, 1000, 10000, 50000]:
    nodos = camino_izquierdo(n)
    phi0 = potencial(nodos[-1])
    phi = phi0
    total, suma_lema = 0, 0.0
    vigilar = n <= 1000
    for k in range(n):
        x = nodos[k]
        r_t, r_x = math.log2(n), math.log2(x.s)
        c = splay(x)
        assert x.p is None                                 # x quedó en la raíz
        cota = 3 * (r_t - r_x) + 1
        if vigilar:
            phi_nuevo = potencial(x)
            assert c + (phi_nuevo - phi) <= cota + 1e-9    # el lema, ejecutado
            phi = phi_nuevo
        total += c
        suma_lema += cota
    t = raiz(nodos[0])
    assert es_abb(t)
    phin = potencial(t)
    gruesa = n * (3 * math.log2(n) + 1) + phi0 - phin
    assert total <= suma_lema + phi0 - phin + 1e-6
    print(f"{n:6} {total:11} {total / n:11.2f} {suma_lema:9.0f} {(suma_lema + phi0 - phin) / total:10.2f}"
          f" {gruesa:18.0f} {phi0:9.0f} {phin:9.0f}")

# 4) subir a la raíz en el mismo escenario
print(f"\n{'n':>6} {'rot. subir a la raíz':>21} {'por acceso':>11} {'n/2':>7}")
for n in [10, 100, 1000, 3000]:
    nodos = camino_izquierdo(n)
    total = sum(subir_a_la_raiz(nodos[k]) for k in range(n))
    assert es_abb(raiz(nodos[0]))
    print(f"{n:6} {total:21} {total / n:11.2f} {n / 2:7.1f}")

# Extra: el teorema de acceso secuencial dice "desde cualquier árbol inicial".
# Pruebo con árboles iniciales aleatorios (insertando claves al azar sin balancear).
def abb_aleatorio(n):
    claves = list(range(1, n + 1)); random.shuffle(claves)
    nodos = {k: Nodo(k) for k in claves}
    t = nodos[claves[0]]
    for k in claves[1:]:
        x, z = t, nodos[k]
        while True:
            if k < x.k:
                if x.l: x = x.l
                else: x.l, z.p = z, x; break
            else:
                if x.r: x = x.r
                else: x.r, z.p = z, x; break
    def arreglar(x):
        if x: arreglar(x.l); arreglar(x.r); actualizar(x)
    import sys; sys.setrecursionlimit(10**6)
    arreglar(t)
    return [nodos[k] for k in range(1, n + 1)]

random.seed(13)
print()
for n in [1000, 10000]:
    nodos = abb_aleatorio(n)
    total = sum(splay(nodos[k]) for k in range(n))
    print(f"árbol inicial aleatorio, n={n}: {total / n:.2f} rotaciones por acceso")
