"""Ejercicio 3: pila con minimo() en O(1) en el peor caso.
Cada nivel guarda el par (elemento, mínimo de los niveles 1..i)."""

import random


class PilaMin:
    def __init__(self):
        self.pares = (
            []
        )  # pares[i-1] = (elemento del nivel i, mínimo de los niveles 1..i)

    def push(self, x):
        if not self.pares:  # pila vacía: el mínimo es x
            self.pares.append((x, x))
        else:
            m = self.pares[-1][1]  # por el invariante, m = mínimo de 1..k
            self.pares.append((x, min(x, m)))

    def pop(self):
        return self.pares.pop()[0]

    def tope(self):
        return self.pares[-1][0]

    def minimo(self):
        return self.pares[-1][1]

    def __len__(self):
        return len(self.pares)

    def invariante(self):
        """Comprueba el invariante en todos los niveles."""
        elementos = [x for x, _ in self.pares]
        return all(
            self.pares[i][1] == min(elementos[: i + 1]) for i in range(len(self.pares))
        )


# Prueba 1: invariante vigilado y minimo() contra la versión lenta min(lista)
random.seed(3)
operaciones = 0
for _ in range(2000):
    pila, espejo = PilaMin(), []
    for _ in range(random.randint(1, 40)):
        if espejo and random.random() < 0.45:
            assert pila.pop() == espejo.pop()
        else:
            x = random.randint(-20, 20)  # rango chico: muchos empates
            pila.push(x)
            espejo.append(x)
        assert pila.invariante()
        if espejo:
            assert pila.minimo() == min(espejo)
        operaciones += 1
print(f"{operaciones:,} operaciones al azar")
