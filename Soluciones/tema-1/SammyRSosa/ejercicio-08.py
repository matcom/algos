import random
from collections import Counter
from pathlib import Path
import matplotlib.pyplot as plt


def primera_pasada(A, vigilar=False, guardar_traza=False):
    """
    Primera pasada de Boyer-Moore generalizada a 2 candidatos (umbral > n/3).
    Si guardar_traza=True, registra en cada paso los candidatos y los trios cancelados.
    """
    c1, k1, c2, k2 = None, 0, None, 0
    trios = []
    traza = []

    for i, x in enumerate(A):
        accion = ""
        if k1 > 0 and x == c1:
            k1 += 1
            accion = f"suma a c1 ({c1})"
        elif k2 > 0 and x == c2:
            k2 += 1
            accion = f"suma a c2 ({c2})"
        elif k1 == 0:
            c1, k1 = x, 1
            accion = f"ocupa c1 libre ({x})"
        elif k2 == 0:
            c2, k2 = x, 1
            accion = f"ocupa c2 libre ({x})"
        else:
            trios.append((c1, c2, x))
            k1 -= 1
            k2 -= 1
            accion = f"forma trio ({c1},{c2},{x})"

        if vigilar:
            verificar_invariante(A[: i + 1], c1, k1, c2, k2, trios)
        if guardar_traza:
            cand1 = f"({c1}, {k1})" if k1 > 0 else "(-, 0)"
            cand2 = f"({c2}, {k2})" if k2 > 0 else "(-, 0)"
            traza.append((i + 1, x, cand1, cand2, list(trios), accion))

    vivos = [(c, k) for c, k in ((c1, k1), (c2, k2)) if k > 0]
    return (vivos, traza) if guardar_traza else vivos


def se_parte_en_trios_distintos(multiconjunto):
    """
    Comprueba si un multiconjunto puede particionarse en trios de elementos
    distintos dos a dos: su cardinal debe ser multiplo de 3 y ningun elemento
    puede aparecer mas de |S|/3 veces.
    """
    m = len(multiconjunto)
    return m % 3 == 0 and all(3 * cuenta <= m for cuenta in Counter(multiconjunto).values())


def verificar_invariante(prefijo, c1, k1, c2, k2, trios):
    if k1 > 0 and k2 > 0:
        assert c1 != c2
    # Verificar que cada trio registrado tiene 3 elementos distintos
    for t in trios:
        assert len(set(t)) == 3
    # Verificar que el prefijo completo es exactamente la union de los trios + copias vivas
    reconstruido = Counter()
    for a, b, c in trios:
        reconstruido[a] += 1
        reconstruido[b] += 1
        reconstruido[c] += 1
    if k1 > 0:
        reconstruido[c1] += k1
    if k2 > 0:
        reconstruido[c2] += k2
    assert reconstruido == Counter(prefijo)

    # Ademas, comprobar la condicion de Hall/mayoria sobre el resto sin candidatos
    resto = Counter(prefijo)
    if k1 > 0:
        resto[c1] -= k1
    if k2 > 0:
        resto[c2] -= k2
    assert se_parte_en_trios_distintos(list(resto.elements()))


def mas_de_un_tercio(A):
    """Algoritmo completo en dos pasadas: filtra los candidatos que superan n/3."""
    return sorted(c for c, _ in primera_pasada(A) if 3 * A.count(c) > len(A))


def candidatos_sin_verificar(A):
    """Version incompleta que devuelve directamente los candidatos con contador > 0."""
    return sorted(c for c, _ in primera_pasada(A))


def oraculo(A):
    return sorted(x for x, cuenta in Counter(A).items() if 3 * cuenta > len(A))


def generar_con_plantados(n, cuantos_plantados, alfabeto, rng):
    """Planta `cuantos_plantados` elementos distintos con floor(n/3) + 1 copias cada uno."""
    elegidos = rng.sample(alfabeto, cuantos_plantados)
    arreglo = []
    for elem in elegidos:
        arreglo.extend([elem] * (n // 3 + 1))
    arreglo.extend(rng.choice(alfabeto) for _ in range(n - len(arreglo)))
    rng.shuffle(arreglo)
    return arreglo


if __name__ == "__main__":
    # 1. Traza paso a paso sobre un ejemplo concreto de largo 9
    ejemplo = list("ABCAADBAC")
    vivos_ej, traza_ej = primera_pasada(ejemplo, vigilar=True, guardar_traza=True)
    print(f"=== Traza paso a paso sobre A = {' '.join(ejemplo)} (n = {len(ejemplo)}, umbral > {len(ejemplo)//3}) ===")
    print(f"{'Paso':>4} | {'x':>2} | {'Cand 1':>8} | {'Cand 2':>8} | {'Accion':>22} | {'Trios cancelados acumulados'}")
    print("-" * 88)
    for paso, x, c1_s, c2_s, t_acum, acc in traza_ej:
        t_str = ", ".join("{" + f"{a},{b},{c}" + "}" for a, b, c in t_acum) if t_acum else "ninguno"
        print(f"{paso:>4} | {x:>2} | {c1_s:>8} | {c2_s:>8} | {acc:>22} | {t_str}")
    print(f"Candidatos al final de la 1ra pasada: {vivos_ej}")
    print(f"Salida del atajo: {candidatos_sin_verificar(ejemplo)} | Salida tras 2da pasada: {mas_de_un_tercio(ejemplo)}\n")

    # 2. Verificacion del invariante en miles de prefijos aleatorios
    rng = random.Random(308)
    total_prefijos = 0
    for _ in range(3000):
        largo = rng.randint(1, 15)
        arr = [rng.choice("ABCD") for _ in range(largo)]
        primera_pasada(arr, vigilar=True)
        total_prefijos += largo
    print(f"Invariante verificado constructivamente en {total_prefijos} prefijos: 0 fallos.")

    # Contraejemplo minimo de 4 elementos para el atajo
    contra = list("AAB")
    print(f"Contraejemplo minimo 'A A B' -> atajo: {candidatos_sin_verificar(contra)}, oraculo: {oraculo(contra)}")
    contra = list("ABCD")
    print(f"Otro contraejemplo 'A B C D' -> atajo: {candidatos_sin_verificar(contra)}, oraculo: {oraculo(contra)}")

    # 3. Comparacion de generadores de prueba frente al atajo y al algoritmo de 2 pasadas
    alf_5 = list("ABCDE")
    generadores = {
        "Binario (|Sigma|=2)": lambda n: [rng.choice("AB") for _ in range(n)],
        "Ternario (|Sigma|=3)": lambda n: [rng.choice("ABC") for _ in range(n)],
        "Uniforme (|Sigma|=5)": lambda n: [rng.choice(alf_5) for _ in range(n)],
        "1 plantado (> n/3)": lambda n: generar_con_plantados(n, 1, alf_5, rng),
        "2 plantados (> n/3)": lambda n: generar_con_plantados(n, 2, alf_5, rng),
    }

    tasas_atajo = {}
    print(f"\n{'Generador':>22} | {'Fallo atajo':>12} | {'Fallo 2 pasadas':>15}")
    print("-" * 56)
    for nombre, gen in generadores.items():
        muestras = [gen(rng.randint(4, 16)) for _ in range(4000)]
        fallo_a = 100.0 * sum(candidatos_sin_verificar(A) != oraculo(A) for A in muestras) / len(muestras)
        fallo_2 = 100.0 * sum(mas_de_un_tercio(A) != oraculo(A) for A in muestras) / len(muestras)
        assert fallo_2 == 0.0
        tasas_atajo[nombre] = fallo_a
        print(f"{nombre:>22} | {fallo_a:>11.1f}% | {fallo_2:>14.1f}%")

    # 4. Generacion de la figura con 2 paneles
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.6))

    # Panel 1: grafico de barras del porcentaje de fallos del atajo segun el generador
    nombres_g = list(tasas_atajo.keys())
    valores_g = [tasas_atajo[k] for k in nombres_g]
    colores_b = ["#1f77b4", "#1f77b4", "#1f77b4", "#ff7f0e", "#2ca02c"]

    barras = ax1.barh(nombres_g, valores_g, color=colores_b, alpha=0.85, edgecolor="#333333")
    for b, val in zip(barras, valores_g):
        ax1.text(val + 1.2, b.get_y() + b.get_height() / 2, f"{val:.1f}%",
                 va="center", ha="left", fontsize=9, fontweight="bold")

    ax1.set_xlim(0, max(valores_g) + 14)
    ax1.set_title("Tasa de fallo del atajo segun el generador (4 <= n <= 16)")
    ax1.set_xlabel("Entradas donde el atajo se equivoca (%)")
    ax1.grid(True, axis="x", alpha=0.3)

    # Panel 2: curva de tasa de fallo del atajo en arreglos uniformes variando |Sigma| in [2..15] y n
    tamanos_sigma = list(range(2, 16))
    largos_n = [6, 12, 24]
    estilos = [("o-", "#d62728"), ("s-", "#1f77b4"), ("^-", "#2ca02c")]

    for (n_fijo, (estilo, col)) in zip(largos_n, estilos):
        curva = []
        for s in tamanos_sigma:
            alf = list(range(s))
            rep = 1200
            fallos = 0
            for _ in range(rep):
                arr = [rng.choice(alf) for _ in range(n_fijo)]
                if candidatos_sin_verificar(arr) != oraculo(arr):
                    fallos += 1
            curva.append(100.0 * fallos / rep)
        ax2.plot(tamanos_sigma, curva, estilo, color=col, lw=1.9, markersize=4.5,
                 label=f"Uniforme con n = {n_fijo}")

    ax2.set_title("Fallo del atajo al variar el alfabeto |Sigma| y el largo n")
    ax2.set_xlabel("Tamano del alfabeto |Sigma|")
    ax2.set_ylabel("Porcentaje de fallo del atajo (%)")
    ax2.set_xticks(tamanos_sigma)
    ax2.set_ylim(0, 105)
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=8.5, loc="lower right")

    plt.tight_layout()
    salida_png = Path(__file__).with_name("ejercicio-08.png")
    plt.savefig(salida_png, dpi=150)
    print(f"\nGrafica guardada en {salida_png.name}")
