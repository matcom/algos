"""Pruebas de las soluciones del Tema 1.

Hay dos clases de pruebas por ejercicio:

- `test_NN_salida`: corre `ejercicio-NN.py` y comprueba que imprime las líneas que
  cita el md. Así un número de la prosa no puede quedar desactualizado.
- las demás: llaman a las funciones del ejercicio y comprueban, en casos pequeños
  (muchas veces todos los casos de un tamaño), lo que afirman los teoremas.

Uso (sin dependencias; también funciona con pytest):
    python test_tema1.py
"""
import importlib
import math
import os
import random
import subprocess
import sys
from itertools import combinations, permutations, product
from math import comb

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

_modulos, _salidas = {}, {}


def ej(n):
    if n not in _modulos:
        _modulos[n] = importlib.import_module(f"ejercicio-{n:02d}")
    return _modulos[n]


def salida(n):
    """Lo que imprime ejercicio-NN.py, línea por línea y sin espacios repetidos."""
    if n not in _salidas:
        texto = subprocess.run([sys.executable, f"ejercicio-{n:02d}.py"], cwd=AQUI,
                               capture_output=True, text=True, check=True).stdout
        _salidas[n] = [" ".join(l.split()) for l in texto.splitlines()]
    return _salidas[n]


def imprime(n, *lineas):
    obtenidas = salida(n)
    for l in lineas:
        assert " ".join(l.split()) in obtenidas, f"ejercicio-{n:02d}.py no imprime: {l!r}"


# --------------------------------------------------------------------------
# 1. Una computadora mil veces más rápida
# --------------------------------------------------------------------------

def test_01_salida():
    imprime(1, "1e+03 31,622 31.62 31.62",
            "1e+06 31,622,776 31.62 31.62",
            "1e+09 31,622,776,601 31.62 31.62",
            "1e+03 524.5 524.5 500.0", "1e+06 679.3 679.3 666.7",
            "1e+09 757.6 757.6 750.0", "1e+12 805.1 805.1 800.0")


def test_01_ejemplos_cuadraticos():
    e = ej(1)
    assert e.mayor_n(lambda n: n ** 2, 10 ** 6) == 1000
    assert e.mayor_n(lambda n: n ** 2, 10 ** 9) == 31622      # n1 ≈ 31 623 en el md
    assert round(math.sqrt(10 ** 9)) == 31623
    assert e.mayor_n(lambda n: 4 * n ** 2, 10 ** 6) == 500
    assert round(math.sqrt(10 ** 9 / 4)) == 15811
    assert round(math.sqrt(1000 / 4), 1) == 15.8 and round(math.sqrt(4000), 1) == 63.2


def test_01_proposicion_2():
    """k está entre la cota inferior y 1000, para n0 de 2 a 10^15."""
    e = ej(1)
    for exp in range(1, 61):
        n0 = 2 ** (exp / 4) if exp > 4 else 2 ** exp
        k = e.factor_nlogn(n0)
        cota = 1000 / (1 + math.log2(1000) / math.log2(n0))
        assert cota < k < 1000
        assert abs(k * (1 + math.log2(k) / math.log2(n0)) - 1000) < 1e-6


def test_01_comprobacion_y_conferencia():
    e = ej(1)
    k = e.factor_nlogn(10 ** 6)
    assert round(math.log2(k), 2) == 9.41 and round(math.log2(10 ** 6), 2) == 19.93
    assert round(1 + 9.41 / 19.93, 3) == 1.472
    # la tabla de la Conferencia 1, §7: una hora a 10^9 operaciones por segundo
    hora = 3600 * 10 ** 9
    f = lambda n: n * math.log2(n)
    n0, n1 = e.mayor_n(f, hora), e.mayor_n(f, 1000 * hora)
    assert f"{n0:.3g}" == "9.86e+10" and f"{n1:.2g}" == "7.8e+13"
    assert round(n1 / n0) == 791                                # «factor ≈ 790»


# --------------------------------------------------------------------------
# 2. Búsqueda binaria
# --------------------------------------------------------------------------

def test_02_salida():
    imprime(2, "127 7 7 128", "peor caso = ceil(log2(n+1)) para todo 1 <= n <= 129",
            "Variante con lo = m, A = [5], x = 7: no termina")


def test_02_ejemplos():
    e = ej(2)
    A = [1, 3, 5, 7, 9, 11, 13]
    assert e.busqueda_binaria(A, 11) == (("está", 5), 2)
    assert e.busqueda_binaria(A, 8) == (("no está", None), 3)


def test_02_lema_2_con_un_algoritmo_que_salta_A5():
    """La Figura 2: sin mirar A[5] = 11, los x = 10, 11 y 12 dan lo mismo, y 11 falla."""
    e = ej(2)
    imprime(2, "x = 10: (('no está', None), 3)", "x = 11: (('no está', None), 3)",
            "x = 12: (('no está', None), 3)")
    A = [1, 3, 5, 7, 9, 11, 13]
    for x in range(0, 15):
        r, _ = e.busqueda_sin(A, 5, x)
        assert (r[0] == "está") == (x in A and x != 11)


def test_02_teoremas_1_y_2():
    """Peor caso exacto = ceil(log2(n+1)), sobre todos los elementos y huecos."""
    e = ej(2)
    for n in range(0, 70):
        A = [2 * i + 1 for i in range(n)]
        peor = 0
        for x in range(0, 2 * n + 2):
            (r, m), c = e.busqueda_binaria(A, x)
            assert (r == "está") == (x in A) and (m is None or A[m] == x)
            peor = max(peor, c)
        assert peor == math.ceil(math.log2(n + 1))


# --------------------------------------------------------------------------
# 3. Pila con mínimo
# --------------------------------------------------------------------------

def test_03_salida():
    imprime(3, "v = [5, 2, 7, 2] m = [5, 2, 2, 2] minimo() = 2",
            "tras tres pop: v = [5] m = [5] minimo() = 5",
            "operaciones comprobadas: 40582, respuestas incorrectas de minimo(): 0",
            "n = 100000: minimo() cuesta 1 operación elemental")


def test_03_invariante_en_todas_las_secuencias_cortas():
    """Todas las secuencias de hasta 7 operaciones sobre valores 0..2."""
    e = ej(3)
    ops = [("push", x) for x in range(3)] + [("pop", None)]
    for largo in range(1, 8):
        for seq in product(ops, repeat=largo):
            p, ref = e.PilaMin(), []
            for op, x in seq:
                if op == "push":
                    p.push(x); ref.append(x)
                elif ref:
                    assert p.pop() == ref.pop()
                assert p.invariante()
                if ref:
                    assert p.minimo() == min(ref)


def test_03_variante_compacta():
    """La versión que guarda solo los mínimos nuevos: con «<=» no falla en ninguna
    secuencia de hasta 7 operaciones; con «<» falla si el mínimo se repite."""
    e = ej(3)
    imprime(3, "Compacta con '<': push(2), push(2), pop() deja v = [2] m = [] minimo() = None",
            "secuencias válidas de hasta 8 operaciones: 59235; fallan con '<': 19959; con '<=': 0",
            "0..1 95.4%", "0..9 41.6%", "0..999 0.4%", "0..10^6 0.0%")
    ops = [("push", x) for x in range(3)] + [("pop", None)]
    for largo in range(1, 8):
        for seq in product(ops, repeat=largo):
            tam = 0
            for op, _ in seq:
                tam += 1 if op == "push" else -1
                if tam < 0:
                    break
            else:
                assert not e.falla_compacta(seq, estricto=False)
    assert e.falla_compacta([("push", 2), ("push", 2), ("pop", None)], estricto=True)


# --------------------------------------------------------------------------
# 4. Contador binario en una máquina de Turing
# --------------------------------------------------------------------------

def test_04_salida():
    imprime(4, "8 7 3 8 30 30",
            "m = 10: total = 36, total/m = 3.600, incremento más caro hasta ahora = 8 pasos",
            "m = 1000: total = 3988, total/m = 3.988, incremento más caro hasta ahora = 20 pasos",
            "m = 4096: total = 16382, total/m = 4.000, incremento más caro hasta ahora = 26 pasos",
            "m = 65536: total = 262142, total/m = 4.000, incremento más caro hasta ahora = 34 pasos")


def test_04_lema_1_y_teoremas():
    e = ej(4)
    cinta, cab, total, phi = {}, 0, 0, 0
    for m in range(1, 2 ** 12 + 1):
        antes = m - 1
        t = (antes ^ (antes + 1)).bit_length() - 1
        cab, pasos = e.incremento(cinta, cab)
        assert cab == 0 and pasos == 2 * t + 2                   # Lema 1
        nuevo = 2 * sum(b == "1" for b in cinta.values())
        assert pasos + nuevo - phi == 4                          # Teorema 1
        phi = nuevo
        total += pasos
        assert total == 4 * m - 2 * bin(m).count("1") < 4 * m    # Teorema 2
        assert e.valor(cinta) == m


# --------------------------------------------------------------------------
# 5. Floyd
# --------------------------------------------------------------------------

def test_05_salida():
    imprime(5, "ciclo 5 2 3 3 3", "sin ciclo 4 4 0 2 2",
            "5000 listas aleatorias: respuesta correcta, invariante y número de vueltas "
            "k* iguales a la fórmula; máx. vueltas/n = 1.00")


def test_05_todas_las_formas_pequenas():
    """Proposiciones 1 a 3 para toda cola mu <= 15 y ciclo lam <= 15."""
    e = ej(5)
    for mu in range(0, 16):
        for lam in range(0, 16):
            head, nodos = e.construir(mu, lam)
            r, v = e.floyd(head, {"nodos": nodos, "mu": mu, "lam": lam})
            n = mu + lam
            if lam == 0:
                assert r is False and v == n // 2
            else:
                k = lam * math.ceil(max(mu, 1) / lam)
                assert r is True and v == k <= n


def test_05_todas_las_listas_de_hasta_60_nodos():
    imprime(5, "todas las listas de hasta 60 nodos (1891 formas): respuesta, invariante "
            "y vueltas iguales a las fórmulas")
    assert sum(n + 1 for n in range(61)) == 1891


def test_05_sin_ciclo_nunca_coinciden_dos_nones():
    """El caso del Hecho 1: sin ciclo, fast puede llegar a None pero slow no."""
    e = ej(5)
    for n in range(1, 30):
        head, _ = e.construir(n, 0)
        slow = fast = head
        while fast is not None and fast.next is not None:
            slow, fast = slow.next, fast.next.next
            assert slow is not None and slow is not fast


# --------------------------------------------------------------------------
# 6. Matriz ordenada
# --------------------------------------------------------------------------

def test_06_salida():
    imprime(6, "x = 9: ((2, 2), 4)", "x = 15: (None, 5)", "12 300 23 23",
            "n = 8: M1 válida sin x, y las 8 matrices M2c válidas con x",
            "6.0 7.0 8.0 10.2", "7.0 8.0 10.4 11.0", "8.0 10.6 11.0 12.0",
            "10.8 11.0 12.0 13.0")


def test_06_teoremas_1_y_2_exhaustivo():
    """Todas las matrices 3x3 con los valores 1..9 crecientes por filas y columnas
    (las 42 tablas de Young), con cada x de 0 a 10."""
    e = ej(6)
    vistas = 0
    for perm in permutations(range(1, 10)):
        M = [list(perm[0:3]), list(perm[3:6]), list(perm[6:9])]
        if not e.es_creciente(M):
            continue
        vistas += 1
        for x in range(0, 11):
            pos, c = e.escalera(M, x)
            assert (pos is not None) == (1 <= x <= 9) and c <= 2 * 3 - 1
    assert vistas == 42


def test_06_escalera_mira_toda_la_antidiagonal():
    """Sobre M1 la escalera hace 2n - 1 comparaciones, por encima de la cota n."""
    e = ej(6)
    for n in range(1, 12):
        M1 = e.antidiagonal(n, 10)
        pos, c = e.escalera(M1, 10)
        assert pos is None and c == 2 * n - 1 >= n


# --------------------------------------------------------------------------
# 7. Mediana de dos arreglos
# --------------------------------------------------------------------------

def test_07_salida():
    imprime(7, "n = 4: (4, 3)", "n = 8: (8, 4)", "1000 40 11 – 11 11",
            "n = 4: posiciones distintas de la mediana observadas = 8 (2n = 8)")


def test_07_todas_las_intercalaciones():
    """Teoremas 1 y 2 sobre las C(2n, n) entradas posibles, n <= 7."""
    e = ej(7)
    for n in range(1, 8):
        posiciones = set()
        for elegidos in combinations(range(2 * n), n):
            A = list(elegidos)
            B = [v for v in range(2 * n) if v not in elegidos]
            m, c = e.mediana(A, B, vigilar=(n <= 4))
            assert m == n - 1                                 # el n-ésimo menor
            assert c == math.ceil(math.log2(n)) + 1 if n > 1 else c == 1
            posiciones.add(("A", A.index(m)) if m in A else ("B", B.index(m)))
        assert len(posiciones) == 2 * n                       # Lema 2


# --------------------------------------------------------------------------
# 8. Más de n/3 veces
# --------------------------------------------------------------------------

def test_08_salida():
    imprime(8, "Teorema comprobado en las 29523 listas con alfabeto ABC y largo 1–9",
            "plantada de dos 0.0% 0.0%", "plantada de uno 46.2% 0.0%",
            "binario 34.8% 0.0%", "3 símbolos 37.0% 0.0%", "5 símbolos 50.6% 0.0%",
            "todos distintos 53.3% 0.0%")
    assert sum(3 ** n for n in range(1, 10)) == 29523


def test_08_trazas():
    e = ej(8)
    assert e.candidatos([1, 2, 1, 2, 3, 1, 2]) == ((1, 2), (2, 2))
    assert e.candidatos([1, 2, 3, 4, 5, 1, 1]) == ((1, 1), (5, 0))
    assert e.sin_verificar([1, 2, 3, 4]) == {4} and e.oraculo([1, 2, 3, 4]) == set()
    assert e.sin_verificar([1, 2, 1, 3, 4]) == {1, 4}
    assert e.sin_verificar(list("AAAAAB")) == {"A", "B"}


def test_08_proposicion_1_exhaustiva():
    """Con exactamente dos respuestas, la versión sin verificar acierta (4 símbolos,
    largo <= 8); con una o ninguna, hay listas donde falla."""
    e = ej(8)
    falla = {0: False, 1: False}
    for n in range(1, 9):
        for L in product("ABCD", repeat=n):
            L = list(L)
            r = e.oraculo(L)
            if len(r) == 2:
                assert e.sin_verificar(L) == r
            elif e.sin_verificar(L) != r:
                falla[len(r)] = True
    assert falla == {0: True, 1: True}


# --------------------------------------------------------------------------
# 9. Mezcla «optimizada»
# --------------------------------------------------------------------------

def test_09_salida():
    imprime(9, "7 13 13 12 12 1716 3432",
            "mezcla optimizada : ([1, 2, 3, 4, 6, 5], 3)",
            "Entrada gemela A'=[1,3,6], B'=[2,4,5]: ([1, 2, 3, 4, 5, 6], 3)")


def test_09_proposiciones_exhaustivas():
    """Proposiciones 1 a 3 sobre todas las intercalaciones, n <= 8."""
    e = ej(9)
    for n in range(1, 9):
        peor_n = peor_o = malas = 0
        for elegidos in combinations(range(2 * n), n):
            A = list(elegidos)
            B = [v for v in range(2 * n) if v not in elegidos]
            m1, c1 = e.mezcla(A, B)
            m2, c2 = e.mezcla_optimizada(A, B)
            assert m1 == list(range(2 * n))
            assert (m2 == m1) == (2 * n - 1 in A)             # Proposición 3
            peor_n, peor_o = max(peor_n, c1), max(peor_o, c2)
            malas += m2 != m1
        assert peor_n == 2 * n - 1 and peor_o == max(2 * n - 2, 0)
        assert malas == comb(2 * n - 1, n) == comb(2 * n, n) // 2


def test_09_adversario():
    e = ej(9)
    A, B = [1, 3, 5], [2, 4, 6]
    vecinos = {frozenset((v, v + 1)) for v in range(1, 6)}
    assert e.pares_vecinos_comparados(A, B, e.mezcla) == vecinos
    faltan = vecinos - e.pares_vecinos_comparados(A, B, e.mezcla_optimizada)
    assert faltan == {frozenset((4, 5)), frozenset((5, 6))}


# --------------------------------------------------------------------------
# 10. Par más cercano en una dimensión
# --------------------------------------------------------------------------

def test_10_salida():
    imprime(10, "10 3,628,800 14",
            "Pares de entradas con órdenes distintos (n = 2, 3, 4): 584; su segmento pasa "
            "por una entrada con repetidos en 584",
            "3000 entradas aleatorias, sin discrepancias",
            "tras 7 y 2.5: delta = 4.5", "mejora: delta = 2.1", "mejora: delta = 0.1",
            "200 6.0 9.0 10.6 103.5 198", "1000 7.7 15.0 13.8 503.5 998",
            "3000 5.5 12.0 16.0 1503.5 2998")


def test_10_profundidad_minima():
    e = ej(10)
    assert [e.profundidad_minima(n) for n in (2, 3, 4, 5, 8, 10)] == [1, 2, 3, 5, 10, 14]
    for n in range(2, 60):                                   # Paso 7 de la Proposición 1
        assert math.factorial(n) >= (n / 2) ** (n / 2)


def test_10_rejilla_correcta():
    e = ej(10)
    rng = random.Random(1)
    for _ in range(2000):
        xs = [rng.randint(0, 60) / 2 for _ in range(rng.randint(2, 25))]
        d, _, _ = e.par_mas_cercano_1d(xs, semilla=rng.randint(0, 999))
        assert abs(d - e.por_ordenamiento(xs)) < 1e-9


def test_10_reconstrucciones_esperadas():
    """Promedio exacto sobre los 7! órdenes de llegada de 7 puntos (sin empates): es
    a lo sumo la suma de 2/i del Teorema 3. El orden adversario reconstruye siempre."""
    e = ej(10)
    xs = [0.0, 1.0, 2.7, 4.1, 6.6, 7.3, 9.9]                 # distancias todas distintas
    n = len(xs)
    total = sum(e.par_mas_cercano_1d(list(orden), barajar=False)[1]
                for orden in permutations(xs))
    assert total / math.factorial(n) <= sum(2 / i for i in range(3, n + 1)) + 1e-12
    _, rc, _ = e.par_mas_cercano_1d(e.entrada_adversaria(300), barajar=False)
    assert rc == 300 - 2


# --------------------------------------------------------------------------
# 11. Mochila
# --------------------------------------------------------------------------

def test_11_salida():
    imprime(11, "Ejemplo: n = 3, W = 5, respuesta = 7", "i = 3: [0, 0, 3, 4, 5, 7]",
            "2000 instancias aleatorias: la tabla coincide con la fuerza bruta",
            "50 562,949,953,421,312 2.25e+15", "64 9,223,372,036,854,775,808 3.69e+19",
            "1024 bits: 2^512 = 1.34e+154 divisiones")


def test_11_lema_1_contra_fuerza_bruta():
    e = ej(11)
    rng = random.Random(11)
    for _ in range(1500):
        n = rng.randint(1, 6)
        p = [rng.randint(1, 7) for _ in range(n)]
        v = [rng.randint(1, 9) for _ in range(n)]
        W = rng.randint(0, 18)
        assert e.mochila(p, v, W)[0] == e.fuerza_bruta(p, v, W)


def test_11_numeros_del_texto():
    assert 4 * (10 ** 6 + 1) == 4_000_004 and 4_000_004 / 24 > 150_000
    assert 2.25e15 / 1e9 / 86400 > 10                       # «más de 10 días»
    for b in range(1, 70):                                  # 2^(b-1) <= W < 2^b
        assert (2 ** (b - 1)).bit_length() == b == (2 ** b - 1).bit_length()


# --------------------------------------------------------------------------
# 12. Gale-Shapley con listas incompletas
# --------------------------------------------------------------------------

def test_12_salida():
    imprime(12, "Ejemplo A: ([0, 1], 3)", "Ejemplo B: ([1, None], 3)",
            "Tres proponentes, cola: [2, 1, None] iteraciones 5 bloqueantes []",
            "máx. iteraciones observadas: 28 (cota n^2 + n)",
            "proponentes que quedaron solos en total: 4482")


def test_12_estable_y_no_depende_del_orden():
    e = ej(12)
    rng = random.Random(120)
    for _ in range(1500):
        n = rng.randint(1, 6)
        listas = [rng.sample(range(n), rng.randint(0, n)) for _ in range(n)]
        pref_b = [rng.sample(range(n), n) for _ in range(n)]
        resultados = set()
        for orden, s in [("pila", 0), ("cola", 0), ("azar", 3)]:
            M, it = e.gale_shapley_incompleto(listas, pref_b, orden, s)
            assert not e.bloqueantes(listas, pref_b, M)              # Teorema 2
            assert it <= sum(map(len, listas)) + n                   # Teorema 1
            for b, a in enumerate(M):
                assert a is None or b in listas[a]                   # Lema 1
            assert len({a for a in M if a is not None}) == sum(a is not None for a in M)
            resultados.add(tuple(M))
        assert len(resultados) == 1


def test_12_potencial_del_ejemplo():
    L = [[0], [0, 1], [0]]
    assert sum(map(len, L)) + len(L) == 7


# --------------------------------------------------------------------------
# 13. Splay sobre un camino
# --------------------------------------------------------------------------

def test_13_salida():
    imprime(13, "inicio: potencial = 4.58",
            "4 8 2.00 9 9 36", "8 22 2.75 35 35 104", "16 54 3.38 135 135 272",
            "64 256 4.00 2079 2079 1600", "256 1096 4.28 32895 32895 8448",
            "1024 4478 4.37 524799 524799 41984",
            "n = 1024: splay total = 1023 (= n - 1)",
            "64 4.09", "256 5.28", "1024 6.52", "4096 7.78")


def test_13_n_igual_4():
    e = ej(13)
    total, phi0, filas = e.accesos_en_orden(4, e.splay, detalle=True)
    assert total == 8 and round(phi0, 2) == 4.58 == round(math.log2(24), 2)
    assert [f[2] for f in filas] == [3, 2, 2, 1]
    assert [round(f[4], 2) for f in filas] == [4.58, 3.00, 3.00, 4.58]
    assert [f[5] for f in filas] == [1, 2, 1, 1]                     # los s_k del texto
    assert [round(rot + phi - antes, 2) for _, _, rot, _, phi, _, antes in filas] \
        == [3.00, 0.42, 2.00, 2.58]
    assert filas[-1][3] == "4(3(2(1,.),.),.)"


def test_13_teoremas_1_y_2():
    e = ej(13)
    for n in range(3, 40):
        s, _, _ = e.accesos_en_orden(n, e.splay)
        r, _, _ = e.accesos_en_orden(n, e.subir_a_la_raiz)
        assert 2 * n - 2 <= s <= 4 * n * math.log2(n) + n            # cota inferior y Teorema 1
        assert r == (n - 1) * (n + 2) // 2                           # Teorema 2


# --------------------------------------------------------------------------
# 14. Torres de Hanoi
# --------------------------------------------------------------------------

def test_14_salida():
    imprime(14, "n = 3: 1:1->3 2:1->2 1:3->2 3:1->3 1:2->1 2:2->3 1:1->3",
            "12 4,095 4,095 4,095",
            "n = 8: Pre y Post vigiladas en 255 llamadas; 247 entran con otra varilla no vacia",
            "10 59,049 1023 1023 1 1023",
            "con 4 varillas, minimo por BFS: [1, 3, 5, 9, 13, 17, 25] "
            "(con 3 varillas: [1, 3, 7, 15, 31, 63, 127] )")


def test_14_algoritmo_y_cota():
    e = ej(14)
    for n in range(1, 9):
        movs = e.resolver(n)
        assert len(movs) == 2 ** n - 1                               # Teorema 2
        *_, final = e.estados_de(movs, n)
        assert final == (2,) * n
        assert e.bfs(n) == (2 ** n - 1, 1)                           # Teorema 3 y unicidad


def test_14_cuatro_varillas():
    e = ej(14)
    assert [e.bfs(n, 4)[0] for n in range(1, 7)] == [1, 3, 5, 9, 13, 17]


def test_14_frame_stewart():
    e = ej(14)
    imprime(14, "8 33 33 4", "9 41 41 5",
            "FS(n) - FS(n-1) = 2^t para t(t+1)/2 < n <= (t+1)(t+2)/2, n <= 60; "
            "FS(20) = 289 contra 2^20 - 1 = 1048575")
    assert [e.frame_stewart(n) for n in range(1, 10)] == [1, 3, 5, 9, 13, 17, 25, 33, 41]
    for n in range(1, 9):
        movimientos = []
        e.fs_mover(list(range(1, n + 1)), 1, 4, 2, 3, movimientos)
        assert e.simular(movimientos, n, 4)[4] == list(range(n, 0, -1))
        assert len(movimientos) == e.frame_stewart(n) == e.bfs(n, 4)[0]
        assert e.frame_stewart(n) <= 2 ** n - 1


# --------------------------------------------------------------------------

if __name__ == "__main__":
    pruebas = [(nombre, f) for nombre, f in sorted(globals().items())
               if nombre.startswith("test_") and callable(f)]
    fallas = 0
    for nombre, f in pruebas:
        try:
            f()
            print(f"ok     {nombre}")
        except AssertionError as error:
            fallas += 1
            print(f"FALLA  {nombre}: {error}")
    print(f"\n{len(pruebas) - fallas} de {len(pruebas)} pruebas pasan")
    sys.exit(1 if fallas else 0)
