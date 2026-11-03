"""Ejercicio 8 del Tema 1: los elementos que aparecen más de n/3 veces, con dos
candidatos.

    python ejercicio-08.py

Imprime todas las tablas que cita ejercicio-08.md, corre las pruebas y regenera las
dos figuras (ejercicio-08-trios.svg y ejercicio-08-generadores.svg). Cada número que
aparece en la prosa sale de aquí. Solo necesita matplotlib.
"""

import itertools
import random
from collections import Counter

import matplotlib

matplotlib.use("svg")
import matplotlib.pyplot as plt


# --------------------------------------------------------------------------
# 1. El algoritmo y sus variantes
# --------------------------------------------------------------------------

def first_pass(A, orden_malo=False):
    """Dos pares candidato-contador. Devuelve (c1, k1, c2, k2). Con orden_malo = True,
    un lugar vacío se llena antes de mirar si x ya es el otro candidato: es el error
    de la sección 6."""
    c1 = c2 = None
    k1 = k2 = 0
    for x in A:
        if k1 > 0 and x == c1:
            k1 += 1
        elif orden_malo and k1 == 0:
            c1, k1 = x, 1
        elif k2 > 0 and x == c2:
            k2 += 1
        elif k1 == 0:
            c1, k1 = x, 1
        elif k2 == 0:
            c2, k2 = x, 1
        else:                                   # x distinto de los dos: se forma un trío
            k1 -= 1
            k2 -= 1
    return c1, k1, c2, k2


def more_than_third(A, orden_malo=False):
    """El algoritmo completo: primera pasada y verificación."""
    c1, k1, c2, k2 = first_pass(A, orden_malo)
    candidatos = [c for c, k in ((c1, k1), (c2, k2)) if k > 0]
    return [c for c in candidatos if 3 * A.count(c) > len(A)]


def unverified(A):
    """El atajo: devolver los candidatos con contador positivo."""
    c1, k1, c2, k2 = first_pass(A)
    return [c for c, k in ((c1, k1), (c2, k2)) if k > 0]


def oraculo(A):
    return {x for x, k in Counter(A).items() if 3 * k > len(A)}


def se_parte_en_trios(S):
    """Un multiconjunto se parte en tríos de elementos distintos si y solo si su
    tamaño es múltiplo de 3 y ningún elemento ocupa más de un tercio."""
    return len(S) % 3 == 0 and all(3 * k <= len(S) for k in Counter(S).values())


def seccion(titulo):
    print()
    print(titulo)
    print("-" * len(titulo))


def miles(x):
    return f"{x:,}".replace(",", " ")


# --------------------------------------------------------------------------
# 2. Las tablas que cita la prosa
# --------------------------------------------------------------------------

EJEMPLO = list("ABCABADBAEAB")


def traza(A):
    """La primera pasada, guardando qué posiciones forman cada trío y cuáles quedan
    como copias de los candidatos."""
    c1 = c2 = None
    p1, p2, trios, filas = [], [], [], []
    for i, x in enumerate(A):
        if p1 and x == c1:
            p1.append(i)
        elif p2 and x == c2:
            p2.append(i)
        elif not p1:
            c1, p1 = x, [i]
        elif not p2:
            c2, p2 = x, [i]
        else:
            trios.append((p1.pop(), p2.pop(), i))
        filas.append((i, x, c1 if p1 else "–", len(p1), c2 if p2 else "–", len(p2)))
    return filas, trios, p1, p2


def ejemplo_chico():
    seccion("§2. Ejemplo chico: A B C A B A D B A E A B")
    A = EJEMPLO
    filas, trios, p1, p2 = traza(A)
    print(f"{'i':>2} {'x':>2}  {'c1':>3} {'k1':>3}  {'c2':>3} {'k2':>3}")
    for i, x, c1, k1, c2, k2 in filas:
        print(f"{i:>2} {x:>2}  {c1:>3} {k1:>3}  {c2:>3} {k2:>3}")
    print("tríos (posiciones):", " ".join(f"{a}-{b}-{c}" for a, b, c in trios))
    print("cuentas:", dict(sorted(Counter(A).items())), f" n/3 = {len(A) / 3:g}")
    print(f"sin verificar devuelve {sorted(unverified(A))}; verificado devuelve "
          f"{sorted(more_than_third(A))}; el oráculo dice {sorted(oraculo(A))}")
    return trios, p1, p2


def invariante_vigilado():
    seccion("§3. El invariante reforzado, vigilado con assert")
    rng = random.Random(3)
    prefijos = 0
    for _ in range(4000):
        A = [rng.choice("ABCD") for _ in range(rng.randint(1, 20))]
        c1 = c2 = None
        k1 = k2 = 0
        for i, x in enumerate(A):
            if k1 > 0 and x == c1:
                k1 += 1
            elif k2 > 0 and x == c2:
                k2 += 1
            elif k1 == 0:
                c1, k1 = x, 1
            elif k2 == 0:
                c2, k2 = x, 1
            else:
                k1 -= 1
                k2 -= 1
            resto = Counter(A[:i + 1])
            if k1:
                resto[c1] -= k1
            if k2:
                resto[c2] -= k2
            assert all(v >= 0 for v in resto.values())
            assert not (k1 > 0 and k2 > 0 and c1 == c2)
            assert se_parte_en_trios(list(resto.elements()))
            prefijos += 1
    print(f"invariante comprobado en {miles(prefijos)} prefijos, sin fallos")


def todas(n, alfabeto):
    return (list(t) for t in itertools.product(alfabeto, repeat=n))


def contraejemplos():
    seccion("§5. Los contraejemplos más cortos")
    for nombre, alfabeto in [("dos símbolos", "AB"), ("tres símbolos", "ABC")]:
        for n in range(1, 13):
            malo = next((A for A in todas(n, alfabeto)
                         if set(unverified(A)) != oraculo(A)), None)
            if malo:
                print(f"{nombre}: {' '.join(malo)} -> cuentas "
                      f"{dict(sorted(Counter(malo).items()))}, sin verificar "
                      f"{sorted(unverified(malo))}, verdad {sorted(oraculo(malo))}")
                break


def plantados(rng, cuantos, alfabeto=100):
    """Planta `cuantos` elementos con más de n/3 apariciones cada uno."""
    n = rng.randint(3 * cuantos, 30)
    elegidos = rng.sample(range(alfabeto), cuantos)
    copias = n // 3 + 1
    A = [e for e in elegidos for _ in range(copias)]
    A += [rng.randrange(alfabeto) for _ in range(n - len(A))]
    rng.shuffle(A)
    return A


def generadores():
    seccion("§5 y §6. Qué generadores atrapan cada error")
    rng = random.Random(5)
    gens = {
        "dos plantados": lambda: plantados(rng, 2),
        "uno plantado": lambda: plantados(rng, 1),
        "mayoría plantada": lambda: (lambda n: rng.sample(
            [0] * (n // 2 + 1) + [rng.randrange(1, 100) for _ in range(n - n // 2 - 1)],
            n))(rng.randint(1, 30)),
        "dos símbolos": lambda: [rng.choice("AB") for _ in range(rng.randint(1, 30))],
        "tres símbolos": lambda: [rng.choice("ABC") for _ in range(rng.randint(1, 30))],
        "cinco símbolos": lambda: [rng.choice("ABCDE") for _ in range(rng.randint(1, 30))],
    }
    tabla = {}
    print(f"{'generador':>17} {'verificado':>11} {'sin verificar':>14} {'orden malo':>11}")
    for nombre, g in gens.items():
        casos = [g() for _ in range(4000)]
        f = [100 * sum(set(v(A)) != oraculo(A) for A in casos) / len(casos)
             for v in (more_than_third, unverified, lambda A: more_than_third(A, True))]
        tabla[nombre] = f
        print(f"{nombre:>17} {f[0]:>10.1f}% {f[1]:>13.1f}% {f[2]:>10.1f}%")
    # los falsos del atajo son siempre de más, nunca de menos
    rng2 = random.Random(9)
    de_menos = 0
    for _ in range(20_000):
        A = [rng2.choice("ABCDE") for _ in range(rng2.randint(1, 30))]
        de_menos += not oraculo(A) <= set(unverified(A))
    print(f"en 20 000 arreglos de cinco símbolos, el atajo deja afuera un elemento "
          f"correcto {de_menos} veces")
    return tabla


def orden_malo_minimo():
    seccion("§6. El orden de los if: el contraejemplo más corto")
    for n in range(1, 10):
        malo = next((A for A in todas(n, "ABC")
                     if set(more_than_third(A, True)) != oraculo(A)), None)
        if malo:
            c1, k1, c2, k2 = first_pass(malo, True)
            print(f"{' '.join(malo)}: candidatos ({c1}, {k1}) y ({c2}, {k2}); "
                  f"verificado con el orden malo {sorted(more_than_third(malo, True))}, "
                  f"verdad {sorted(oraculo(malo))}")
            break


# --------------------------------------------------------------------------
# 3. Pruebas
# --------------------------------------------------------------------------

def pruebas():
    seccion("Pruebas")
    comprobaciones = 0
    rng = random.Random(2026)

    # (a) el algoritmo contra el oráculo, en todos los arreglos chicos de 4 símbolos
    for n in range(0, 8):
        for A in todas(n, "ABCD"):
            assert sorted(more_than_third(A)) == sorted(oraculo(A))
            comprobaciones += 1

    # (b) y en arreglos al azar más grandes
    for _ in range(20_000):
        k = rng.choice([2, 3, 4, 10, 100])
        A = [rng.randrange(k) for _ in range(rng.randint(0, 60))]
        assert sorted(more_than_third(A)) == sorted(oraculo(A))
        assert oraculo(A) <= set(unverified(A))     # el atajo nunca deja a nadie afuera
        comprobaciones += 2

    # (c) con dos plantados, el atajo no se equivoca nunca
    for _ in range(20_000):
        A = plantados(rng, 2, alfabeto=rng.choice([3, 5, 100]))
        assert sorted(unverified(A)) == sorted(oraculo(A))
        comprobaciones += 1

    # (d) el criterio de los tríos coincide con buscar la partición por fuerza bruta
    def particion_bruta(S):
        if not S:
            return True
        x = S[0]
        resto = S[1:]
        for i, j in itertools.combinations(range(len(resto)), 2):
            if len({x, resto[i], resto[j]}) == 3:
                nuevo = [v for k, v in enumerate(resto) if k not in (i, j)]
                if particion_bruta(nuevo):
                    return True
        return False

    for n in range(0, 10):
        for S in itertools.combinations_with_replacement("ABCD", n):
            assert se_parte_en_trios(list(S)) == particion_bruta(list(S))
            comprobaciones += 1

    print(f"{miles(comprobaciones)} comprobaciones, 0 fallos")


# --------------------------------------------------------------------------
# 4. Figuras
# --------------------------------------------------------------------------

TINTA, APAGADO, REGLA = "#1a1a1a", "#6b7280", "#d8dce3"
ACENTO, OSCURO, CALIDO, ALARMA = "#0891b2", "#0e7490", "#b45309", "#be123c"


def _estilo():
    plt.rcParams.update({
        "font.size": 9, "axes.edgecolor": APAGADO, "axes.labelcolor": TINTA,
        "xtick.color": APAGADO, "ytick.color": APAGADO,
        "figure.facecolor": "white", "svg.hashsalt": "ejercicio-08",
    })


def _guardar(fig, nombre):
    fig.tight_layout()
    fig.savefig(nombre, metadata={"Date": None})
    plt.close(fig)


def figura_trios(trios, p1, p2):
    A = EJEMPLO
    fig, ax = plt.subplots(figsize=(6.8, 2.4))
    colores_trio = [ACENTO, CALIDO, "#7c3aed", "#059669"]
    grupo = {}
    for t, trio in enumerate(trios):
        for p in trio:
            grupo[p] = colores_trio[t % len(colores_trio)]
    for p in p1 + p2:
        grupo[p] = ALARMA
    for i, x in enumerate(A):
        color = grupo[i]
        ax.add_patch(plt.Rectangle((i, 0), 0.85, 0.85, facecolor="white", edgecolor=color,
                                   lw=1.8))
        ax.text(i + 0.425, 0.425, x, ha="center", va="center", fontsize=10, color=color)
        ax.text(i + 0.425, -0.3, str(i), ha="center", fontsize=7, color=APAGADO)
    for t, trio in enumerate(trios):
        color = colores_trio[t % len(colores_trio)]
        xs = [p + 0.425 for p in trio]
        y = 1.1 + 0.28 * t
        ax.plot([min(xs), max(xs)], [y, y], color=color, lw=1.2)
        for xx in xs:
            ax.plot([xx, xx], [0.85, y], color=color, lw=0.8)
    ax.text(len(A) + 0.2, 0.425, "en rojo: copias\nde los candidatos", fontsize=8,
            color=ALARMA, va="center")
    ax.set_xlim(-0.3, len(A) + 2.6)
    ax.set_ylim(-0.6, 1.1 + 0.28 * len(trios) + 0.2)
    ax.set_aspect("equal")
    ax.axis("off")
    _guardar(fig, "ejercicio-08-trios.svg")


def figura_generadores(tabla):
    fig, ax = plt.subplots(figsize=(7.0, 3.0))
    nombres = list(tabla)
    ancho = 0.27
    for k, (etiqueta, color) in enumerate([("verificado", OSCURO),
                                           ("sin verificar", ALARMA),
                                           ("orden malo", CALIDO)]):
        alturas = [tabla[n][k] for n in nombres]
        pos = [i + (k - 1) * ancho for i in range(len(nombres))]
        ax.bar(pos, alturas, ancho, color=color, label=etiqueta)
        for xx, h in zip(pos, alturas):
            ax.text(xx, h + 1, f"{h:.0f}", ha="center", fontsize=7, color=color)
    ax.set_xticks(range(len(nombres)))
    ax.set_xticklabels(nombres, fontsize=8)
    ax.set_ylabel("% de arreglos mal")
    ax.set_ylim(0, max(max(v) for v in tabla.values()) * 1.2 + 3)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color=REGLA, lw=0.6)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    _guardar(fig, "ejercicio-08-generadores.svg")


if __name__ == "__main__":
    trios, p1, p2 = ejemplo_chico()
    invariante_vigilado()
    contraejemplos()
    tabla = generadores()
    orden_malo_minimo()
    pruebas()
    _estilo()
    figura_trios(trios, p1, p2)
    figura_generadores(tabla)
    print("\nfiguras: ejercicio-08-trios.svg, ejercicio-08-generadores.svg")
