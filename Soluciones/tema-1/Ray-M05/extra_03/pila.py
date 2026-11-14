import sys
from itertools import product

from comun.tabla import tabla_md


class PilaConMinimo:
    def __init__(self):
        self.cima = None

    def vacia(self):
        return self.cima is None

    def apilar(self, x):
        if self.cima is None:
            self.cima = (x, x, None)
        else:
            _, m, _ = self.cima
            self.cima = (x, x if x < m else m, self.cima)

    def desapilar(self):
        x, _, abajo = self.cima
        self.cima = abajo
        return x

    def tope(self):
        return self.cima[0]

    def minimo(self):
        return self.cima[1]


def invariante(pila):
    nodos = []
    nodo = pila.cima
    while nodo is not None:
        nodos.append(nodo)
        nodo = nodo[2]
    debajo = None
    for valor, minimo, _ in reversed(nodos):
        esperado = valor if debajo is None else min(valor, debajo)
        assert minimo == esperado, f"nodo {valor}: guarda {minimo}, debería {esperado}"
        debajo = esperado


def ejecutar(pila, operaciones, vigilar=False):
    lista = []
    for i, op in enumerate(operaciones, start=1):
        if op[0] == "+":
            pila.apilar(op[1])
            lista.append(op[1])
        else:
            assert pila.desapilar() == lista.pop()
        if vigilar:
            invariante(pila)
        if lista and (pila.tope() != lista[-1] or pila.minimo() != min(lista)):
            return i
        if not lista and not pila.vacia():
            return i
    return None


def secuencias(largo, valores):
    acciones = [("+", v) for v in valores] + [("-",)]
    for ops in product(acciones, repeat=largo):
        tam = 0
        valida = True
        for op in ops:
            tam += 1 if op[0] == "+" else -1
            if tam < 0:
                valida = False
                break
        if valida:
            yield ops


def _exhaustivo():
    filas = []
    for largo in range(1, 9):
        total = comprobadas = malas = 0
        for ops in secuencias(largo, (0, 1, 2)):
            total += 1
            comprobadas += largo
            malas += ejecutar(PilaConMinimo(), ops, vigilar=True) is not None
        filas.append([largo, f"{total:,}", f"{comprobadas:,}", malas])
    print(tabla_md(["operaciones", "secuencias", "operaciones comprobadas", "fallos"],
                   filas, "dddd"))


SECCIONES = {
    "exhaustivo": _exhaustivo,
}

if __name__ == "__main__":
    SECCIONES[sys.argv[1]]()
