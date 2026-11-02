"""
Ejercicio 9: una mezcla "optimizada" de dos listas ordenadas de largo n.

La mezcla optimizada deja de comparar cuando a la primera lista le queda un
solo elemento, y lo pone al final. Hay que:
  1. contar cuantas comparaciones hace en el peor caso,
  2. decidir si es correcta usando la cota de 2n - 1 comparaciones,
  3. construir con el adversario la entrada en la que falla.

Modelo: comparaciones (solo se pregunta  x <= y).

Uso:
    python ejercicio9_mezcla.py             # corre los experimentos
    python ejercicio9_mezcla.py --figuras   # ademas genera png y gif
"""
import math
import random
import sys
from itertools import combinations


# --------------------------------------------------------------------------
# 1. Las dos mezclas
# --------------------------------------------------------------------------
def mezclar(I, D, cuenta, registro=None):
    """Mezcla correctamente dos listas ordenadas."""
    R, i, j = [], 0, 0
    while i < len(I) and j < len(D):
        cuenta[0] += 1
        if registro is not None:
            registro.append((I[i], D[j]))
        if I[i] <= D[j]:
            R.append(I[i])
            i += 1
        else:
            R.append(D[j])
            j += 1
    return R + I[i:] + D[j:]


def mezclar_optimizada(I, D, cuenta, registro=None):
    """Version propuesta en el enunciado; se conserva para mostrar su fallo."""
    R, i, j = [], 0, 0
    while len(I) - i > 1 and j < len(D):         # <-- antes era i < len(I)
        cuenta[0] += 1
        if registro is not None:
            registro.append((I[i], D[j]))
        if I[i] <= D[j]:
            R.append(I[i])
            i += 1
        else:
            R.append(D[j])
            j += 1
    return R + D[j:] + I[i:]                      # <-- lo que queda de I va al final


def repartos(n):
    """Todas las formas de repartir 1..2n entre las dos listas (valores distintos)."""
    for idx in combinations(range(1, 2 * n + 1), n):
        I = list(idx)
        D = [x for x in range(1, 2 * n + 1) if x not in idx]
        yield I, D


def intercalada(n):
    """La entrada del adversario: a1 < b1 < a2 < b2 < ... < an < bn."""
    return list(range(0, 2 * n, 2)), list(range(1, 2 * n, 2))


# --------------------------------------------------------------------------
# 2. Experimentos
# --------------------------------------------------------------------------
def exp_peor_caso():
    print("== Peor caso exacto, mirando todas las entradas ==")
    print(f"{'n':>2} {'entradas':>9} {'mezcla normal':>14} {'2n-1':>5} {'optimizada':>11} {'2n-2':>5} "
          f"{'fallos':>7} {'C(2n-1,n)':>10} {'fallos = el mayor esta en D':>28}")
    for n in range(1, 8):
        peor_n = peor_o = fallos = total = 0
        solo_si_mayor_en_D = True
        for I, D in repartos(n):
            c = [0]
            m = mezclar(I, D, c)
            peor_n = max(peor_n, c[0])
            assert m == sorted(I + D)
            c = [0]
            salida = mezclar_optimizada(I, D, c)
            peor_o = max(peor_o, c[0])
            mal = salida != sorted(I + D)
            fallos += mal
            solo_si_mayor_en_D &= (mal == (I[-1] < D[-1]))
            total += 1
        print(f"{n:>2} {total:>9} {peor_n:>14} {2*n-1:>5} {peor_o:>11} {2*n-2:>5} "
              f"{fallos:>7} {math.comb(2*n-1, n):>10} {str(solo_si_mayor_en_D):>28}")
    print()


def exp_entrada_adversario():
    print("== La entrada del adversario ==")
    for n in (2, 4, 5):
        I, D = intercalada(n)
        c, reg = [0], []
        salida = mezclar_optimizada(I, D, c, reg)
        print(f"n = {n}: I = {I}, D = {D}")
        print(f"   comparaciones: {c[0]}  (la cota es {2*n-1})")
        print(f"   salida:   {salida}")
        print(f"   correcta: {sorted(I + D)}   ->  {'bien' if salida == sorted(I + D) else 'MAL'}")
    print()


def exp_intercambio():
    print("== Los pares de vecinos que no se comparan (n = 5) ==")
    n = 5
    I, D = intercalada(n)
    c, reg = [0], []
    salida = mezclar_optimizada(I, D, c, reg)
    comparados = {frozenset(par) for par in reg}
    cadena = sorted(I + D)
    vecinos = [(cadena[k], cadena[k + 1]) for k in range(2 * n - 1)]
    sin = [par for par in vecinos if frozenset(par) not in comparados]
    print(f"   pares de vecinos: {len(vecinos)}, comparados: {len(vecinos) - len(sin)}, sin comparar: {sin}")
    x, y = sin[0]
    cambio = {x: y, y: x}
    I2 = [cambio.get(v, v) for v in I]
    D2 = [cambio.get(v, v) for v in D]
    assert I2 == sorted(I2) and D2 == sorted(D2)
    c2, reg2 = [0], []
    salida2 = mezclar_optimizada(I2, D2, c2, reg2)
    mismas = [(a <= b) for a, b in reg] == [(a <= b) for a, b in reg2]
    print(f"   cambio los valores {x} y {y} entre las listas:")
    print(f"   I = {I2}, D = {D2}")
    print(f"   las {len(reg)} comparaciones dan las mismas respuestas: {mismas}")
    print(f"   salida original:  {salida}   (correcta: {sorted(I + D)})")
    print(f"   salida cambiada:  {salida2}   (correcta: {sorted(I2 + D2)})")
    print("   Misma respuesta a todas las preguntas, misma salida (en posiciones), pero las correctas"
          " son distintas: se equivoca en una.\n")


def exp_generadores():
    print("== Cuanto lo ven las pruebas al azar (4000 casos cada una) ==")

    def al_azar(n):
        v = random.sample(range(10 * n), 2 * n)
        return sorted(v[:n]), sorted(v[n:])

    def mayor_en_I(n):
        v = sorted(random.sample(range(10 * n), 2 * n))
        mayor, resto = v[-1], v[:-1]
        random.shuffle(resto)
        return sorted(resto[:n - 1] + [mayor]), sorted(resto[n - 1:])

    def mayor_en_D(n):
        v = sorted(random.sample(range(10 * n), 2 * n))
        mayor, resto = v[-1], v[:-1]
        random.shuffle(resto)
        return sorted(resto[:n]), sorted(resto[n:] + [mayor])

    gens = {"listas al azar": al_azar,
            "el mayor siempre en la primera lista": mayor_en_I,
            "el mayor siempre en la segunda lista": mayor_en_D,
            "intercalada (la del adversario)": lambda n: intercalada(n)}
    random.seed(9)
    print(f"{'generador':>40} {'la optimizada se equivoca':>26}")
    for nombre, g in gens.items():
        malos = 0
        for _ in range(4000):
            I, D = g(random.randint(1, 12))
            malos += mezclar_optimizada(I, D, [0]) != sorted(I + D)
        print(f"{nombre:>40} {100 * malos / 4000:>25.1f}%")
    print()


# --------------------------------------------------------------------------
# 3. Figuras: png y gif (necesita matplotlib y pillow)
# --------------------------------------------------------------------------
def figuras():
    import io
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    from PIL import Image

    # --- png: la cadena del adversario con los pares comparados y no comparados
    n = 5
    I, D = intercalada(n)
    c, reg = [0], []
    mezclar_optimizada(I, D, c, reg)
    comparados = {frozenset(p) for p in reg}
    fig, ax = plt.subplots(figsize=(9, 3.6))
    ax.set_xlim(-0.5, 2 * n + 0.2); ax.set_ylim(-0.9, 2.2); ax.axis("off")
    pos = {}
    for k in range(2 * n):
        v = k
        arriba = (v % 2 == 0)
        pos[v] = (k + 0.2, 1.4 if arriba else 0.2)
    for k in range(2 * n - 1):
        (x1, y1), (x2, y2) = pos[k], pos[k + 1]
        ok = frozenset((k, k + 1)) in comparados
        (xa, ya), (xb, yb) = ((x1, y1), (x2, y2)) if y1 > y2 else ((x2, y2), (x1, y1))
        ax.plot([xa + 0.3, xb + 0.3], [ya, yb + 0.5],          # del borde de abajo de la caja de arriba
                color="#2e8b57" if ok else "#d62728", lw=2.5, ls="-" if ok else "--", zorder=1)
    for v, (x, y) in pos.items():
        nombre = ("a" if v % 2 == 0 else "b") + str(v // 2 + 1)
        ax.add_patch(Rectangle((x, y), 0.6, 0.5, fc="#bdd7ee" if v % 2 == 0 else "#f8cbad", ec="#333", zorder=2))
        ax.text(x + 0.3, y + 0.25, nombre, ha="center", va="center", fontsize=11, zorder=3)
    ax.text(-0.4, 1.65, "lista I", fontsize=10); ax.text(-0.4, 0.45, "lista D", fontsize=10)
    ax.set_title(f"Entrada del adversario (n = {n}): la mezcla optimizada hace {c[0]} comparaciones;"
                 f" la cota es {2 * n - 1}", fontsize=10, loc="left")
    ax.text(0, -0.25, "verde: par de vecinos que sí se comparó   |   rojo punteado: par de vecinos que NO se comparó",
            fontsize=9, color="#444")
    ax.text(0, -0.65, "si queda un par de vecinos sin comparar, se pueden intercambiar sus valores sin cambiar ninguna respuesta",
            fontsize=9, color="#444")
    fig.tight_layout()
    fig.savefig("mezcla_adversario.png", dpi=110)
    plt.close(fig)

    # --- gif: la mezcla optimizada paso a paso sobre n = 4
    n = 4
    I, D = intercalada(n)
    correcta = sorted(I + D)
    pasos = [dict(i=0, j=0, R=[], comp=None, n_comp=0, texto="Empezamos: se compara mientras a I le queden 2 o más")]
    i = j = 0
    R, k = [], 0
    while len(I) - i > 1 and j < len(D):
        k += 1
        if I[i] <= D[j]:
            texto = f"{I[i]} <= {D[j]}: sale {I[i]} de I"
            comp = (i, j); R = R + [I[i]]; i += 1
        else:
            texto = f"{I[i]} > {D[j]}: sale {D[j]} de D"
            comp = (i, j); R = R + [D[j]]; j += 1
        pasos.append(dict(i=i, j=j, R=list(R), comp=comp, n_comp=k, texto=texto))
    final = R + D[j:] + I[i:]
    pasos.append(dict(i=i, j=j, R=list(R), comp=None, n_comp=k, final=final,
                      texto=f"A I le queda un solo elemento ({I[i]}): se pone al final sin comparar"))

    def dibujar(p):
        fig, ax = plt.subplots(figsize=(9, 3.8))
        ax.set_xlim(-1.3, 2 * n + 0.3); ax.set_ylim(-1.9, 3.2); ax.axis("off")
        ax.set_title(p["texto"], loc="left", fontsize=11, family="monospace")
        for fila, (nombre, lista, ptr) in enumerate([("I", I, p["i"]), ("D", D, p["j"])]):
            y = 2.2 - fila * 1.2
            ax.text(-1.1, y + 0.3, nombre, fontsize=14, weight="bold", va="center")
            for idx, v in enumerate(lista):
                gastado = idx < ptr
                activo = p["comp"] is not None and idx == (p["comp"][0] if nombre == "I" else p["comp"][1]) \
                    and False
                fc = "#e0e0e0" if gastado else "white"
                if idx == ptr and "final" not in p:
                    fc = "#f4b183"
                ax.add_patch(Rectangle((idx * 1.0 + 0.1, y), 0.8, 0.6, fc=fc, ec="#333"))
                ax.text(idx + 0.5, y + 0.3, str(v), ha="center", va="center", fontsize=13)
        ax.text(-1.1, 0.35, "salida", fontsize=11, weight="bold", va="center")
        salida = p.get("final", p["R"])
        for idx in range(2 * n):
            x = idx * 0.95 + 0.1
            if idx < len(salida):
                mal = "final" in p and salida[idx] != correcta[idx]
                fc = "#f4a6a6" if mal else "#bdd7ee"
                ax.add_patch(Rectangle((x, 0.05), 0.8, 0.6, fc=fc, ec="#333"))
                ax.text(x + 0.4, 0.35, str(salida[idx]), ha="center", va="center", fontsize=13)
            else:
                ax.add_patch(Rectangle((x, 0.05), 0.8, 0.6, fc="white", ec="#bbb", ls="--"))
        ax.text(0, -0.5, f"comparaciones hasta ahora: {p['n_comp']}   (la cota para mezclar es {2 * n - 1})",
                fontsize=11, family="monospace")
        if "final" in p:
            ax.text(0, -1.0, f"salida correcta: {correcta}", fontsize=11, family="monospace", color="#2e8b57")
            ax.text(0, -1.5, "en rojo: los que quedaron mal puestos (el 6 es menor que el 7)", fontsize=10, color="#b22222")
        else:
            ax.text(0, -1.0, "naranja: los dos que se comparan en el próximo paso", fontsize=9, color="#666")
        fig.tight_layout()
        buf = io.BytesIO(); fig.savefig(buf, format="png", dpi=90); plt.close(fig)
        buf.seek(0)
        return Image.open(buf).convert("P", palette=Image.ADAPTIVE)

    frames = [dibujar(p) for p in pasos]
    frames[0].save("mezcla_animacion.gif", save_all=True, append_images=frames[1:],
                   duration=1800, loop=0)
    print("figuras escritas: mezcla_adversario.png, mezcla_animacion.gif")


def figuras_adversario():
    """Segunda animacion: la cadena del adversario, las comparaciones que se hacen
    y el intercambio de los dos vecinos que quedaron sin comparar (n = 5)."""
    import io
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    from PIL import Image

    n = 5
    I, D = intercalada(n)
    c, reg = [0], []
    salida = mezclar_optimizada(I, D, c, reg)
    comparados = [frozenset(par) for par in reg]
    todos = {frozenset((k, k + 1)) for k in range(2 * n - 1)}
    sin = sorted((tuple(sorted(par)) for par in todos - set(comparados)))
    x, y = sin[0]                                   # los dos vecinos que se intercambian
    I2 = [y if v == x else x if v == y else v for v in I]
    D2 = [y if v == x else x if v == y else v for v in D]
    salida2 = mezclar_optimizada(I2, D2, [0])
    correcta = sorted(I + D)

    def nombre(k):
        return ("a" if k % 2 == 0 else "b") + str(k // 2 + 1)

    def dibujar(titulo, verdes, rojos, valores, lineas=()):
        fig, ax = plt.subplots(figsize=(9, 4.2))
        ax.set_xlim(-0.6, 2 * n + 0.2); ax.set_ylim(-1.9, 2.4); ax.axis("off")
        ax.set_title(titulo, loc="left", fontsize=10, family="monospace")
        pos = {k: (k + 0.1, 1.4 if k % 2 == 0 else 0.3) for k in range(2 * n)}
        for k in range(2 * n - 1):
            par = frozenset((k, k + 1))
            if par in verdes or par in rojos:
                (xa, ya), (xb, yb) = (pos[k], pos[k + 1]) if k % 2 == 0 else (pos[k + 1], pos[k])
                ax.plot([xa + 0.4, xb + 0.4], [ya, yb + 0.6], zorder=1, lw=3,
                        color="#2e8b57" if par in verdes else "#d62728",
                        ls="-" if par in verdes else "--")
        for k, (px, py) in pos.items():
            cambiado = valores[k] != k
            ax.add_patch(Rectangle((px, py), 0.8, 0.6, zorder=2, ec="#333", lw=2.5 if cambiado else 1,
                                   fc="#ffe699" if cambiado else ("#bdd7ee" if k % 2 == 0 else "#f8cbad")))
            ax.text(px + 0.4, py + 0.3, str(valores[k]), ha="center", va="center", fontsize=13, zorder=3)
            ax.text(px + 0.4, py + (0.75 if k % 2 == 0 else -0.2), nombre(k), ha="center", fontsize=8, color="#666")
        ax.text(-0.5, 1.7, "I", fontsize=13, weight="bold"); ax.text(-0.5, 0.6, "D", fontsize=13, weight="bold")
        for t, linea in enumerate(lineas):
            ax.text(0, -0.7 - 0.45 * t, linea, fontsize=9, family="monospace")
        fig.tight_layout()
        buf = io.BytesIO(); fig.savefig(buf, format="png", dpi=90); plt.close(fig)
        buf.seek(0)
        return Image.open(buf).convert("P", palette=Image.ADAPTIVE)

    ident = list(range(2 * n))
    cuadros = [dibujar(f"Entrada del adversario, n = {n}: hay {2 * n - 1} pares de vecinos",
                       set(), set(), ident,
                       ["todavia no se ha hecho ninguna comparacion"])]
    verdes = set()
    for t, (a, b) in enumerate(reg, start=1):
        verdes.add(frozenset((a, b)))
        signo = "<=" if a <= b else ">"
        cuadros.append(dibujar(f"comparacion {t}: {a} {signo} {b}  (respuesta: {a <= b})",
                               set(verdes), set(), ident,
                               [f"comparaciones hechas: {t}   |   cota para mezclar: {2 * n - 1}"]))
    rojos = {frozenset(par) for par in sin}
    cuadros.append(dibujar(f"A I le queda un solo elemento ({I[-1]}): para. Quedaron {len(sin)} pares sin comparar",
                           set(verdes), rojos, ident,
                           [f"comparaciones hechas: {c[0]}  <  {2 * n - 1}", "rojo punteado: pares de vecinos sin comparar"]))
    val2 = list(ident)
    val2[x], val2[y] = y, x
    cuadros.append(dibujar(f"Intercambio los valores {x} y {y} (vecinos sin comparar): las listas siguen ordenadas",
                           set(verdes), rojos, val2,
                           [f"I = {I2}", f"D = {D2}"]))
    cuadros.append(dibujar("Las comparaciones hechas dan las mismas respuestas: el algoritmo hace lo mismo",
                           set(verdes), rojos, val2,
                           [f"salida con la entrada original:    {salida}",
                            f"salida con la entrada cambiada:    {salida2}",
                            f"correcta (original):  {correcta}",
                            f"correcta (cambiada):  {sorted(I2 + D2)}"]))
    cuadros[0].save("mezcla_adversario_animacion.gif", save_all=True, append_images=cuadros[1:],
                    duration=1500, loop=0)
    print("figura escrita: mezcla_adversario_animacion.gif")


if __name__ == "__main__":
    exp_peor_caso()
    exp_entrada_adversario()
    exp_intercambio()
    exp_generadores()
    if "--figuras" in sys.argv:
        figuras()
        figuras_adversario()
