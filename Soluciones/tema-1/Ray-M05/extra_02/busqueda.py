import random
import sys
from bisect import bisect_left
from itertools import combinations_with_replacement

from comun.tabla import tabla_md


def comparar(a, b):
    return (a > b) - (a < b)


def busqueda_binaria(A, x, comparar=comparar):
    lo, hi = 0, len(A)
    while lo < hi:
        m = (lo + hi) // 2
        r = comparar(x, A[m])
        if r == 0:
            return ("está", m)
        if r < 0:
            hi = m
        else:
            lo = m + 1
    return ("hueco", lo)


def busqueda_vigilada(A, x):
    n = len(A)
    lo, hi, vueltas = 0, n, 0
    while True:
        assert 0 <= lo <= hi <= n
        assert all(A[i] < x for i in range(lo)), "invariante: A[0:lo] < x"
        assert all(A[i] > x for i in range(hi, n)), "invariante: A[hi:n] > x"
        assert hi - lo <= n >> vueltas, "potencial: Φ_j ≤ ⌊n / 2^j⌋"
        if lo >= hi:
            return ("hueco", lo), vueltas
        m = (lo + hi) // 2
        vueltas += 1
        r = comparar(x, A[m])
        if r == 0:
            return ("está", m), vueltas
        if r < 0:
            hi = m
        else:
            lo = m + 1


def es_correcta(A, x, resultado):
    if resultado is None:
        return False
    tipo, valor = resultado
    if tipo == "está":
        return 0 <= valor < len(A) and A[valor] == x
    return x not in A and valor == bisect_left(A, x)


def cota(n):
    return n.bit_length()


def variante_lo_m(A, x):
    lo, hi, vueltas = 0, len(A), 0
    while lo < hi:
        vueltas += 1
        if vueltas > 2 * cota(len(A)) + 2:
            return None
        m = (lo + hi) // 2
        r = comparar(x, A[m])
        if r == 0:
            return ("está", m)
        if r < 0:
            hi = m
        else:
            lo = m
    return ("hueco", lo)


def variante_hi_m_menos_1(A, x):
    lo, hi = 0, len(A)
    while lo < hi:
        m = (lo + hi) // 2
        r = comparar(x, A[m])
        if r == 0:
            return ("está", m)
        if r < 0:
            hi = m - 1
        else:
            lo = m + 1
    return ("hueco", lo)


def primer_fallo_vigilado(variante, A, x):
    n = len(A)
    lo, hi, vueltas = 0, n, 0
    while lo < hi:
        m = (lo + hi) // 2
        vueltas += 1
        r = comparar(x, A[m])
        if r == 0:
            return None
        antes = hi - lo
        if r < 0:
            hi = m - 1 if variante is variante_hi_m_menos_1 else m
        else:
            lo = m if variante is variante_lo_m else m + 1
        if not all(A[i] > x for i in range(max(hi, 0), n)):
            return vueltas, f"el invariante A[hi:n] > x falla con hi = {hi}"
        if hi - lo >= antes:
            return vueltas, f"el potencial no baja: Φ = {antes} antes y {hi - lo} después"
    return None


def _exhaustivo():
    filas = []
    tamanos = [1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 31, 32, 100, 1023, 1024]
    for n in tamanos:
        A = list(range(0, 2 * n, 2))
        xs = range(-1, 2 * n)
        peor = 0
        for x in xs:
            resultado, comparaciones = busqueda_vigilada(A, x)
            assert es_correcta(A, x, resultado)
            peor = max(peor, comparaciones)
        filas.append([n, 2 * n + 1, peor, cota(n), "sí" if peor == cota(n) else "no"])
    print(tabla_md(["n", "situaciones", "peor caso medido", "⌈log₂(n+1)⌉", "coinciden"],
                   filas, "ddddc"))


def _repetidos():
    casos = 0
    for n in range(0, 9):
        for A in combinations_with_replacement(range(4), n):
            for x in range(-1, 5):
                resultado, comparaciones = busqueda_vigilada(list(A), x)
                assert es_correcta(list(A), x, resultado) and comparaciones <= cota(n)
                casos += 1
    print(f"Con valores repetidos la cuenta de situaciones cambia, así que se recorren todos los "
          f"arreglos no decrecientes de largo hasta 8 con valores en {{0, 1, 2, 3}}, con x en "
          f"{{−1, …, 4}}: {casos:,} búsquedas, todas correctas, sin que falle ningún assert y "
          f"sin pasar nunca de ⌈log₂(n+1)⌉ comparaciones.")


GENERADORES = {
    "x presente": lambda A, rng: rng.choice(A),
    "x ausente, al azar": lambda A, rng: rng.randrange(-1, 2 * len(A) + 1) | 1,
    "x menor que todos": lambda A, rng: -1,
    "x mayor que todos": lambda A, rng: 2 * len(A) + 1,
}


def _variantes():
    rng = random.Random(2)
    filas = []
    for nombre, generar in GENERADORES.items():
        casos = []
        for _ in range(4000):
            A = list(range(0, 2 * rng.randint(1, 40), 2))
            casos.append((A, generar(A, rng)))
        fallos = [100 * sum(not es_correcta(A, x, f(A, x)) for A, x in casos) / len(casos)
                  for f in (busqueda_binaria, variante_lo_m, variante_hi_m_menos_1)]
        filas.append([nombre] + [f"{p:.1f}%" for p in fallos])
    print(tabla_md(["generador", "correcta", "lo = m (no termina)",
                    "hi = m − 1 (responde mal)"], filas, "iddd"))


def _minimos():
    filas = []
    for variante, nombre in [(variante_lo_m, "lo = m"), (variante_hi_m_menos_1, "hi = m − 1")]:
        hallado = None
        for n in range(1, 6):
            A = list(range(0, 2 * n, 2))
            for x in range(-1, 2 * n):
                if not es_correcta(A, x, variante(A, x)):
                    hallado = (A, x)
                    break
            if hallado:
                break
        A, x = hallado
        salida = variante(A, x)
        vuelta, motivo = primer_fallo_vigilado(variante, A, x)
        filas.append([nombre, f"A = {A}, x = {x}",
                      "no termina" if salida is None else f"{salida[0]} {salida[1]}",
                      f"vuelta {vuelta}: {motivo}"])
    print(tabla_md(["variante", "entrada mínima", "devuelve", "lo que se rompe primero"],
                   filas, "iiii"))


SECCIONES = {
    "exhaustivo": _exhaustivo,
    "repetidos": _repetidos,
    "variantes": _variantes,
    "minimos": _minimos,
}

if __name__ == "__main__":
    SECCIONES[sys.argv[1]]()
