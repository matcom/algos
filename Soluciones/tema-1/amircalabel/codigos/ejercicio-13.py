import math
import random

class Nodo:
    def __init__(self, clave):
        self.clave = clave
        self.izq = None
        self.der = None
        self.padre = None

def rotar(x):
    p = x.padre
    g = p.padre
    if p.izq is x:
        p.izq = x.der
        if x.der:
            x.der.padre = p
        x.der = p
    else:
        p.der = x.izq
        if x.izq:
            x.izq.padre = p
        x.izq = p
    p.padre = x
    x.padre = g
    if g:
        if g.izq is p:
            g.izq = x
        else:
            g.der = x

def splay(x):
    rotaciones = 0
    while x.padre:
        p = x.padre
        g = p.padre
        if g is None:
            rotar(x)
            rotaciones += 1
        elif (g.izq is p) == (p.izq is x):
            rotar(p)
            rotar(x)
            rotaciones += 2
        else:
            rotar(x)
            rotar(x)
            rotaciones += 2
    return rotaciones

def subir_a_la_raiz(x):
    rotaciones = 0
    while x.padre:
        rotar(x)
        rotaciones += 1
    return rotaciones

def buscar(raiz, clave):
    x = raiz
    while x.clave != clave:
        x = x.izq if clave < x.clave else x.der
    return x

def camino(n):
    nodos = [Nodo(k) for k in range(1, n + 1)]
    for k in range(1, n):
        nodos[k].izq = nodos[k - 1]
        nodos[k - 1].padre = nodos[k]
    return nodos[-1]

def costo_por_acceso(reorganizar, n, rondas=3):
    raiz = camino(n)
    total = 0
    for _ in range(rondas):
        for clave in range(1, n + 1):
            x = buscar(raiz, clave)
            total += max(reorganizar(x), 1)
            raiz = x
    return total / (rondas * n)

def main():
    print(f"{'n':>6} {'splay':>8} {'subir a la raíz':>16} {'log2 n':>8}")
    for n in [100, 200, 400, 800]:
        s = costo_por_acceso(splay, n)
        r = costo_por_acceso(subir_a_la_raiz, n)
        print(f"{n:>6} {s:>8.1f} {r:>16.1f} {math.log2(n):>8.1f}")

if __name__ == "__main__":
    main()
