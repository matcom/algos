import math
from pathlib import Path
import matplotlib.pyplot as plt


class Nodo:
    def __init__(self, clave):
        self.clave = clave
        self.izq = None
        self.der = None
        self.padre = None


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
    s = {}
    for x in reversed(orden):
        s[x] = 1 + s.get(x.izq, 0) + s.get(x.der, 0)
    return s


def alturas(raiz):
    orden, pila = [], [(raiz, 0)]
    prof = {}
    while pila:
        x, d = pila.pop()
        prof[x.clave] = d
        if x.izq:
            pila.append((x.izq, d + 1))
        if x.der:
            pila.append((x.der, d + 1))
    return prof


def potencial(raiz):
    return sum(math.log2(t) for t in tamanos(raiz).values())


def una_ronda(n, vigilar=False):
    raiz = camino(n)
    total = 0
    costos = []
    potenciales = [potencial(raiz)] if vigilar else []

    for clave in range(1, n + 1):
        x = buscar(raiz, clave)
        if vigilar:
            antes = potenciales[-1]
            r_x = math.log2(tamanos(raiz)[x])
        c = max(splay(x), 1)
        raiz = x
        if vigilar:
            despues = potencial(raiz)
            assert c + despues - antes <= 3 * (math.log2(n) - r_x) + 1 + 1e-9
            potenciales.append(despues)
        total += c
        costos.append(c)

    if vigilar:
        return total, costos, potenciales
    return total, costos[0], max(costos[1:], default=0)


if __name__ == "__main__":
    # 1. Inspeccion estructural tras splay(1) sobre un camino de n = 9 nodos
    r9 = camino(9)
    prof_antes = alturas(r9)
    x1 = buscar(r9, 1)
    rots_1 = splay(x1)
    r9 = x1
    prof_despues = alturas(r9)
    print("=== Efecto estructural del primer acceso splay(1) en camino(9) ===")
    print(f"Profundidades antes de splay(1):   {prof_antes} (altura = {max(prof_antes.values())})")
    print(f"Profundidades despues de splay(1): {prof_despues} (altura = {max(prof_despues.values())}, rotaciones = {rots_1})\n")

    # 2. Verificacion del lema de acceso paso a paso
    for n_prueba in [2, 10, 50, 200]:
        una_ronda(n_prueba, vigilar=True)
    print("Lema de acceso verificado en cada operacion individual para n = 2, 10, 50, 200.\n")

    # 3. Medicion de una ronda completa para n grandes
    print(f"{'n':>7} {'costo medido':>13} {'por acceso':>11} {'primer acceso':>14} "
          f"{'cota del lema':>14} {'cota / medido':>14}")
    for n in [100, 1000, 10_000, 100_000]:
        total, primero, _ = una_ronda(n)
        cota = n * (3 * math.log2(n) + 1) + math.lgamma(n + 1) / math.log(2)
        print(f"{n:>7} {total:>13,} {total / n:>11.2f} {primero:>14,} {cota:>14,.0f} "
              f"{cota / total:>14.1f}")

    # 4. Datos para la grafica (Panel 1: ronda con n = 60; Panel 2: escalamiento n en [50..5000])
    n_detalle = 60
    _, costos_60, pot_60 = una_ronda(n_detalle, vigilar=True)

    ns_escala = [50, 100, 250, 500, 1000, 2000, 3500, 5000]
    medidos_escala = []
    cotas_escala = []
    recta_44n = []
    for n_val in ns_escala:
        tot, _, _ = una_ronda(n_val)
        cota_val = n_val * (3 * math.log2(n_val) + 1) + math.lgamma(n_val + 1) / math.log(2)
        medidos_escala.append(tot)
        cotas_escala.append(cota_val)
        recta_44n.append(4.42 * n_val)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.8, 4.4))

    pasos = list(range(1, n_detalle + 1))
    color_costo = "#1f77b4"
    color_pot = "#d62728"

    ax1.bar(pasos, costos_60, color=color_costo, alpha=0.75, width=0.75, label="Costo real c_i (rotaciones)")
    ax1.set_xlabel("Clave accedida i (en orden 1..60)")
    ax1.set_ylabel("Costo real c_i por acceso", color=color_costo)
    ax1.tick_params(axis="y", labelcolor=color_costo)
    ax1.set_title("Caida del potencial y costo por acceso (n = 60)")
    ax1.grid(True, alpha=0.25)

    ax1_b = ax1.twinx()
    ax1_b.plot(range(0, n_detalle + 1), pot_60, "-", color=color_pot, lw=2.2, label="Potencial Phi_i = sum log2 s(x)")
    ax1_b.set_ylabel("Potencial Phi del arbol", color=color_pot)
    ax1_b.tick_params(axis="y", labelcolor=color_pot)

    # Leyenda combinada en ax1
    lineas1, etiq1 = ax1.get_legend_handles_labels()
    lineas2, etiq2 = ax1_b.get_legend_handles_labels()
    ax1.legend(lineas1 + lineas2, etiq1 + etiq2, loc="upper right", fontsize=8.5)

    ax2.plot(ns_escala, cotas_escala, "s--", color="#d62728", lw=1.8, markersize=5,
             label="Cota del lema: 3n log2(n) + n + log2(n!)")
    ax2.plot(ns_escala, medidos_escala, "o-", color="#2ca02c", lw=2.2, markersize=5,
             label="Costo total medido en la ronda")
    ax2.plot(ns_escala, recta_44n, ":", color="#111111", lw=1.6,
             label="Ajuste lineal (~ 4.42 n)")
    ax2.set_title("Costo total acumulado vs cota del lema (n = 50..5000)")
    ax2.set_xlabel("Numero de nodos (n)")
    ax2.set_ylabel("Operaciones totales en la ronda")
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=8.5)

    plt.tight_layout()
    salida_png = Path(__file__).with_name("ejercicio-13.png")
    plt.savefig(salida_png, dpi=150)
    print(f"\nGrafica guardada en {salida_png.name}")
