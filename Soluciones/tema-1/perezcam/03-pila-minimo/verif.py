import random

class PilaMin:
    """Dos pilas paralelas: principal y de minimos corrientes."""
    def __init__(self):
        self.principal = []
        self.minimos = []

    def push(self, x):
        self.principal.append(x)
        if not self.minimos or x <= self.minimos[-1]:
            self.minimos.append(x)
        else:
            self.minimos.append(self.minimos[-1])

    def pop(self):
        self.minimos.pop()
        return self.principal.pop()

    def minimo(self):
        return self.minimos[-1]

def test(clase, nombre, trials=2000, max_ops=200):
    random.seed(42)
    for t in range(trials):
        pila = clase()
        referencia = []
        for _ in range(random.randint(1, max_ops)):
            if referencia and random.random() < 0.4:
                x1 = pila.pop()
                x2 = referencia.pop()
                assert x1 == x2, f"{nombre}: pop devolvio {x1}, esperaba {x2}"
            else:
                x = random.randint(-1000, 1000)
                pila.push(x)
                referencia.append(x)
            if referencia:
                m1 = pila.minimo()
                m2 = min(referencia)
                assert m1 == m2, f"{nombre}: minimo()={m1}, esperaba {m2}, pila={referencia}"
    print(f"{nombre}: {trials} secuencias aleatorias verificadas, sin fallos")

test(PilaMin, "PilaMin (dos pilas)")
