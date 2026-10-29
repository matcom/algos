"""Ejercicio 4 ★★ — El contador binario en una máquina de Turing (C1, C4)

Código de validación de ejercicio-04.md.
Ejecutar con: python ejercicio-04.py
"""


# -------------------- Parte 1 --------------------

def ejecutar(delta, cinta, cabezal, estado, final):
    """Corre la máquina hasta el estado final. Devuelve (cabezal, pasos)."""
    pasos = 0
    while estado != final:
        simbolo = cinta.get(cabezal, "_")
        escribe, mueve, estado = delta[(estado, simbolo)]
        cinta[cabezal] = escribe
        cabezal += 1 if mueve == "R" else -1
        pasos += 1
    return cabezal, pasos

INC = {
    ("inc", "1"): ("0", "L", "inc"),
    ("inc", "0"): ("1", "R", "vuelta"),
    ("inc", "_"): ("1", "R", "vuelta"),
    ("vuelta", "0"): ("0", "R", "vuelta"),
    ("vuelta", "1"): ("1", "R", "vuelta"),
    ("vuelta", "_"): ("_", "L", "fin"),
}

def leer(cinta):
    bits = "".join(cinta[p] for p in sorted(cinta) if cinta[p] in "01")
    return int(bits, 2)

def unos_finales(i):
    t = 0
    while i & 1:
        i, t = i >> 1, t + 1
    return t

# -------------------- Parte 2 --------------------

def potencial(cinta):
    return 2 * sum(1 for s in cinta.values() if s == "1")

cinta, cabezal = {0: "0"}, 0          # el LSB está en la posición 0
total, peor = 0, 0
for i in range(1, 5000 + 1):
    antes = potencial(cinta)
    t = unos_finales(i - 1)
    cabezal, pasos = ejecutar(INC, cinta, cabezal, "inc", "fin")
    assert cabezal == 0 and leer(cinta) == i
    assert pasos == 2 * t + 2
    assert pasos + potencial(cinta) - antes == 4          # costo amortizado
    total += pasos
    peor = max(peor, pasos)
    if i in (10, 100, 1000, 5000):
        print(f"m = {i:>5}: total = {total:>6}  4m - 2 popcount(m) = {4 * i - 2 * bin(i).count('1'):>6}"
              f"  peor incremento = {peor:>2} = 2*floor(log2 m) + 2")
        assert total == 4 * i - 2 * bin(i).count("1")
        assert peor == 2 * (i.bit_length() - 1) + 2

# -------------------- Parte 3 --------------------

cinta, cabezal = {0: "0"}, 0
filas = []
for i in range(1, 17):
    antes = potencial(cinta)
    cabezal, pasos = ejecutar(INC, cinta, cabezal, "inc", "fin")
    filas.append((i, format(i, "b"), pasos, potencial(cinta), pasos + potencial(cinta) - antes))
print(f"{'i':>3} {'binario':>8} {'real':>5} {'Phi':>4} {'amortizado':>11}")
for f in filas:
    print(f"{f[0]:>3} {f[1]:>8} {f[2]:>5} {f[3]:>4} {f[4]:>11}")
