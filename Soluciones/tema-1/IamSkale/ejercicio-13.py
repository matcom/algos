"""Ejercicio 13 ★★ — Splay tree: acceso secuencial sobre un camino (C4)

Código de validación de ejercicio-13.md.
Ejecutar con: python ejercicio-13.py
"""


# -------------------- Parte 1 --------------------

import math, random

class Nodo:
    __slots__ = ("clave", "izq", "der", "padre")
    def __init__(self, clave):
        self.clave, self.izq, self.der, self.padre = clave, None, None, None

def rotar(x):
    p, g = x.padre, x.padre.padre
    if p.izq is x:
        p.izq, x.der = x.der, p
        if p.izq:
            p.izq.padre = p
    else:
        p.der, x.izq = x.izq, p
        if p.der:
            p.der.padre = p
    p.padre, x.padre = x, g
    if g:
        if g.izq is p:
            g.izq = x
        else:
            g.der = x

def splay(x):
    rotaciones = 0
    while x.padre:
        p, g = x.padre, x.padre.padre
        if g is None:                                  # zig
            rotar(x); rotaciones += 1
        elif (g.izq is p) == (p.izq is x):             # zig-zig: primero el padre
            rotar(p); rotar(x); rotaciones += 2
        else:                                          # zig-zag
            rotar(x); rotar(x); rotaciones += 2
    return rotaciones

def subir_a_la_raiz(x):
    rotaciones = 0
    while x.padre:
        rotar(x); rotaciones += 1
    return rotaciones

def buscar(raiz, clave):
    x = raiz
    while x.clave != clave:
        x = x.izq if clave < x.clave else x.der
    return x

def camino(n):
    nodos = [Nodo(k) for k in range(1, n + 1)]
    for k in range(1, n):
        nodos[k].izq, nodos[k - 1].padre = nodos[k - 1], nodos[k]
    return nodos[-1]

def tamanos(raiz):
    orden, pila = [], [raiz]
    while pila:
        x = pila.pop()
        orden.append(x)
        pila.extend(h for h in (x.izq, x.der) if h)
    s = {}
    for x in reversed(orden):
        s[x] = 1 + (s[x.izq] if x.izq else 0) + (s[x.der] if x.der else 0)
    return s

def potencial(raiz):
    return sum(math.log2(v) for v in tamanos(raiz).values())

def es_camino_izquierdo(raiz, n):
    x, k = raiz, n
    while x:
        if x.clave != k or x.der is not None:
            return False
        x, k = x.izq, k - 1
    return k == 0

# -------------------- Parte 2 --------------------

print(f"{'n':>5} {'real':>6} {'real/n':>7} {'lema exacto':>12} {'cota C4 §5':>11} "
      f"{'cota/real':>10} {'Phi_n = Phi_0':>14}")
for n in [100, 200, 400, 800, 1600]:
    raiz = camino(n)
    phi0 = potencial(raiz)
    assert abs(phi0 - math.lgamma(n + 1) / math.log(2)) < 1e-6        # Phi_0 = log2 n!
    real, lema = 0, 0.0
    for k in range(1, n + 1):
        x = buscar(raiz, k)
        antes, r_x = potencial(raiz), math.log2(tamanos(raiz)[x])
        c = max(splay(x), 1)
        raiz = x
        amortizado = c + potencial(raiz) - antes
        cota_acceso = 3 * (math.log2(n) - r_x) + 1
        assert amortizado <= cota_acceso + 1e-9                         # el lema de acceso
        real += c
        lema += cota_acceso
    phin = potencial(raiz)
    cota = n * (3 * math.log2(n) + 1) + phi0
    print(f"{n:>5} {real:>6} {real / n:>7.2f} {lema + phi0 - phin:>12.0f} {cota:>11.0f} "
          f"{cota / real:>10.1f} {str(es_camino_izquierdo(raiz, n) and abs(phin - phi0) < 1e-6):>14}")

# -------------------- Parte 3 --------------------

def costo_por_acceso(reorganizar, n, rondas=3):
    raiz, total = camino(n), 0
    for _ in range(rondas):
        for clave in range(1, n + 1):
            x = buscar(raiz, clave)
            total += max(reorganizar(x), 1)
            raiz = x
    return total / (rondas * n)

print(f"{'n':>6} {'splay':>8} {'subir a la raíz':>16} {'3 log2 n + 1':>13}")
for n in [100, 200, 400, 800]:
    print(f"{n:>6} {costo_por_acceso(splay, n):>8.1f} {costo_por_acceso(subir_a_la_raiz, n):>16.1f} "
          f"{3 * math.log2(n) + 1:>13.1f}")

# -------------------- Parte 4 --------------------

random.seed(13)
print(f"{'n':>6} {'rotaciones por acceso (al azar)':>32} {'log2 n':>7}")
for n in [100, 400, 1600, 6400]:
    raiz = camino(n)
    for k in range(1, n + 1):                      # una ronda para salir del camino
        x = buscar(raiz, k); splay(x); raiz = x
    total = 0
    for _ in range(5 * n):
        x = buscar(raiz, random.randint(1, n))
        total += max(splay(x), 1)
        raiz = x
    print(f"{n:>6} {total / (5 * n):>32.2f} {math.log2(n):>7.2f}")
