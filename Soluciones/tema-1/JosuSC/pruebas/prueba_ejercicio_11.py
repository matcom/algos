#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejercicio 11 - Casos de prueba
La mochila entera por programación dinámica: ¿es polinomial?

Qué se comprueba:
  1. Correctitud contra fuerza bruta (2500 instancias aleatorias) y la
     fórmula exacta de iteraciones: sum_i max(0, W - w_i + 1).
  2. La familia I_b del Teorema 1: tamaño en bits l(I_b) = b + 6 y
     costo 2(2^b - 1): el tamaño crece lineal, el costo exponencial.
  3. Que cada bit de W DUPLICA el costo de la mochila (razón entre
     consecutivos = 2) y que cada bit de N multiplica el costo de la
     primalidad por sqrt(2) (razón entre b y b+2 = 2): las dos curvas
     exponenciales del ejercicio, solo que de base distinta.

Ejecutar:  python3 prueba_ejercicio_11.py
Solo usa la biblioteca estándar.
"""

import random
from math import isqrt


def mochila(pesos, valores, W, contar=False):
    dp = [0] * (W + 1)
    it = 0
    for w, v in zip(pesos, valores):
        for c in range(W, w - 1, -1):
            if dp[c - w] + v > dp[c]:
                dp[c] = dp[c - w] + v
            it += 1
    return (dp[W], it) if contar else dp[W]


def fuerza_bruta(pesos, valores, W):
    n = len(pesos)
    best = 0
    for mask in range(1 << n):
        pw = sum(pesos[i] for i in range(n) if mask >> i & 1)
        if pw <= W:
            best = max(best, sum(valores[i] for i in range(n) if mask >> i & 1))
    return best


def bits(m):
    return m.bit_length()


def es_primo_mr(n):
    """Miller-Rabin determinista (solo para elegir primos de prueba)."""
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def primo_bajo(b):
    """El mayor primo menor que 2^b."""
    n = 2**b - 1
    while not es_primo_mr(n):
        n -= 2
    return n


def primo_por_division(N):
    d, cnt = 2, 0
    while d * d <= N:
        cnt += 1
        if N % d == 0:
            return False, cnt
        d += 1
    return True, cnt


def main():
    # ------------------------------------------------------------------
    # 1) Correctitud y conteo exacto de iteraciones
    # ------------------------------------------------------------------
    random.seed(3)
    casos = 0
    for _ in range(2500):
        n = random.randint(1, 8)
        W = random.randint(0, 40)
        pesos = [random.randint(1, 45) for _ in range(n)]
        valores = [random.randint(0, 30) for _ in range(n)]
        v, it = mochila(pesos, valores, W, True)
        assert v == fuerza_bruta(pesos, valores, W)
        assert it == sum(max(0, W - w + 1) for w in pesos)   # la fórmula de 2.3
        casos += 1

    # ------------------------------------------------------------------
    # 2) La familia I_b: tamaño lineal en bits, costo exponencial
    # ------------------------------------------------------------------
    iteraciones = {}
    for b in range(1, 17):
        W = 2**b - 1
        v, it = mochila([1, 1], [1, 1], W, True)
        l = bits(2) + bits(W) + 4 * bits(1)
        assert l == b + 6, (b, l)                    # tamaño en bits: lineal
        assert it == 2 * (2**b - 1), (b, it)         # costo: exponencial
        assert v == min(2, W)
        iteraciones[b] = it
    for b in range(8, 16):                            # cada bit duplica
        r = iteraciones[b + 1] / iteraciones[b]
        assert 1.9 < r < 2.1, (b, r)

    # ------------------------------------------------------------------
    # 3) Primalidad por división: cada DOS bits duplica (x sqrt(2) por bit)
    # ------------------------------------------------------------------
    cuentas = {}
    for b in range(10, 35, 2):
        N = primo_bajo(b)
        ok, cnt = primo_por_division(N)
        assert ok and es_primo_mr(N)
        assert cnt == isqrt(N) - 1, (b, cnt, isqrt(N))   # prueba todos los d <= sqrt(N)
        assert abs(cnt - 2**(b / 2)) < 2**(b / 2) / 8    # y eso es ~2^(b/2)
        cuentas[b] = cnt
    for b in range(10, 33, 2):
        r = cuentas[b + 2] / cuentas[b]
        assert 1.85 < r < 2.15, (b, r)                   # dos bits: factor 2

    print("ejercicio 11: todo correcto")
    print(f"  {casos} instancias contra fuerza bruta; iteraciones = sum max(0, W-w_i+1) exactas")
    print("  familia I_b: l(I_b) = b+6 bits, costo = 2(2^b - 1): lineal vs exponencial")
    print("  mochila: cada bit de W multiplica el costo por 2 (b = 1..16)")
    print("  primalidad: cada dos bits de N lo multiplican por 2 (x sqrt(2) por bit)")
    print(f"    ejemplo: b = 30 -> N = {primo_bajo(30):,} necesita {cuentas[30]:,} divisiones")


if __name__ == "__main__":
    main()
