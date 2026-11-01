import math
import random
from pathlib import Path
import matplotlib.pyplot as plt


def por_ordenamiento(xs):
    ys = sorted(xs)
    return min(b - a for a, b in zip(ys, ys[1:]))


def rejilla_1d(xs, barajar=True, semilla=2026, guardar_traza=False):
    """
    Algoritmo incremental con rejilla 1D para el par mas cercano en la recta.
    Devuelve (delta, num_reconstrucciones, ops_hash[, traza]).
    """
    pts = list(xs)
    if barajar:
        random.Random(semilla).shuffle(pts)

    delta = abs(pts[0] - pts[1])
    if delta == 0:
        if guardar_traza:
            return 0.0, 0, 2, []
        return 0.0, 0, 2

    rejilla = {math.floor(pts[0] / delta): pts[0], math.floor(pts[1] / delta): pts[1]}
    reconstrucciones = 0
    ops_hash = 2  # las dos inserciones iniciales
    traza = []

    if guardar_traza:
        traza.append((1, f"{pts[0]}, {pts[1]}", delta, "-", "inicializacion", dict(rejilla)))

    for i in range(2, len(pts)):
        p = pts[i]
        antes = delta
        c = math.floor(p / delta)
        vecinos_vistos = []

        for d in (-1, 0, 1):
            ops_hash += 1
            q = rejilla.get(c + d)
            if q is not None:
                vecinos_vistos.append(f"{c+d}:{q}")
                if abs(p - q) < delta:
                    delta = abs(p - q)

        if delta == 0:
            if guardar_traza:
                traza.append((i + 1, f"{p}", 0.0, f"{c-1}, {c}, {c+1}", "repetido (fin)", dict(rejilla)))
                return 0.0, reconstrucciones, ops_hash, traza
            return 0.0, reconstrucciones, ops_hash

        if delta < antes:
            rejilla = {math.floor(x / delta): x for x in pts[:i + 1]}
            reconstrucciones += 1
            ops_hash += (i + 1)
            evento = f"reconstruye (delta: {antes:g} -> {delta:g})"
        else:
            rejilla[c] = p
            ops_hash += 1
            evento = f"inserta en celda {c}"

        if guardar_traza:
            traza.append((i + 1, f"{p}", delta, f"{c-1}, {c}, {c+1}", evento, dict(rejilla)))

    if guardar_traza:
        return delta, reconstrucciones, ops_hash, traza
    return delta, reconstrucciones, ops_hash


if __name__ == "__main__":
    # 1. Traza detallada sobre una lista fija de 7 puntos (sin barajar extra para reproducir la tabla)
    ejemplo = [10.0, 2.0, 7.5, 4.0, 3.2, 9.1, 3.5]
    d_ej, rec_ej, ops_ej, traza_ej = rejilla_1d(ejemplo, barajar=False, guardar_traza=True)
    print("=== Traza paso a paso sobre 7 puntos ===")
    print(f"Puntos en orden de insercion: {ejemplo}")
    for paso, p_str, d_val, celdas_str, ev, rej in traza_ej:
        print(f"Paso {paso} (p={p_str:>8}): celdas=({celdas_str:>10}) | {ev:<32} | delta={d_val:g} | rejilla={rej}")
    print(f"Resultado: delta = {d_ej:g}, reconstrucciones = {rec_ej}, operaciones hash = {ops_ej}\n")

    # 2. Verificacion contra el algoritmo por ordenamiento en 3000 instancias aleatorias
    rng = random.Random(73)
    for _ in range(3000):
        n = rng.randint(2, 60)
        if rng.random() < 0.3:
            xs = [rng.randrange(4 * n) for _ in range(n)]
        else:
            xs = [rng.uniform(-100.0, 100.0) for _ in range(n)]
        d_rej, _, _ = rejilla_1d(xs, semilla=rng.randrange(10**6))
        d_ord = por_ordenamiento(xs)
        assert abs(d_rej - d_ord) < 1e-9
    print("Verificacion superada: 3000 instancias aleatorias (con y sin repetidos) coinciden con ordenamiento.\n")

    # 3. Experimento para distintos tamanos de entrada hasta n = 200,000
    tamanos = [200, 500, 1000, 2500, 5000, 10000, 25000, 50000, 100000, 200000]
    repeticiones = 12
    media_rec = []
    cota_armonica = []
    cota_log = []
    media_ops = []
    comparacion_nlogn = []

    print(f"{'n':>9} {'reconstrucciones (media)':>25} {'sum_{k=3}^n 2/k':>17} {'2 ln n':>10} {'ops_hash / n':>14}")
    # Precalculamos la suma armonica 2 * sum_{k=3}^n (1/k)
    armonica_acum = 0.0
    k_actual = 3
    for n in tamanos:
        while k_actual <= n:
            armonica_acum += 2.0 / k_actual
            k_actual += 1

        xs_base = [rng.random() for _ in range(n)]
        recs, ops = 0, 0
        for r in range(repeticiones):
            _, rec_i, ops_i = rejilla_1d(xs_base, semilla=500 + 31 * r)
            recs += rec_i
            ops += ops_i

        prom_r = recs / repeticiones
        prom_o = ops / repeticiones
        media_rec.append(prom_r)
        cota_armonica.append(armonica_acum)
        cota_log.append(2.0 * math.log(n))
        media_ops.append(prom_o)
        comparacion_nlogn.append(n * math.log2(n))

        print(f"{n:>9,} {prom_r:>25.2f} {armonica_acum:>17.2f} {2 * math.log(n):>10.2f} {prom_o / n:>14.2f}")

    # 4. Generacion de la grafica con 2 paneles
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.4))

    ax1.plot(tamanos, cota_log, ":", color="#888888", lw=1.6, label="Aproximacion 2 ln(n)")
    ax1.plot(tamanos, cota_armonica, "--", color="#d62728", lw=1.8, label="Suma armonica sum_{k=3..n} 2/k")
    ax1.plot(tamanos, media_rec, "o-", color="#1f77b4", lw=2, markersize=5, label="Reconstrucciones medidas (media)")
    ax1.set_xscale("log")
    ax1.set_title("Reconstrucciones de la rejilla vs n (escala log)")
    ax1.set_xlabel("Numero de puntos (n)")
    ax1.set_ylabel("Cantidad de reconstrucciones")
    ax1.grid(True, which="both", alpha=0.3)
    ax1.legend(fontsize=8.5)

    ax2.plot(tamanos, comparacion_nlogn, "s--", color="#d62728", lw=1.8, markersize=4,
             label="Referencia ordenamiento: n log2(n)")
    ax2.plot(tamanos, media_ops, "o-", color="#2ca02c", lw=2, markersize=5,
             label="Operaciones en tabla hash (~ 5.8n)")
    ax2.set_title("Trabajo total en la tabla hash vs n log2(n)")
    ax2.set_xlabel("Numero de puntos (n)")
    ax2.set_ylabel("Operaciones (consultas + inserciones)")
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=8.5)

    plt.tight_layout()
    salida_png = Path(__file__).with_name("ejercicio-10.png")
    plt.savefig(salida_png, dpi=150)
    print(f"\nGrafica guardada en {salida_png.name}")
