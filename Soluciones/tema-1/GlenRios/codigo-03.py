class PilaMin:
    def __init__(self):
        self.principal = []
        self.minimos = []
    def push(self, x):
        self.principal.append(x)
        if not self.minimos or x <= self.minimos[-1]:
            self.minimos.append(x)
    def pop(self):
        x = self.principal.pop()
        if x == self.minimos[-1]:
            self.minimos.pop()
        return x
    def min(self):
        return self.minimos[-1]

import random
import os
RUTA = os.path.join("Soluciones", "tema-1", "GlenRios")
os.makedirs(RUTA, exist_ok=True)  # crea la carpeta si no existe
p = PilaMin()
for _ in range(10000):
    op = random.choice(['push', 'pop', 'min'])
    if op == 'push':
        p.push(random.randint(0, 1000))
    elif op == 'pop' and p.principal:
        p.pop()
    elif op == 'min' and p.principal:
        assert p.min() == min(p.principal), "Invariante violado"
print("Todas las operaciones mantienen el invariante.")