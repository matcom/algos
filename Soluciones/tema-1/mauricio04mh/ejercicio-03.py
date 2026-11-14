"""Ejercicio 3. Pila con mínimo en O(1)."""
import random


class PilaMin:
    def __init__(self):
        self.v = []      # valores
        self.m = []      # m[i] = mínimo de v[0..i]
        self.operaciones = 0

    def push(self, x):
        self.v.append(x)
        self.m.append(x if not self.m else min(x, self.m[-1]))
        self.operaciones += 3          # comparación + dos append

    def pop(self):
        self.m.pop()
        self.operaciones += 2
        return self.v.pop()

    def minimo(self):
        self.operaciones += 1
        return self.m[-1]

    def invariante(self):
        return (len(self.v) == len(self.m) and
                all(self.m[i] == min(self.v[:i + 1]) for i in range(len(self.v))))


class PilaMinCompacta:
    """Variante que ahorra memoria: m guarda solo los mínimos nuevos.
    Con estricto=True usa '<' al apilar, y falla si el mínimo se repite."""

    def __init__(self, estricto):
        self.v, self.m, self.estricto = [], [], estricto

    def push(self, x):
        self.v.append(x)
        if not self.m or (x < self.m[-1] if self.estricto else x <= self.m[-1]):
            self.m.append(x)

    def pop(self):
        x = self.v.pop()
        if x == self.m[-1]:
            self.m.pop()
        return x

    def minimo(self):
        return self.m[-1] if self.m else None


def falla_compacta(operaciones, estricto):
    """True si la variante compacta da un mínimo incorrecto en algún momento."""
    p, ref = PilaMinCompacta(estricto), []
    for op, x in operaciones:
        if op == "push":
            p.push(x); ref.append(x)
        else:
            p.pop(); ref.pop()
        if ref and p.minimo() != min(ref):
            return True
    return False


def secuencia_aleatoria(rng, valores, largo=20):
    ops, tam = [], 0
    for _ in range(largo):
        if tam and rng.random() < 0.4:
            ops.append(("pop", None)); tam -= 1
        else:
            ops.append(("push", rng.choice(valores))); tam += 1
    return ops


if __name__ == "__main__":
    # Ejemplo del enunciado
    p = PilaMin()
    for x in [5, 2, 7, 2]:
        p.push(x)
    print("v =", p.v, " m =", p.m, " minimo() =", p.minimo())
    for _ in range(3):
        p.pop()
    print("tras tres pop: v =", p.v, " m =", p.m, " minimo() =", p.minimo())

    # Prueba aleatoria contra una pila ingenua, con el invariante vigilado
    random.seed(3)
    pasos, malos = 0, 0
    for _ in range(2000):
        p, ref = PilaMin(), []
        for _ in range(random.randint(1, 40)):
            if ref and random.random() < 0.4:
                assert p.pop() == ref.pop()
            else:
                x = random.randint(-20, 20)
                p.push(x)
                ref.append(x)
            assert p.invariante()
            if ref:
                malos += p.minimo() != min(ref)
            pasos += 1
    print(f"operaciones comprobadas: {pasos}, respuestas incorrectas de minimo(): {malos}")

    # Costo: operaciones elementales por operación, no depende del tamaño
    for n in [10, 1_000, 100_000]:
        p = PilaMin()
        for i in range(n):
            p.push(i)
        antes = p.operaciones
        p.minimo()
        print(f"n = {n:>7}: minimo() cuesta {p.operaciones - antes} operación elemental")

    # Extensión: la variante compacta con '<' en lugar de '<='
    p = PilaMinCompacta(estricto=True)
    p.push(2); p.push(2); p.pop()
    print("\nCompacta con '<': push(2), push(2), pop() deja v =", p.v, " m =", p.m,
          " minimo() =", p.minimo())

    # Todas las secuencias de hasta 8 operaciones con valores 0, 1, 2
    from itertools import product
    ops = [("push", x) for x in range(3)] + [("pop", None)]
    total = fallan_menor = fallan_menor_igual = 0
    for largo in range(1, 9):
        for seq in product(ops, repeat=largo):
            tam, valida = 0, True
            for op, _ in seq:
                tam += 1 if op == "push" else -1
                valida = valida and tam >= 0
            if not valida:
                continue
            total += 1
            if falla_compacta(seq, estricto=True):
                fallan_menor += 1
                # toda falla tiene un push de un valor igual al mínimo del momento
                pila, repetido = [], False
                for op, x in seq:
                    if op == "push":
                        repetido = repetido or (bool(pila) and x == min(pila))
                        pila.append(x)
                    else:
                        pila.pop()
                assert repetido
            fallan_menor_igual += falla_compacta(seq, estricto=False)
    assert fallan_menor_igual == 0
    print(f"secuencias válidas de hasta 8 operaciones: {total}; fallan con '<': "
          f"{fallan_menor}; con '<=': {fallan_menor_igual}")

    # Qué atrapa cada generador de pruebas (secuencias de 20 operaciones)
    rng = random.Random(30)
    print(f"{'valores':>14} {'fallan con <':>13}")
    for nombre, valores in [("0..1", range(2)), ("0..9", range(10)),
                            ("0..999", range(1000)), ("0..10^6", range(10 ** 6))]:
        casos = [secuencia_aleatoria(rng, valores) for _ in range(4000)]
        f = sum(falla_compacta(c, estricto=True) for c in casos) / len(casos)
        print(f"{nombre:>14} {100 * f:>12.1f}%")
