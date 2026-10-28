"""Ejercicio 5 ★★ — Detección de ciclos de Floyd (C3)

Código de validación de ejercicio-05.md.
Ejecutar con: python ejercicio-05.py
"""


# -------------------- Parte 1 --------------------

def floyd(cabeza):
    """Devuelve (hay_ciclo, vueltas)."""
    tortuga = liebre = cabeza
    vueltas = 0
    while liebre is not None and liebre.sig is not None:
        tortuga = tortuga.sig
        liebre = liebre.sig.sig
        vueltas += 1
        if tortuga is liebre:
            return True, vueltas
    return False, vueltas

# -------------------- Parte 2 --------------------

class Nodo:
    __slots__ = ("sig",)
    def __init__(self):
        self.sig = None

def lista(mu, lam):
    """Cola de mu nodos y ciclo de lam nodos; lam = 0 significa sin ciclo (lista de mu nodos)."""
    nodos = [Nodo() for _ in range(mu + lam)]
    for a, b in zip(nodos, nodos[1:]):
        a.sig = b
    if lam > 0:
        nodos[-1].sig = nodos[mu]
    return nodos[0] if nodos else None

def oraculo(cabeza):
    vistos = set()
    x = cabeza
    while x is not None:
        if id(x) in vistos:
            return True
        vistos.add(id(x))
        x = x.sig
    return False

def vueltas_esperadas(mu, lam):
    if lam == 0:
        return mu // 2
    k = max(mu, 1)
    return k + (-k) % lam          # primer múltiplo de lam que es >= max(mu, 1)

# -------------------- Parte 3 --------------------

casos = {
    "lista vacía": (0, 0),
    "un nodo, sin ciclo": (1, 0),
    "un nodo que se apunta a sí mismo": (0, 1),
    "dos nodos en ciclo": (0, 2),
    "cola 1 + ciclo 1": (1, 1),
    "cola 5 + ciclo 3": (5, 3),
    "10 nodos sin ciclo": (10, 0),
}
for nombre, (mu, lam) in casos.items():
    r, v = floyd(lista(mu, lam))
    print(f"{nombre:<34} ciclo={str(r):<5} vueltas={v}")
    assert r == (lam > 0) and v == vueltas_esperadas(mu, lam)

# -------------------- Parte 4 --------------------

for mu in range(0, 41):
    for lam in range(0, 41):
        cabeza = lista(mu, lam)
        r, v = floyd(cabeza)
        assert r == oraculo(cabeza) == (lam > 0)
        assert v == vueltas_esperadas(mu, lam)
        assert v <= mu + lam
print("1681 formas de lista: respuesta correcta, vueltas exactas y siempre <= n")

# -------------------- Parte 5 --------------------

def floyd_vigilado(mu, lam):
    cabeza = lista(mu, lam)
    pos = {}
    x, i = cabeza, 0
    while x is not None and id(x) not in pos:
        pos[id(x)] = i
        x, i = x.sig, i + 1
    tortuga = liebre = cabeza
    k, d_ant = 0, None
    while liebre is not None and liebre.sig is not None:
        tortuga, liebre, k = tortuga.sig, liebre.sig.sig, k + 1
        assert pos[id(tortuga)] == (k if k < mu else mu + (k - mu) % lam)
        if k >= mu:
            d = (-k) % lam
            if d_ant is not None:
                assert d == d_ant - 1
            d_ant = d
        if tortuga is liebre:
            assert k >= mu and k % lam == 0
            return True
    return False

for mu in range(0, 25):
    for lam in range(1, 25):
        assert floyd_vigilado(mu, lam)
print("invariante y potencial de la fase 2 comprobados en 600 listas con ciclo")

# -------------------- Parte 6 --------------------

def inicio_y_largo(cabeza):
    tortuga = liebre = cabeza
    while liebre is not None and liebre.sig is not None:
        tortuga, liebre = tortuga.sig, liebre.sig.sig
        if tortuga is liebre:
            mu, a = 0, cabeza
            while a is not tortuga:
                a, tortuga, mu = a.sig, tortuga.sig, mu + 1
            lam, b = 1, a.sig
            while b is not a:
                b, lam = b.sig, lam + 1
            return mu, lam
    return None

assert all(inicio_y_largo(lista(m, l)) == (m, l) for m in range(30) for l in range(1, 30))
assert inicio_y_largo(lista(7, 0)) is None
print("mu y lambda recuperados correctamente en 870 listas")
