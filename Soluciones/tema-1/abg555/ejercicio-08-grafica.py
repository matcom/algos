import importlib
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

bm = importlib.import_module("ejercicio-08-boyer_moore")


def iguales(r1, r2):
    return sorted(map(str, r1)) == sorted(map(str, r2))


def una_plantada(n, simbolos="ABCDE"):
    m = random.choice(simbolos)
    A = [m] * (n // 3 + 1) + [random.choice(simbolos) for _ in range(n - n // 3 - 1)]
    random.shuffle(A)
    return A


def dos_plantadas(n, simbolos="ABCDE"):
    a, b = random.sample(simbolos, 2)
    k = n // 3 + 1
    A = [a] * k + [b] * k + [random.choice(simbolos) for _ in range(n - 2 * k)]
    random.shuffle(A)
    return A


largos_dos = [2] + list(range(4, 16))
generadores = {
    "una plantada": lambda: una_plantada(random.randint(1, 15)),
    "dos plantadas": lambda: dos_plantadas(random.choice(largos_dos)),
    "binario": lambda: [random.choice("AB") for _ in range(random.randint(1, 15))],
    "3 simbolos": lambda: [random.choice("ABC") for _ in range(random.randint(1, 15))],
    "5 simbolos": lambda: [random.choice("ABCDE") for _ in range(random.randint(1, 15))],
}

# Figura 1 y 2: las trazas de los dos ejemplos, con los triples que se cancelan
# pintados del mismo color


def dibujar_traza(texto, archivo):
    A = list(texto)
    trace = []
    bm.first_pass(A, trace)

    # reconstruir que posiciones forman cada triple
    copias1, copias2, triples = [], [], []
    cand1 = cand2 = None
    count1 = count2 = 0
    for i, x in enumerate(A):
        if x == cand1:
            count1 += 1
            copias1.append(i)
        elif x == cand2:
            count2 += 1
            copias2.append(i)
        elif count1 == 0:
            cand1, count1 = x, 1
            copias1.append(i)
        elif count2 == 0:
            cand2, count2 = x, 1
            copias2.append(i)
        else:
            count1 -= 1
            count2 -= 1
            triples.append((copias1.pop(), copias2.pop(), i))

    colores_triple = ["#f6d7a7", "#d5c6f0"]
    color = {}
    for t, triple in enumerate(triples):
        for i in triple:
            color[i] = colores_triple[t]
    for i in copias1 + copias2:
        color[i] = "#cfe8f3"

    fig, ax = plt.subplots(figsize=(1.1 * len(A) + 1.5, 3.4))
    for i, x in enumerate(A):
        ax.add_patch(Rectangle((i * 1.1, 2), 0.9, 0.9, facecolor=color.get(i, "white"),
                               edgecolor="black"))
        ax.text(i * 1.1 + 0.45, 2.45, x, ha="center", va="center", fontsize=13)
        ax.text(i * 1.1 + 0.45, 3.15, str(i + 1), ha="center", fontsize=9, color="gray")
        c1, k1, c2, k2 = trace[i]
        ax.text(i * 1.1 + 0.45, 1.45, f"{c1}:{k1}", ha="center", fontsize=10, color="tab:blue")
        ax.text(i * 1.1 + 0.45, 0.85, f"{c2}:{k2}", ha="center", fontsize=10, color="tab:red")
    ax.text(-0.3, 3.15, "paso", ha="right", fontsize=9, color="gray")
    ax.text(-0.3, 1.45, "cand1:count1", ha="right", fontsize=9, color="tab:blue")
    ax.text(-0.3, 0.85, "cand2:count2", ha="right", fontsize=9, color="tab:red")
    ax.text(len(A) * 1.1 / 2, 0.1,
            "naranja y violeta: los dos triples que se cancelan; azul: las copias que sobreviven",
            ha="center", fontsize=9)
    ax.set_xlim(-2.2, len(A) * 1.1)
    ax.set_ylim(-0.1, 3.5)
    ax.axis("off")
    plt.tight_layout()
    plt.savefig(archivo, dpi=120)


dibujar_traza("ABCAABDAB", "ejercicio-08-traza.png")
dibujar_traza("DACCCCBDBBB", "ejercicio-08-traza2.png")

# Figura 3: cuanto falla el atajo segun el generador (de la prueba 6)
random.seed(6)
nombres, f_atajo, f_bien = [], [], []
for nombre, generar in generadores.items():
    arreglos = [generar() for _ in range(4000)]
    nombres.append(nombre)
    f_atajo.append(sum(not iguales(bm.more_than_third_shortcut(A), bm.oracle(A))
                       for A in arreglos) / 40)
    f_bien.append(sum(not iguales(bm.more_than_third(A), bm.oracle(A))
                      for A in arreglos) / 40)

x = range(len(nombres))
plt.figure(figsize=(7.5, 4))
b1 = plt.bar([i - 0.2 for i in x], f_atajo, width=0.4, label="atajo (sin verificar)",
             color="tab:orange")
plt.bar([i + 0.2 for i in x], f_bien, width=0.4, label="dos pasadas", color="tab:blue")
for b, f in zip(b1, f_atajo):
    plt.text(b.get_x() + b.get_width() / 2, f + 1.5, f"{f:.1f}%", ha="center", fontsize=9)
plt.xticks(list(x), nombres)
plt.ylim(0, 65)
plt.ylabel("% de arreglos con respuesta mal")
plt.title("El generador de dos plantadas nunca atrapa al atajo")
plt.legend()
plt.tight_layout()
plt.savefig("ejercicio-08-fallos.png", dpi=120)
