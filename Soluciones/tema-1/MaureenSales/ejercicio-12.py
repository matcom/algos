"""Ejercicio 12 — Gale-Shapley con listas incompletas

Código extraído de ejercicio-12.md, en el mismo orden en que aparece allí.
Ejecutar con:  python ejercicio-12.py
La salida esperada es la de la sección "Salida" de ejercicio-12.md.
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")   # para que la consola de Windows imprima δ, ≤, ⌈⌉...

# ----------------------------------------------------------------------
# Del md, sección: 3. Algoritmo adaptado
# ----------------------------------------------------------------------
from collections import deque

def gale_shapley_incompleto(Lp, Lr):
    """Lp[p] = receptores que p acepta, del preferido al menos preferido (lista incompleta).
    Lr[r] = todos los proponentes, en el orden de preferencia de r (lista completa).
    Devuelve (pareja de cada proponente o None, número de propuestas)."""
    rango = {r: {p: k for k, p in enumerate(Lr[r])} for r in Lr}   # menor = mejor
    siguiente = {p: 0 for p in Lp}          # próximo índice de su lista a proponer
    pareja_r = {r: None for r in Lr}
    libres = deque(Lp)
    propuestas = 0
    while libres:
        p = libres.popleft()
        if siguiente[p] == len(Lp[p]):       # se le acabó la lista: se rinde y queda solo
            continue
        r = Lp[p][siguiente[p]]
        siguiente[p] += 1
        propuestas += 1
        if pareja_r[r] is None:              # r estaba sola: acepta
            pareja_r[r] = p
        elif rango[r][p] < rango[r][pareja_r[r]]:   # r prefiere a p: cambia
            libres.append(pareja_r[r])
            pareja_r[r] = p
        else:                                # r prefiere a su pareja actual
            libres.append(p)
    pareja_p = {p: None for p in Lp}
    for r, p in pareja_r.items():
        if p is not None:
            pareja_p[p] = r
    return pareja_p, propuestas


# ----------------------------------------------------------------------
# Del md, sección: 7. Casos de prueba
# ----------------------------------------------------------------------
import random, itertools

def es_valido(M, Lp, Lr):
    usados_r = [r for r in M.values() if r is not None]
    return len(usados_r) == len(set(usados_r)) and \
           all(r is None or r in Lp[p] for p, r in M.items())

def bloqueantes(M, Lp, Lr):
    pareja_r = {r: None for r in Lr}
    for p, r in M.items():
        if r is not None: pareja_r[r] = p
    res = []
    for p in Lp:
        for r in Lp[p]:                                           # cond. 1: r en la lista de p
            if M[p] == r:
                continue                                          # cond. 2
            p_quiere = M[p] is None or Lp[p].index(r) < Lp[p].index(M[p])               # cond. 3
            r_quiere = pareja_r[r] is None or Lr[r].index(p) < Lr[r].index(pareja_r[r])  # cond. 4
            if p_quiere and r_quiere:
                res.append((p, r))
    return res

def todos_los_estables(Lp, Lr):
    P = list(Lp)
    opciones = [[None] + Lp[p] for p in P]
    for eleccion in itertools.product(*opciones):
        M = dict(zip(P, eleccion))
        if es_valido(M, Lp, Lr) and not bloqueantes(M, Lp, Lr):
            yield M

def instancia_aleatoria(np_, nr, prob):
    """Listas incompletas para los proponentes (cada receptor entra con probabilidad prob),
    listas completas para los receptores."""
    P = [f"p{i}" for i in range(np_)]; R = [f"r{j}" for j in range(nr)]
    Lp = {}
    for p in P:
        L = [r for r in R if random.random() < prob]; random.shuffle(L); Lp[p] = L
    Lr = {r: random.sample(P, len(P)) for r in R}
    return Lp, Lr

# Ejemplo de la sección 3
Lp = {"A": ["X", "Y"], "B": ["X"], "C": ["Y"]}
Lr = {"X": ["B", "A", "C"], "Y": ["A", "C", "B"], "Z": ["A", "B", "C"]}
M, prop = gale_shapley_incompleto(Lp, Lr)
print("ejemplo:", M, f"({prop} propuestas)")
print("estables del ejemplo:", list(todos_los_estables(Lp, Lr)))
assert M == {"A": "Y", "B": "X", "C": None} and not bloqueantes(M, Lp, Lr)

random.seed(12)
total, con_solos = 0, 0
for _ in range(1500):
    Lp, Lr = instancia_aleatoria(random.randint(1, 5), random.randint(1, 5), random.choice([0.3, 0.5, 0.8, 1.0]))
    M, prop = gale_shapley_incompleto(Lp, Lr)
    estables = list(todos_los_estables(Lp, Lr))
    # 1) válido y estable
    assert es_valido(M, Lp, Lr) and not bloqueantes(M, Lp, Lr)
    # 2) óptimo para proponentes
    for p in Lp:
        validas = {E[p] for E in estables if E[p] is not None}
        mejor = min(validas, key=Lp[p].index) if validas else None
        assert M[p] == mejor
    # 3) potencial
    assert prop <= sum(len(L) for L in Lp.values())
    # 4) quiénes quedan solos: los mismos en todos los estables
    solos = {frozenset(p for p in E if E[p] is None) for E in estables}
    assert len(solos) == 1
    total += 1
    con_solos += any(r is None for r in M.values())
print(f"{total} instancias aleatorias: estable, óptimo para proponentes, propuestas <= sum |L_p|,")
print(f"  mismos solos en todos los estables. ({con_solos} de ellas dejaban a algún proponente solo)")

def gs_sin_rendicion(Lp, Lr, reiniciar, tope=10_000):
    """Gale-Shapley de C3 sin la línea nueva. reiniciar=False: lee fuera de la lista.
    reiniciar=True: quien agota su lista vuelve a empezarla. Devuelve qué pasó."""
    rango = {r: {p: k for k, p in enumerate(Lr[r])} for r in Lr}
    siguiente = {p: 0 for p in Lp}
    pareja_r = {r: None for r in Lr}
    libres = deque(Lp)
    for _ in range(tope):
        if not libres:
            return "termina"
        p = libres.popleft()
        if reiniciar and siguiente[p] == len(Lp[p]):
            siguiente[p] = 0
        if siguiente[p] >= len(Lp[p]):
            return "se cae"                  # Lp[p][siguiente[p]] daría IndexError
        r = Lp[p][siguiente[p]]
        siguiente[p] += 1
        if pareja_r[r] is None:
            pareja_r[r] = p
        elif rango[r][p] < rango[r][pareja_r[r]]:
            libres.append(pareja_r[r])
            pareja_r[r] = p
        else:
            libres.append(p)
    return "no termina"

Lp = {"A": ["X", "Y"], "B": ["X"], "C": ["Y"]}
Lr = {"X": ["B", "A", "C"], "Y": ["A", "C", "B"], "Z": ["A", "B", "C"]}
print("\nejemplo, sin adaptar:", gs_sin_rendicion(Lp, Lr, reiniciar=False))
print("ejemplo, reiniciando la lista:", gs_sin_rendicion(Lp, Lr, reiniciar=True))

generadores = {
    "completas n×n": lambda: instancia_aleatoria(*[random.randint(1, 5)] * 2, 1.0),
    "incompletas 0.8": lambda: instancia_aleatoria(random.randint(1, 5), random.randint(1, 5), 0.8),
    "incompletas 0.5": lambda: instancia_aleatoria(random.randint(1, 5), random.randint(1, 5), 0.5),
}
print(f"\n{'generador':>16} {'sin adaptar':>12} {'reiniciando':>12} {'adaptado':>9}")
for nombre, generar in generadores.items():
    casos = [generar() for _ in range(2000)]
    fallas = {"sin adaptar": 0, "reiniciando": 0, "adaptado": 0}
    for Lp, Lr in casos:
        M = gale_shapley_incompleto(Lp, Lr)[0]
        fallas["adaptado"] += not es_valido(M, Lp, Lr) or bool(bloqueantes(M, Lp, Lr))
        alguien_solo = None in M.values()
        for clave, reiniciar in [("sin adaptar", False), ("reiniciando", True)]:
            falla = gs_sin_rendicion(Lp, Lr, reiniciar) != "termina"
            assert falla == alguien_solo       # fallan justo cuando alguien debe quedar solo
            fallas[clave] += falla
    print(f"{nombre:>16} {100 * fallas['sin adaptar'] / len(casos):>11.1f}% "
          f"{100 * fallas['reiniciando'] / len(casos):>11.1f}% "
          f"{100 * fallas['adaptado'] / len(casos):>8.1f}%")

# Costo: lineal en el tamaño de la entrada
print(f"\n{'|P|=|R|':>8} {'prob':>5} {'sum |L_p|':>10} {'propuestas':>11}")
for n in [100, 1000]:
    for prob in [0.05, 0.5]:
        Lp, Lr = instancia_aleatoria(n, n, prob)
        M, prop = gale_shapley_incompleto(Lp, Lr)
        print(f"{n:8} {prob:5} {sum(len(L) for L in Lp.values()):10} {prop:11}")
