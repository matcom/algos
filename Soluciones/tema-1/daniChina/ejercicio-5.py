"""
Tema 1, ejercicio 5: detección de ciclos en una lista enlazada (Floyd).

Dos punteros: la tortuga avanza 1 nodo por vuelta, la liebre avanza 2.
Hay que probar:
  * correctitud parcial (con un invariante): devuelve True  <=>  hay ciclo
  * terminación (con un potencial)
  * costo

Modelo: RAM. Seguir un puntero cuesta 1, comparar dos referencias cuesta 1.
Uso:  python ejercicio5_floyd.py
"""
import math
import random
from pathlib import Path


# ----------------------------------------------------------------------------
# Estructura de datos y generador de listas
# ----------------------------------------------------------------------------
class Nodo:
    __slots__ = ("valor", "siguiente")

    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None


def construir(mu, lam):
    """Lista con mu nodos de cola y lam nodos de ciclo (lam = 0: sin ciclo).

    El ultimo nodo apunta al nodo de indice mu. Con mu = 0 la lista es
    circular pura. Devuelve la cabeza (None si la lista es vacia)."""
    nodos = [Nodo(i) for i in range(mu + lam)]
    for a, b in zip(nodos, nodos[1:]):
        a.siguiente = b
    if lam > 0:
        nodos[-1].siguiente = nodos[mu]
    return nodos[0] if nodos else None


# ----------------------------------------------------------------------------
# El algoritmo
# ----------------------------------------------------------------------------
def floyd(cabeza):
    t = h = cabeza                         # tortuga y liebre
    while h is not None and h.siguiente is not None:
        t = t.siguiente                    # 1 paso
        h = h.siguiente.siguiente          # 2 pasos
        if t is h:                         # se compara DESPUES de mover
            return True
    return False


# ----------------------------------------------------------------------------
# Oraculo: el que recorre todo y recuerda lo que vio (O(n) memoria)
# ----------------------------------------------------------------------------
def estructura(cabeza):
    """Devuelve (orden, mu, lam): los nodos alcanzables en orden v_0, v_1, ...
    mu = indice donde empieza el ciclo, lam = largo del ciclo (0 si no hay)."""
    visto, orden = {}, []
    p = cabeza
    while p is not None and id(p) not in visto:
        visto[id(p)] = len(orden)
        orden.append(p)
        p = p.siguiente
    if p is None:
        return orden, len(orden), 0
    mu = visto[id(p)]
    return orden, mu, len(orden) - mu


def v(orden, mu, lam, i):
    """El nodo v_i de la sucesion v_0 = cabeza, v_{i+1} = v_i.siguiente.
    None si la sucesion ya se acabo (solo pasa si no hay ciclo)."""
    if i < len(orden):
        return orden[i]
    if lam == 0:
        return None
    return orden[mu + (i - mu) % lam]


def distancia_ciclo(desde, hasta):
    """Pasos hacia adelante (por el ciclo) para ir de 'desde' a 'hasta'."""
    pasos, p = 0, desde
    while p is not hasta:
        p = p.siguiente
        pasos += 1
    return pasos


def tiene_ciclo_oraculo(cabeza):
    return estructura(cabeza)[2] > 0


# ----------------------------------------------------------------------------
# Floyd vigilado: ejecuta el invariante y el potencial de la demostracion
# ----------------------------------------------------------------------------
def floyd_vigilado(cabeza):
    orden, mu, lam = estructura(cabeza)
    n = len(orden)                         # nodos distintos alcanzables
    t = h = cabeza
    k = 0                                  # vueltas completadas
    e_prev = None                          # e_k: distancia de la liebre a la tortuga
    while True:
        # INVARIANTE: despues de k vueltas, t = v_k y h = v_2k
        assert t is v(orden, mu, lam, k) and h is v(orden, mu, lam, 2 * k)
        # POTENCIAL: phi = n - k, entero y no negativo
        assert n - k >= 0
        if not (h is not None and h.siguiente is not None):
            assert lam == 0                # salir por la guarda => no hay ciclo
            return False, k
        assert n - k >= 1                  # entrar a una vuelta exige phi > 0
        t = t.siguiente
        h = h.siguiente.siguiente
        k += 1
        if lam > 0 and k >= max(mu, 1):    # ya estan los dos dentro del ciclo
            e = distancia_ciclo(h, t)      # POTENCIAL del reciproco
            assert 0 <= e < lam
            if e_prev is not None:
                assert e == e_prev - 1     # baja exactamente 1 por vuelta
            e_prev = e
        if t is h:
            assert lam > 0 and k <= max(mu, 1) + lam - 1 <= n
            return True, k


# ----------------------------------------------------------------------------
# Un "atajo" plausible y roto: la liebre vuelve al inicio => hay ciclo
# ----------------------------------------------------------------------------
def floyd_atajo(cabeza, limite):
    h = cabeza
    pasos = 0
    while h is not None and h.siguiente is not None:
        if pasos >= limite:
            return "no termina"
        h = h.siguiente.siguiente
        pasos += 1
        if h is cabeza:
            return "ciclo"
    return "sin ciclo"


def veredicto(r):
    return {"ciclo": True, "sin ciclo": False}.get(r, r)


# ----------------------------------------------------------------------------
# Animacion (opcional, necesita Pillow)
# ----------------------------------------------------------------------------
def generar_gif(mu, lam, ruta):
    from PIL import Image, ImageDraw

    assert mu >= 1 and lam >= 2
    X0, Y, DX, R, r = 60, 160, 70, 90, 16
    cx = X0 + DX * (mu - 1) + DX + R
    W, H = cx + R + 60, 320
    n = mu + lam

    def pos(idx):
        if idx < mu:
            return X0 + DX * idx, Y
        ang = math.pi + 2 * math.pi * (idx - mu) / lam
        return cx + R * math.cos(ang), Y + R * math.sin(ang)

    def idx_de(i):                         # v_i -> indice de nodo
        return i if i < mu else mu + (i - mu) % lam

    def flecha(d, a, b):
        (x1, y1), (x2, y2) = pos(a), pos(b)
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        sx, sy, ex, ey = x1 + ux * r, y1 + uy * r, x2 - ux * r, y2 - uy * r
        d.line([sx, sy, ex, ey], fill="#555555", width=2)
        px, py = -uy, ux
        d.polygon([(ex, ey), (ex - ux * 9 + px * 5, ey - uy * 9 + py * 5),
                   (ex - ux * 9 - px * 5, ey - uy * 9 - py * 5)], fill="#555555")

    # primera vuelta k >= 1 con v_k = v_2k
    k_meet = next(k for k in range(1, n + 1)
                  if idx_de(k) == idx_de(2 * k))
    frames = []
    for k in range(k_meet + 1):
        im = Image.new("RGB", (W, H), "white")
        d = ImageDraw.Draw(im)
        for a in range(n):
            flecha(d, a, a + 1 if a + 1 < n else mu)
        it, ih = idx_de(k), idx_de(2 * k)
        for a in range(n):
            x, y = pos(a)
            relleno = "#ffffff"
            if a == it and a == ih:
                relleno = "#d9a7f0"
            elif a == it:
                relleno = "#a9d1f7"
            elif a == ih:
                relleno = "#f7b0b0"
            d.ellipse([x - r, y - r, x + r, y + r], fill=relleno,
                      outline="#222222", width=2)
            d.text((x - 4 * len(str(a)), y - 5), str(a), fill="black")
        d.text((15, 10), f"k = {k}    tortuga T = v_{k} (azul)    "
                         f"liebre H = v_{2 * k} (roja)", fill="black")
        d.text((15, 28), f"phi = n - k = {n} - {k} = {n - k}", fill="#444444")
        if k == k_meet:
            d.text((15, 46), "T is H  ->  hay ciclo", fill="#b00020")
        frames.append(im)
    frames += [frames[-1]] * 2
    frames[0].save(ruta, save_all=True, append_images=frames[1:],
                   duration=1000, loop=0)


# ----------------------------------------------------------------------------
# Experimentos
# ----------------------------------------------------------------------------
def traza(mu, lam):
    cab = construir(mu, lam)
    orden, mu_, lam_ = estructura(cab)
    n = len(orden)
    print(f"Traza sobre mu={mu}, lam={lam} (n={n}):")
    print(f"{'k':>3} {'T=v_k':>7} {'H=v_2k':>7} {'phi=n-k':>8}")
    t = h = cab
    k = 0
    while True:
        print(f"{k:>3} {orden.index(t):>7} {orden.index(h):>7} {n - k:>8}")
        if k > 0 and t is h:
            print("    t is h -> True")
            return
        t, h, k = t.siguiente, h.siguiente.siguiente, k + 1


def exhaustivo(tope=30):
    casos = 0
    for mu in range(tope + 1):
        for lam in range(tope + 1):
            cab = construir(mu, lam)
            n = mu + lam
            res, k = floyd_vigilado(cab)           # los assert viven aqui
            assert res == (lam > 0) == floyd(cab) == tiene_ciclo_oraculo(cab)
            if lam > 0:                            # se encuentran a tiempo
                assert k <= max(mu, 1) + lam - 1 <= n
            else:
                assert k <= n // 2
            casos += 1
    print(f"invariante, potencial y resultado comprobados en {casos} listas "
          f"(mu, lam <= {tope}), sin fallos")


def experimento_atajo():
    rng = random.Random(7)
    gens = {
        "circulares y rectas": lambda: rng.choice(
            [(0, rng.randint(1, 10)), (rng.randint(0, 10), 0)]),
        "cola + ciclo": lambda: (rng.randint(1, 10), rng.randint(1, 10)),
        "todo mezclado": lambda: rng.choice(
            [(0, rng.randint(1, 10)), (rng.randint(0, 10), 0),
             (rng.randint(1, 10), rng.randint(1, 10))]),
    }
    print(f"{'generador':>20} {'atajo':>8} {'Floyd':>8}")
    for nombre, g in gens.items():
        fa = ff = 0
        N = 2000
        for _ in range(N):
            mu, lam = g()
            cab = construir(mu, lam)
            esperado = tiene_ciclo_oraculo(cab)
            fa += veredicto(floyd_atajo(cab, 4 * (mu + lam) + 4)) != esperado
            ff += floyd(cab) != esperado
        print(f"{nombre:>20} {100 * fa / N:>7.1f}% {100 * ff / N:>7.1f}%")


def main():
    traza(4, 5)
    print()
    exhaustivo()
    print()
    experimento_atajo()
    print()
    try:
        ruta = Path(__file__).with_name("floyd_animacion.gif")
        generar_gif(4, 5, ruta)
        print("animacion guardada en", ruta.name)
    except ImportError:
        print("(sin Pillow: se omite la animacion)")


if __name__ == "__main__":
    main()
