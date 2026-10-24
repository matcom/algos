"""Ejercicio 3: pila con minimo en O(1) en el peor caso.

Corre: python ejercicio-03.py
"""
import random

class PilaMin:
    """Cada celda guarda (valor, mínimo de la pila hasta esa celda inclusive)."""
    def __init__(self):
        self.celdas = []

    def apilar(self, x):
        m = x if not self.celdas else min(x, self.celdas[-1][1])
        self.celdas.append((x, m))

    def desapilar(self):
        return self.celdas.pop()[0]

    def tope(self):
        return self.celdas[-1][0]

    def minimo(self):
        return self.celdas[-1][1]

    def vacia(self):
        return not self.celdas

    def invariante(self):
        # I: celdas[i].min == min(valores[0..i]) para todo i
        m = None
        for x, mi in self.celdas:
            m = x if m is None else min(m, x)
            if mi != m:
                return False
        return True


class PilaMinAhorro:
    """Variante con pila auxiliar que solo guarda los mínimos nuevos.
    ERROR PLANTADO: usa < en lugar de <=, y se rompe con valores repetidos."""
    def __init__(self, estricta=True):
        self.datos, self.mins, self.estricta = [], [], estricta

    def apilar(self, x):
        self.datos.append(x)
        if not self.mins or (x < self.mins[-1] if self.estricta else x <= self.mins[-1]):
            self.mins.append(x)

    def desapilar(self):
        x = self.datos.pop()
        if self.mins and x == self.mins[-1]:
            self.mins.pop()
        return x

    def minimo(self):
        return self.mins[-1]

    def vacia(self):
        return not self.datos


def secuencia(rng, ops, valores):
    """Operaciones al azar: 'a' apila un valor de `valores`, 'd' desapila (si se puede)."""
    tam = 0
    for _ in range(ops):
        if tam == 0 or rng.random() < 0.55:
            yield ("a", rng.choice(valores)); tam += 1
        else:
            yield ("d", None); tam -= 1


def contra_oraculo(clase, sec, vigilar=False):
    """Compara minimo() con min(lista) tras cada operación. Devuelve True si nunca difieren."""
    p, ref = clase(), []
    for op, x in sec:
        if op == "a":
            p.apilar(x); ref.append(x)
        else:
            assert p.desapilar() == ref.pop()
        try:
            if ref and p.minimo() != min(ref):
                return False
        except IndexError:          # la auxiliar quedó vacía con la pila no vacía
            return False
        if vigilar:
            assert p.invariante()
    return True


if __name__ == "__main__":
    rng = random.Random(2026)

    # 1. Casos borde a mano
    p = PilaMin()
    for x in [5, 3, 7, 3, 1, 1, 9]:
        p.apilar(x)
    assert p.minimo() == 1
    assert [p.desapilar() for _ in range(3)] == [9, 1, 1]
    assert p.minimo() == 3
    p.desapilar(); assert p.minimo() == 3      # se fue el 3 repetido; queda el otro
    p.desapilar(); p.desapilar(); assert p.minimo() == 5
    p.desapilar(); assert p.vacia()

    # 2. Pruebas aleatorias con invariante vigilado (como el de Boyer-Moore en la sección 4 de la conferencia 3)
    for _ in range(2000):
        assert contra_oraculo(PilaMin, secuencia(rng, 60, range(10)), vigilar=True)
    print("PilaMin: 2000 secuencias, invariante vigilado en cada paso, 0 fallos")

    # 3. El error plantado: cuánto lo ven las pruebas según el generador
    print(f"\n{'generador':>34} {'fallos PilaMinAhorro(<)':>24} {'con <=':>7}")
    generadores = {
        "valores distintos (rango 10^9)": lambda: secuencia(rng, 60, range(10**9)),
        "valores en rango 0..99":         lambda: secuencia(rng, 60, range(100)),
        "valores en rango 0..9":          lambda: secuencia(rng, 60, range(10)),
        "valores en {0, 1}":              lambda: secuencia(rng, 60, range(2)),
    }
    for nombre, gen in generadores.items():
        N = 2000
        fallos = sum(not contra_oraculo(PilaMinAhorro, gen()) for _ in range(N))
        bien = sum(not contra_oraculo(lambda: PilaMinAhorro(estricta=False), gen()) for _ in range(N))
        print(f"{nombre:>34} {100 * fallos / N:>23.1f}% {bien:>7}")
        assert bien == 0

    # 4. El contraejemplo mínimo que anuncia la demostración: un mínimo repetido
    malo = PilaMinAhorro()
    malo.apilar(1); malo.apilar(1); malo.desapilar()
    print("\napilar 1, apilar 1, desapilar ->",
          "minimo() lanza IndexError" if not malo.mins else f"minimo() = {malo.minimo()}")
    assert not malo.mins   # la pila tiene un 1, pero la auxiliar quedó vacía
