"""Ejercicio 13: splay tree que empieza como camino, accediendo a 1, 2, ..., n en orden.

Corre: python ejercicio-13.py
El árbol, rotar, splay, buscar y camino son los de la sección 4 de la conferencia 4.
"""
import math, random

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
            rotar(x); rotaciones += 1
        elif (g.izq is p) == (p.izq is x):
            rotar(p); rotar(x); rotaciones += 2
        else:
            rotar(x); rotar(x); rotaciones += 2
    return rotaciones

def buscar(raiz, clave):
    x = raiz
    while x.clave != clave:
        x = x.izq if clave < x.clave else x.der
    return x

def camino(n):
    """n en la raíz, cada clave hija izquierda de la siguiente (la clave 1 está a profundidad n-1)."""
    nodos = [Nodo(k) for k in range(1, n + 1)]
    for k in range(1, n):
        nodos[k].izq, nodos[k - 1].padre = nodos[k - 1], nodos[k]
    return nodos[-1]

# --- utilidades iterativas (el camino inicial es demasiado profundo para recursión) ---

def tamanos(raiz):
    """dict nodo -> tamaño de su subárbol, en O(n)."""
    orden, pila = [], [raiz]
    while pila:
        x = pila.pop()
        orden.append(x)
        pila += [h for h in (x.izq, x.der) if h]
    s = {}
    for x in reversed(orden):
        s[x] = 1 + s.get(x.izq, 0) + s.get(x.der, 0)
    return s

def potencial(raiz):
    return sum(math.log2(v) for v in tamanos(raiz).values())

def tamano_subarbol(x):
    t, pila = 0, [x]
    while pila:
        y = pila.pop(); t += 1
        pila += [h for h in (y.izq, y.der) if h]
    return t

def profundidad(x):
    d = 0
    while x.padre:
        x, d = x.padre, d + 1
    return d


def experimento(n, claves, vigilar=False):
    """Accede a `claves` sobre un camino de n nodos. Devuelve el costo real total (rotaciones,
    con mínimo 1 por acceso, como en la conferencia) y la cota del lema de acceso término a término."""
    raiz = camino(n)
    phi0 = potencial(raiz)
    real = cota_lema = 0.0
    log_n = math.log2(n)
    for clave in claves:
        x = buscar(raiz, clave)
        r_x = math.log2(tamano_subarbol(x))
        antes = potencial(raiz) if vigilar else None
        c = max(splay(x), 1)
        raiz = x
        real += c
        cota_lema += 3 * (log_n - r_x) + 1
        if vigilar:   # el lema, acceso por acceso: c + ΔΦ <= 3 (log n - r(x)) + 1
            assert c + potencial(raiz) - antes <= 3 * (log_n - r_x) + 1 + 1e-9
    phi_final = potencial(raiz)
    return real, cota_lema, phi0, phi_final, raiz


if __name__ == "__main__":
    # 0. El lema vigilado en cada acceso (n chico, potencial recalculado entero)
    for n in [1, 2, 3, 10, 50, 200]:
        experimento(n, range(1, n + 1), vigilar=True)
    print("lema de acceso vigilado en cada acceso para n = 1, 2, 3, 10, 50, 200: se cumple siempre")

    # 0b. Hechos usados en el texto
    raiz = camino(64)
    assert splay(buscar(raiz, 1)) == 63                  # el primer acceso cuesta n - 1
    assert math.isclose(potencial(camino(64)), math.log2(math.factorial(64)))

    # 1. Una ronda 1..n: la cota del lema contra el costo real
    print(f"\n{'n':>6} {'real':>8} {'real/n':>7} {'cota lema + Φ0 - Φn':>20} {'cota gruesa':>12} {'cota/real':>10}")
    filas = []
    for n in [100, 200, 400, 800, 1600, 3200, 6400, 12800]:
        real, lema, phi0, phin, _ = experimento(n, range(1, n + 1))
        exacta = lema + phi0 - phin                      # Σ c_i = Σ ĉ_i - (Φ_n - Φ_0) <= ...
        gruesa = n * (3 * math.log2(n) + 1) + math.log2(math.factorial(n))
        assert real <= exacta + 1e-6 <= gruesa + 1e-6
        filas.append((n, real, exacta, gruesa))
        print(f"{n:>6} {real:>8.0f} {real / n:>7.2f} {exacta:>20.0f} {gruesa:>12.0f} {exacta / real:>10.1f}")
    por_acceso = [f[1] / f[0] for f in filas]
    assert por_acceso[-1] < 4.5                             # lineal: menos de 4.5 rotaciones por acceso
    saltos = [b - a for a, b in zip(por_acceso, por_acceso[1:])]
    assert saltos[-1] < saltos[0] / 2                       # y cada vez crece menos
    assert filas[-1][2] / filas[-1][1] > filas[0][2] / filas[0][1]   # la brecha crece con n

    # 2. Comparación con la sección 6 de la conferencia 4: tres rondas, costo por acceso; y otros órdenes de acceso
    def bit_reverso(n):
        b = max(1, (n - 1).bit_length())
        return sorted(range(1, n + 1), key=lambda k: int(format(k - 1, f"0{b}b")[::-1], 2))
    rng = random.Random(2026)
    print(f"\n{'n':>6} {'en orden ×3':>17} {'al azar':>8} {'bit-reverso':>12} {'log2 n':>7}   (rotaciones por acceso)")
    por_orden = {"en orden": [], "al azar": [], "bit-reverso": []}
    for n in [128, 256, 512, 1024, 2048]:
        r3 = experimento(n, list(range(1, n + 1)) * 3)[0] / (3 * n)
        # para los otros órdenes, primero una ronda en orden para "desarmar" el camino y medir solo lo siguiente
        def despues_de_una_ronda(claves):
            real_total = experimento(n, list(range(1, n + 1)) + claves)[0]
            real_ronda = experimento(n, list(range(1, n + 1)))[0]
            return (real_total - real_ronda) / len(claves)
        az = despues_de_una_ronda([rng.randint(1, n) for _ in range(n)])
        br = despues_de_una_ronda(bit_reverso(n) * 2)
        por_orden["en orden"].append((n, r3)); por_orden["al azar"].append((n, az)); por_orden["bit-reverso"].append((n, br))
        print(f"{n:>6} {r3:>17.2f} {az:>8.2f} {br:>12.2f} {math.log2(n):>7.1f}")

    # 3. Profundidad tras cada acceso: cómo se "desarma" el camino
    n = 32
    raiz = camino(n)
    prof = []
    for k in range(1, n + 1):
        x = buscar(raiz, k)
        prof.append(profundidad(x))
        splay(x); raiz = x
    print(f"\nn = {n}: profundidad de la clave k justo antes de accederla:")
    print(" ", prof)

    # 4. Figura
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("(sin matplotlib)")
    else:
        fig, axs = plt.subplots(1, 2, figsize=(11, 4))
        ns = [f[0] for f in filas]
        ax = axs[0]
        ax.plot(ns, [f[1] / f[0] for f in filas], "o-", label="real (una ronda 1..n)")
        ax.plot(ns, [f[2] / f[0] for f in filas], "s--", label="cota del lema, Σ ĉᵢ + Φ₀ − Φₙ")
        ax.plot(ns, [f[3] / f[0] for f in filas], "^:", label="cota gruesa n(3 log n + 1) + log n!")
        ax.set_xscale("log", base=2); ax.set_xlabel("n"); ax.set_ylabel("rotaciones por acceso")
        ax.set_title("Acceso en orden sobre un camino"); ax.legend(fontsize=8)
        ax = axs[1]
        for nombre, pts in por_orden.items():
            ax.plot([p[0] for p in pts], [p[1] for p in pts], "o-", label=nombre)
        ax.plot([p[0] for p in por_orden["en orden"]], [math.log2(p[0]) for p in por_orden["en orden"]], ":", c="gray", label="log₂ n")
        ax.set_xscale("log", base=2); ax.set_xlabel("n"); ax.set_ylabel("rotaciones por acceso")
        ax.set_title("¿Qué órdenes alcanzan la cota?"); ax.legend(fontsize=8)
        fig.tight_layout()
        fig.savefig("ejercicio-13-splay.png", dpi=150)
        print("\nfigura: ejercicio-13-splay.png")
