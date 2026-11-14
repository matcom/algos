class Nodo:
    __slots__ = ("sig",)

    def __init__(self):
        self.sig = None


def hay_ciclo(cabeza):
    a1 = a2 = cabeza
    while a2 is not None and a2.sig is not None:
        a1 = a1.sig
        a2 = a2.sig.sig
        if a1 is a2:
            return True
    return False


def vueltas_formula(cola, ciclo):
    if ciclo == 0:
        return cola // 2
    k = max(1, -(-cola // ciclo))
    return k * ciclo
