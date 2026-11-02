"""Ejercicio 5 — Detección de ciclos con la liebre y la tortuga (Floyd)

Código extraído de ejercicio-05.md, en el mismo orden en que aparece allí.
Ejecutar con:  python ejercicio-05.py
La salida esperada es la de la sección "Salida" de ejercicio-05.md.
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")   # para que la consola de Windows imprima δ, ≤, ⌈⌉...

# ----------------------------------------------------------------------
# Del md, sección: 2. Algoritmo
# ----------------------------------------------------------------------

def floyd(x0, sig, contador=None):
    """True si la lista que empieza en x0 tiene un ciclo."""
    tortuga, liebre = x0, x0
    while True:
        # la liebre avanza 2
        for _ in range(2):
            if liebre is None:
                return False
            liebre = sig(liebre)
            if contador is not None: contador[0] += 1
        if liebre is None:
            return False
        tortuga = sig(tortuga)
        if contador is not None: contador[0] += 1
        if tortuga == liebre:
            return True


# ----------------------------------------------------------------------
# Del md, sección: 8. Casos de prueba
# ----------------------------------------------------------------------

import random

def construir(mu, lam, sin_ciclo_largo=None):
    """Lista con nodos 0..n-1 representada como diccionario sig.
    Si sin_ciclo_largo es un número L, la lista es 0 -> 1 -> ... -> L -> None."""
    if sin_ciclo_largo is not None:
        L = sin_ciclo_largo
        sig = {i: (i + 1 if i < L else None) for i in range(L + 1)}
    else:
        n = mu + lam
        sig = {i: i + 1 for i in range(n - 1)}
        sig[n - 1] = mu                     # el último vuelve a x_mu
    # renombro los nodos al azar para que el orden de las etiquetas no ayude
    etiquetas = list(sig.keys()); random.shuffle(etiquetas)
    ren = dict(zip(sig.keys(), etiquetas))
    sig2 = {ren[a]: (ren[b] if b is not None else None) for a, b in sig.items()}
    return ren[0], (lambda x: sig2[x])

def floyd_vigilado(x0, sig, mu, lam):
    """Floyd devolviendo la iteración del encuentro; vigila el potencial D."""
    tortuga = liebre = x0
    k, D_anterior = 0, None
    while True:
        for _ in range(2):
            if liebre is None: return None
            liebre = sig(liebre)
        if liebre is None: return None
        tortuga = sig(tortuga)
        k += 1
        if lam is not None and k >= mu:
            D = (-k) % lam
            if D_anterior is not None and D_anterior > 0:
                assert D == D_anterior - 1, "el potencial no bajó exactamente 1"
            D_anterior = D
        if tortuga == liebre:
            return k

def mu_lambda(x0, sig):
    tortuga = liebre = x0
    while True:
        tortuga = sig(tortuga); liebre = sig(sig(liebre))
        if tortuga == liebre: break
    mu, a, b = 0, x0, liebre
    while a != b:
        a, b, mu = sig(a), sig(b), mu + 1
    lam, c = 1, sig(a)
    while c != a:
        c, lam = sig(c), lam + 1
    return mu, lam

random.seed(5)

# Casos a mano
x0, s = construir(0, 1);  assert floyd(x0, s)            # un nodo que se apunta a sí mismo
x0, s = construir(3, 1);  assert floyd(x0, s)
x0, s = construir(0, 0, sin_ciclo_largo=0); assert not floyd(x0, s)   # un solo nodo
assert not floyd(None, lambda x: None)                    # lista vacía
print("casos a mano: OK")

# Exhaustivo en tamaños chicos, con ciclo
for mu in range(0, 30):
    for lam in range(1, 30):
        x0, s = construir(mu, lam)
        c = [0]
        assert floyd(x0, s, c)
        k = floyd_vigilado(x0, s, mu, lam)
        esperado = lam * -(-max(mu, 1) // lam)       # menor múltiplo de lam >= max(mu,1)
        assert k == esperado, (mu, lam, k, esperado)
        assert c[0] == 3 * k <= 3 * (mu + lam)
        assert mu_lambda(x0, s) == (mu, lam)
print("con ciclo, mu y lambda en [0,30): encuentro, potencial, costo y (mu, lambda): OK")

# Exhaustivo sin ciclo
for L in range(0, 200):
    x0, s = construir(0, 0, sin_ciclo_largo=L)
    c = [0]
    assert not floyd(x0, s, c)
    assert c[0] == (L + 1) + L // 2
print("sin ciclo, L en [0,200): OK")

# Tabla de costos para listas grandes
print(f"\n{'mu':>7} {'lambda':>7} {'iter. encuentro':>16} {'llamadas a sig':>15} {'3(mu+lambda)':>13}")
for mu, lam in [(0, 1), (1000, 1), (1, 1000), (500, 500), (999, 7), (100000, 99999)]:
    x0, s = construir(mu, lam)
    c = [0]
    floyd(x0, s, c)
    k = c[0] // 3
    print(f"{mu:7} {lam:7} {k:16} {c[0]:15} {3*(mu+lam):13}")
