import random

class PilaMinimo:
    def __init__(self):
        self.S = []

    def push(self, x):
        if not self.S:
            m = x
        else:
            m = min(x, self.S[-1][1])

        self.S.append((x, m))

    
    def pop(self):
        return self.S.pop()[0]

    def tope(self):
        return self.S[-1][0]

    def minimo(self):
        return self.S[-1][1]

def verificar(p, modelo):
    for j, (v,m) in enumerate(p.S):
        assert m == min(v2 for v2, _ in p.S[:j + 1])

    assert [v for v, _ in p.S] == modelo
    if modelo: 
        p.minimo() == min(modelo) and p.tope() == modelo[-1]


random.seed(0)
for _ in range(2000):
    p, modelo = PilaMinimo(), []

    for _ in range(random.randint(0, 60)):
        if modelo and random.random() < 0.4:
            assert p.pop() == modelo.pop()
        else:
            x = random.randint(0,10)
            p.push(x)
            modelo.append(x)
        verificar(p, modelo)

print("FETEN")