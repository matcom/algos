#!/usr/bin/env python3
"""Verificación del ejercicio 1 (Conferencia 1, DAA 2026).

Pregunta: con una computadora k veces más rápida y el mismo tiempo, ¿cuánto
crece el mayor tamaño de entrada resoluble, para costos n, n log n, n^2, n^3, 2^n?

Python 3, sin dependencias externas.
"""
import math
import random

# ---------------------------------------------------------------- algoritmo

def mayor_n(costo, presupuesto):
    """Mayor n >= 1 con costo(n) <= presupuesto (búsqueda binaria).

    Precondiciones: costo estrictamente creciente en n >= 1 y
    costo(1) <= presupuesto. Búsqueda binaria con fase previa de duplicación.
    """
    alto = 2
    while costo(alto) <= presupuesto:      # fase 1: duplicar hasta pasarse
        alto *= 2
    bajo = alto // 2
    while bajo + 1 < alto:                 # fase 2: bisección
        medio = (bajo + alto) // 2
        if costo(medio) <= presupuesto:
            bajo = medio
        else:
            alto = medio
    return bajo


def fuerza_bruta(costo, presupuesto):
    """Escaneo lineal: referencia para comparar con mayor_n."""
    n = 1
    while costo(n + 1) <= presupuesto:
        n += 1
    return n


COSTOS = {
    "n": lambda n: n,
    "n log n": lambda n: n * math.log2(n),
    "n^2": lambda n: n ** 2,
    "n^3": lambda n: n ** 3,
    "2^n": lambda n: 2 ** n,
}

HORA = 3600 * 10 ** 9   # una hora a 10^9 operaciones por segundo


def fmt(x):
    return f"{x:.3g}"


# ------------------------------------------------- 1. casos de referencia

def casos_referencia():
    esperado = {   # valores de referencia (notación .3g)
        "n":       ("3.6e+12", "3.6e+13", "3.6e+15"),
        "n log n": ("9.86e+10", "9.06e+11", "7.8e+13"),
        "n^2":     ("1.9e+06", "6e+06", "6e+07"),
        "n^3":     ("1.53e+04", "3.3e+04", "1.53e+05"),
        "2^n":     ("41", "45", "51"),
    }
    print("### Tabla 1. Mayor `n` resuelto en una hora\n")
    print("| costo | actual | 10x | 1000x | factor 1000x |")
    print("|---|---|---|---|---|")
    for nombre, costo in COSTOS.items():
        ns = [mayor_n(costo, HORA * k) for k in (1, 10, 1000)]
        obtenido = tuple(fmt(n) for n in ns)
        assert obtenido == esperado[nombre], (nombre, obtenido, esperado[nombre])
        print(f"| {nombre} | {obtenido[0]} | {obtenido[1]} | {obtenido[2]} "
              f"| {ns[2] / ns[0]:.1f} |")
    print()


# ------------------------------------------- 2. exhaustivo y aleatorio vs BF

def exhaustivo_pequeno(tope=3000):
    total = 0
    for nombre, costo in COSTOS.items():
        for B in range(math.ceil(costo(1)), tope + 1):
            N = mayor_n(costo, B)
            assert N == fuerza_bruta(costo, B), (nombre, B)
            assert costo(N) <= B < costo(N + 1), (nombre, B)
            total += 1
    return total


def aleatorio_vs_fuerza_bruta(ensayos=300, tope=20000, semilla=0):
    rnd = random.Random(semilla)
    for nombre, costo in COSTOS.items():
        for _ in range(ensayos):
            B = rnd.randint(math.ceil(costo(1)), tope)
            assert mayor_n(costo, B) == fuerza_bruta(costo, B), (nombre, B)
    return ensayos * len(COSTOS)


# ----------------------------------------------------- 3. factores teóricos

def factores_cuadratico():
    print("### Tabla 2. Factor para `n^2` con k = 1000\n")
    print("| presupuesto B | n (B) | n' (1000 B) | n'/n | raíz de 1000 |")
    print("|---|---|---|---|---|")
    for e in range(6, 19, 3):
        B = 10 ** e
        N, M = mayor_n(COSTOS["n^2"], B), mayor_n(COSTOS["n^2"], 1000 * B)
        f = M / N
        for k in (10, 100, 1000):
            Nk = mayor_n(COSTOS["n^2"], k * B)
            assert abs(Nk / N - math.sqrt(k)) <= math.sqrt(k) * 2 / N
        print(f"| 1e{e} | {fmt(N)} | {fmt(M)} | {f:.2f} | {math.sqrt(1000):.2f} |")
    print()


def factores_nlogn():
    print("### Tabla 3. Factor para `n log n` con k = 1000\n")
    print("| presupuesto B | n (B) | n' (1000 B) | f = n'/n | cota inferior | k |")
    print("|---|---|---|---|---|---|")
    k = 1000
    previo = 0
    filas = [("1e6", 10 ** 6), ("1e9", 10 ** 9), ("1e12", 10 ** 12),
             ("3.6e12 (1 h)", HORA), ("1e15", 10 ** 15), ("1e18", 10 ** 18)]
    for etiqueta, B in filas:
        costo = COSTOS["n log n"]
        N, M = mayor_n(costo, B), mayor_n(costo, k * B)
        f = M / N
        cota = k / (1 + math.log2(k) / math.log2(N))
        tol = 2 / N
        assert f < k                                   # f < k
        assert f >= cota * (1 - tol)                   # cota inferior
        # ecuación de punto fijo  f (1 + log f / log n) = k
        assert abs(f * (1 + math.log2(f) / math.log2(N)) - k) <= k * tol * 50
        assert f > previo                              # f crece con B (empírico)
        previo = f
        print(f"| {etiqueta} | {fmt(N)} | {fmt(M)} | {f:.1f} | {cota:.1f} | {k} |")
    print()


def factores_por_k():
    print("### Tabla 4. Factor de crecimiento de la entrada según k (B = 1 hora)\n")
    print("| costo | k = 10 | k = 100 | k = 1000 | predicción |")
    print("|---|---|---|---|---|")
    pred = {"n": "k", "n log n": "< k, casi k", "n^2": "raíz de k",
            "n^3": "raíz cúbica de k", "2^n": "suma log2 k"}
    for nombre, costo in COSTOS.items():
        N = mayor_n(costo, HORA)
        celdas = []
        for k in (10, 100, 1000):
            M = mayor_n(costo, k * HORA)
            celdas.append(f"+{M - N}" if nombre == "2^n" else f"{M / N:.1f}")
        print(f"| {nombre} | " + " | ".join(celdas) + f" | {pred[nombre]} |")
    # sumas esperadas para 2^n: floor(log2 k) o ceil
    N = mayor_n(COSTOS["2^n"], HORA)
    for k in (10, 100, 1000):
        s = mayor_n(COSTOS["2^n"], k * HORA) - N
        assert abs(s - math.log2(k)) < 1
    print()


# --------------------------------------------------------------------- main

if __name__ == "__main__":
    casos_referencia()
    total = exhaustivo_pequeno()
    print(f"Exhaustivo (B <= 3000, 5 costos): {total} casos, mayor_n == fuerza bruta.")
    total = aleatorio_vs_fuerza_bruta()
    print(f"Aleatorio (B <= 20000, semilla 0): {total} casos, mayor_n == fuerza bruta.\n")
    factores_cuadratico()
    factores_nlogn()
    factores_por_k()
    print("TODAS LAS VERIFICACIONES PASARON")
