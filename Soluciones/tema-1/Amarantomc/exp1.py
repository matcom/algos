from collections import Counter
import random

def con_atajo(A):
    c1, c2 = None, None
    v1, v2 = 0, 0
    for x in A:
        if v1 > 0 and x == c1:
            v1 += 1
        elif v2 > 0 and x == c2:
            v2 += 1
        elif v1 == 0:
            c1, v1 = x, 1
        elif v2 == 0:
            c2, v2 = x, 1
        else:
            v1 -= 1
            v2 -= 1
            
     
    resultado = []
    if v1 > 0: resultado.append(c1)
    if v2 > 0: resultado.append(c2)
    return set(resultado)

def dos_pasadas_correcto(A):
    c1, c2 = None, None
    v1, v2 = 0, 0
    for x in A:
        if v1 > 0 and x == c1:
            v1 += 1
        elif v2 > 0 and x == c2:
            v2 += 1
        elif v1 == 0:
            c1, v1 = x, 1
        elif v2 == 0:
            c2, v2 = x, 1
        else:
            v1 -= 1
            v2 -= 1
            
    # Segunda pasada de verificación exacta
    candidatos = {c for c in (c1, c2) if c is not None}
    validos = set()
    n = len(A)
    for c in candidatos:
        if A.count(c) * 3 > n:
            validos.add(c)
    return validos

def gen_mayoria_plantada(n):
    # Inserta elementos con frecuencia claramente superior a n/3
    m = random.choice(["A", "B", "C", "D", "E"])
    A = [m] * (n // 3 + 2) + [random.choice(["A", "B", "C", "D", "E"]) for _ in range(n - (n // 3 + 2))]
    random.shuffle(A)
    return A

def gen_3_simbolos(n):
    return [random.choice(["A", "B", "C"]) for _ in range(n)]

def gen_4_simbolos(n):
    return [random.choice(["A", "B", "C", "D"]) for _ in range(n)]

def gen_5_simbolos(n):
    return [random.choice(["A", "B", "C", "D", "E"]) for _ in range(n)]

generadores = {
    "mayoría plantada": gen_mayoria_plantada,
    "3 símbolos": gen_3_simbolos,
    "4 símbolos": gen_4_simbolos,
    "5 símbolos": gen_5_simbolos,
}
def oraculo_n3(A):
    n = len(A)
    conteo = Counter(A)
    return {elem for elem, count in conteo.items() if count * 3 > n}

# Simulación de pruebas
random.seed(42)
pct_atajo = []
pct_correcto = []

for nombre, generar in generadores.items():
    casos = [generar(random.randint(10, 30)) for _ in range(2000)]
    fallos_atajo = sum(1 for A in casos if con_atajo(A) != oraculo_n3(A))
    fallos_correcto = sum(1 for A in casos if dos_pasadas_correcto(A) != oraculo_n3(A))
    
    pct_atajo.append((fallos_atajo / len(casos)) * 100)
    pct_correcto.append((fallos_correcto / len(casos)) * 100)
    print(f"{nombre:>20} | {pct_atajo[-1]:>13.1f}% | {pct_correcto[-1]:>17.1f}%")

    import matplotlib.pyplot as plt

nombres = ["Mayoría Plantada", "3 Símbolos", "4 Símbolos", "5 Símbolos"]


x = range(len(nombres))
ancho = 0.35

fig, ax = plt.subplots(figsize=(8, 5))
rects1 = ax.bar([i - ancho/2 for i in x], pct_atajo, ancho, label='Versión con Atajo', color='#e74c3c')
rects2 = ax.bar([i + ancho/2 for i in x], pct_correcto, ancho, label='Dos Pasadas (Correcto)', color='#2ecc71')

ax.set_ylabel('% de Arreglos con Errores')
ax.set_title('Porcentaje de Fallos según el Generador de Pruebas (Umbral > n/3)')
ax.set_xticks(x)
ax.set_xticklabels(nombres)
ax.legend()
ax.set_ylim(0, 100)

plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('grafica_fallos_n3.png', dpi=300)
