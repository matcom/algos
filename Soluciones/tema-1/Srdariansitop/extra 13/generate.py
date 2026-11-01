import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter

OUT = os.path.dirname(os.path.abspath(__file__))
AZUL, NARANJA, ROJO, VERDE, GRIS = "#2b6cb0", "#ed8936", "#c53030", "#2f855a", "#718096"


# ----------------------------------------------------------------- estructura
class Arbol:
    """BST con punteros al padre. Claves 1..n; 0 = nulo."""

    def __init__(self, n):
        self.n = n
        self.L = [0] * (n + 1)
        self.R = [0] * (n + 1)
        self.P = [0] * (n + 1)
        for k in range(1, n):          # camino(n): k es hijo izquierdo de k+1
            self.L[k + 1] = k
            self.P[k] = k + 1
        self.root = n

    def rotar(self, x):
        p = self.P[x]
        g = self.P[p]
        if self.L[p] == x:
            b = self.R[x]
            self.L[p] = b
            self.R[x] = p
        else:
            b = self.L[x]
            self.R[p] = b
            self.L[x] = p
        if b:
            self.P[b] = p
        self.P[p] = x
        self.P[x] = g
        if g == 0:
            self.root = x
        elif self.L[g] == p:
            self.L[g] = x
        else:
            self.R[g] = x

    def profundidad(self, x):
        d = 0
        while self.P[x]:
            x = self.P[x]
            d += 1
        return d

    def tamanos(self):
        """s(v) para todo v (iterativo, sin recursion)."""
        s = [0] * (self.n + 1)
        orden, pila = [], [self.root]
        while pila:
            v = pila.pop()
            orden.append(v)
            for h in (self.L[v], self.R[v]):
                if h:
                    pila.append(h)
        for v in reversed(orden):
            s[v] = 1 + s[self.L[v]] + s[self.R[v]]
        return s

    def potencial(self):
        s = self.tamanos()
        return sum(math.log2(s[v]) for v in range(1, self.n + 1))

    def splay(self, x, paso=None):
        """Devuelve el costo real = rotaciones (1 si x ya es la raiz)."""
        if self.P[x] == 0:
            return 1
        costo = 0
        while self.P[x]:
            p = self.P[x]
            g = self.P[p]
            if g == 0:
                self.rotar(x); costo += 1; tipo = "zig"
            elif (self.L[g] == p) == (self.L[p] == x):
                self.rotar(p); self.rotar(x); costo += 2; tipo = "zig-zig"
            else:
                self.rotar(x); self.rotar(x); costo += 2; tipo = "zig-zag"
            if paso:
                paso(tipo)
        return costo

    def a_la_raiz(self, x):
        """Heuristica 'subir a la raiz': solo rotaciones simples."""
        if self.P[x] == 0:
            return 1
        c = 0
        while self.P[x]:
            self.rotar(x); c += 1
        return c

    def posiciones(self):
        """x = posicion inorden, y = -profundidad."""
        pos, pila, v, i = {}, [], self.root, 0
        prof = {self.root: 0}
        while pila or v:
            while v:
                pila.append(v)
                h = self.L[v]
                if h:
                    prof[h] = prof[v] + 1
                v = h
            v = pila.pop()
            pos[v] = (i, -prof[v])
            i += 1
            h = self.R[v]
            if h:
                prof[h] = prof[v] + 1
            v = h
        return pos


def dibujar(ax, T, resaltar=None, rangos=False, titulo=""):
    pos = T.posiciones()
    s = T.tamanos() if rangos else None
    for v, (x, y) in pos.items():
        for h in (T.L[v], T.R[v]):
            if h:
                ax.plot([x, pos[h][0]], [y, pos[h][1]], color=GRIS, lw=1.2, zorder=1)
    for v, (x, y) in pos.items():
        c = NARANJA if v == resaltar else AZUL
        ax.scatter([x], [y], s=520, color=c, zorder=2, edgecolor="white", lw=1.5)
        ax.text(x, y, str(v), ha="center", va="center", color="white",
                fontsize=9, fontweight="bold", zorder=3)
        if rangos:
            ax.text(x + 0.18, y + 0.30, f"s={s[v]}", fontsize=7, color=ROJO)
    ax.set_title(titulo, fontsize=10)
    ax.set_xlim(-1, T.n)
    ax.set_ylim(min(p[1] for p in pos.values()) - 1, 1)
    ax.axis("off")


def guardar(fig, nombre):
    ruta = os.path.join(OUT, nombre)
    fig.savefig(ruta, dpi=130, bbox_inches="tight")
    plt.close(fig)
    print("  ->", nombre)


# ---------------------------------------------------------------- simulaciones
def simular(n, metodo="splay"):
    """Accede 1..n. Devuelve costos, potenciales (Phi_0..Phi_n), rangos de x_i."""
    T = Arbol(n)
    costos, phis, rx = [], [T.potencial()], []
    for k in range(1, n + 1):
        rx.append(math.log2(T.tamanos()[k]))
        c = T.splay(k) if metodo == "splay" else T.a_la_raiz(k)
        costos.append(c)
        phis.append(T.potencial())
    return np.array(costos), np.array(phis), np.array(rx)


# --------------------------------------------------------------------- figuras
def fig1_problema(n=8):
    T = Arbol(n)
    fig, ax = plt.subplots(figsize=(7, 5))
    dibujar(ax, T, rangos=True,
            titulo=f"Fig. 1 - camino({n}): raíz = {n}, clave 1 a profundidad {n-1}\n"
                   f"tamaños s = 1,2,...,{n}  =>  Φ0 = log2({n}!) = {math.log2(math.factorial(n)):.2f}")
    guardar(fig, "fig1_problema_camino_inicial.png")


def fig2_primeros_accesos(n=8, accesos=4):
    fig, axs = plt.subplots(1, accesos + 1, figsize=(3.3 * (accesos + 1), 4.2))
    T = Arbol(n)
    dibujar(axs[0], T, titulo="Inicial")
    for k in range(1, accesos + 1):
        c = T.splay(k)
        dibujar(axs[k], T, resaltar=k, titulo=f"Tras acceder {k}\ncosto real = {c}")
    fig.suptitle("Fig. 2 - El primer acceso cuesta n-1 y deja el árbol 'enrollado': "
                 "los siguientes son baratos", fontsize=11, y=1.06)
    guardar(fig, "fig2_primeros_accesos.png")


def fig3_gif(n=10):
    T = Arbol(n)
    estados = [(T.L[:], T.R[:], T.P[:], T.root, None, "Árbol inicial (camino)")]
    for k in range(1, n + 1):
        def paso(tipo, k=k):
            estados.append((T.L[:], T.R[:], T.P[:], T.root, k, f"acceso({k}): {tipo}"))
        T.splay(k, paso)
        if len(estados) == 0 or estados[-1][4] != k:      # x ya era la raiz
            estados.append((T.L[:], T.R[:], T.P[:], T.root, k, f"acceso({k}): ya es la raíz"))
    fig, ax = plt.subplots(figsize=(7, 4.5))
    aux = Arbol(n)

    def cuadro(i):
        ax.clear()
        aux.L, aux.R, aux.P, aux.root, nodo, txt = estados[i]
        dibujar(ax, aux, resaltar=nodo, titulo=f"Fig. 3 - {txt}")
    anim = FuncAnimation(fig, cuadro, frames=len(estados), interval=700)
    ruta = os.path.join(OUT, "fig3_animacion_splay.gif")
    anim.save(ruta, writer=PillowWriter(fps=1.4))
    plt.close(fig)
    print("  -> fig3_animacion_splay.gif")


def fig4_costo_por_acceso(n=128):
    c, _, _ = simular(n)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(range(1, n + 1), c, color=AZUL)
    ax.axhline(c[1:].mean(), color=ROJO, ls="--",
               label=f"media sin el 1.er acceso = {c[1:].mean():.2f}")
    ax.set_yscale("log")
    ax.annotate(f"acceso 1: {c[0]} rotaciones\n(= n-1)", xy=(1, c[0]),
                xytext=(n * 0.25, c[0] * 0.5), arrowprops=dict(arrowstyle="->"))
    ax.set_xlabel("acceso i (clave i)")
    ax.set_ylabel("costo real c_i (escala log)")
    ax.set_title(f"Fig. 4 - Costo real por acceso, n = {n}: un único pico y luego ≈ 2-4")
    ax.legend()
    guardar(fig, "fig4_costo_por_acceso.png")


def fig5_potencial(n=128):
    c, phi, _ = simular(n)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(range(n + 1), phi, color=AZUL, lw=2, label="Φ_i (potencial real)")
    ax.axhline(n * math.log2(n), color=ROJO, ls="--", label="n·log2 n (cota usada para Φ0)")
    ax.axhline(math.log2(math.factorial(n)), color=VERDE, ls=":", label="Φ0 = log2(n!)")
    ax.set_xlabel("accesos realizados i")
    ax.set_ylabel("Φ")
    ax.set_title(f"Fig. 5 - Potencial, n = {n}: arranca en Φ0 ≈ n log n y se libera casi todo\n"
                 f"en pocos accesos; Φ_n = {phi[-1]:.0f}  (>= 0, >= log2 n)")
    ax.legend()
    guardar(fig, "fig5_potencial.png")


def fig6_cota_vs_medido():
    ns = [25, 50, 100, 200, 400, 800]
    cota, sp, ar = [], [], []
    for n in ns:
        cota.append(4 * math.log2(n) + 1)
        sp.append(simular(n, "splay")[0].mean())
        ar.append(simular(n, "raiz")[0].mean())
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(ns, cota, "o--", color=ROJO, label="cota del lema: 4 log2 n + 1")
    ax.plot(ns, sp, "o-", color=AZUL, label="splay (medido)")
    ax.plot(ns, ar, "o-", color=NARANJA, label="subir a la raíz (medido)")
    ax.plot(ns, [n / 2 for n in ns], ":", color=GRIS, label="n/2")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("n"); ax.set_ylabel("costo medio por acceso")
    ax.set_title("Fig. 6 - Lema vs sección 6: splay queda plano; subir a la raíz crece como n")
    ax.legend()
    guardar(fig, "fig6_cota_vs_medido.png")


def fig7_total_y_holgura():
    ns = np.array([16, 32, 64, 128, 256, 512, 1024])
    tot_s = [simular(int(n), "splay")[0].sum() for n in ns]
    cota = 4 * ns * np.log2(ns) + ns
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.8))
    ax = axs[0]
    ax.plot(ns, cota, "o--", color=ROJO, label="cota C ≤ 4 n log2 n + n")
    ax.plot(ns, tot_s, "o-", color=AZUL, label="C medido (splay)")
    ax.plot(ns, ns, ":", color=VERDE, label="cota inferior C ≥ n")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("n"); ax.set_ylabel("costo total C")
    ax.set_title("Costo total: la cota es O(n log n), lo real es Θ(n)")
    ax.legend()
    ax = axs[1]
    ax.plot(ns, cota / np.array(tot_s), "o-", color=NARANJA)
    ax.plot(ns, np.log2(ns), ":", color=GRIS, label="log2 n (referencia)")
    ax.set_xscale("log")
    ax.set_xlabel("n"); ax.set_ylabel("cota / costo real")
    ax.set_title("Holgura de la cota: crece como log n")
    ax.legend()
    fig.suptitle("Fig. 7 - ¿Es ajustada la cota para ESTA secuencia? No", fontsize=12)
    guardar(fig, "fig7_total_y_holgura.png")


def fig8_lema_por_acceso(n=128):
    c, phi, rx = simular(n)
    a = c + phi[1:] - phi[:-1]                         # costo amortizado a_i
    lema = 3 * (math.log2(n) - rx) + 1                  # cota del lema de acceso
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.plot(range(1, n + 1), lema, color=ROJO, label="cota del lema: 3(r(t) - r(x_i)) + 1")
    ax.plot(range(1, n + 1), a, color=AZUL, label="costo amortizado a_i = c_i + ΔΦ")
    ax.plot(range(1, n + 1), c, color=VERDE, alpha=0.6, label="costo real c_i")
    ax.set_yscale("symlog", linthresh=10)
    ax.set_xlabel("acceso i"); ax.set_ylabel("costo")
    ax.set_title(f"Fig. 8 - a_i ≤ cota del lema en todos los accesos (n = {n}); "
                 f"Σ a_i = {a.sum():.0f}, Σ cotas = {lema.sum():.0f}", fontsize=10)
    ax.legend()
    assert np.all(a <= lema + 1e-9), "el lema deberia cumplirse siempre"
    guardar(fig, "fig8_lema_por_acceso.png")


if __name__ == "__main__":
    print("Generando figuras en:", OUT)
    fig1_problema()
    fig2_primeros_accesos()
    fig3_gif()
    fig4_costo_por_acceso()
    fig5_potencial()
    fig6_cota_vs_medido()
    fig7_total_y_holgura()
    fig8_lema_por_acceso()
    print("Listo.")