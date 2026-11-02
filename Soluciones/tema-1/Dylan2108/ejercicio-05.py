"""Ejercicio 5: detección de ciclos de Floyd (tortuga y liebre).

Corre: python ejercicio-05.py
"""
import math

class Nodo:
    __slots__ = ("sig",)
    def __init__(self):
        self.sig = None


def lista(mu, lam):
    """Lista con una cola de mu nodos y un ciclo de lam nodos (lam = 0: sin ciclo, mu nodos).
    Devuelve (cabeza, nodos) con nodos[i] = x_i."""
    nodos = [Nodo() for _ in range(mu + lam)]
    for a, b in zip(nodos, nodos[1:]):
        a.sig = b
    if lam:
        nodos[-1].sig = nodos[mu]
    return (nodos[0] if nodos else None), nodos


def floyd(cabeza, vel_t=1, vel_h=2, tope=None):
    """Devuelve (hay_ciclo, iteraciones). vel_t, vel_h: pasos por iteración (para las variantes)."""
    t = h = cabeza
    k = 0
    while True:
        # la liebre avanza vel_h pasos; si encuentra el final, no hay ciclo
        for _ in range(vel_h):
            if h is None:
                return False, k
            h = h.sig
        if h is None:
            return False, k + 1
        for _ in range(vel_t):
            t = t.sig
        k += 1
        if t is h:
            return True, k
        if tope and k >= tope:
            return None, k               # "no termina"


def floyd_vigilado(cabeza, nodos, mu, lam):
    """Floyd con el invariante y el potencial comprobados en cada iteración."""
    t = h = cabeza
    k = 0
    phi_prev = None
    while h is not None and h.sig is not None:
        t, h = t.sig, h.sig.sig
        k += 1
        # Invariante: t = x_k, h = x_{2k}, y no se encontraron antes
        assert t is x(nodos, mu, lam, k) and h is x(nodos, mu, lam, 2 * k)
        if lam:
            # Potencial: n - k mientras la tortuga no entra al ciclo; después, la distancia
            # de la liebre a la tortuga a lo largo del ciclo
            phi = (-k) % lam if k >= max(mu, 1) else mu + lam - k
            assert phi >= 0 and (phi_prev is None or phi < phi_prev)
            phi_prev = phi
        if t is h:
            return True, k
    return False, k


def x(nodos, mu, lam, i):
    """x_i: el nodo al que se llega desde la cabeza con i pasos (None si se sale de la lista)."""
    if i < mu + lam:
        return nodos[i]
    return None if lam == 0 else nodos[mu + (i - mu) % lam]


def k_estrella(mu, lam):
    """La primera iteración k >= 1 con x_k = x_{2k}: el menor múltiplo de lam que es >= max(mu, 1)."""
    return lam * max(1, math.ceil(mu / lam))


def inicio_del_ciclo(cabeza):
    """Fase 2 clásica: tras el encuentro, una tortuga desde la cabeza y otra desde el encuentro."""
    t = h = cabeza
    while True:
        t, h = t.sig, h.sig.sig
        if t is h:
            break
    t = cabeza
    mu = 0
    while t is not h:
        t, h = t.sig, h.sig
        mu += 1
    lam, h = 1, t.sig
    while h is not t:
        h, lam = h.sig, lam + 1
    return mu, lam


if __name__ == "__main__":
    # 1. Exhaustivo: todas las formas (mu, lam) con mu, lam <= 40
    for mu in range(0, 41):
        for lam in range(0, 41):
            if mu + lam == 0:
                continue
            cab, nodos = lista(mu, lam)
            hay, k = floyd_vigilado(cab, nodos, mu, lam)
            assert hay == (lam > 0)
            assert floyd(cab) == (hay, k)
            if lam:
                assert k == k_estrella(mu, lam) <= mu + lam
                assert inicio_del_ciclo(cab) == (mu, lam)
            else:
                assert k == mu // 2                  # sin ciclo: floor(L/2) iteraciones
    print("mu, lam <= 40: correcto, invariante y potencial vigilados;")
    print("  iteraciones = lam * ceil(mu/lam) (con ciclo) y floor(L/2) (sin ciclo); fase 2 halla mu y lam")

    # 2. Tabla de costos
    print(f"\n{'mu':>4} {'lam':>4} {'iteraciones':>12} {'mu+lam':>7} {'pasos de puntero':>17}")
    for mu, lam in [(0, 1), (0, 10), (1, 10), (9, 10), (10, 10), (11, 10), (100, 1), (1, 100), (500, 500)]:
        cab, _ = lista(mu, lam)
        _, k = floyd(cab)
        print(f"{mu:>4} {lam:>4} {k:>12} {mu + lam:>7} {3 * k:>17}")

    # 3. Variantes de velocidad: ¿cuáles funcionan? Se prueban listas con ciclo Y sin ciclo.
    print(f"\n{'velocidades':>12} {'fallos con ciclo':>17} {'fallos sin ciclo':>17}")
    fallos = {}
    for vt, vh in [(1, 2), (1, 3), (2, 3), (0, 1), (1, 1)]:
        con = [(mu, lam) for mu in range(0, 31) for lam in range(1, 31)
               if floyd(lista(mu, lam)[0], vt, vh, tope=10 * (mu + lam) + 10)[0] is not True]
        sin = [L for L in range(1, 61) if floyd(lista(L, 0)[0], vt, vh)[0] is not False]
        fallos[(vt, vh)] = (con, sin)
        print(f"{f'({vt}, {vh})':>12} {len(con):>10} de 930 {len(sin):>10} de 60"
              + (f"   p. ej. con ciclo {con[0]}" if con else "") + (f"   p. ej. sin ciclo L={sin[0]}" if sin else ""))
    for v in [(1, 2), (1, 3), (2, 3)]:
        assert fallos[v] == ([], [])
    assert all(mu > 0 for mu, _ in fallos[(0, 1)][0]) and len(fallos[(0, 1)][0]) == 900 and not fallos[(0, 1)][1]
    assert not fallos[(1, 1)][0] and len(fallos[(1, 1)][1]) == 59     # todas salvo L = 1

    # 4. Figura: iteraciones hasta el encuentro en función de mu
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("(sin matplotlib)")
    else:
        fig, ax = plt.subplots(figsize=(7.5, 3.8))
        lam = 7
        mus = list(range(0, 50))
        ax.step(mus, [k_estrella(m, lam) for m in mus], where="post", label="iteraciones de Floyd = λ⌈μ/λ⌉")
        ax.plot(mus, [m + lam for m in mus], "--", c="gray", label="cota μ + λ")
        ax.plot(mus, mus, ":", c="gray", label="μ (la tortuga tiene que llegar al ciclo)")
        ax.set_xlabel("μ (largo de la cola)"); ax.set_ylabel("iteraciones")
        ax.set_title(f"Floyd con un ciclo de largo λ = {lam}")
        ax.legend(fontsize=8); fig.tight_layout()
        fig.savefig("ejercicio-05-iteraciones.png", dpi=150)
        print("\nfigura: ejercicio-05-iteraciones.png")
