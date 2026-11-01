import math

def trailing_ones(v):
    """numero de bits 1 consecutivos desde el bit menos significativo de v"""
    t = 0
    while v & 1:
        t += 1
        v >>= 1
    return t

def popcount(v):
    return bin(v).count("1")

def simular(m):
    """Simula m incrementos desde 0. Devuelve costo total en 'pasos de maquina de Turing'
    (ida+vuelta del cabezal) y en 'bits volteados' (lo que acota el potencial)."""
    pasos_tm = 0
    bits_volteados = 0
    peor_incremento = 0
    v = 0
    for _ in range(m):
        t = trailing_ones(v)          # cuantos 1 consecutivos hay que voltear
        costo_flips = t + 1           # t unos pasan a 0 y un 0 pasa a 1: t+1 bits cambian
        costo_tm = 2 * (t + 1)        # ida (t+1 celdas) + vuelta (t+1 celdas)
        pasos_tm += costo_tm
        bits_volteados += costo_flips
        peor_incremento = max(peor_incremento, costo_tm)
        v += 1
    return pasos_tm, bits_volteados, peor_incremento

print("        m   pasos TM   TM/m   cota 4m  peor op  log2 m")
for m in [10, 100, 1_000, 10_000, 100_000, 1_000_000]:
    pasos_tm, flips, peor = simular(m)
    assert flips < 2 * m                  # la cota amortizada de bits volteados (Teorema)
    assert pasos_tm <= 4 * m              # la cota en pasos de Turing (Corolario)
    print(f"{m:>9}{pasos_tm:>11}{pasos_tm/m:>7.3f}{4*m:>10}{peor:>9}{math.log2(m):>8.2f}")

# Verificacion del potencial de Hamming exacto: Delta(Phi) = 1 - t_i en cada paso
print()
print("verificando Delta(Phi) = 1 - t_i exactamente, paso a paso, para m=200000:")
v = 0
Phi_anterior = popcount(v)
fallos = 0
for i in range(200_000):
    t = trailing_ones(v)
    v_nuevo = v + 1
    Phi_nuevo = popcount(v_nuevo)
    if Phi_nuevo - Phi_anterior != 1 - t:
        fallos += 1
    Phi_anterior = Phi_nuevo
    v = v_nuevo
print("fallos (deberia ser 0):", fallos)

# El peor incremento individual ocurre en m = 2^k - 1 -> 2^k, y cuesta Theta(log m)
print()
print("peor incremento individual, por valor de v justo antes de incrementar:")
for k in [4, 8, 12, 16, 20]:
    v = 2**k - 1              # ...111 (k unos)
    t = trailing_ones(v)
    etiqueta = f"v = 2^{k}-1 = {v}:"
    print(f"{etiqueta:<22}trailing_ones = {t:<2} (=k), costo de ESE incremento = {2*(t+1)}")
