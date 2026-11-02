import random

# Ejercicio 3, Tema 1: pila con operacion minimo en O(1) en el peor caso.
#
# Idea: cada elemento se guarda junto con el minimo de todo lo que hay
# debajo de el (incluyendolo). Asi el minimo de la pila siempre esta arriba.
#
# Invariante: para cada posicion i, datos[i] = (v_i, m_i) con
#             m_i = min(v_0, ..., v_i)


class PilaMin:
    def __init__(self):
        self.datos = []                      # lista de pares (valor, minimo hasta aqui)

    def vacia(self):
        return not self.datos

    def push(self, x):
        if self.datos:
            m = min(x, self.datos[-1][1])    # minimo de lo de abajo y x
        else:
            m = x
        self.datos.append((x, m))

    def pop(self):
        return self.datos.pop()[0]           # da error si esta vacia

    def top(self):
        return self.datos[-1][0]

    def minimo(self):
        return self.datos[-1][1]             # el minimo de toda la pila


class PilaMala:
    """Version que NO funciona: guarda una sola variable con el minimo."""

    def __init__(self):
        self.datos = []
        self.m = None

    def push(self, x):
        self.datos.append(x)
        self.m = x if self.m is None else min(self.m, x)

    def pop(self):
        return self.datos.pop()              # el minimo no se actualiza

    def minimo(self):
        return self.m


def invariante(pila):
    """Comprueba que cada par guarde el minimo de todo lo que tiene debajo."""
    actual = None
    for v, m in pila.datos:
        actual = v if actual is None else min(actual, v)
        if m != actual:
            return False
    return True


def secuencia_aleatoria(largo):
    """Lista de operaciones al azar; pop solo si hay algo que sacar."""
    ops, tam = [], 0
    for _ in range(largo):
        if tam > 0 and random.random() < 0.4:
            ops.append(("pop", None))
            tam -= 1
        else:
            ops.append(("push", random.randint(0, 20)))
            tam += 1
    return ops


if __name__ == "__main__":
    random.seed(1)

    # contraejemplo minimo de la version mala
    mala = PilaMala()
    mala.push(5)
    mala.push(3)
    mala.pop()
    print(f"Version mala: push 5, push 3, pop -> minimo = {mala.minimo()} (deberia ser 5)")
    print()

    # prueba contra una lista normal
    pruebas = 5000
    fallos_buena = fallos_mala = 0
    operaciones = 0
    for _ in range(pruebas):
        buena, mala, ref = PilaMin(), PilaMala(), []
        for op, x in secuencia_aleatoria(random.randint(1, 30)):
            if op == "push":
                buena.push(x)
                mala.push(x)
                ref.append(x)
            else:
                assert buena.pop() == ref[-1]
                mala.pop()
                ref.pop()
            operaciones += 1
            assert invariante(buena)         # el invariante siempre se cumple
            if ref:
                assert buena.minimo() == min(ref)
                assert buena.top() == ref[-1]
                if mala.minimo() != min(ref):
                    fallos_mala += 1
    print(f"{pruebas} secuencias al azar, {operaciones} operaciones")
    print("PilaMin: invariante y minimo correctos en todas")
    print(f"PilaMala: dio un minimo equivocado en {fallos_mala} consultas")
