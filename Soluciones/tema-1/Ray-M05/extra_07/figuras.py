import sys
from pathlib import Path

from matplotlib.patches import Rectangle

from comun import estilo
from comun.estilo import SERIES, TEXTO, TEXTO_2

AZUL, NARANJA = SERIES[0], SERIES[1]
CARPETA = Path(__file__).resolve().parent

A = [1, 4, 6, 9, 14, 17, 21, 25]
B = [2, 3, 8, 10, 11, 13, 19, 30]


def _rgb(hexa, alfa):
    return (*[int(hexa[k:k + 2], 16) / 255 for k in (1, 3, 5)], alfa)


def estados():
    n = len(A)
    lo, hi = 0, n
    cuadros = [(lo, hi, None, None, None, None,
                f"El corte i toma los i primeros de A y los n − i primeros de B. "
                f"Puede ser cualquiera de 0 a {n}.")]
    while lo < hi:
        i = (lo + hi) // 2
        par = (i, n - i - 1)
        cuadros.append((lo, hi, i, par, None, None,
                        f"Corte i = {i}: ¿A{i + 1} = {A[i]} ≥ B{n - i} = {B[n - i - 1]}?"))
        if A[i] >= B[n - i - 1]:
            hi = i
            texto = f"Sí: el corte buscado es ≤ {i}. Quedan los cortes de {lo} a {hi}."
        else:
            lo = i + 1
            texto = f"No: el corte buscado es ≥ {i + 1}. Quedan los cortes de {lo} a {hi}."
        cuadros.append((lo, hi, i, par, None, None, texto))
    i = lo
    tomados = (i, n - i)
    if 0 < i < n:
        respuesta = ("A", i - 1) if A[i - 1] >= B[n - i - 1] else ("B", n - i - 1)
        valor = A[i - 1] if respuesta[0] == "A" else B[n - i - 1]
        texto = (f"Corte i = {i}: los {n} menores son A1…A{i} y B1…B{n - i}. "
                 f"La mediana es max(A{i}, B{n - i}) = {valor}.")
    else:
        respuesta = ("B", n - 1) if i == 0 else ("A", n - 1)
        texto = f"Corte i = {i}."
    cuadros.append((lo, hi, i, None, tomados, respuesta, texto))
    return cuadros


def animacion():
    n = len(A)
    cuadros = estados()
    estilo.aplicar()
    fig, ax = estilo.figura(9, 3.8)
    ax.axis("off")
    ax.set_xlim(-1.2, n + 0.3)
    ax.set_ylim(-1.3, 3.1)
    ax.set_title("Mediana de dos arreglos: buscar el corte con búsqueda binaria", pad=4)
    filas = {"A": (A, 1.3), "B": (B, 0.0)}
    cajas, numeros = {}, []
    for lado, (valores, y) in filas.items():
        ax.text(-0.6, y + 0.4, lado, ha="center", va="center", fontsize=12, fontweight="bold")
        for k, v in enumerate(valores):
            r = Rectangle((k, y), 0.85, 0.8, facecolor="white", edgecolor=TEXTO_2)
            ax.add_patch(r)
            cajas[lado, k] = r
            numeros.append(ax.text(k + 0.425, y + 0.4, str(v), ha="center", va="center",
                                   fontsize=11, zorder=3))
            ax.text(k + 0.425, y - 0.18 if lado == "B" else y + 1.0, str(k + 1),
                    ha="center", va="center", fontsize=7, color=TEXTO_2)
    corte_A = ax.plot([], [], color=NARANJA, linewidth=3)[0]
    corte_B = ax.plot([], [], color=NARANJA, linewidth=3)[0]
    rango = ax.plot([], [], color=TEXTO, linewidth=2, solid_capstyle="butt")[0]
    rotulo_rango = ax.text(0, 2.85, "", ha="center", va="center", fontsize=9, color=TEXTO)
    texto = ax.text(-1.1, -0.75, "", ha="left", va="top", fontsize=10, color=TEXTO)

    def actualizar(c):
        lo, hi, i, par, tomados, respuesta, mensaje = cuadros[c]
        for (lado, k), r in cajas.items():
            tomado = tomados is not None and k < (tomados[0] if lado == "A" else tomados[1])
            r.set_facecolor(_rgb(AZUL, 0.3) if tomado else "white")
            marcado = (par is not None and ((lado == "A" and k == par[0]) or
                                            (lado == "B" and k == par[1]))) or \
                      (respuesta is not None and (lado, k) == respuesta)
            r.set_linewidth(3 if marcado else 1)
            r.set_edgecolor(TEXTO if marcado else TEXTO_2)
        if i is None:
            corte_A.set_data([], [])
            corte_B.set_data([], [])
        else:
            xa, xb = i - 0.075, (n - i) - 0.075
            corte_A.set_data([xa, xa], [1.15, 2.25])
            corte_B.set_data([xb, xb], [-0.15, 0.95])
        rango.set_data([lo - 0.075, hi - 0.075], [2.55, 2.55])
        rotulo_rango.set_position(((lo + hi) / 2 - 0.075, 2.85))
        rotulo_rango.set_text(f"cortes posibles: {lo}…{hi}" if lo < hi else f"corte: {lo}")
        texto.set_text(mensaje)


    moviles = list(cajas.values()) + numeros + [corte_A, corte_B, rango, rotulo_rango, texto]
    fig.tight_layout()
    print(estilo.guardar_gif(fig, moviles, actualizar, len(cuadros),
                             CARPETA / "corte.gif", "la búsqueda del corte",
                             fps=0.8, pausa=4.0))


FIGURAS = {"animacion": animacion}

if __name__ == "__main__":
    FIGURAS[sys.argv[1]]()
