"""Genera figuras para la Pregunta 1 sobre el efecto de una computadora 1000x más rápida.

Las imágenes se guardan automáticamente en la misma carpeta donde se encuentra
este archivo. Requisitos: matplotlib, numpy (dependencia de matplotlib) y Pillow.

Instalación, si hace falta:
    python -m pip install matplotlib pillow

Ejecución:
    python graficos_pregunta1.py
"""

from pathlib import Path
import math
import io

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from PIL import Image


# ===============================================================
# CONFIGURACIÓN GENERAL
# ===============================================================

CARPETA_SALIDA = Path(__file__).resolve().parent

C_ORIGINAL = 1_000_000
FACTOR_VELOCIDAD = 1_000
C_NUEVA = C_ORIGINAL * FACTOR_VELOCIDAD

# Paleta unificada, siguiendo el estilo del código de referencia.
C_INT = "#90caf9"       # Azul: máquina/presupuesto original
C_HOJA = "#ffcc80"      # Naranja: máquina/presupuesto nuevo
C_RUTA = "#d32f2f"      # Rojo: mejora o resultado destacado
C_BORDE = "#455a64"
C_GRIS = "#78909c"
C_VERDE = "#a5d6a7"
C_FONDO = "#ffffff"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.titleweight": "bold",
    "figure.facecolor": C_FONDO,
    "axes.facecolor": C_FONDO,
})


# ===============================================================
# CÁLCULOS BASE: LOS MISMOS DEL ANÁLISIS MATEMÁTICO
# ===============================================================

def max_cuadratica(presupuesto: int) -> int:
    """Mayor n entero que cumple n² <= presupuesto."""
    return math.isqrt(presupuesto)


def max_exponencial(presupuesto: int) -> int:
    """Mayor n entero que cumple 2ⁿ <= presupuesto."""
    if presupuesto < 1:
        return -1
    return presupuesto.bit_length() - 1


N2_ORIGINAL = max_cuadratica(C_ORIGINAL)
N2_NUEVA = max_cuadratica(C_NUEVA)
NEXP_ORIGINAL = max_exponencial(C_ORIGINAL)
NEXP_NUEVA = max_exponencial(C_NUEVA)
FACTOR_CUADRATICO = N2_NUEVA / N2_ORIGINAL
INCREMENTO_EXPONENCIAL = NEXP_NUEVA - NEXP_ORIGINAL

# Comprobaciones para evitar generar gráficos si los datos se alteran por error.
assert C_NUEVA == 1_000_000_000
assert (N2_ORIGINAL, N2_NUEVA) == (1000, 31622)
assert (NEXP_ORIGINAL, NEXP_NUEVA) == (19, 29)


def guardar_figura(fig, nombre: str) -> None:
    ruta = CARPETA_SALIDA / nombre
    fig.savefig(ruta, dpi=160, bbox_inches="tight", facecolor=C_FONDO)
    plt.close(fig)
    print(f"-> Generado: {ruta.name}")


# ===============================================================
# FIGURA 1: PRESUPUESTO DE OPERACIONES
# ===============================================================

def generar_figura_presupuestos() -> None:
    fig, ax = plt.subplots(figsize=(10, 5.2))

    etiquetas = ["Computadora original", "Computadora nueva"]
    valores = [C_ORIGINAL, C_NUEVA]
    colores = [C_INT, C_HOJA]
    barras = ax.bar(etiquetas, valores, color=colores, edgecolor=C_BORDE,
                    linewidth=1.3, width=0.52)

    ax.set_yscale("log")
    ax.set_ylabel("Operaciones disponibles en una hora (escala logarítmica)")
    ax.set_title("Una mejora de hardware de 1000 veces multiplica el presupuesto de operaciones")
    ax.grid(axis="y", which="both", alpha=0.22)
    ax.set_axisbelow(True)

    for barra, valor in zip(barras, valores):
        ax.text(barra.get_x() + barra.get_width() / 2,
                valor * 1.18,
                f"{valor:,.0f}",
                ha="center", va="bottom", fontweight="bold", fontsize=12)

    ax.annotate("1000 veces más operaciones",
                xy=(1, C_NUEVA * 0.7), xytext=(0.48, 2.5e7),
                ha="center", color=C_RUTA, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=C_RUTA, lw=2))

    ax.text(0.5, -0.22,
            r"$C_{nueva}=1000\cdot C_{original}=10^9$ operaciones",
            transform=ax.transAxes, ha="center", fontsize=12)
    ax.spines[["top", "right"]].set_visible(False)
    guardar_figura(fig, "fig1_presupuesto_operaciones.png")


# ===============================================================
# FIGURA 2: TAMAÑOS DE ENTRADA QUE SE PUEDEN RESOLVER
# ===============================================================

def generar_figura_tamanos() -> None:
    fig, axs = plt.subplots(1, 2, figsize=(12, 5.3))
    etiquetas = ["Original", "1000x más rápida"]
    colores = [C_INT, C_HOJA]

    datos = [
        (axs[0], [N2_ORIGINAL, N2_NUEVA], r"Algoritmo $O(n^2)$",
         "Tamaño máximo de entrada", f"Crecimiento: × {FACTOR_CUADRATICO:.2f}"),
        (axs[1], [NEXP_ORIGINAL, NEXP_NUEVA], r"Algoritmo $O(2^n)$",
         "Tamaño máximo de entrada", f"Crecimiento: + {INCREMENTO_EXPONENCIAL} elementos"),
    ]

    for ax, valores, titulo, eje_y, anotacion in datos:
        barras = ax.bar(etiquetas, valores, color=colores,
                        edgecolor=C_BORDE, linewidth=1.2, width=0.55)
        ax.set_title(titulo)
        ax.set_ylabel(eje_y)
        ax.grid(axis="y", alpha=0.22)
        ax.set_axisbelow(True)
        ax.spines[["top", "right"]].set_visible(False)
        ax.set_ylim(0, max(valores) * 1.25)
        for barra, valor in zip(barras, valores):
            ax.text(barra.get_x() + barra.get_width() / 2,
                    barra.get_height() + max(valores) * 0.025,
                    f"{valor:,}".replace(",", "."),
                    ha="center", va="bottom", fontweight="bold", fontsize=12)
        ax.text(0.5, 0.91, anotacion, transform=ax.transAxes,
                ha="center", color=C_RUTA, fontweight="bold", fontsize=11,
                bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=C_RUTA, alpha=0.95))

    fig.suptitle("El mismo aumento de velocidad produce efectos distintos según la complejidad",
                 fontsize=14, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.91))
    guardar_figura(fig, "fig2_tamanos_de_entrada.png")


# ===============================================================
# FIGURA 3: FACTOR DE CRECIMIENTO EN FUNCIÓN DE LA VELOCIDAD
# ===============================================================

def generar_figura_factores() -> None:
    fig, ax = plt.subplots(figsize=(10.5, 5.8))

    factores = [10 ** (i / 20) for i in range(0, 121)]  # desde 1 hasta 1 000 000
    crecimiento_cuad = [math.sqrt(k) for k in factores]
    crecimiento_exp = [math.log2(k) for k in factores]

    ax.plot(factores, crecimiento_cuad, color=C_RUTA, lw=2.8,
            label=r"$O(n^2)$: factor del tamaño = $\sqrt{k}$")
    ax.plot(factores, crecimiento_exp, color="#1565c0", lw=2.8,
            label=r"$O(2^n)$: elementos adicionales = $\log_2(k)$")

    k = FACTOR_VELOCIDAD
    y_cuad = math.sqrt(k)
    y_exp = math.log2(k)
    ax.scatter([k], [y_cuad], s=85, color=C_RUTA, edgecolor="white", linewidth=1.2, zorder=5)
    ax.scatter([k], [y_exp], s=85, color="#1565c0", edgecolor="white", linewidth=1.2, zorder=5)
    ax.axvline(k, color=C_GRIS, ls="--", lw=1.5)
    ax.annotate(rf"$k=1000$: $\sqrt{{1000}}\approx{y_cuad:.2f}$",
                xy=(k, y_cuad), xytext=(1600, y_cuad + 115),
                arrowprops=dict(arrowstyle="->", color=C_RUTA), color=C_RUTA,
                fontweight="bold")
    ax.annotate(rf"$\log_2(1000)\approx{y_exp:.2f}$ elementos",
                xy=(k, y_exp), xytext=(1500, y_exp + 85),
                arrowprops=dict(arrowstyle="->", color="#1565c0"), color="#1565c0",
                fontweight="bold")

    ax.set_xscale("log")
    ax.set_xlabel("Factor de aumento de velocidad de la computadora (k)")
    ax.set_ylabel("Crecimiento del tamaño de entrada")
    ax.set_title("Relación teórica entre la mejora del hardware y el tamaño de entrada")
    ax.grid(which="both", alpha=0.22)
    ax.legend(frameon=False, loc="upper left")
    ax.spines[["top", "right"]].set_visible(False)
    guardar_figura(fig, "fig3_factores_de_crecimiento.png")


# ===============================================================
# FIGURA 4: COSTO DE LOS ALGORITMOS Y PRESUPUESTOS
# ===============================================================

def generar_figura_costos() -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.8))

    # Caso cuadrático: se muestra el costo n² y los dos presupuestos.
    xs = list(range(1, N2_NUEVA + 1, 100))
    ys = [n * n for n in xs]
    ax1.plot(xs, ys, color="#1565c0", lw=2.5, label=r"Costo $n^2$")
    ax1.axhline(C_ORIGINAL, color=C_INT, ls="--", lw=2,
                label=r"Presupuesto original $10^6$")
    ax1.axhline(C_NUEVA, color=C_RUTA, ls="--", lw=2,
                label=r"Presupuesto nuevo $10^9$")
    ax1.axvline(N2_ORIGINAL, color=C_INT, ls=":", lw=1.8)
    ax1.axvline(N2_NUEVA, color=C_RUTA, ls=":", lw=1.8)
    ax1.scatter([N2_ORIGINAL, N2_NUEVA],
                [N2_ORIGINAL ** 2, N2_NUEVA ** 2],
                color=[C_INT, C_RUTA], edgecolor=C_BORDE, zorder=5, s=60)
    ax1.annotate("n = 1000", (N2_ORIGINAL, N2_ORIGINAL ** 2),
                 xytext=(2500, 2.2e6), arrowprops=dict(arrowstyle="->", color=C_GRIS))
    ax1.annotate("n = 31622", (N2_NUEVA, N2_NUEVA ** 2),
                 xytext=(20500, 2.2e8), arrowprops=dict(arrowstyle="->", color=C_GRIS))
    ax1.set_yscale("log")
    ax1.set_xlabel("Tamaño de entrada n")
    ax1.set_ylabel("Operaciones requeridas (escala logarítmica)")
    ax1.set_title(r"Costo cuadrático: $n^2$")
    ax1.grid(which="both", alpha=0.2)
    ax1.legend(frameon=False, fontsize=8, loc="upper left")
    ax1.spines[["top", "right"]].set_visible(False)

    # Caso exponencial: se muestran los umbrales enteros 19 y 29.
    ns = list(range(0, NEXP_NUEVA + 2))
    costos = [2 ** n for n in ns]
    ax2.plot(ns, costos, color="#1565c0", lw=2.5, marker="o", ms=4,
             label=r"Costo $2^n$")
    ax2.axhline(C_ORIGINAL, color=C_INT, ls="--", lw=2,
                label=r"Presupuesto original $10^6$")
    ax2.axhline(C_NUEVA, color=C_RUTA, ls="--", lw=2,
                label=r"Presupuesto nuevo $10^9$")
    ax2.axvline(NEXP_ORIGINAL, color=C_INT, ls=":", lw=1.8)
    ax2.axvline(NEXP_NUEVA, color=C_RUTA, ls=":", lw=1.8)
    ax2.scatter([NEXP_ORIGINAL, NEXP_NUEVA],
                [2 ** NEXP_ORIGINAL, 2 ** NEXP_NUEVA],
                color=[C_INT, C_RUTA], edgecolor=C_BORDE, zorder=5, s=65)
    ax2.annotate("n = 19", (NEXP_ORIGINAL, 2 ** NEXP_ORIGINAL),
                 xytext=(9, 4e7), arrowprops=dict(arrowstyle="->", color=C_GRIS))
    ax2.annotate("n = 29", (NEXP_NUEVA, 2 ** NEXP_NUEVA),
                 xytext=(22, 2e8), arrowprops=dict(arrowstyle="->", color=C_GRIS))
    ax2.set_yscale("log")
    ax2.set_xlabel("Tamaño de entrada n")
    ax2.set_ylabel("Operaciones requeridas (escala logarítmica)")
    ax2.set_title(r"Costo exponencial: $2^n$")
    ax2.grid(which="both", alpha=0.2)
    ax2.legend(frameon=False, fontsize=8, loc="upper left")
    ax2.spines[["top", "right"]].set_visible(False)

    fig.suptitle("Cuánto permite resolver cada presupuesto según el costo del algoritmo",
                 fontsize=14, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    guardar_figura(fig, "fig4_costos_y_presupuestos.png")


# ===============================================================
# FIGURA 5: GIF DE LA EVOLUCIÓN AL AUMENTAR LA VELOCIDAD
# ===============================================================

def crear_frame_gif(k: int) -> Image.Image:
    factor_cuad = math.sqrt(k)
    incremento_exp = math.log2(k)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.2))
    fig.suptitle(f"Efecto de multiplicar la velocidad por k = {k:,}".replace(",", "."),
                 fontsize=14, fontweight="bold")

    # El caso cuadrático crece multiplicativamente.
    ax1.bar(["Tamaño relativo"], [factor_cuad], color=C_INT,
            edgecolor=C_BORDE, width=0.5)
    ax1.set_ylim(0, math.sqrt(FACTOR_VELOCIDAD) * 1.25)
    ax1.set_ylabel("Factor respecto al tamaño original")
    ax1.set_title(r"$O(n^2)$: $\sqrt{k}$")
    ax1.text(0, factor_cuad + 0.7, f"× {factor_cuad:.2f}",
             ha="center", fontweight="bold", color=C_RUTA, fontsize=12)
    ax1.grid(axis="y", alpha=0.2)
    ax1.set_axisbelow(True)
    ax1.spines[["top", "right"]].set_visible(False)

    # El caso exponencial crece aditivamente.
    ax2.bar(["Elementos extra"], [incremento_exp], color=C_HOJA,
            edgecolor=C_BORDE, width=0.5)
    ax2.set_ylim(0, math.log2(FACTOR_VELOCIDAD) * 1.45)
    ax2.set_ylabel("Elementos adicionales")
    ax2.set_title(r"$O(2^n)$: $\log_2(k)$")
    ax2.text(0, incremento_exp + 0.25, f"+ {incremento_exp:.2f}",
             ha="center", fontweight="bold", color=C_RUTA, fontsize=12)
    ax2.grid(axis="y", alpha=0.2)
    ax2.set_axisbelow(True)
    ax2.spines[["top", "right"]].set_visible(False)

    fig.text(0.5, 0.035,
             "La mejora ayuda mucho más al algoritmo cuadrático que al exponencial.",
             ha="center", fontsize=10, color=C_BORDE)
    fig.tight_layout(rect=(0, 0.09, 1, 0.88))

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", dpi=105, facecolor=C_FONDO)
    plt.close(fig)
    buffer.seek(0)
    return Image.open(buffer).convert("RGB")


def generar_gif() -> None:
    factores = [1, 2, 5, 10, 25, 50, 100, 250, 500, 1_000]
    frames = [crear_frame_gif(k) for k in factores]
    duraciones = [900] * (len(frames) - 1) + [2600]

    ruta = CARPETA_SALIDA / "fig5_evolucion_mejora_hardware.gif"
    frames[0].save(ruta, save_all=True, append_images=frames[1:],
                   duration=duraciones, loop=0, optimize=True)
    for frame in frames:
        frame.close()
    print(f"-> Generado: {ruta.name} ({len(factores)} etapas)")


# ===============================================================
# EJECUCIÓN
# ===============================================================

def main() -> None:
    print("Generando visualizaciones de la Pregunta 1...\n")
    generar_figura_presupuestos()
    generar_figura_tamanos()
    generar_figura_factores()
    generar_figura_costos()
    generar_gif()

    print("\n¡Listo! Se generaron 5 archivos en la carpeta del script:")
    print(" - fig1_presupuesto_operaciones.png")
    print(" - fig2_tamanos_de_entrada.png")
    print(" - fig3_factores_de_crecimiento.png")
    print(" - fig4_costos_y_presupuestos.png")
    print(" - fig5_evolucion_mejora_hardware.gif")
    print("\nResultados usados:")
    print(f" - O(n²): {N2_ORIGINAL} -> {N2_NUEVA} (factor {FACTOR_CUADRATICO:.4f})")
    print(f" - O(2ⁿ): {NEXP_ORIGINAL} -> {NEXP_NUEVA} (+{INCREMENTO_EXPONENCIAL} elementos)")


if __name__ == "__main__":
    main()
