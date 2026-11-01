"""Ejercicio 14: el minimo local de un arreglo, el ciclo completo de C2.

Todo lo que afirma ejercicio-14.pdf se calcula aqui. Las secciones imprimen
'== k. titulo ==' y el PDF pega cada bloque con su nombre.
Modelo de comparaciones (C5 1): los algoritmos tocan los datos SOLO con mayor(),
que anota cada comparacion y su respuesta en c; el costo es len(c) y la transcripcion
tuple(c) es la hoja del arbol de decision. Comparar con los centinelas (+inf en
A[-1] y A[n]) no cuenta: se resuelve con los indices.

El problema completo recibe un arreglo y consultas (l, r): para cada una hay que
devolver un minimo local de A[l..r], con +inf en los bordes de la consulta. Los tres
algoritmos resuelven UNA consulta sobre la vista B = A[l..r] (ver Vista y responder).
"""
import itertools
import random


# ---- inicio de los algoritmos
def mayor(A, i, j, c):
    """La unica comparacion del modelo: es A[i] > A[j]? Cuesta 1 y se anota en c."""
    r = A[i] > A[j]
    c.append((i, j, r))
    return r


def minimo_local_barrido(A, c):
    """V0, fuerza bruta: el primer i con A[i] <= A[i+1] (n-1 comparaciones, a lo sumo)."""
    n = len(A)
    for i in range(n - 1):
        if not mayor(A, i, i + 1, c):
            return i
    return n - 1


def minimo_local_dos_vecinos(A, c):
    """V1, busqueda binaria mirando los dos vecinos de la mitad."""
    n = len(A)
    lo, hi = 0, n - 1
    while True:
        m = (lo + hi) // 2
        if m > 0 and mayor(A, m, m - 1, c):          # el vecino izquierdo es menor
            hi = m - 1
        elif m < n - 1 and mayor(A, m, m + 1, c):    # el vecino derecho es menor
            lo = m + 1
        else:                                        # ningun vecino es menor
            return m


def minimo_local(A, c):
    """V2, busqueda binaria sobre el signo de A[i] - A[i+1]: una comparacion por vuelta."""
    lo, hi = 0, len(A) - 1
    while lo < hi:
        m = (lo + hi) // 2
        if mayor(A, m, m + 1, c):                    # A baja entre m y m+1
            lo = m + 1
        else:                                        # A sube (o empata) entre m y m+1
            hi = m
    return lo
# ---- fin de los algoritmos


# ---- inicio de las versiones vigiladas
def dos_vecinos_vigilado(A):
    """V1 con su invariante comprobado en cada vuelta. Devuelve (m, vueltas)."""
    n, c = len(A), []
    lo, hi, vueltas = 0, n - 1, 0
    while True:
        # I1: ventana no vacia y el valor de afuera no es menor que el del borde
        assert 0 <= lo <= hi <= n - 1
        assert lo == 0 or A[lo - 1] >= A[lo]
        assert hi == n - 1 or A[hi + 1] >= A[hi]
        vueltas += 1
        m = (lo + hi) // 2
        antes = hi - lo                                # el potencial
        if m > 0 and mayor(A, m, m - 1, c):
            hi = m - 1
        elif m < n - 1 and mayor(A, m, m + 1, c):
            lo = m + 1
        else:
            return m, vueltas
        assert hi - lo < antes                         # el potencial baja


def un_vecino_vigilado(A):
    """V2 con su invariante comprobado en cada vuelta. Devuelve (lo, vueltas)."""
    n, c = len(A), []
    lo, hi, vueltas = 0, n - 1, 0
    while True:
        # I2: P(lo-1) es cierta y P(hi) es falsa, con P(i) = "A[i] > A[i+1]"
        assert 0 <= lo <= hi <= n - 1
        assert lo == 0 or A[lo - 1] > A[lo]
        assert hi == n - 1 or A[hi] <= A[hi + 1]
        if lo == hi:
            return lo, vueltas
        vueltas += 1
        m = (lo + hi) // 2
        antes = hi - lo
        if mayor(A, m, m + 1, c):
            lo = m + 1
        else:
            hi = m
        assert hi - lo < antes
# ---- fin de las versiones vigiladas


# ------------------------------------------------------------------ utilidades
def es_minimo_local(A, i):
    n = len(A)
    return (i == 0 or A[i - 1] >= A[i]) and (i == n - 1 or A[i + 1] >= A[i])


def minimos_locales(A):
    return [i for i in range(len(A)) if es_minimo_local(A, i)]


class Valle:
    """V_k de longitud n sin construirlo: decrece hasta k y crece despues, valores
    distintos. A[k] = 0; a la izquierda 2(k-i); a la derecha 2(i-k)-1."""
    def __init__(self, n, k):
        self.n, self.k = n, k

    def __len__(self):
        return self.n

    def __getitem__(self, i):
        k = self.k
        return 2 * (k - i) if i < k else (0 if i == k else 2 * (i - k) - 1)


def hoja(alg, A):
    """(salida, transcripcion): la hoja del arbol de decision donde cae A."""
    c = []
    salida = alg(A, c)
    return salida, tuple(c)


def costo(alg, A):
    c = []
    alg(A, c)
    return len(c)


def peor_en_valles(alg, n):
    return max(costo(alg, Valle(n, k)) for k in range(n))


def piso_log2(n):
    return n.bit_length() - 1


def techo_log2(n):
    return (n - 1).bit_length()


def es_minimo_local_consulta(A, l, r, i):
    """i es minimo local de la consulta (l, r): l <= i <= r y +inf en los bordes de la consulta."""
    return l <= i <= r and (i == l or A[i - 1] >= A[i]) and (i == r or A[i + 1] >= A[i])


# ---- inicio de las consultas
class Vista:
    """B = A[l..r] sin copiar: B[i] = A[l + i]. Una consulta (l, r) sobre A es el problema
    de un solo arreglo sobre B."""
    def __init__(self, A, l, r):
        self.A, self.l, self.n = A, l, r - l + 1

    def __len__(self):
        return self.n

    def __getitem__(self, i):
        return self.A[self.l + i]


def responder(alg, A, consultas, memoria=True):
    """Responde cada consulta (l, r) con alg sobre B = A[l..r]. Devuelve (respuestas,
    costo), con costo = comparaciones distintas de A si memoria, o todas si no."""
    respuestas, comparados, costo_total = [], set(), 0
    for l, r in consultas:
        c = []
        respuestas.append(l + alg(Vista(A, l, r), c))
        for i, j, _resultado in c:
            par = (min(i, j) + l, max(i, j) + l)
            if memoria and par in comparados:
                continue                      # la respuesta se recuerda: no cuesta
            comparados.add(par)
            costo_total += 1
    return respuestas, costo_total
# ---- fin de las consultas


# ================================================================== secciones
def seccion_1():
    print("== 1. el ejemplo: cuatro consultas y sus ganadores ==")
    A = [7, 4, 9, 6, 8, 3, 5, 2, 10, 1]
    Q = [(0, 9), (2, 6), (5, 9), (6, 6)]
    print("A =", A, " n =", len(A))
    print(f"{'(l,r)':>7} {'L':>2}  {'A[l..r]':<22} {'ganadores':<11} valores")
    for l, r in Q:
        g = [i for i in range(l, r + 1) if es_minimo_local_consulta(A, l, r, i)]
        print(f"{str((l, r)):>7} {r - l + 1:>2}  {' '.join(map(str, A[l:r + 1])):<22} "
              f"{' '.join(map(str, g)):<11} {' '.join(str(A[i]) for i in g)}")
    print(f"indice 6 (A[6] = {A[6]}, con A[5] = {A[5]} a su izquierda):")
    print(f"  minimo local de A? {es_minimo_local(A, 6)}"
          f"   ganador de la consulta (6, 6)? {es_minimo_local_consulta(A, 6, 6, 6)}")


def seccion_1c():
    print("== 1c. por que los bordes de la consulta valen +infinito ==")
    A = [7, 4, 9, 6, 8, 3, 5, 2, 10, 1]
    n = len(A)
    sin = [(l, r) for l in range(n) for r in range(l, n)
           if not any(es_minimo_local(A, i) for i in range(l, r + 1))]
    print("con los vecinos reales de A (sin paredes) habria consultas sin respuesta:")
    print(f"  en A: {len(sin)} de {n * (n + 1) // 2} consultas, p. ej. {sin[:3]}")
    C, (l, r) = [6, 4, 3], (0, 1)
    k = min(range(l, r + 1), key=lambda i: C[i])
    con = [i for i in range(l, r + 1) if es_minimo_local_consulta(C, l, r, i)]
    sin_p = [i for i in range(l, r + 1) if es_minimo_local(C, i)]
    print(f"  C = {C}, consulta {(l, r)}: el minimo del rango es C[{k}] = {C[k]}")
    print(f"  y C[{r + 1}] = {C[r + 1]} es menor; ganadores con paredes: {con}; sin paredes: {sin_p}")


def traza(alg_nombre, A):
    """Las vueltas de V1 o V2: (lo, hi, m, comparaciones de la vuelta, decision)."""
    n, filas = len(A), []
    lo, hi = 0, n - 1
    while True:
        if alg_nombre == "V2" and lo == hi:
            filas.append((lo, hi, None, [], f"devuelve {lo}"))
            return filas
        m = (lo + hi) // 2
        comps = []
        if alg_nombre == "V1":
            if m > 0:
                r = A[m] > A[m - 1]
                comps.append((m, m - 1, r))
                if r:
                    filas.append((lo, hi, m, comps, "izquierda"))
                    hi = m - 1
                    continue
            if m < n - 1:
                r = A[m] > A[m + 1]
                comps.append((m, m + 1, r))
                if r:
                    filas.append((lo, hi, m, comps, "derecha"))
                    lo = m + 1
                    continue
            filas.append((lo, hi, m, comps, f"devuelve {m}"))
            return filas
        r = A[m] > A[m + 1]
        comps.append((m, m + 1, r))
        filas.append((lo, hi, m, comps, "derecha" if r else "izquierda"))
        if r:
            lo = m + 1
        else:
            hi = m


def seccion_1b():
    print("== 1b. trazas sobre el ejemplo ==")
    A = [7, 4, 9, 6, 8, 3, 5, 2, 10, 1]
    for nombre in ("V1", "V2"):
        print(f"{nombre}: vuelta lo hi m  {'comparaciones (A[i]>A[j]?)':<30} decision")
        for t, (lo, hi, m, comps, dec) in enumerate(traza(nombre, A), 1):
            txt = "; ".join(f"A[{i}]>A[{j}] {'si' if r else 'no'}" for i, j, r in comps)
            ms = "-" if m is None else str(m)
            print(f"{'':>3}{t:>6} {lo:>2} {hi:>2} {ms:>2}  {txt:<30} {dec}")


def familias(rng):
    """Entradas de prueba: distintas, con empates, valles, monotonas, sierra."""
    for n in list(range(1, 41)) + [100, 257, 1000]:
        yield "distintos", rng.sample(range(10 * n + 10), n)
        yield "con empates", [rng.randrange(max(2, n // 4)) for _ in range(n)]
        yield "valle", [abs(i - rng.randrange(n)) for i in range(n)]
        yield "creciente", sorted(rng.sample(range(10 * n + 10), n))
        yield "decreciente", sorted(rng.sample(range(10 * n + 10), n), reverse=True)
        yield "sierra", [(i % 2) * 5 + i // 7 for i in range(n)]


def seccion_2():
    print("== 2. correctitud: pruebas ==")
    rng = random.Random(14)
    algs = (("V0 barrido", minimo_local_barrido), ("V1 dos vecinos", minimo_local_dos_vecinos),
            ("V2 un vecino", minimo_local))
    total = {nombre: [0, 0] for nombre, _ in algs}
    n_pruebas = 0
    for _tipo, A in familias(rng):
        n_pruebas += 1
        for nombre, alg in algs:
            total[nombre][0] += es_minimo_local(A, alg(A, []))
            total[nombre][1] += 1
    print(f"{n_pruebas} arreglos (distintos, con empates, valles, monotonos, sierra):")
    for nombre, (ok, t) in total.items():
        print(f"  {nombre:<15} devuelve un minimo local: {ok} de {t}")
    # todas las permutaciones
    print("todas las permutaciones de n elementos (n <= 8):")
    for nombre, alg in algs:
        ok = t = 0
        for n in range(1, 9):
            for p in itertools.permutations(range(n)):
                t += 1
                ok += es_minimo_local(list(p), alg(list(p), []))
        print(f"  {nombre:<15} {ok} de {t}")


def seccion_3():
    print("== 3. invariantes ejecutados ==")
    rng = random.Random(15)
    vueltas1 = vueltas2 = n_pruebas = 0
    for _tipo, A in familias(rng):
        n_pruebas += 1
        m, v = dos_vecinos_vigilado(A)
        assert es_minimo_local(A, m)
        vueltas1 += v
        i, v = un_vecino_vigilado(A)
        assert es_minimo_local(A, i)
        vueltas2 += v
    for n in range(1, 9):
        for p in itertools.permutations(range(n)):
            dos_vecinos_vigilado(list(p))
            un_vecino_vigilado(list(p))
            n_pruebas += 1
    print(f"{n_pruebas} arreglos; ninguna asercion salto (0 violaciones).")
    print(f"vueltas comprobadas: V1 {vueltas1}, V2 {vueltas2} (en los arreglos de familias)")


def seccion_4():
    print("== 4. costo de V0 y V1 en el peor caso ==")
    print(f"{'n':>6} {'V0':>6} {'V1':>4} {'2 floor(log2 n)+2':>18}")
    for n in (1, 2, 3, 4, 5, 8, 16, 100, 1000, 1024, 1025, 65536):
        w0 = peor_en_valles(minimo_local_barrido, n) if n <= 1025 else n - 1
        w1 = peor_en_valles(minimo_local_dos_vecinos, n)
        print(f"{n:>6} {w0:>6} {w1:>4} {2 * piso_log2(n) + 2:>18}")
    print()
    ok = True
    for n in range(1, 10):
        peor = max(costo(minimo_local_dos_vecinos, list(p))
                   for p in itertools.permutations(range(n)))
        ok = ok and peor == peor_en_valles(minimo_local_dos_vecinos, n)
    print("n <= 9: peor caso de V1 sobre TODAS las permutaciones = sobre las V_k:", ok)
    exacto = all(peor_en_valles(minimo_local_dos_vecinos, n) == 2 * piso_log2(n) + 1
                 for n in range(3, 1025))
    print("V1: peor caso = 2 floor(log2 n) + 1 para 3 <= n <= 1024:", exacto)


def seccion_5():
    print("== 5. la cota: hojas distintas ==")
    print(f"{'n':>5} {'minimos locales':>16} {'hojas V1':>9} {'altura V1':>10} {'ceil log2 n':>12}")
    for n in (2, 3, 5, 8, 13, 21, 64, 100, 257):
        unicos = all(len(minimos_locales([Valle(n, k)[i] for i in range(n)])) == 1
                     for k in range(n))
        h1 = [hoja(minimo_local_dos_vecinos, Valle(n, k)) for k in range(n)]
        print(f"{n:>5} {'1 por cada V_k' if unicos else 'MAL':>16} "
              f"{len(set(t for _s, t in h1)):>9} {max(len(t) for _s, t in h1):>10} "
              f"{techo_log2(n):>12}")


# ---- inicio de la busqueda exhaustiva
def hay_respuesta_comun(S, n, Q=None):
    """Para cada consulta (l, r) de Q, algun indice es minimo local de la consulta
    en TODAS las permutaciones de S? (Q por defecto: el arreglo entero.)"""
    Q = Q or ((0, n - 1),)
    return all(any(all(es_minimo_local_consulta(p, l, r, i) for p in S)
                   for i in range(l, r + 1)) for l, r in Q)


def resoluble(S, n, h, memo, Q=None):
    """Existe un algoritmo de comparaciones (cualquier comparacion A[i] > A[j], adaptativo)
    que resuelva TODAS las permutaciones de S con a lo sumo h comparaciones?"""
    clave = (S, h)
    if clave not in memo:
        if hay_respuesta_comun(S, n, Q):
            memo[clave] = True
        elif h == 0:
            memo[clave] = False
        else:
            memo[clave] = False
            for i, j in itertools.combinations(range(n), 2):
                si = frozenset(p for p in S if p[i] > p[j])
                no = S - si
                if si and no and resoluble(si, n, h - 1, memo, Q) and resoluble(no, n, h - 1, memo, Q):
                    memo[clave] = True
                    break
    return memo[clave]


def profundidad_optima(n, Q=None):
    S, memo = frozenset(itertools.permutations(range(n))), {}
    return next(h for h in range(n) if resoluble(S, n, h, memo, Q))
# ---- fin de la busqueda exhaustiva


def seccion_5b():
    print("== 5b. el optimo sobre todos los algoritmos, por fuerza bruta ==")
    print(f"{'n':>3} {'profundidad optima':>19} {'ceil log2 n':>12}")
    for n in range(1, 9):
        opt = profundidad_optima(n)
        assert opt == techo_log2(n)
        print(f"{n:>3} {opt:>19} {techo_log2(n):>12}")


def seccion_6():
    print("== 6. el hueco y su cierre ==")
    print(f"{'n':>5} {'hojas V2':>9} {'altura V2':>10} {'ceil log2 n':>12}")
    for n in (2, 3, 5, 8, 13, 21, 64, 100, 257):
        h2 = [hoja(minimo_local, Valle(n, k)) for k in range(n)]
        assert all(s == k for k, (s, _t) in enumerate(h2))
        print(f"{n:>5} {len(set(t for _s, t in h2)):>9} {max(len(t) for _s, t in h2):>10} "
              f"{techo_log2(n):>12}")
    print()
    print(f"{'n':>6} {'V1':>4} {'V2':>4} {'cota':>5} {'V1/cota':>8} {'V2/cota':>8}")
    for k in (2, 4, 6, 8, 10, 12, 16):
        n = 2 ** k
        w1, w2, cota = (peor_en_valles(minimo_local_dos_vecinos, n),
                        peor_en_valles(minimo_local, n), techo_log2(n))
        print(f"{n:>6} {w1:>4} {w2:>4} {cota:>5} {w1 / cota:>8.2f} {w2 / cota:>8.2f}")
    print()
    ok = True
    for n in range(1, 10):
        peor = max(costo(minimo_local, list(p)) for p in itertools.permutations(range(n)))
        ok = ok and peor == peor_en_valles(minimo_local, n)
    print("n <= 9: peor caso de V2 sobre TODAS las permutaciones = sobre las V_k:", ok)
    exacto = all(peor_en_valles(minimo_local, n) == techo_log2(n) for n in range(1, 1025))
    print("V2: peor caso = ceil(log2 n) para 1 <= n <= 1024:", exacto)


# ================================================================== varias consultas
def seccion_10():
    print("== 10. el ejemplo con consultas ==")
    A = [7, 4, 9, 6, 8, 3, 5, 2, 10, 1]
    Q = [(0, 9), (2, 6), (5, 9), (6, 6)]
    print("A =", A)
    print("consultas (l, r):", Q)
    print(f"{'(l,r)':>7} {'L':>2}  {'V2':>2} {'comp.':>5}  pares (m, m+1) comparados; * = ya comparado")
    vistos = set()
    for l, r in Q:
        c = []
        i = l + minimo_local(Vista(A, l, r), c)
        pares = [(a + l, b + l) for a, b, _r in c]
        txt = " ".join(f"({a},{b}){'*' if (a, b) in vistos else ''}" for a, b in pares)
        vistos |= set(pares)
        print(f"{str((l, r)):>7} {r - l + 1:>2}  {i:>2} {len(c):>5}  {txt or '-'}")
    _, sin = responder(minimo_local, A, Q, memoria=False)
    _, con = responder(minimo_local, A, Q, memoria=True)
    suma = sum(techo_log2(r - l + 1) for l, r in Q)
    print(f"comparaciones en total, sin recordar respuestas: {sin}")
    print(f"comparaciones en total, recordando respuestas:   {con}")
    print(f"cotas: suma de ceil(log2 L) = {suma};  n - 1 = {len(A) - 1}")


def seccion_11():
    print("== 11. consultas de rango: correctitud ==")
    rng = random.Random(16)
    algs = (("V0 barrido", minimo_local_barrido), ("V1 dos vecinos", minimo_local_dos_vecinos),
            ("V2 un vecino", minimo_local))
    ok = {nombre: 0 for nombre, _ in algs}
    consultas = reduccion = 0
    for _tipo, A in familias(rng):
        n = len(A)
        for _ in range(6):
            l = rng.randrange(n)
            r = rng.randrange(l, n)
            consultas += 1
            B = [A[i] for i in range(l, r + 1)]
            reduccion += [i for i in range(l, r + 1) if es_minimo_local_consulta(A, l, r, i)] \
                == [l + j for j in minimos_locales(B)]
            for nombre, alg in algs:
                i = responder(alg, A, [(l, r)])[0][0]
                ok[nombre] += es_minimo_local_consulta(A, l, r, i)
    print(f"{consultas} consultas (l, r) sobre los arreglos de la seccion 3:")
    for nombre, _ in algs:
        print(f"  {nombre:<15} devuelve un minimo local de la consulta: {ok[nombre]} de {consultas}")
    print("todas las permutaciones de n <= 6 y todos los rangos (l, r):")
    tot = {nombre: [0, 0] for nombre, _ in algs}
    for n in range(1, 7):
        for p in itertools.permutations(range(n)):
            for l in range(n):
                for r in range(l, n):
                    for nombre, alg in algs:
                        i = responder(alg, list(p), [(l, r)])[0][0]
                        tot[nombre][0] += es_minimo_local_consulta(list(p), l, r, i)
                        tot[nombre][1] += 1
    for nombre, _ in algs:
        print(f"  {nombre:<15} {tot[nombre][0]} de {tot[nombre][1]}")
    print(f"minimos de (l,r) en A = minimos de A[l..r] desplazados: {reduccion} de {consultas}")


def peor_v2(n, Q, memoria=True):
    """Peor caso exacto de V2 sobre las n! permutaciones, respondiendo todas las consultas."""
    return max(responder(minimo_local, list(p), Q, memoria)[1] for p in itertools.permutations(range(n)))


def seccion_12():
    print("== 12. consultas disjuntas: la suma es exacta ==")
    print(f"{'largos':>9} {'n':>2} {'suma ceil(log2 L)':>18} {'peor V2':>8} {'optimo':>7}")
    casos = [((2, 3), 0), ((3, 2), 0), ((3, 3), 0), ((2, 4), 0), ((1, 5), 0), ((2, 2, 2), 0), ((2, 3), 1)]
    for largos, hueco in casos:
        Q, pos = [], 0
        for L in largos:
            Q.append((pos, pos + L - 1))
            pos += L + hueco
        n = pos - hueco
        suma = sum(techo_log2(L) for L in largos)
        peor, opt = peor_v2(n, Q), profundidad_optima(n, tuple(Q))
        assert peor == opt == suma
        etiqueta = "+".join(map(str, largos)) + (" hueco" if hueco else "")
        print(f"{etiqueta:>9} {n:>2} {suma:>18} {peor:>8} {opt:>7}")
    print()
    print(f"{'largos':>22} {'q':>3} {'suma ceil(log2 L)':>18} {'V2 en el arreglo adversario':>28}")
    for largos in ((100, 50, 7, 1000), (64, 64, 64), (2,) * 8, (1000, 1000)):
        A, Q, pos = [], [], 0
        for j, L in enumerate(largos):
            k = max(range(L), key=lambda k: costo(minimo_local, Valle(L, k)))
            V = Valle(L, k)
            A += [j * 10 ** 6 + V[i] for i in range(L)]       # el bloque j va por encima del j-1
            Q.append((pos, pos + L - 1))
            pos += L
        suma = sum(techo_log2(L) for L in largos)
        medido = responder(minimo_local, A, Q, memoria=False)[1]
        assert medido == suma
        etiqueta = "+".join(map(str, largos)) if len(largos) < 5 else "2 x 8"
        print(f"{etiqueta:>22} {len(largos):>3} {suma:>18} {medido:>28}")


def cota_disjuntas(Q):
    """max, sobre las subfamilias de consultas disjuntas dos a dos, de la suma de ceil(log2 L)."""
    mejor = 0
    for k in range(len(Q) + 1):
        for sub in itertools.combinations(Q, k):
            if all(a[1] < b[0] or b[1] < a[0] for a, b in itertools.combinations(sub, 2)):
                mejor = max(mejor, sum(techo_log2(r - l + 1) for l, r in sub))
    return mejor


def seccion_13():
    print("== 13. consultas cualesquiera ==")
    print("cadena de consultas de largo 2: (0,1), (1,2), ..., (n-2,n-1)")
    print(f"{'n':>6} {'q':>5} {'optimo':>8} {'V2 con memoria':>15} {'V2 sin memoria':>15}")
    for n in (2, 3, 4, 5, 6, 8, 1000):
        Q = tuple((i, i + 1) for i in range(n - 1))
        if n <= 6:
            opt = profundidad_optima(n, Q)
            assert opt == n - 1
        else:
            opt = "-"
        con = responder(minimo_local, [(i * 7919) % n for i in range(n)], Q)[1]
        sin = responder(minimo_local, [(i * 7919) % n for i in range(n)], Q, memoria=False)[1]
        print(f"{n:>6} {n - 1:>5} {opt:>8} {con:>15} {sin:>15}")
    print()
    print("todos los conjuntos de consultas (n elementos, todas las permutaciones):")
    print(f"{'n':>3} {'consultas':>10} {'conjuntos':>10} {'optimo=V2':>10} {'optimo<V2':>10} "
          f"{'opt=cota inf':>13}")
    primero = None
    for n, maxq in ((4, 4), (5, 3)):
        rangos = [(l, r) for l in range(n) for r in range(l, n)]
        tot = igual = menor = exacta = 0
        for q in range(1, maxq + 1):
            for Q in itertools.combinations(rangos, q):
                opt, v2 = profundidad_optima(n, Q), peor_v2(n, Q)
                suma = sum(techo_log2(r - l + 1) for l, r in Q)
                inferior = cota_disjuntas(Q)
                assert inferior <= opt <= v2 <= min(n - 1, suma), (n, Q, inferior, opt, v2, suma)
                tot += 1
                igual += opt == v2
                menor += opt < v2
                exacta += opt == inferior
                if opt < v2 and primero is None:
                    primero = (n, Q, opt, v2)
        print(f"{n:>3} {'1 a ' + str(maxq):>10} {tot:>10} {igual:>10} {menor:>10} {exacta:>13}")
    n, Q, opt, v2 = primero
    print(f"primer caso con optimo < V2: n = {n}, Q = {list(Q)}")
    print(f"  optimo {opt}, V2 con memoria {v2}")


def main():
    for f in (seccion_1, seccion_1c, seccion_1b, seccion_2, seccion_3, seccion_4, seccion_5,
              seccion_5b, seccion_6, seccion_10, seccion_11, seccion_12, seccion_13):
        f()
        print()


if __name__ == "__main__":
    main()
