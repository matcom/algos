import math
import matplotlib.pyplot as plt


def factor_formula(n, veces=1000):
    k = veces
    for _ in range(50):
        k = veces * math.log2(n) / (math.log2(n) + math.log2(k))
    return k


# Figura 1: el factor de n log n segun el n de partida
ns = [10**(e / 4) for e in range(8, 121)]  # de 100 a 10^30
factores = [factor_formula(n) for n in ns]

plt.figure(figsize=(8, 4.5))
plt.plot(ns, factores, label="n log n", linewidth=2)
plt.axhline(1000, color="gray", linestyle="--", label="1000 (lineal)")
plt.axhline(math.sqrt(1000), color="red", linestyle="--", label="31.6 (n²)")
plt.axvline(9.86e10, color="green", linestyle=":", label="n de la conferencia")
plt.xscale("log")
plt.ylim(0, 1100)
plt.xlabel("n que se resolvia antes")
plt.ylabel("cuantas veces crece la entrada")
plt.title("Computadora 1000 veces mas rapida")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("ejercicio-01-factor.png", dpi=120)

# Figura 2: cuanto trabajo hay que hacer si la entrada crece 1000 veces
# (antes n = 10^11). Si el trabajo pasa de 1000, no alcanza.
n = 10**11
trabajo_nlogn = (1000 * n * math.log2(1000 * n)) / (n * math.log2(n))
nombres = ["n", "n log n", "n²"]
trabajo = [1000, trabajo_nlogn, 1000**2]

plt.figure(figsize=(7, 4))
barras = plt.bar(nombres, trabajo, color=["tab:green", "tab:orange", "tab:red"])
plt.axhline(1000, color="black", linestyle="--", label="lo que da la maquina nueva (1000x)")
plt.yscale("log")
plt.ylabel("veces mas trabajo")
plt.title("Si la entrada crece 1000 veces, ¿cuanto mas trabajo es?")
for b, t in zip(barras, trabajo):
    plt.text(b.get_x() + b.get_width() / 2, t * 1.15, f"{t:,.0f}", ha="center")
plt.legend()
plt.tight_layout()
plt.savefig("ejercicio-01-trabajo.png", dpi=120)
