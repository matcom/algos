"""Ejercicio 13 del Tema 1: splay tree sobre un camino, claves en orden.

Los bloques van en el orden de ejercicio-13.md, y cada uno imprime lo que el .md
muestra debajo de él. Ejecutarlo desde Soluciones/tema-1/alinadelanoval/:

    pip install tesserax        # para la figura
    python codigo/ejercicio-13.py
"""

# == bloque: imports (oculto)
import math
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[3] / "Lectures" / "2026"))   # donde vive figuras.py
sys.setrecursionlimit(10_000)

# == bloque: splay (oculto)
class Nodo:
    def __init__(self, clave):
        self.clave, self.izq, self.der, self.padre = clave, None, None, None

def rotar(x):
    """Sube x un nivel rotando la arista con su padre. Preserva el orden."""
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
            rotar(x)
            rotaciones += 1
        elif (g.izq is p) == (p.izq is x):             # zig-zig: primero el padre
            rotar(p)
            rotar(x)
            rotaciones += 2
        else:                                          # zig-zag
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
    """n en la raíz, cada clave hija izquierda de la siguiente."""
    nodos = [Nodo(k) for k in range(1, n + 1)]
    for k in range(1, n):
        nodos[k].izq, nodos[k - 1].padre = nodos[k - 1], nodos[k]
    return nodos[-1]

# == bloque: lema
def rangos(x, salida):
    # devuelve s(x) y acumula en salida la suma de los rangos del subárbol
    if x is None:
        return 0
    s = 1 + rangos(x.izq, salida) + rangos(x.der, salida)
    salida[0] += math.log2(s)
    return s

def potencial(raiz):
    total = [0.0]
    rangos(raiz, total)
    return total[0]

def cota_total(n, m):
    return m * (3 * math.log2(n) + 1) + math.log2(math.factorial(n))

print(f"{'n':>4} {'rondas':>7} {'costo real':>11} {'cota':>9} {'máx. ĉᵢ':>8} {'3 log₂ n + 1':>13}")
for n in (50, 100, 200):
    for rondas in (1, 3):
        raiz = camino(n)
        assert math.isclose(potencial(raiz), math.log2(math.factorial(n)))   # Φ₀ = log₂ n!
        total, peor = 0, 0.0
        for _ in range(rondas):
            for clave in range(1, n + 1):
                x = buscar(raiz, clave)
                antes = potencial(raiz)
                c = max(splay(x), 1)
                raiz = x
                total += c
                peor = max(peor, c + potencial(raiz) - antes)           # ĉᵢ
        assert peor <= 3 * math.log2(n) + 1 + 1e-9                      # lema de acceso
        assert total <= cota_total(n, rondas * n)                       # costo total
        print(f"{n:>4} {rondas:>7} {total:>11,} {cota_total(n, rondas * n):>9,.0f}"
              f" {peor:>8.1f} {3 * math.log2(n) + 1:>13.1f}")

# == bloque: medido
def costo_por_acceso(n, rondas=3):
    raiz, total = camino(n), 0
    for _ in range(rondas):
        for clave in range(1, n + 1):
            x = buscar(raiz, clave)
            total += max(splay(x), 1)
            raiz = x
    return total / (rondas * n)

medido, cota = [], []
print(f"{'n':>5} {'log₂ n':>7} {'cota por acceso':>16} {'medido':>7}")
for n in [100, 200, 400, 800]:
    c = cota_total(n, 3 * n) / (3 * n)
    s = costo_por_acceso(n)
    assert s <= c
    medido.append((n, s))
    cota.append((n, c))
    print(f"{n:>5} {math.log2(n):>7.1f} {c:>16.1f} {s:>7.1f}")
raiz = camino(800)
print(f"\nprimer acceso, a la clave 1 con n = 800: {splay(buscar(raiz, 1))} rotaciones")

# == bloque: figura (oculto)
try:
    import figuras as F
except ImportError:
    print("sin tesserax no se regenera la figura")
else:
    figura = F.grafica_log_log({"cota (k = 3)": cota, "medido": medido}, "n",
                               "rotaciones por acceso", ident="ejercicio-13-cota")
    svg = figura[figura.index("<svg"):figura.index("</svg>") + len("</svg>")]
    vb = svg.split('viewBox="')[1].split('"')[0].split()   # fondo blanco para GitHub
    fondo = f'<rect x="{vb[0]}" y="{vb[1]}" width="{vb[2]}" height="{vb[3]}" fill="white"/>'
    (AQUI.parent / "figuras" / "ejercicio-13-cota.svg").write_text(
        svg.replace(">", ">" + fondo, 1), encoding="utf-8")
