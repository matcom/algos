import matplotlib.pyplot as plt
import numpy as np

def dibujar_grid_1d():
    fig, ax = plt.subplots(figsize=(10, 3))
    
    r = 1.0 # lado del intervalo
    # Dibujar divisiones de celdas
    for c in range(-3, 4):
        ax.axvline(x=c*r, color='gray', linestyle='--', alpha=0.7)
        ax.text(c*r + 0.4*r, 0.6, f'Celda {c}', fontsize=9)

    # Resaltar las 5 celdas inspeccionadas para un punto en Celda 0
    ax.axvspan(-2*r, 3*r, color='green', alpha=0.15, label='Bloque de 5 Celdas Inspeccionadas (c-2 a c+2)')
    
    # Dibujar punto nuevo p
    p_x = 0.3 * r
    ax.scatter([p_x], [0.2], color='red', s=120, zorder=5, label='Punto Nuevo (p)')
    
    ax.set_xlim(-3.5*r, 4.5*r)
    ax.set_ylim(0, 1)
    ax.get_yaxis().set_visible(False)
    ax.set_xlabel('Recta Real 1D (Intervalos de tamaño r = δ/2)')
    ax.set_title('Estructura del Grid 1D y Rango de Búsqueda de Vecinos')
    ax.legend(loc='upper right')
    
    plt.tight_layout()
    plt.savefig('grid_1d_ilustracion.png', dpi=300)
    

if __name__ == "__main__":
    dibujar_grid_1d()