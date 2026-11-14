"""Ejercicio 13. Splay tree sobre un camino: accesos 1..n en orden."""
import math
import sys

sys.setrecursionlimit(100000)


class Nodo:
    def __init__(self, k):
        self.k, self.izq, self.der, self.padre = k, None, None, None


def rotar(x):
    p, g = x.padre, x.padre.padre
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
    p.padre, x.padre = x, g
    if g:
        if g.izq is p:
            g.izq = x
        else:
            g.der = x


def splay(x):
    rot = 0
    while x.padre:
        p, g = x.padre, x.padre.padre
        if g is None:
            rotar(x); rot += 1
        elif (g.izq is p) == (p.izq is x):
            rotar(p); rotar(x); rot += 2
        else:
            rotar(x); rotar(x); rot += 2
    return rot


def subir_a_la_raiz(x):
    rot = 0
    while x.padre:
        rotar(x); rot += 1
    return rot


def camino_izquierdo(n):
    """Raíz n; cada nodo tiene como hijo izquierdo al anterior (1 queda al fondo)."""
    nodos = {k: Nodo(k) for k in range(1, n + 1)}
    for k in range(n, 1, -1):
        nodos[k].izq = nodos[k - 1]
        nodos[k - 1].padre = nodos[k]
    return nodos, nodos[n]


def camino_derecho(n):
    nodos = {k: Nodo(k) for k in range(1, n + 1)}
    for k in range(1, n):
        nodos[k].der = nodos[k + 1]
        nodos[k + 1].padre = nodos[k]
    return nodos, nodos[1]


def tamano(x):
    return 0 if x is None else 1 + tamano(x.izq) + tamano(x.der)


def potencial(x):
    if x is None:
        return 0.0
    return math.log2(tamano(x)) + potencial(x.izq) + potencial(x.der)


def mostrar(x):
    if x is None:
        return "."
    if x.izq is None and x.der is None:
        return str(x.k)
    return f"{x.k}({mostrar(x.izq)},{mostrar(x.der)})"


def accesos_en_orden(n, reorganizar, forma="izquierdo", detalle=False):
    nodos, raiz = (camino_izquierdo if forma == "izquierdo" else camino_derecho)(n)
    total, filas = 0, []
    phi0 = potencial(raiz)
    for k in range(1, n + 1):
        x = nodos[k]
        prof = 0
        y = x
        while y.padre:
            y, prof = y.padre, prof + 1
        s = tamano(x)
        antes = potencial(raiz)
        rot = reorganizar(x)
        raiz = x
        total += rot
        if detalle:
            filas.append((k, prof, rot, mostrar(raiz), potencial(raiz), s, antes))
    return total, phi0, filas


if __name__ == "__main__":
    print("n = 4, splay sobre el camino 4(3(2(1))):")
    _, phi0, filas = accesos_en_orden(4, splay, detalle=True)
    print(f"  inicio: potencial = {phi0:.2f}")
    for k, prof, rot, arbol, phi, s, antes in filas:
        amort = rot + phi - antes
        cota = 3 * (math.log2(4) - math.log2(s)) + 1
        print(f"  acceso {k}: prof {prof}, rot {rot}, árbol {arbol:<22} Φ = {phi:.2f}, "
              f"amortizado = {amort:.2f}, cota del lema = {cota:.2f}")
        assert amort <= cota + 1e-9

    print("\nn = 4, subir a la raíz:")
    _, _, filas = accesos_en_orden(4, subir_a_la_raiz, detalle=True)
    for k, prof, rot, arbol, phi, s, antes in filas:
        print(f"  acceso {k}: prof {prof}, rot {rot}, árbol {arbol}")

    print("\nCosto total (rotaciones) al acceder a 1..n en orden, camino con 1 al fondo")
    print(f"{'n':>6} {'splay':>8} {'splay/n':>8} {'subir a la raíz':>16} {'(n-1)(n+2)/2':>13} "
          f"{'cota 4n log2 n + n':>19}")
    for n in [4, 8, 16, 64, 256, 1024]:
        s, p0, _ = accesos_en_orden(n, splay)
        r, _, _ = accesos_en_orden(n, subir_a_la_raiz)
        assert r == (n - 1) * (n + 2) // 2
        cota = 4 * n * math.log2(n) + n
        assert s <= cota
        print(f"{n:>6} {s:>8} {s / n:>8.2f} {r:>16} {(n - 1) * (n + 2) // 2:>13} {cota:>19.0f}")

    print("\nOtra orientación (raíz 1, hijo derecho):")
    for n in [4, 64, 1024]:
        s, _, _ = accesos_en_orden(n, splay, forma="derecho")
        print(f"  n = {n:>5}: splay total = {s} (= n - 1)")
        assert s == n - 1

    print("\nInvariante de 'subir a la raíz' con n = 8 (árbol antes del acceso k):")
    nodos, raiz = camino_izquierdo(8)
    for k in range(1, 9):
        x = nodos[k]
        if k >= 3:
            print(f"  antes del acceso {k}: {mostrar(raiz)}")
        subir_a_la_raiz(x)
        raiz = x

    print("\nSuma de las cotas del lema con los tamaños reales s_k: sigue creciendo como n log n")
    print(f"{'n':>6} {'promedio de log2(n/s_k)':>25}")
    for n in [64, 256, 1024, 4096]:
        nodos, raiz = camino_izquierdo(n)
        tot = 0.0
        for k in range(1, n + 1):
            x = nodos[k]
            tot += math.log2(n / tamano(x))
            splay(x)
        print(f"{n:>6} {tot / n:>25.2f}")
