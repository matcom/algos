"""Ejercicio 11: ¿es polinomial la mochila en O(nW)? El tamaño de la entrada medido en bits.

Corre: python ejercicio-11.py  (verifica la programación dinámica contra fuerza bruta, mide
su costo en función de los bits de la entrada, lo compara con la primalidad por división
y genera la figura)
"""
import itertools
import math
import random


def mochila(pesos, valores, W):
    """Mochila 0/1 por programación dinámica. Devuelve (mejor valor, celdas calculadas).
    mejor[c] = el mayor valor con capacidad c usando los objetos vistos hasta ahora."""
    mejor = [0] * (W + 1)
    celdas = 0
    for p, v in zip(pesos, valores):
        for c in range(W, -1, -1):          # de arriba abajo: cada objeto se usa a lo sumo una vez
            celdas += 1
            if p <= c:
                mejor[c] = max(mejor[c], mejor[c - p] + v)
    return mejor[W], celdas


def fuerza_bruta(pesos, valores, W):
    n = len(pesos)
    return max(sum(valores[i] for i in S)
               for r in range(n + 1) for S in itertools.combinations(range(n), r)
               if sum(pesos[i] for i in S) <= W)


def bits(x):
    return max(1, x.bit_length())


def tamano(pesos, valores, W):
    """Bits de la entrada: los de cada peso, cada valor y la capacidad."""
    return sum(bits(p) + bits(v) for p, v in zip(pesos, valores)) + bits(W)


def instancia(rng, n, b):
    """n objetos con pesos y valores de b bits; la capacidad es la mitad de la suma de los pesos."""
    pesos = [rng.randrange(2 ** (b - 1), 2 ** b) for _ in range(n)]
    valores = [rng.randrange(2 ** (b - 1), 2 ** b) for _ in range(n)]
    return pesos, valores, sum(pesos) // 2


def divisiones(n):
    """Primalidad por división (conferencia 1): cuántas divisiones hace con n primo."""
    return math.isqrt(n) - 1


if __name__ == "__main__":
    rng = random.Random(2026)

    # 1. La programación dinámica es correcta: contra fuerza bruta en 3000 instancias chicas
    for _ in range(3000):
        n = rng.randint(0, 8)
        pesos = [rng.randint(1, 20) for _ in range(n)]
        valores = [rng.randint(0, 30) for _ in range(n)]
        W = rng.randint(0, 60)
        valor, celdas = mochila(pesos, valores, W)
        assert valor == fuerza_bruta(pesos, valores, W)
        assert celdas == n * (W + 1)
    print("3000 instancias chicas: la programación dinámica coincide con fuerza bruta")

    # 2. n fijo y números cada vez más largos: cada bit más duplica el costo
    n = 10
    print(f"\nn = {n} objetos, pesos y valores de b bits:")
    print(f"{'b':>4} {'bits entrada':>13} {'celdas n(W+1)':>15} {'celdas / bits^3':>16}")
    filas = []
    for b in [4, 8, 12, 16, 20]:
        pesos, valores, W = instancia(rng, n, b)
        L = tamano(pesos, valores, W)
        celdas = n * (W + 1)
        if b <= 16:                                    # las grandes solo se cuentan, no se corren
            assert mochila(pesos, valores, W)[1] == celdas
        filas.append((b, L, celdas))
        print(f"{b:>4} {L:>13} {celdas:>15} {celdas / L**3:>16.3g}")
    for (b1, L1, c1), (b2, L2, c2) in zip(filas, filas[1:]):
        # 4 bits más por número: el costo se multiplica por unos 2^4 = 16,
        # mucho más de lo que crecería cualquier polinomio de grado 3 en los bits
        assert c2 > 8 * c1 and c2 / c1 > (L2 / L1) ** 3
    assert all(c / L**3 < c2 / L2**3 for (_, L, c), (_, L2, c2) in zip(filas, filas[1:]))

    # 3. La misma entrada con números chicos (W polinomial en n): ahí sí es polinomial
    print(f"\nPesos y valores entre 1 y n (W ≤ n²/2):")
    print(f"{'n':>5} {'bits entrada':>13} {'celdas n(W+1)':>15} {'celdas / bits^3':>16}")
    for n in [10, 20, 40, 80, 160]:
        pesos = [rng.randint(1, n) for _ in range(n)]
        valores = [rng.randint(1, n) for _ in range(n)]
        W = sum(pesos) // 2
        L = tamano(pesos, valores, W)
        celdas = mochila(pesos, valores, W)[1]
        assert celdas <= L ** 3                      # n(W+1) ≤ n³ y L ≥ n
        print(f"{n:>5} {L:>13} {celdas:>15} {celdas / L**3:>16.3g}")

    # 4. La primalidad por división, en las mismas unidades
    print(f"\nPrimalidad por división de un primo de b bits:")
    print(f"{'b':>4} {'divisiones':>12} {'2^(b/2)':>10}")
    for p in [251, 65521, 4294967291, 18446744073709551557]:   # el mayor primo de 8, 16, 32 y 64 bits
        b = p.bit_length()
        d = divisiones(p)
        assert 2 ** (b / 2 - 1) <= d < 2 ** (b / 2)
        print(f"{b:>4} {d:>12.3g} {2 ** (b / 2):>10.3g}")

    # 5. Figura
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("\n(sin matplotlib: no se genera la figura)")
    else:
        fig, ax = plt.subplots(figsize=(7, 4.2))
        n = 10
        xs, ys = [], []
        for b in range(2, 41, 2):
            pesos, valores, W = instancia(random.Random(b), n, b)
            xs.append(tamano(pesos, valores, W)); ys.append(n * (W + 1))
        ax.plot(xs, ys, "o-", ms=3, c="#2563eb", label="mochila n(W+1), n = 10, números de b bits")
        ax.plot(xs, [L ** 3 for L in xs], "--", c="gray", label="(bits)³: un polinomio")
        ax.plot(xs, [L ** 2 for L in xs], ":", c="gray", label="(bits)²")
        ax.set_yscale("log")
        ax.set_xlabel("tamaño de la entrada en bits"); ax.set_ylabel("celdas de la tabla")
        ax.set_title("La mochila O(nW) es exponencial en los bits")
        ax.legend(fontsize=8); fig.tight_layout()
        fig.savefig("ejercicio-11-bits.png", dpi=150)
        print("\nfigura: ejercicio-11-bits.png")
