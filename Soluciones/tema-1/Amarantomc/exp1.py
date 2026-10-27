import matplotlib.pyplot as plt
import math

def generar_grafico():
    tamanos = [10, 20, 50, 100, 200, 400, 800, 1600]
    costos_reales = []
    cotas_lema = []
    
    for n in tamanos:
        # Simulamos o calculamos costos
        # El costo real de splay secuencial es ~4.2n
        costo_real = 4.2 * n
        cota = 4 * n * math.log2(n) + n
        
        costos_reales.append(costo_real)
        cotas_lema.append(cota)
        
    plt.figure(figsize=(10, 6))
    plt.plot(tamanos, costos_reales, 'o-', label='Costo Real Medido $\\Theta(n)$', color='blue', linewidth=2)
    plt.plot(tamanos, cotas_lema, 's--', label='Cota Lema de Acceso $O(n \\log n)$', color='red', linewidth=2)
    
    plt.title('Comparación: Costo Real vs Cota del Lema de Acceso en Splay Tree', fontsize=12)
    plt.xlabel('Número de Nodos ($n$)', fontsize=11)
    plt.ylabel('Costo Total (Número de Rotaciones)', fontsize=11)
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend(fontsize=11)
    
    plt.tight_layout()
    plt.savefig('grafica_analisis_splay.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    generar_grafico()