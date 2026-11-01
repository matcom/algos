from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np


class Nodo:
    __slots__ = ("sig", "idx")

    def __init__(self, idx=0):
        self.sig = None
        self.idx = idx


def construir_lista(mu, lam):
    """
    Construye una lista enlazada con una cola de mu nodos y un ciclo de lam nodos.
    Si lam == 0, la lista no tiene ciclo y cuenta con mu nodos en total.
    """
    nodos = [Nodo(i) for i in range(mu + lam)]
    for a, b in zip(nodos, nodos[1:]):
        a.sig = b
    if lam > 0:
        nodos[-1].sig = nodos[mu]
    return (nodos[0] if nodos else None), nodos


def nodo_en_paso(nodos, mu, lam, i):
    """Devuelve el nodo x_i de la sucesion x_0 = cabeza, x_{i+1} = x_i.sig."""
    if lam == 0 or i < mu:
        return nodos[i] if i < len(nodos) else None
    return nodos[mu + (i - mu) % lam]


def floyd(cabeza, vigilar=None):
    """
    Ejecuta el algoritmo de la tortuga y la liebre de Floyd.
    Devuelve (hay_ciclo, vueltas).
    """
    t = h = cabeza
    k = 0
    while h is not None and h.sig is not None:
        if vigilar is not None:
            vigilar(k, t, h)
        t = t.sig
        h = h.sig.sig
        k += 1
        if t is h:
            if vigilar is not None:
                vigilar(k, t, h, final=True)
            return True, k
    return False, k


def traza_con_potenciales(mu, lam):
    """Devuelve la lista de estados por vuelta (k, idx_t, idx_h, fase, phi1, g_k, phi_total)."""
    cabeza, _ = construir_lista(mu, lam)
    k0 = max(mu, 1)
    estados = []

    def registrar(k, t, h, final=False):
        fase = 1 if k < k0 else 2
        phi1 = max(k0 - k, 0)
        gk = (-k) % lam
        phi_total = lam * phi1 + gk
        estados.append((k, t.idx, h.idx, fase, phi1, gk, phi_total))

    floyd(cabeza, vigilar=registrar)
    return estados


if __name__ == "__main__":
    # 1. Traza detallada para mu = 7, lambda = 5
    mu_ej, lam_ej = 7, 5
    estados_ej = traza_con_potenciales(mu_ej, lam_ej)
    print(f"=== Traza paso a paso para mu = {mu_ej}, lambda = {lam_ej} ===")
    print(f"{'k':>3} | {'tortuga (x_k)':>14} | {'liebre (x_2k)':>15} | {'Fase':>9} | {'Phi_1':>5} | {'g_k':>4} | {'Phi total':>9}")
    print("-" * 73)
    for k, it, ih, fase, phi1, gk, ptot in estados_ej:
        etiqueta_f = f"Fase {fase}" if k < estados_ej[-1][0] else "Encuentro"
        print(f"{k:>3} | {'x_' + str(k) + f' (nodo {it})':>14} | {'x_' + str(2*k) + f' (nodo {ih})':>15} | {etiqueta_f:>9} | {phi1:>5} | {gk:>4} | {ptot:>9}")
    print()

    # 2. Verificacion exhaustiva sobre todas las listas con mu, lam in [0, 25]
    casos = 0
    for mu in range(0, 26):
        for lam in range(0, 26):
            if mu + lam == 0:
                continue
            cabeza, nodos = construir_lista(mu, lam)
            prev_g = {}

            def revisar(k, t, h, final=False):
                assert t is nodo_en_paso(nodos, mu, lam, k)
                assert h is nodo_en_paso(nodos, mu, lam, 2 * k)
                if not final and lam > 0 and k >= max(mu, 1):
                    g = (-k) % lam
                    if "val" in prev_g:
                        assert g == prev_g["val"] - 1
                    prev_g["val"] = g

            hay, vueltas = floyd(cabeza, vigilar=revisar)
            assert hay == (lam > 0)
            if lam > 0:
                k0 = max(mu, 1)
                k_est = ((k0 + lam - 1) // lam) * lam
                assert vueltas == k_est <= mu + lam
            else:
                assert vueltas == mu // 2
            casos += 1

    print(f"Verificadas {casos} configuraciones (mu, lambda <= 25): invariante, potencial y pasos exactos sin fallos.")

    print(f"\n{'mu':>5} {'lambda':>7} {'vueltas k*':>11} {'cota mu + lambda':>17}")
    for mu, lam in [(0, 1), (0, 10), (4, 5), (7, 5), (11, 6), (10, 10), (100, 37)]:
        cab, _ = construir_lista(mu, lam)
        _, v = floyd(cab)
        print(f"{mu:>5} {lam:>7} {v:>11} {mu + lam:>17}")

    # 3. Generacion de la figura con 2 paneles
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.6))

    # Panel 1: evolucion de potenciales para (mu=7, lam=5) y (mu=11, lam=6)
    ejemplos = [
        (7, 5, "#1f77b4", "o"),
        (11, 6, "#d62728", "s"),
    ]
    for mu, lam, color, marker in ejemplos:
        est = traza_con_potenciales(mu, lam)
        ks = [ fila[0] for fila in est ]
        phi1s = [ fila[4] for fila in est ]
        gks = [ fila[5] for fila in est ]

        # Graficamos Phi_1 en fase 1 (k <= mu) y g_k en fase 2 (k >= mu)
        ks_f1 = [k for k in ks if k <= mu]
        p1_f1 = [phi1s[i] for i, k in enumerate(ks) if k <= mu]
        ks_f2 = [k for k in ks if k >= mu]
        gk_f2 = [gks[i] for i, k in enumerate(ks) if k >= mu]

        ax1.plot(ks_f1, p1_f1, linestyle="--", color=color, alpha=0.65, lw=1.8,
                 label=f"Fase 1: Phi_1 (mu={mu}, lam={lam})")
        ax1.plot(ks_f2, gk_f2, linestyle="-", marker=marker, color=color, lw=2.2, markersize=5,
                 label=f"Fase 2: g_k (mu={mu}, lam={lam})")
        ax1.axvline(mu, color=color, linestyle=":", alpha=0.4)

    ax1.set_title("Caida por fases de Phi_1(k) y g_k hasta el encuentro")
    ax1.set_xlabel("Vuelta k")
    ax1.set_ylabel("Valor del potencial en la fase activa")
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=8.5)

    # Panel 2: mapa de calor de k*(mu, lambda) para mu, lambda in [1, 25]
    max_val = 25
    matriz_k = np.zeros((max_val, max_val), dtype=int)
    for m_idx, mu in enumerate(range(1, max_val + 1)):
        for l_idx, lam in enumerate(range(1, max_val + 1)):
            matriz_k[l_idx, m_idx] = ((mu + lam - 1) // lam) * lam

    im = ax2.imshow(matriz_k, origin="lower", cmap="viridis", aspect="auto",
                    extent=[0.5, max_val + 0.5, 0.5, max_val + 0.5])
    cbar = fig.colorbar(im, ax=ax2)
    cbar.set_label("Pasos hasta el encuentro k*")
    ax2.set_title("Mapa de calor de k*(mu, lambda) = multiplo de lambda >= mu")
    ax2.set_xlabel("Longitud de la cola (mu)")
    ax2.set_ylabel("Longitud del ciclo (lambda)")
    ax2.set_xticks(range(1, max_val + 1, 3))
    ax2.set_yticks(range(1, max_val + 1, 3))

    plt.tight_layout()
    salida_png = Path(__file__).with_name("ejercicio-05.png")
    plt.savefig(salida_png, dpi=150)
    print(f"\nGrafica guardada en {salida_png.name}")
