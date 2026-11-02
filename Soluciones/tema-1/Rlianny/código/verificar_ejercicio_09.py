#!/usr/bin/env python3
"""
verificar_ejercicio_NN.py

Mezcla "optimizada" de dos listas ordenadas de largo n: deja de comparar cuando
a A le queda un solo elemento y lo pone al final.

Modelo: comparaciones. Cada comparacion A[i] <= B[j] cuenta como 1.
Elementos distintos. Solo Python 3, sin dependencias externas.

Qué verifica:
  1. Casos de prueba fijos (entrada, salida, comparaciones).
  2. Búsqueda exhaustiva para n = 1..8: peor caso y entradas que fallan.
  3. La cadena intercalada del adversario: 2n-3 comparaciones y salida incorrecta.
  4. El argumento del intercambio: dos entradas, misma salida (en posiciones).
  5. Pruebas aleatorias contra fuerza bruta (sorted).
  6. Cota inferior exacta de la mezcla (minimax sobre todos los algoritmos
     de comparaciones) para n pequeño: debe dar 2n-1.
"""
import random
from itertools import combinations
from functools import lru_cache


# ---------------------------------------------------------------- algoritmos
def mezcla_normal(A, B):
    """Mezcla clásica. Devuelve (resultado, comparaciones)."""
    R, i, j, c = [], 0, 0, 0
    while i < len(A) and j < len(B):
        c += 1
        if A[i] <= B[j]:
            R.append(A[i]); i += 1
        else:
            R.append(B[j]); j += 1
    return R + A[i:] + B[j:], c


def mezcla_optimizada_origen(A, B):
    """Mezcla optimizada. Devuelve (origenes, comparaciones).
    origenes es la salida en posiciones: ('A', i) o ('B', j)."""
    n = len(A)
    R, i, j, c = [], 0, 0, 0
    while n - i >= 2 and j < len(B):      # a A le quedan al menos 2
        c += 1
        if A[i] <= B[j]:
            R.append(("A", i)); i += 1
        else:
            R.append(("B", j)); j += 1
    resto_B = [("B", k) for k in range(j, len(B))]
    resto_A = [("A", k) for k in range(i, n)]   # si queda 1, va al final
    return R + resto_B + resto_A, c


def mezcla_optimizada(A, B):
    """Devuelve (resultado, comparaciones)."""
    origen, c = mezcla_optimizada_origen(A, B)
    return [A[k] if t == "A" else B[k] for t, k in origen], c


# ------------------------------------------------------------------ entradas
def todas_las_entradas(n):
    """Todas las formas de repartir 0..2n-1 en dos listas ordenadas de largo n."""
    for S in combinations(range(2 * n), n):
        A = list(S)
        B = [x for x in range(2 * n) if x not in S]
        yield A, B


def cadena(n):
    """Cadena del adversario: a1 < b1 < a2 < b2 < ... < an < bn."""
    return list(range(0, 2 * n, 2)), list(range(1, 2 * n, 2))


def peor_caso_conocido(n):
    """b1 < a1 < b2 < a2 < ... < bn < an: 2n-2 comparaciones y sale bien."""
    return list(range(1, 2 * n, 2)), list(range(0, 2 * n, 2))


def tabla(cabecera, filas):
    print("| " + " | ".join(cabecera) + " |")
    print("|" + "|".join("---" for _ in cabecera) + "|")
    for f in filas:
        print("| " + " | ".join(str(x) for x in f) + " |")
    print()


# --------------------------------------------------- 1. casos de prueba fijos
def casos_de_prueba():
    casos = [
        ("n = 1, a < b (falla)", [0], [1]),
        ("n = 1, b < a", [1], [0]),
        ("n = 2, cadena (falla)", [0, 2], [1, 3]),
        ("n = 2, máximo en A", [1, 3], [0, 2]),
        ("n = 2, A < B", [0, 1], [2, 3]),
        ("n = 2, B < A", [2, 3], [0, 1]),
        ("n = 5, cadena (falla)", *cadena(5)),
        ("n = 5, peor caso (2n-2)", *peor_caso_conocido(5)),
    ]
    filas = []
    for nombre, A, B in casos:
        esperado = sorted(A + B)
        salida, c = mezcla_optimizada(A, B)
        ok = "sí" if salida == esperado else "**no**"
        filas.append((nombre, A, B, salida, c, ok))
    print("### Casos de prueba\n")
    tabla(["Caso", "A", "B", "Salida", "Comparaciones", "¿Correcta?"], filas)


# ------------------------------------------------------- 2. búsqueda exhaustiva
def exhaustivo(nmax=8):
    filas = []
    for n in range(1, nmax + 1):
        peor, fallos, total = 0, 0, 0
        for A, B in todas_las_entradas(n):
            salida, c = mezcla_optimizada(A, B)
            peor = max(peor, c)
            total += 1
            mal = salida != sorted(A + B)
            fallos += mal
            # falla si y solo si el máximo está en B
            assert mal == (B[-1] > A[-1]), (A, B)
        assert peor == 2 * n - 2, (n, peor)
        filas.append((n, total, peor, 2 * n - 2, fallos,
                      f"{100 * fallos / total:.1f}%"))
    print("### Búsqueda exhaustiva (todas las entradas)\n")
    tabla(["n", "entradas", "peor caso", "2n-2", "entradas que fallan",
           "% que fallan"], filas)


# ---------------------------------------------------------------- 3. la cadena
def prueba_cadena(ns=(2, 3, 4, 5, 8, 16, 64)):
    filas = []
    for n in ns:
        A, B = cadena(n)
        s_opt, c_opt = mezcla_optimizada(A, B)
        s_nor, c_nor = mezcla_normal(A, B)
        assert c_nor == 2 * n - 1 and s_nor == sorted(A + B)
        assert c_opt == 2 * n - 3 and s_opt != sorted(A + B)
        filas.append((n, c_nor, 2 * n - 1, c_opt, 2 * n - 3, "no"))
    print("### Cadena intercalada del adversario\n")
    tabla(["n", "mezcla normal", "2n-1", "optimizada", "2n-3",
           "¿optimizada correcta?"], filas)


# --------------------------------------------------- 4. argumento del intercambio
def prueba_intercambio(ns=(2, 3, 4, 5, 6)):
    """Intercambia los valores de a_n y b_n (par que la optimizada no compara).
    Las dos entradas deben dar la misma salida en posiciones, y exactamente una
    de las dos debe estar mal."""
    filas = []
    for n in ns:
        A, B = cadena(n)
        A2, B2 = A[:], B[:]
        A2[-1], B2[-1] = B[-1], A[-1]          # intercambia a_n y b_n
        assert A2 == sorted(A2) and B2 == sorted(B2)
        o1, c1 = mezcla_optimizada_origen(A, B)
        o2, c2 = mezcla_optimizada_origen(A2, B2)
        assert o1 == o2
        ok1 = mezcla_optimizada(A, B)[0] == sorted(A + B)
        ok2 = mezcla_optimizada(A2, B2)[0] == sorted(A2 + B2)
        assert ok1 != ok2
        filas.append((n, "sí", "no" if not ok1 else "sí",
                      "no" if not ok2 else "sí"))
    print("### Argumento del intercambio (a_n <-> b_n)\n")
    tabla(["n", "misma salida en posiciones", "cadena correcta",
           "intercambiada correcta"],
          [(n, a, "no" if b == "no" else "sí", "sí" if c == "sí" else "no")
           for n, a, b, c in filas])


# ------------------------------------------------------ 5. pruebas aleatorias
def aleatorias(semilla=7):
    random.seed(semilla)
    filas = []
    for n, pruebas in [(5, 20000), (20, 20000), (100, 5000)]:
        fallos = 0
        for _ in range(pruebas):
            valores = random.sample(range(10 * n), 2 * n)
            S = sorted(random.sample(range(2 * n), n))
            val = sorted(valores)
            A = [val[k] for k in S]
            B = [val[k] for k in range(2 * n) if k not in set(S)]
            salida, c = mezcla_optimizada(A, B)
            mal = salida != sorted(A + B)
            assert mal == (B[-1] > A[-1])
            assert c <= 2 * n - 2
            fallos += mal
        filas.append((n, pruebas, f"{100 * fallos / pruebas:.1f}%", "50%"))
    print("### Pruebas aleatorias contra fuerza bruta\n")
    tabla(["n", "pruebas", "fallos", "esperado"], filas)


# ------------------------------------- 6. cota inferior exacta (minimax)
def cota_exacta(nmax=4):
    """Mínimo, sobre todos los algoritmos de comparaciones, del máximo de
    comparaciones necesarias para mezclar dos listas de largo n.
    Estado = conjunto de intercalaciones aún consistentes con las respuestas."""
    filas = []
    for n in range(1, nmax + 1):
        # una intercalación es la tupla de posiciones de a_1..a_n y b_1..b_n
        inter = []
        for S in combinations(range(2 * n), n):
            posA = list(S)
            posB = [x for x in range(2 * n) if x not in S]
            inter.append((tuple(posA), tuple(posB)))

        @lru_cache(maxsize=None)
        def f(estado):
            if len(estado) == 1:
                return 0
            mejor = 10 ** 9
            for i in range(n):
                for j in range(n):
                    menor = frozenset(s for s in estado if s[0][i] < s[1][j])
                    mayor = estado - menor
                    if menor and mayor:
                        mejor = min(mejor, 1 + max(f(menor), f(mayor)))
            return mejor

        v = f(frozenset(inter))
        assert v == 2 * n - 1, (n, v)
        filas.append((n, len(inter), v, 2 * n - 1))
    print("### Cota inferior exacta (minimax sobre todos los algoritmos)\n")
    tabla(["n", "intercalaciones", "mínimo del peor caso", "2n-1"], filas)


if __name__ == "__main__":
    casos_de_prueba()
    exhaustivo()
    prueba_cadena()
    prueba_intercambio()
    aleatorias()
    cota_exacta()
    print("Todas las verificaciones pasaron.")
