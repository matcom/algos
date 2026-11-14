import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]
SUPERFICIE = "#fcfcfb"
TEXTO = "#0b0b0b"
TEXTO_2 = "#52514e"
REJILLA = "#e4e3df"


def aplicar():
    plt.rcParams.update({
        "figure.facecolor": SUPERFICIE,
        "axes.facecolor": SUPERFICIE,
        "savefig.facecolor": SUPERFICIE,
        "axes.edgecolor": TEXTO_2,
        "axes.labelcolor": TEXTO,
        "axes.titlecolor": TEXTO,
        "axes.titlesize": 12,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.labelsize": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.axisbelow": True,
        "grid.color": REJILLA,
        "grid.linewidth": 0.8,
        "xtick.color": TEXTO_2,
        "ytick.color": TEXTO_2,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.frameon": False,
        "legend.fontsize": 9,
        "lines.linewidth": 2,
        "lines.markersize": 7,
        "font.size": 10,
    })


def figura(ancho=8, alto=4.6):
    aplicar()
    return plt.subplots(figsize=(ancho, alto))


def etiqueta(ax, x, y, texto, dx=6, dy=0, ha="left", va="center"):
    ax.annotate(texto, (x, y), xytext=(dx, dy), textcoords="offset points",
                ha=ha, va=va, fontsize=9, color=TEXTO)


def _imagen_md(archivo, alt):
    return f"![{alt}]({os.path.relpath(archivo).replace(os.sep, '/')})"


def guardar(fig, archivo, alt):
    fig.savefig(archivo, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return _imagen_md(archivo, alt)


def guardar_gif(fig, moviles, actualizar, cuadros, archivo, alt, fps=12, pausa=2.0, dpi=90):
    fig.set_dpi(dpi)
    for a in moviles:
        a.set_animated(True)
    lienzo = fig.canvas
    lienzo.draw()
    fondo = lienzo.copy_from_bbox(fig.bbox)
    imagenes = []
    for i in range(cuadros):
        lienzo.restore_region(fondo)
        actualizar(i)
        for a in moviles:
            fig.draw_artist(a)
        rgba = Image.frombuffer("RGBA", lienzo.get_width_height(), lienzo.buffer_rgba())
        imagenes.append(rgba.convert("RGB").quantize(colors=128))
    duraciones = [round(1000 / fps)] * (cuadros - 1) + [round(1000 * pausa)]
    imagenes[0].save(archivo, save_all=True, append_images=imagenes[1:],
                     duration=duraciones, loop=0, optimize=True)
    plt.close(fig)
    return _imagen_md(archivo, alt)
