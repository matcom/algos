"""Ejercicio 10. Par más cercano en una dimensión."""
import math
import random
import time
from itertools import permutations


# ---------- Parte 1: la cota (comprobación del argumento de convexidad) -------------
def hojas_minimas(n):
    """n! órdenes: cada orden necesita su propia hoja."""
    return math.factorial(n)


def profundidad_minima(n):
    """Menor d con 3^d >= n!."""
    d = 0
    while 3 ** d < math.factorial(n):
        d += 1
    return d


def segmento_cruza_pared(P, Q):
    """Si P y Q tienen órdenes distintos, el segmento PQ contiene un punto con
    dos coordenadas iguales (entrada con repetidos)."""
    n = len(P)
    for i in range(n):
        for j in range(i + 1, n):
            f = lambda t: (P[i] + t * (Q[i] - P[i])) - (P[j] + t * (Q[j] - P[j]))
            if f(0) * f(1) < 0:
                t = f(0) / (f(0) - f(1))
                R = [P[k] + t * (Q[k] - P[k]) for k in range(n)]
                return abs(R[i] - R[j]) < 1e-9
    return False


# ---------- Parte 4: algoritmo de la rejilla en una dimensión ------------------------
def par_mas_cercano_1d(xs, barajar=True, semilla=0):
    """Devuelve (distancia mínima, reconstrucciones, trabajo).

    El trabajo cuenta las lecturas y escrituras en la tabla (incluidas las de las
    reconstrucciones), que es lo que el análisis del texto acota por O(n) esperado."""
    pts = list(xs)
    if barajar:
        random.Random(semilla).shuffle(pts)
    delta = abs(pts[0] - pts[1])
    if delta == 0:
        return 0.0, 0, 0
    tabla = {math.floor(q / delta): q for q in pts[:2]}
    reconstrucciones, trabajo = 0, 2
    for i in range(2, len(pts)):
        p = pts[i]
        k = math.floor(p / delta)
        mejor = delta
        for c in (k - 1, k, k + 1):
            trabajo += 1
            if c in tabla:
                mejor = min(mejor, abs(p - tabla[c]))
        if mejor < delta:
            delta = mejor
            if delta == 0:
                return 0.0, reconstrucciones, trabajo
            tabla = {math.floor(q / delta): q for q in pts[:i + 1]}
            reconstrucciones += 1
            trabajo += i + 1
        else:
            tabla[k] = p
            trabajo += 1
    return delta, reconstrucciones, trabajo


def por_ordenamiento(xs):
    ys = sorted(xs)
    return min(ys[i + 1] - ys[i] for i in range(len(ys) - 1))


def entrada_adversaria(n):
    """Puntos 1 + 1/i: cada punto nuevo forma un par más cercano que todos los anteriores."""
    return [1 + 1 / i for i in range(1, n + 1)]


if __name__ == "__main__":
    print("Hojas mínimas (n!) y profundidad mínima con tres ramas por nodo")
    print(f"{'n':>3} {'n!':>10} {'menor d con 3^d >= n!':>22}")
    for n in [2, 3, 4, 5, 8, 10]:
        print(f"{n:>3} {hojas_minimas(n):>10,} {profundidad_minima(n):>22}")

    rng = random.Random(10)
    pares, bien = 0, 0
    for n in [2, 3, 4]:
        ordenes = list(permutations(range(1, n + 1)))
        for P in ordenes:
            for Q in ordenes:
                if P != Q:
                    pares += 1
                    bien += segmento_cruza_pared(list(P), list(Q))
    print(f"\nPares de entradas con órdenes distintos (n = 2, 3, 4): {pares}; "
          f"su segmento pasa por una entrada con repetidos en {bien}")

    print("\nReducción: distancia mínima = 0  <=>  hay repetidos")
    for xs in ([7, 3, 7, 1], [7, 3, 5, 1]):
        print(f"  {xs}: distancia mínima = {por_ordenamiento(xs)}, repetidos = {len(set(xs)) < len(xs)}")

    print("\nCorrección del algoritmo de la rejilla contra el ordenamiento")
    casos = 0
    for _ in range(3000):
        n = rng.randint(2, 30)
        xs = [round(rng.uniform(0, 50), 1) for _ in range(n)]
        d, _, _ = par_mas_cercano_1d(xs, semilla=rng.randint(0, 99))
        assert abs(d - por_ordenamiento(xs)) < 1e-9
        casos += 1
    print(f"  {casos} entradas aleatorias, sin discrepancias")

    print("\nEjemplo del texto: orden de inserción 7, 2.5, 9.1, 2.6")
    pts = [7, 2.5, 9.1, 2.6]
    delta = abs(pts[0] - pts[1])
    print(f"  tras 7 y 2.5: delta = {delta}")
    for p in pts[2:]:
        k = math.floor(p / delta)
        celdas = [c for c in (k - 1, k, k + 1)]
        print(f"  punto {p}: celda {k}, se revisan {celdas}")
        previos = pts[:pts.index(p)]
        mejor = min(abs(p - q) for q in previos)
        if mejor < delta:
            delta = mejor
            print(f"    mejora: delta = {delta:.1f}")

    print("\nTrabajo por punto en la tabla, con el orden aleatorio y con el orden adversario")
    print(f"{'n':>6} {'azar: trabajo/n':>16} {'azar: reconstr.':>16} {'2 ln n':>7} "
          f"{'adversario: trabajo/n':>22} {'adversario: reconstr.':>22}")
    for n in [200, 1000, 3000]:
        xs = [rng.uniform(0, 1) for _ in range(n)]
        veces = 5
        t = r = 0.0
        for s_ in range(veces):
            _, rc, tr = par_mas_cercano_1d(xs, semilla=s_)
            t += tr / n
            r += rc
        ys = entrada_adversaria(n)
        d, rc_adv, tr_adv = par_mas_cercano_1d(ys, barajar=False)
        assert abs(d - por_ordenamiento(ys)) < 1e-12
        _, rc_az, tr_az = par_mas_cercano_1d(ys, barajar=True, semilla=1)
        print(f"{n:>6} {t / veces:>16.1f} {r / veces:>16.1f} {2 * math.log(n):>7.1f} "
              f"{tr_adv / n:>22.1f} {rc_adv:>22}")
        print(f"{'':>6} (mismos puntos adversarios, pero barajados: trabajo/n = {tr_az / n:.1f}, "
              f"reconstrucciones = {rc_az})")
