"""
Tema 1, ejercicio 13: un splay tree que empieza como un camino de n nodos y
al que se accede a las claves 1, 2, ..., n en orden.

  * se acota el costo total con el lema de acceso
  * se compara con el costo real medido
  * se discute si la cota es ajustada

Costo real de un acceso = rotaciones que hacen falta para subir el nodo a la
raiz (1 si ya es la raiz).
Uso:  python ejercicio13_splay.py
"""
import math
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
    """Sube x un nivel rotando la arista con su padre (conserva el orden)."""
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
    """Sube x a la raiz de dos niveles en dos. Devuelve las rotaciones."""
    rotaciones = 0
    while x.padre:
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
    return rotaciones


def subir_a_la_raiz(x):
    """Heuristica ingenua: una rotacion simple por nivel."""
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
    """n en la raiz y cada clave es hija izquierda de la siguiente."""
    nodos = [Nodo(k) for k in range(1, n + 1)]
    for k in range(1, n):
        nodos[k].izq = nodos[k - 1]
        nodos[k - 1].padre = nodos[k]
    return nodos[-1]


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
    for v in reversed(orden):                       # los hijos antes que el padre
        tam[v] = (1 + (tam[v.izq] if v.izq else 0)
                  + (tam[v.der] if v.der else 0))
    return tam


def potencial(tam):
    return sum(math.log2(t) for t in tam.values())


# ----------------------------------------------------------------------------
# Costo total de la secuencia 1, 2, ..., n
# ----------------------------------------------------------------------------
def costo_total(n, reorganizar):
    raiz, total = camino(n), 0
    for clave in range(1, n + 1):
        x = buscar(raiz, clave)
        total += max(reorganizar(x), 1)
        raiz = x
    return total


def cota_del_lema(n):
    """Cota de peor caso para n accesos: n (3 log2 n + 1) + potencial inicial."""
    return n * (3 * math.log2(n) + 1) + math.log2(math.factorial(n))


def vigilar(n, filas=None):
    """Corre la secuencia vigilando el lema de acceso en cada acceso y la suma
    telescopica. Devuelve las cantidades que se comparan."""
    raiz = camino(n)
    tam = tamanos(raiz)
    phi0 = phi = potencial(tam)
    real = suma_cotas = suma_amort = 0.0
    for i in range(1, n + 1):
        x = buscar(raiz, i)
        r = math.log2(tam[x])                       # rango de x ANTES del splay
        c = max(splay(x), 1)
        raiz = x
        tam = tamanos(raiz)
        phi_nuevo = potencial(tam)
        amortizado = c + phi_nuevo - phi
        cota = 3 * (math.log2(n) - r) + 1           # lema de acceso
        assert amortizado <= cota + 1e-9            # EL LEMA
        if filas is not None:
            filas.append((i, c, r, cota, amortizado, phi_nuevo))
        real += c
        suma_cotas += cota
        suma_amort += amortizado
        phi = phi_nuevo
    assert abs(real - (suma_amort + phi0 - phi)) < 1e-6   # suma telescopica
    return {"real": real, "cota_fina": suma_cotas + phi0 - phi,
            "phi0": phi0, "phin": phi, "suma_amort": suma_amort}


# ----------------------------------------------------------------------------
# Animacion del arbol (opcional, necesita Pillow)
# ----------------------------------------------------------------------------
def _posiciones(raiz):
    """x = lugar en el recorrido en orden, y = profundidad."""
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


def generar_gif(n, ruta):
    from PIL import Image, ImageDraw, ImageFont

    try:
        fuente = ImageFont.load_default(size=14)
        chica = ImageFont.load_default(size=12)
    except TypeError:
        fuente = chica = ImageFont.load_default()
    DX, DY, X0, Y0, R = 38, 30, 30, 90, 12
    ANCHO, ALTO = X0 * 2 + DX * n, Y0 + DY * (n - 1) + 60

    def cuadro(raiz, resaltado, l1, l2, l3):
        im = Image.new("RGB", (ANCHO, ALTO), "white")
        d = ImageDraw.Draw(im)
        pos = _posiciones(raiz)
        centro = {v: (X0 + k * DX, Y0 + p * DY) for v, (k, p) in pos.items()}
        for v, (cx, cy) in centro.items():
            for h in (v.izq, v.der):
                if h:
                    d.line([cx, cy, *centro[h]], fill="#555555", width=2)
        for v, (cx, cy) in centro.items():
            fondo = "#ffe27a" if v is resaltado else "white"
            d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=fondo,
                      outline="#222222", width=2)
            d.text((cx - 4 * len(str(v.clave)), cy - 7), str(v.clave),
                   fill="black", font=chica)
        d.text((15, 10), l1, fill="black", font=fuente)
        d.text((15, 34), l2, fill="#b00020", font=chica)
        d.text((15, 56), l3, fill="#444444", font=chica)
        return im

    raiz = camino(n)
    tam = tamanos(raiz)
    frames = [cuadro(raiz, None, f"camino de {n} nodos: se accede a 1, 2, ..., {n}",
                     "estado inicial", f"potencial = {potencial(tam):.1f}")]
    total = 0
    for i in range(1, n + 1):
        x = buscar(raiz, i)
        prof = _posiciones(raiz)[x][1]
        frames.append(cuadro(raiz, x, f"acceso a la clave {i}",
                             f"esta a profundidad {prof}: hay que subirla a la raiz",
                             f"costo total hasta ahora = {total}"))
        c = max(splay(x), 1)
        raiz = x
        total += c
        tam = tamanos(raiz)
        frames.append(cuadro(raiz, x, f"despues del splay de {i}",
                             f"costo real de este acceso = {c} rotaciones",
                             f"costo total = {total}   potencial = {potencial(tam):.1f}"))
    frames += [frames[-1]]
    frames[0].save(ruta, save_all=True, append_images=frames[1:],
                   duration=900, loop=0)


def generar_grafica(ruta):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return False
    ns = [25, 50, 100, 200, 400, 800, 1600]
    real = [costo_total(n, splay) for n in ns]
    cota = [cota_del_lema(n) for n in ns]
    raiz_ = [costo_total(n, subir_a_la_raiz) for n in ns]
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    ax.loglog(ns, raiz_, "o-", color="#c2571a", label="subir a la raíz (real)")
    ax.loglog(ns, cota, "s--", color="#444444", label="cota del lema: n(3 log n + 1) + Φ₀")
    ax.loglog(ns, real, "o-", color="#1f6feb", label="splay (real)")
    ax.set_xlabel("n (tamaño del camino = número de accesos)")
    ax.set_ylabel("rotaciones en total")
    ax.set_title("Accesos 1, 2, ..., n sobre un camino")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(ruta, dpi=130)
    return True


# ----------------------------------------------------------------------------
# Experimentos
# ----------------------------------------------------------------------------
def traza(n=15):
    filas = []
    res = vigilar(n, filas)
    print(f"Traza con n = {n} (splay):  cota_i = 3 (log2 n - r(x_i)) + 1")
    print(f"{'i':>3} {'costo real':>11} {'r(x_i)':>7} {'cota_i':>7} {'amortizado':>11} {'potencial':>10}")
    for i, c, r, cota, a, phi in filas:
        print(f"{i:>3} {c:>11} {r:>7.2f} {cota:>7.2f} {a:>11.2f} {phi:>10.2f}")
    print(f"potencial inicial = {res['phi0']:.2f} (= log2 {n}!), final = {res['phin']:.2f}")
    print(f"costo real total = {res['real']:.0f}, suma de amortizados = {res['suma_amort']:.2f}, "
          f"real = amortizados + phi0 - phin  (se comprueba)")


def termina_como_camino(n):
    """Despues de accesos 1..n, el arbol vuelve a ser un camino?"""
    raiz = camino(n)
    for clave in range(1, n + 1):
        x = buscar(raiz, clave)
        splay(x)
        raiz = x
    tam = tamanos(raiz)
    return all((v.izq is None) or (v.der is None) for v in tam), abs(potencial(tam) - potencial(tamanos(camino(n)))) < 1e-9


def tabla_comparacion():
    print(f"{'n':>5} {'real':>8} {'real/n':>7} {'cota lema':>10} {'cota/n':>7} "
          f"{'cota fina':>10} {'cota fina/(n log n)':>20} {'subir a raiz':>13} {'n^2/2':>9}")
    for n in (50, 100, 200, 400):
        res = vigilar(n)
        rr = costo_total(n, subir_a_la_raiz)
        cota = cota_del_lema(n)
        print(f"{n:>5} {res['real']:>8.0f} {res['real'] / n:>7.2f} {cota:>10.0f} "
              f"{cota / n:>7.1f} {res['cota_fina']:>10.0f} {res['cota_fina'] / (n * math.log2(n)):>20.2f} "
              f"{rr:>13} {n * n // 2:>9}")
    camino_final, mismo_phi = termina_como_camino(400)
    print(f"con n = 400 el arbol final es un camino: {camino_final}, mismo potencial que al inicio: {mismo_phi}")
    print("sin vigilar (solo contar rotaciones):")
    print(f"{'n':>5} {'real':>8} {'real/n':>7} {'log2 n':>7} {'cota lema / real':>17}")
    for n in (800, 1600, 3200, 6400):
        real = costo_total(n, splay)
        print(f"{n:>5} {real:>8} {real / n:>7.2f} {math.log2(n):>7.1f} "
              f"{cota_del_lema(n) / real:>17.1f}")


def costo_por_acceso(reorganizar, n, rondas):
    """Costo medio por acceso al recorrer las claves 1..n varias veces seguidas."""
    raiz, total = camino(n), 0
    for _ in range(rondas):
        for clave in range(1, n + 1):
            x = buscar(raiz, clave)
            total += max(reorganizar(x), 1)
            raiz = x
    return total / (rondas * n)


def tabla_rondas():
    print("Costo por acceso, recorriendo las claves en orden 1 ronda o 3 rondas seguidas:")
    print(f"{'n':>5} {'splay 1 ronda':>14} {'splay 3 rondas':>15} {'subir a raiz 3 rondas':>22} {'log2 n':>7}")
    for n in (100, 200, 400, 800):
        print(f"{n:>5} {costo_por_acceso(splay, n, 1):>14.2f} {costo_por_acceso(splay, n, 3):>15.2f} "
              f"{costo_por_acceso(subir_a_la_raiz, n, 3):>22.1f} {math.log2(n):>7.1f}")


def main():
    traza()
    print()
    tabla_comparacion()
    print()
    tabla_rondas()
    print()
    try:
        base = Path(__file__).parent
        generar_gif(15, base / "splay_secuencial.gif")
        print("animacion guardada en splay_secuencial.gif")
        if generar_grafica(base / "cotas_vs_real.png"):
            print("grafica guardada en cotas_vs_real.png")
        else:
            print("(sin matplotlib: se omite la grafica)")
    except ImportError:
        print("(sin Pillow: se omite la animacion)")


if __name__ == "__main__":
    main()
