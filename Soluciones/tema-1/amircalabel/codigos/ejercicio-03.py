
import random

class PilaConMinimo:
    def __init__(self):
        self.principal = []
        self.minimos = []

    def push(self, x):
        self.principal.append(x)
        if not self.minimos or x <= self.minimos[-1]:
            self.minimos.append(x)
        self._verificar()

    def pop(self):
        if not self.principal:
            raise IndexError("pila vacía")
        x = self.principal.pop()
        if x == self.minimos[-1]:
            self.minimos.pop()
        self._verificar()
        return x

    def minimo(self):
        if not self.minimos:
            raise IndexError("pila vacía")
        return self.minimos[-1]

    def _verificar(self):
        # Invariante: el tope de minimos es el mínimo de principal
        if self.principal:
            assert self.minimos[-1] == min(self.principal), \
                f"Invariante violado: min={min(self.principal)}, tope={self.minimos[-1]}"
        # Invariante: minimos es no decreciente de abajo hacia arriba
        for i in range(len(self.minimos) - 1):
            assert self.minimos[i] >= self.minimos[i + 1], \
                "minimos no es no decreciente"

def traza():
    p = PilaConMinimo()
    ops = [("push", 5), ("push", 3), ("push", 7), ("minimo", None),
           ("pop", None), ("minimo", None), ("pop", None), ("minimo", None),
           ("push", 2), ("minimo", None), ("pop", None), ("minimo", None),
           ("pop", None)]
    print(f"{'op':>8} {'principal':>15} {'minimos':>15} {'resultado':>10}")
    for op, val in ops:
        if op == "push":
            p.push(val)
            res = "—"
        elif op == "pop":
            res = p.pop()
        else:
            res = p.minimo()
        print(f"{op:>8} {str(p.principal):>15} {str(p.minimos):>15} {str(res):>10}")

def test_aleatorio(n=10000):
    p = PilaConMinimo()
    for _ in range(n):
        if not p.principal or random.random() < 0.6:
            p.push(random.randint(0, 100))
        else:
            p.pop()
    print(f"Test aleatorio con {n} operaciones: OK")

if __name__ == "__main__":
    traza()
    print()
    test_aleatorio()
