"""
Tema 1, ejercicio 14: recorrer el ciclo completo sobre un problema.

Problema: un arbol binario de busqueda con las claves 1..n que empieza como
un camino. Llegan m accesos. Cuanto cuesta, en el peor caso, atenderlos?

  algoritmo       : splay tree (subir la clave accedida a la raiz de dos en dos)
  correctitud     : el arbol sigue siendo de busqueda y la clave queda en la raiz
  cota superior   : lema de acceso, O((m + n) log n)
  cota minima     : un adversario que pide siempre la clave mas profunda, m log n
  conclusion      : coinciden, Theta(m log n) cuando m >= n

Modelo de costo: buscar una clave visita (profundidad + 1) nodos; cada rotacion
cuesta 1. La cota minima cuenta solo los nodos visitados al buscar.
Uso:  python ejercicio14_ciclo_splay.py
"""
import math
import random
from pathlib import Path


# ----------------------------------------------------------------------------
# El arbol y las dos heuristicas
# ----------------------------------------------------------------------------
class Nodo:
    __slots__ = ("clave", "izq", "der", "padre")

    def __init__(self, clave):
        self.clave = clave
        self.izq = self.der = self.padre = None


def rotar(x):
    """Sube x un nivel rotando la arista con su padre."""
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


def profundidad(x):
    d = 0
    while x.padre:
        x, d = x.padre, d + 1
    return d


def splay(x, vigilado=False):
    """Sube x a la raiz de dos niveles en dos. Devuelve las rotaciones."""
    rotaciones = 0
    while x.padre:
        d0 = profundidad(x) if vigilado else 0
        p = x.padre
        g = p.padre
        if g is None:                               # zig
            rotar(x)
            rotaciones += 1
        elif (g.izq is p) == (p.izq is x):          # zig-zig: primero el padre
            rotar(p)
            rotar(x)
            rotaciones += 2
        else:                                       # zig-zag
            rotar(x)
            rotar(x)
            rotaciones += 2
        if vigilado:                                # POTENCIAL: la profundidad de x baja
            assert profundidad(x) < d0
    return rotaciones


def subir_a_la_raiz(x):
    """Heuristica ingenua: una rotacion simple por nivel."""
    rotaciones = 0
    while x.padre:
        rotar(x)
        rotaciones += 1
    return rotaciones


def camino(n):
    """n en la raiz y cada clave es hija izquierda de la siguiente."""
    nodos = [Nodo(k) for k in range(1, n + 1)]
    for k in range(1, n):
        nodos[k].izq = nodos[k - 1]
        nodos[k - 1].padre = nodos[k]
    return nodos[-1]


def arbol_aleatorio(n, rng):
    claves = list(range(1, n + 1))
    rng.shuffle(claves)
    raiz = Nodo(claves[0])
    for c in claves[1:]:
        v = raiz
        while True:
            lado = "izq" if c < v.clave else "der"
            hijo = getattr(v, lado)
            if hijo is None:
                nuevo = Nodo(c)
                nuevo.padre = v
                setattr(v, lado, nuevo)
                break
            v = hijo
    return raiz


def buscar(raiz, clave):
    """Devuelve (nodo, nodos visitados)."""
    x, visitados = raiz, 1
    while x.clave != clave:
        x = x.izq if clave < x.clave else x.der
        visitados += 1
    return x, visitados


def mas_profundo(raiz):
    """La clave mas profunda del arbol: lo que pide el adversario."""
    mejor, mejor_d, pila = raiz, 0, [(raiz, 0)]
    while pila:
        v, d = pila.pop()
        if d > mejor_d:
            mejor, mejor_d = v, d
        if v.izq:
            pila.append((v.izq, d + 1))
        if v.der:
            pila.append((v.der, d + 1))
    return mejor, mejor_d


def inorden(raiz):
    res, pila, v = [], [], raiz
    while pila or v:
        while v:
            pila.append(v)
            v = v.izq
        v = pila.pop()
        res.append(v.clave)
        v = v.der
    return res


# ----------------------------------------------------------------------------
# Potencial: suma de los rangos, rango(v) = log2 (tamano del subarbol de v)
# ----------------------------------------------------------------------------
def tamanos(raiz):
    orden, pila = [], [raiz]
    while pila:
        v = pila.pop()
        orden.append(v)
        if v.izq:
            pila.append(v.izq)
        if v.der:
            pila.append(v.der)
    tam = {}
    for v in reversed(orden):
        tam[v] = (1 + (tam[v.izq] if v.izq else 0)
                  + (tam[v.der] if v.der else 0))
    return tam


def potencial(tam):
    return sum(math.log2(t) for t in tam.values())


# ----------------------------------------------------------------------------
# Cotas
# ----------------------------------------------------------------------------
def cota_inferior(n, m):
    """Busqueda: el primer acceso baja hasta el fondo del camino (n nodos) y los
    demas, a la clave mas profunda de cualquier arbol con n nodos."""
    return n + (m - 1) * math.ceil(math.log2(n + 1))


def cota_superior(n, m):
    """Cota para visitas mas rotaciones usando el lema de acceso."""
    rotaciones = m * (3 * math.log2(n) + 1) + math.log2(math.factorial(n))
    return 2 * rotaciones + m


# ----------------------------------------------------------------------------
# El juego del adversario
# ----------------------------------------------------------------------------
def jugar(n, m, reorganizar):
    """El adversario ve el arbol y pide siempre la clave mas profunda.
    Devuelve (nodos visitados, rotaciones, visitados por acceso)."""
    raiz = camino(n)
    busqueda = rotaciones = 0
    historial = []
    for _ in range(m):
        x, d = mas_profundo(raiz)
        visitados = d + 1
        r = reorganizar(x)
        raiz = x
        busqueda += visitados
        rotaciones += r
        historial.append(visitados)
    return busqueda, rotaciones, historial


def lema_en_el_juego(n, m):
    """Lo mismo, pero vigilando el lema de acceso en cada acceso y la suma
    telescopica."""
    raiz = camino(n)
    tam = tamanos(raiz)
    phi0 = phi = potencial(tam)
    rotaciones_reales = suma_amort = 0.0
    costo_real = 0.0
    for _ in range(m):
        x, _ = mas_profundo(raiz)
        r = math.log2(tam[x])                       # rango de x antes del splay
        rotaciones = splay(x)
        raiz = x
        tam = tamanos(raiz)
        phi_nuevo = potencial(tam)
        amortizado = rotaciones + phi_nuevo - phi
        assert amortizado <= 3 * (math.log2(n) - r) + 1 + 1e-9      # EL LEMA
        rotaciones_reales += rotaciones
        costo_real += 2 * rotaciones + 1
        suma_amort += amortizado
        phi = phi_nuevo
    assert abs(rotaciones_reales - (suma_amort + phi0 - phi)) < 1e-6
    assert costo_real <= cota_superior(n, m) + 1e-6
    return rotaciones_reales


def secuencial(n, reorganizar):
    """La secuencia del ejercicio anterior: claves 1, 2, ..., n en orden."""
    raiz, total = camino(n), 0
    for clave in range(1, n + 1):
        x, _ = buscar(raiz, clave)
        total += max(reorganizar(x), 1)
        raiz = x
    return total


# ----------------------------------------------------------------------------
# Animacion (opcional, necesita Pillow)
# ----------------------------------------------------------------------------
def _posiciones(raiz):
    pos, pila, v, k = {}, [], raiz, 0
    prof = {raiz: 0}
    while pila or v:
        while v:
            pila.append(v)
            if v.izq:
                prof[v.izq] = prof[v] + 1
            v = v.izq
        v = pila.pop()
        pos[v] = (k, prof[v])
        k += 1
        if v.der:
            prof[v.der] = prof[v] + 1
        v = v.der
    return pos


def generar_gif(n, pasos, ruta):
    from PIL import Image, ImageDraw, ImageFont

    try:
        fuente = ImageFont.load_default(size=14)
        chica = ImageFont.load_default(size=12)
    except TypeError:
        fuente = chica = ImageFont.load_default()
    DX, DY, X0, Y0, R = 38, 30, 30, 100, 12
    ANCHO, ALTO = X0 * 2 + DX * n, Y0 + DY * (n - 1) + 40

    def cuadro(raiz, pedido, l1, l2, l3):
        im = Image.new("RGB", (ANCHO, ALTO), "white")
        d = ImageDraw.Draw(im)
        pos = _posiciones(raiz)
        centro = {v: (X0 + k * DX, Y0 + p * DY) for v, (k, p) in pos.items()}
        for v, (cx, cy) in centro.items():
            for h in (v.izq, v.der):
                if h:
                    d.line([cx, cy, *centro[h]], fill="#555555", width=2)
        for v, (cx, cy) in centro.items():
            fondo = pedido and v is pedido[0] and pedido[1] or "white"
            d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=fondo,
                      outline="#222222", width=2)
            d.text((cx - 4 * len(str(v.clave)), cy - 7), str(v.clave),
                   fill="black", font=chica)
        d.text((15, 10), l1, fill="black", font=fuente)
        d.text((15, 36), l2, fill="#b00020", font=chica)
        d.text((15, 58), l3, fill="#444444", font=chica)
        return im

    raiz = camino(n)
    frames = [cuadro(raiz, None, f"camino de {n} nodos: el adversario pide la clave mas profunda",
                     "estado inicial", "")]
    total = 0
    for t in range(1, pasos + 1):
        x, d = mas_profundo(raiz)
        frames.append(cuadro(raiz, (x, "#f4a6a6"), f"acceso {t}: el adversario pide la clave {x.clave}",
                             f"es la mas profunda: hay que visitar {d + 1} nodos",
                             f"nodos visitados hasta ahora = {total}"))
        total += d + 1
        splay(x)
        raiz = x
        frames.append(cuadro(raiz, (x, "#ffe27a"), f"despues del splay de {x.clave}",
                             f"se visitaron {d + 1} nodos en este acceso",
                             f"nodos visitados en total = {total}"))
    frames += [frames[-1]]
    frames[0].save(ruta, save_all=True, append_images=frames[1:],
                   duration=1100, loop=0)


def generar_grafica(ruta, n=255, m=2000):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return False
    _, _, hist = jugar(n, m, splay)
    acum, suma = [], 0
    for i, v in enumerate(hist, 1):
        suma += v
        acum.append(suma / i)
    xs = list(range(1, m + 1))
    inf = [math.ceil(math.log2(n + 1))] * m
    sup = [(i * (3 * math.log2(n) + 1) + math.log2(math.factorial(n)) + i) / i
           for i in xs]
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    ax.loglog(xs, sup, "--", color="#444444", label="cota superior (lema de acceso)")
    ax.loglog(xs, acum, color="#1f6feb", label="splay contra el adversario (promedio)")
    ax.loglog(xs, inf, "-", color="#c2571a", label="cota mínima: ⌈log₂(n+1)⌉")
    ax.set_xlabel("número de accesos")
    ax.set_ylabel("nodos visitados por acceso")
    ax.set_title(f"n = {n}: el promedio queda entre las dos cotas")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(ruta, dpi=130)
    return True


# ----------------------------------------------------------------------------
# Experimentos
# ----------------------------------------------------------------------------
def comprobar_correctitud():
    rng = random.Random(14)
    accesos = 0
    for _ in range(300):
        n = rng.randint(1, 40)
        raiz = arbol_aleatorio(n, rng)
        for _ in range(60):
            clave = rng.randint(1, n)
            x, _ = buscar(raiz, clave)
            d = profundidad(x)
            rot = splay(x, vigilado=True)               # asserts del potencial
            raiz = x
            assert raiz.padre is None and raiz.clave == clave   # la clave queda en la raiz
            assert inorden(raiz) == list(range(1, n + 1))       # sigue siendo de busqueda
            assert rot == d                                     # una rotacion por nivel
            accesos += 1
    print(f"splay vigilado: {accesos} accesos sobre 300 arboles aleatorios; la clave queda "
          f"en la raiz, el orden en-orden no cambia y la profundidad de x baja en cada paso")


def tabla_adversario():
    print(f"{'n':>5} {'m':>6} {'visitados':>10} {'cota inferior':>14} {'visit/inf':>10} "
          f"{'total':>9} {'cota superior':>14} {'total/sup':>10} {'visit/acceso':>13}")
    for n in (63, 255, 511):
        m = 4 * n
        busqueda, rot, _ = jugar(n, m, splay)
        total = busqueda + rot
        inf, sup = cota_inferior(n, m), cota_superior(n, m)
        assert busqueda >= inf and total <= sup
        print(f"{n:>5} {m:>6} {busqueda:>10} {inf:>14.0f} {busqueda / inf:>10.2f} "
              f"{total:>9} {sup:>14.0f} {total / sup:>10.2f} {busqueda / m:>13.2f}")
    print("subir a la raiz, contra el mismo adversario (visitados por acceso):")
    for n in (63, 255):
        busqueda, _, _ = jugar(n, 4 * n, subir_a_la_raiz)
        print(f"  n = {n:>4}: {busqueda / (4 * n):>7.1f}   (log2(n+1) = {math.log2(n + 1):.1f}, n = {n})")


def comparar_secuencial():
    print(f"{'n':>6} {'real (rotaciones)':>18} {'real / n':>9} {'cota del lema':>14} {'cota / real':>12}")
    for n in (100, 400, 1600, 6400):
        real = secuencial(n, splay)
        cota = n * (3 * math.log2(n) + 1) + math.log2(math.factorial(n))
        print(f"{n:>6} {real:>18} {real / n:>9.2f} {cota:>14.0f} {cota / real:>12.1f}")


def main():
    comprobar_correctitud()
    print()
    c = lema_en_el_juego(63, 400)
    print(f"lema de acceso vigilado contra el adversario (n = 63, m = 400): cumplido en cada "
          f"acceso; rotaciones reales = {c:.0f}")
    print()
    tabla_adversario()
    print()
    comparar_secuencial()
    print()
    try:
        base = Path(__file__).parent
        generar_gif(15, 8, base / "adversario_splay.gif")
        print("animacion guardada en adversario_splay.gif")
        if generar_grafica(base / "cotas_ciclo.png"):
            print("grafica guardada en cotas_ciclo.png")
        else:
            print("(sin matplotlib: se omite la grafica)")
    except ImportError:
        print("(sin Pillow: se omite la animacion)")


if __name__ == "__main__":
    main()
