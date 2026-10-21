"""Ejercicio 13: splay desde un camino de n nodos, accediendo a 1..n en orden (C4 sec. 4-6).
Costo = rotaciones (1 si ya es la raiz). r(x) = log2 s(x). Phi = suma de rangos, mantenido incrementalmente."""
import math
import sys

sys.setrecursionlimit(100000)
log2 = math.log2


class Nodo:
    __slots__ = ("clave", "izq", "der", "padre", "s")

    def __init__(self, k):
        self.clave, self.izq, self.der, self.padre, self.s = k, None, None, None, 1


class Arbol:
    def __init__(self, n):
        """camino(n): n en la raiz, cada clave k hija izquierda de k+1 (como en C4)."""
        self.n = n
        self.nodos = [Nodo(k) for k in range(1, n + 1)]
        for k in range(1, n):
            self.nodos[k].izq, self.nodos[k - 1].padre = self.nodos[k - 1], self.nodos[k]
            self.nodos[k].s = k + 1
        self.raiz = self.nodos[-1]
        self.phi = sum(log2(k) for k in range(1, n + 1))        # = log2 n!  (rangos del camino)
        self.zigzig = self.zigzag = self.zig = 0

    def rotar(self, x):
        p, g = x.padre, x.padre.padre
        viejo = log2(p.s) + log2(x.s)
        if p.izq is x:
            p.izq = x.der
            if p.izq:
                p.izq.padre = p
            x.der = p
        else:
            p.der = x.izq
            if p.der:
                p.der.padre = p
            x.izq = p
        p.padre, x.padre = x, g
        if g:
            if g.izq is p:
                g.izq = x
            else:
                g.der = x
        p.s = 1 + (p.izq.s if p.izq else 0) + (p.der.s if p.der else 0)
        x.s = 1 + (x.izq.s if x.izq else 0) + (x.der.s if x.der else 0)
        self.phi += log2(p.s) + log2(x.s) - viejo

    def splay(self, x):
        rot = 0
        while x.padre:
            p, g = x.padre, x.padre.padre
            if g is None:
                self.rotar(x)
                rot += 1
                self.zig += 1
            elif (g.izq is p) == (p.izq is x):
                self.rotar(p)
                self.rotar(x)
                rot += 2
                self.zigzig += 1
            else:
                self.rotar(x)
                self.rotar(x)
                rot += 2
                self.zigzag += 1
        self.raiz = x
        return rot

    def subir(self, x):
        rot = 0
        while x.padre:
            self.rotar(x)
            rot += 1
        self.raiz = x
        return rot

    def phi_desde_cero(self):
        def rec(x):
            return 0.0 if x is None else log2(x.s) + rec(x.izq) + rec(x.der)
        return rec(self.raiz)

    def pre(self, x=None, primero=True):
        x = self.raiz if primero else x
        if x is None:
            return "."
        if x.izq is None and x.der is None:
            return str(x.clave)
        return f"({x.clave} {self.pre(x.izq, False)} {self.pre(x.der, False)})"


def ejecutar(n, heur="splay"):
    """Accede a 1..n en orden. Devuelve dict con costos y cantidades de la cota."""
    T = Arbol(n)
    phi0 = T.phi
    logn = log2(n)
    total = suma_hat = suma_r = cota_lema = 0.0
    costos, rs, phis = [], [], [phi0]
    violaciones = 0
    for k in range(1, n + 1):
        x = T.nodos[k - 1]
        r = log2(x.s)
        antes = T.phi
        c = max(T.splay(x) if heur == "splay" else T.subir(x), 1)
        hat = c + T.phi - antes
        tope = 3 * (logn - r) + 1
        if heur == "splay" and hat > tope + 1e-9:
            violaciones += 1
        total += c
        suma_hat += hat
        suma_r += r
        cota_lema += tope
        costos.append(c)
        rs.append(r)
        phis.append(T.phi)
    return dict(n=n, T=int(total), costos=costos, rs=rs, phis=phis, phi0=phi0, phif=T.phi, suma_hat=suma_hat,
                suma_r=suma_r, A=cota_lema, viol=violaciones, arbol=T)


def tikz_arbol(raiz, etiqueta=""):
    """Dibuja un arbol: x = lugar en el recorrido en orden, y = profundidad."""
    pos, filas = {}, []
    cnt = [0]

    def rec(x, d):
        if x is None:
            return
        rec(x.izq, d + 1)
        pos[x.clave] = (cnt[0], d)
        cnt[0] += 1
        rec(x.der, d + 1)
    rec(raiz, 0)
    L = ["\\begin{tikzpicture}[x=0.36cm,y=0.5cm,every node/.style={font=\\tiny,inner sep=0.8pt,circle,draw}]"]
    for k, (px, py) in pos.items():
        L.append(f"\\node (n{k}) at ({px},{-py}) {{{k}}};")

    def aristas(x):
        if x is None:
            return
        for h in (x.izq, x.der):
            if h is not None:
                L.append(f"\\draw (n{x.clave})--(n{h.clave});")
                aristas(h)
    aristas(raiz)
    L.append("\\end{tikzpicture}")
    return "\n".join(L) + "\n"


# --------------------------------------------------------------------------- 1
print("=== 1. El primer acceso (clave 1 desde camino(n)): costo exacto y forma del arbol ===")
malos = 0
for n in range(1, 301):
    T = Arbol(n)
    rot = T.splay(T.nodos[0])
    esperado_rot = n - 1
    zz_esperado = (n - 1) // 2
    zig_esperado = 1 if (n - 1) % 2 == 1 else 0
    # forma esperada: raiz 1, hijo derecho = espina de pares con impares como hijos derechos
    def peine(j, n):
        if j == 0:
            return None
        return (2 * j, peine(j - 1, n), (2 * j + 1) if 2 * j + 1 <= n else None)

    def a_texto(t):
        if t is None:
            return "."
        if isinstance(t, int):
            return str(t)
        c, i, d = t
        if i is None and d is None:
            return str(c)
        return f"({c} {a_texto(i)} {a_texto(d)})"
    j = (n - 1) // 2
    if n == 1:
        esperado = "1"
    elif n % 2 == 1:
        esperado = a_texto((1, None, peine(j, n)))
    else:
        esperado = a_texto((1, None, (n, peine(j, n), None)))
    ok = (rot == esperado_rot or n == 1) and T.zigzig == zz_esperado and T.zig == zig_esperado and T.pre() == esperado
    malos += not ok
print(f"  n = 1..300: rotaciones = n-1, zig-zig = floor((n-1)/2), zig = 1 si n es par (0 si es impar), y la forma coincide con la")
print(f"  del lema (raiz 1; hijo derecho = espina izquierda de pares 2,4,..; cada par 2j con el impar 2j+1 como hijo derecho): fallos = {malos}")
for n in (7, 15, 16):
    T = Arbol(n)
    T.splay(T.nodos[0])
    print(f"  n={n:>2}: tras acceder a 1:  {T.pre()}   (zig-zig {T.zigzig}, zig {T.zig})")
T = Arbol(15)
for k in (1, 2, 3):
    T.splay(T.nodos[k - 1])
    print(f"  n=15 tras acceder a 1..{k}:  {T.pre()}")
for k in (1, 2, 3):
    Tm = Arbol(15)
    for j in range(1, k + 1):
        Tm.subir(Tm.nodos[j - 1])
    open(f"ej13_splay_{k}.tex", "w").write(tikz_arbol(Tm.raiz) if False else "")
T = Arbol(15)
for k in (1, 2, 3):
    T.splay(T.nodos[k - 1])
    open(f"ej13_splay_{k}.tex", "w").write(tikz_arbol(T.raiz))
Tm = Arbol(15)
for k in (1, 2, 3):
    Tm.subir(Tm.nodos[k - 1])
    open(f"ej13_raiz_{k}.tex", "w").write(tikz_arbol(Tm.raiz))
    print(f"  n=15, subir a la raiz tras acceder a 1..{k}: {Tm.pre()}")

# --------------------------------------------------------------------------- 2
print()
print("=== 2. El costo real de n accesos en orden desde camino(n), y las cotas del lema ===")
print("  Cota cruda (C4): sum c <= n (3 log2 n + 1) + log2 n!   [r(x) >= 0, Phi_final >= 0]")
print("  Cota cruda afinada con Phi_final >= log2 n (la raiz):  n (3 log2 n + 1) + log2 n! - log2 n")
print("  Cota fina: sum_k [3 (log2 n - r_k) + 1] + Phi_0 - Phi_final, con los r_k y Phi_final REALES de la ejecucion")
print(f"  {'n':>7} {'costo total':>12} {'total/n':>8} {'cruda':>11} {'cruda/n':>8} {'fina':>11} {'fina/n':>8} {'cruda/total':>12} {'fina/total':>11}")
filas = []
for n in (15, 31, 63, 127, 255, 511, 1023, 4095, 16383, 65535, 262143):
    R = ejecutar(n)
    assert R["viol"] == 0
    phi0 = R["phi0"]
    cruda = 3 * n * log2(n) + n + phi0
    cruda2 = cruda - log2(n)
    fina = R["A"] + phi0 - R["phif"]
    ident = R["suma_hat"] + phi0 - R["phif"]
    assert abs(ident - R["T"]) < 1e-3 * max(1, R["T"]) * 1e-3 + 1e-3, (n, ident, R["T"])     # sum c = sum c_hat + Phi_0 - Phi_final
    assert R["T"] <= fina + 1e-6 <= cruda2 + 1e-6
    filas.append((n, R["T"], cruda, fina))
    print(f"  {n:>7} {R['T']:>12} {R['T'] / n:>8.3f} {cruda:>11.0f} {cruda / n:>8.2f} {fina:>11.0f} {fina / n:>8.2f} {cruda / R['T']:>12.2f} {fina / R['T']:>11.2f}")
print("  (verificado con assert: sum c = sum c_hat + Phi_0 - Phi_final, y total <= fina <= cruda afinada)")
with open("ej13_cotas.dat", "w") as fh:
    fh.write("n total cruda fina\n")
    for n, T_, c, f in filas:
        fh.write(f"{n} {T_} {c:.1f} {f:.1f}\n")

# --------------------------------------------------------------------------- 3
print()
print("=== 3. Reproduccion de la tabla de C4 sec. 6: 3 rondas, costo por acceso ===")
def costo_por_acceso(heur, n, rondas=3):
    T = Arbol(n)
    total = 0
    for _ in range(rondas):
        for k in range(1, n + 1):
            x = T.nodos[k - 1]
            total += max(T.splay(x) if heur == "splay" else T.subir(x), 1)
    return total / (rondas * n)
print(f"  {'n':>5} {'splay':>7} {'subir a la raiz':>16}   (C4: 4,2 4,2 4,3 4,4  y  50,5 100,5 200,5 400,5)")
for n in (100, 200, 400, 800):
    print(f"  {n:>5} {costo_por_acceso('splay', n):>7.1f} {costo_por_acceso('subir', n):>16.1f}")

# --------------------------------------------------------------------------- 4
print()
print("=== 4. Por que la cota pierde: de donde sale (n accesos en orden) ===")
print("  Lema J_k (demostrado en el texto): tras acceder a 1..k la raiz es k y su subarbol izquierdo es la cadena izquierda k-1 -> ... -> 1, sin hijos derechos.")
print("  Consecuencia: tras acceder a 1..n el arbol es camino(n) y Phi_final = Phi_0.")


def cumple_J(T, k):
    if T.raiz.clave != k:
        return False
    x, esperado = T.raiz.izq, k - 1
    while esperado >= 1:
        if x is None or x.clave != esperado or x.der is not None:
            return False
        x, esperado = x.izq, esperado - 1
    return x is None


fallos_J = comprobaciones_J = malos = 0
for n in range(1, 301):
    T = Arbol(n)
    for k in range(1, n + 1):
        T.splay(T.nodos[k - 1])
        comprobaciones_J += 1
        fallos_J += not cumple_J(T, k)
    malos += T.pre() != Arbol(n).pre()
print(f"  J_k comprobado con assert tras CADA acceso para n = 1..300 ({comprobaciones_J} comprobaciones): fallos = {fallos_J}")
assert fallos_J == 0
print(f"  forma final == camino(n) para n = 1..300: fallos = {malos}")
print(f"  {'n':>7} {'costo real T':>13} {'A=sum[3(log n - r_k)+1]':>24} {'n(3 log n+1)':>13} {'3 sum r_k':>10} {'Phi_0':>10} {'Phi_final':>10} {'cota fina=A':>12} {'A/T':>6}")
for n in (1023, 16383, 262143):
    R = ejecutar(n)
    A, phi0, phif = R["A"], R["phi0"], R["phif"]
    assert abs(phi0 - phif) < 1e-3 * 1e-3 * phi0 + 1e-3
    print(f"  {n:>7} {R['T']:>13} {A:>24.0f} {n * (3 * log2(n) + 1):>13.0f} {3 * R['suma_r']:>10.0f} {phi0:>10.0f} {phif:>10.0f} {A + phi0 - phif:>12.0f} {A / R['T']:>6.2f}")
print("  La cota fina es A + (Phi_0 - Phi_final) = A: Phi_0 y Phi_final SE CANCELAN. Toda la perdida esta en los terminos 3(log n - r_k) + 1.")
print("  Cota cruda = n(3 log n + 1) + Phi_0; fina = cruda - 3 sum r_k - Phi_0 + (Phi_0 - Phi_final) = cruda - 3 sum r_k - Phi_final.")
n = 1023
R = ejecutar(n)
costos, rs, phis = R["costos"], R["rs"], R["phis"]
hats = [costos[k] + phis[k + 1] - phis[k] for k in range(n)]
print(f"  n = {n}: Phi_0 = {phis[0]:.0f}; tras el 1er acceso Phi = {phis[1]:.0f}; tras n/4 accesos {phis[n // 4]:.0f}; tras n/2 {phis[n // 2]:.0f}; "
      f"tras 3n/4 {phis[3 * n // 4]:.0f}; final {phis[-1]:.0f}  (baja y vuelve a subir)")
print(f"  costo amortizado c_hat_k: suma = {sum(hats):.0f} = costo real (el potencial vuelve a su valor); 1er acceso c_hat = {hats[0]:.0f} (el potencial cae), "
      f"maximo {max(hats):.1f}, media de los demas {(sum(hats) - hats[0]) / (n - 1):.2f}")
print(f"  el tope del lema 3(log2 n - r_k) + 1 vale en media {R['A'] / n:.1f} por acceso; el costo real por acceso es {R['T'] / n:.2f}")
print(f"  r_k reales (primeros 14): {[round(x, 2) for x in rs[:14]]}   (media {sum(rs) / n:.2f}; la cota cruda supone 0)")
with open("ej13_phi.dat", "w") as fh:
    fh.write("k phi\n")
    for k, v in enumerate(phis):
        fh.write(f"{k} {v:.3f}\n")

# --------------------------------------------------------------------------- 5
print()
print("=== 5. Constante empirica del acceso secuencial (Tarjan 1985: O(n) desde cualquier arbol inicial) ===")
print(f"  {'n':>8} {'costo total':>12} {'total/n':>9}")
for n in (7, 15, 31, 100, 1000, 4095, 16383, 65535, 262143, 1048575):
    R = ejecutar(n)
    print(f"  {n:>8} {R['T']:>12} {R['T'] / n:>9.4f}")
mx, arg = 0, 0
for n in range(2, 1501):
    t = ejecutar(n)["T"]
    if t / n > mx:
        mx, arg = t / n, n
print(f"  maximo de total/n para 2 <= n <= 1500 (todos los n): {mx:.4f}  en n = {arg}")
import random as _r
_g = _r.Random(13)
muestras = sorted({int(2 ** _g.uniform(11, 17)) for _ in range(40)})
mx2 = max((ejecutar(n)["T"] / n, n) for n in muestras)
print(f"  maximo de total/n en 40 valores de n entre 2^11 y 2^17 elegidos al azar: {mx2[0]:.4f} en n = {mx2[1]}")

# --------------------------------------------------------------------------- 6
print()
print("=== 6. Contraste: subir a la raiz en la misma secuencia ===")
malos = 0
for n in range(2, 201):
    R = ejecutar(n, "subir")
    esperado = [n - 1] + [n - j + 1 for j in range(2, n + 1)]
    malos += (R["costos"] != esperado) or (R["T"] != n * (n + 1) // 2 - 1)
print(f"  n = 2..200: costos por acceso = [n-1, n-1, n-2, ..., 1] y total = n(n+1)/2 - 1: fallos = {malos}")
print(f"  {'n':>6} {'subir a la raiz':>16} {'n(n+1)/2 - 1':>14} {'splay':>10} {'cociente':>9}")
for n in (15, 100, 1000, 4000):
    Rr, Rs = ejecutar(n, "subir"), ejecutar(n, "splay")
    print(f"  {n:>6} {Rr['T']:>16} {n * (n + 1) // 2 - 1:>14} {Rs['T']:>10} {Rr['T'] / Rs['T']:>9.1f}")
