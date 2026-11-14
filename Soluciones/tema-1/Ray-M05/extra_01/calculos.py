import math
import sys

from comun.tabla import cientifica, num, potencia, tabla_md

HORA = 3600 * 10**9
K = 1000


def mayor_n(costo, presupuesto):
    alto = 2
    while costo(alto) <= presupuesto:
        alto *= 2
    bajo = alto // 2
    while bajo + 1 < alto:
        medio = (bajo + alto) // 2
        if costo(medio) <= presupuesto:
            bajo = medio
        else:
            alto = medio
    return bajo


def factor(costo, presupuesto, k=K):
    return mayor_n(costo, k * presupuesto) / mayor_n(costo, presupuesto)


def cuadratico(n):
    return n * n


def n_log_n(n):
    return n * math.log2(n)


def tamano_n_log_n(C):
    bajo, alto = 1.0, max(2.0, C)
    for _ in range(300):
        medio = (bajo + alto) / 2
        if medio * math.log2(medio) <= C:
            bajo = medio
        else:
            alto = medio
    return bajo


def g(f, L, k=K):
    return k * L / (L + math.log2(f))


def factor_n_log_n(L, k=K):
    bajo, alto = 1.0, float(k)
    for _ in range(200):
        medio = (bajo + alto) / 2
        if medio * (L + math.log2(medio)) <= k * L:
            bajo = medio
        else:
            alto = medio
    return bajo


def cotas_n_log_n(L, k=K):
    f1 = g(k, L, k)
    return f1, g(f1, L, k)


def _verificacion():
    L = math.log2(tamano_n_log_n(HORA))
    filas = []
    for k in [10, 100, 1000, 10**6]:
        f1, f2 = cotas_n_log_n(L, k)
        filas.append([f"{k:,}", num(factor(cuadratico, HORA, k), 2), num(math.sqrt(k), 2),
                      num(factor(n_log_n, HORA, k), 1), num(factor_n_log_n(L, k), 1),
                      f"{num(f1, 1)} – {num(f2, 1)}"])
    print(tabla_md(["k", "n²: medido", "√k", "n log n: medido", "n log n: f",
                    "f₁ – f₂ (a mano)"], filas, "dddddd"))


def _por_tamano():
    filas = []
    for exponente in [3, 6, 9, 12, 18, 30, 100]:
        L = exponente * math.log2(10)
        f = factor_n_log_n(L)
        f1, _ = cotas_n_log_n(L)
        filas.append([potencia(10, exponente), num(L, 1), num(f, 1), num(f1, 1),
                      f"{100 * (1 - f / K):.1f}%"])
    print(tabla_md(["n actual", "L = log₂ n", "factor f", "cota inferior f₁",
                    "pérdida 1 − f/k"], filas, "ddddd"))


SECCIONES = {
    "verificacion": _verificacion,
    "por_tamano": _por_tamano,
}

if __name__ == "__main__":
    SECCIONES[sys.argv[1]]()
