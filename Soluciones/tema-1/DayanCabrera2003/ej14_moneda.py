"""Ejercicio 14: la moneda falsa de Dyson. n monedas, una falsa (mas pesada o mas liviana, no se sabe), sin moneda
genuina extra; balanza con 3 resultados; hay que decir cual y en que sentido.
Estados (u, h, l, g): u desconocidas, h posibles-pesadas, l posibles-livianas, g genuinas conocidas."""
import itertools
import math
import sys
from functools import lru_cache

sys.setrecursionlimit(100000)


def kmin(n):
    k = 1
    while n > (3 ** k - 3) // 2:
        k += 1
    return k


# =====================================================================================================
#  A. La estrategia (regla explicita) a nivel de CONTADORES
# =====================================================================================================
def regla(u, h, l, g, k, raiz=False):
    """Devuelve la pesada (u1, u2, h1, h2, l1, l2, relleno) para el estado (u,h,l,g) con k pesadas por delante.
    izquierda: u1 desconocidas, h1 posibles-pesadas, l1 posibles-livianas; derecha: u2, h2, l2; 'relleno' genuinas
    en el platillo con MENOS monedas (|diferencia| = relleno)."""
    B = 3 ** (k - 1)
    if raiz:                                                   # n monedas, sin genuinas: m contra m
        n = u
        M = (3 ** (k - 1) - 1) // 2
        m = min(M, (n - 1) // 2)
        return (m, m, 0, 0, 0, 0, 0)
    if u > 0:                                                  # fase A: solo desconocidas (h = l = 0, g >= 1)
        assert h == 0 and l == 0 and g >= 1
        U = min(u, B)
        u1, u2 = (U + 1) // 2, U // 2
        return (u1, u2, 0, 0, 0, 0, u1 - u2)
    # fase B: solo posibles-pesadas y posibles-livianas
    N = h + l
    assert N >= 2
    if N == 3 ** k:
        T = 2 * B                                              # unico caso con T par forzado: p par
    else:
        T = min(N, 2 * B)
        if T % 2 == 0:
            T -= 1                                             # T impar
    c1, c2 = (T + 1) // 2, T // 2
    # p monedas H y q = T - p monedas L en la balanza
    lo, hi = max(0, T - l), min(h, T)
    if T % 2 == 0:
        p = next(x for x in range(lo, hi + 1) if x % 2 == 0)   # p par (existe: ver el texto)
    else:
        p = hi
    q = T - p
    a1 = p // 2 if p % 2 == 0 else (p + 1) // 2                # lema de colocacion
    a2 = p - a1
    b1, b2 = c1 - a1, c2 - a2
    assert min(a1, a2, b1, b2) >= 0 and b1 + b2 == q
    izquierda = a1 + b2                                        # H de la clase '>' y L de la clase '<'
    derecha = a2 + b1
    return (0, 0, a1, a2, b2, b1, abs(izquierda - derecha))


def transiciones(u, h, l, g, pes):
    """Los tres estados que resultan de la pesada (lema de transicion). Devuelve {'>':(...), '=':(...), '<':(...)}."""
    u1, u2, h1, h2, l1, l2, _ = pes
    total = u + h + l + g
    mayor = (0, u1 + h1, u2 + l2)                              # izquierda mas pesada
    menor = (0, u2 + h2, u1 + l1)
    igual = (u - u1 - u2, h - h1 - h2, l - l1 - l2)
    res = {}
    for r, (uu, hh, ll) in (('>', mayor), ('<', menor), ('=', igual)):
        res[r] = (uu, hh, ll, total - uu - hh - ll)
    return res


def resolver(u, h, l, g, k, raiz=False):
    """Aplica la regla en todos los resultados. Devuelve la profundidad usada, o None si la regla falla."""
    hip = 2 * u + h + l
    if hip <= 1:
        return 0
    if k == 0:
        return None
    pes = regla(u, h, l, g, k, raiz)
    u1, u2, h1, h2, l1, l2, pad = pes
    if pad > g:
        return None
    sL, sR = u1 + h1 + l1, u2 + h2 + l2
    if abs(sL - sR) != pad and not (pad == abs(sL - sR)):
        return None
    prof = 0
    for r, (uu, hh, ll, gg) in transiciones(u, h, l, g, pes).items():
        if 2 * uu + hh + ll > 3 ** (k - 1):
            return None
        d = resolver(uu, hh, ll, gg, k - 1)
        if d is None:
            return None
        prof = max(prof, d)
    return prof + 1


# =====================================================================================================
#  B. Busqueda minimax INDEPENDIENTE (no usa la regla): estados (u, h, l, g)
# =====================================================================================================
@lru_cache(maxsize=None)
def puede(u, h, l, g, k):
    N = 2 * u + h + l
    if N <= 1:
        return True
    if k == 0 or N > 3 ** k:
        return False
    B = 3 ** (k - 1)
    total = u + h + l + g
    for u1 in range(u + 1):
        for u2 in range(u - u1 + 1):
            U = u1 + u2
            if U > B:
                break
            for h1 in range(h + 1):
                for l2 in range(l + 1):
                    if U + h1 + l2 > B:
                        break
                    for h2 in range(h - h1 + 1):
                        for l1 in range(l - l2 + 1):
                            if U + h2 + l1 > B:
                                break
                            sL, sR = u1 + h1 + l1, u2 + h2 + l2
                            if sL + sR == 0 or abs(sL - sR) > g:
                                continue
                            if 2 * (u - U) + (h - h1 - h2) + (l - l1 - l2) > B:
                                continue
                            if not puede(0, u1 + h1, u2 + l2, total - (u1 + h1 + u2 + l2), k - 1):
                                continue
                            if not puede(0, u2 + h2, u1 + l1, total - (u2 + h2 + u1 + l1), k - 1):
                                continue
                            if puede(u - U, h - h1 - h2, l - l1 - l2,
                                     total - (u - U) - (h - h1 - h2) - (l - l1 - l2), k - 1):
                                return True
    return False


@lru_cache(maxsize=None)
def puede_solo_moneda(u, h, l, g, k):
    """Variante: basta decir CUAL es la falsa (no el sentido). Sin poda por informacion."""
    if u + h + l <= 1:
        return True
    if k == 0:
        return False
    total = u + h + l + g
    for u1 in range(u + 1):
        for u2 in range(u - u1 + 1):
            for h1 in range(h + 1):
                for h2 in range(h - h1 + 1):
                    for l1 in range(l + 1):
                        for l2 in range(l - l1 + 1):
                            sL, sR = u1 + h1 + l1, u2 + h2 + l2
                            if sL + sR == 0 or abs(sL - sR) > g:
                                continue
                            ok = True
                            for (uu, hh, ll) in ((0, u1 + h1, u2 + l2), (0, u2 + h2, u1 + l1),
                                                 (u - u1 - u2, h - h1 - h2, l - l1 - l2)):
                                if not puede_solo_moneda(uu, hh, ll, total - uu - hh - ll, k - 1):
                                    ok = False
                                    break
                            if ok:
                                return True
    return False


# =====================================================================================================
#  C. La estrategia con MONEDAS concretas; arbol de decision y simulacion de las 2n hipotesis
# =====================================================================================================
def arbol(n, k_total):
    """Construye el arbol de decision de la estrategia con monedas 0..n-1. Cada nodo interno es una pesada."""
    hojas = []
    pesadas_hechas = [0]

    def rec(U, H, L, G, k, raiz):
        hip = [(i, 'H') for i in U | H] + [(i, 'L') for i in U | L]
        if len(hip) <= 1:
            return ('hoja', hip[0] if hip else None)
        assert k >= 1
        u, h, l, g = len(U), len(H), len(L), len(G)
        u1, u2, h1, h2, l1, l2, pad = regla(u, h, l, g, k, raiz)
        Ul, Ur = sorted(U)[:u1], sorted(U)[u1:u1 + u2]
        # elegir las monedas concretas
        Hs, Ls = sorted(H), sorted(L)
        Hl, Hr = Hs[:h1], Hs[h1:h1 + h2]
        Ll, Lr = Ls[:l1], Ls[l1:l1 + l2]
        izq = Ul + Hl + Ll
        der = Ur + Hr + Lr
        Gs = sorted(G)
        if len(izq) < len(der):
            izq = izq + Gs[:len(der) - len(izq)]
        elif len(der) < len(izq):
            der = der + Gs[:len(izq) - len(der)]
        assert len(izq) == len(der) and len(izq) >= 1
        assert set(izq).isdisjoint(der)
        todas = U | H | L | G
        # resultados
        hijos = {}
        Sx, Sy = set(izq), set(der)
        for r in ('>', '=', '<'):
            if r == '>':       # izquierda mas pesada: H a la izquierda, L a la derecha
                H2 = {i for i in Sx if i in U | H}
                L2 = {i for i in Sy if i in U | L}
                U2 = set()
            elif r == '<':
                H2 = {i for i in Sy if i in U | H}
                L2 = {i for i in Sx if i in U | L}
                U2 = set()
            else:
                U2, H2, L2 = U - Sx - Sy, H - Sx - Sy, L - Sx - Sy
            G2 = todas - U2 - H2 - L2
            if 2 * len(U2) + len(H2) + len(L2) > 3 ** (k - 1):
                raise RuntimeError("clase demasiado grande")
            hijos[r] = rec(U2, H2, L2, G2, k - 1, False)
        return ('pesada', sorted(izq), sorted(der), hijos)

    return rec(set(range(n)), set(), set(), set(), k_total, True)


def profundidad(T):
    if T[0] == 'hoja':
        return 0
    return 1 + max(profundidad(h) for h in T[3].values())


def hojas_arbol(T, acc=None):
    acc = [] if acc is None else acc
    if T[0] == 'hoja':
        acc.append(T[1])
    else:
        for r in ('>', '=', '<'):
            hojas_arbol(T[3][r], acc)
    return acc


def simular(T, i, signo):
    """Sigue la estrategia con la moneda falsa i y el sentido signo ('H' o 'L'). Devuelve (hipotesis final, pesadas)."""
    pes = 0
    while T[0] == 'pesada':
        izq, der, hijos = T[1], T[2], T[3]
        if i in izq:
            r = '>' if signo == 'H' else '<'
        elif i in der:
            r = '<' if signo == 'H' else '>'
        else:
            r = '='
        T = hijos[r]
        pes += 1
    return T[1], pes


if __name__ == "__main__":
    # ------------------------------------------------------------------------------------------------ 1
    print("=== 1. n = 2 es imposible con cualquier numero de pesadas (y n = 1 tambien) ===")
    # Con n = 2 las unicas pesadas no vacias son {a} contra {b}: (a,pesada) y (b,liviana) dan el mismo resultado siempre.
    def resultado(izq, der, i, s):
        if i in izq:
            return '>' if s == 'H' else '<'
        if i in der:
            return '<' if s == 'H' else '>'
        return '='
    pes_posibles = [((), ()), ((0,), (1,)), ((1,), (0,))]
    print("  pesadas posibles con 2 monedas (mismo tamano, disjuntas):", pes_posibles)
    print("  (a,pesada) y (b,liviana) dan el MISMO resultado en todas:",
          all(resultado(a, b, 0, 'H') == resultado(a, b, 1, 'L') for a, b in pes_posibles),
          "; (a,liviana) y (b,pesada):", all(resultado(a, b, 0, 'L') == resultado(a, b, 1, 'H') for a, b in pes_posibles))
    print("  minimax: n = 1, 2 resolubles con k = 1..5 pesadas?",
          {n: any(puede(n, 0, 0, 0, k) for k in range(1, 6)) for n in (1, 2)})

    # ------------------------------------------------------------------------------------------------ 2
    print()
    print("=== 2. Busqueda minimax independiente: n_max(k) y n_max(k)+1 ===")
    print(f"  {'k':>2} {'(3^k-3)/2':>10} {'n_max (minimax)':>16} {'n_max+1 resoluble?':>20} {'2n <= 3^k mas grande':>22}")
    nmax = {}
    for k in (2, 3, 4):
        mx = max(n for n in range(3, 45) if puede(n, 0, 0, 0, k))
        nmax[k] = mx
        print(f"  {k:>2} {(3 ** k - 3) // 2:>10} {mx:>16} {str(puede(mx + 1, 0, 0, 0, k)):>20} {(3 ** k - 1) // 2:>22}")
        assert mx == (3 ** k - 3) // 2 and not puede(mx + 1, 0, 0, 0, k)
    ok_all = all((puede(n, 0, 0, 0, k) == (3 <= n <= (3 ** k - 3) // 2)) for k in (2, 3, 4) for n in range(0, 44) if n >= 3)
    print(f"  para k = 2, 3, 4 y todo 3 <= n < 44: resoluble <=> n <= (3^k - 3)/2 : {ok_all}")
    print("  n = 13 con k = 3: 2n = 26 <= 27 (pasa la informacion) y minimax dice resoluble =", puede(13, 0, 0, 0, 3))
    print("  n = 40 con k = 4: 2n = 80 <= 81 (pasa la informacion) y minimax dice resoluble =", puede(40, 0, 0, 0, 4))

    print()
    print("=== 3. Los lemas auxiliares, por minimax ===")
    print("  (i) estados (0,h,l,g): resoluble en k pesadas <=> h+l <= 3^k, salvo (1,1) con g = 0")
    for k in (1, 2, 3):
        for g in (0, 1, 2):
            malos = [(h, l) for h in range(0, 3 ** k + 1) for l in range(0, 3 ** k + 1 - h) if not puede(0, h, l, g, k)]
            # y nada con h + l > 3^k es resoluble (informacion)
            sobran = [(h, l) for h in range(0, 3 ** k + 3) for l in range(0, 3 ** k + 3)
                      if h + l > 3 ** k and h + l <= 3 ** k + 2 and puede(0, h, l, g, k)]
            print(f"     k={k}, g={g}: h+l <= 3^k pero NO resolubles: {malos};  h+l > 3^k resolubles: {sobran}")
            assert sobran == [] and malos == ([(1, 1)] if g == 0 else [])
    print("  (ii) estados (u, 0, 0, g): u maximo resoluble")
    for k in (1, 2, 3):
        for g in (0, 1, 2):
            ok = [u for u in range(0, 3 ** k) if puede(u, 0, 0, g, k)]
            print(f"     k={k}, g={g}: u resolubles = {ok}")
            if g >= 1:
                assert ok == list(range(0, (3 ** k - 1) // 2 + 1))
    print("     (con g >= 1: u <= (3^k-1)/2 para k = 1, 2, 3;  k = 4, g = 1: u=40:",
          puede(40, 0, 0, 1, 4), " u=41:", puede(41, 0, 0, 1, 4), ")")

    # ------------------------------------------------------------------------------------------------ 4
    print()
    print("=== 4. La REGLA (estrategia explicita) sobre todos los estados, a nivel de contadores ===")
    fallos = 0
    total = 0
    for k in (1, 2, 3, 4):
        for g in (1, 2, 5):
            for h in range(0, 3 ** k + 1):
                for l in range(0, 3 ** k + 1 - h):
                    if h + l <= 1:
                        continue
                    total += 1
                    d = resolver(0, h, l, g, k)
                    fallos += (d is None or d > k)
            for u in range(1, (3 ** k - 1) // 2 + 1):
                total += 1
                d = resolver(u, 0, 0, g, k)
                fallos += (d is None or d > k)
    print(f"  estados (0,h,l,g>=1), h+l <= 3^k, y (u,0,0,g>=1), u <= (3^k-1)/2, k <= 4:")
    print(f"  {total} estados; la regla falla en {fallos}")
    assert fallos == 0
    resumen = []
    for n in range(3, 123):
        k = kmin(n)
        d = resolver(n, 0, 0, 0, k, raiz=True)
        resumen.append((n, k, d))
        assert d is not None and d <= k
    print(f"  desde (n,0,0,0), 3 <= n <= 122: la regla resuelve todo n; profundidad = k(n) en "
          f"{sum(1 for n, k, d in resumen if d == k)} de {len(resumen)} valores")

    # ------------------------------------------------------------------------------------------------ 5
    print()
    print("=== 5. Simulacion exhaustiva con monedas concretas: las 2n hipotesis, 3 <= n <= 120 ===")
    print(f"  {'n':>4} {'k(n)':>5} {'peor caso':>10} {'hojas usadas':>13} {'2n':>5} {'hojas 3^k':>10}")
    detalle = {}
    for n in list(range(3, 41)) + [60, 100, 120]:
        k = kmin(n)
        T = arbol(n, k)
        peor = 0
        bien = 0
        for i in range(n):
            for s in ('H', 'L'):
                h, pes = simular(T, i, s)
                assert h == (i, s), (n, i, s, h)
                peor = max(peor, pes)
                bien += 1
        hs = [x for x in hojas_arbol(T) if x is not None]
        assert len(set(hs)) == 2 * n and bien == 2 * n and profundidad(T) <= k
        detalle[n] = (k, peor, len(hs))
        if n <= 14 or n in (39, 40, 60, 100, 120):
            print(f"  {n:>4} {k:>5} {peor:>10} {len(hs):>13} {2 * n:>5} {3 ** k:>10}")
    print("  (assert para n = 3..40, 60, 100, 120: cada una de las 2n hipotesis termina en una hoja")
    print("   distinta, con la hipotesis correcta, en <= k(n) pesadas)")
    assert all(peor == k for n, (k, peor, _) in detalle.items())
    print("  el peor caso medido es exactamente k(n) en todos los n probados.")
    print("  primer n con k(n) = k, es decir (3^(k-1)-3)/2 + 1:", [(k, (3 ** (k - 1) - 3) // 2 + 1) for k in (2, 3, 4, 5)])

    # ------------------------------------------------------------------------------------------------ 6
    print()
    print("=== 6. La pesada inicial: m contra m, y las tres clases tienen tamano PAR ===")
    print("  Tras pesar m contra m: clases '>' y '<' de 2m hipotesis, '=' de 2(n-2m). Todas pares.")
    print("  Para cada (n, k): los m con las tres clases <= 3^(k-1) (el mayor, y sus tres clases):")
    for n, k in ((12, 3), (13, 3), (13, 4), (39, 4), (40, 4), (40, 5)):
        utiles = [m for m in range(1, n // 2 + 1) if max(2 * m, 2 * (n - 2 * m)) <= 3 ** (k - 1)]
        if utiles:
            m = utiles[-1]
            print(f"  n={n:>2} k={k} (2n={2 * n:>2}, 3^(k-1)={3 ** (k - 1):>2}): m <= {m}; con m={m}: {2 * m}, {2 * m}, {2 * (n - 2 * m)}")
        else:
            print(f"  n={n:>2} k={k} (2n={2 * n:>2}, 3^(k-1)={3 ** (k - 1):>2}): NINGUN m sirve")

    # ------------------------------------------------------------------------------------------------ 7
    print()
    print("=== 7. Variantes: con una moneda genuina extra y 'basta decir cual es la falsa' ===")
    print(f"  {'k':>2} {'sin ref+sentido':>16} {'con ref+sentido':>16} {'sin ref+moneda':>15} {'con ref+moneda':>15}")
    for k in (1, 2, 3):
        a = max([n for n in range(0, 20) if puede(n, 0, 0, 0, k) and n >= 3] or [0])
        b = max([n for n in range(0, 30) if puede(n, 0, 0, 1, k)] or [0])
        c = max([n for n in range(0, 20) if puede_solo_moneda(n, 0, 0, 0, k)] or [0])
        d = max([n for n in range(0, 20) if puede_solo_moneda(n, 0, 0, 1, k)] or [0])
        print(f"  {k:>2} {a:>16} {b:>16} {c:>15} {d:>15}")
    print("  formulas: (3^k-3)/2, (3^k-1)/2, (3^k-1)/2, (3^k+1)/2")

    # ------------------------------------------------------------------------------------------------ 8
    print()
    print("=== 8. El arbol de decision para n = 12, k = 3 (las pesadas W1..W13) ===")
    T = arbol(12, 3)
    nodos = []

    def numerar(nodo):
        cola = [nodo]
        while cola:
            x = cola.pop(0)
            if x[0] == 'pesada':
                nodos.append(x)
                for r in ('>', '=', '<'):
                    cola.append(x[3][r])
    numerar(T)
    ident = {id(x): j + 1 for j, x in enumerate(nodos)}
    for j, x in enumerate(nodos, 1):
        print(f"  W{j}: {' '.join(str(c + 1) for c in x[1]):<9} | {' '.join(str(c + 1) for c in x[2])}")
    print(f"  profundidad {profundidad(T)}; hojas con hipotesis: {len([h for h in hojas_arbol(T) if h is not None])} de {3 ** 3} posibles")
    # --- tikz
    xs = {}
    contador = [0]

    def posiciones(nodo, nivel):
        if nodo[0] == 'hoja':
            xs[id(nodo)] = (contador[0], nivel)
            contador[0] += 1
            return
        hs = [nodo[3][r] for r in ('>', '=', '<')]
        for h in hs:
            posiciones(h, nivel + 1)
        xs[id(nodo)] = (sum(xs[id(h)][0] for h in hs) / 3, nivel)
    posiciones(T, 0)
    lineas = ["\\begin{tikzpicture}[x=0.52cm,y=-1.45cm,every node/.style={font=\\tiny,inner sep=1.2pt}]"]

    def dibujar(nodo):
        px, py = xs[id(nodo)]
        if nodo[0] == 'hoja':
            hip = nodo[1]
            texto = "$\\times$" if hip is None else f"{hip[0] + 1}{'p' if hip[1] == 'H' else 'l'}"
            estilo = "draw=gray,text=gray" if hip is None else "draw,fill=blue!8"
            lineas.append(f"\\node[{estilo}] at ({px:.3f},{py}) {{{texto}}};")
            return
        lineas.append(f"\\node[draw,circle,fill=orange!20] (w{ident[id(nodo)]}) at ({px:.3f},{py}) {{W{ident[id(nodo)]}}};")
        for r, simb in (('>', '>'), ('=', '='), ('<', '<')):
            h = nodo[3][r]
            hx, hy = xs[id(h)]
            lineas.append(f"\\draw (w{ident[id(nodo)]}) -- ({hx:.3f},{hy}) node[midway,fill=white,inner sep=0.5pt] {{{simb}}};")
            dibujar(h)
    dibujar(T)
    lineas.append("\\end{tikzpicture}")
    open("ej14_arbol.tex", "w").write("\n".join(lineas) + "\n")
    filas = [f"W{j} & {' '.join(str(c + 1) for c in x[1])} & {' '.join(str(c + 1) for c in x[2])} \\\\" for j, x in enumerate(nodos, 1)]
    open("ej14_pesadas.tex", "w").write("\n".join(filas) + "\n")
