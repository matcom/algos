import itertools
import os
import random
from collections import Counter
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/daa-mpl-cache")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def misra_gries(A):
    """Dos candidatos, dos contadores. Primera pasada: cancelacion.
    Segunda pasada: verificacion real."""
    cand1 = cand2 = None
    c1 = c2 = 0
    for x in A:
        if c1 > 0 and x == cand1:
            c1 += 1
        elif c2 > 0 and x == cand2:
            c2 += 1
        elif c1 == 0:
            cand1, c1 = x, 1
        elif c2 == 0:
            cand2, c2 = x, 1
        else:
            c1 -= 1
            c2 -= 1
    # segunda pasada: verificar de verdad
    n = len(A)
    resultado = []
    for cand in (cand1, cand2):
        if cand is not None and A.count(cand) > n / 3:
            resultado.append(cand)
    return sorted(set(resultado)), (cand1, c1, cand2, c2)

def misra_gries_atajo(A):
    """Version sin segunda pasada: devuelve los candidatos con contador positivo, sin verificar."""
    cand1 = cand2 = None
    c1 = c2 = 0
    for x in A:
        if c1 > 0 and x == cand1:
            c1 += 1
        elif c2 > 0 and x == cand2:
            c2 += 1
        elif c1 == 0:
            cand1, c1 = x, 1
        elif c2 == 0:
            cand2, c2 = x, 1
        else:
            c1 -= 1
            c2 -= 1
    res = []
    if c1 > 0:
        res.append(cand1)
    if c2 > 0:
        res.append(cand2)
    return sorted(set(res))

def oraculo(A):
    n = len(A)
    return sorted(x for x, k in Counter(A).items() if k > n / 3)

# 1) Teorema: cualquier elemento con >n/3 apariciones sobrevive como candidato (verificado via el oraculo
#    comparado con la version CON segunda pasada, que debe coincidir siempre)
random.seed(0)
fallos_teorema = 0
pruebas = 0
for _ in range(5000):
    n = random.randint(1, 50)
    A = [random.choice("ABCDE") for _ in range(n)]
    esperado = oraculo(A)
    obtenido, _ = misra_gries(A)
    pruebas += 1
    if obtenido != esperado:
        fallos_teorema += 1
print(f"version con 2 pasadas vs oraculo: {pruebas} pruebas, fallos (deberia ser 0): {fallos_teorema}")

# 2) El contraejemplo concreto para el atajo, con 2 simbolos solamente
A = ["A"] + ["B"] * 99
res_atajo = misra_gries_atajo(A)
res_oraculo = oraculo(A)
print()
print("contraejemplo A + 99*B:")
print("  atajo (sin verificar) dice:", res_atajo)
print("  respuesta correcta (oraculo):", res_oraculo)
print(f"  'A' aparece 1 vez; n/3 = {len(A)/3:.1f} -> 1 NO es > n/3, A no deberia calificar")

# 3) Un generador que NO atrapa el atajo: ruido en trios cancelables, seguido de una mayoria.
def generador_no_atrapa(r):
    return ["B", "C", "D"] * r + ["A"] * (2 * r + 1)

casos_no_atrapa = [generador_no_atrapa(r) for r in range(1, 2001)]
fallos_no_atrapa = sum(
    1 for A in casos_no_atrapa if misra_gries_atajo(A) != oraculo(A)
)
print()
print(
    "generador ruido cancelable + mayoria:",
    len(casos_no_atrapa),
    "pruebas, fallos (deberia ser 0):",
    fallos_no_atrapa,
)

# 4) Bateria de pruebas por tamano de alfabeto, igual que C3 S5
def generador(alfabeto_tam, n, rng=random):
    letras = [chr(ord("A") + i) for i in range(alfabeto_tam)]
    return [rng.choice(letras) for _ in range(n)]

print()
print(f"{'alfabeto':>10} {'% fallos del atajo (vs oraculo)':>32}")
random.seed(5)
for tam in [2, 3, 4, 5]:
    casos = [generador(tam, random.randint(1, 60)) for _ in range(6000)]
    fallos = sum(1 for A in casos if misra_gries_atajo(A) != oraculo(A)) / len(casos)
    print(f"{tam:>10} {100*fallos:>31.2f}%")


# 5) Generadores dirigidos y análisis reproducible del atajo.
def gen_minimo_binario():
    """Contraejemplo binario mínimo: exacto [B], atajo [A, B]."""
    return list("ABB")


def gen_todos_distintos():
    """No hay elemento frecuente, pero puede sobrevivir un candidato falso."""
    return list("ABCD")


def gen_frontera_exacta(r=2):
    """Cada símbolo aparece r veces; con 4 bloques, r no supera n/3."""
    return list("A" * r + "B" * r + "C" * r + "D" * r)


def gen_frontera_con_cola():
    """ABCABC + DDD: D aparece exactamente n/3 veces."""
    return list("ABCABCDDD")


def gen_cancelacion_completa(r=8):
    """(ABC)^r: cada grupo de tres se cancela y nadie supera n/3."""
    return list("ABC" * r)


def gen_dos_frecuentes(r=5):
    """Dos elementos superan n/3: A y B aparecen r veces cada uno."""
    return list("A" * r + "B" * r + "CD")


def gen_mayoria_apenas_supera(n, seed):
    """Planta floor(n/3)+1 copias y mezcla el resto de forma reproducible."""
    principal = "A"
    cantidad = n // 3 + 1
    resto = ["B", "C", "D", "E", "F"]
    A = [principal] * cantidad
    A.extend(resto[i % len(resto)] for i in range(n - cantidad))
    random.Random(seed).shuffle(A)
    return A


def gen_orden_adversario(r, seed):
    """Misma multiconjunto A^r B^r C^r D^r, en un orden aleatorio."""
    A = list("A" * r + "B" * r + "C" * r + "D" * r)
    random.Random(seed).shuffle(A)
    return A


def gen_sesgado(n, seed):
    """Distribución sesgada: una señal fuerte y ruido con varias categorías."""
    rng = random.Random(seed)
    valores = ["A", "B", "C", "D", "E"]
    pesos = [0.62, 0.16, 0.10, 0.07, 0.05]
    return rng.choices(valores, weights=pesos, k=n)


def error_rate(casos):
    if not casos:
        return 0.0
    return sum(misra_gries_atajo(A) != oraculo(A) for A in casos) / len(casos)


def primer_contraejemplo_exhaustivo(max_n=8):
    """Busca el menor fallo al enumerar todos los arreglos sobre ABCD."""
    for n in range(1, max_n + 1):
        total = 0
        fallos = 0
        primero = None
        for tupla in itertools.product("ABCD", repeat=n):
            total += 1
            A = list(tupla)
            if misra_gries_atajo(A) != oraculo(A):
                fallos += 1
                if primero is None:
                    primero = "".join(A)
        if primero is not None:
            return n, total, fallos, primero
    return None


familias = {
    "minimo binario": [gen_minimo_binario()],
    "todos distintos": [gen_todos_distintos()],
    "frontera exacta": [gen_frontera_exacta()],
    "frontera con cola": [gen_frontera_con_cola()],
    "cancelacion completa": [gen_cancelacion_completa(r) for r in range(1, 101)],
    "dos frecuentes": [gen_dos_frecuentes()],
    "mayoria apenas supera": [
        gen_mayoria_apenas_supera(n, 1000 + n) for n in range(3, 81)
    ],
    "orden adversario": [
        gen_orden_adversario(r, 2000 + r * 17 + j)
        for r in range(1, 9)
        for j in range(250)
    ],
    "distribucion sesgada": [
        gen_sesgado(20 + (j % 61), 3000 + j) for j in range(2000)
    ],
    "ruido cancelable + mayoria": [
        generador_no_atrapa(r) for r in range(1, 2001)
    ],
}

print()
print("bateria dirigida del atajo:")
print(f"{'generador':>28} {'casos':>8} {'fallos':>10}")
resumen_familias = []
for nombre, casos in familias.items():
    tasa = error_rate(casos)
    resumen_familias.append((nombre, len(casos), tasa))
    print(f"{nombre:>28} {len(casos):>8} {100*tasa:>9.2f}%")

exhaustivo = primer_contraejemplo_exhaustivo()
print()
print("exhaustivo ABCD hasta n=8:")
if exhaustivo:
    n, total, fallos, primero = exhaustivo
    print(
        f"  primer fallo: n={n}, entrada={primero}, "
        f"casos hasta ese n={total}, fallos en ese n={fallos}"
    )
else:
    print("  no se encontró fallo")


def guardar_graficos():
    """Genera un panel de análisis para incluirlo en el informe."""
    out = Path(__file__).resolve().parent

    # Curva por tamaño de alfabeto, con tamaños más amplios que la tabla principal.
    alfabeto_x = list(range(2, 17))
    alfabeto_y = []
    for tam in alfabeto_x:
        rng = random.Random(4000 + tam)
        casos = [
            generador(tam, rng.randint(5, 80), rng=rng)
            for _ in range(1800)
        ]
        alfabeto_y.append(100 * error_rate(casos))

    # Sensibilidad al orden sobre la misma multiconjunto.
    orden_x = list(range(1, 9))
    orden_y = []
    for r in orden_x:
        casos = [gen_orden_adversario(r, 5000 + r * 100 + j) for j in range(1000)]
        orden_y.append(100 * error_rate(casos))

    # Búsqueda exhaustiva de cuántos fallos aparecen por tamaño.
    exhaustivo_x, exhaustivo_y = [], []
    for n in range(1, 9):
        fallos = 0
        for tupla in itertools.product("ABCD", repeat=n):
            A = list(tupla)
            fallos += misra_gries_atajo(A) != oraculo(A)
        exhaustivo_x.append(n)
        exhaustivo_y.append(fallos)

    # Barras dirigidas: se excluyen las baterías grandes para que el gráfico sea legible.
    nombres = [
        "minimo binario", "todos distintos", "frontera exacta",
        "frontera con cola", "cancelacion completa", "dos frecuentes",
        "mayoria apenas supera", "ruido cancelable + mayoria",
    ]
    tasas = [
        100 * next(t for n, _, t in resumen_familias if n == nombre)
        for nombre in nombres
    ]

    fig, axes = plt.subplots(2, 2, figsize=(11, 7.2), constrained_layout=True)
    fig.suptitle("Misra-Gries: análisis del atajo sin segunda pasada", fontsize=14, fontweight="bold")

    ax = axes[0, 0]
    ax.barh(nombres[::-1], tasas[::-1], color="#C2552A")
    ax.set_xlim(0, 105)
    ax.set_xlabel("% de entradas donde atajo ≠ oráculo")
    ax.set_title("Casos dirigidos")
    ax.grid(axis="x", alpha=.25)

    ax = axes[0, 1]
    ax.plot(alfabeto_x, alfabeto_y, marker="o", color="#7564C7")
    ax.set_xlabel("tamaño del alfabeto")
    ax.set_ylabel("% de fallos")
    ax.set_title("Aleatorios uniformes")
    ax.grid(alpha=.25)

    ax = axes[1, 0]
    ax.plot(orden_x, orden_y, marker="o", color="#0E9C8A")
    ax.set_xlabel("r en A^r B^r C^r D^r")
    ax.set_ylabel("% de fallos tras barajar")
    ax.set_title("El orden también importa para el atajo")
    ax.set_xticks(orden_x)
    ax.grid(alpha=.25)

    ax = axes[1, 1]
    ax.bar(exhaustivo_x, exhaustivo_y, color="#B47B13")
    ax.set_xlabel("n")
    ax.set_ylabel("número de contraejemplos sobre ABCD")
    ax.set_title("Búsqueda exhaustiva")
    ax.set_xticks(exhaustivo_x)
    ax.grid(axis="y", alpha=.25)

    fig.savefig(out / "analisis-generadores.png", dpi=180, bbox_inches="tight")
    plt.close(fig)
    print()
    print("grafico generado:", out / "analisis-generadores.png")
    print("tasas por alfabeto 2..16:", [round(x, 2) for x in alfabeto_y])
    print("tasas por orden r=1..8:", [round(x, 2) for x in orden_y])
    print("fallos exhaustivos n=1..8:", exhaustivo_y)


if __name__ == "__main__":
    guardar_graficos()
