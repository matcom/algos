#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejercicio 5 - Casos de prueba
Detección de ciclos con dos punteros (algoritmo de Floyd).

Qué se comprueba:
  1. Con ciclo: para TODAS las formas (mu, lam) con 0 <= mu <= 40 y
     1 <= lam <= 40, el número de iteraciones es exactamente
     t* = lam * max(1, ceil(mu/lam)), y se cumple n/2 <= t* <= n.
  2. Sin ciclo: iteraciones = piso(n/2) para n = 0..200.
  3. El invariante I(t): lento = v_t y rapido = v_2t, vigilado en cada
     guarda sobre 256 listas chicas (incluye la vacía y el autolazo).
  4. Las dos variantes con error plantado de la sección 10:
     A (guarda incompleta) revienta en listas impares sin ciclo,
     B (comparar antes de mover) da falsos positivos en toda lista no vacía.

Ejecutar:  python3 prueba_ejercicio_05.py
Solo usa la biblioteca estándar.
"""

from math import ceil


class Nodo:
    __slots__ = ("next",)

    def __init__(self):
        self.next = None


def construir(mu, lam):
    """lam = 0: lista sin ciclo de mu nodos. lam >= 1: cola de mu + ciclo de lam."""
    nodos = [Nodo() for _ in range(mu + lam)]
    for a, b in zip(nodos, nodos[1:]):
        a.next = b
    if lam > 0:
        nodos[-1].next = nodos[mu]
    return nodos


def floyd(head):
    """Devuelve (hay_ciclo, iteraciones)."""
    lento = rapido = head
    t = 0
    while rapido is not None and rapido.next is not None:
        lento = lento.next
        rapido = rapido.next.next
        t += 1
        if lento is rapido:
            return True, t
    return False, t


def v(head, i):
    """El i-ésimo elemento v_i de la sucesión (None si la lista terminó antes)."""
    x = head
    for _ in range(i):
        if x is None:
            return None
        x = x.next
    return x


def floyd_vigilado(head):
    """Floyd, pero comprueba I(t) en cada guarda: lento = v_t y rapido = v_2t."""
    lento = rapido = head
    t = 0
    while True:
        assert lento is v(head, t) and rapido is v(head, 2 * t), f"I({t}) roto"
        if not (rapido is not None and rapido.next is not None):
            return False, t
        lento, rapido = lento.next, rapido.next.next
        t += 1
        if lento is rapido:
            return True, t


def t_estrella(mu, lam):
    return lam * max(1, ceil(mu / lam))


def main():
    # ------------------------------------------------------------------
    # 1) Con ciclo: todas las formas (mu, lam)
    # ------------------------------------------------------------------
    con_ciclo = 0
    for mu in range(41):
        for lam in range(1, 41):
            n, ts = mu + lam, t_estrella(mu, lam)
            assert floyd(construir(mu, lam)[0]) == (True, ts), (mu, lam)
            assert n / 2 <= ts <= n, (mu, lam, ts, n)
            if mu == 0:
                assert ts == n
            else:
                assert ts <= n - 1
            con_ciclo += 1

    # los ejemplos de la tabla del ejercicio
    for (mu, lam), ts_tabla in [((0, 7), 7), ((5, 3), 6), ((12, 5), 15),
                                ((10, 1), 10), ((1, 100), 100)]:
        assert t_estrella(mu, lam) == ts_tabla
        assert floyd(construir(mu, lam)[0]) == (True, ts_tabla)

    # ------------------------------------------------------------------
    # 2) Sin ciclo: iteraciones = piso(n/2)
    # ------------------------------------------------------------------
    for n in range(201):
        nodos = construir(n, 0)
        assert floyd(nodos[0] if nodos else None) == (False, n // 2), n

    # ------------------------------------------------------------------
    # 3) Invariante I(t) vigilado (256 listas chicas, incluye casos borde)
    # ------------------------------------------------------------------
    for mu in range(16):
        for lam in range(16):
            nodos = construir(mu, lam)
            head = nodos[0] if nodos else None
            assert floyd_vigilado(head)[0] == (lam > 0), (mu, lam)

    # ------------------------------------------------------------------
    # 4) Las dos variantes con error plantado
    # ------------------------------------------------------------------
    # Variante A: la guarda es solo "rapido is not None".
    # En listas sin ciclo de longitud impar, rapido.next.next revienta.
    def floyd_A(head):
        lento = rapido = head
        while rapido is not None:                 # <-- le falta el .next
            lento = lento.next
            rapido = rapido.next.next
            if lento is rapido:
                return True
        return False

    revienta = 0
    for n in range(1, 200):
        nodos = construir(n, 0)
        head = nodos[0]
        try:
            floyd_A(head)
            assert n % 2 == 0, ("debería reventar con n impar", n)
        except AttributeError:
            revienta += 1
            assert n % 2 == 1, ("no debería reventar con n par", n)
    assert revienta == 100                        # exactamente los n impares

    # Variante B: comparar ANTES de mover. Falso positivo en toda lista con >= 2 nodos.
    def floyd_B(head):
        lento = rapido = head
        while rapido is not None and rapido.next is not None:
            if lento is rapido:                   # <-- comparación adelantada
                return True
            lento = lento.next
            rapido = rapido.next.next
        return False

    falsos = 0
    for n in range(0, 200):
        nodos = construir(n, 0)
        if floyd_B(nodos[0] if nodos else None):
            falsos += 1
            assert n >= 2                         # solo pasan la vacía y la de 1 nodo
    assert falsos == 198                          # exactamente n = 2..199

    print("ejercicio 5: todo correcto")
    print(f"  con ciclo: {con_ciclo} formas (mu, lam), iteraciones = t* = lam*max(1, ceil(mu/lam))")
    print("  sin ciclo: 201 longitudes, iteraciones = piso(n/2)")
    print("  invariante I(t) vigilado en 256 listas: nunca se rompe")
    print(f"  variante A (guarda incompleta): revienta en las {revienta} listas impares")
    print(f"  variante B (comparar antes de mover): {falsos} falsos positivos (todo n >= 2)")


if __name__ == "__main__":
    main()
