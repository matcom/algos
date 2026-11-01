import os
import platform
from PIL import Image, ImageDraw, ImageFont

# Carpeta de salida: la misma donde está este script
OUT = os.path.dirname(os.path.abspath(__file__))

W, H = 960, 600

# Detección automática de fuentes según el sistema operativo (Windows / Linux)
if platform.system() == "Windows":
  FD = "C:/Windows/Fonts/"
  F_TITLE = ImageFont.truetype(FD + "arialbd.ttf", 26)
  F_BIG = ImageFont.truetype(FD + "arialbd.ttf", 22)
  F_VAL = ImageFont.truetype(FD + "arialbd.ttf", 22)
  F_M = ImageFont.truetype(FD + "consola.ttf", 16)
  F_TXT = ImageFont.truetype(FD + "arial.ttf", 17)
  F_TXT_B = ImageFont.truetype(FD + "arialbd.ttf", 17)
  F_SMALL = ImageFont.truetype(FD + "arial.ttf", 14)
  F_HUGE = ImageFont.truetype(FD + "arialbd.ttf", 36)
else:
  FD = "/usr/share/fonts/truetype/dejavu/"
  F_TITLE = ImageFont.truetype(FD + "DejaVuSans-Bold.ttf", 26)
  F_BIG = ImageFont.truetype(FD + "DejaVuSans-Bold.ttf", 22)
  F_VAL = ImageFont.truetype(FD + "DejaVuSans-Bold.ttf", 22)
  F_M = ImageFont.truetype(FD + "DejaVuSansMono.ttf", 16)
  F_TXT = ImageFont.truetype(FD + "DejaVuSans.ttf", 17)
  F_TXT_B = ImageFont.truetype(FD + "DejaVuSans-Bold.ttf", 17)
  F_SMALL = ImageFont.truetype(FD + "DejaVuSans.ttf", 14)
  F_HUGE = ImageFont.truetype(FD + "DejaVuSans-Bold.ttf", 36)

BG = (250, 249, 245)
INK = (35, 35, 40)
MUTED = (120, 120, 128)
BOX = (232, 236, 244)
BOX_EDGE = (150, 160, 185)
ACCENT = (217, 119, 87)  # naranja: cima / operacion
GOOD = (46, 139, 110)  # verde: minimo
GOOD_BG = (222, 241, 233)

BOX_W, BOX_H, GAP = 260, 52, 10
STACK_X = 60
BASE_Y = H - 50


def box_y(i):
  return BASE_Y - (i + 1) * BOX_H - i * GAP


def draw_node(d, y, val, m, top=False, ghost=0.0):
  x0, x1 = STACK_X, STACK_X + BOX_W
  fill = BOX
  edge = ACCENT if top else BOX_EDGE
  d.rounded_rectangle(
      [x0, y, x1, y + BOX_H], 10, fill=fill, outline=edge, width=3 if top else 2
  )
  d.text((x0 + 16, y + BOX_H // 2), f"val = {val}", font=F_VAL, fill=INK, anchor="lm")
  d.text((x1 - 16, y + BOX_H // 2), f"m = {m}", font=F_M, fill=GOOD, anchor="rm")


def frame(
    stack, title, line1, line2, min_txt, drop=None, leaving=None, show_arrow=False
):
  img = Image.new("RGB", (W, H), BG)
  d = ImageDraw.Draw(img)

  d.text((40, 32), "Pila con mínimo en O(1)", font=F_TITLE, fill=INK, anchor="lm")
  d.text(
      (40, 62),
      "cada nodo guarda m = mínimo desde la base hasta él",
      font=F_SMALL,
      fill=MUTED,
      anchor="lm",
  )

  # suelo
  d.line(
      [STACK_X - 20, BASE_Y + 6, STACK_X + BOX_W + 20, BASE_Y + 6],
      fill=INK,
      width=4,
  )
  d.text(
      (STACK_X + BOX_W // 2, BASE_Y + 24),
      "base",
      font=F_SMALL,
      fill=MUTED,
      anchor="mm",
  )

  n = len(stack)
  for i, (v, m) in enumerate(stack):
    is_top = (i == n - 1) and drop is None
    draw_node(d, box_y(i), v, m, top=is_top)
  if drop:
    v, m, t = drop
    y_final = box_y(n)
    y = y_final - (1 - t) * 140
    draw_node(d, y, v, m, top=True)
  if leaving:
    v, m, t = leaving
    y = box_y(n) - t * 80
    draw_node(d, y, v, m, top=True, ghost=min(1.0, t / 1.2))

  if n > 0 and drop is None:
    yc = box_y(n - 1) + BOX_H // 2
    d.text((STACK_X + BOX_W + 12, yc), "◀ cima", font=F_TXT_B, fill=ACCENT, anchor="lm")

  # panel derecho
  px = 360
  d.rounded_rectangle(
      [px, 100, W - 30, 240], 14, fill=(255, 255, 255), outline=BOX_EDGE, width=2
  )
  d.text((px + 20, 130), "Operación", font=F_SMALL, fill=MUTED, anchor="lm")
  d.text((px + 20, 164), title, font=F_BIG, fill=ACCENT, anchor="lm")
  d.text((px + 20, 198), line1, font=F_TXT, fill=INK, anchor="lm")
  d.text((px + 20, 222), line2, font=F_SMALL, fill=MUTED, anchor="lm") if line2 else None

  d.rounded_rectangle(
      [px, 255, W - 30, 430], 14, fill=GOOD_BG, outline=GOOD, width=3
  )
  d.text((px + 20, 285), "min()  =  cima.m", font=F_TXT_B, fill=GOOD, anchor="lm")
  d.text(((px + W - 30) // 2, 355), str(min_txt), font=F_HUGE, fill=GOOD, anchor="mm")
  d.text(
      ((px + W - 30) // 2, 405),
      "lectura directa en O(1)",
      font=F_SMALL,
      fill=GOOD,
      anchor="mm",
  )

  d.text(
      (px, 460),
      "INV: mᵢ = min(a₁, …, aᵢ) para todo nodo i",
      font=F_TXT_B,
      fill=INK,
      anchor="lm",
  )
  d.text(
      (px, 490),
      "push / pop solo operan en el extremo superior,",
      font=F_SMALL,
      fill=MUTED,
      anchor="lm",
  )
  d.text(
      (px, 514),
      "por lo que los prefijos inferiores nunca cambian.",
      font=F_SMALL,
      fill=MUTED,
      anchor="lm",
  )

  if show_arrow and n > 0:
    d.rounded_rectangle(
        [STACK_X - 6, box_y(n - 1) - 6, STACK_X + BOX_W + 6, box_y(n - 1) + BOX_H + 6],
        14,
        outline=GOOD,
        width=4,
    )
  return img


def simular(ops):
  frames, durs = [], []
  stack = []

  def add(img, ms):
    frames.append(img)
    durs.append(ms)

  add(frame([], "pila vacía", "n = 0", "", "–"), 1200)

  for op in ops:
    if op[0] == "push":
      x = op[1]
      if stack:
        m_prev = stack[-1][1]
        m = min(x, m_prev)
        l1 = f"push({x})"
        l2 = f"m = min({x}, {m_prev}) = {m}"
      else:
        m = x
        l1 = f"push({x})"
        l2 = f"pila vacía → m = {x}"
      mn_before = stack[-1][1] if stack else "–"
      for k in range(1, 7):
        t = k / 6
        add(frame(stack, f"push({x})", l2, "", mn_before, drop=(x, m, t)), 70)
      stack.append((x, m))
      add(frame(stack, f"push({x})", l2, "", m, show_arrow=False), 1500)
    else:
      x, m = stack[-1]
      for k in range(1, 7):
        t = k / 6
        add(
            frame(
                stack[:-1],
                f"pop() → {x}",
                "se quita el nodo de la cima",
                "",
                m,
                leaving=(x, m, t),
            ),
            70,
        )
      stack.pop()
      if stack:
        l2 = f"el mínimo {stack[-1][1]} ya estaba guardado: no se calcula"
        add(
            frame(
                stack,
                f"pop() → {x}",
                f"min() vuelve a {stack[-1][1]}",
                l2,
                stack[-1][1],
                show_arrow=True,
            ),
            1900,
        )
      else:
        add(frame(stack, f"pop() → {x}", "la pila quedó vacía", "", "–"), 1500)
  return frames, durs


# --- NUEVA IMAGEN EXPLICATIVA DEL SISTEMA (Reemplaza al PNG simple) ---
def crear_imagen_explicativa():
  img = Image.new("RGB", (W, H), BG)
  d = ImageDraw.Draw(img)

  # Título principal
  d.text(
      (40, 36),
      "Anatomía de la Pila con Mínimo en O(1)",
      font=F_TITLE,
      fill=INK,
      anchor="lm",
  )
  d.text(
      (40, 68),
      "Diseño de la estructura, nodos y mantenimiento del invariante",
      font=F_SMALL,
      fill=MUTED,
      anchor="lm",
  )

  # --- COLUMNA IZQUIERDA: Ejemplo visual de pila con 4 elementos ---
  stack_ej = [(5, 5), (3, 3), (8, 3), (2, 2)]
  for i, (v, m) in enumerate(stack_ej):
    y = box_y(i)
    is_top = i == len(stack_ej) - 1
    draw_node(d, y, v, m, top=is_top)

  # Suelo y etiquetas de la pila
  d.line(
      [STACK_X - 20, BASE_Y + 6, STACK_X + BOX_W + 20, BASE_Y + 6],
      fill=INK,
      width=4,
  )
  d.text(
      (STACK_X + BOX_W // 2, BASE_Y + 24),
      "base de la pila",
      font=F_SMALL,
      fill=MUTED,
      anchor="mm",
  )
  yc = box_y(len(stack_ej) - 1) + BOX_H // 2
  d.text((STACK_X + BOX_W + 12, yc), "◀ cima (min = 2)", font=F_TXT_B, fill=ACCENT, anchor="lm")

  # --- COLUMNA DERECHA: Tarjetas explicativas ---
  px = 370

  # Tarjeta 1: Anatomía del Nodo
  d.rounded_rectangle(
      [px, 105, W - 30, 260], 14, fill=(255, 255, 255), outline=BOX_EDGE, width=2
  )
  d.text((px + 20, 135), "1. Estructura de cada Nodo", font=F_BIG, fill=ACCENT, anchor="lm")
  d.text((px + 20, 172), "• val: el valor insertado (ej. 8)", font=F_TXT, fill=INK, anchor="lm")
  d.text((px + 20, 202), "• m: mínimo desde la base hasta este nodo", font=F_TXT, fill=INK, anchor="lm")
  d.text((px + 20, 232), "  → Nodo = ⟨val: T, m: T, sig: Nodo*⟩", font=F_SMALL, fill=MUTED, anchor="lm")

  # Tarjeta 2: El Invariante y Eficiencia
  d.rounded_rectangle(
      [px, 280, W - 30, 520], 14, fill=GOOD_BG, outline=GOOD, width=3
  )
  d.text((px + 20, 315), "2. El Invariante y Operación min()", font=F_BIG, fill=GOOD, anchor="lm")
  d.text(
      (px + 20, 355),
      "INV(P): mᵢ = min(a₁, a₂, …, aᵢ) para todo nodo i.",
      font=F_TXT_B,
      fill=GOOD,
      anchor="lm",
  )
  d.text((px + 20, 395), "• push(x): calcula m = min(x, cima.m) en O(1).", font=F_TXT, fill=INK, anchor="lm")
  d.text((px + 20, 425), "• pop(): al quitar la cima, los prefijos inferiores", font=F_TXT, fill=INK, anchor="lm")
  d.text((px + 20, 450), "  no cambian. El mínimo anterior ya está escrito.", font=F_TXT, fill=INK, anchor="lm")
  d.text((px + 20, 485), "⇒ min() solo lee cima.m en Θ(1) sin recorrer nada.", font=F_TXT_B, fill=GOOD, anchor="lm")

  return img


# --- Ejecución principal ---
ops = [
    ("push", 5),
    ("push", 3),
    ("push", 8),
    ("push", 2),
    ("pop",),
    ("pop",),
    ("push", 1),
    ("pop",),
    ("pop",),
    ("pop",),
]

# 1. Generar GIF animado
frames, durs = simular(ops)
frames[0].save(
    os.path.join(OUT, "pila_min.gif"),
    save_all=True,
    append_images=frames[1:],
    duration=durs,
    loop=0,
    optimize=True,
    disposal=2,
)

# 2. Generar PNG explicativo del sistema
crear_imagen_explicativa().save(os.path.join(OUT, "pila_min_explicacion.png"))

print("¡Archivos generados exitosamente en la carpeta del script!")
print(f" - GIF: {os.path.join(OUT, 'pila_min.gif')}")
print(f" - PNG Explicativo: {os.path.join(OUT, 'pila_min_explicacion.png')}")