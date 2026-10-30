"""Ejercicio 3 ★ — Pila con `minimo` en $O(1)$ en el peor caso (C3)

Código de validación de ejercicio-03.md.
Ejecutar con: python ejercicio-03.py
"""


# -------------------- Parte 1 --------------------

class Nodo:
    __slots__ = ("valor", "minimo", "abajo")
    def __init__(self, valor, minimo, abajo):
        self.valor, self.minimo, self.abajo = valor, minimo, abajo

class PilaMin:
    def __init__(self):
        self.cima = None
        self.tam = 0

    def apilar(self, x):
        if self.cima is None or x < self.cima.minimo:
            m = x
        else:
            m = self.cima.minimo
        self.cima = Nodo(x, m, self.cima)
        self.tam += 1

    def desapilar(self):
        nodo = self.cima
        self.cima = nodo.abajo
        self.tam -= 1
        return nodo.valor

    def tope(self):
        return self.cima.valor

    def minimo(self):
        return self.cima.minimo

# -------------------- Parte 2 --------------------

p = PilaMin()
traza = []
for op in ["a5", "a3", "a7", "a3", "d", "d", "d", "a1", "d", "d"]:
    if op[0] == "a":
        p.apilar(int(op[1:]))
    else:
        p.desapilar()
    traza.append(f"{op:>3}: min={p.minimo() if p.tam else '-'}")
print("  ".join(traza))

# -------------------- Parte 3 --------------------

import random

def comprobar_invariante(p):
    nodos = []
    x = p.cima
    while x is not None:
        nodos.append(x)
        x = x.abajo
    nodos.reverse()                       # del fondo al tope
    minimo = None
    for nodo in nodos:
        minimo = nodo.valor if minimo is None else min(minimo, nodo.valor)
        if nodo.minimo != minimo:
            return False
    return True

random.seed(3)
operaciones, fallos = 0, 0
for _ in range(500):
    p, ref = PilaMin(), []
    for _ in range(60):
        bien = True
        if ref and random.random() < 0.45:
            bien = p.desapilar() == ref.pop()
        else:
            x = random.randrange(5)       # pocos valores: muchos empates
            p.apilar(x)
            ref.append(x)
        bien = comprobar_invariante(p) and bien
        if ref:
            bien = bien and p.minimo() == min(ref) and p.tope() == ref[-1]
        fallos += not bien
        operaciones += 1
if fallos == 0:
    print(f"{operaciones} operaciones al azar, invariante y oráculo sin fallos")
else:
    print(f"{operaciones} operaciones al azar: {fallos} fallan el invariante o el oráculo")

# -------------------- Parte 4 --------------------

import time

for k in [10**3, 10**5, 10**6]:
    p = PilaMin()
    for i in range(k):
        p.apilar(k - i)                   # cada elemento es un nuevo mínimo
    t0 = time.perf_counter()
    for _ in range(10**5):
        p.minimo()
    t = (time.perf_counter() - t0) / 10**5
    print(f"k = {k:>9,}: minimo() tarda {t * 1e9:6.1f} ns por llamada")
