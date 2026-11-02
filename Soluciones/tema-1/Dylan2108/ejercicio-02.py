"""Ejercicio 2: invariante, potencial y cota de información de la búsqueda binaria.

Corre: python ejercicio-02.py
"""
import math, random

def busqueda_binaria(A, x, vigilar=False, variante=None, tope_iter=None):
    """Devuelve (resultado, comparaciones). resultado = ("está", i) o ("hueco", g).
    variante: None (correcta), "hi=m-1" (rompe el invariante), "lo=m" (rompe el potencial)."""
    lo, hi, comps = 0, len(A), 0
    phi_prev = hi - lo
    iters = 0
    while lo < hi:
        iters += 1
        if tope_iter and iters > tope_iter:
            return ("no termina", None), comps
        m = (lo + hi) // 2
        comps += 1                                   # una comparación de tres vías
        if x == A[m]:
            return ("está", m), comps
        if x < A[m]:
            hi = m - 1 if variante == "hi=m-1" else m
        else:
            lo = m if variante == "lo=m" else m + 1
        if vigilar:
            # I1: 0 <= lo <= hi <= n
            assert 0 <= lo <= hi <= len(A)
            # I2: todo lo que está a la izquierda de lo es < x, y todo desde hi es > x
            assert all(a < x for a in A[:lo]) and all(a > x for a in A[hi:])
            # potencial: Φ = hi - lo baja al menos a la mitad (redondeada abajo)
            assert hi - lo <= phi_prev // 2
            phi_prev = hi - lo
    return ("hueco", lo), comps


def todas_las_consultas(n):
    """A = [2, 4, ..., 2n]; las consultas 2g+1 caen en el hueco g, las 2i+2 están en i."""
    A = list(range(2, 2 * n + 1, 2))
    return A, [(2 * g + 1, ("hueco", g)) for g in range(n + 1)] + \
              [(2 * i + 2, ("está", i)) for i in range(n)]


if __name__ == "__main__":
    # 1. Correctitud exhaustiva con invariante y potencial vigilados, n = 0..300
    for n in range(301):
        A, consultas = todas_las_consultas(n)
        peor = 0
        for x, esperado in consultas:
            r, c = busqueda_binaria(A, x, vigilar=True)
            assert r == esperado, (n, x, r)
            peor = max(peor, c)
        # 2. El peor caso coincide EXACTAMENTE con la cota de información
        assert peor == math.ceil(math.log2(n + 1)), (n, peor)
    print("n = 0..300: todas las consultas correctas, I y Φ vigilados en cada paso")
    print("peor caso == ceil(log2(n+1)) para todo n = 0..300")

    print(f"\n{'n':>6} {'huecos':>7} {'cota ⌈log2(n+1)⌉':>17} {'peor caso medido':>17}")
    for n in [1, 2, 3, 7, 8, 100, 1000, 10**5]:
        A, consultas = todas_las_consultas(n)
        peor = max(busqueda_binaria(A, x)[1] for x, _ in consultas)
        print(f"{n:>6} {n + 1:>7} {math.ceil(math.log2(n + 1)):>17} {peor:>17}")

    # 3. Errores plantados: qué ven las pruebas
    rng = random.Random(2026)
    print(f"\n{'variante':>8} {'consultas que están':>20} {'consultas en huecos':>20} {'exhaustivo n<=50':>17}")
    for var in ["hi=m-1", "lo=m"]:
        fallos_dentro = fallos_hueco = 0
        for _ in range(2000):
            n = rng.randint(1, 100)
            A, consultas = todas_las_consultas(n)
            dentro = [q for q in consultas if q[1][0] == "está"]
            fuera = [q for q in consultas if q[1][0] == "hueco"]
            for lista, cuenta in ((dentro, "d"), (fuera, "h")):
                x, esp = rng.choice(lista)
                r, _ = busqueda_binaria(A, x, variante=var, tope_iter=4 * n + 4)
                if r != esp:
                    if cuenta == "d": fallos_dentro += 1
                    else: fallos_hueco += 1
        exhaustivo = any(busqueda_binaria(A, x, variante=var, tope_iter=4 * n + 4)[0] != esp
                         for n in range(51) for A, cs in [todas_las_consultas(n)] for x, esp in cs)
        print(f"{var:>8} {100 * fallos_dentro / 2000:>19.1f}% {100 * fallos_hueco / 2000:>19.1f}% "
              f"{'lo atrapa' if exhaustivo else 'no':>17}")

    # contraejemplos mínimos
    print("\nhi=m-1, A=[1,2,3], x=1 ->", busqueda_binaria([1, 2, 3], 1, variante="hi=m-1")[0])
    print("lo=m,   A=[1,2],   x=3 ->", busqueda_binaria([1, 2], 3, variante="lo=m", tope_iter=100)[0])
