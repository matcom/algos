"""
Ejercicio 7: mediana de dos arreglos ordenados de largo n.

Problema: A y B ordenados, de largo n cada uno. Hallar el n-esimo menor de los
2n elementos. Modelo: comparaciones (solo se pregunta  x <= y ).

Uso:
    python ejercicio7_mediana.py          # corre todos los experimentos
    python ejercicio7_mediana.py --svg    # ademas genera mediana_animacion.svg
"""
import math
import random
import sys
from itertools import combinations


# --------------------------------------------------------------------------
# 1. El algoritmo
# --------------------------------------------------------------------------
def mediana(A, B, cuenta, traza=None, vigilar=False):
    """Devuelve ('A', k) o ('B', k): la mediana es A[k] o B[k] (k desde 1).

    cuenta[0] se incrementa en 1 por cada comparacion entre elementos.
    Se busca i* = cuantos de los n menores estan en A (empates: A primero).
    """
    n = len(A)
    a = lambda k: A[k - 1]          # A[k], indexando desde 1 como en la prueba
    b = lambda k: B[k - 1]

    if vigilar:
        objetivo = i_estrella(A, B)

    lo, hi = 0, n                   # invariante: lo <= i* <= hi
    while lo < hi:                  # potencial: hi - lo
        if vigilar:
            assert lo <= objetivo <= hi, "el invariante se rompio"
        mid = (lo + hi) // 2        # siempre mid < hi, asi que mid < n
        cuenta[0] += 1
        if a(mid + 1) <= b(n - mid):    # A[mid+1] esta entre los n menores
            lo = mid + 1
            r = "A[mid+1] <= B[n-mid]: i* >= mid+1"
        else:
            hi = mid
            r = "A[mid+1] >  B[n-mid]: i* <= mid"
        if traza is not None:
            traza.append((mid, r, lo, hi))

    i = lo                          # lo == hi == i*
    if vigilar:
        assert i == objetivo
    if i == 0:
        return ("B", n)
    if i == n:
        return ("A", n)
    cuenta[0] += 1                  # el n-esimo menor es el mayor de los dos ultimos
    return ("A", i) if a(i) >= b(n - i) else ("B", n - i)


def valor(A, B, pos):
    return (A if pos[0] == "A" else B)[pos[1] - 1]


# --------------------------------------------------------------------------
# 2. Oraculos (fuerza bruta)
# --------------------------------------------------------------------------
def oraculo(A, B):
    return sorted(A + B)[len(A) - 1]


def i_estrella(A, B):
    """i* por definicion: ordena con empates a favor de A y cuenta los de A."""
    etiquetados = [(x, 0, k) for k, x in enumerate(A)] + [(x, 1, k) for k, x in enumerate(B)]
    etiquetados.sort()
    return sum(1 for (_, lado, _) in etiquetados[:len(A)] if lado == 0)


def cota_algoritmo(n):
    return math.ceil(math.log2(n + 1)) + 1


def cota_informacion(n):
    return math.ceil(math.log2(2 * n))


def entradas_exhaustivas(n):
    """Todas las formas de repartir 1..2n entre A y B (valores distintos)."""
    for idx in combinations(range(1, 2 * n + 1), n):
        A = list(idx)
        B = [x for x in range(1, 2 * n + 1) if x not in idx]
        yield A, B


# --------------------------------------------------------------------------
# 3. Experimentos
# --------------------------------------------------------------------------
def exp_traza():
    print("== Traza sobre el ejemplo del .md ==")
    A, B = [1, 4, 5, 9, 12, 14], [2, 3, 7, 8, 10, 15]
    cuenta, traza = [0], []
    pos = mediana(A, B, cuenta, traza)
    print(f"A = {A}\nB = {B}\ni* = {i_estrella(A, B)}")
    for mid, r, lo, hi in traza:
        print(f"  mid={mid}: {r:38s} -> lo={lo}, hi={hi}")
    print(f"mediana = {valor(A, B, pos)} ({pos[0]}[{pos[1]}]), "
          f"comparaciones = {cuenta[0]}, oraculo = {oraculo(A, B)}\n")


def exp_correctitud():
    print("== Correctitud contra el oraculo (con muchos empates) ==")
    random.seed(7)
    for rango, etiqueta in [(5, "rango 5: muchos empates"), (10**6, "rango 1e6: casi sin empates")]:
        malos = 0
        for _ in range(20000):
            n = random.randint(1, 12)
            A = sorted(random.randrange(rango) for _ in range(n))
            B = sorted(random.randrange(rango) for _ in range(n))
            pos = mediana(A, B, [0], vigilar=True)       # vigilar: assert del invariante
            malos += valor(A, B, pos) != oraculo(A, B)
        print(f"  {etiqueta:30s} fallos: {malos} de 20000 (invariante vigilado en cada vuelta)")
    print()


def exp_costo():
    print("== Peor caso exacto (todas las entradas) vs. cotas ==")
    print(f"{'n':>3} {'entradas':>9} {'peor caso':>10} {'ceil(log2(n+1))+1':>18} {'ceil(log2 2n)':>14} {'salidas distintas':>18}")
    for n in range(1, 9):
        peor, salidas, total = 0, set(), 0
        for A, B in entradas_exhaustivas(n):
            c = [0]
            pos = mediana(A, B, c)
            assert valor(A, B, pos) == oraculo(A, B)
            peor = max(peor, c[0])
            salidas.add(pos)
            total += 1
        print(f"{n:>3} {total:>9} {peor:>10} {cota_algoritmo(n):>18} {cota_informacion(n):>14} {len(salidas):>14} (2n={2*n})")
        assert peor <= cota_algoritmo(n)
        assert len(salidas) == 2 * n            # Lema: cada posicion puede ser la mediana
    print()


def exp_errores():
    print("== Errores plantados ==")

    # (a) lo = mid en vez de mid + 1: el potencial hi - lo deja de bajar.
    def mediana_mala(A, B, limite=200):
        n = len(A)
        lo, hi, vueltas = 0, n, 0
        while lo < hi:
            vueltas += 1
            if vueltas > limite:
                return None                      # no termino
            mid = (lo + hi) // 2
            if A[mid] <= B[n - mid - 1]:
                lo = mid                         # <-- el error
            else:
                hi = mid
        return lo
    A, B = [1, 2], [3, 4]
    print(f"  (a) lo = mid, A={A}, B={B}: ", "no termina (hi - lo se queda en 1)"
          if mediana_mala(A, B) is None else "termina")

    # (b) el atajo que se salta la comparacion final.
    def atajo(A, B, cuenta):
        n = len(A)
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            cuenta[0] += 1
            if A[mid] <= B[n - mid - 1]:
                lo = mid + 1
            else:
                hi = mid
        return A[lo - 1] if lo > 0 else B[n - 1]  # devuelve A[i] sin compararlo con B[n-i]

    random.seed(3)
    print(f"  (b) atajo sin comparacion final:")
    print(f"      {'n':>3} {'comparaciones':>14} {'cota de informacion':>20} {'fallos en 3000 pruebas':>24}")
    for n in [3, 6, 12, 30]:
        malos, c = 0, [0]
        for _ in range(3000):
            A = sorted(random.sample(range(10 * n), n))
            B = sorted(random.sample(range(10 * n), n))
            c = [0]
            malos += atajo(A, B, c) != oraculo(A, B)
        print(f"      {n:>3} {c[0]:>14} {cota_informacion(n):>20} {100 * malos / 3000:>23.1f}%")
    print("      Si comparaciones < cota de informacion, esta mal sin correr nada.\n")


# --------------------------------------------------------------------------
# 4. Animacion SVG (SMIL): un cuadro por vuelta del ciclo
# --------------------------------------------------------------------------
def generar_svg(ruta="mediana_animacion.svg"):
    A, B = [1, 4, 5, 9, 12, 14], [2, 3, 7, 8, 10, 15]
    n = len(A)
    cuenta, traza = [0], []
    pos = mediana(A, B, cuenta, traza)
    cuadros, lo, hi = [], 0, n
    cuadros.append((0, lo, hi, None, "Inicio: i* esta en [0, 6]"))
    for mid, r, lo2, hi2 in traza:
        cuadros.append((1, lo2, hi2, mid, f"mid = {mid}: {r}  ->  i* en [{lo2}, {hi2}]"))
    i = traza[-1][2]
    cuadros.append((2, i, i, None, f"lo = hi = i* = {i}. mediana = max(A[{i}], B[{n - i}]) = {valor(A, B, pos)}"))

    K, T, ancho, w = len(cuadros), 3.0, 40, 46
    partes = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 250" font-family="monospace" font-size="13">',
              '<rect width="560" height="250" fill="white"/>',
              '<text x="10" y="20" font-weight="bold">Mediana de dos arreglos ordenados (n = 6)</text>']
    for k, (tipo, lo_, hi_, mid, texto) in enumerate(cuadros):
        if k == 0:
            vals, kt = "1;0", f"0;{1 / K}"
        elif k == K - 1:
            vals, kt = "0;1", f"0;{(K - 1) / K}"
        else:
            vals, kt = "0;1;0", f"0;{k / K};{(k + 1) / K}"
        g = [f'<g opacity="0"><animate attributeName="opacity" calcMode="discrete" '
             f'values="{vals}" keyTimes="{kt}" dur="{K * T}s" repeatCount="indefinite"/>']
        for fila, (nombre, arr) in enumerate([("A", A), ("B", B)]):
            y = 60 + fila * 70
            g.append(f'<text x="10" y="{y + 22}">{nombre}</text>')
            for j, x in enumerate(arr, start=1):
                tomado = (j <= (mid if mid is not None else lo_)) if nombre == "A" else \
                         (j <= n - (mid if mid is not None else lo_))
                if tipo == 2:
                    tomado = (j <= lo_) if nombre == "A" else (j <= n - lo_)
                comparado = mid is not None and ((nombre == "A" and j == mid + 1) or (nombre == "B" and j == n - mid))
                relleno = "#f4b183" if comparado else ("#bdd7ee" if tomado else "#f2f2f2")
                g.append(f'<rect x="{40 + (j - 1) * (w + 6)}" y="{y}" width="{w}" height="32" fill="{relleno}" stroke="#333"/>'
                         f'<text x="{40 + (j - 1) * (w + 6) + w / 2}" y="{y + 21}" text-anchor="middle">{x}</text>')
        g.append(f'<text x="10" y="200">lo = {lo_}, hi = {hi_}</text>')
        g.append(f'<text x="10" y="222">{texto}</text>')
        g.append('<text x="10" y="242" fill="#555">azul: los que se toman con i = mid | naranja: los que se comparan</text>')
        g.append('</g>')
        partes.append("".join(g))
    partes.append('</svg>')
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("\n".join(partes))
    print(f"SVG escrito en {ruta}")


if __name__ == "__main__":
    exp_traza()
    exp_correctitud()
    exp_costo()
    exp_errores()
    if "--svg" in sys.argv:
        generar_svg()
