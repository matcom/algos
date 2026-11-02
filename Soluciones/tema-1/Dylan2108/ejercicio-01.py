"""Ejercicio 1: cuánto crece la entrada resoluble con una computadora 1000 veces más rápida.

Corre: python ejercicio-01.py  (imprime las tablas, comprueba las estimaciones y genera la figura)
"""
import math

def mayor_n(costo, presupuesto):
    # el mayor n con costo(n) <= presupuesto (mismo método que la sección 7 de la conferencia 1)
    alto = 2
    while costo(alto) <= presupuesto:
        alto *= 2
    bajo = alto // 2
    while bajo + 1 < alto:
        medio = (bajo + alto) // 2
        if costo(medio) <= presupuesto:
            bajo = medio
        else:
            alto = medio
    return bajo

cuadratico = lambda n: n * n
nlogn = lambda n: n * math.log2(n)

def factor_estimado(n, k):
    # solución de f (log2(f)/log2(n) + 1) = k, ecuación (1), por búsqueda binaria en [1, k]:
    # el lado izquierdo crece con f, vale 1 en f = 1 y más que k en f = k
    h = lambda f: f * (math.log2(f) / math.log2(n) + 1)
    bajo, alto = 1, k
    for _ in range(50):
        medio = (bajo + alto) / 2
        if h(medio) < k:
            bajo = medio
        else:
            alto = medio
    return bajo

K = 1000
# no sabemos qué tamaño se resuelve hoy en una hora, así que probamos muchos
TAMANOS = [10**e for e in range(1, 19, 2)]

def factor_medido(costo, n0):
    # el mayor n que cabe en 1000 veces las operaciones que hoy gasta n0, dividido entre n0
    return mayor_n(costo, K * costo(n0)) / n0

if __name__ == "__main__":
    print(f"{'n0':>8} {'f medido (n^2)':>15} {'f medido (nlogn)':>17} {'f por ec. (1)':>14}")
    filas = []
    for n0 in TAMANOS:
        f2, fl, est = factor_medido(cuadratico, n0), factor_medido(nlogn, n0), factor_estimado(n0, K)
        filas.append(fl)
        print(f"{n0:>8.0e} {f2:>15.2f} {fl:>17.2f} {est:>14.2f}")
        assert abs(f2 - math.sqrt(K)) / math.sqrt(K) < 0.01   # n^2: siempre raíz de 1000
        assert 1 < est < K                                    # n log n: menor que 1000
        assert abs(fl - est) / fl < 0.01                      # la ecuación (1) coincide con lo medido
    assert filas == sorted(filas)             # y el factor de n log n sube al crecer n

    # la figura
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("\n(sin matplotlib: no se genera la figura)")
    else:
        xs = [round(10**(e / 4)) for e in range(4, 73)]
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(xs, [factor_medido(nlogn, n) for n in xs], label="n log n")
        ax.plot(xs, [factor_medido(cuadratico, n) for n in xs], label="n²")
        ax.axhline(K, ls="--", c="gray", lw=0.8)
        ax.text(xs[0], K * 1.08, "n (lineal): 1000", color="gray", fontsize=8)
        ax.set_xscale("log"); ax.set_yscale("log")
        ax.set_xlabel("tamaño que se resuelve hoy en una hora (n₀)"); ax.set_ylabel("factor de crecimiento de n")
        ax.set_title("Computadora 1000 veces más rápida")
        ax.legend(); fig.tight_layout()
        fig.savefig("ejercicio-01-factor.png", dpi=150)
        print("\nfigura: ejercicio-01-factor.png")
