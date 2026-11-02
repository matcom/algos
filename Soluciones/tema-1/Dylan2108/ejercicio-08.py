"""Ejercicio 8: elementos que aparecen más de n/3 veces (Boyer-Moore con dos candidatos).

Corre: python ejercicio-08.py
"""
import itertools, random
from collections import Counter

def primera_pasada(A, orden_malo=False):
    """Devuelve [(c1, k1), (c2, k2)]. orden_malo: mira los contadores en 0 ANTES de comparar
    con los candidatos (error plantado: puede dejar c1 == c2)."""
    c1 = c2 = None
    k1 = k2 = 0
    for x in A:
        if orden_malo:              # mira los contadores en 0 antes que los candidatos
            if k1 == 0: c1, k1 = x, 1
            elif k2 == 0: c2, k2 = x, 1
            elif x == c1: k1 += 1
            elif x == c2: k2 += 1
            else: k1 -= 1; k2 -= 1
            continue
        if k1 > 0 and x == c1:
            k1 += 1
        elif k2 > 0 and x == c2:
            k2 += 1
        elif k1 == 0:
            c1, k1 = x, 1
        elif k2 == 0:
            c2, k2 = x, 1
        else:                       # x distinto de los dos: se cancela un trío
            k1 -= 1; k2 -= 1
    return [(c1, k1), (c2, k2)]


def mas_de_un_tercio(A):
    """La versión correcta: primera pasada + verificación."""
    cands = {c for c, k in primera_pasada(A) if k > 0}
    return {c for c in cands if 3 * A.count(c) > len(A)}


def sin_verificar(A, **kw):
    """El atajo: los candidatos con contador positivo."""
    return {c for c, k in primera_pasada(A, **kw) if k > 0}


def oraculo(A):
    return {x for x, k in Counter(A).items() if 3 * k > len(A)}


def se_parte_en_trios(S):
    """Un multiconjunto se parte en tríos de distintos sii |S| = 3t y nadie aparece más de t veces."""
    return len(S) % 3 == 0 and all(3 * k <= len(S) for k in Counter(S).values())


def particion_constructiva(S):
    """El lema, constructivo: ordenar (agrupando iguales) y formar tríos (i, i+t, i+2t)."""
    S = sorted(S, key=lambda x: (str(type(x)), x))
    t = len(S) // 3
    return [(S[i], S[i + t], S[i + 2 * t]) for i in range(t)]


def primera_pasada_vigilada(A):
    c1 = c2 = None
    k1 = k2 = 0
    for i, x in enumerate(A):
        if k1 > 0 and x == c1: k1 += 1
        elif k2 > 0 and x == c2: k2 += 1
        elif k1 == 0: c1, k1 = x, 1
        elif k2 == 0: c2, k2 = x, 1
        else: k1 -= 1; k2 -= 1
        # Invariante reforzado: (a) si los dos contadores son positivos, c1 != c2;
        # (b) quitando k1 copias de c1 y k2 de c2, el prefijo se parte en tríos de distintos.
        assert not (k1 > 0 and k2 > 0 and c1 == c2)
        resto = Counter(A[:i + 1])
        if k1: resto[c1] -= k1
        if k2: resto[c2] -= k2
        assert min(resto.values(), default=0) >= 0
        S = list(resto.elements())
        assert se_parte_en_trios(S)
        assert all(len(set(t)) == 3 for t in particion_constructiva(S))
    return [(c1, k1), (c2, k2)]


if __name__ == "__main__":
    # 1. El teorema, exhaustivo en arreglos chicos: todo elemento > n/3 es candidato con contador > 0
    total = 0
    for sigma, L in [("ABC", 9), ("ABCD", 7)]:
        for n in range(L + 1):
            for A in itertools.product(sigma, repeat=n):
                A = list(A)
                total += 1
                pos = {c for c, k in primera_pasada_vigilada(A) if k > 0}
                assert oraculo(A) <= pos
                assert mas_de_un_tercio(A) == oraculo(A)
    print(f"exhaustivo: {total} arreglos (alfabeto 3 hasta n=9, alfabeto 4 hasta n=7)")
    print("  invariante reforzado vigilado en cada prefijo; versión verificada == oráculo")

    # 2. Pruebas aleatorias grandes
    rng = random.Random(2026)
    for _ in range(3000):
        n = rng.randint(0, 60)
        A = [rng.choice("ABCDEFG"[:rng.randint(1, 7)]) for _ in range(n)]
        assert mas_de_un_tercio(A) == oraculo(A)
    print("3000 arreglos aleatorios (n <= 60): versión verificada == oráculo")

    # 3. El atajo sin verificar: ¿qué generador NO lo atrapa?
    def plantar(n, pesados):
        """`pesados` elementos con más de n/3 copias cada uno; el resto, al azar entre 5 símbolos."""
        A = []
        for p in "XY"[:pesados]:
            A += [p] * (n // 3 + 1)
        A += [rng.choice("ABCDE") for _ in range(n - len(A))]
        rng.shuffle(A)
        return A

    generadores = {
        "binario {A,B}": lambda n: [rng.choice("AB") for _ in range(n)],
        "3 símbolos": lambda n: [rng.choice("ABC") for _ in range(n)],
        "5 símbolos": lambda n: [rng.choice("ABCDE") for _ in range(n)],
        "1 elemento > n/3 plantado": lambda n: plantar(n, 1),
        "2 elementos > n/3 plantados": lambda n: plantar(n, 2),
        "mayoría (> n/2) plantada": lambda n: (lambda m: rng.sample([m] * (n // 2 + 1) + [rng.choice("ABCDE") for _ in range(n - n // 2 - 1)], n))(rng.choice("ABCDE")),
    }
    print(f"\n{'generador':>30} {'atajo sin verificar':>20} {'verificada':>11}")
    resultados = {}
    for nombre, g in generadores.items():
        casos = [g(rng.randint(3, 30)) for _ in range(4000)]
        fa = sum(sin_verificar(A) != oraculo(A) for A in casos) / len(casos)
        fv = sum(mas_de_un_tercio(A) != oraculo(A) for A in casos) / len(casos)
        resultados[nombre] = 100 * fa
        assert fv == 0
        print(f"{nombre:>30} {100 * fa:>19.1f}% {100 * fv:>10.1f}%")
    assert resultados["2 elementos > n/3 plantados"] == 0
    assert resultados["binario {A,B}"] > 0

    # contraejemplos mínimos
    print("\natajo en 'AAB':", sin_verificar(list("AAB")), " oráculo:", oraculo(list("AAB")))
    print("atajo en 'ABCD':", sin_verificar(list("ABCD")), " oráculo:", oraculo(list("ABCD")),
          "(A, B, C se cancelan; D sobrevive con contador 1)")

    # 4. Segundo error plantado: el orden de las ramas
    malos = [A for A in (list(p) for n in range(1, 7) for p in itertools.product("ABC", repeat=n))
             if {c for c, k in primera_pasada(A, orden_malo=True) if k > 0 and 3 * A.count(c) > len(A)} != oraculo(A)]
    print(f"\norden de ramas equivocado: falla (aun verificando) en {len(malos)} arreglos de n <= 6; el menor: {''.join(min(malos, key=len))}")
    A = list(min(malos, key=len))
    print("  estado final:", primera_pasada(A, orden_malo=True), " oráculo:", oraculo(A))
    verif_malo = lambda A: {c for c, k in primera_pasada(A, orden_malo=True) if k > 0 and 3 * A.count(c) > len(A)}
    for nombre in ["binario {A,B}", "3 símbolos", "2 elementos > n/3 plantados"]:
        casos = [generadores[nombre](rng.randint(3, 30)) for _ in range(4000)]
        f = sum(verif_malo(A) != oraculo(A) for A in casos) / len(casos)
        print(f"  {nombre:>30}: {100 * f:.1f}% de fallos (con verificación)")

    # 5. Figura
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("(sin matplotlib)")
    else:
        fig, ax = plt.subplots(figsize=(8, 3.6))
        nombres = list(resultados)
        ax.barh(nombres, [resultados[k] for k in nombres], color=["#dc2626" if resultados[k] else "#9ca3af" for k in nombres])
        for i, k in enumerate(nombres):
            ax.text(resultados[k] + 1, i, f"{resultados[k]:.1f} %", va="center", fontsize=9)
        ax.invert_yaxis()
        ax.set_xlabel("% de arreglos en que el atajo sin verificar se equivoca")
        ax.set_xlim(0, 105)
        ax.set_title("¿Qué generador atrapa el atajo?")
        fig.tight_layout()
        fig.savefig("ejercicio-08-generadores.png", dpi=150)
        print("\nfigura: ejercicio-08-generadores.png")
