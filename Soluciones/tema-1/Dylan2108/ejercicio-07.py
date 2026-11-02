"""Ejercicio 7: mediana de dos arreglos ordenados de largo n (el n-ésimo menor de los 2n).

Corre: python ejercicio-07.py
"""
import itertools, math, random
from functools import lru_cache

def par(k, n):
    """El k-ésimo eslabón de la cadena (k = 0..2n-2): un par (i, j) para comparar A[i] con B[j].
    P_{2i} = (i, n-1-i)   y   P_{2i+1} = (i, n-2-i)."""
    i = k // 2
    return (i, n - 1 - i) if k % 2 == 0 else (i, n - 2 - i)


def mediana(A, B, cmp=None):
    """Devuelve (valor, comparaciones). cmp(a, b) -> True si a <= b."""
    n = len(A)
    assert n == len(B) and n >= 1
    cuenta = [0]
    def menor_o_igual(a, b):
        cuenta[0] += 1
        return cmp(a, b) if cmp else a <= b
    # t = cantidad de eslabones verdaderos, en 0..2n-1. Invariante: P_k verdadero para k < lo,
    # falso para k >= hi (los eslabones van de verdaderos a falsos).
    lo, hi = 0, 2 * n - 1
    while lo < hi:
        m = (lo + hi) // 2
        i, j = par(m, n)
        if menor_o_igual(A[i], B[j]):
            lo = m + 1
        else:
            hi = m
    t = lo
    resultado = A[t // 2] if t % 2 == 1 else B[n - 1 - t // 2]
    return resultado, cuenta[0]


def mediana_particion(A, B):
    """La versión de "punto de corte" que circula en internet: búsqueda binaria sobre cuántos
    elementos aporta A, con dos comparaciones por paso y una al final."""
    n = len(A)
    comps = 0
    lo, hi = 0, n
    INF = float("inf")
    while True:
        i = (lo + hi) // 2
        j = n - i
        a_izq = A[i - 1] if i > 0 else -INF
        a_der = A[i] if i < n else INF
        b_izq = B[j - 1] if j > 0 else -INF
        b_der = B[j] if j < n else INF
        if i > 0 and j < n:
            comps += 1
            if a_izq > b_der:
                hi = i - 1; continue
        if j > 0 and i < n:
            comps += 1
            if b_izq > a_der:
                lo = i + 1; continue
        if i > 0 and j > 0:
            comps += 1
        return max(a_izq, b_izq), comps


def interleavings(n):
    """Todas las C(2n, n) entradas con valores 0..2n-1 distintos."""
    for S in itertools.combinations(range(2 * n), n):
        A = list(S)
        B = [v for v in range(2 * n) if v not in S]
        yield A, B


def optimo(n):
    """El mínimo número de comparaciones A_i vs B_j en el peor caso, por búsqueda en árboles de decisión."""
    ent = []
    for A, B in interleavings(n):
        med = sorted(A + B)[n - 1]
        ent.append((A, B, ("A", A.index(med)) if med in A else ("B", B.index(med))))
    @lru_cache(None)
    def alcanza(S, k):                      # ¿se resuelve el conjunto S con k comparaciones?
        salidas = {ent[s][2] for s in S}
        if len(salidas) == 1:
            return True
        if (1 << k) < len(salidas):         # la cota de información dentro de la búsqueda
            return False
        for i in range(n):
            for j in range(n):
                si = frozenset(s for s in S if ent[s][0][i] < ent[s][1][j])
                if si and si != S and alcanza(si, k - 1) and alcanza(S - si, k - 1):
                    return True
        return False
    todo = frozenset(range(len(ent)))
    k = 0
    while not alcanza(todo, k):
        k += 1
    return k


if __name__ == "__main__":
    # 1. Monotonía de la cadena: en cada entrada, los eslabones van de verdaderos a falsos
    for n in range(1, 9):
        for A, B in interleavings(n):
            v = [A[i] <= B[j] for i, j in (par(k, n) for k in range(2 * n - 1))]
            assert v == sorted(v, reverse=True)
    print("cadena monótona en todas las entradas con n <= 8")

    # 2. Correctitud exhaustiva y peor caso = ⌈log2 2n⌉
    print(f"\n{'n':>3} {'entradas':>9} {'peor caso':>10} {'⌈log2 2n⌉':>10} {'partición':>10}")
    for n in range(1, 11):
        peor = peor_p = 0
        for A, B in interleavings(n):
            esperado = sorted(A + B)[n - 1]
            m, c = mediana(A, B)
            assert m == esperado
            mp, cp = mediana_particion(A, B)
            assert mp == esperado
            peor, peor_p = max(peor, c), max(peor_p, cp)
        assert peor == math.ceil(math.log2(2 * n))
        print(f"{n:>3} {math.comb(2 * n, n):>9} {peor:>10} {math.ceil(math.log2(2 * n)):>10} {peor_p:>10}")

    # 3. Con valores repetidos y n grande (aleatorio)
    rng = random.Random(2026)
    for _ in range(20000):
        n = rng.randint(1, 300)
        R = rng.choice([3, 10, 10**9])
        A = sorted(rng.randint(0, R) for _ in range(n))
        B = sorted(rng.randint(0, R) for _ in range(n))
        m, c = mediana(A, B)
        assert m == sorted(A + B)[n - 1] and c <= math.ceil(math.log2(2 * n))
    print("\n20000 pares aleatorios (n <= 300, con y sin repetidos): correcto, nunca más de ⌈log2 2n⌉ comparaciones")

    # 4. El óptimo exacto por fuerza bruta coincide con la cota de información
    print(f"\n{'n':>3} {'óptimo (fuerza bruta)':>22} {'⌈log2 2n⌉':>10}")
    for n in range(1, 8):
        o = optimo(n)
        assert o == math.ceil(math.log2(2 * n))
        print(f"{n:>3} {o:>22} {math.ceil(math.log2(2 * n)):>10}")

    # 5. Cada una de las 2n salidas ocurre (necesario para la cota de información)
    for n in range(1, 9):
        salidas = set()
        for A, B in interleavings(n):
            med = sorted(A + B)[n - 1]
            salidas.add(("A", A.index(med)) if med in A else ("B", B.index(med)))
        assert len(salidas) == 2 * n
    print("\ncada una de las 2n posiciones es la mediana en alguna entrada (n <= 8)")

    # 6. Figura: la matriz de comparaciones A_i <= B_j, la escalera y la cadena
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.patches import Rectangle
    except ImportError:
        print("(sin matplotlib)")
    else:
        n = 8
        r = random.Random(5)
        S = sorted(r.sample(range(1, 100), 2 * n))
        A = sorted(r.sample(S, n)); B = sorted(v for v in S if v not in A)
        med, _ = mediana(A, B)
        fig, ax = plt.subplots(figsize=(6.4, 6.4))
        cadena = {par(k, n): k for k in range(2 * n - 1)}
        visitados = []
        lo, hi = 0, 2 * n - 1
        while lo < hi:
            m = (lo + hi) // 2; visitados.append(m)
            i, j = par(m, n)
            if A[i] <= B[j]: lo = m + 1
            else: hi = m
        for i in range(n):
            for j in range(n):
                v = A[i] <= B[j]
                col = "#bbf7d0" if v else "#fecaca"
                if (i, j) in cadena:
                    col = "#16a34a" if v else "#dc2626"
                ax.add_patch(Rectangle((j, i), 1, 1, fc=col, ec="white", lw=1.5))
                txt = "≤" if v else ">"
                if (i, j) in cadena and cadena[(i, j)] in visitados:
                    txt = f"#{visitados.index(cadena[(i, j)]) + 1}"
                ax.text(j + .5, i + .5, txt, ha="center", va="center", fontsize=9,
                        color="white" if (i, j) in cadena else "#555", weight="bold" if txt.startswith("#") else None)
        ax.set_xticks([j + .5 for j in range(n)], [f"B{j}\n{B[j]}" for j in range(n)], fontsize=8)
        ax.set_yticks([i + .5 for i in range(n)], [f"A{i} {A[i]}" for i in range(n)], fontsize=8)
        ax.set_xlim(0, n); ax.set_ylim(n, 0); ax.set_aspect("equal")
        ax.set_title(f"A[i] ≤ B[j]: la cadena (oscuro) cruza la escalera una vez\n"
                     f"#1..#{len(visitados)}: comparaciones de la búsqueda; mediana = {med}", fontsize=10)
        fig.tight_layout()
        fig.savefig("ejercicio-07-cadena.png", dpi=150)
        print("\nfigura: ejercicio-07-cadena.png")
