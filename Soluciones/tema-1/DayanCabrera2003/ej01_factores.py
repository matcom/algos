"""Ejercicio 1: factor de crecimiento del tamano de entrada con una maquina K veces mas rapida.

Modelo: word RAM; tiempo = costo/velocidad. Con presupuesto T (operaciones), c(n) = costo; la maquina nueva tiene K*T operaciones.
Salida principal por stdout (-> ej01_salida.txt); datos de la grafica en ej01_curva.dat.
"""
import math

K = 1000
LNK = math.log(K)


def mayor_n(costo, presupuesto):
    """Mayor n entero con costo(n) <= presupuesto (misma busqueda que C1 sec. 7).
    Requiere costo no decreciente."""
    alto = 2
    while costo(alto) <= presupuesto:
        alto *= 2
    bajo = alto // 2
    while bajo + 1 < alto:
        medio = (bajo + alto) // 2
        if costo(medio) <= presupuesto:
            bajo = medio
        else:
            alto = medio
    return bajo


def f_exacto(n, k=K):
    """f con (f n) ln(f n) = k n ln n, por biseccion en (1, max(k,1)]. Reales."""
    obj = k * n * math.log(n)
    lo, hi = 1e-12 if k < 1 else 1.0, max(float(k), 1.0)
    lo = max(lo, 1.0 / n * 1.0001)  # f n > 1
    for _ in range(300):
        mid = (lo + hi) / 2
        if mid * n * math.log(mid * n) <= obj:
            lo = mid
        else:
            hi = mid
    return lo


def phi(f, n):
    return K * math.log(n) / (math.log(n) + math.log(f))


def cota_inf(n):
    return K / (1 + LNK / math.log(n))


def elasticidad(n):
    return K ** (math.log(n) / (math.log(n) + 1))


print("=== A. Theta(n^2) con c(n) = a n^2 exacto: n'^2 = K n^2 ===")
print(f"sqrt({K}) = {math.sqrt(K):.6f}")
for n0 in (10, 10**3, 10**6, 10**9):
    c = lambda n: n * n
    n1 = mayor_n(c, K * c(n0))
    print(f"  n0={n0:>10}  n'={n1:>12}  n'/n0={n1/n0:.4f}")

print()
print("=== B. Theta(n^2) con menor orden: c(n) = n^2 + 1000 n ===")
for n0 in (10, 10**3, 10**6, 10**9):
    c = lambda n: n * n + 1000 * n
    n1 = mayor_n(c, K * c(n0))
    print(f"  n0={n0:>10}  n'={n1:>12}  n'/n0={n1/n0:.4f}")

print()
print("=== C. Theta pura (c1=1, c2=4) NO fija el factor ===")
print(f"cotas: sqrt(K c1/c2) = {math.sqrt(K/4):.4f} <= f <= "
      f"sqrt(K c2/c1) = {math.sqrt(K*4):.4f}")
N1, N2 = 10**6, 2 * 10**6
cbaja = lambda n: n * n if n <= N1 else 4 * n * n           # c = 1 y luego 4
calta = lambda n: 4 * n * n if n <= N1 else (4 * N1 * N1 if n <= N2 else n * n)
for nombre, cc, n0 in (("c = n^2 (n<=1e6), 4n^2 despues", cbaja, 10**6),
                      ("c = 4n^2 (n<=1e6), meseta, n^2  ", calta, 5 * 10**5)):
    n1 = mayor_n(cc, K * cc(n0))
    print(f"  {nombre}: n0={n0:>8} n'={n1:>10} f={n1/n0:.4f}")
print("  Analogo n log n con c2/c1=4, n=1e11: f_(K c1/c2) <= f <= f_(K c2/c1)")
print(f"    f_250 = {f_exacto(1e11, K/4):.2f}   f_1000 = {f_exacto(1e11):.2f}"
      f"   f_4000 = {f_exacto(1e11, 4*K):.2f}")

print()
print("=== D. Theta(n log n), c(n) = a n log n: n' log n' = K n log n ===")
print(f"{'n':>9} {'cota lema':>9} {'elastic.':>9} {'f exacto':>9} {'f entero':>9}")
n_c1 = mayor_n(lambda n: n * math.log2(n), 3600 * 10**9)
filas = []
for n0 in (10, 10**2, 10**3, 10**4, 10**6, 10**9, n_c1, 10**12, 10**15):
    li, el, ex = cota_inf(n0), elasticidad(n0), f_exacto(n0)
    c = lambda n: n * math.log2(n)
    ent = mayor_n(c, K * c(n0)) / n0
    assert li <= ex < K and el < ex
    etq = "9.857e10" if n0 == n_c1 else f"{n0:.0e}".replace("e+0", "e").replace("e+", "e")
    print(f"{etq:>9} {li:9.1f} {el:9.1f} {ex:9.1f} {ent:9.1f}")
for e in (20, 50, 100):
    n0 = 10.0 ** e
    assert cota_inf(n0) <= f_exacto(n0) < K and elasticidad(n0) < f_exacto(n0)
print("(asserts: cota del lema <= f < K y elasticidad < f, tambien en 1e20, 1e50, 1e100)")

print()
print("=== E. Convergencia de f <- K ln n / (ln n + ln f) desde f = K ===")
for n0 in (1e3, 1e11):
    fs = f_exacto(n0)
    f, prev = float(K), None
    L = cota_inf(n0)
    print(f"  n={n0:.0e}  f*={fs:.4f}  1/ln(f* n)={1/math.log(fs*n0):.4f}")
    for k in range(1, 7):
        f = phi(f, n0)
        err = abs(f - fs)
        r = "" if prev is None or prev == 0 else f"  err/err_ant={err/prev:.4f}"
        print(f"    paso {k}: f={f:12.6f}  err={err:.2e}{r}")
        prev = err
    assert L <= fs <= K
# cota de |phi'| en [L,K]: cruda K/(L ln(L n)) (decreciente en n, pues L y ln(L n) crecen con n) y fina phi(L)/(L ln(L n))
def cruda(n):
    L = cota_inf(n)
    return K / (L * math.log(L * n))
def fina(n):
    L = cota_inf(n)
    return phi(L, n) / (L * math.log(L * n))
print(f"  cota cruda K/(L ln(L n)) en n=4: {cruda(4):.4f} (< 1, y decrece con n: vale para todo n >= 4)")
print(f"  cota fina phi(L)/(L ln(L n)): n=2: {fina(2):.4f}   n=3: {fina(3):.4f}")
assert cruda(4) < 1 and fina(2) < 1 and fina(3) < 1 and cruda(5) < cruda(4)

print()
print("=== F. Discretizacion: razon c(n+1)/c(n) de n log n ===")
for n0 in (2, 3, 10, 10**3, 10**6):
    c = lambda n: n * math.log2(n)
    print(f"  n={n0:>8}  c(n+1)/c(n)={c(n0+1)/c(n0):.6f}")
for n0 in (2, 3):
    c = lambda n: n * math.log2(n)
    n1 = mayor_n(c, K * c(n0))
    print(f"  n0={n0}: n'={n1}  f_entero={n1/n0:.1f}  f_real={f_exacto(n0):.1f}"
          f"  cota lema={cota_inf(n0):.1f}")

# Rango del factor entero en los bordes: T recorre [c(n), c(n+1)) (el codigo usa T = c(n))
print("  Rango completo con T en [c(n), c(n+1)), c = n log2 n:")
for n0 in (2, 3):
    c = lambda n: n * math.log2(n)
    lo = mayor_n(c, K * c(n0)) / n0
    hi = mayor_n(c, K * c(n0 + 1) * (1 - 1e-12)) / n0
    print(f"    n0={n0}: f_entero va de {lo:.1f} (T=c(n)) a {hi:.1f} (T->c(n+1)-)")

# datos de la grafica: log10 n, f(n log n), f(n^2 + 1000 n)
with open("ej01_curva.dat", "w") as fh:
    fh.write("x f q\n")
    x = 1.0
    while x <= 30.0001:
        n = 10.0 ** x
        b = 1000.0
        nq = (-b + math.sqrt(b * b + 4 * K * (n * n + b * n))) / 2
        fh.write(f"{x:.1f} {f_exacto(n):.3f} {nq/n:.3f}\n")
        x += 0.5
