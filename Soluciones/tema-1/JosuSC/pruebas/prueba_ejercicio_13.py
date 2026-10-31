#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejercicio 13 - Casos de prueba
Splay tree: camino inicial y accesos ordenados 1..n (tres rondas).

Qué se comprueba (midiendo rotaciones una por una):
  1. El primer acceso splay(1) sobre el camino cuesta exactamente n-1
     rotaciones (todo zig-zig), y deja el árbol reorganizado.
  2. El potencial inicial es exactamente log2(n!) = sum log2 k.
  3. La cota del lema de acceso se cumple: el total de las 3n accesiones
     no pasa de 3n(3 log2 n + 1) + log2(n!).
  4. Pero el costo MEDIDO por acceso es constante (~4), mientras que
     subir a la raíz cuesta ~n/2 por acceso: la cota del lema no es
     ajustada para esta secuencia.
  5. El árbol sigue siendo un BST válido después de cada ronda.

Ejecutar:  python3 prueba_ejercicio_13.py   (tarda unos segundos)
Solo usa la biblioteca estándar.
"""

import math


class Nodo:
    __slots__ = ("val", "l", "r")

    def __init__(self, val):
        self.val, self.l, self.r = val, None, None


def rot_der(p):
    q = p.l
    p.l = q.r
    q.r = p
    return q


def rot_izq(p):
    q = p.r
    p.r = q.l
    q.l = p
    return q


def splay(raiz, x, cont):
    """Splay bottom-up estándar. cont[0] cuenta las rotaciones."""
    if raiz is None or raiz.val == x:
        return raiz
    if x < raiz.val:
        if raiz.l is None:
            return raiz
        if x < raiz.l.val:                       # zig-zig
            raiz.l.l = splay(raiz.l.l, x, cont)
            raiz = rot_der(raiz); cont[0] += 1   # primero el padre...
            raiz = rot_der(raiz); cont[0] += 1   # ...después x
        elif x > raiz.l.val:                     # zig-zag
            raiz.l.r = splay(raiz.l.r, x, cont)
            raiz.l = rot_izq(raiz.l); cont[0] += 1
            raiz = rot_der(raiz); cont[0] += 1
        else:                                    # zig
            raiz = rot_der(raiz); cont[0] += 1
        return raiz
    else:
        if raiz.r is None:
            return raiz
        if x > raiz.r.val:                       # zig-zig derecho
            raiz.r.r = splay(raiz.r.r, x, cont)
            raiz = rot_izq(raiz); cont[0] += 1
            raiz = rot_izq(raiz); cont[0] += 1
        elif x < raiz.r.val:                     # zig-zag
            raiz.r.l = splay(raiz.r.l, x, cont)
            raiz.r = rot_der(raiz.r); cont[0] += 1
            raiz = rot_izq(raiz); cont[0] += 1
        else:                                    # zig
            raiz = rot_izq(raiz); cont[0] += 1
        return raiz


def camino_a(raiz, x):
    pila = []
    while raiz is not None:
        pila.append(raiz)
        if x == raiz.val:
            return pila
        raiz = raiz.l if x < raiz.val else raiz.r
    return None


def subir_a_la_raiz(raiz, x, cont):
    """Rotar x hasta la raíz de a una rotación por nivel (el mal ejemplo)."""
    pila = camino_a(raiz, x)
    if pila is None:
        return raiz
    for j in range(len(pila) - 2, -1, -1):
        padre = pila[j]
        if padre.l is pila[-1]:
            nuevo = rot_der(padre)
        else:
            nuevo = rot_izq(padre)
        cont[0] += 1
        if j == 0:
            raiz = nuevo
        else:
            abu = pila[j - 1]
            if abu.l is padre:
                abu.l = nuevo
            else:
                abu.r = nuevo
    return raiz


def construir_camino(n):
    """Camino de n nodos: raíz n, cadena de hijos izquierdos hasta 1."""
    raiz = Nodo(n)
    actual = raiz
    for k in range(n - 1, 0, -1):
        actual.l = Nodo(k)
        actual = actual.l
    return raiz


def en_orden(raiz):
    salida = []
    pila, p = [], raiz
    while pila or p:
        while p:
            pila.append(p)
            p = p.l
        p = pila.pop()
        salida.append(p.val)
        p = p.r
    return salida


def tamanos(raiz):
    """dict clave -> tamaño del subárbol (para el potencial)."""
    tam = {}

    def rec(p):
        if p is None:
            return 0
        t = 1 + rec(p.l) + rec(p.r)
        tam[p.val] = t
        return t

    rec(raiz)
    return tam


def correr(n, algoritmo, rondas=3):
    """Costo (rotaciones) de cada uno de los rondas*n accesos 1..n."""
    raiz = construir_camino(n)
    # el potencial inicial del camino: sum_{k=1}^{n} log2 k = log2(n!)
    assert tamanos(raiz) == {k: k for k in range(1, n + 1)}
    phi0 = sum(math.log2(k) for k in range(1, n + 1))

    costos = []
    for _ in range(rondas):
        for k in range(1, n + 1):
            cont = [0]
            if algoritmo == "splay":
                raiz = splay(raiz, k, cont)
            else:
                raiz = subir_a_la_raiz(raiz, k, cont)
            assert raiz.val == k                 # el accedido queda en la raíz
            costos.append(cont[0])
        assert en_orden(raiz) == list(range(1, n + 1))   # sigue siendo un BST
    return costos, phi0


def main():
    print(f"{'n':>5} {'splay (rot/acceso)':>19} {'subir a la raíz':>16} {'log2 n':>7}")
    for n in (100, 200, 400, 800):
        costos_s, phi0 = correr(n, "splay")
        costos_r, _ = correr(n, "subir")

        # 1) el primer acceso es el caro: n-1 rotaciones, todo zig-zig
        assert costos_s[0] == n - 1, (n, costos_s[0])
        assert costos_r[0] == n - 1

        # 3) la cota del lema de acceso + sección 5 se cumple
        cota = 3 * n * (3 * math.ceil(math.log2(n)) + 1) + phi0
        assert sum(costos_s) <= cota, (n, sum(costos_s), cota)

        # 4) pero el promedio medido es constante, no logarítmico
        prom_s = sum(costos_s) / len(costos_s)
        prom_r = sum(costos_r) / len(costos_r)
        assert prom_s < 10, (n, prom_s)                 # plano, ~4
        assert 0.30 * n < prom_r < 0.80 * n, (n, prom_r)   # ~n/2

        print(f"{n:>5} {prom_s:>19.2f} {prom_r:>16.1f} {math.log2(n):>7.1f}")

    # la brecha entre los dos crece con n (ratio ~n / 2*4)
    cs800, _ = correr(800, "splay")
    cr800, _ = correr(800, "subir")
    ratio = (sum(cr800) / len(cr800)) / (sum(cs800) / len(cs800))
    assert ratio > 50

    print("ejercicio 13: todo correcto")
    print("  primer acceso = n-1 rotaciones (zig-zig continuo), ambos algoritmos")
    print("  potencial inicial = log2(n!) exacto (subárboles de tamaño k en el camino)")
    print("  la cota del lema (3n(3 log2 n + 1) + log2 n!) se cumple...")
    print("  ...pero splay mide ~4 rotaciones por acceso (constante): cota NO ajustada")
    print(f"  subir a la raíz: ~n/2 por acceso; en n = 800 es {ratio:.0f} veces más caro")


if __name__ == "__main__":
    main()
