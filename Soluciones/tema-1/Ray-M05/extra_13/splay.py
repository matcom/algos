import math
import sys

from comun.tabla import num, tabla_md


class Nodo:
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
    t = {}
    for x in reversed(orden):
        t[x] = 1 + t.get(x.izq, 0) + t.get(x.der, 0)
    return t


def potencial(raiz):
    return sum(math.log2(s) for s in tamanos(raiz).values())


def es_el_camino(raiz, n):
    x, k = raiz, n
    while x:
        if x.clave != k or x.der is not None:
            return False
        x, k = x.izq, k - 1
    return k == 0


def ronda(raiz, n):
    total, lema = 0, 0.0
    for clave in range(1, n + 1):
        x = buscar(raiz, clave)
        r_x = math.log2(tamanos(x)[x]) if n <= 1000 else 0.0
        costo = max(splay(x), 1)
        total += costo
        lema += 3 * (math.log2(n) - r_x) + 1
        raiz = x
    return raiz, total, lema


def _comparacion():
    filas = []
    for n in (100, 200, 400, 800):
        raiz = camino(n)
        phi0 = potencial(raiz)
        costos = []
        for _ in range(3):
            raiz, total, lema = ronda(raiz, n)
            assert es_el_camino(raiz, n) and abs(potencial(raiz) - phi0) < 1e-6
            costos.append(total)
        assert costos[0] == costos[1] == costos[2]
        filas.append([n, f"{costos[0]:,}", num(costos[0] / n, 1), num(lema / n, 1),
                      num(3 * math.log2(n) + 1, 1)])
    print(tabla_md(["n", "costo de una ronda", "por acceso", "lema con los rangos reales, por acceso",
                    "3 log₂ n + 1"], filas, "ddddd"))
    grandes = []
    for n in (10_000, 100_000):
        raiz, total, _ = ronda(camino(n), n)
        assert es_el_camino(raiz, n)
        grandes.append(f"{num(total / n, 2)} con n = {n:,}")
    print(f"\nCon $n$ más grande, una ronda cuesta {' y '.join(grandes)} rotaciones por acceso.")


SECCIONES = {
    "comparacion": _comparacion,
}

if __name__ == "__main__":
    SECCIONES[sys.argv[1]]()
