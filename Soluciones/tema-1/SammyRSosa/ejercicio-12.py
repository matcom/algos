import random
import time
from collections import deque
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def gale_shapley_incompleto(pref_a, pref_b, orden="cola", semilla=42, guardar_traza=False):
    """
    Gale-Shapley adaptado a listas incompletas.
    pref_a[a]: lista ordenada de receptores aceptables para el proponente a.
    pref_b[b]: lista ordenada de proponentes aceptables para el receptor b.
    """
    na, nb = len(pref_a), len(pref_b)
    rango = [{a: pos for pos, a in enumerate(pref_b[b])} for b in range(nb)]

    sig = [0] * na
    pareja_b = [None] * nb
    libres = deque(a for a in range(na) if len(pref_a[a]) > 0)
    rng = random.Random(semilla)

    phi = sum(len(lista) for lista in pref_a)
    propuestas = 0
    traza = []

    while libres:
        if orden == "azar":
            libres.rotate(rng.randrange(len(libres)))
        a = libres.popleft() if orden == "cola" else libres.pop()

        b = pref_a[a][sig[a]]
        sig[a] += 1
        propuestas += 1
        phi -= 1

        actual = pareja_b[b]
        if a not in rango[b]:
            rechazado = a
            tipo = "inaceptable"
            evento = f"b{b} rechaza a a{a} (no esta en L(b))"
        elif actual is None:
            pareja_b[b] = a
            rechazado = None
            tipo = "acepta"
            evento = f"b{b} libre acepta a a{a}"
        elif rango[b][a] < rango[b][actual]:
            pareja_b[b] = a
            rechazado = actual
            tipo = "cambia"
            evento = f"b{b} cambia a a{actual} por a{a}"
        else:
            rechazado = a
            tipo = "rechaza"
            evento = f"b{b} prefiere a a{actual} y rechaza a a{a}"

        if rechazado is not None and sig[rechazado] < len(pref_a[rechazado]):
            libres.append(rechazado)

        if guardar_traza:
            traza.append({
                "paso": propuestas,
                "a": a,
                "b": b,
                "antes": actual,
                "despues": pareja_b[b],
                "pareja_b": list(pareja_b),
                "sig": list(sig),
                "libres": list(libres),
                "phi": phi,
                "tipo": tipo,
                "evento": evento,
            })

    pareja_a = [None] * na
    for b, a in enumerate(pareja_b):
        if a is not None:
            pareja_a[a] = b

    if guardar_traza:
        return pareja_a, propuestas, traza
    return pareja_a, propuestas


def prefiere(lista, candidato, actual):
    if candidato not in lista:
        return False
    if actual is None:
        return True
    return lista.index(candidato) < lista.index(actual)


def buscar_bloqueantes(M, pref_a, pref_b):
    pareja_b = {b: a for a, b in enumerate(M) if b is not None}
    bloqueantes = []
    for a in range(len(pref_a)):
        for b in range(len(pref_b)):
            if M[a] != b:
                if prefiere(pref_a[a], b, M[a]) and prefiere(pref_b[b], a, pareja_b.get(b)):
                    bloqueantes.append((a, b))
    return bloqueantes


def es_aceptable(M, pref_a, pref_b):
    for a, b in enumerate(M):
        if b is not None and (b not in pref_a[a] or a not in pref_b[b]):
            return False
    return True


def generar_instancia(na, nb, rng, p_a=0.6, p_b=1.0):
    pref_a = [[b for b in rng.sample(range(nb), nb) if rng.random() < p_a] for _ in range(na)]
    pref_b = [[a for a in rng.sample(range(na), na) if rng.random() < p_b] for _ in range(nb)]
    return pref_a, pref_b


def emparejamientos_parciales(na, nb):
    def backtrack(a, usados):
        if a == na:
            yield []
            return
        for resto in backtrack(a + 1, usados):
            yield [None] + resto
        for b in range(nb):
            if b not in usados:
                for resto in backtrack(a + 1, usados | {b}):
                    yield [b] + resto
    return backtrack(0, frozenset())


def crear_gif_animado(ej_a, ej_b, traza, M_final, ruta_gif):
    na, nb = len(ej_a), len(ej_b)
    phi_ini = sum(len(l) for l in ej_a)

    fig, (ax_grafo, ax_phi) = plt.subplots(
        1, 2, figsize=(10.5, 4.6), gridspec_kw={"width_ratios": [1.5, 1.0]}
    )

    frames = [None] + traza + ["FIN"]

    def dibujar(idx):
        ax_grafo.clear()
        ax_phi.clear()

        y_a = [na - 1 - i for i in range(na)]
        y_b = [nb - 1 - j for j in range(nb)]

        # Dibujar aristas aceptables de fondo en gris muy suave
        for a in range(na):
            for b in ej_a[a]:
                if a in ej_b[b]:
                    ax_grafo.plot([0, 1], [y_a[a], y_b[b]], color="#dddddd", lw=1.0, zorder=1)

        estado = frames[idx]
        if estado is None:
            pareja_b = [None] * nb
            sig = [0] * na
            libres = [a for a in range(na) if ej_a[a]]
            titulo = f"Estado inicial: Potencial Phi = {phi_ini}"
            paso_actual = 0
        elif estado == "FIN":
            pareja_b = [None] * nb
            for a, b in enumerate(M_final):
                if b is not None:
                    pareja_b[b] = a
            sig = traza[-1]["sig"]
            libres = []
            titulo = f"Fin: emparejamiento estable en {len(traza)} propuestas (Phi = {traza[-1]['phi']})"
            paso_actual = len(traza)
        else:
            pareja_b = estado["pareja_b"]
            sig = estado["sig"]
            libres = estado["libres"]
            titulo = f"Paso {estado['paso']}: {estado['evento']}"
            paso_actual = estado["paso"]

        # Dibujar emparejamiento actual en azul solido
        for b, a in enumerate(pareja_b):
            if a is not None:
                ax_grafo.plot([0, 1], [y_a[a], y_b[b]], color="#1f77b4", lw=3.2, zorder=3)

        # Si estamos en un paso intermedio, resaltar la propuesta actual
        if isinstance(estado, dict):
            a_act, b_act = estado["a"], estado["b"]
            color_prop = "#2ca02c" if estado["tipo"] in ("acepta", "cambia") else "#d62728"
            estilo_prop = "-" if estado["tipo"] in ("acepta", "cambia") else "--"
            ax_grafo.plot(
                [0, 1], [y_a[a_act], y_b[b_act]],
                color=color_prop, linestyle=estilo_prop, lw=2.8, zorder=4
            )

        # Nodos proponentes
        emparejados_a = {a for a in pareja_b if a is not None}
        for a in range(na):
            if a in emparejados_a:
                c_nodo = "#1f77b4"
                estado_txt = "emparejado"
            elif a in libres:
                c_nodo = "#ff7f0e"
                estado_txt = f"libre ({sig[a]}/{len(ej_a[a])})"
            else:
                c_nodo = "#888888"
                estado_txt = "SOLO (agoto lista)"
            ax_grafo.scatter([0], [y_a[a]], s=360, color=c_nodo, zorder=5, edgecolors="black")
            ax_grafo.text(0, y_a[a], f"a{a}", color="white", ha="center", va="center", fontweight="bold", zorder=6)
            lista_str = ",".join(f"b{b}" for b in ej_a[a])
            ax_grafo.text(-0.08, y_a[a], f"L=[{lista_str}]\n({estado_txt})", ha="right", va="center", fontsize=8.5)

        # Nodos receptores
        for b in range(nb):
            c_nodo = "#1f77b4" if pareja_b[b] is not None else "#aaaaaa"
            ax_grafo.scatter([1], [y_b[b]], s=360, color=c_nodo, zorder=5, edgecolors="black")
            ax_grafo.text(1, y_b[b], f"b{b}", color="white", ha="center", va="center", fontweight="bold", zorder=6)
            lista_str = ",".join(f"a{a}" for a in ej_b[b])
            ax_grafo.text(1.08, y_b[b], f"L=[{lista_str}]", ha="left", va="center", fontsize=8.5)

        ax_grafo.set_xlim(-0.55, 1.55)
        ax_grafo.set_ylim(-0.6, max(na, nb) - 0.3)
        ax_grafo.axis("off")
        ax_grafo.set_title(titulo, fontsize=10.5, fontweight="bold")

        # Panel derecho: evolucion del potencial Phi paso a paso
        xs = list(range(paso_actual + 1))
        ys = [phi_ini - k for k in xs]
        ax_phi.plot(range(len(traza) + 1), [phi_ini - k for k in range(len(traza) + 1)],
                    "--", color="#cccccc", lw=1.5, label="Trayectoria completa")
        ax_phi.plot(xs, ys, "o-", color="#2ca02c", lw=2.5, markersize=6, label="Potencial Phi(k)")
        ax_phi.set_xlim(-0.3, len(traza) + 0.5)
        ax_phi.set_ylim(0, phi_ini + 1)
        ax_phi.set_xlabel("Propuestas realizadas (k)")
        ax_phi.set_ylabel("Potencial Phi = sum(|L(a)| - sig[a])")
        ax_phi.set_title("Caida estricta del potencial Phi", fontsize=10.5)
        ax_phi.grid(True, alpha=0.3)
        ax_phi.legend(loc="upper right", fontsize=8.5)

        plt.tight_layout()

    ani = animation.FuncAnimation(fig, dibujar, frames=len(frames), interval=1100, repeat=True)
    ani.save(ruta_gif, writer=animation.PillowWriter(fps=1))
    plt.close(fig)


if __name__ == "__main__":
    # 1. Ejemplo pequeno paso a paso (4x4)
    ej_a = [
        [0, 1],       # a0 solo acepta a b0, b1
        [0, 2, 1],    # a1 acepta a b0, b2, b1
        [1, 0],       # a2 solo acepta a b1, b0
        [0],          # a3 solo acepta a b0
    ]
    ej_b = [
        [1, 0, 2, 3],
        [2, 0, 1, 3],
        [1, 0, 2, 3],
        [0, 1, 2, 3],
    ]
    M_ej, prop_ej, traza_ej = gale_shapley_incompleto(ej_a, ej_b, guardar_traza=True)
    print("=== Traza del ejemplo 4x4 ===")
    print(f"Potencial inicial Lambda = {sum(len(x) for x in ej_a)}")
    for reg in traza_ej:
        print(f"Paso {reg['paso']}: a{reg['a']} -> b{reg['b']} | {reg['evento']} | Phi = {reg['phi']}")
    print("Emparejamiento final:", {f"a{a}": (f"b{b}" if b is not None else "solo") for a, b in enumerate(M_ej)})
    print("Parejas bloqueantes:", buscar_bloqueantes(M_ej, ej_a, ej_b))
    print()

    # Guardar animacion GIF del ejemplo 4x4
    ruta_gif = Path(__file__).with_name("ejercicio-12-anim.gif")
    crear_gif_animado(ej_a, ej_b, traza_ej, M_ej, ruta_gif)
    print(f"Animacion paso a paso guardada en {ruta_gif.name}")

    # 2. Verificacion exhaustiva en instancias aleatorias
    rng = random.Random(2026)
    casos = 2000
    for _ in range(casos):
        na, nb = rng.randint(2, 8), rng.randint(2, 8)
        pa, pb = generar_instancia(na, nb, rng, p_a=0.55, p_b=0.75)
        salidas = []
        for modo in ("cola", "pila", "azar"):
            M, k = gale_shapley_incompleto(pa, pb, orden=modo, semilla=99)
            assert es_aceptable(M, pa, pb)
            assert len(buscar_bloqueantes(M, pa, pb)) == 0
            assert k <= sum(len(l) for l in pa)
            salidas.append(M)
        assert salidas[0] == salidas[1] == salidas[2]
    print(f"Verificadas {casos} instancias aleatorias (listas incompletas en uno y ambos lados): 0 fallos.")

    # 3. Verificacion de optimalidad y Teorema de los Hospitales Rurales en 4x4
    for _ in range(200):
        pa, pb = generar_instancia(4, 4, rng, p_a=0.6, p_b=0.8)
        M, _ = gale_shapley_incompleto(pa, pb)
        estables = [
            E for E in emparejamientos_parciales(4, 4)
            if es_aceptable(E, pa, pb) and not buscar_bloqueantes(E, pa, pb)
        ]
        assert M in estables
        solos_gs = {a for a, b in enumerate(M) if b is None}
        for E in estables:
            # Teorema de Hospitales Rurales: los agentes que quedan solos son exactamente los mismos
            solos_e = {a for a, b in enumerate(E) if b is None}
            assert solos_gs == solos_e
        for a in range(4):
            pos_gs = len(pa[a]) if M[a] is None else pa[a].index(M[a])
            mejor_pos = min(len(pa[a]) if E[a] is None else pa[a].index(E[a]) for E in estables)
            assert pos_gs == mejor_pos
    print("Optimalidad y Teorema de Hospitales Rurales verificados en 200 instancias 4x4.")

    # 4. Medicion de tiempos reales de ejecucion y escalabilidad lineal O(m)
    print("\n=== Escalabilidad lineal respecto al numero de aristas aceptables m ===")
    print(f"{'n':>6} {'aristas m':>12} {'propuestas':>12} {'tiempo (ms)':>12} {'ns / arista':>12}")
    for n_esc in [50, 100, 200, 400]:
        pa_e, pb_e = generar_instancia(n_esc, n_esc, rng, p_a=0.4, p_b=0.8)
        m_aristas = sum(len(l) for l in pa_e) + sum(len(l) for l in pb_e)
        t0 = time.perf_counter()
        _, props = gale_shapley_incompleto(pa_e, pb_e)
        dt_ms = (time.perf_counter() - t0) * 1000
        ns_por_arista = (dt_ms * 1e6) / m_aristas
        print(f"{n_esc:>6} {m_aristas:>12} {props:>12} {dt_ms:>12.3f} {ns_por_arista:>12.1f}")

    # 5. Experimento y grafica variando la densidad p de las listas
    n = 25
    densidades = [i / 20 for i in range(1, 21)]
    rep = 150

    solos_unilateral, solos_bilateral = [], []
    prop_unilateral, lambda_unilateral = [], []

    for p in densidades:
        s_uni, s_bi = 0, 0
        k_uni, lam_uni = 0, 0
        for _ in range(rep):
            pa1, pb1 = generar_instancia(n, n, rng, p_a=p, p_b=1.0)
            M1, k1 = gale_shapley_incompleto(pa1, pb1)
            s_uni += sum(1 for b in M1 if b is None) / n
            k_uni += k1
            lam_uni += sum(len(l) for l in pa1)

            pa2, pb2 = generar_instancia(n, n, rng, p_a=p, p_b=p)
            M2, _ = gale_shapley_incompleto(pa2, pb2)
            s_bi += sum(1 for b in M2 if b is None) / n

        solos_unilateral.append(100 * s_uni / rep)
        solos_bilateral.append(100 * s_bi / rep)
        prop_unilateral.append(k_uni / rep)
        lambda_unilateral.append(lam_uni / rep)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.3))

    ax1.plot(densidades, solos_unilateral, "o-", color="#1f77b4", lw=2, markersize=4,
             label="Incompletas solo en proponentes")
    ax1.plot(densidades, solos_bilateral, "s--", color="#d62728", lw=1.8, markersize=4,
             label="Incompletas en ambos lados")
    ax1.set_title("Agentes que se quedan solos segun densidad (n = 25)")
    ax1.set_xlabel("Fraccion esperada de aceptables en la lista (p)")
    ax1.set_ylabel("Proponentes que terminan solos (%)")
    ax1.grid(True, alpha=0.3)
    ax1.legend()

    ax2.plot(densidades, lambda_unilateral, "--", color="#555555", lw=1.8,
             label="Cota del potencial Lambda = sum |L(a)|")
    ax2.plot(densidades, prop_unilateral, "o-", color="#2ca02c", lw=2, markersize=4,
             label="Propuestas reales promedio")
    ax2.set_title("Propuestas realizadas vs cota del potencial (n = 25)")
    ax2.set_xlabel("Fraccion esperada de aceptables en la lista (p)")
    ax2.set_ylabel("Numero de propuestas")
    ax2.grid(True, alpha=0.3)
    ax2.legend()

    plt.tight_layout()
    salida_png = Path(__file__).with_name("ejercicio-12.png")
    plt.savefig(salida_png, dpi=150)
    plt.close(fig)
    print(f"\nGrafica guardada en {salida_png.name}")
