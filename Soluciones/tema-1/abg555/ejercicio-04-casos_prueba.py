import importlib
import math

tm = importlib.import_module("ejercicio-04-turing")
counter, counter_from_left = tm.counter, tm.counter_from_left


def unos_al_final(k):
    # cuantos 1 hay al final de k escrito en binario
    t = 0
    while k & 1:
        k >>= 1
        t += 1
    return t


# ===============================================================
print("Prueba 1: los primeros incrementos, con la cinta")
M = counter()
print(f"{'incremento':>11} {'valor':>6} {'pasos':>6}   cinta (el cabezal entre corchetes)")
for k in range(1, 9):
    pasos = M.run()
    print(f"{k:>11} {M.value():>6} {pasos:>6}   {M.text()}")
assert M.value() == 8
print("OK\n")

# ===============================================================
print("Prueba 2: el valor y la posicion del cabezal, contra el oraculo")
M = counter()
for k in range(1, 5001):
    M.run()
    assert M.value() == k                     # la cinta tiene el numero correcto
    assert M.head == 0                        # el cabezal vuelve al bit menos significativo
print("5000 incrementos: siempre el valor correcto y el cabezal en el bit menos significativo")
print("OK\n")

# ===============================================================
print("Prueba 3: el costo de un incremento es 2t + 2 (t = unos al final antes de sumar)")
M = counter()
for k in range(1, 5001):
    pasos = M.run()
    assert pasos == 2 * unos_al_final(k - 1) + 2
print("5000 incrementos: el costo coincide siempre con 2t + 2")
print("OK\n")

# ===============================================================
print("Prueba 4: el potencial, Phi = 2 * (cantidad de unos en la cinta)")
M = counter()
amortizados = set()
for k in range(1, 5001):
    antes = 2 * M.ones()
    pasos = M.run()
    despues = 2 * M.ones()
    assert despues >= 0
    amortizados.add(pasos + despues - antes)
print("costos amortizados que aparecen en 5000 incrementos:", amortizados)
assert amortizados == {4}
print("OK\n")

# ===============================================================
print("Prueba 5: el costo total de m incrementos desde 0")
print(f"{'m':>8} {'total':>9} {'4m - 2*unos(m)':>15} {'total / m':>10} {'el mas caro':>12} {'2*log2(m)+2':>12}")
M, total, mas_caro, m = counter(), 0, 0, 0
for objetivo in [10, 100, 1000, 1024, 10000, 65535, 65536]:
    while m < objetivo:
        pasos = M.run()
        total += pasos
        mas_caro = max(mas_caro, pasos)
        m += 1
    formula = 4 * m - 2 * bin(m).count("1")
    print(f"{m:>8,} {total:>9,} {formula:>15,} {total / m:>10.3f} {mas_caro:>12} "
          f"{2 * math.log2(m) + 2:>12.1f}")
    assert total == formula and total <= 4 * m
print("OK\n")

# ===============================================================
print("Prueba 6: un solo incremento puede costar Theta(log m)")
print(f"{'de':>8} {'a':>8} {'pasos':>6} {'2 * bits + 2':>13}")
M = counter()
for k in range(1, 2 ** 16 + 1):
    pasos = M.run()
    if k & (k - 1) == 0 and k >= 2:           # k es potencia de 2: de 2^j - 1 a 2^j
        j = int(math.log2(k))
        if j in (1, 4, 8, 12, 16):
            print(f"{k - 1:>8,} {k:>8,} {pasos:>6} {2 * j + 2:>13}")
        assert pasos == 2 * j + 2
print("OK\n")

# ===============================================================
print("Prueba 7: la variante que deja el cabezal en el bit mas significativo")
print(f"{'m':>7} {'total / m (LSB)':>16} {'total / m (MSB)':>16} {'log2(m)':>8}")
for m in [16, 256, 4096, 2 ** 15]:
    A, B = counter(), counter_from_left()
    ta = sum(A.run() for _ in range(m))
    tb = sum(B.run() for _ in range(m))
    assert A.value() == B.value() == m
    print(f"{m:>7,} {ta / m:>16.2f} {tb / m:>16.2f} {math.log2(m):>8.1f}")
print("OK")
