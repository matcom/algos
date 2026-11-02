"""
Tema 1, ejercicio 12: emparejamiento estable con listas incompletas.

Cada proponente (y cada receptor) lista solo a algunos del otro lado, y
prefiere quedarse solo antes que con alguien que no listo. Se adaptan:
  * el algoritmo (aceptacion diferida)
  * el potencial (para la terminacion)
  * la definicion de pareja bloqueante
y se comprueba que el resultado sigue siendo estable.
Uso:  python ejercicio12_listas_incompletas.py
"""
import itertools
import random
from collections import deque
from pathlib import Path

INF = float("inf")


# ----------------------------------------------------------------------------
# El algoritmo adaptado
#   pref_a[a] = receptores que lista el proponente a, de mas a menos preferido
#   pref_b[b] = proponentes que lista el receptor b, de mas a menos preferido
#   M[a] = receptor de a, o None si se queda solo
# ----------------------------------------------------------------------------
def gale_shapley_incompleto(pref_a, pref_b, orden="cola", semilla=0, traza=None,
                            vigilado=False, _retirar=True, _verificar=True):
    """Los dos ultimos parametros existen solo para mostrar errores de
    adaptacion (seccion de experimentos); en el algoritmo correcto no se tocan."""
    na, nb = len(pref_a), len(pref_b)
    rango = [{a: lugar for lugar, a in enumerate(pref_b[b])} for b in range(nb)]
    siguiente = [0] * na                       # a quien le propone a continuacion
    pareja_de_b = [None] * nb
    if _retirar:                               # libres CON alguien que probar
        libres = deque(a for a in range(na) if pref_a[a])
    else:
        libres = deque(range(na))
    azar = random.Random(semilla)
    L = sum(len(l) for l in pref_a)            # propuestas posibles en total
    propuestas = 0
    mejor_rango = [INF] * nb                   # para vigilar el invariante

    while libres:
        if vigilado:
            phi = sum(len(pref_a[x]) - siguiente[x] for x in range(na))
            assert phi == L - propuestas and phi >= 1          # POTENCIAL
            assert all(siguiente[x] < len(pref_a[x]) and x not in pareja_de_b
                       for x in libres)                       # los libres tienen opciones
        if orden == "azar":
            libres.rotate(azar.randrange(len(libres)))
        a = libres.popleft() if orden == "cola" else libres.pop()
        b = pref_a[a][siguiente[a]]
        siguiente[a] += 1
        propuestas += 1
        actual = pareja_de_b[b]
        if _verificar and a not in rango[b]:
            motivo, rechazado = "no lista", a                 # b no lista a a
        elif actual is None:
            pareja_de_b[b], motivo, rechazado = a, "acepta", None
        elif rango[b].get(a, INF) < rango[b][actual]:
            pareja_de_b[b], motivo, rechazado = a, "cambia", actual
        else:
            motivo, rechazado = "rechaza", a
        if rechazado is not None and (siguiente[rechazado] < len(pref_a[rechazado])
                                      or not _retirar):
            libres.append(rechazado)           # si no le quedan opciones, se queda solo
        if vigilado and pareja_de_b[b] is not None:
            r = rango[b].get(pareja_de_b[b], INF)
            assert r <= mejor_rango[b]         # la pareja de b solo mejora (y nunca queda sola)
            mejor_rango[b] = r
        if traza is not None:
            traza.append((a, b, actual, motivo))
    if vigilado:
        assert propuestas <= L
    M = [None] * na
    for b, a in enumerate(pareja_de_b):
        if a is not None:
            M[a] = b
    return M, propuestas


# ----------------------------------------------------------------------------
# Definiciones: emparejamiento valido y pareja bloqueante
# ----------------------------------------------------------------------------
def es_valido(M, pref_a, pref_b):
    """Cada receptor a lo sumo una vez, y solo pares donde se listan mutuamente."""
    usados = set()
    for a, b in enumerate(M):
        if b is None:
            continue
        if b not in pref_a[a] or a not in pref_b[b] or b in usados:
            return False
        usados.add(b)
    return True


def pares_bloqueantes(M, pref_a, pref_b):
    """(a, b) bloquea si se listan mutuamente, no estan juntos, a prefiere b a
    su pareja (o esta solo) y b prefiere a a su pareja (o esta sola)."""
    pareja_de_b = {b: a for a, b in enumerate(M) if b is not None}
    res = []
    for a in range(len(pref_a)):
        for b in pref_a[a]:
            if b == M[a] or a not in pref_b[b]:
                continue
            a_prefiere = M[a] is None or pref_a[a].index(b) < pref_a[a].index(M[a])
            b_prefiere = (b not in pareja_de_b
                          or pref_b[b].index(a) < pref_b[b].index(pareja_de_b[b]))
            if a_prefiere and b_prefiere:
                res.append((a, b))
    return res


def pares_bloqueantes_ingenuo(M, pref_a, pref_b):
    """Definicion mal adaptada: solo mira a los que YA tienen pareja."""
    pareja_de_b = {b: a for a, b in enumerate(M) if b is not None}
    return [(a, b) for (a, b) in pares_bloqueantes(M, pref_a, pref_b)
            if M[a] is not None and b in pareja_de_b]


def instancia_incompleta(n, rng, p):
    """Cada persona lista a cada persona del otro lado con probabilidad p."""
    def listas():
        return [rng.sample(range(n), sum(rng.random() < p for _ in range(n)))
                for _ in range(n)]
    return listas(), listas()


# ----------------------------------------------------------------------------
# Animacion (opcional, necesita Pillow)
# ----------------------------------------------------------------------------
def generar_gif(pref_a, pref_b, ruta):
    from PIL import Image, ImageDraw, ImageFont

    try:
        fuente = ImageFont.load_default(size=18)
        chica = ImageFont.load_default(size=14)
    except TypeError:
        fuente = chica = ImageFont.load_default()
    na, nb = len(pref_a), len(pref_b)
    traza = []
    M, total = gale_shapley_incompleto(pref_a, pref_b, traza=traza)
    L = sum(len(l) for l in pref_a)
    W, H, XA, XB, Y0, DY = 800, 440, 250, 550, 80, 70

    def etiqueta(letra, k):
        return f"{letra}{k + 1}"

    def lista_a(a):
        return " > ".join(etiqueta("b", b) for b in pref_a[a]) or "(vacia)"

    def lista_b(b):
        return " > ".join(etiqueta("a", a) for a in pref_b[b]) or "(vacia)"

    def cuadro(pareja_de_b, hechas, flecha, msg, final):
        im = Image.new("RGB", (W, H), "white")
        d = ImageDraw.Draw(im)
        d.text((15, 10), "proponentes (izquierda) y receptores (derecha), con sus listas",
               fill="black", font=chica)
        for b, a in enumerate(pareja_de_b):                      # lineas de parejas
            if a is not None:
                d.line([XA + 22, Y0 + a * DY, XB - 22, Y0 + b * DY],
                       fill="#1f6feb", width=4)
        if flecha:
            a, b, color = flecha
            d.line([XA + 22, Y0 + a * DY, XB - 22, Y0 + b * DY], fill=color, width=3)
            d.ellipse([XB - 30, Y0 + b * DY - 8, XB - 14, Y0 + b * DY + 8], fill=color)
        pareja_de_a = {a: b for b, a in enumerate(pareja_de_b) if a is not None}
        for a in range(na):
            solo_final = a not in pareja_de_a and hechas[a] == len(pref_a[a])
            fondo = "#a9d1f7" if a in pareja_de_a else ("#cccccc" if solo_final else "white")
            y = Y0 + a * DY
            d.ellipse([XA - 22, y - 22, XA + 22, y + 22], fill=fondo, outline="#222222", width=2)
            d.text((XA - 12, y - 9), etiqueta("a", a), fill="black", font=fuente)
            d.text((15, y - 8), lista_a(a), fill="#444444", font=chica)
            if solo_final:
                d.text((XA - 70, y + 24), "solo", fill="#888888", font=chica)
        pareja_b_set = {b for b, a in enumerate(pareja_de_b) if a is not None}
        for b in range(nb):
            fondo = "#a9d1f7" if b in pareja_b_set else "white"
            y = Y0 + b * DY
            d.ellipse([XB - 22, y - 22, XB + 22, y + 22], fill=fondo, outline="#222222", width=2)
            d.text((XB - 12, y - 9), etiqueta("b", b), fill="black", font=fuente)
            d.text((XB + 32, y - 8), lista_b(b), fill="#444444", font=chica)
            if b not in pareja_b_set and final:
                d.text((XB - 20, y + 24), "sola", fill="#888888", font=chica)
        d.text((15, H - 85), msg, fill="#b00020", font=chica)
        faltan = L - sum(hechas)
        d.text((15, H - 55), f"Phi = propuestas que faltan = {faltan}", fill="#444444", font=chica)
        return im

    frames = [cuadro([None] * nb, [0] * na, None, "inicio: nadie tiene pareja", False)]
    pareja_de_b, hechas = [None] * nb, [0] * na
    for k, (a, b, actual, motivo) in enumerate(traza, 1):
        hechas[a] += 1
        if motivo == "acepta":
            pareja_de_b[b] = a
            msg, color = f"{etiqueta('a', a)} propone a {etiqueta('b', b)}: estaba libre y lo lista, acepta", "#2e9e44"
        elif motivo == "cambia":
            pareja_de_b[b] = a
            msg, color = (f"{etiqueta('a', a)} propone a {etiqueta('b', b)}: {etiqueta('b', b)} "
                          f"prefiere {etiqueta('a', a)} a {etiqueta('a', actual)}, cambia"), "#2e9e44"
        elif motivo == "no lista":
            msg, color = f"{etiqueta('a', a)} propone a {etiqueta('b', b)}: {etiqueta('b', b)} no lista a {etiqueta('a', a)}, rechaza", "#d62828"
        else:
            msg, color = (f"{etiqueta('a', a)} propone a {etiqueta('b', b)}: {etiqueta('b', b)} "
                          f"prefiere a {etiqueta('a', actual)}, rechaza"), "#d62828"
        frames.append(cuadro(list(pareja_de_b), list(hechas), (a, b, color),
                             f"propuesta {k}: " + msg, False))
    frames.append(cuadro(list(pareja_de_b), list(hechas), None,
                         "fin: no queda ningun proponente libre con opciones. "
                         "Emparejamiento estable", True))
    frames += [frames[-1]]
    frames[0].save(ruta, save_all=True, append_images=frames[1:], duration=1500, loop=0)


# ----------------------------------------------------------------------------
# Ejemplo (indices desde 0: a1 = 0, b1 = 0, ...)
# ----------------------------------------------------------------------------
EJ_A = [[1, 0], [0, 1, 2], [0], [3]]     # a1: b2>b1  a2: b1>b2>b3  a3: b1  a4: b4
EJ_B = [[2, 0, 1], [0, 1], [1], [0]]     # b1: a3>a1>a2  b2: a1>a2  b3: a2  b4: a1


def nombre(M):
    return "  ".join(f"a{a + 1}-{'b' + str(b + 1) if b is not None else 'solo'}"
                     for a, b in enumerate(M))


# ----------------------------------------------------------------------------
# Experimentos
# ----------------------------------------------------------------------------
def traza_ejemplo():
    traza = []
    M, k = gale_shapley_incompleto(EJ_A, EJ_B, traza=traza, vigilado=True)
    print("Traza del ejemplo (estrategia de cola):")
    print(f"{'paso':>5} {'proponente':>11} {'receptor':>9} {'tenia':>6} {'resultado':>10}")
    for i, (a, b, actual, motivo) in enumerate(traza, 1):
        tenia = f"a{actual + 1}" if actual is not None else "-"
        print(f"{i:>5} {'a' + str(a + 1):>11} {'b' + str(b + 1):>9} {tenia:>6} {motivo:>10}")
    L = sum(len(l) for l in EJ_A)
    print(f"resultado: {nombre(M)}   propuestas = {k}, L = {L}")
    assert es_valido(M, EJ_A, EJ_B) and not pares_bloqueantes(M, EJ_A, EJ_B)


def exhaustivo_n2():
    """Todas las instancias con 2 + 2 personas: cada lista es un subconjunto ordenado."""
    listas = [list(t) for r in range(3) for t in itertools.permutations(range(2), r)]
    casos = 0
    for pa in itertools.product(listas, repeat=2):
        for pb in itertools.product(listas, repeat=2):
            pa_, pb_ = [list(x) for x in pa], [list(x) for x in pb]
            for orden in ("cola", "pila", "azar"):
                M, _ = gale_shapley_incompleto(pa_, pb_, orden=orden, vigilado=True)
                assert es_valido(M, pa_, pb_)
                assert not pares_bloqueantes(M, pa_, pb_)
                casos += 1
    print(f"n = 2: las {len(listas) ** 4} instancias posibles x 3 estrategias = "
          f"{casos} ejecuciones, todas validas y sin parejas bloqueantes")


def experimento_aleatorio():
    rng = random.Random(12)
    print(f"{'n':>4} {'instancias':>11} {'bloqueantes':>12} {'propuestas':>11} "
          f"{'L (total)':>11} {'proponentes solos':>18}")
    for n, veces in [(3, 600), (6, 400), (10, 200), (30, 40)]:
        bloq = props = Ls = solos = 0
        for _ in range(veces):
            p = rng.choice([0.3, 0.6, 1.0])
            pa, pb = instancia_incompleta(n, rng, p)
            for orden, semilla in [("cola", 0), ("pila", 0), ("azar", 1)]:
                M, k = gale_shapley_incompleto(pa, pb, orden=orden, semilla=semilla,
                                               vigilado=True)
                assert es_valido(M, pa, pb)
                bloq += len(pares_bloqueantes(M, pa, pb))
            props += k
            Ls += sum(len(l) for l in pa)
            solos += sum(1 for b in M if b is None)
        print(f"{n:>4} {veces:>11} {bloq:>12} {props / veces:>11.1f} "
              f"{Ls / veces:>11.1f} {solos / veces:>18.2f}")


def listas_completas_dan_perfecto():
    rng = random.Random(3)
    perfectos = 0
    for _ in range(300):
        pa, pb = instancia_incompleta(6, rng, 1.0)
        M, _ = gale_shapley_incompleto(pa, pb)
        perfectos += all(b is not None for b in M)
    print(f"con listas completas el emparejamiento es perfecto: {perfectos} de 300")


def errores_de_adaptacion():
    # 1) definicion de pareja bloqueante mal adaptada
    vacio = [None] * len(EJ_A)
    print("definicion de pareja bloqueante, con el emparejamiento vacio:")
    print("  ingenua (solo mira a los que tienen pareja):", pares_bloqueantes_ingenuo(vacio, EJ_A, EJ_B))
    print("  adaptada (los solos tambien cuentan):       ",
          [(f"a{a + 1}", f"b{b + 1}") for a, b in pares_bloqueantes(vacio, EJ_A, EJ_B)])
    rng = random.Random(9)
    con_pares = ingenuo_acepta = 0
    for _ in range(1000):
        pa, pb = instancia_incompleta(5, rng, 0.5)
        if any(a in pb[b] for a in range(5) for b in pa[a]):    # hay algun par aceptable
            con_pares += 1
            ingenuo_acepta += not pares_bloqueantes_ingenuo([None] * 5, pa, pb)
    print(f"  en {con_pares} instancias con algun par aceptable, la definicion ingenua "
          f"dio por 'estable' al emparejamiento vacio en {ingenuo_acepta}")
    # 2) no retirar al proponente al que se le acaba la lista
    try:
        gale_shapley_incompleto(EJ_A, EJ_B, _retirar=False)
        print("no retirar: no fallo")
    except IndexError:
        print("no retirar al que agota su lista: IndexError (el potencial se pasa de 0)")
    # 3) el receptor no rechaza a quien no lista
    M, _ = gale_shapley_incompleto(EJ_A, EJ_B, _verificar=False)
    print("receptor que acepta a quien no lista:", nombre(M),
          "| es valido:", es_valido(M, EJ_A, EJ_B))


def main():
    traza_ejemplo()
    print()
    exhaustivo_n2()
    print()
    experimento_aleatorio()
    print()
    listas_completas_dan_perfecto()
    print()
    errores_de_adaptacion()
    print()
    try:
        ruta = Path(__file__).with_name("listas_incompletas.gif")
        generar_gif(EJ_A, EJ_B, ruta)
        print("animacion guardada en", ruta.name)
    except ImportError:
        print("(sin Pillow: se omite la animacion)")


if __name__ == "__main__":
    main()
