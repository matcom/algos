"""
Visualización del algoritmo de Floyd (tortuga y liebre).
Genera:
  floyd_con_ciclo.gif / .png   (cola mu=3, ciclo lambda=5)
  floyd_sin_ciclo.gif / .png   (lista de n=7 nodos)
Requiere:  pip install pillow
Uso:       python3 floyd_gif.py
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 960, 560
BG = (250, 250, 247)
INK = (40, 40, 40)
GREEN = (34, 139, 84)     # tortuga
ORANGE = (230, 120, 20)   # liebre
RED = (200, 40, 40)
GRAY = (150, 150, 150)
NODE_R = 20


def font(size, bold=False):
    names = ["DejaVuSans-Bold.ttf", "DejaVuSans.ttf"] if bold else ["DejaVuSans.ttf"]
    for n in names:
        for base in ("", "/usr/share/fonts/truetype/dejavu/"):
            try:
                return ImageFont.truetype(base + n, size)
            except OSError:
                pass
    return ImageFont.load_default()


F_S, F_M, F_L = font(15), font(18), font(22, True)


# ---------------------------------------------------------------- dibujo base
def arrow(d, p, q, color=INK, r=NODE_R):
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    a = (p[0] + ux * r, p[1] + uy * r)
    b = (q[0] - ux * (r + 2), q[1] - uy * (r + 2))
    d.line([a, b], fill=color, width=2)
    hx, hy = -uy, ux
    tip = b
    base = (b[0] - ux * 10, b[1] - uy * 10)
    d.polygon([tip, (base[0] + hx * 5, base[1] + hy * 5),
               (base[0] - hx * 5, base[1] - hy * 5)], fill=color)


def node(d, c, label, fill=(255, 255, 255), outline=INK):
    d.ellipse([c[0] - NODE_R, c[1] - NODE_R, c[0] + NODE_R, c[1] + NODE_R],
              fill=fill, outline=outline, width=2)
    d.text(c, str(label), font=F_M, fill=INK, anchor="mm")


def markers(d, c, has_t, has_l, meet):
    if meet:
        d.ellipse([c[0] - NODE_R, c[1] - NODE_R, c[0] + NODE_R, c[1] + NODE_R],
                  fill=(255, 220, 220), outline=RED, width=3)
    if has_t:
        r = NODE_R + 6
        d.ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], outline=GREEN, width=4)
        d.text((c[0] - 34, c[1] - 34), "T", font=F_L, fill=GREEN, anchor="mm")
    if has_l:
        r = NODE_R + 12
        d.ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], outline=ORANGE, width=4)
        d.text((c[0] + 34, c[1] - 34), "L", font=F_L, fill=ORANGE, anchor="mm")


def legend(d, title):
    d.text((24, 18), title, font=F_L, fill=INK)
    d.ellipse([24, 56, 40, 72], outline=GREEN, width=4)
    d.text((48, 64), "T = tortuga (1 paso)", font=F_S, fill=INK, anchor="lm")
    d.ellipse([230, 56, 246, 72], outline=ORANGE, width=4)
    d.text((254, 64), "L = liebre (2 pasos)", font=F_S, fill=INK, anchor="lm")


def panel(d, lines, color=INK, last=None):
    d.rounded_rectangle([20, 380, W - 20, H - 20], radius=12, fill=(240, 240, 235),
                        outline=GRAY)
    y = 396
    for ln in lines:
        d.text((40, y), ln, font=F_M, fill=color)
        y += 30
    if last:
        d.text((40, y + 6), last[0], font=F_L, fill=last[1])


# ---------------------------------------------------------------- caso con ciclo
def caso_con_ciclo(mu=3, lam=5):
    n = mu + lam
    center, R = (640, 215), 125
    coords = {}
    for i in range(mu):
        coords[i] = (180 + 105 * i, 215)
    for j in range(lam):
        th = math.pi + j * 2 * math.pi / lam
        coords[mu + j] = (center[0] + R * math.cos(th), center[1] + R * math.sin(th))

    def node_of(i):                      # a_i -> índice de nodo
        return i if i < mu else mu + (i - mu) % lam

    kstar = lam * max(1, math.ceil(mu / lam))
    frames, durs = [], []

    def frame(k, final=False):
        im = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(im)
        legend(d, f"Floyd con ciclo  (cola μ={mu}, ciclo λ={lam})")
        for i in range(n - 1):
            arrow(d, coords[i], coords[i + 1])
        arrow(d, coords[n - 1], coords[mu])
        d.text((coords[0][0], coords[0][1] + 38), "h", font=F_M, fill=GRAY, anchor="mm")
        t, l = node_of(k), node_of(2 * k)
        for i in range(n):
            node(d, coords[i], f"a{i}")
        for i in range(n):
            markers(d, coords[i], i == t, i == l, final and i == t)
        lines = [
            f"Iteración k = {k}",
            f"Invariante:  t = a_{k},  l = a_{2*k}   →  ventaja de la liebre = k = {k}",
            (f"Dentro del ciclo: D = k mod λ = {k % lam}   (distancia T→L)"
             if k >= mu else "La tortuga aún está en la cola (D no definida)"),
            f"Potencial  Ψ = k* − k = {kstar} − {k} = {kstar - k}   (k* = {kstar})",
        ]
        if final:
            panel(d, lines, last=(f"t = l = a_{k} → ¡HAY CICLO!  (se encuentran en k* = {k})", RED))
        else:
            panel(d, lines)
        return im

    k = 0
    frames.append(frame(0)); durs.append(1500)
    while True:
        k += 1
        if node_of(k) == node_of(2 * k):
            frames.append(frame(k, final=True)); durs.append(3500)
            break
        frames.append(frame(k)); durs.append(1300)
    return frames, durs


# ---------------------------------------------------------------- caso sin ciclo
def caso_sin_ciclo(n=7):
    coords = {i: (80 + 110 * i, 215) for i in range(n + 1)}   # índice n = nil

    def node_of(i):
        return min(i, n)

    frames, durs = [], []

    def frame(k, final=False):
        im = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(im)
        legend(d, f"Floyd sin ciclo  (n = {n} nodos)")
        for i in range(n):
            arrow(d, coords[i], coords[i + 1], r=NODE_R if i + 1 < n else NODE_R)
        for i in range(n):
            node(d, coords[i], f"a{i}")
        c = coords[n]
        d.rectangle([c[0] - 24, c[1] - 18, c[0] + 24, c[1] + 18], outline=GRAY, width=2)
        d.text(c, "nil", font=F_M, fill=GRAY, anchor="mm")
        d.text((coords[0][0], coords[0][1] + 38), "h", font=F_M, fill=GRAY, anchor="mm")
        t, l = node_of(k), node_of(2 * k)
        for i in range(n + 1):
            markers(d, coords[i], i == t, i == l, False)
        lines = [
            f"Iteración k = {k}",
            f"Invariante:  t = a_{k},  l = a_{min(2*k, n)}   →  ventaja = k = {k}",
            f"Potencial  Φ = n − 2k = {n} − {2*k} = {n - 2*k}   (el bucle sigue mientras Φ ≥ 2)",
        ]
        if final:
            panel(d, lines, last=("l.next = nil → la guarda falla → NO hay ciclo (FALSO)", GREEN))
        else:
            panel(d, lines)
        return im

    k = 0
    frames.append(frame(0)); durs.append(1500)
    while 2 * k + 1 <= n - 1:            # guarda: l ≠ nil y l.next ≠ nil
        k += 1
        # tras avanzar, ¿la liebre sigue pudiendo moverse?
        last = not (2 * k + 1 <= n - 1)
        frames.append(frame(k, final=last)); durs.append(3500 if last else 1300)
    return frames, durs


def guardar(nombre, frames, durs):
    frames[0].save(nombre + ".gif", save_all=True, append_images=frames[1:],
                   duration=durs, loop=0, optimize=True)
    frames[-1].save(nombre + ".png")
    print("generado:", nombre + ".gif", nombre + ".png", f"({len(frames)} cuadros)")


if __name__ == "__main__":
    guardar("floyd_con_ciclo", *caso_con_ciclo())
    guardar("floyd_sin_ciclo", *caso_sin_ciclo())