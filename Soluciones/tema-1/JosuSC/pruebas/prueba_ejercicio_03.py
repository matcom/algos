#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejercicio 3 - Casos de prueba
Pila con operación minimo en O(1) peor caso (dos pilas: P y M).

Qué se comprueba:
  1. El comportamiento LIFO y el min() contra un oráculo ingenuo
     (una lista y min() de Python), sobre 20000 operaciones aleatorias.
  2. El invariante M[i] = min(P[1..i]) vigilado DESPUÉS DE CADA operación:
     |P| == |M| y cada nivel de M es el mínimo del prefijo de P.
  3. Casos borde: pila vacía, un elemento, todo iguales, creciente
     estricto, decreciente estricto, y vaciar por completo.
  4. Que pop desapila también de M (si no, el invariante se rompe).

Ejecutar:  python3 prueba_ejercicio_03.py
Solo usa la biblioteca estándar.
"""

import random


class PilaMin:
    def __init__(self):
        self.P = []   # elementos
        self.M = []   # mínimos: M[i] = min(P[0..i])

    def push(self, x):
        self.P.append(x)
        if not self.M or x <= self.M[-1]:
            self.M.append(x)
        else:
            self.M.append(self.M[-1])

    def pop(self):
        self.M.pop()
        return self.P.pop()

    def top(self):
        return self.P[-1]

    def min(self):
        return self.M[-1]

    def empty(self):
        return len(self.P) == 0


def revisa_invariante(p):
    """El invariante de la sección 3, completo."""
    assert len(p.P) == len(p.M), (p.P, p.M)
    for i in range(len(p.P)):
        assert p.M[i] == min(p.P[:i + 1]), (p.P, p.M, i)


def main():
    # ------------------------------------------------------------------
    # 1) Aleatorio contra oráculo + invariante vigilado en cada operación
    # ------------------------------------------------------------------
    random.seed(11)
    p, referencia = PilaMin(), []
    operaciones = 0
    for _ in range(20000):
        if p.empty() or random.random() < 0.55 and len(p.P) < 60 or referencia == []:
            x = random.randint(0, 5)     # rango chico: muchos duplicados
            p.push(x)
            referencia.append(x)
        else:
            x = p.pop()
            assert x == referencia.pop()
        operaciones += 1
        # oráculo
        assert p.empty() == (len(referencia) == 0)
        if not p.empty():
            assert p.top() == referencia[-1]
            assert p.min() == min(referencia)
        # invariante completo (cada operación, no al final)
        revisa_invariante(p)

    # ------------------------------------------------------------------
    # 2) Casos borde construidos a mano
    # ------------------------------------------------------------------
    # vacía
    p = PilaMin()
    assert p.empty()
    # un elemento
    p.push(7)
    assert (p.top(), p.min()) == (7, 7) and not p.empty()
    assert p.pop() == 7 and p.empty()
    # todos iguales
    p = PilaMin()
    for _ in range(5):
        p.push(3)
    assert p.min() == 3
    assert p.pop() == 3 and p.min() == 3        # pop también saca de M
    # creciente estricto: M se llena del primer elemento
    p = PilaMin()
    for x in [1, 2, 3, 4, 5]:
        p.push(x)
    assert p.M == [1, 1, 1, 1, 1] and p.min() == 1
    # decreciente estricto: M copia a P
    p = PilaMin()
    for x in [5, 4, 3, 2, 1]:
        p.push(x)
    assert p.M == [5, 4, 3, 2, 1] and p.min() == 1
    # el mínimo "vuelve" al desapilar los chicos
    for esperado in [1, 2, 3, 4, 5]:
        assert p.min() == esperado
        assert p.pop() == esperado
    assert p.empty()

    # ------------------------------------------------------------------
    # 3) Una secuencia mezclada con verificación de M completa
    # ------------------------------------------------------------------
    p = PilaMin()
    secuencia = [5, 3, 7, 1, 4, 2]
    for x in secuencia:
        p.push(x)
    assert p.P == [5, 3, 7, 1, 4, 2]
    assert p.M == [5, 3, 3, 1, 1, 1]            # el ejemplo de la ilustración
    p.pop(); p.pop()                            # saca 2 y 4
    assert p.M == [5, 3, 3, 1] and p.min() == 1 # el mínimo sigue siendo 1

    print("ejercicio 3: todo correcto")
    print(f"  {operaciones} operaciones aleatorias contra oráculo, invariante vigilado en cada una")
    print("  casos borde: vacía, un elemento, duplicados, creciente, decreciente, vaciar")


if __name__ == "__main__":
    main()
