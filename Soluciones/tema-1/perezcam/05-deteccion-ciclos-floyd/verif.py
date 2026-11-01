import math
import random

class Nodo:
    __slots__ = ("sig",)
    def __init__(self):
        self.sig = None

def construir_lista(mu, lam):
    """Cola de longitud mu (sin ciclo) seguida de un ciclo de longitud lam.
    Si lam == 0, la lista es simplemente acíclica de longitud mu."""
    nodos = [Nodo() for _ in range(mu + lam)]
    for i in range(len(nodos) - 1):
        nodos[i].sig = nodos[i + 1]
    if lam > 0:
        nodos[-1].sig = nodos[mu]       # cierra el ciclo apuntando de vuelta a donde empieza
    cabeza = nodos[0] if nodos else None
    return cabeza, nodos

def floyd(cabeza):
    """Devuelve (hay_ciclo, pasos_lentos, nodo_encuentro)."""
    lento = rapido = cabeza
    pasos = 0
    while rapido is not None and rapido.sig is not None:
        lento = lento.sig
        rapido = rapido.sig.sig
        pasos += 1
        if lento is rapido:
            return True, pasos, lento
    return False, pasos, None

def encontrar_inicio_ciclo(cabeza, encuentro):
    """Segunda fase: un puntero desde la cabeza, otro desde el encuentro, avanzan de a 1."""
    p1, p2 = cabeza, encuentro
    pasos = 0
    while p1 is not p2:
        p1, p2 = p1.sig, p2.sig
        pasos += 1
    return p1, pasos

def indice_de(nodos, nodo):
    for i, x in enumerate(nodos):
        if x is nodo:
            return i
    return None

random.seed(0)
casos = 0
fallos_deteccion = 0
fallos_cota_pasos = 0
fallos_inicio_ciclo = 0

for _ in range(3000):
    mu = random.randint(0, 25)
    lam = random.choice([0] + list(range(1, 25)))  # 0 = sin ciclo
    cabeza, nodos = construir_lista(mu, lam)
    casos += 1

    tiene_ciclo_real = lam > 0
    hay_ciclo, pasos, encuentro = floyd(cabeza)

    if hay_ciclo != tiene_ciclo_real:
        fallos_deteccion += 1
        continue

    if tiene_ciclo_real:
        # el encuentro debe ocurrir dentro de mu + lam pasos del puntero lento
        if pasos > mu + lam:
            fallos_cota_pasos += 1
        # fase 2: encontrar el inicio del ciclo
        inicio, pasos2 = encontrar_inicio_ciclo(cabeza, encuentro)
        if indice_de(nodos, inicio) != mu or pasos2 != mu:    # el nodo es el mu-esimo y P1 camino mu pasos
            fallos_inicio_ciclo += 1

print(f"casos probados: {casos}")
print(f"fallos de deteccion (hay_ciclo correcto, deberia ser 0): {fallos_deteccion}")
print(f"fallos de la cota pasos <= mu+lam (deberia ser 0): {fallos_cota_pasos}")
print(f"fallos al encontrar el inicio exacto del ciclo (deberia ser 0): {fallos_inicio_ciclo}")

# Verificacion directa del potencial Phi = (pos_lento - pos_rapido) mod lam una vez ambos en el ciclo,
# calculado con los nodos reales (indice del nodo en la lista) antes y despues de cada paso conjunto.
print()
print("verificando que Phi baja 1 (mod lam) en cada paso conjunto, ambos en el ciclo:")
fallos_potencial = 0
for _ in range(500):
    mu = random.randint(0, 15)
    lam = random.randint(1, 15)
    cabeza, nodos = construir_lista(mu, lam)
    indice = {id(x): i for i, x in enumerate(nodos)}
    lento = rapido = cabeza
    while True:
        if indice[id(lento)] >= mu and indice[id(rapido)] >= mu:      # ambos ya estan en el ciclo
            phi_antes = (indice[id(lento)] - indice[id(rapido)]) % lam
            sig_lento, sig_rapido = lento.sig, rapido.sig.sig
            phi_despues = (indice[id(sig_lento)] - indice[id(sig_rapido)]) % lam
            if phi_despues != (phi_antes - 1) % lam:
                fallos_potencial += 1
        lento, rapido = lento.sig, rapido.sig.sig
        if lento is rapido:
            break
print("fallos del potencial (deberia ser 0):", fallos_potencial)

# Curiosidad (no es un resultado nuevo, es consecuencia directa del argumento de arriba):
# el encuentro no solo ocurre en <= mu+lam vueltas, ocurre EXACTAMENTE en la primera vuelta t
# que es a la vez >= mu (ambos punteros ya en el ciclo) y multiplo de lam (Phi=0).
print()
print("verificando t* = lam * ceil(max(mu,1)/lam) contra la simulacion real:")
fallos_formula = 0
casos_formula = 0
for _ in range(5000):
    mu = random.randint(0, 50)
    lam = random.randint(1, 50)
    cabeza, nodos = construir_lista(mu, lam)
    hay_ciclo, pasos, encuentro = floyd(cabeza)
    t_formula = lam * math.ceil(max(mu, 1) / lam)
    casos_formula += 1
    if pasos != t_formula:
        fallos_formula += 1
print(f"casos: {casos_formula}, fallos (deberia ser 0): {fallos_formula}")
