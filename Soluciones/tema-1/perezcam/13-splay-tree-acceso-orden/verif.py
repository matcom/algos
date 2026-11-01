"""Ejercicio 13 (C4): splay tree, acceso a 1..n en orden desde un camino.

Todo lo que afirma ejercicio-13.pdf se calcula aqui. Las secciones imprimen
'== k. titulo ==' y el PDF pega trozos literales de esa salida (sin el titulo).
Modelo de costo (C4 4): rotaciones, y 1 cuando el nodo ya es la raiz.
"""
import math
import random
from functools import lru_cache


# ---- inicio del splay (C4 4; splay devuelve las rotaciones)
class Nodo:
    def __init__(self, clave):
        self.clave, self.izq, self.der, self.padre = clave, None, None, None


def rotar(x):
    """Sube x un nivel rotando la arista con su padre. Preserva el orden."""
    p, g = x.padre, x.padre.padre
    if p.izq is x:
        p.izq, x.der = x.der, p
        if p.izq:
            p.izq.padre = p
    else:
        p.der, x.izq = x.izq, p
        if p.der:
            p.der.padre = p
    p.padre, x.padre = x, g
    if g:
        if g.izq is p:
            g.izq = x
        else:
            g.der = x


def splay(x):
    rotaciones = 0
    while x.padre:
        p, g = x.padre, x.padre.padre
        if g is None:                                       # zig
            rotar(x)
            rotaciones += 1
        elif (g.izq is p) == (p.izq is x):                  # zig-zig: primero el padre
            rotar(p)
            rotar(x)
            rotaciones += 2
        else:                                               # zig-zag
            rotar(x)
            rotar(x)
            rotaciones += 2
    return rotaciones


def subir_a_la_raiz(x):
    rotaciones = 0
    while x.padre:
        rotar(x)
        rotaciones += 1
    return rotaciones


def buscar(raiz, clave):
    x = raiz
    while x.clave != clave:
        x = x.izq if clave < x.clave else x.der
    return x


def camino(n):
    """Arbol inicial (el de mayor potencial): n en la raiz, cada clave hija izquierda de la siguiente."""
    nodos = [Nodo(k) for k in range(1, n + 1)]
    for k in range(1, n):
        nodos[k].izq, nodos[k - 1].padre = nodos[k - 1], nodos[k]
    return nodos[-1]
# ---- fin del splay


# ---- inicio de la pasada
def pasada(raiz, n, reorganizar=splay):
    """Accede a 1, 2, ..., n en orden. Devuelve (raiz final, costo de cada acceso)."""
    costos = []
    for clave in range(1, n + 1):
        x = buscar(raiz, clave)
        costos.append(max(reorganizar(x), 1))
        raiz = x
    return raiz, costos
# ---- fin de la pasada


# ---------------------------------------------------------------- utilidades
def tamanos(raiz):
    """Tamano del subarbol de cada nodo (iterativo)."""
    orden, pila = [], [raiz]
    while pila:
        v = pila.pop()
        orden.append(v)
        pila += [h for h in (v.izq, v.der) if h]
    t = {}
    for v in reversed(orden):
        t[v] = 1 + (t[v.izq] if v.izq else 0) + (t[v.der] if v.der else 0)
    return t


def potencial(raiz):
    return sum(math.log2(s) for s in tamanos(raiz).values())


def raiz_de(x):
    while x.padre:
        x = x.padre
    return x


def forma(x):
    """Cadena 'k(izq,der)' del arbol, para comparar formas."""
    if x is None:
        return "."
    if x.izq is None and x.der is None:
        return str(x.clave)
    return f"{x.clave}({forma(x.izq)},{forma(x.der)})"


def inorden(raiz):
    sal, pila, v = [], [], raiz
    while pila or v:
        while v:
            pila.append(v)
            v = v.izq
        v = pila.pop()
        sal.append(v.clave)
        v = v.der
    return sal


def profundidad(x):
    d = 0
    while x.padre:
        x, d = x.padre, d + 1
    return d


def espina_izq(x):
    """Numero de nodos en la espina izquierda de x (0 si x es None)."""
    c = 0
    while x:
        x, c = x.izq, c + 1
    return c


def arbol_aleatorio(n, rng, modo=None):
    """BST sobre 1..n por insercion en un orden dado."""
    claves = list(range(1, n + 1))
    modo = modo or rng.choice(["azar", "azar", "creciente", "decreciente", "zigzag"])
    if modo == "azar":
        rng.shuffle(claves)
    elif modo == "decreciente":
        claves.reverse()
    elif modo == "zigzag":
        claves = zigzag(claves)
    nodos = {}
    raiz = None
    for c in claves:
        v = Nodo(c)
        nodos[c] = v
        if raiz is None:
            raiz = v
            continue
        y = raiz
        while True:
            lado = "izq" if c < y.clave else "der"
            h = getattr(y, lado)
            if h is None:
                setattr(y, lado, v)
                v.padre = y
                break
            y = h
    return raiz


def zigzag(claves):
    """Orden de insercion 1, n, 2, n-1, ...: da un camino en zigzag."""
    i, j, sal = 0, len(claves) - 1, []
    while i <= j:
        sal.append(claves[i])
        i += 1
        if i <= j:
            sal.append(claves[j])
            j -= 1
    return sal


# ---- inicio de la version vigilada
def splay_vigilado(x, zigzig_mal=False):
    """Splay de x que comprueba el lema de paso de C4 5 en cada paso.
    Devuelve (rotaciones, pasos); cada paso es (tipo, amortizado, cota)."""
    rotaciones, pasos = 0, []
    while x.padre:
        p, g = x.padre, x.padre.padre
        tam = tamanos(raiz_de(x))
        phi, r_ant = sum(math.log2(s) for s in tam.values()), math.log2(tam[x])
        if g is None:
            tipo, costo = "zig", 1
            rotar(x)
        elif (g.izq is p) == (p.izq is x):
            tipo, costo = "zig-zig", 2
            if zigzig_mal:                      # rotar x dos veces: subir a la raiz
                rotar(x)
            else:
                rotar(p)
            rotar(x)
        else:
            tipo, costo = "zig-zag", 2
            rotar(x)
            rotar(x)
        tam = tamanos(raiz_de(x))
        phi2, r_nue = sum(math.log2(s) for s in tam.values()), math.log2(tam[x])
        amortizado = costo + phi2 - phi
        cota = 3 * (r_nue - r_ant) + (1 if tipo == "zig" else 0)
        pasos.append((tipo, amortizado, cota))
        rotaciones += costo
    return rotaciones, pasos
# ---- fin de la version vigilada


def acceso_vigilado(raiz, clave, zigzig_mal=False):
    """Un acceso completo vigilado. Devuelve (nueva raiz, rotaciones, pasos,
    exceso por acceso respecto de 3(log2 |t| - r(x)) + 1)."""
    x = buscar(raiz, clave)
    tam = tamanos(raiz)
    phi, r_x, n = sum(math.log2(s) for s in tam.values()), math.log2(tam[x]), tam[raiz]
    rot, pasos = splay_vigilado(x, zigzig_mal)
    c = max(rot, 1)
    a = c + potencial(x) - phi
    return x, rot, pasos, a - (3 * (math.log2(n) - r_x) + 1)


def acumular(estad, pasos):
    for tipo, a, cota in pasos:
        e = estad.setdefault(tipo, [0, -1e9, 0])
        e[0] += 1
        e[1] = max(e[1], a - cota)
        e[2] += a - cota > 1e-9


def formas(lo, hi):
    return _formas(lo, hi)


@lru_cache(None)
def _formas(lo, hi):
    if lo > hi:
        return (None,)
    return tuple((k, i, d) for k in range(lo, hi + 1)
                 for i in _formas(lo, k - 1) for d in _formas(k + 1, hi))


def construir(f, padre=None):
    if f is None:
        return None
    k, i, d = f
    x = Nodo(k)
    x.padre, x.izq, x.der = padre, construir(i, x), construir(d, x)
    return x


def total_pasada(raiz, n, reorganizar=splay):
    return sum(pasada(raiz, n, reorganizar)[1])


def costo_total(n):
    """T(n): costo de una pasada 1..n con splay desde camino(n)."""
    return total_pasada(camino(n), n)


def potencial_pasada(n):
    """Una pasada con el potencial medido: (T, phi0, phi_n, suma a_i, a maximo,
    suma de las cotas por acceso 3(log2 n - r(x_i)) + 1, r(x_i) medio)."""
    raiz = camino(n)
    phi0 = phi = potencial(raiz)
    t = sa = cotas = amax = rsum = 0.0
    for k in range(1, n + 1):
        x = buscar(raiz, k)
        r_x = math.log2(sum(1 for _ in _sub(x)))
        c = max(splay(x), 1)
        raiz = x
        phi2 = potencial(raiz)
        a = c + phi2 - phi
        phi = phi2
        t, sa, amax = t + c, sa + a, max(amax, a)
        cotas += 3 * (math.log2(n) - r_x) + 1
        rsum += r_x
    return t, phi0, phi, sa, amax, cotas, rsum / n


def _sub(x):
    pila = [x]
    while pila:
        v = pila.pop()
        yield v
        pila += [h for h in (v.izq, v.der) if h]


def instrumentada(raiz, n):
    """Pasada que anota, antes de cada acceso k, l_k (nodos en la espina izquierda
    del subarbol a recorrer) y lambda_k (espina izquierda del hijo derecho de k)."""
    ls, lams, costos = [], [], []
    for k in range(1, n + 1):
        x = buscar(raiz, k)
        d = profundidad(x)
        ls.append(d + (1 if k == 1 else 0))
        lams.append(espina_izq(x.der))
        costos.append(max(splay(x), 1))
        raiz = x
    return raiz, ls, lams, costos


# ================================================================== secciones
def seccion_1():
    print("== 1. el ejemplo: camino de 15 nodos ==")
    n = 15
    raiz, costos = pasada(camino(n), n)
    print("costo de acceder a 1..15:", " ".join(map(str, costos)))
    print(f"total T(15) = {sum(costos)};  primer acceso = {costos[0]} = n-1")
    print(f"el resto de los accesos cuesta {sum(costos[1:])}, "
          f"{sum(costos[1:]) / costos[0]:.1f} veces el primero")
    print("arbol final == arbol inicial:", forma(raiz) == forma(camino(n)))
    for n2 in (31, 63):
        c = pasada(camino(n2), n2)[1]
        print(f"n={n2}: primeros 12 costos {' '.join(map(str, c[:12]))} ...  T = {sum(c)}")


def seccion_2():
    print("== 2. el splay es una operacion correcta ==")
    rng = random.Random(13)
    N, ok_ord, ok_raiz, ok_prof, ok_rot = 3000, 0, 0, 0, 0
    for _ in range(N):
        raiz = arbol_aleatorio(rng.randint(1, 40), rng)
        antes = inorden(raiz)
        x = buscar(raiz, rng.choice(antes))
        d0, ok = profundidad(x), True
        rot = 0
        while x.padre:
            d_ant = profundidad(x)
            g = x.padre.padre
            if g is None:
                rotar(x)
                paso = 1
            elif (g.izq is x.padre) == (x.padre.izq is x):
                rotar(x.padre)
                rotar(x)
                paso = 2
            else:
                rotar(x)
                rotar(x)
                paso = 2
            rot += paso
            ok = ok and profundidad(x) == d_ant - paso
        ok_ord += inorden(x) == antes
        ok_raiz += x.padre is None
        ok_prof += ok
        ok_rot += rot == d0
    print(f"{N} splays en arboles de 1 a 40 nodos (formas variadas):")
    print(f"  el recorrido inorden no cambia:            {ok_ord} de {N}")
    print(f"  x termina en la raiz:                      {ok_raiz} de {N}")
    print(f"  la profundidad de x baja 1 o 2 por paso:   {ok_prof} de {N}")
    print(f"  rotaciones = profundidad inicial de x:     {ok_rot} de {N}")


def seccion_3():
    print("== 3. el lema de acceso, ejecutado ==")
    rng = random.Random(7)
    estad, estad_mal = {}, {}
    accesos = viol_acc = 0
    peor_acc = -1e9
    # secuencia del ejercicio y arboles al azar, con accesos al azar y en orden
    trabajos = [("camino", n) for n in (16, 31, 50)]
    trabajos += [("azar", rng.randint(2, 40)) for _ in range(150)]
    for tipo, n in trabajos:
        raiz = camino(n) if tipo == "camino" else arbol_aleatorio(n, rng)
        claves = list(range(1, n + 1)) + [rng.randint(1, n) for _ in range(n)]
        for k in claves:
            raiz, _rot, pasos, exceso = acceso_vigilado(raiz, k)
            acumular(estad, pasos)
            accesos += 1
            viol_acc += exceso > 1e-9
            peor_acc = max(peor_acc, exceso)
    print(f"{accesos} accesos en 3 caminos (n=16,31,50) y 150 arboles al azar de 2 a 40 nodos;")
    print("en cada uno, las claves 1..n y despues n claves al azar:")
    print(f"{'paso':>9} {'cantidad':>9} {'violan':>7} {'max(amortizado-cota)':>22}")
    for tipo in ("zig", "zig-zig", "zig-zag"):
        c, m, v = estad[tipo]
        print(f"{tipo:>9} {c:>9} {v:>7} {m:>22.3f}")
    print(f"por acceso: violan {viol_acc} de {accesos}; "
          f"max(a - cota del acceso) = {peor_acc:.3f}")
    # el mismo vigilante con el zig-zig mal ordenado (rotar x dos veces)
    accesos = viol_acc = 0
    for n in (16, 31, 50):
        raiz = camino(n)
        for k in range(1, n + 1):
            raiz, _r, pasos, exceso = acceso_vigilado(raiz, k, zigzig_mal=True)
            acumular(estad_mal, pasos)
            accesos += 1
            viol_acc += exceso > 1e-9
    print("zig-zig mal ordenado (rotar x dos veces), camino 1..n con n=16,31,50:")
    for tipo in ("zig", "zig-zig", "zig-zag"):
        c, m, v = estad_mal[tipo]
        print(f"{tipo:>9} {c:>9} {v:>7} {m:>22.3f}")
    print(f"por acceso: violan {viol_acc} de {accesos}")


def primer_fallo():
    """Menor n para el que el paso zig-zig mal ordenado viola la cota de paso en
    la primera subida del camino, y el detalle del primer paso que falla."""
    for n in range(3, 80):
        raiz = camino(n)
        x = buscar(raiz, 1)
        _rot, pasos = splay_vigilado(x, zigzig_mal=True)
        for i, (tipo, a, cota) in enumerate(pasos, 1):
            if a - cota > 1e-9:
                return n, i, tipo, a, cota
    return None


def tamanos_del_primer_fallo(n, paso):
    """s(x) antes, s'(g) y s'(x) despues, en el paso que falla (zig-zig mal)."""
    raiz = camino(n)
    x = buscar(raiz, 1)
    for i in range(1, paso + 1):
        p, g = x.padre, x.padre.padre
        if i == paso:
            sx = tamanos(raiz_de(x))[x]
            rotar(x)
            rotar(x)
            tam = tamanos(raiz_de(x))
            return sx, tam[g], tam[x]
        rotar(x)
        rotar(x)


def seccion_3b():
    print("== 3b. el primer fallo de subir a la raiz ==")
    n, paso, tipo, a, cota = primer_fallo()
    print(f"camino de n={n}, acceso a 1: el paso {paso} ({tipo}) viola la cota")
    print(f"  amortizado = {a:.3f}  >  3(r'(x)-r(x)) = {cota:.3f}")
    sx, sg, sxx = tamanos_del_primer_fallo(n, paso)
    print(f"  s(x) = {sx}, s'(g) = {sg}, s'(x) = {sxx}:  "
          f"s(x)+s'(g) = {sx + sg}  >  s'(x)-1 = {sxx - 1}")
    print("primer acceso del camino con subir a la raiz (amortizado = n-1):")
    print(f"{'n':>4} {'costo':>6} {'delta phi':>10} {'3 log2 n + 1':>13} {'viola':>6}")
    for m in range(11, 17):
        raiz = camino(m)
        phi = potencial(raiz)
        x = buscar(raiz, 1)
        c = subir_a_la_raiz(x)
        dphi = potencial(x) - phi
        cota_m = 3 * math.log2(m) + 1
        print(f"{m:>4} {c:>6} {dphi:>10.3f} {cota_m:>13.3f} {str(c + dphi > cota_m + 1e-9):>6}")
    menor = next(m for m in range(2, 100) if subir_costo(m) > 3 * math.log2(m) + 1 + 1e-9)
    print(f"menor n con violacion en el primer acceso: {menor}")


def subir_costo(n):
    raiz = camino(n)
    phi = potencial(raiz)
    x = buscar(raiz, 1)
    c = subir_a_la_raiz(x)
    return c + potencial(x) - phi


def seccion_4():
    print("== 4. la pasada devuelve el camino ==")
    # (a) invariante I(k): tras k accesos, raiz k con subarbol izquierdo = camino k-1
    malos = 0
    for n in range(1, 61):
        raiz = camino(n)
        for k in range(1, n + 1):
            x = buscar(raiz, k)
            splay(x)
            raiz = x
            ok = raiz.clave == k and forma(raiz.izq) == forma(sub_camino(k - 1)) \
                and sorted(inorden(raiz.der)) == list(range(k + 1, n + 1))
            malos += not ok
    print(f"invariante I(k) tras cada acceso, n=1..60:  fallos = {malos}")
    # (b) el arbol final es el inicial
    iguales = 0
    for n in range(1, 201):
        raiz, _c = pasada(camino(n), n)
        iguales += forma(raiz) == forma(camino(n))
    print(f"arbol final == camino(n), n=1..200:         {iguales} de 200")
    # (c) rondas repetidas cuestan lo mismo
    raiz, filas = camino(100), []
    for _ in range(4):
        raiz, c = pasada(raiz, 100)
        filas.append(sum(c))
    print("costo de 4 pasadas seguidas, n=100:", filas)
    # (d) la tabla de cotas
    print()
    print(f"{'n':>5} {'T(n)':>6} {'T/n':>5} {'phi0':>8} {'phi_n':>8} "
          f"{'suma a_i':>9} {'cota lema':>10} {'sin phi0':>9}")
    for n in (16, 64, 256, 1024):
        t, phi0, phin, sa, amax, cotas, rmed = potencial_pasada(n)
        generica = n * (3 * math.log2(n) + 1) + phi0
        print(f"{n:>5} {t:>6.0f} {t / n:>5.2f} {phi0:>8.1f} {phin:>8.1f} "
              f"{sa:>9.1f} {generica:>10.1f} {n * (3 * math.log2(n) + 1):>9.1f}")


def sub_camino(m):
    """Camino de m nodos con claves 1..m: m arriba, cada clave hija izquierda de la siguiente."""
    return camino(m) if m > 0 else None


def seccion_5():
    print("== 5. donde pierde la cota ==")
    print(f"{'n':>5} {'T/n':>5} {'suma cotas':>11} {'cota/T':>7} {'r medio':>8} "
          f"{'log2 n':>7} {'max a':>6} {'2log2 n':>8}")
    for n in (16, 64, 256, 1024):
        t, phi0, phin, sa, amax, cotas, rmed = potencial_pasada(n)
        print(f"{n:>5} {t / n:>5.2f} {cotas:>11.1f} {cotas / t:>7.1f} {rmed:>8.2f} "
              f"{math.log2(n):>7.1f} {amax:>6.2f} {2 * math.log2(n):>8.2f}")


def seccion_6():
    print("== 6. T(n) para n grande ==")
    print(f"{'n':>7} {'T(n)':>8} {'T/n':>6} {'3 log2 n + 1':>13} "
          f"{'(3 log2 n+1)/(T/n)':>19} {'cota lema/T':>12}")
    for k in range(4, 17):
        n = 2 ** k
        t = costo_total(n)
        lema = n * (3 * math.log2(n) + 1) + sum(math.log2(j) for j in range(2, n + 1))
        print(f"{n:>7} {t:>8} {t / n:>6.3f} {3 * math.log2(n) + 1:>13.1f} "
              f"{(3 * math.log2(n) + 1) / (t / n):>19.2f} {lema / t:>12.2f}")


def seccion_7():
    print("== 7. todas las formas iniciales (n pequeno) ==")
    print(f"{'n':>3} {'formas':>7} {'min':>4} {'max':>4} {'max/n':>6} {'camino':>7} "
          f"{'camino es el max':>17}")
    peor = 0.0
    for n in range(1, 13):
        fs = formas(1, n)
        vals = [total_pasada(construir(f), n) for f in fs]
        t_camino = costo_total(n)
        peor = max(peor, max(vals) / n)
        print(f"{n:>3} {len(fs):>7} {min(vals):>4} {max(vals):>4} {max(vals) / n:>6.2f} "
              f"{t_camino:>7} {str(t_camino == max(vals)):>17}")
    print(f"max T/n sobre todas las formas con n <= 12: {peor:.2f}")


def seccion_8():
    print("== 8. la recurrencia de la espina izquierda ==")
    rng = random.Random(5)
    fallos = pruebas = fallos_t = 0
    exacto = lambda ls, lams, cs: all(
        ls[k + 1] == ls[k] // 2 + lams[k] for k in range(len(ls) - 1))
    for n in range(2, 121):
        _r, ls, lams, cs = instrumentada(camino(n), n)
        pruebas += 1
        fallos += not exacto(ls, lams, cs)
        fallos_t += sum(cs) != sum(ls) - (ls[0] >= 2)
    for _ in range(600):
        n = rng.randint(2, 60)
        _r, ls, lams, cs = instrumentada(arbol_aleatorio(n, rng), n)
        pruebas += 1
        fallos += not exacto(ls, lams, cs)
        fallos_t += sum(cs) != sum(ls) - (ls[0] >= 2)
    print(f"l_(k+1) = floor(l_k/2) + lambda_k, {pruebas} pasadas:   fallos = {fallos}")
    print(f"T = suma de l_k - 1 (l_1 >= 2), las mismas pasadas: fallos = {fallos_t}")
    # en un arbol fijo, suma de lambda_k = n - l_1
    malos = 0
    for _ in range(500):
        raiz = arbol_aleatorio(rng.randint(2, 60), rng)
        n = len(inorden(raiz))
        s = sum(espina_izq(buscar(raiz, k).der) for k in range(1, n + 1))
        malos += s != n - espina_izq(raiz)
    print(f"arbol que no cambia: suma lambda_k = n - l_1 en 500 arboles: fallos = {malos}")
    print()
    print(f"{'n':>6} {'T(n)':>7} {'suma lambda':>12} {'lambda/n':>9} "
          f"{'2(n + suma lambda)':>19}")
    for n in (16, 64, 256, 1024, 4096):
        _r, ls, lams, cs = instrumentada(camino(n), n)
        lam = sum(lams)
        assert sum(cs) <= 2 * n + 2 * lam - 2
        print(f"{n:>6} {sum(cs):>7} {lam:>12} {lam / n:>9.2f} {2 * (n + lam):>19}")


def seccion_9():
    print("== 9. donde se gasta el costo (n=1023) ==")
    n = 1023
    _r, costos = pasada(camino(n), n)
    print("primeros 10 costos:", " ".join(map(str, costos[:10])))
    resto = costos[10:]
    print(f"los 10 primeros suman {sum(costos[:10])} (2n = {2 * n}); "
          f"los otros {len(resto)} suman {sum(resto)}")
    print(f"los otros: promedio {sum(resto) / len(resto):.2f}, "
          f"maximo {max(resto)} (log2 n = {math.log2(n):.1f})")
    print(f"{'costo >=':>9} {'accesos':>8} {'fraccion':>9}")
    for m in (1, 2, 4, 8, 16):
        c = sum(1 for x in resto if x >= m)
        print(f"{m:>9} {c:>8} {c / len(resto):>9.3f}")


def seccion_10():
    print("== 10. accesos al azar: la cota si es ajustada ahi ==")
    rng = random.Random(3)
    print(f"{'n':>6} {'cost/acceso':>12} {'log2 n':>7} {'cost/log2 n':>12} "
          f"{'3 log2 n + 1':>13}")
    for k in (6, 8, 10, 12, 14):
        n = 2 ** k
        raiz = camino(n)
        for _ in range(4 * n):                      # calentamiento
            x = buscar(raiz, rng.randint(1, n))
            splay(x)
            raiz = x
        total, m = 0, 20 * n
        for _ in range(m):
            x = buscar(raiz, rng.randint(1, n))
            total += max(splay(x), 1)
            raiz = x
        print(f"{n:>6} {total / m:>12.2f} {math.log2(n):>7.1f} "
              f"{total / m / math.log2(n):>12.2f} {3 * math.log2(n) + 1:>13.1f}")


def seccion_11():
    print("== 11. subir a la raiz ==")
    malos = 0
    for n in range(2, 201):
        raiz, c = pasada(camino(n), n, subir_a_la_raiz)
        esperado = [n - 1] + list(range(n - 1, 0, -1))
        malos += (c != esperado) or sum(c) != (n - 1) * (n + 2) // 2 \
            or forma(raiz) != forma(camino(n))
    print(f"costos = n-1, n-1, n-2, ..., 1; total (n-1)(n+2)/2; arbol final = camino:")
    print(f"  fallos en n=2..200: {malos}")
    print()
    print("costo por acceso en 3 pasadas (la tabla de C4 6):")
    print(f"{'n':>5} {'splay':>7} {'subir a la raiz':>16} {'(n-1)(n+2)/(2n)':>16}")
    for n in (100, 200, 400, 800):
        a = b = 0
        ra, rb = camino(n), camino(n)
        for _ in range(3):
            ra, c = pasada(ra, n)
            a += sum(c)
            rb, c = pasada(rb, n, subir_a_la_raiz)
            b += sum(c)
        print(f"{n:>5} {a / (3 * n):>7.2f} {b / (3 * n):>16.2f} "
              f"{(n - 1) * (n + 2) / (2 * n):>16.2f}")


def main():
    for f in (seccion_1, seccion_2, seccion_3, seccion_3b, seccion_4, seccion_5,
              seccion_6, seccion_7, seccion_8, seccion_9, seccion_10, seccion_11):
        f()
        print()


if __name__ == "__main__":
    main()
