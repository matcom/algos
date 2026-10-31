import importlib
import random

pila = importlib.import_module("ejercicio-03-pila")
MinStack, NormalStack, SavingStack = pila.MinStack, pila.NormalStack, pila.SavingStack


def secuencia(n, valores):
    # n operaciones al azar
    ops, tam = [], 0
    for _ in range(n):
        if tam == 0 or random.random() < 0.55:
            ops.append(("push", valores()))
            tam += 1
        else:
            ops.append(("pop", None))
            tam -= 1
    return ops


def respuestas(P, ops):
    # aplica las operaciones y devuelve el minimo despues de cada una
    p, salida = P(), []
    for op, x in ops:
        try:
            p.push(x) if op == "push" else p.pop()
            salida.append(None if p.is_empty() else p.minimo())
        except IndexError:
            salida.append("error")
            break
    return salida


def oraculo(ops):
    # lo obvio: guardar la lista y calcular min() cada vez
    datos, salida = [], []
    for op, x in ops:
        datos.append(x) if op == "push" else datos.pop()
        salida.append(min(datos) if datos else None)
    return salida


# ===============================================================
print("Prueba 1: el ejemplo hecho a mano")
p = MinStack()
traza = [("push", 5), ("push", 3), ("push", 7), ("push", 1),
         ("pop", None), ("pop", None), ("pop", None),
         ("push", 6)]
esperado = [5, 3, 3, 1, 3, 3, 5, 5]
print(f"{'operacion':>12} {'pila (abajo -> arriba)':>24} {'minimo':>7}")
for (op, x), e in zip(traza, esperado):
    p.push(x) if op == "push" else p.pop()
    contenido = [n.value for n in p.nodes()][::-1]
    nombre = f"push {x}" if op == "push" else "pop"
    print(f"{nombre:>12} {str(contenido):>24} {p.minimo():>7}")
    assert p.minimo() == e
print("OK\n")

# ===============================================================
print("Prueba 2: casos borde")
p = MinStack()
for metodo in (p.pop, p.top, p.minimo):
    try:
        metodo()
        assert False, "tenia que dar error con la pila vacia"
    except IndexError:
        pass
print("  pila vacia: pop, top y minimo dan error                   OK")

p = MinStack()
for x in [2, 2, 2]:
    p.push(x)
for _ in range(2):
    p.pop()
    assert p.minimo() == 2
print("  repetidos [2, 2, 2]: el minimo sigue siendo 2             OK")

p = MinStack()
for x in range(10, 0, -1):          # 10, 9, ..., 1: el minimo cambia siempre
    p.push(x)
for esperado in range(2, 11):
    p.pop()
    assert p.minimo() == esperado
print("  decreciente 10..1: con cada pop el minimo vuelve a subir  OK")

p = MinStack()
for x in range(1, 11):              # 1, 2, ..., 10: el minimo nunca cambia
    p.push(x)
    assert p.minimo() == 1
print("  creciente 1..10: el minimo siempre es 1                   OK")

p = MinStack()
for x in [-3, 0, -7, 4]:
    p.push(x)
assert p.minimo() == -7 and p.top() == 4
print("  negativos [-3, 0, -7, 4]: minimo -7, top 4                OK")

p = MinStack()
for x in ["pera", "kiwi", "uva"]:
    p.push(x)
assert p.minimo() == "kiwi"
print("  palabras: minimo 'kiwi' (orden alfabetico)                OK\n")

# ===============================================================
print("Prueba 3: el invariante vigilado")
# despues de cada operacion reviso TODOS los nodos:
# el minimo guardado tiene que ser el menor de ese nodo y los de abajo
random.seed(3)
nodos_revisados = 0
for _ in range(2000):
    p = MinStack()
    for op, x in secuencia(random.randint(1, 40), lambda: random.randint(0, 20)):
        p.push(x) if op == "push" else p.pop()
        lista = list(p.nodes())                 # de arriba hacia abajo
        for i, node in enumerate(lista):
            assert node.min == min(n.value for n in lista[i:])
            nodos_revisados += 1
print(f"invariante comprobado en {nodos_revisados:,} nodos, sin fallos")
print("OK\n")

# ===============================================================
print("Prueba 4: contra el oraculo, con distintos tipos de valores")
generadores = {
    "reales distintos": lambda: random.random(),
    "enteros 0..1000": lambda: random.randint(0, 1000),
    "enteros 0..9": lambda: random.randint(0, 9),
    "solo 0 y 1": lambda: random.randint(0, 1),
}
random.seed(4)
print(f"{'valores':>18} {'secuencias':>11} {'fallos':>7}")
for nombre, valores in generadores.items():
    casos = [secuencia(random.randint(1, 60), valores) for _ in range(3000)]
    malos = sum(respuestas(MinStack, ops) != oraculo(ops) for ops in casos)
    print(f"{nombre:>18} {len(casos):>11} {malos:>7}")
    assert malos == 0
print("OK\n")

# ===============================================================
print("Prueba 5: cuantas comparaciones cuesta cada operacion")
print(f"{'n':>7} {'push':>8} {'minimo':>8} {'minimo normal':>15}")
for n in [10, 100, 1000, 10000]:
    p, q = MinStack(), NormalStack()
    peor_push = 0
    for x in range(n, 0, -1):
        antes = p.comparisons
        p.push(x)
        q.push(x)
        peor_push = max(peor_push, p.comparisons - antes)
    antes = p.comparisons
    p.minimo()
    costo_min = p.comparisons - antes
    q.minimo()
    print(f"{n:>7,} {peor_push:>8} {costo_min:>8} {q.comparisons:>15,}")
    assert peor_push <= 1 and costo_min == 0 and q.comparisons == n - 1
print("OK\n")

# ===============================================================
print("Prueba 6: la version que ahorra memoria, con <= y con <")
random.seed(6)
print(f"{'valores':>18} {'con <=':>8} {'con <':>8}")
for nombre, valores in generadores.items():
    casos = [secuencia(random.randint(1, 60), valores) for _ in range(3000)]
    bien = sum(respuestas(lambda: SavingStack(), ops) != oraculo(ops) for ops in casos)
    mal = sum(respuestas(lambda: SavingStack(strict=True), ops) != oraculo(ops)
              for ops in casos)
    print(f"{nombre:>18} {100 * bien / len(casos):>7.1f}% {100 * mal / len(casos):>7.1f}%")
    assert bien == 0
    if nombre == "reales distintos":
        assert mal == 0      # con valores distintos el error no se ve
print("OK\n")

# ===============================================================
print("Prueba 7: el contraejemplo mas chico de la version con <")
p = SavingStack(strict=True)
p.push(1)
p.push(1)
p.pop()
try:
    print("minimo =", p.minimo())
except IndexError:
    print("push 1, push 1, pop -> minimo() revienta, y en la pila queda un 1")
q = SavingStack()
q.push(1)
q.push(1)
q.pop()
assert q.minimo() == 1
print("con <= da 1, que es lo correcto")
print("OK")
