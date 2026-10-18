#!/usr/bin/env python3
"""
Verificación del Ejercicio 3: pila con operación min() en O(1) en el peor caso.

Qué hace:
  1. Implementa la estructura (dos pilas: stack y stack_min) con primitivas contadas.
  2. Comprueba el invariante después de CADA operación de todos los casos de prueba.
  3. Verifica los casos C1..C8 y el ejemplo ilustrado, e imprime las tablas en Markdown.
  4. Compara contra una pila ingenua (recorre todo para hallar el mínimo) con pruebas aleatorias.
  5. Mide cuántas primitivas hace cada operación según el tamaño de la pila (costo constante).

Uso:  python3 verificar_ejercicio_03.py
"""
import random


# ----------------------------------------------------------------------------
# Estructura
# ----------------------------------------------------------------------------
class Contador:
    def __init__(self):
        self.primitivas = 0   # push, pop, top, isEmpty
        self.comparaciones = 0


class Pila:
    """Pila con las cuatro primitivas contadas. contenido() y tamano() son solo
    para verificar y no se cuentan."""

    def __init__(self, contador):
        self._datos = []
        self._c = contador

    def push(self, v):
        self._c.primitivas += 1
        self._datos.append(v)

    def pop(self):
        self._c.primitivas += 1
        return self._datos.pop()

    def top(self):
        self._c.primitivas += 1
        return self._datos[-1]

    def is_empty(self):
        self._c.primitivas += 1
        return len(self._datos) == 0

    def contenido(self):
        return list(self._datos)

    def tamano(self):
        return len(self._datos)


class MinStack:
    def __init__(self):
        self.contador = Contador()
        self.stack = Pila(self.contador)
        self.stack_min = Pila(self.contador)

    def _menor(self, a, b):
        self.contador.comparaciones += 1
        return a < b

    def push(self, num):
        self.stack.push(num)
        # if stack_min.isEmpty() or num < stack_min.top: ...
        if self.stack_min.is_empty() or self._menor(num, self.stack_min.top()):
            self.stack_min.push(num)
        else:
            self.stack_min.push(self.stack_min.top())

    def pop(self):
        if self.stack.tamano() == 0:
            raise IndexError("pop() sobre pila vacía")
        valor = self.stack.pop()
        self.stack_min.pop()
        return valor

    def min(self):
        if self.stack.tamano() == 0:
            raise IndexError("min() sobre pila vacía")
        return self.stack_min.top()


def invariante(m):
    """|stack_min| = n  y  stack_min[i] = min(stack[1..i]) para todo i."""
    s = m.stack.contenido()
    sm = m.stack_min.contenido()
    if len(s) != len(sm):
        return False
    return all(sm[i] == min(s[: i + 1]) for i in range(len(s)))


# ----------------------------------------------------------------------------
# Utilidades de formato
# ----------------------------------------------------------------------------
def fmt_ops(ops):
    partes = []
    for op in ops:
        partes.append(f"push({op[1]})" if op[0] == "push" else f"{op[0]}()")
    return ", ".join(partes)


def fmt_lista(xs):
    return "(" + ",".join(str(x) for x in xs) + ")" if xs else "vacía"


def ejecutar(ops):
    """Ejecuta las operaciones comprobando el invariante tras cada una."""
    m = MinStack()
    for k, op in enumerate(ops, start=1):
        if op[0] == "push":
            m.push(op[1])
        elif op[0] == "pop":
            m.pop()
        elif op[0] == "min":
            m.min()
        assert invariante(m), f"Invariante violado tras la operación {k}: {op}"
    return m


# ----------------------------------------------------------------------------
# Casos de prueba (C1..C8)
# ----------------------------------------------------------------------------
P, O, M = "push", "pop", "min"

CASOS = [
    # id,  qué prueba,                                      operaciones,                              stack_min esperada, min esperado
    ("C1", "primer `push` con pila vacía",
     [(P, 4)], [4], 4),
    ("C2", "orden creciente: el mínimo no cambia",
     [(P, 1), (P, 2), (P, 3)], [1, 1, 1], 1),
    ("C3", "orden decreciente: el mínimo cambia siempre",
     [(P, 3), (P, 2), (P, 1)], [3, 2, 1], 1),
    ("C4", "valores repetidos",
     [(P, 4), (P, 4), (O,), (M,)], [4], 4),
    ("C5", "ejemplo ilustrado",
     [(P, 5), (P, 3), (P, 7), (P, 3), (O,), (O,), (O,)], [5], 5),
    ("C6", "`pop` que restaura un mínimo anterior",
     [(P, 5), (P, 2), (O,), (M,)], [5], 5),
    ("C7", "vaciar la pila y volver a usarla",
     [(P, 1), (O,), (P, 9), (M,)], [9], 9),
]


def verificar_casos():
    print("=" * 78)
    print("CASOS DE PRUEBA (el invariante se comprueba tras cada operación)")
    print("=" * 78)
    filas = []
    for (cid, que, ops, esperada, esperado_min) in CASOS:
        m = ejecutar(ops)
        obtenida = m.stack_min.contenido()
        obtenido_min = m.min()
        assert obtenida == esperada, f"{cid}: stack_min {obtenida} != {esperada}"
        assert obtenido_min == esperado_min, f"{cid}: min {obtenido_min} != {esperado_min}"
        ops_txt = "ver ejemplo" if cid == "C5" else f"`{fmt_ops(ops)}`"
        sm_txt = "ver ejemplo" if cid == "C5" else fmt_lista(obtenida)
        min_txt = "ver ejemplo" if cid == "C5" else str(obtenido_min)
        filas.append(f"| {cid} | {que} | {ops_txt} | {sm_txt} | {min_txt} |")
        print(f"  {cid}: OK   stack_min = {fmt_lista(obtenida)}   min() = {obtenido_min}")

    # C8: precondición
    for nombre, f in (("pop()", lambda m: m.pop()), ("min()", lambda m: m.min())):
        try:
            f(MinStack())
        except IndexError:
            pass
        else:
            raise AssertionError(f"C8: {nombre} sobre pila vacía debió fallar")
    print("  C8: OK   pop() y min() sobre pila vacía lanzan error")
    filas.append("| C8 | precondición | `pop()` o `min()` sobre pila vacía | error | error |")

    print("\nTabla para pegar en el markdown:\n")
    print("| ID | Qué prueba | Operaciones | `stack_min` esperada | `min()` esperado |")
    print("|----|------------|-------------|----------------------|------------------|")
    for f in filas:
        print(f)


# ----------------------------------------------------------------------------
# Traza del ejemplo ilustrado
# ----------------------------------------------------------------------------
def traza_ejemplo():
    print()
    print("=" * 78)
    print("TRAZA DEL EJEMPLO ILUSTRADO (para la tabla resumen y los frames)")
    print("=" * 78)
    ops = [(P, 5), (P, 3), (P, 7), (P, 3), (O,), (O,), (O,)]
    m = MinStack()
    print("| Paso | Operación | `stack` (fondo → tope) | `stack_min` (fondo → tope) | `min()` |")
    print("|------|-----------|------------------------|----------------------------|---------|")
    print("| 0 | inicio | vacía | vacía | no definido |")
    for k, op in enumerate(ops, start=1):
        if op[0] == "push":
            m.push(op[1])
            nombre = f"`push({op[1]})`"
        else:
            m.pop()
            nombre = "`pop()`"
        assert invariante(m)
        s = m.stack.contenido()
        sm = m.stack_min.contenido()
        mn = m.min() if s else "no definido"
        print(f"| {k} | {nombre} | {' '.join(map(str, s)) or 'vacía'} | "
              f"{' '.join(map(str, sm)) or 'vacía'} | {mn} |")


# ----------------------------------------------------------------------------
# Pruebas aleatorias contra una pila ingenua
# ----------------------------------------------------------------------------
def pruebas_aleatorias(intentos=3000, largo=120, semilla=2026):
    print()
    print("=" * 78)
    print("PRUEBAS ALEATORIAS contra una pila ingenua")
    print("=" * 78)
    rnd = random.Random(semilla)
    total_ops = 0
    for _ in range(intentos):
        m = MinStack()
        ingenua = []
        rango = rnd.choice([3, 10, 1000])  # rango pequeño => muchos repetidos
        for _ in range(largo):
            r = rnd.random()
            if r < 0.5 or not ingenua:
                v = rnd.randint(-rango, rango)
                m.push(v)
                ingenua.append(v)
            elif r < 0.8:
                assert m.pop() == ingenua.pop()
            else:
                assert m.min() == min(ingenua)
            assert invariante(m)
            if ingenua:
                assert m.min() == min(ingenua)
            total_ops += 1
    print(f"  OK: {intentos} secuencias, {total_ops} operaciones, "
          f"sin discrepancias con la pila ingenua y con el invariante intacto.")


# ----------------------------------------------------------------------------
# Costo constante
# ----------------------------------------------------------------------------
def medir_costos():
    print()
    print("=" * 78)
    print("COSTO POR OPERACIÓN (primitivas de pila) según el tamaño n")
    print("=" * 78)
    print("| n | `push` | `pop` | `min` |")
    print("|---|--------|-------|-------|")
    for n in (0, 10, 1_000, 100_000):
        m = MinStack()
        for i in range(n):
            m.push(0)           # todos iguales: cada push sigue la rama "else"
        c = m.contador
        a = c.primitivas
        m.push(1)               # peor caso de push: pila no vacía y num >= mínimo
        costo_push = c.primitivas - a
        a = c.primitivas
        m.min()
        costo_min = c.primitivas - a
        a = c.primitivas
        m.pop()
        costo_pop = c.primitivas - a
        print(f"| {n} | {costo_push} | {costo_pop} | {costo_min} |")
    print("\n  (Las primitivas son push, pop, top e isEmpty. `push` usa como máximo 5:")
    print("   stack.push, isEmpty, top, top y stack_min.push; más una comparación.)")


if __name__ == "__main__":
    verificar_casos()
    traza_ejemplo()
    pruebas_aleatorias()
    medir_costos()
    print("\nTodo verificado.")
