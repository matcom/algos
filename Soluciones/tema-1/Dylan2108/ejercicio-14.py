"""Ejercicio 14: el subarreglo de suma máxima, del problema a la cota mínima.

Corre: python ejercicio-14.py  (prueba los tres algoritmos contra la definición, vigila el
invariante de Kadane, cuenta lecturas, enfrenta al adversario con algoritmos que no leen
todo, prueba dos errores plantados con varios generadores y genera la figura)
"""
import random
import time


class Arreglo:
    """Un arreglo que cuenta cuántas veces se lee y qué posiciones se leyeron."""
    def __init__(self, datos):
        self.datos, self.lecturas, self.leidas = list(datos), 0, set()

    def __len__(self):
        return len(self.datos)

    def __getitem__(self, i):
        self.lecturas += 1
        self.leidas.add(i)
        return self.datos[i]


def definicion(A):
    """La respuesta por definición: el máximo sobre todos los tramos no vacíos."""
    return max(sum(A[i:j]) for i in range(len(A)) for j in range(i + 1, len(A) + 1))


def fuerza_bruta(A):
    """Probar cada tramo [i, j] y sumarlo desde cero: Θ(n³) lecturas."""
    n, mejor = len(A), None
    for i in range(n):
        for j in range(i, n):
            s = 0
            for k in range(i, j + 1):
                s += A[k]
            if mejor is None or s > mejor:
                mejor = s
    return mejor


def acumuladas(A):
    """Sumas acumuladas: P[k] = A[0] + ... + A[k-1], y la suma de [i, j] es P[j+1] - P[i].
    n lecturas de A, pero Θ(n²) restas."""
    n = len(A)
    P = [0] * (n + 1)
    for k in range(n):
        P[k + 1] = P[k] + A[k]
    return max(P[j + 1] - P[i] for i in range(n) for j in range(i, n))


def kadane(A, vigilar=False):
    """Una pasada. Devuelve (mejor suma, inicio, fin) del mejor tramo no vacío."""
    max_actual, ini_actual = A[0], 0              # el mejor tramo que termina en la posición actual
    max_global, ini, fin = max_actual, 0, 0       # el mejor tramo visto hasta ahora
    for i in range(1, len(A)):
        x = A[i]
        if max_actual + x < x:                    # empezar de nuevo en i es mejor que extender
            max_actual, ini_actual = x, i
        else:
            max_actual += x
        if max_actual > max_global:
            max_global, ini, fin = max_actual, ini_actual, i
        if vigilar:                               # el invariante, comparado con la definición
            datos = A.datos if isinstance(A, Arreglo) else A
            assert max_actual == max(sum(datos[k:i + 1]) for k in range(i + 1))
            assert max_global == definicion(datos[:i + 1])
            assert sum(datos[ini:fin + 1]) == max_global
    return max_global, ini, fin


# Algoritmos que no leen todo, para el adversario
def kadane_sin_el_ultimo(A):
    """El error de rango típico: range(1, n - 1) en lugar de range(1, n)."""
    max_actual = max_global = A[0]
    for i in range(1, len(A) - 1):
        max_actual = max(A[i], max_actual + A[i])
        max_global = max(max_global, max_actual)
    return max_global


def adversario(algoritmo, datos):
    """Si el algoritmo termina sin leer alguna posición i, el adversario cambia solo esa
    posición por (respuesta + 1). El algoritmo lee exactamente lo mismo, responde lo mismo,
    y se equivoca. Devuelve la entrada que lo rompe, o None si leyó todo."""
    A = Arreglo(datos)
    r = algoritmo(A)
    sin_leer = [i for i in range(len(datos)) if i not in A.leidas]
    if not sin_leer:
        return None
    i = sin_leer[0]
    malo = list(datos)
    malo[i] = r + 1                           # el tramo [i] solo ya suma más que la respuesta
    A2 = Arreglo(malo)
    assert algoritmo(A2) == r                 # no se entera: leyó los mismos valores
    assert definicion(malo) >= r + 1 > r      # pero la respuesta correcta es otra
    return malo


# Dos errores plantados
def kadane_con_cero(A):
    """La versión que circula: reinicia en 0, así que nunca devuelve algo negativo."""
    max_actual = max_global = 0
    for i in range(len(A)):
        max_actual = max(0, max_actual + A[i])
        max_global = max(max_global, max_actual)
    return max_global


def kadane_desfasado(A):
    """Actualiza `max_global` antes que `max_actual`: cada tramo se registra un paso tarde."""
    max_actual = max_global = A[0]
    for i in range(1, len(A)):
        max_global = max(max_global, max_actual)
        max_actual = max(A[i], max_actual + A[i])
    return max_global


if __name__ == "__main__":
    rng = random.Random(2026)

    # 1. Correctitud de los tres algoritmos, y el invariante de Kadane vigilado
    for _ in range(3000):
        n = rng.randint(1, 30)
        datos = [rng.randint(-20, 20) for _ in range(n)]
        d = definicion(datos)
        assert fuerza_bruta(datos) == acumuladas(datos) == d
        assert kadane(datos, vigilar=True)[0] == d
    for datos in ([5], [-5], [-3, -1, -2], [0, 0, 0], [2, -5, 3, 4, -1, 6, -8]):
        assert kadane(datos)[0] == definicion(datos)
    print("3000 arreglos aleatorios y casos borde: los tres algoritmos coinciden con la definición,")
    print("  y el invariante de Kadane se cumple en cada paso")
    print("  ejemplo [2, -5, 3, 4, -1, 6, -8]:", kadane([2, -5, 3, 4, -1, 6, -8]))

    # 2. Lecturas del arreglo: Kadane lee exactamente n
    print(f"\n{'n':>6} {'fuerza bruta':>14} {'n(n+1)(n+2)/6':>14} {'acumuladas':>11} {'kadane':>7}")
    for n in [1, 2, 10, 100, 300]:
        datos = [rng.randint(-100, 100) for _ in range(n)]
        lect = []
        for alg in (fuerza_bruta, acumuladas, lambda A: kadane(A)):
            A = Arreglo(datos); alg(A); lect.append(A.lecturas)
        assert lect[0] == n * (n + 1) * (n + 2) // 6 and lect[1] == n and lect[2] == n
        print(f"{n:>6} {lect[0]:>14} {n * (n + 1) * (n + 2) // 6:>14} {lect[1]:>11} {lect[2]:>7}")

    # 3. El adversario contra algoritmos que no leen todo
    print()
    for nombre, alg in [("Kadane sin el último elemento", kadane_sin_el_ultimo),
                        ("Kadane", lambda A: kadane(A)[0])]:
        datos = [rng.randint(-20, 20) for _ in range(8)]
        malo = adversario(alg, datos)
        if malo is None:
            print(f"  {nombre:<32} leyó las 8 posiciones: el adversario no puede hacer nada")
        else:
            print(f"  {nombre:<32} no leyó alguna posición; con {malo} responde "
                  f"{alg(malo)}, pero la respuesta es {definicion(malo)}")
    for _ in range(1000):                     # Kadane lee todo en cualquier entrada
        datos = [rng.randint(-20, 20) for _ in range(rng.randint(1, 20))]
        assert adversario(lambda A: kadane(A)[0], datos) is None

    # 4. Los errores plantados, contra varios generadores
    generadores = {
        "enteros en [-100, 100]":       lambda n: [rng.randint(-100, 100) for _ in range(n)],
        "mayoría positivos [-10, 100]": lambda n: [rng.randint(-10, 100) for _ in range(n)],
        "todos negativos":              lambda n: [rng.randint(-100, -1) for _ in range(n)],
        "el mejor tramo al final":      lambda n: [rng.randint(-100, -1) for _ in range(n - 1)] + [50],
    }
    print(f"\n{'generador':<30} {'reinicia en 0':>14} {'desfasado':>10}   (fallos en 2000 arreglos, n de 1 a 30)")
    tabla = {}
    for nombre, gen in generadores.items():
        f1 = f2 = 0
        for _ in range(2000):
            datos = gen(rng.randint(1, 30))
            d = kadane(datos)[0]
            f1 += kadane_con_cero(datos) != d
            f2 += kadane_desfasado(datos) != d
        tabla[nombre] = (f1, f2)
        print(f"{nombre:<30} {100 * f1 / 2000:>13.1f}% {100 * f2 / 2000:>9.1f}%")
    assert tabla["enteros en [-100, 100]"][0] < 100          # el generador uniforme casi no ve el primero
    assert tabla["todos negativos"][0] == 2000               # el que lo ve siempre
    assert tabla["el mejor tramo al final"][1] > 1500        # el que ve el segundo

    # 5. Tiempos y figura
    tiempos = {"fuerza bruta": [], "sumas acumuladas": [], "Kadane": []}
    for n in [50, 100, 200, 400, 800, 1600, 3200]:
        datos = [rng.randint(-100, 100) for _ in range(n)]
        for nombre, alg, limite in [("fuerza bruta", fuerza_bruta, 400),
                                    ("sumas acumuladas", acumuladas, 3200),
                                    ("Kadane", kadane, 3200)]:
            if n <= limite:
                t = time.perf_counter(); alg(datos); tiempos[nombre].append((n, time.perf_counter() - t))
    print()
    for nombre, puntos in tiempos.items():
        print(f"  {nombre:<17}" + "  ".join(f"n={n}: {s:.2g}s" for n, s in puntos))
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("\n(sin matplotlib: no se genera la figura)")
    else:
        fig, ax = plt.subplots(figsize=(7, 4.2))
        for (nombre, puntos), m in zip(tiempos.items(), "o^s"):
            ax.plot(*zip(*puntos), m + "-", label=nombre)
        ax.set_xscale("log"); ax.set_yscale("log")
        ax.set_xlabel("n"); ax.set_ylabel("segundos")
        ax.set_title("Subarreglo de suma máxima: pendientes 3, 2 y 1")
        ax.legend(); fig.tight_layout()
        fig.savefig("ejercicio-14-tiempos.png", dpi=150)
        print("\nfigura: ejercicio-14-tiempos.png")
