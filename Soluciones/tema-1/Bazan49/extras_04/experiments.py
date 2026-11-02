"""Experimentos del ejercicio 4"""
import json

from solution import cinta_de, texto, unos, incrementar, total_exacto

R = {}

# ---- A. n incrementos seguidos desde 0 ----
print("\nA. n incrementos seguidos desde 0 (una sola cinta, simulando la maquina paso a paso)")
print(f"{'n':>9} {'T(n)':>10} {'4n-2 s2(n)':>11} {'T/n':>7} {'peor operacion':>15} {'n*peor':>12} {'n*peor / T':>11}")
cinta = cinta_de("0")
T, peor = 0, 0
E_MAX = 20
marcas = {2 ** e for e in range(0, E_MAX + 1)} | {10 ** 6}
filasA, acum = [], []
for i in range(1, 2 ** E_MAX + 1):
    p = incrementar(cinta)[0]
    T += p
    peor = max(peor, p)
    assert T == total_exacto(i), (i, T)                     # la formula exacta en CADA n
    if i in marcas:
        print(f"{i:>9} {T:>10} {total_exacto(i):>11} {T / i:>7.4f} {peor:>15} {i * peor:>12} {i * peor / T:>11.2f}")
        filasA.append({"n": i, "T": T, "peor": peor})
R["A"] = filasA
print(f"   verificado en cada n <= 2^{E_MAX} = {2 ** E_MAX}: T(n) = 4n - 2 s2(n)")

# ---- B. Los primeros incrementos: costo real, potencial y costo amortizado ----
print("\nB. Primeros 32 incrementos: costo real c_i, potencial Phi_i = 2 (unos), costo amortizado c_i + Phi_i - Phi_(i-1)")
cinta = cinta_de("0")
phi, filasB = 0, []
for i in range(1, 129):
    p = incrementar(cinta)[0]
    phi2 = 2 * unos(cinta)
    filasB.append({"i": i, "c": p, "phi": phi2, "amort": p + phi2 - phi, "bin": texto(cinta)})
    phi = phi2
for f in filasB[:32]:
    print(f"  i={f['i']:>3}  {f['bin']:>7}  c={f['c']:>2}  Phi={f['phi']:>2}  amortizado={f['amort']}")
R["B"] = filasB

with open("resultados_experimentos_04.json", "w") as f:
    json.dump(R, f)
