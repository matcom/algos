"""Ejercicio 9: la mezcla 'optimizada' que deja de comparar cuando a A le queda un solo elemento (C5 sec. 6 y 8)."""
import itertools
import math
import random

random.seed(9)


def mezclar(A, B):
    """Mezcla normal. Devuelve (salida, comparaciones, lista de pares comparados)."""
    R, i, j, cmp_ = [], 0, 0, []
    while i < len(A) and j < len(B):
        cmp_.append((A[i], B[j]))
        if A[i] < B[j]:
            R.append(A[i])
            i += 1
        else:
            R.append(B[j])
            j += 1
    return R + A[i:] + B[j:], len(cmp_), cmp_


def mezclar_opt(A, B):
    """La variante: mientras A tenga >= 2 elementos y B no este vacia, compara; al salir, vuelca el resto de B y
    pone al final lo que quede de A (un solo elemento, o nada, o -si B se agoto- el resto normal de A)."""
    R, i, j, cmp_ = [], 0, 0, []
    while len(A) - i >= 2 and j < len(B):
        cmp_.append((A[i], B[j]))
        if A[i] < B[j]:
            R.append(A[i])
            i += 1
        else:
            R.append(B[j])
            j += 1
    return R + B[j:] + A[i:], len(cmp_), cmp_


def mezclar_ins(A, B):
    """Version CORRECTA de la idea: si a A le queda un solo elemento, se ubica por busqueda binaria en el resto de B."""
    R, i, j, cmp_ = [], 0, 0, []
    while len(A) - i >= 2 and j < len(B):
        cmp_.append((A[i], B[j]))
        if A[i] < B[j]:
            R.append(A[i])
            i += 1
        else:
            R.append(B[j])
            j += 1
    if len(A) - i == 1 and j < len(B):                   # ubicar a = A[i] en B[j:] por biseccion
        a, lo, hi = A[i], j, len(B)
        while lo < hi:
            mid = (lo + hi) // 2
            cmp_.append((a, B[mid]))
            if a < B[mid]:
                hi = mid
            else:
                lo = mid + 1
        return R + B[j:lo] + [a] + B[lo:], len(cmp_), cmp_
    return R + B[j:] + A[i:], len(cmp_), cmp_


def todas(n):
    """Todas las entradas con 2n valores distintos 0..2n-1: A = sub-conjunto de n valores, B = el resto."""
    for sub in itertools.combinations(range(2 * n), n):
        A = list(sub)
        B = [v for v in range(2 * n) if v not in sub]
        yield A, B


def cadena(n, a_primero):
    """Intercalada perfecta. a_primero: a1<b1<a2<...  si no: b1<a1<b2<..."""
    impares = list(range(1, 2 * n, 2))
    pares = list(range(2, 2 * n + 1, 2))
    if a_primero:
        A, B = impares, pares
    else:
        B, A = impares, pares
    nombres = {}
    for k in range(n):
        nombres[A[k]] = f"a{k + 1}"
        nombres[B[k]] = f"b{k + 1}"
    return A, B, nombres


print("=== 1. Especificacion en codigo y casos de borde ===")
print("  mientras len(A)-i >= 2 y j < len(B): comparar;  al salir: R += B[j:] + A[i:]")
for A, B, desc in (([5], [3], "n=1, A=[5], B=[3]"), ([3], [5], "n=1, A=[3], B=[5]"),
                   ([1, 2], [3, 4], "B no se agota antes: A < B"), ([3, 4], [1, 2], "B se agota antes: B < A"),
                   ([2], [], "B vacia, A con un elemento"), ([], [1, 2], "A vacia")):
    R, c, _ = mezclar_opt(A, B)
    N, cn, _ = mezclar(A, B)
    print(f"  {desc:<32} variante: {R} ({c} comp.)   normal: {N} ({cn} comp.)   correcta: {R == sorted(A + B)}")

print()
print("=== 2. Peor caso EXACTO de comparaciones, sobre TODAS las entradas ===")
print(f"  {'n':>2} {'entradas':>9} {'variante: max':>14} {'2n-2':>5} {'normal: max':>12} {'2n-1':>5}  entrada que alcanza 2n-2 (primera)")
for n in range(1, 9):
    mv = mn = -1
    ej = None
    cnt = 0
    for A, B in todas(n):
        cnt += 1
        cv = mezclar_opt(A, B)[1]
        cn = mezclar(A, B)[1]
        mn = max(mn, cn)
        if cv > mv:
            mv, ej = cv, (A, B)
    assert mv == 2 * n - 2 and mn == 2 * n - 1
    print(f"  {n:>2} {cnt:>9} {mv:>14} {2 * n - 2:>5} {mn:>12} {2 * n - 1:>5}  A={ej[0]} B={ej[1]}")

print()
print("=== 3. Las dos intercaladas del adversario, n = 5 ===")
informe = {}
for a_primero in (True, False):
    n = 5
    A, B, nombre = cadena(n, a_primero)
    orden = sorted(A + B)
    cadena_txt = " < ".join(nombre[v] for v in orden)
    R, c, comps = mezclar_opt(A, B)
    N, cn, _ = mezclar(A, B)
    pares_vecinos = {frozenset((nombre[orden[k]], nombre[orden[k + 1]])) for k in range(2 * n - 1)}
    comparados = {frozenset((nombre[x], nombre[y])) for x, y in comps}
    assert comparados <= pares_vecinos
    sin = sorted(tuple(sorted(p)) for p in pares_vecinos - comparados)
    print(f"  {'a-primero' if a_primero else 'b-primero'}: {cadena_txt}")
    print(f"    A = {A}  B = {B}")
    print(f"    variante: {c} comparaciones (de {2 * n - 1} pares vecinos), salida {R}  correcta: {R == orden}")
    print(f"    normal:   {cn} comparaciones, salida correcta: {N == orden}")
    print(f"    pares vecinos NUNCA comparados: {sin}")
    informe[a_primero] = (A, B, nombre, orden, comps, sin, R)
    # intercambiar los valores de cada par no comparado (como en la demostracion de C5 sec. 6)
    inv = {nm: v for v, nm in nombre.items()}
    for par in sin:
        x, y = inv[par[0]], inv[par[1]]
        A2 = [y if v == x else (x if v == y else v) for v in A]
        B2 = [y if v == x else (x if v == y else v) for v in B]
        assert A2 == sorted(A2) and B2 == sorted(B2)             # siguen ordenadas
        R2, c2, comps2 = mezclar_opt(A2, B2)
        resp1 = [(x1 < y1) for x1, y1 in comps]
        resp2 = [(x1 < y1) for x1, y1 in comps2]
        iguales = (resp1 == resp2) and (c == c2)
        correcta1, correcta2 = R == orden, R2 == sorted(A2 + B2)
        print(f"    intercambio {par[0]}<->{par[1]}: A={A2} B={B2}")
        def casilla(v, x=x, y=y):                                  # a que casilla (nombre) pertenece el valor v de la intercambiada
            return nombre[y] if v == x else (nombre[x] if v == y else nombre[v])
        misma_salida = [casilla(v) for v in R2] == [nombre[v] for v in R]
        print(f"      misma transcripcion de respuestas: {iguales}; misma salida como orden de casillas: {misma_salida}")
        print(f"      salida con valores: {R2} (original: {R}) -> correcta en la original: {correcta1}, en la intercambiada: {correcta2}")
        assert iguales and misma_salida and not (correcta1 and correcta2)

print()
print("=== 4. Cuando falla: exactamente cuando el maximo de los 2n esta en B (b_n > a_n) ===")
for n in range(1, 9):
    fallan = 0
    tot = 0
    for A, B in todas(n):
        tot += 1
        mala = mezclar_opt(A, B)[0] != sorted(A + B)
        assert mala == (B[-1] > A[-1]), (A, B)
        fallan += mala
    assert fallan == math.comb(2 * n - 1, n) == tot // 2
    print(f"  n={n}: {tot} entradas, la variante falla en {fallan} = C(2n-1,n) = la mitad exacta; falla <=> b_n > a_n (assert)")

print()
print("=== 5. Pruebas al azar: frecuencia de fallo contra la probabilidad exacta (1/2) ===")
print(f"  {'n':>5} {'pruebas':>8} {'fallos':>8} {'exacta':>8}")
for n, pruebas in ((2, 20000), (4, 20000), (16, 20000), (64, 20000), (1024, 4000)):
    fallos = 0
    for _ in range(pruebas):
        v = random.sample(range(10 * n), 2 * n)
        A, B = sorted(v[:n]), sorted(v[n:])
        fallos += mezclar_opt(A, B)[0] != sorted(v)
    print(f"  {n:>5} {pruebas:>8} {100 * fallos / pruebas:>7.2f}% {50.0:>7.2f}%")
print()
print("  Por generador (n = 16, 2000 entradas; las intercaladas y las separadas son deterministas):")
n = 16
gens = {
    "aleatoria (todas las particiones)": lambda: (lambda v: (sorted(v[:n]), sorted(v[n:])))(random.sample(range(1000), 2 * n)),
    "intercalada a1<b1<a2<...": lambda: cadena(n, True)[:2],
    "intercalada b1<a1<b2<... (la del adversario, pegada al reves)": lambda: cadena(n, False)[:2],
    "A entera menor que B": lambda: (list(range(n)), list(range(n, 2 * n))),
    "B entera menor que A": lambda: (list(range(n, 2 * n)), list(range(n))),
    "A con el maximo plantado": lambda: (lambda v: (sorted(v[:n - 1] + [10 ** 6]), sorted(v[n - 1:2 * n - 1])))(random.sample(range(1000), 2 * n - 1)),
}
for nombre, g in gens.items():
    f = 0
    for _ in range(2000):
        A, B = g()
        f += mezclar_opt(A, B)[0] != sorted(A + B)
    print(f"    {nombre:<62} falla en {100 * f / 2000:>5.1f}%")

print()
print("=== 6. Informacion: log2 C(2n,n) contra el peor caso de la variante (2n-2) ===")
print(f"  {'n':>4} {'log2 C(2n,n)':>13} {'ceil':>5} {'2n-2':>5} {'2n-1':>5}  la informacion sola refuta a la variante?")
umbral = None
for n in list(range(1, 11)) + [16, 64, 256, 1024]:
    inf = math.log2(math.comb(2 * n, n))
    refuta = math.ceil(inf) > 2 * n - 2
    if not refuta and umbral is None:
        umbral = n
    print(f"  {n:>4} {inf:>13.2f} {math.ceil(inf):>5} {2 * n - 2:>5} {2 * n - 1:>5}  {'SI (2n-2 < ceil(info))' if refuta else 'no'}")
print(f"  primer n en que ceil(log2 C(2n,n)) <= 2n-2 (la informacion deja de detectarla): n = {umbral}")
assert all(math.ceil(math.log2(math.comb(2 * n, n))) <= 2 * n - 2 for n in range(umbral, 400))

print()
print("=== 7. La version correcta: ubicar el ultimo elemento de A por biseccion en lo que queda de B ===")
print(f"  {'n':>2} {'correcta en todas':>18} {'peor caso':>10} {'2n-1':>5}")
for n in range(1, 8):
    ok = True
    peor = 0
    for A, B in todas(n):
        R, c, _ = mezclar_ins(A, B)
        ok &= R == sorted(A + B)
        peor = max(peor, c)
    assert ok and peor == 2 * n - 1
    print(f"  {n:>2} {str(ok):>18} {peor:>10} {2 * n - 1:>5}")


# ---- figuras tikz generadas desde las ejecuciones reales (n = 5)
def figura(a_primero, archivo):
    n = 5
    A, B, nombre, orden, comps, sin, R = informe[a_primero]
    pos = {nombre[v]: k + 1 for k, v in enumerate(orden)}
    lineas = ["\\begin{tikzpicture}[x=0.82cm,y=1.25cm,every node/.style={font=\\small,inner sep=1.5pt}]"]
    for k in range(1, n + 1):
        lineas.append(f"\\node (a{k}) at ({pos['a' + str(k)]},1) {{$a_{k}$}};")
        lineas.append(f"\\node (b{k}) at ({pos['b' + str(k)]},0) {{$b_{k}$}};")
    vistos = set()
    for x, y in comps:
        p = frozenset((nombre[x], nombre[y]))
        if p in vistos:
            continue
        vistos.add(p)
        u, v = sorted(p)
        lineas.append(f"\\draw[thick] ({u}) -- ({v});")
    for u, v in sin:
        lineas.append(f"\\draw[red,very thick,dashed] ({u}) -- ({v});")
    lineas.append(f"\\node[anchor=west,font=\\scriptsize] at (11,0.5) {{{len(vistos)} comparaciones, {len(sin)} par(es) sin comparar}};")
    lineas.append("\\end{tikzpicture}")
    with open(archivo, "w") as fh:
        fh.write("\n".join(lineas) + "\n")


figura(True, "ej09_fig_a.tex")
figura(False, "ej09_fig_b.tex")
