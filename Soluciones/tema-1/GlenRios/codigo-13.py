"""
Problema 13: Splay tree desde un camino.
Versión corregida: sin recursión profunda.
"""
import os
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RUTA = os.path.join("Soluciones", "tema-1", "GlenRios")
os.makedirs(RUTA, exist_ok=True)


class Nodo:
    def __init__(self, clave):
        self.clave = clave
        self.izq = None
        self.der = None
        self.padre = None
        self.tam = 1


def actualizar_tam(x):
    if x is None:
        return
    x.tam = 1
    if x.izq:
        x.tam += x.izq.tam
    if x.der:
        x.tam += x.der.tam


def rotar(x):
    p = x.padre
    g = p.padre if p else None
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
    actualizar_tam(p)
    actualizar_tam(x)


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
    while x and x.clave != clave:
        if clave < x.clave:
            x = x.izq
        else:
            x = x.der
    return x


def camino(n):
    """Construye el camino 1 <- 2 <- ... <- n y calcula tamaños iterativamente."""
    nodos = [Nodo(k) for k in range(1, n + 1)]
    for k in range(1, n):
        nodos[k].izq = nodos[k - 1]
        nodos[k - 1].padre = nodos[k]
    # Tamaños: nodos[0].tam = 1, nodos[k].tam = 1 + nodos[k-1].tam
    nodos[0].tam = 1
    for k in range(1, n):
        nodos[k].tam = 1 + nodos[k - 1].tam
    return nodos[-1]


def potencial(raiz):
    """Potencial iterativo (recorrido con pila)."""
    if raiz is None:
        return 0.0
    total = 0.0
    pila = [raiz]
    while pila:
        x = pila.pop()
        if x.tam > 0:
            total += math.log2(x.tam)
        if x.izq:
            pila.append(x.izq)
        if x.der:
            pila.append(x.der)
    return total


def experimento_total_y_acceso():
    ns = [50, 100, 200, 400, 800, 1600]
    total_splay, total_subir = [], []
    por_acceso_splay, por_acceso_subir = [], []

    print(f"{'n':>6} {'splay total':>12} {'subir total':>12} "
          f"{'splay/acceso':>14} {'subir/acceso':>14}")
    for n in ns:
        raiz = camino(n)
        total = 0
        for clave in range(1, n + 1):
            x = buscar(raiz, clave)
            total += max(splay(x), 1)
            raiz = x
        total_splay.append(total)
        por_acceso_splay.append(total / n)

        raiz = camino(n)
        total = 0
        for clave in range(1, n + 1):
            x = buscar(raiz, clave)
            total += max(subir_a_la_raiz(x), 1)
            raiz = x
        total_subir.append(total)
        por_acceso_subir.append(total / n)

        print(f"{n:>6} {total_splay[-1]:>12} {total_subir[-1]:>12} "
              f"{por_acceso_splay[-1]:>14.1f} {por_acceso_subir[-1]:>14.1f}")

    # Figura 1: costo total vs n
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(ns, total_splay, "o-", label="splay", color="tab:blue")
    ax.plot(ns, total_subir, "s-", label="subir a la raiz", color="tab:red")
    ax.plot(ns, [n * math.log2(n) for n in ns], "--", label="n log2 n", color="gray")
    ax.plot(ns, ns, ":", label="n", color="black")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("n"); ax.set_ylabel("rotaciones totales")
    ax.set_title("Costo total de acceder a 1, ..., n desde un camino")
    ax.legend(); ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(RUTA, "fig_p13_total.png"), dpi=150)
    plt.close(fig)

    # Figura 2: costo por acceso vs n
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(ns, por_acceso_splay, "o-", label="splay", color="tab:blue")
    ax.plot(ns, por_acceso_subir, "s-", label="subir a la raiz", color="tab:red")
    ax.plot(ns, [math.log2(n) for n in ns], "--", label="log2 n", color="gray")
    ax.set_xscale("log")
    ax.set_xlabel("n"); ax.set_ylabel("rotaciones por acceso")
    ax.set_title("Costo por acceso (promedio sobre 1, ..., n)")
    ax.legend(); ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(RUTA, "fig_p13_acceso.png"), dpi=150)
    plt.close(fig)

    print("\n  guardadas fig_p13_total.png y fig_p13_acceso.png")


def experimento_potencial():
    n = 30
    raiz = camino(n)
    potenciales = [potencial(raiz)]
    for clave in range(1, n + 1):
        x = buscar(raiz, clave)
        splay(x)
        raiz = x
        potenciales.append(potencial(raiz))

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(range(len(potenciales)), potenciales, "o-", color="tab:purple")
    ax.set_xlabel("accesos completados")
    ax.set_ylabel("Phi (suma de rangos)")
    ax.set_title(f"Evolucion del potencial durante los accesos (n={n})")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(RUTA, "fig_p13_potencial.png"), dpi=150)
    plt.close(fig)
    print("  guardada fig_p13_potencial.png")


if __name__ == "__main__":
    print("=" * 60)
    print("Costo total y por acceso")
    print("=" * 60)
    experimento_total_y_acceso()

    print("\n" + "=" * 60)
    print("Evolucion del potencial")
    print("=" * 60)
    experimento_potencial()

    print("\nFiguras generadas en Soluciones/tema-1/GlenRios/")