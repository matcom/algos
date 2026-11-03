"""Renderiza las animaciones y deja en esta carpeta un MP4 y un GIF por escena, con el
nombre ejercicio-NN-<nombre>, que es como los citan los .md.

    uv run --python 3.13 --with manim python renderizar.py            # todas
    uv run --python 3.13 --with manim python renderizar.py 02 05      # solo algunas

El MP4 sale en calidad media (720p, 30 cuadros por segundo), para la exposición. El
GIF sale del MP4 con ffmpeg, a 640 px de ancho y 15 cuadros por segundo, para verlo
dentro de los .md en GitHub. Si no hay ffmpeg, se usa el GIF que genera manim.
"""

import shutil
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent

# ejercicio -> [(escena, nombre del archivo)], en el orden en que aparecen en el .md
ESCENAS = {
    "01": [("Factor", "factor")],
    "02": [("Invariante", "invariante"), ("Bits", "bits"), ("Testigo", "testigo"),
           ("Estancada", "estancada")],
    "03": [("Paralela", "paralela"), ("Repetidos", "repetidos")],
    "04": [("Monedas", "monedas"), ("Cabezal", "cabezal")],
    "05": [("Invariante", "invariante"), ("Potencial", "potencial"),
           ("EntradaAlCiclo", "entrada")],
    "06": [("Escalera", "escalera"), ("Adversario", "adversario")],
    "07": [("Corte", "corte"), ("Centinela", "centinela")],
    "08": [("Trios", "trios"), ("OrdenMalo", "orden-malo")],
    "09": [("Intercambio", "intercambio"), ("Optimizada", "optimizada")],
    "10": [("Rejilla", "rejilla"), ("HaciaAtras", "hacia-atras"),
           ("OrdenAdversario", "orden-adversario")],
    "11": [("Fila", "fila"), ("Bits", "bits")],
    "12": [("Propuestas", "propuestas"), ("Verificador", "verificador")],
    "13": [("PrimerAcceso", "primer-acceso"), ("VuelveAlCamino", "vuelve-al-camino")],
    "14": [("PrimerSi", "primer-si"), ("Adversario", "adversario"),
           ("ReferenciaCero", "referencia-cero")],
}


def manim(*args):
    subprocess.run([sys.executable, "-m", "manim", *args], cwd=AQUI, check=True)


def renderizar(nn, escena, nombre):
    fuente = f"ejercicio-{nn}.py"
    manim("-qm", "--disable_caching", fuente, escena)
    mp4 = AQUI / "media" / "videos" / f"ejercicio-{nn}" / "720p30" / f"{escena}.mp4"
    destino_mp4 = AQUI / f"ejercicio-{nn}-{nombre}.mp4"
    shutil.copyfile(mp4, destino_mp4)
    destino_gif = AQUI / f"ejercicio-{nn}-{nombre}.gif"
    if shutil.which("ffmpeg"):
        filtro = ("fps=15,scale=640:-1:flags=lanczos,split[a][b];"
                  "[a]palettegen=max_colors=64[p];[b][p]paletteuse=dither=none")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(destino_mp4),
                        "-vf", filtro, str(destino_gif)], check=True)
    else:
        manim("-ql", "--disable_caching", "--format", "gif", fuente, escena)
        gif = AQUI / "media" / "videos" / f"ejercicio-{nn}" / "480p15" / f"{escena}.gif"
        shutil.copyfile(gif, destino_gif)
    for archivo in (destino_mp4, destino_gif):
        print(f"{archivo.name}: {archivo.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    pedidos = sys.argv[1:] or list(ESCENAS)
    for nn in pedidos:
        for escena, nombre in ESCENAS[nn]:
            renderizar(nn, escena, nombre)
