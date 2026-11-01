import random

def mezclar_correcta(A, B, contador=None):
    R, i, j = [], 0, 0
    while i < len(A) and j < len(B):
        if contador is not None:
            contador[0] += 1
        if A[i] <= B[j]:
            R.append(A[i]); i += 1
        else:
            R.append(B[j]); j += 1
    return R + A[i:] + B[j:]

def mezclar_optimizada(A, B, contador=None):
    """Dejar de comparar en cuanto a A le queda un solo elemento: lo pone al final."""
    R, i, j = [], 0, 0
    n = len(A)
    while (n - i) > 1 and j < len(B):
        if contador is not None:
            contador[0] += 1
        if A[i] <= B[j]:
            R.append(A[i]); i += 1
        else:
            R.append(B[j]); j += 1
    # a A le queda <=1 elemento, o B se vacio
    R.extend(B[j:])
    R.extend(A[i:])          # el ultimo elemento de A (si queda) se pone AL FINAL
    return R

def es_correcto(A, B, R):
    return R == sorted(A + B)

random.seed(1)
# 1) cota de comparaciones: <= 2n-2 en el peor caso (barrido aleatorio); la mezcla correcta, medida igual
print(f"{'n':>6} {'max comp. optimizada':>21} {'2n-2':>6} {'max comp. correcta':>19} {'2n-1':>6}")
for n in [2, 5, 10, 50, 200, 1000]:
    peor_opt = peor_cor = 0
    for _ in range(300):
        A = sorted(random.sample(range(0, 10**6), n))
        B = sorted(random.sample(range(0, 10**6), n))
        c = [0]
        mezclar_optimizada(A, B, c)
        peor_opt = max(peor_opt, c[0])
        c = [0]
        mezclar_correcta(A, B, c)
        peor_cor = max(peor_cor, c[0])
    print(f"{n:>6} {peor_opt:>21} {2*n-2:>6} {peor_cor:>19} {2*n-1:>6}")

# 2) via C5 S6: 2n-2 < 2n-1 = cota minima de CUALQUIER mezcla correcta -> no puede ser siempre correcta
print()
print("2n-2 < 2n-1 (cota minima de C5 S6) para todo n>=1 => la version optimizada NO PUEDE ser correcta")
print("siempre, sin necesidad de probarla primero (C5 S8: cota minima como detector de errores).")

# 3) el contraejemplo explicito: la cadena intercalada de C5 S6, A=impares, B=pares
print()
print("contraejemplo con la cadena a1<b1<a2<b2<...<an<bn (la misma de C5 S6):")
for n in [4, 5, 8]:
    A = list(range(1, 2*n, 2))      # impares: 1,3,5,...,2n-1
    B = list(range(2, 2*n+1, 2))    # pares:   2,4,6,...,2n
    R = mezclar_optimizada(A, B)
    correcto = es_correcto(A, B, R)
    print(f"  n={n}: A={A} B={B}")
    print(f"       salida optimizada: {R}")
    print(f"       correcta (ordenada)?: {correcto}  (deberia ser: False)")

# 4) que tan rara es la falla con entradas al azar (igual tema del "caso tipico no es la garantia")
print()
random.seed(2)
fallos = 0
pruebas = 20000
for _ in range(pruebas):
    n = random.randint(2, 30)
    A = sorted(random.sample(range(0, 1000), n))
    B = sorted(random.sample(range(0, 1000), n))
    R = mezclar_optimizada(A, B)
    if not es_correcto(A, B, R):
        fallos += 1
print(f"entradas aleatorias uniformes: {fallos}/{pruebas} fallan ({100*fallos/pruebas:.2f}%)")


# 5) Generadores dirigidos: cada familia representa una razon distinta para que el atajo
#    funcione o produzca una salida rota.
def ejecutar_optimizada(A, B):
    comparaciones = [0]
    R = mezclar_optimizada(A, B, comparaciones)
    return R, comparaciones[0]


def numero_inversiones(R):
    """Cuenta pares fuera de orden en la salida; sirve para medir cuanto se rompe."""
    return sum(R[i] > R[j] for i in range(len(R)) for j in range(i + 1, len(R)))


def _construir_con_cola(n, cola, ultimo_A):
    """Construye listas que dejan exactamente cola pendiente cuando A tiene un elemento."""
    r = len(cola)
    if n < 2 or not (1 <= r < n):
        raise ValueError("se necesita 1 <= len(cola) < n")

    # El prefijo alterna y luego termina antes de la cola de B.
    A_prefijo = list(range(0, 2 * n - 2, 2))
    B_prefijo = list(range(1, 2 * (n - r), 2))
    cola = list(cola)
    if not (A_prefijo[-1] < ultimo_A and B_prefijo[-1] < cola[0]):
        raise ValueError("los valores no forman listas ordenadas")
    if cola != sorted(cola):
        raise ValueError("la cola de B debe estar ordenada")
    A = A_prefijo + [ultimo_A]
    B = B_prefijo + cola
    assert A == sorted(A) and B == sorted(B)
    return A, B


def gen_B_se_vacia(n):
    """Caso de control: B se consume completamente antes de la parada prematura."""
    return list(range(1000, 1000 + n)), list(range(n))


def gen_parada_correcta(n, r=3):
    """Caso de control: quedan r elementos de B, todos menores que el ultimo de A."""
    r = min(r, n - 1)
    cola = list(range(2 * n + 1, 2 * n + 1 + r))
    ultimo_A = 2 * n + r + 10
    return _construir_con_cola(n, cola, ultimo_A)


def gen_una_inversion(n):
    """Fallo minimo de esta familia: el bloque pendiente provoca una sola inversion."""
    return _construir_con_cola(n, [2 * n + 1], 2 * n)


def gen_varias_inversiones(n, r=3):
    """Fallo con r elementos de B mayores que el ultimo de A: deja r inversiones."""
    r = min(r, n - 1)
    cola = [2 * n + 1 + i for i in range(r)]
    return _construir_con_cola(n, cola, 2 * n)


def gen_cola_mixta(n):
    """Fallo mixto: parte de la cola es menor y parte mayor que el ultimo de A."""
    cola = [2 * n + 1, 2 * n + 2, 2 * n + 5, 2 * n + 6]
    return _construir_con_cola(n, cola, 2 * n + 3)


def gen_intercalada(n):
    """Adversario de C5: A y B quedan perfectamente intercaladas."""
    return list(range(1, 2 * n, 2)), list(range(2, 2 * n + 1, 2))


def gen_aleatoria_ordenada(n, seed):
    """Dos listas ordenadas aleatorias, con semilla para hacer el experimento reproducible."""
    rng = random.Random(seed)
    A = sorted(rng.sample(range(0, 100000), n))
    B = sorted(rng.sample(range(0, 100000), n))
    return A, B


def analizar_familia(casos):
    registros = []
    for A, B in casos:
        R, comparaciones = ejecutar_optimizada(A, B)
        registros.append((
            not es_correcto(A, B, R),
            comparaciones,
            numero_inversiones(R),
        ))
    if not registros:
        return {"casos": 0, "fallos": 0, "tasa": 0.0, "comp_media": 0.0,
                "comp_max": 0, "inv_media": 0.0, "inv_max": 0}
    return {
        "casos": len(registros),
        "fallos": sum(fallo for fallo, _, _ in registros),
        "tasa": sum(fallo for fallo, _, _ in registros) / len(registros),
        "comp_media": sum(c for _, c, _ in registros) / len(registros),
        "comp_max": max(c for _, c, _ in registros),
        "inv_media": sum(inv for _, _, inv in registros) / len(registros),
        "inv_max": max(inv for _, _, inv in registros),
    }


familias = {
    "B se vacia": [gen_B_se_vacia(n) for n in range(2, 31)],
    "parada correcta": [gen_parada_correcta(n, 3) for n in range(3, 31)],
    "una inversion": [gen_una_inversion(n) for n in range(2, 31)],
    "varias inversiones": [gen_varias_inversiones(n, 5) for n in range(6, 31)],
    "cola mixta": [gen_cola_mixta(n) for n in range(5, 31)],
    "intercalada adversaria": [gen_intercalada(n) for n in range(2, 31)],
    "aleatorias ordenadas": [
        gen_aleatoria_ordenada(2 + (j % 29), 1000 + j) for j in range(1000)
    ],
}

print()
print("familias dirigidas: fallos, comparaciones e inversiones de la salida")
print(f"{'generador':>24} {'casos':>6} {'fallos':>8} {'comp.media':>11} "
      f"{'comp.max':>9} {'inv.media':>10} {'inv.max':>8}")
for nombre, casos in familias.items():
    datos = analizar_familia(casos)
    print(
        f"{nombre:>24} {datos['casos']:>6} "
        f"{100 * datos['tasa']:>7.2f}% {datos['comp_media']:>11.2f} "
        f"{datos['comp_max']:>9} {datos['inv_media']:>10.2f} {datos['inv_max']:>8}"
    )

print()
print("ejemplos de salidas rotas:")
ejemplos = {
    "una inversion": gen_una_inversion(8),
    "varias inversiones": gen_varias_inversiones(8, 3),
    "cola mixta": gen_cola_mixta(8),
    "intercalada adversaria": gen_intercalada(4),
}
for nombre, (A, B) in ejemplos.items():
    R, comparaciones = ejecutar_optimizada(A, B)
    print(f"  {nombre}: A={A}, B={B}")
    print(f"    salida=[..., {str(R[-6:])[1:-1]}], comparaciones={comparaciones}, inversiones={numero_inversiones(R)}")
