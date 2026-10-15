"""Ejercicio 4 del Tema 1: el contador binario en una máquina de Turing.

Los bloques van en el orden de ejercicio-04.md, y cada uno imprime lo que el .md
muestra debajo de él. Ejecutarlo desde Soluciones/tema-1/alinadelanoval/:

    pip install tesserax        # para la figura
    python codigo/ejercicio-04.py
"""

# == bloque: imports (oculto)
import math
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[3] / "Lectures" / "2026"))   # donde vive figuras.py

# == bloque: maquina
delta = {                               # (estado, lee) -> (escribe, movimiento, nuevo estado)
    ("q0", "1"): ("0", -1, "q0"),
    ("q0", "0"): ("1", +1, "q1"),
    ("q0", "$"): ("1", +1, "q1"),
    ("q1", "0"): ("0", +1, "q1"),
    ("q1", "1"): ("1", +1, "q1"),
    ("q1", "$"): ("$", -1, "q2"),
}

def incrementar(cinta, cabeza):
    # aplica δ hasta que la máquina se traba; devuelve la cabeza y el número de pasos
    estado, pasos = "q0", 0
    while (estado, cinta.get(cabeza, "$")) in delta:
        escribe, movimiento, estado = delta[(estado, cinta.get(cabeza, "$"))]
        cinta[cabeza] = escribe
        cabeza += movimiento
        pasos += 1
    assert estado == "q2"                       # se traba en el estado final
    return cabeza, pasos

def leer(cinta):
    return int("".join(cinta[i] for i in sorted(cinta) if cinta[i] != "$"), 2)

M = 10_000
cinta, cabeza = {0: "0"}, 0                     # el 0 escrito en una sola celda
costos, potencial = [], [0]
for i in range(1, M + 1):
    cabeza, c = incrementar(cinta, cabeza)
    assert leer(cinta) == i                                          # deja escrito n + 1
    assert cinta[cabeza] != "$" and cinta.get(cabeza + 1, "$") == "$"  # cabezal en el bit menos significativo
    costos.append(c)
    potencial.append(2 * list(cinta.values()).count("1"))
print(f"{M:,} incrementos desde 0: después de cada uno la cinta dice n + 1")
print("y el cabezal está otra vez en el bit menos significativo")

# == bloque: costo
for i, c in enumerate(costos, start=1):
    b = bin(i - 1)
    k = len(b) - len(b.rstrip("1"))             # unos en que termina i - 1
    assert c == 2 * k + 2
print("c = 2k + 2 en todos los incrementos\n")
for m in (10, 100, 1_000, 10_000):
    caro = max(costos[:m])
    i = costos.index(caro) + 1
    assert caro == 2 * math.floor(math.log2(m)) + 2
    assert i - 1 == 2 ** math.floor(math.log2(m)) - 1
    print(f"m = {m:>6,}: el más caro cuesta {caro:>2} pasos, el que parte de {i - 1:,}")

# == bloque: traza (asis)
def mostrar(cinta, cabeza, desde, hasta):
    return " ".join(f"[{cinta.get(k, '$')}]" if k == cabeza else cinta.get(k, "$")
                    for k in range(desde, hasta + 1))

cinta, cabeza = {-2: "1", -1: "1", 0: "1"}, 0          # 7 = 111, cabezal en el último 1
estado, paso = "q0", 0
print("| paso | estado | lee | escribe | mueve | cinta después |")
print("|---|---|---|---|---|---|")
print(f"| 0 | | | | | `{mostrar(cinta, cabeza, -4, 1)}` |")
while (estado, cinta.get(cabeza, "$")) in delta:
    lee = cinta.get(cabeza, "$")
    escribe, movimiento, nuevo = delta[(estado, lee)]
    cinta[cabeza] = escribe
    cabeza += movimiento
    paso += 1
    print(f"| {paso} | {estado} → {nuevo} | `{lee}` | `{escribe}` | {'L' if movimiento < 0 else 'R'} |"
          f" `{mostrar(cinta, cabeza, -4, 1)}` |")
    estado = nuevo
assert leer(cinta) == 8 and paso == 2 * 3 + 2           # k = 3 unos: c = 2k + 2 = 8

# == bloque: potencial
amortizados = [c + potencial[i] - potencial[i - 1] for i, c in enumerate(costos, start=1)]
assert all(a == 4 for a in amortizados)
print(f"costo amortizado = 4 en los {M:,} incrementos\n")
for m in (10, 100, 1_000, 10_000):
    total = sum(costos[:m])
    assert total == 4 * m - potencial[m] <= 4 * m
    print(f"m = {m:>6,}: total {total:>6,}   4m − Φₘ = {4 * m - potencial[m]:>6,}"
          f"   4m = {4 * m:>6,}")

# == bloque: figura (oculto)
try:
    import figuras as F
except ImportError:
    print("sin tesserax no se regenera la figura")
else:
    figura = F.cola_potencial(costos[:32], amortizados[:32], potencial[1:33],
                              ident="ejercicio-04-potencial")
    svg = figura[figura.index("<svg"):figura.index("</svg>") + len("</svg>")]
    vb = svg.split('viewBox="')[1].split('"')[0].split()   # fondo blanco para GitHub
    fondo = f'<rect x="{vb[0]}" y="{vb[1]}" width="{vb[2]}" height="{vb[3]}" fill="white"/>'
    (AQUI.parent / "figuras" / "ejercicio-04-potencial.svg").write_text(
        svg.replace(">", ">" + fondo, 1), encoding="utf-8")
