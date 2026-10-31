#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejercicio 14 - Casos de prueba
La moneda falsa: partir en tres grupos con la balanza.

Qué se comprueba:
  1. Para n = 1..400 y TODAS las posiciones de la falsa: el algoritmo la
     encuentra, el invariante "la falsa está en [lo, hi)" se vigila en cada
     pesada, los platillos llevan igual cantidad, y el peor caso es
     EXACTAMENTE ceil(log3 n).
  2. La variante con piso (a = floor(m/3)) sigue encontrando la moneda
     pero se pasa de la cota: con n = 8 necesita 3 pesadas (la cota es 2).
     Es "el error que la demostración anuncia".
  3. El óptimo exacto por búsqueda exhaustiva de estrategias coincide con
     ceil(log3 n) para n <= 30 (sin moneda de referencia).
  4. La tabla comparativa: ceil(log3 n) <= ceil(log2 n) <= n/2.

Ejecutar:  python3 prueba_ejercicio_14.py   (tarda unos segundos)
Solo usa la biblioteca estándar.
"""

import math
from functools import lru_cache


def techo_log3(n):
    """Menor k con 3^k >= n."""
    k, p = 0, 1
    while p < n:
        k += 1
        p *= 3
    return k


def techo_log2(n):
    return (n - 1).bit_length() if n > 1 else 0


def buscar_falsa(n, falsa, vigilar=False):
    """Las monedas son 0..n-1 y la falsa (más liviana) es `falsa`.
    Devuelve (moneda encontrada, número de pesadas)."""
    lo, hi, pesadas = 0, n, 0
    while hi - lo > 1:
        m = hi - lo
        a = -(-m // 3)                     # ceil(m / 3)
        izq, der = range(lo, lo + a), range(lo + a, lo + 2 * a)
        if vigilar:
            assert len(izq) == len(der) and 0 <= m - 2 * a <= a
            assert lo <= falsa < hi                          # el invariante
        pesadas += 1
        if falsa in izq:                   # la izquierda pesa menos
            hi = lo + a
        elif falsa in der:                 # la derecha pesa menos
            lo, hi = lo + a, lo + 2 * a
        else:                              # equilibrio: está fuera
            lo = lo + 2 * a
        if vigilar:
            assert lo <= falsa < hi and hi - lo <= a
    return lo, pesadas


def buscar_falsa_piso(n, falsa):
    """Igual, pero con a = floor(m/3): correcta, pero no alcanza la cota."""
    lo, hi, pesadas = 0, n, 0
    while hi - lo > 1:
        m = hi - lo
        a = max(1, m // 3)
        izq, der = range(lo, lo + a), range(lo + a, lo + 2 * a)
        pesadas += 1
        if falsa in izq:
            hi = lo + a
        elif falsa in der:
            lo, hi = lo + a, lo + 2 * a
        else:
            lo = lo + 2 * a
    return lo, pesadas


@lru_cache(maxsize=None)
def optimo(m, g, N):
    """Mínimo de pesadas en el peor caso para localizar la falsa entre m
    candidatas, con g monedas genuinas conocidas (N en total). Prueba TODAS
    las pesadas posibles: x candidatas a la izquierda, y a la derecha,
    completando con genuinas si hace falta."""
    if m <= 1:
        return 0
    mejor = math.inf
    for x in range(1, m):                  # x == m no descarta nada
        for y in range(0, min(x, m - x) + 1):
            if x - y > g:
                continue                   # no alcanzan las genuinas
            resto = m - x - y
            val = 1 + max(optimo(x, N - x, N),
                          optimo(y, N - y, N) if y > 0 else 0,
                          optimo(resto, N - resto, N) if resto > 0 else 0)
            mejor = min(mejor, val)
    return mejor


def main():
    # ------------------------------------------------------------------
    # 1) n = 1..400, todas las posiciones, invariante vigilado
    # ------------------------------------------------------------------
    for n in range(1, 401):
        peor = 0
        for f in range(n):
            enc, p = buscar_falsa(n, f, vigilar=True)
            assert enc == f and p <= techo_log3(n)
            peor = max(peor, p)
        assert peor == techo_log3(n), (n, peor, techo_log3(n))

    # casos chicos de la fórmula
    for n, esperado in [(1, 0), (2, 1), (3, 1), (8, 2), (9, 2), (10, 3), (27, 3), (28, 4)]:
        peor = max((buscar_falsa(n, f)[1] for f in range(n)), default=0)
        assert peor == techo_log3(n) == esperado, (n, peor)

    # ------------------------------------------------------------------
    # 2) La variante con piso: correcta, pero se pasa de la cota
    # ------------------------------------------------------------------
    malas = []
    for n in range(1, 401):
        peor = 0
        for f in range(n):
            enc, p = buscar_falsa_piso(n, f)
            assert enc == f                          # siempre la encuentra
            peor = max(peor, p)
        if peor > techo_log3(n):
            malas.append((n, peor, techo_log3(n)))
    assert len(malas) > 0
    assert (8, 3, 2) in malas[:20]                   # el ejemplo del ejercicio
    assert all(m[1] == m[2] + 1 for m in malas[:50])  # se pasa por poco
    for n in (9, 27, 81):
        assert n not in [m[0] for m in malas]        # con n = 3^k el piso no duele

    # ------------------------------------------------------------------
    # 3) Óptimo exacto por búsqueda exhaustiva (n <= 30)
    # ------------------------------------------------------------------
    for n in range(1, 31):
        assert optimo(n, 0, n) == techo_log3(n), n   # la estrategia óptima

    # ------------------------------------------------------------------
    # 4) La tabla comparativa del ejercicio
    # ------------------------------------------------------------------
    for n in [3, 9, 12, 27, 28, 100, 10**6]:
        assert techo_log3(n) <= techo_log2(n)           # tres grupos <= dos grupos
        assert techo_log3(n) * 2 >= techo_log2(n)       # y solo por la constante: log3 = log2/log2(3)
    assert (techo_log3(3), techo_log2(3)) == (1, 2)     # las dos primeras filas de la tabla
    assert (techo_log3(9), techo_log2(9)) == (2, 4)
    assert (techo_log3(27), techo_log2(27)) == (3, 5)
    assert techo_log3(10**6) == 13 and techo_log2(10**6) == 20

    print("ejercicio 14: todo correcto")
    print("  n = 1..400, todas las posiciones: encontrada siempre, invariante")
    print("  vigilado (platillos iguales, falsa en [lo,hi)), y peor caso = ceil(log3 n) exacto")
    print(f"  variante con piso: correcta pero se pasa de la cota en {len(malas)} valores")
    print(f"  de n <= 400; empieza en {malas[0]}; n = 8: 3 pesadas contra la cota 2")
    print("  óptimo exacto por exhaustiva = ceil(log3 n) para n = 1..30")
    print("  10^6 monedas: 13 pesadas con tres grupos, 20 partiendo en dos")


if __name__ == "__main__":
    main()
