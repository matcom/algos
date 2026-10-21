"""Ejercicio 8: elementos con mas de n/3 copias (Misra-Gries con dos candidatos), C3 sec. 4-5.
Invariante: el prefijo se parte en ternas de tres valores distintos mas k1 copias de c1 y k2 de c2."""
import itertools
import random
from collections import Counter

random.seed(8)


def primera_pasada(A, vigilar=False, traza=None):
    """Orden correcto: primero las dos coincidencias ACTIVAS, despues los contadores en 0."""
    c1, k1, c2, k2 = None, 0, None, 0
    for i, x in enumerate(A):
        if k1 > 0 and x == c1:
            k1 += 1
            caso = "x = c1"
        elif k2 > 0 and x == c2:
            k2 += 1
            caso = "x = c2"
        elif k1 == 0:
            c1, k1 = x, 1
            caso = "c1 libre"
        elif k2 == 0:
            c2, k2 = x, 1
            caso = "c2 libre"
        else:
            k1 -= 1
            k2 -= 1
            caso = "terna"
        if traza is not None:
            traza.append((i + 1, x, caso, c1 if k1 else "-", k1, c2 if k2 else "-", k2))
        if vigilar:
            invariante(A[:i + 1], c1, k1, c2, k2)
    return c1, k1, c2, k2


def primera_pasada_orden_malo(A, traza=None):
    """Orden equivocado: mira los contadores en 0 ANTES de las coincidencias."""
    c1, k1, c2, k2 = None, 0, None, 0
    for i, x in enumerate(A):
        if k1 == 0:
            c1, k1 = x, 1
        elif k2 == 0:
            c2, k2 = x, 1
        elif x == c1:
            k1 += 1
        elif x == c2:
            k2 += 1
        else:
            k1 -= 1
            k2 -= 1
        if traza is not None:
            traza.append((i + 1, x, c1 if k1 else "-", k1, c2 if k2 else "-", k2))
    return c1, k1, c2, k2


def candidatos(estado):
    c1, k1, c2, k2 = estado
    return {c for c, k in ((c1, k1), (c2, k2)) if k > 0}


def pesados(A):
    n = len(A)
    return {v for v, k in Counter(A).items() if 3 * k > n}


def con_verificacion(A):
    c1, k1, c2, k2 = primera_pasada(A)
    cuenta = Counter()
    for x in A:                                   # segunda pasada: dos contadores
        if (k1 > 0 and x == c1) or (k2 > 0 and x == c2):
            cuenta[x] += 1
    return {v for v, k in cuenta.items() if 3 * k > len(A)}


def sin_verificar(A):
    return candidatos(primera_pasada(A))


def se_parte_en_ternas(S):
    c = Counter(S)
    return len(S) % 3 == 0 and all(3 * k <= len(S) for k in c.values())


def invariante(prefijo, c1, k1, c2, k2):
    resto = Counter(prefijo)
    if k1 > 0:
        resto[c1] -= k1
    if k2 > 0:
        resto[c2] -= k2
    assert all(v >= 0 for v in resto.values())                         # las copias existen
    assert not (k1 > 0 and k2 > 0 and c1 == c2)                       # candidatos activos distintos
    assert se_parte_en_ternas(list(resto.elements()))                  # el resto se parte en ternas de distintos


def parte_en_ternas_bruto(S):
    """Fuerza bruta: se puede partir el multiconjunto en ternas de tres valores distintos?"""
    c = Counter(S)
    if not c:
        return True
    if sum(c.values()) % 3:
        return False
    vals = sorted(v for v in c if c[v] > 0)
    for a, b, d in itertools.combinations(vals, 3):
        c[a] -= 1
        c[b] -= 1
        c[d] -= 1
        if all(v >= 0 for v in c.values()) and parte_en_ternas_bruto(list(c.elements())):
            c[a] += 1
            c[b] += 1
            c[d] += 1
            return True
        c[a] += 1
        c[b] += 1
        c[d] += 1
    return False


print("=== 1. Lema: un multiconjunto se parte en ternas de distintos  <=>  |S| multiplo de 3 y ningun valor > |S|/3 ===")
total = 0
for tam in range(0, 10):
    for S in itertools.combinations_with_replacement("ABCD", tam):
        total += 1
        assert parte_en_ternas_bruto(list(S)) == se_parte_en_ternas(list(S)), S
print(f"  {total} multiconjuntos de tamano <= 9 sobre 4 valores: criterio == fuerza bruta")

print()
print("=== 2. Invariante vigilado con assert (primera pasada, orden correcto) ===")
prefijos = 0
for _ in range(6000):
    A = [random.choice("ABCDE"[:random.choice([2, 3, 4, 5])]) for _ in range(random.randint(1, 14))]
    primera_pasada(A, vigilar=True)
    prefijos += len(A)
print(f"  6000 arreglos aleatorios (alfabetos de 2 a 5 simbolos): invariante comprobado en {prefijos} prefijos, sin fallos")
prefijos = 0
for L in range(1, 9):
    for A in itertools.product("ABCD", repeat=L):
        primera_pasada(list(A), vigilar=True)
        prefijos += L
print(f"  exhaustivo: todos los arreglos sobre 4 simbolos de largo <= 8: {prefijos} prefijos, sin fallos")

print()
print("=== 3. Traza de un ejemplo: A = B A C A B A D A C ===")
A = list("BACABADAC")
tz = []
primera_pasada(A, traza=tz)
print("  i  x  caso      c1 k1  c2 k2")
for i, x, caso, c1, k1, c2, k2 in tz:
    print(f"  {i}  {x}  {caso:<9} {c1:>2} {k1:>2}  {c2:>2} {k2:>2}")
n = len(A)
print(f"  n = {n}, terna = 3 copias distintas; pesados (> n/3 = {n / 3:.2f}): {sorted(pesados(A))};"
      f" candidatos: {sorted(candidatos(primera_pasada(A)))}; con verificacion: {sorted(con_verificacion(A))}")

print()
print("=== 4. Correctitud contra el oraculo (con verificacion) y mitad buena del algoritmo sin verificar ===")
for L in range(1, 9):
    for A in itertools.product("ABCD", repeat=L):
        A = list(A)
        assert con_verificacion(A) == pesados(A)
        assert pesados(A) <= sin_verificar(A)             # todo pesado esta entre los candidatos
print("  todos los arreglos sobre 4 simbolos de largo <= 8: con_verificacion == oraculo; pesados contenidos en candidatos")
casos = 0
for _ in range(20000):
    alfa = random.choice([2, 3, 4, 6, 10])
    A = [random.randrange(alfa) for _ in range(random.randint(1, 40))]
    assert con_verificacion(A) == pesados(A) and pesados(A) <= sin_verificar(A)
    casos += 1
print(f"  {casos} arreglos aleatorios mas (alfabetos de 2 a 10 simbolos, largo hasta 40): sin fallos")

print()
print("=== 5. El orden equivocado de los if produce c1 == c2 y falla ===")
mal = None
for L in range(1, 8):
    for A in itertools.product("ABC", repeat=L):
        A = list(A)
        est = primera_pasada_orden_malo(A)
        if not pesados(A) <= candidatos(est):
            mal = A
            break
    if mal:
        break
print(f"  entrada mas corta (alfabeto ABC) donde falta un pesado entre los candidatos: {''.join(mal)}")
tz = []
est = primera_pasada_orden_malo(mal, traza=tz)
print("  i  x   c1 k1  c2 k2   (orden equivocado)")
for i, x, c1, k1, c2, k2 in tz:
    print(f"  {i}  {x}  {c1:>2} {k1:>2}  {c2:>2} {k2:>2}")
print(f"  candidatos finales: {sorted(candidatos(est))}; pesados: {sorted(pesados(mal))}; "
      f"con el orden correcto: {sorted(candidatos(primera_pasada(mal)))}")
fallan = 0
tot = 0
for L in range(1, 8):
    for A in itertools.product("ABC", repeat=L):
        tot += 1
        fallan += not pesados(list(A)) <= candidatos(primera_pasada_orden_malo(list(A)))
print(f"  arreglos sobre ABC de largo <= 7 donde el orden equivocado pierde un pesado: {fallan} de {tot}")

print()
print("=== 6. La version sin verificar: falsos positivos y generadores de prueba ===")
print("  Entrada mas corta con falso positivo, por tamano de alfabeto (arreglos que usan EXACTAMENTE ese numero de simbolos):")
for alfa in (2, 3, 4):
    hallado = None
    for L in range(1, 11):
        for A in itertools.product("ABCDE"[:alfa], repeat=L):
            if len(set(A)) != alfa:
                continue
            A = list(A)
            if sin_verificar(A) != pesados(A):
                hallado = A
                break
        if hallado:
            break
    if hallado:
        print(f"    {alfa} simbolos: {''.join(hallado)}  candidatos {sorted(sin_verificar(hallado))}, pesados {sorted(pesados(hallado))}")
    else:
        print(f"    {alfa} simbolos: ninguno hasta largo 10")


def dos_plantados(n):
    """Dos simbolos con n//3 + 1 copias cada uno (necesita n >= 4); el resto, de otros simbolos."""
    t = n // 3 + 1
    a, b = random.sample("ABCDE", 2)
    otros = [c for c in "CDEFGHIJ" if c not in (a, b)]
    A = [a] * t + [b] * t + [random.choice(otros) for _ in range(n - 2 * t)]
    random.shuffle(A)
    return A


def uno_plantado(n):
    t = n // 3 + 1
    a = random.choice("ABCDE")
    otros = [c for c in "ABCDEFGH" if c != a]
    A = [a] * t + [random.choice(otros) for _ in range(n - t)]
    random.shuffle(A)
    return A


def mayoria_plantada(n):
    t = n // 2 + 1
    a = random.choice("ABCDE")
    otros = [c for c in "ABCDEFGH" if c != a]
    A = [a] * t + [random.choice(otros) for _ in range(n - t)]
    random.shuffle(A)
    return A


generadores = {
    "dos plantados": dos_plantados,
    "uno plantado": uno_plantado,
    "mayoria plantada": mayoria_plantada,
    "binario": lambda n: [random.choice("AB") for _ in range(n)],
    "3 simbolos": lambda n: [random.choice("ABC") for _ in range(n)],
    "5 simbolos": lambda n: [random.choice("ABCDE") for _ in range(n)],
    "todos distintos": lambda n: random.sample("ABCDEFGHIJKLMNOPQRST", n),
}
print()
print(f"  {'generador':>17} {'sin verificar':>14} {'dos pasadas':>12}   (4000 arreglos de largo 4..15 por generador)")
random.seed(5)
tabla = {}
for nombre, g in generadores.items():
    casos = [g(random.randint(4, 15)) for _ in range(4000)]
    f_sv = sum(sin_verificar(A) != pesados(A) for A in casos) / len(casos)
    f_cv = sum(con_verificacion(A) != pesados(A) for A in casos) / len(casos)
    tabla[nombre] = (100 * f_sv, 100 * f_cv)
    print(f"  {nombre:>17} {100 * f_sv:>13.1f}% {100 * f_cv:>11.1f}%")
assert tabla["dos plantados"][0] == 0.0
print()
print("  Para los generadores de 'dos plantados': candidatos = pesados por cardinalidad (<= 2 candidatos, 2 pesados):")
ok = 0
for _ in range(20000):
    A = dos_plantados(random.randint(4, 30))
    assert len(pesados(A)) == 2 and sin_verificar(A) == pesados(A)
    ok += 1
print(f"    {ok} arreglos con exactamente dos pesados: la version sin verificar acierta siempre")

print()
print("=== 7. Alfabeto de 3 simbolos (el analogo del binario de C3): caracterizacion exacta ===")
print("  Toda terna de distintos sobre 3 simbolos tiene una copia de cada uno; luego cuenta(c_i) = k_i + T,")
print("  cuenta(v) = T para v no candidato, n = 3T + k1 + k2, y  c_i (k_i > 0) es frecuente  <=>  2 k_i > k_j.")


def regla_2k(A):
    c1, k1, c2, k2 = primera_pasada(A)
    res = set()
    if k1 > 0 and 2 * k1 > k2:
        res.add(c1)
    if k2 > 0 and 2 * k2 > k1:
        res.add(c2)
    return res


total = 0
for L in range(0, 11):
    for A in itertools.product("ABC", repeat=L):
        A = list(A)
        c1, k1, c2, k2 = primera_pasada(A)
        n = len(A)
        assert (n - k1 - k2) % 3 == 0
        T = (n - k1 - k2) // 3
        cuenta = Counter(A)
        for v in "ABC":
            esperado = T + (k1 if (k1 > 0 and v == c1) else 0) + (k2 if (k2 > 0 and v == c2) else 0)
            assert cuenta[v] == esperado, (A, v)
        assert regla_2k(A) == pesados(A)
        total += 1
print(f"  assert en los {total} arreglos sobre {{A,B,C}} de largo <= 10: cuenta(v) = T + k_i, y regla '2 k_i > k_j' == oraculo")
for L in range(0, 9):
    for A in itertools.product("AB", repeat=L):
        assert regla_2k(list(A)) == pesados(list(A))
print("  (tambien exacta con 1 y 2 simbolos: son casos de 3 simbolos con alguna cuenta en 0)")
A = list("AAABBC")
c1, k1, c2, k2 = primera_pasada(A)
print(f"  AAABBC: estado {c1}:{k1}, {c2}:{k2}, T = {(len(A) - k1 - k2) // 3};  "
      f"B: 2*{k2} > {k1}? {2 * k2 > k1} -> falso positivo del atajo; regla 2k: {sorted(regla_2k(A))}; oraculo {sorted(pesados(A))}")
print("  Con 4 o mas simbolos la regla deja de ser exacta (las ternas ya no llevan todos los simbolos):")
for alfa in (4,):
    mal = None
    for L in range(1, 9):
        for A in itertools.product("ABCD"[:alfa], repeat=L):
            if regla_2k(list(A)) != pesados(list(A)):
                mal = list(A)
                break
        if mal:
            break
    print(f"    regla 2k: entrada mas corta sobre {alfa} simbolos donde falla: {''.join(mal)}  "
          f"(estado {primera_pasada(mal)}, devuelve {sorted(regla_2k(mal))}, oraculo {sorted(pesados(mal))})")
print()
print(f"  {'simbolos':>9} {'atajo (k>0)':>12} {'regla 2k_i>k_j':>15}   (4000 arreglos de largo 4..15 por tamano de alfabeto)")
random.seed(11)
for alfa in (1, 2, 3, 4, 5, 8):
    casos = [[random.choice("ABCDEFGH"[:alfa]) for _ in range(random.randint(4, 15))] for _ in range(4000)]
    f1 = sum(sin_verificar(A) != pesados(A) for A in casos) / len(casos)
    f2 = sum(regla_2k(A) != pesados(A) for A in casos) / len(casos)
    print(f"  {alfa:>9} {100 * f1:>11.1f}% {100 * f2:>14.1f}%")
