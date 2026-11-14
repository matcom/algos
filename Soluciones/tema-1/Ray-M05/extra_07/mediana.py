import math
import sys
from itertools import combinations

from comun.tabla import tabla_md


def mediana(A, B, mayor_o_igual=lambda x, y: x >= y):
    n = len(A)
    lo, hi = 0, n
    while lo < hi:
        i = (lo + hi) // 2
        if mayor_o_igual(A[i], B[n - i - 1]):
            hi = i
        else:
            lo = i + 1
    i = lo
    if i == 0:
        return "B", n - 1
    if i == n:
        return "A", n - 1
    return ("A", i - 1) if mayor_o_igual(A[i - 1], B[n - i - 1]) else ("B", n - i - 1)


def intercalaciones(n):
    for lugares in combinations(range(2 * n), n):
        en_A = set(lugares)
        yield ([r for r in range(2 * n) if r in en_A],
               [r for r in range(2 * n) if r not in en_A])


SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def nombre(lado, k):
    return f"{lado}{str(k + 1).translate(SUB)}"


def arbol(n):
    raiz = {}
    for rangos_A, rangos_B in intercalaciones(n):
        A = [("A", k, r) for k, r in enumerate(rangos_A)]
        B = [("B", k, r) for k, r in enumerate(rangos_B)]
        preguntas = []

        def mayor_o_igual(x, y):
            preguntas.append((nombre(x[0], x[1]), nombre(y[0], y[1]), x[2] >= y[2]))
            return x[2] >= y[2]

        lado, k = mediana(A, B, mayor_o_igual)
        nodo = raiz
        for p, q, respuesta in preguntas:
            nodo.setdefault("pregunta", (p, q))
            assert nodo["pregunta"] == (p, q)
            nodo = nodo.setdefault(respuesta, {})
        nodo["salida"] = nombre(lado, k)

    hojas, altura = [], 0

    def recorrer(nodo, prof):
        nonlocal altura
        if "salida" in nodo:
            hojas.append(nodo["salida"])
            altura = max(altura, prof)
        else:
            for r in (True, False):
                if r in nodo:
                    recorrer(nodo[r], prof + 1)

    recorrer(raiz, 0)
    return raiz, hojas, altura


def mermaid(raiz):
    lineas, contador = ["flowchart TD"], [0]

    def visitar(nodo):
        mio = f"n{contador[0]}"
        contador[0] += 1
        if "salida" in nodo:
            lineas.append(f'    {mio}(["{nodo["salida"]}"])')
            return mio
        p, q = nodo["pregunta"]
        lineas.append(f'    {mio}{{"{p} ≥ {q}"}}')
        for r, rotulo in ((True, "sí"), (False, "no")):
            if r in nodo:
                hijo = visitar(nodo[r])
                lineas.append(f"    {mio} -->|{rotulo}| {hijo}")
        return mio

    visitar(raiz)
    return "\n".join(lineas)


def _arbol():
    raiz, hojas, altura = arbol(3)
    print("```mermaid\n" + mermaid(raiz) + "\n```")


def _cuentas():
    filas = []
    for n in range(1, 9):
        peor, salidas = 0, set()
        for A, B in intercalaciones(n):
            cuenta = [0]

            def mayor_o_igual(x, y):
                cuenta[0] += 1
                return x >= y

            lado, k = mediana(A, B, mayor_o_igual)
            assert (A if lado == "A" else B)[k] == sorted(A + B)[n - 1]
            peor = max(peor, cuenta[0])
            salidas.add((lado, k))
        filas.append([n, f"{math.comb(2 * n, n):,}", len(salidas), peor,
                      math.ceil(math.log2(n + 1)) + 1, math.ceil(math.log2(2 * n))])
    print(tabla_md(["n", "intercalaciones", "salidas distintas", "peor caso medido",
                    "⌈log₂(n+1)⌉ + 1", "cota ⌈log₂ 2n⌉"], filas, "dddddd"))


SECCIONES = {
    "arbol": _arbol,
    "cuentas": _cuentas,
}

if __name__ == "__main__":
    SECCIONES[sys.argv[1]]()
