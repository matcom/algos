import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Configuración de la figura
fig, ax = plt.subplots(figsize=(6, 6))

n = 4
ax.set_xlim(0, n)
ax.set_ylim(0, n)

# Dibujar la cuadrícula (grid)
for x in range(n + 1):
    ax.axhline(x, color='gray', linestyle='-', linewidth=0.8, alpha=0.4)
    ax.axvline(x, color='gray', linestyle='-', linewidth=0.8, alpha=0.4)

# Contenido de las celdas (organizadas desde y=0 en la base hasta y=3 arriba)
matrix_text = [
    ["D0", "+1", "+1", "+1"],  # Fila inferior (y = 0)
    ["-1", "D1", "+1", "+1"],  # Fila 1 (y = 1)
    ["-1", "-1", "D2", "+1"],  # Fila 2 (y = 2)
    ["-1", "-1", "-1", "D3"]   # Fila superior (y = 3)
]

# Coordenadas de los nodos destacados con círculos rojos
red_cells = {(0, 0), (1, 1), (2, 2), (3, 3)}

# Rellenar celdas con texto y círculos
for r in range(n):
    for c in range(n):
        text = matrix_text[r][c]
        x_center = c + 0.5
        y_center = r + 0.5
        
        if (c, r) in red_cells:
            circle = patches.Circle((x_center, y_center), 0.35, color='red', alpha=0.2)
            ax.add_patch(circle)
            ax.text(x_center, y_center, text, color='red', weight='bold', fontsize=12, ha='center', va='center')
        else:
            ax.text(x_center, y_center, text, color='black', fontsize=12, ha='center', va='center')

# Ruta / Trayectoria del adversario en forma de escalera
path_x = [0, 1, 1, 2, 2, 3, 3, 4]
path_y = [3, 3, 2, 2, 1, 1, 0, 0]
ax.plot(path_x, path_y, color='#e74c3c', linewidth=2.5, label='Diagonal del adversario')

# Ajustes de visualización
ax.set_aspect('equal')
ax.axis('off')

# Título / Pie de figura explicativo
caption = "Demostración del Adversario:\nDiagonal Secundaria $D$ de $n$ elementos no consultados."
ax.text(2, -0.6, caption, ha='center', va='top', fontsize=11, family='sans-serif')

plt.tight_layout()
plt.savefig("grafica_adversario.png")