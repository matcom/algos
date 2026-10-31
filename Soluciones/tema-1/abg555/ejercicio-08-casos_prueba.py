import importlib
import random
from collections import Counter

bm = importlib.import_module("ejercicio-08-boyer_moore")
first_pass, more_than_third, more_than_third_shortcut, oracle = (
    bm.first_pass, bm.more_than_third, bm.more_than_third_shortcut, bm.oracle)


def iguales(r1, r2):
    # el orden de la respuesta no importa
    return sorted(map(str, r1)) == sorted(map(str, r2))


def se_parte_en_triples(S):
    # Un multiconjunto se parte en triples de tres elementos distintos si y solo si
    # su tamano es multiplo de 3 y ningun elemento aparece mas de un tercio de las veces.
    return len(S) % 3 == 0 and all(3 * k <= len(S) for k in Counter(S).values())


# Generadores de arreglos (n es el largo)
def una_plantada(n, simbolos="ABCDE"):
    m = random.choice(simbolos)
    A = [m] * (n // 3 + 1) + [random.choice(simbolos) for _ in range(n - n // 3 - 1)]
    random.shuffle(A)
    return A


def dos_plantadas(n, simbolos="ABCDE"):
    # dos elementos distintos que aparecen mas de n/3 veces cada uno (necesita n = 2 o n >= 4)
    a, b = random.sample(simbolos, 2)
    k = n // 3 + 1
    A = [a] * k + [b] * k + [random.choice(simbolos) for _ in range(n - 2 * k)]
    random.shuffle(A)
    return A


largos_dos = [2] + list(range(4, 16))          # los n donde caben dos respuestas

generadores = {
    "una plantada": lambda: una_plantada(random.randint(1, 15)),
    "dos plantadas": lambda: dos_plantadas(random.choice(largos_dos)),
    "binario": lambda: [random.choice("AB") for _ in range(random.randint(1, 15))],
    "3 simbolos": lambda: [random.choice("ABC") for _ in range(random.randint(1, 15))],
    "5 simbolos": lambda: [random.choice("ABCDE") for _ in range(random.randint(1, 15))],
}

# ===============================================================
print("Prueba 1: la traza del ejemplo")
A = list("ABCAABDAB")
trace = []
first_pass(A, trace)
print(f"{'paso':>5} {'x':>3} {'cand1':>6} {'count1':>7} {'cand2':>6} {'count2':>7}")
for i, (x, (c1, k1, c2, k2)) in enumerate(zip(A, trace), start=1):
    print(f"{i:>5} {x:>3} {str(c1):>6} {k1:>7} {str(c2):>6} {k2:>7}")
print("respuesta:", more_than_third(A), " (n = 9, hace falta aparecer mas de 3 veces)")
assert more_than_third(A) == ["A"]
print("OK\n")

# ===============================================================
print("Prueba 1b: el segundo ejemplo, con dos respuestas y candidatos que cambian")
A = list("DACCCCBDBBB")
trace = []
first_pass(A, trace)
print(f"{'paso':>5} {'x':>3} {'cand1':>6} {'count1':>7} {'cand2':>6} {'count2':>7}")
for i, (x, (c1, k1, c2, k2)) in enumerate(zip(A, trace), start=1):
    print(f"{i:>5} {x:>3} {str(c1):>6} {k1:>7} {str(c2):>6} {k2:>7}")
print("respuesta:", more_than_third(A), " (n = 11, hace falta aparecer mas de 11/3, o sea 4 o mas)")
assert [t[0] for t in trace[:3]] == ["D", "D", "D"] and trace[3][0] == "C"   # cand1: D -> C
assert trace[1][2] == "A" and trace[6][2] == "B"                             # cand2: A -> B
assert iguales(more_than_third(A), ["C", "B"])
print("OK\n")

# ===============================================================
print("Prueba 2: casos borde")
casos = [
    ([], [], "arreglo vacio: no hay respuesta"),
    (["A"], ["A"], "un elemento: es respuesta (1 > 1/3)"),
    (list("AB"), ["A", "B"], "dos distintos: los dos son respuesta (1 > 2/3)"),
    (list("ABC"), [], "tres distintos: ninguno (1 no es > 1)"),
    (list("AAB"), ["A"], "A A B: solo A"),
    (list("AABBC"), ["A", "B"], "A A B B C: dos respuestas"),
    (list("AAABBBCCC"), [], "cada uno exactamente n/3 veces: ninguno"),
    ([7, 7, 1, 2, 7, 3], ["7"], "numeros: 7 aparece 3 de 6 veces"),
    (["sol", "mar", "sol", "luna", "sol"], ["sol"], "palabras"),
]
for entrada, esperado, texto in casos:
    assert iguales(more_than_third(entrada), esperado), texto
    print(f"  {texto:<52}OK")
print()

# ===============================================================
print("Prueba 3: el invariante vigilado")
# despues de cada paso, el prefijo se parte en triples de distintos,
# mas count1 copias de cand1 y count2 copias de cand2, con cand1 != cand2
random.seed(3)
prefijos = 0
for _ in range(3000):
    A = [random.choice("ABCD") for _ in range(random.randint(1, 15))]
    trace = []
    first_pass(A, trace)
    for i, (c1, k1, c2, k2) in enumerate(trace, start=1):
        resto = Counter(A[:i])
        resto[c1] -= k1
        resto[c2] -= k2
        assert c1 != c2
        assert resto[c1] >= 0 and resto[c2] >= 0
        assert se_parte_en_triples(list(resto.elements()))
        prefijos += 1
print(f"invariante comprobado en {prefijos:,} prefijos, sin fallos")
print("OK\n")

# ===============================================================
print("Prueba 4: contra el oraculo, con distintos generadores")
random.seed(4)
print(f"{'generador':>15} {'casos':>7} {'fallos':>7}")
for nombre, generar in generadores.items():
    malos = 0
    for _ in range(4000):
        A = generar()
        malos += not iguales(more_than_third(A), oracle(A))
    print(f"{nombre:>15} {4000:>7} {malos:>7}")
    assert malos == 0
print("OK\n")

# ===============================================================
print("Prueba 5: costo, comparaciones y memoria")


class Elem:
    # un elemento que cuenta cuantas veces se compara con ==
    comparaciones = 0

    def __init__(self, v):
        self.v = v

    def __eq__(self, otro):
        Elem.comparaciones += 1
        return isinstance(otro, Elem) and self.v == otro.v

    def __hash__(self):
        return hash(self.v)


random.seed(5)
print(f"{'n':>8} {'comparaciones':>14} {'por elemento':>13} {'variables':>10} {'entradas del oraculo':>21}")
for n in [10, 100, 1_000, 10_000, 100_000]:
    A = [Elem(random.randrange(n)) for _ in range(n)]
    Elem.comparaciones = 0
    more_than_third(A)
    c = Elem.comparaciones
    print(f"{n:>8,} {c:>14,} {c / n:>13.2f} {4:>10} {len(Counter(A)):>21,}")
    assert c <= 4 * n
print("OK\n")

# ===============================================================
print("Prueba 6: el atajo sin segunda pasada, con distintos generadores")
random.seed(6)
print(f"{'generador':>15} {'atajo':>8} {'dos pasadas':>12}")
for nombre, generar in generadores.items():
    casos = [generar() for _ in range(4000)]
    f_atajo = sum(not iguales(more_than_third_shortcut(A), oracle(A)) for A in casos) / 40
    f_bien = sum(not iguales(more_than_third(A), oracle(A)) for A in casos) / 40
    print(f"{nombre:>15} {f_atajo:>7.1f}% {f_bien:>11.1f}%")
    if nombre == "dos plantadas":
        assert f_atajo == 0
print("OK\n")

# ===============================================================
print("Prueba 7: el contraejemplo mas chico del atajo")
A = list("AAB")
print("A A B:", "atajo ->", more_than_third_shortcut(A), " correcto ->", oracle(A))
assert more_than_third_shortcut(A) == ["A", "B"] and oracle(A) == ["A"]
print("OK")
