#!/usr/bin/env python3
"""
verificar_ejercicio_05.py

Detección de ciclos de Floyd (punteros a velocidad 1 y 2).

Modelo: lista enlazada con nodos 0..n-1; sig[v] es el siguiente de v o None.
cabeza es un nodo o None (lista vacía). Costo: vueltas del while.
Solo Python 3, sin dependencias externas.

Qué verifica:
  1. Casos de prueba fijos.
  2. El invariante I(t) y el potencial N - t, ejecutables, sobre todas las
     entradas pequeñas (versión instrumentada).
  3. Vueltas observadas = fórmula exacta: m // 2 (sin ciclo) y
     lam * ceil(max(mu, 1) / lam) (con ciclo), en todas las formas rho.
  4. Peor caso por número de nodos.
  5. Búsqueda exhaustiva (todas las listas con n <= 6 nodos) contra fuerza bruta.
  6. Pruebas aleatorias contra fuerza bruta, con dos generadores.
"""
import random
from itertools import product


# ---------------------------------------------------------------- algoritmo
def floyd(sig, cabeza):
    """Devuelve (hay_ciclo, vueltas)."""
    lento = cabeza
    rapido = cabeza
    vueltas = 0
    while rapido is not None and sig[rapido] is not None:
        lento = sig[lento]
        rapido = sig[sig[rapido]]
        vueltas += 1
        if lento == rapido:
            return True, vueltas
    return False, vueltas


# ------------------------------------------------------------ modelo / oráculo
def x(sig, cabeza, k):
    """x_k: k pasos desde la cabeza; None se queda en None."""
    v = cabeza
    for _ in range(k):
        if v is None:
            return None
        v = sig[v]
    return v


def forma(sig, cabeza):
    """('aciclica', m, None, N) o ('ciclica', mu, lam, N), N = nodos distintos."""
    vistos, k, v = {}, 0, cabeza
    while v is not None and v not in vistos:
        vistos[v] = k
        v = sig[v]
        k += 1
    if v is None:
        return ("aciclica", k, None, k)
    mu = vistos[v]
    return ("ciclica", mu, k - mu, k)


def hay_ciclo_fuerza_bruta(sig, cabeza):
    vistos, v = set(), cabeza
    while v is not None:
        if v in vistos:
            return True
        vistos.add(v)
        v = sig[v]
    return False


def vueltas_formula(f):
    if f[0] == "aciclica":
        return f[1] // 2
    _, mu, lam, _ = f
    return lam * (-(-max(mu, 1) // lam))


# ------------------------------------------- versión instrumentada (invariante)
def floyd_instrumentado(sig, cabeza):
    """Misma lógica que floyd, con asserts del invariante I(t) y del potencial.
    t es una variable fantasma: número de vueltas completadas."""
    f = forma(sig, cabeza)
    ciclica, N = f[0] == "ciclica", f[3]
    lento = rapido = cabeza
    t = 0
    while True:
        # Invariante I(t), con 0 <= t:
        assert lento == x(sig, cabeza, t)
        assert rapido == x(sig, cabeza, 2 * t)
        for s in range(1, t + 1):
            assert x(sig, cabeza, s) is not None
            assert x(sig, cabeza, s) != x(sig, cabeza, 2 * s)
        if not (rapido is not None and sig[rapido] is not None):
            assert not ciclica            # corolario: false => sin ciclo
            return False, t
        assert N - t >= 1                 # potencial positivo al entrar
        phi_antes = N - t
        lento = sig[lento]
        rapido = sig[sig[rapido]]
        t += 1
        assert N - t == phi_antes - 1     # el potencial baja en 1
        if lento == rapido:
            assert x(sig, cabeza, t) is not None
            assert x(sig, cabeza, t) == x(sig, cabeza, 2 * t)
            assert ciclica                # corolario: true => hay ciclo
            return True, t


# --------------------------------------------------------------- constructores
def lineal(m):
    sig = [i + 1 for i in range(m - 1)] + [None] if m > 0 else []
    return sig, (0 if m > 0 else None)


def rho(mu, lam):
    n = mu + lam
    sig = [i + 1 for i in range(n - 1)] + [mu]
    return sig, 0


def mostrar(sig, cabeza):
    if cabeza is None:
        return "null"
    partes, vistos, v = [], set(), cabeza
    while v is not None and v not in vistos:
        partes.append(str(v)); vistos.add(v); v = sig[v]
    partes.append("null" if v is None else str(v))
    return "→".join(partes)


def tabla(cabecera, filas):
    print("| " + " | ".join(cabecera) + " |")
    print("|" + "|".join("---" for _ in cabecera) + "|")
    for f in filas:
        print("| " + " | ".join(str(c) for c in f) + " |")
    print()


# ------------------------------------------------------ 1. casos de prueba fijos
def casos_de_prueba():
    casos = [
        ("lista vacía", *lineal(0)),
        ("1 nodo, sin ciclo", *lineal(1)),
        ("1 nodo, se apunta a sí mismo", *rho(0, 1)),
        ("2 nodos, sin ciclo", *lineal(2)),
        ("2 nodos, ciclo de 2", *rho(0, 2)),
        ("5 nodos, sin ciclo", *lineal(5)),
        ("cola 3, ciclo 4", *rho(3, 4)),
        ("cola 5, ciclo 1", *rho(5, 1)),
        ("cola 1, ciclo 2", *rho(1, 2)),
        ("ciclo puro de 6", *rho(0, 6)),
    ]
    filas = []
    for nombre, sig, cab in casos:
        res, v = floyd(sig, cab)
        esperado = hay_ciclo_fuerza_bruta(sig, cab)
        f = forma(sig, cab)
        assert res == esperado and v == vueltas_formula(f)
        assert floyd_instrumentado(sig, cab) == (res, v)
        filas.append((nombre, f"`{mostrar(sig, cab)}`",
                      "sí" if esperado else "no",
                      "true" if res else "false", v, vueltas_formula(f)))
    print("### Casos de prueba\n")
    tabla(["Caso", "Lista", "¿ciclo?", "Devuelve", "Vueltas",
           "Fórmula"], filas)


def traza(mu, lam):
    sig, cab = rho(mu, lam)
    filas, lento, rapido, t = [], cab, cab, 0
    filas.append((0, lento, rapido, "—"))
    while rapido is not None and sig[rapido] is not None:
        lento = sig[lento]; rapido = sig[sig[rapido]]; t += 1
        filas.append((t, lento, rapido, "sí" if lento == rapido else "no"))
        if lento == rapido:
            break
    print(f"### Traza sobre `{mostrar(sig, cab)}` (cola {mu}, ciclo {lam})\n")
    tabla(["t", "lento = x_t", "rapido = x_2t", "¿lento == rapido?"], filas)


# ---------------------------------------------- 2/3. fórmulas por todas las formas
def formulas(nmax=40):
    for m in range(0, nmax + 1):
        sig, cab = lineal(m)
        assert floyd(sig, cab) == (False, m // 2)
        assert floyd_instrumentado(sig, cab) == (False, m // 2)
    cuenta = 0
    for mu in range(0, nmax + 1):
        for lam in range(1, nmax + 1):
            sig, cab = rho(mu, lam)
            res, v = floyd(sig, cab)
            assert res is True
            assert v == lam * (-(-max(mu, 1) // lam))
            assert max(mu, 1) <= v <= mu + lam      # t* <= mu + lam
            if mu + lam <= 25:
                assert floyd_instrumentado(sig, cab) == (res, v)
            cuenta += 1
    return cuenta


def peor_caso(nmax=12):
    filas = []
    for n in range(1, nmax + 1):
        mejor, forma_mejor = n // 2, "sin ciclo"
        for mu in range(0, n):
            lam = n - mu
            v = floyd(*rho(mu, lam))[1]
            assert v <= n
            if v > mejor:
                mejor, forma_mejor = v, f"cola {mu}, ciclo {lam}"
        assert mejor == n and forma_mejor == f"cola 0, ciclo {n}"
        filas.append((n, n // 2, mejor, forma_mejor))
    print("### Peor caso con N nodos alcanzables\n")
    tabla(["N", "peor sin ciclo (N // 2)", "peor en total",
           "forma del peor caso"], filas)


# ------------------------------------------------------ 4. búsqueda exhaustiva
def exhaustivo(nmax=6, instr_max=5):
    filas = []
    for n in range(1, nmax + 1):
        total = con = 0
        for sig in product([None] + list(range(n)), repeat=n):
            sig = list(sig)
            for cab in [None] + list(range(n)):
                res, v = floyd(sig, cab)
                esperado = hay_ciclo_fuerza_bruta(sig, cab)
                assert res == esperado
                assert v == vueltas_formula(forma(sig, cab))
                if n <= instr_max:
                    assert floyd_instrumentado(sig, cab) == (res, v)
                total += 1
                con += esperado
        filas.append((n, total, con, total - con, 0))
    print("### Búsqueda exhaustiva (todas las listas con n nodos)\n")
    tabla(["n", "entradas", "con ciclo", "sin ciclo", "errores"], filas)


# -------------------------------------------------------- 5. pruebas aleatorias
def relabel(sig, cab, rng):
    n = len(sig)
    p = list(range(n)); rng.shuffle(p)
    nuevo = [None] * n
    for v in range(n):
        nuevo[p[v]] = None if sig[v] is None else p[sig[v]]
    return nuevo, (None if cab is None else p[cab])


def aleatorias(semilla=5):
    rng = random.Random(semilla)
    filas = []
    for n, pruebas in [(10, 5000), (50, 5000), (300, 2000)]:
        for gen in ("formas rho", "función al azar"):
            con = 0
            for _ in range(pruebas):
                if gen == "formas rho":
                    if rng.random() < 0.5:
                        sig, cab = lineal(rng.randint(0, n))
                    else:
                        lam = rng.randint(1, n)
                        sig, cab = rho(rng.randint(0, n - lam), lam)
                    sig, cab = relabel(sig, cab, rng)
                else:
                    sig = [None if rng.random() < 1.0 / n else rng.randrange(n)
                           for _ in range(n)]
                    cab = rng.randrange(n)
                res, v = floyd(sig, cab)
                esperado = hay_ciclo_fuerza_bruta(sig, cab)
                assert res == esperado
                assert v == vueltas_formula(forma(sig, cab))
                con += esperado
            filas.append((n, gen, pruebas, f"{100 * con / pruebas:.0f}%", 0))
    print("### Pruebas aleatorias contra fuerza bruta\n")
    tabla(["n", "generador", "pruebas", "con ciclo", "errores"], filas)


if __name__ == "__main__":
    casos_de_prueba()
    traza(3, 4)
    n_formas = formulas()
    print(f"Fórmulas de vueltas comprobadas en {n_formas} formas rho "
          f"y en 41 listas sin ciclo.\n")
    peor_caso()
    exhaustivo()
    aleatorias()
    print("Todas las verificaciones pasaron.")
