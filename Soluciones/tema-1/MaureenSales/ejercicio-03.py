"""Ejercicio 3 — Una pila con `minimo` en $O(1)$

Código extraído de ejercicio-03.md, en el mismo orden en que aparece allí.
Ejecutar con:  python ejercicio-03.py
La salida esperada es la de la sección "Salida" de ejercicio-03.md.
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")   # para que la consola de Windows imprima δ, ≤, ⌈⌉...

# ----------------------------------------------------------------------
# Del md, sección: 1. Diseño de la estructura
# ----------------------------------------------------------------------

class PilaMin:
    def __init__(self):
        self.S = []     # elementos
        self.M = []     # M[i] = min(S[0..i])

    def push(self, x):
        self.S.append(x)
        if not self.M or x < self.M[-1]:
            self.M.append(x)
        else:
            self.M.append(self.M[-1])

    def pop(self):
        self.M.pop()
        return self.S.pop()

    def minimo(self):
        return self.M[-1]

    def __len__(self):
        return len(self.S)


# ----------------------------------------------------------------------
# Del md, sección: 4. Casos de prueba
# ----------------------------------------------------------------------

import random

def chequear_invariante(p):
    assert len(p.S) == len(p.M)
    for i in range(len(p.S)):
        assert p.M[i] == min(p.S[:i + 1])

def prueba_aleatoria(clase, generar_valor, ops=200, vigilar=False):
    p, ref = clase(), []
    for _ in range(ops):
        if ref and random.random() < 0.45:
            assert p.pop() == ref.pop()
        else:
            x = generar_valor()
            p.push(x); ref.append(x)
        if ref:
            if p.minimo() != min(ref):
                return False
        if vigilar:
            chequear_invariante(p)
    return True

random.seed(3)

# 1) Ejemplo de la ilustración
p = PilaMin()
for x in [5, 7, 3, 8, 3]:
    p.push(x)
assert p.minimo() == 3
assert p.pop() == 3 and p.minimo() == 3
assert p.pop() == 8 and p.minimo() == 3
assert p.pop() == 3 and p.minimo() == 5
p.push(1); assert p.minimo() == 1
print("ejemplo de la ilustración: OK")

# 2) PilaMin con invariante vigilado, valores con muchos empates
for _ in range(300):
    assert prueba_aleatoria(PilaMin, lambda: random.randint(0, 5), vigilar=True)
print("PilaMin: 300 secuencias aleatorias, invariante vigilado en cada paso: OK")

# 3) Costo: contar comparaciones por operación (debe ser <= 1 siempre)
class PilaMinContada(PilaMin):
    comps = 0
    def push(self, x):
        if self.M:
            PilaMinContada.comps += 1
        super().push(x)
p = PilaMinContada()
for i in range(10000):
    p.push(random.random())
print(f"10000 push -> {PilaMinContada.comps} comparaciones (<= 1 por push)")
assert PilaMinContada.comps <= 10000
