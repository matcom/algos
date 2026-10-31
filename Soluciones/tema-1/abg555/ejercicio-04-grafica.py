import importlib
import matplotlib.pyplot as plt

tm = importlib.import_module("ejercicio-04-turing")
counter, counter_from_left = tm.counter, tm.counter_from_left

# Figura 1: costo real, costo amortizado y potencial en los primeros 40 incrementos
M = counter()
ks, reales, amortizados, potenciales = [], [], [], []
for k in range(1, 41):
    antes = 2 * M.ones()
    pasos = M.run()
    despues = 2 * M.ones()
    ks.append(k)
    reales.append(pasos)
    amortizados.append(pasos + despues - antes)
    potenciales.append(despues)

fig, (a1, a2) = plt.subplots(2, 1, figsize=(9, 5.5), sharex=True)
a1.bar(ks, reales, color="tab:orange", label="costo real (pasos)")
a1.plot(ks, amortizados, color="tab:blue", lw=2, label="costo amortizado")
a1.set_ylabel("pasos")
a1.legend(loc="upper left")
a1.set_title("Los incrementos caros (a 8, 16, 32) los paga el potencial que se fue acumulando")
a2.plot(ks, potenciales, "o-", color="tab:green", label="potencial  2 * (unos en la cinta)")
a2.set_xlabel("incremento")
a2.set_ylabel("potencial")
a2.legend(loc="upper left")
plt.tight_layout()
plt.savefig("ejercicio-04-potencial.png", dpi=120)

# Figura 2: costo promedio por incremento, cabezal en el bit menos o mas significativo
ms = [2 ** j for j in range(1, 16)]
lsb, msb = [], []
A, B, ta, tb, m = counter(), counter_from_left(), 0, 0, 0
for objetivo in ms:
    while m < objetivo:
        ta += A.run()
        tb += B.run()
        m += 1
    lsb.append(ta / m)
    msb.append(tb / m)

plt.figure(figsize=(7.5, 4))
plt.plot(ms, lsb, "o-", label="cabezal en el bit menos significativo")
plt.plot(ms, msb, "o-", color="tab:red", label="cabezal en el bit mas significativo")
plt.axhline(4, color="gray", linestyle="--", label="4 (la cota amortizada)")
plt.xscale("log", base=2)
plt.xlabel("m (incrementos desde 0)")
plt.ylabel("pasos por incremento, en promedio")
plt.title("Volver al bit menos significativo hace que el promedio sea constante")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("ejercicio-04-promedio.png", dpi=120)
