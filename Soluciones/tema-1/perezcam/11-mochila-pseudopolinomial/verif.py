"""Ejercicio 11 - la mochila entera y la pseudopolinomialidad.

Las secciones de este archivo siguen el orden del texto (el ciclo de cinco preguntas de C2 sec. 1).
Los listados de ejercicio-11.tex son literalmente las funciones mochila_dp y mochila_vigilada de este
archivo (el .tex las incluye con \\lstinputlisting, por rango de lineas). Todo lo que se imprime es
ASCII porque el .tex pega la salida tal cual.
"""
import math
import random
import time

import numpy as np


# ------------------------------------------------------------------ el algoritmo del ejercicio
def mochila_dp(pesos, valores, W):
    """dp[j] = mejor valor con capacidad j. Devuelve (valor, celdas actualizadas)."""
    dp = [0] * (W + 1)
    celdas = 0
    for w_i, v_i in zip(pesos, valores):
        for j in range(W, w_i - 1, -1):          # de W hacia abajo: cada objeto una vez
            celdas += 1
            if dp[j - w_i] + v_i > dp[j]:
                dp[j] = dp[j - w_i] + v_i
    return dp[W], celdas
# ---- fin del listado


def mochila_numpy(pesos, valores, W):
    """La misma DP, una fila entera por objeto (solo para medir tiempos con W grande)."""
    dp = np.zeros(W + 1, dtype=np.int64)
    for w_i, v_i in zip(pesos, valores):
        if w_i <= W:
            dp[w_i:] = np.maximum(dp[w_i:], dp[:W + 1 - w_i] + v_i)
    return int(dp[W])


def traza(pesos, valores, W, ascendente=False):
    """dp tras cada objeto (para el ejemplo del texto)."""
    dp = [0] * (W + 1)
    filas = [list(dp)]
    for w_i, v_i in zip(pesos, valores):
        rango = range(w_i, W + 1) if ascendente else range(W, w_i - 1, -1)
        for j in rango:
            if dp[j - w_i] + v_i > dp[j]:
                dp[j] = dp[j - w_i] + v_i
        filas.append(list(dp))
    return filas


def mochila_ascendente(pesos, valores, W):
    """Variante INCORRECTA: ciclo interno ascendente = mochila no acotada (un objeto se puede repetir)."""
    return traza(pesos, valores, W, ascendente=True)[-1][W]


def fuerza_bruta(pesos, valores, W):
    """Devuelve (mejor valor, subconjunto como lista de indices desde 1)."""
    n = len(pesos)
    mejor, quien = 0, []
    for mask in range(1 << n):
        pw = sum(pesos[i] for i in range(n) if mask >> i & 1)
        if pw <= W:
            val = sum(valores[i] for i in range(n) if mask >> i & 1)
            if val > mejor:
                mejor, quien = val, [i + 1 for i in range(n) if mask >> i & 1]
    return mejor, quien


def celdas_formula(pesos, W):
    return sum(W - p + 1 for p in pesos if p <= W)


def tabla_optimos(pesos, valores, W):
    """f[i][c] = mejor valor con los primeros i objetos y capacidad c, enumerando subconjuntos."""
    f = [[0] * (W + 1)]
    subs = [(0, 0)]
    for i in range(1, len(pesos) + 1):
        subs = subs + [(pw + pesos[i - 1], vl + valores[i - 1]) for pw, vl in subs]
        mejor = [0] * (W + 1)
        for pw, vl in subs:
            if pw <= W and vl > mejor[pw]:
                mejor[pw] = vl
        for c in range(1, W + 1):
            mejor[c] = max(mejor[c], mejor[c - 1])
        f.append(mejor)
    return f


# ---- inicio de la version vigilada
def mochila_vigilada(pesos, valores, W, f, ascendente=False):
    """El algoritmo, comprobando los dos invariantes en cada vuelta.
    f[i][c] = optimo de los primeros i objetos con capacidad c.
    Devuelve (vueltas, primer fallo interno, rondas con fallo externo)."""
    dp = [0] * (W + 1)
    vueltas, primer, fallos_ext = 0, None, 0
    for i, (w_i, v_i) in enumerate(zip(pesos, valores), start=1):
        rango = range(w_i, W + 1) if ascendente else range(W, w_i - 1, -1)
        tocadas = set()
        for j in rango:
            if dp[j - w_i] + v_i > dp[j]:
                dp[j] = dp[j - w_i] + v_i
            tocadas.add(j)
            vueltas += 1
            # invariante interno: celdas tocadas = f(i, .), las demas = f(i-1, .)
            esperado = [f[i][c] if c in tocadas else f[i - 1][c] for c in range(W + 1)]
            if primer is None and dp != esperado:
                primer = (i, j)
        if dp != f[i]:                       # invariante externo: dp = f(i, .)
            fallos_ext += 1
    return vueltas, primer, fallos_ext
# ---- fin de la version vigilada


def mochila_no_acotada(pesos, valores, W):
    """Oraculo independiente de la variante ascendente: cada objeto se puede llevar varias veces."""
    g = [0] * (W + 1)
    for w_i, v_i in zip(pesos, valores):
        for c in range(w_i, W + 1):
            g[c] = max(g[c], g[c - w_i] + v_i)
    return g[W]


def tamano_bits(pesos, valores, W):
    """Tamano de la entrada: los bits de cada numero (bit_length es exacto para enteros grandes)."""
    return sum(p.bit_length() for p in pesos) + sum(v.bit_length() for v in valores) + W.bit_length()


# ================================================================== 1. el ejemplo que atraviesa el ejercicio
print("== 1. el ejemplo que usamos en todo el ejercicio ==")
EP, EV, EW = [2, 3, 4, 5], [3, 4, 5, 6], 8
print("objetos (peso, valor): " + "  ".join(f"({p},{v})" for p, v in zip(EP, EV)) + f"   capacidad W = {EW}")
mejor, quien = fuerza_bruta(EP, EV, EW)
print(f"fuerza bruta (2^4 = 16 subconjuntos): mejor valor {mejor}, con los objetos {quien}")
print("dp[j] para j = 0..8, tras cada objeto (ciclo interno descendente):")
filas = traza(EP, EV, EW)
for i, fila in enumerate(filas):
    etiqueta = "inicio" if i == 0 else f"objeto {i} ({EP[i - 1]},{EV[i - 1]})"
    print(f"  {etiqueta:<14} " + " ".join(f"{x:>2}" for x in fila))
print(f"resultado: dp[8] = {filas[-1][EW]}  (celdas actualizadas: {mochila_dp(EP, EV, EW)[1]})")

# ================================================================== 2. correctitud
print()
print("== 2. correctitud ==")
random.seed(1)
inst = []
for _ in range(2000):
    n = random.randint(1, 9)
    inst.append(([random.randint(1, 12) for _ in range(n)], [random.randint(1, 20) for _ in range(n)], random.randint(0, 40)))
mal = sum(mochila_dp(p, v, W)[0] != fuerza_bruta(p, v, W)[0] for p, v, W in inst)
print(f"ciclo descendente contra fuerza bruta: 2000 instancias, fallos (deberia ser 0): {mal}")
mal = sum(mochila_numpy(p, v, W) != mochila_dp(p, v, W)[0] for p, v, W in inst)
print(f"numpy contra ciclo descendente: 2000 instancias, fallos (deberia ser 0): {mal}")
ok = sum(mochila_dp(p, v, W)[1] == celdas_formula(p, W) for p, v, W in inst)
print(f"celdas actualizadas = suma de (W - w_i + 1): coincide en {ok} de 2000 instancias")
distinto = sum(mochila_ascendente(p, v, W) != fuerza_bruta(p, v, W)[0] for p, v, W in inst)
print(f"ciclo ASCENDENTE: resultado distinto del correcto en {distinto} de 2000 instancias")
print(f"ejemplo: el ascendente da dp[8] = {mochila_ascendente(EP, EV, EW)} (4 copias del objeto 1); el correcto, {mejor}")
tablas = [tabla_optimos(p, v, W) for p, v, W in inst]
vueltas = rondas = viol = 0
for (p, v, W), f in zip(inst, tablas):
    vu, primer, ext = mochila_vigilada(p, v, W, f)
    vueltas += vu; rondas += len(p); viol += (primer is not None) + ext
print(f"invariantes ejecutados (ciclo descendente): {vueltas} vueltas, {rondas} rondas")
print(f"   violaciones de algun invariante (deberia ser 0): {viol}")
fallan = tarde = 0
for (p, v, W), f in zip(inst, tablas):
    vu, primer, ext = mochila_vigilada(p, v, W, f, ascendente=True)
    if primer is not None:
        fallan += 1
        tarde += primer[1] >= 2 * p[primer[0] - 1]
print(f"ciclo ascendente: el invariante interno falla en {fallan} de 2000 instancias")
print(f"   y el primer fallo ocurre en j >= 2*w_i en {tarde} de {fallan}")
iguales = sum(mochila_ascendente(p, v, W) == mochila_no_acotada(p, v, W) for p, v, W in inst)
print(f"ciclo ascendente = mochila no acotada: coincide en {iguales} de 2000 instancias")
fE = tabla_optimos(EP, EV, EW)
filaA = traza(EP, EV, EW, ascendente=True)[1]
_, primerE, _ = mochila_vigilada(EP, EV, EW, fE, ascendente=True)
print("ejemplo, ciclo ascendente, tras el objeto 1: dp = " + " ".join(str(x) for x in filaA))
print(f"   primer fallo del invariante: objeto {primerE[0]}, j = {primerE[1]} (dp[{primerE[1]}] = {filaA[primerE[1]]}, pero f({primerE[0]},{primerE[1]}) = {fE[primerE[0]][primerE[1]]})")

# ------------------------------------------------------------------ la familia de instancias para medir
# n = 40, pesos ~ U[1, W/2] (el tamano de la entrada crece con b), valores ~ U[1, 1000]
random.seed(5)
N40 = 40
familia = []
for bits in range(12, 25):
    W = 2 ** bits
    familia.append((bits, W, [random.randint(1, W // 2) for _ in range(N40)], [random.randint(1, 1000) for _ in range(N40)]))

# ================================================================== 3. costo: lineal en n
print()
print("== 3. costo: W = 2^16 fijo, n creciendo ==")
print(f"{'n':>6} {'celdas':>13} {'tiempo (s)':>11} {'tiempo/n (ms)':>14}")
random.seed(7)
for n2 in [50, 100, 200, 400, 800, 1600]:
    W = 2 ** 16
    ps = [random.randint(1, W // 2) for _ in range(n2)]
    vs = [random.randint(1, 1000) for _ in range(n2)]
    t0 = time.perf_counter(); mochila_numpy(ps, vs, W); t = time.perf_counter() - t0
    print(f"{n2:>6} {celdas_formula(ps, W):>13,} {t:>11.4f} {1000 * t / n2:>14.4f}")

# ================================================================== 4. costo: lineal en el valor de W
print()
print("== 4. costo: n = 40 fijo, el VALOR de W creciendo ==")
print(f"{'W':>10} {'celdas':>13} {'celdas/(n*W)':>13}")
for bits, W, ps, vs in familia:
    c = celdas_formula(ps, W)
    print(f"{W:>10} {c:>13,} {c / (N40 * W):>13.3f}")

# ================================================================== 5. los mismos datos, leidos en bits
print()
print("== 5. los mismos 13 puntos, leidos en bits: el tamano de la entrada crece con b ==")
print(f"{'bits':>4} {'tam. entrada':>12} {'celdas':>13} {'log2 celdas':>11} {'celdas/ant.':>11} {'tiempo (s)':>10} {'t/ant.':>6}")
prev_c = prev_t = None
for bits, W, ps, vs in familia:
    t0 = time.perf_counter(); mochila_numpy(ps, vs, W); t = time.perf_counter() - t0
    c = celdas_formula(ps, W)
    print(f"{bits:>4} {tamano_bits(ps, vs, W):>12} {c:>13,} {math.log2(c):>11.2f} "
          f"{(c / prev_c if prev_c else float('nan')):>11.2f} {t:>10.4f} {(t / prev_t if prev_t else float('nan')):>6.2f}")
    prev_c, prev_t = c, t

# ================================================================== 6. la trampa: instancias que se vuelven triviales
print()
print("== 6. por que los pesos crecen con W: si W >= suma de pesos, la respuesta es 'llevarse todo' ==")
random.seed(0)
n = 40
ps = [random.randint(1, 1000) for _ in range(n)]
vs = [random.randint(1, 1000) for _ in range(n)]
print(f"n=40, pesos <= 1000: suma de pesos = {sum(ps)}, suma de valores = {sum(vs)}")
for bits in (12, 14, 15, 16, 20):
    W = 2 ** bits
    r = mochila_numpy(ps, vs, W)
    print(f"   W = 2^{bits:<2}: mejor valor = {r:>6}  {'(= suma de valores: instancia trivial)' if r == sum(vs) else '(instancia no trivial)'}")
random.seed(11)
fallos = 0
for _ in range(500):
    n3 = random.randint(1, 8)
    p3 = [random.randint(1, 30) for _ in range(n3)]
    v3 = [random.randint(1, 30) for _ in range(n3)]
    W = random.randint(0, 400)
    if mochila_dp(p3, v3, W)[0] != mochila_dp(p3, v3, min(W, sum(p3)))[0]:
        fallos += 1
print(f"recortar W a min(W, suma de pesos): 500 instancias, fallos (deberia ser 0): {fallos}")

# ================================================================== 7. de la medicion a la demostracion
print()
print("== 7. una instancia minima: n = 1, w = 1, v = 1, capacidad W = 2^b ==")
print(f"{'b':>4} {'W':>10} {'tamano de la entrada (bits)':>28} {'celdas actualizadas':>20}")
for b in (4, 8, 12, 16, 20):
    W = 2 ** b
    _, celdas = mochila_dp([1], [1], W)
    print(f"{b:>4} {W:>10} {tamano_bits([1], [1], W):>28} {celdas:>20}")
print()
print("el tamano s desde el cual 2^(s-3) supera al polinomio s^k:")
for k in (1, 2, 3, 5, 10):
    s = 4
    while 2 ** (s - 3) <= s ** k:
        s += 1
    print(f"   k = {k:>2}: desde s = {s:>3} bits   (2^{s - 3} = {2 ** (s - 3):.3g} > {s}^{k} = {s ** k:.3g})")

# ================================================================== 8. memoria y tiempo, al estilo de C1 sec. 6, 7 y 8
print()
print("== 8. memoria y tiempo: n = 40, 10^9 celdas por segundo, 8 bytes por celda ==")
print(f"{'b':>4} {'celdas':>10} {'memoria':>10} {'tiempo':>12}")
anio = 3600 * 24 * 365
unidades = [("B", 1), ("KB", 1e3), ("MB", 1e6), ("GB", 1e9), ("TB", 1e12), ("PB", 1e15), ("EB", 1e18)]
for b in (20, 32, 40, 64, 128):
    cells = 40 * 2 ** b
    mem = 8 * 2 ** b
    seg = cells / 1e9
    tiempo = (f"{seg:.3g} s" if seg < 60 else f"{seg / 60:.3g} min" if seg < 3600 else f"{seg / 3600:.3g} h" if seg < 86400
              else f"{seg / 86400:.3g} dias" if seg < anio else f"{seg / anio:.3g} anios")
    u, d = [x for x in unidades if mem >= x[1]][-1]
    print(f"{b:>4} {cells:>10.3g} {mem / d:>7.3g} {u:>2} {tiempo:>12}")
hora = 3600 * 10 ** 9
for k in (1, 1000):
    bmax = int(math.log2(hora * k / 40))
    mem = 8 * 2 ** bmax
    u, d = [x for x in unidades if mem >= x[1]][-1]
    print(f"1 hora, {k}x mas rapida: 40*2^b <= {hora * k:.3g} -> b = {bmax}, tabla {mem / d:.3g} {u}")

# ================================================================== 9. la quinta pregunta: el paralelo con la primalidad
print()
print("== 9. cuantos bits mas resuelve una computadora k veces mas rapida (C1 sec. 7) ==")
print(f"{'k':>6} {'primalidad (2^(b/2))':>22} {'mochila (n*2^b)':>17}")
for k in (10, 100, 1000):
    print(f"{k:>6} {2 * math.log2(k):>22.1f} {math.log2(k):>17.1f}")

# ================================================================== 10. contar bits: floats contra enteros
print()
print("== 10. contar los bits de W: math.log2 con floats contra bit_length exacto ==")
for b in (40, 52, 60, 100):
    W = 2 ** b
    print(f"W = 2^{b:<3}: ceil(log2(W + 1)) = {math.ceil(math.log2(W + 1)):>3}   W.bit_length() = {W.bit_length():>3}")
primero = next(b for b in range(1, 200) if math.ceil(math.log2(2 ** b + 1)) != (2 ** b).bit_length())
print(f"primer b con W = 2^b en que los floats fallan: b = {primero}")
