import matplotlib.pyplot as plt

def graficar_analisis_amortizado_contador(m=32):
    """
    Genera un gráfico comparativo del Costo Real, Costo Amortizado
    y la Función de Potencial Phi a lo largo de m incrementos.
    """
    bits = [0]
    costos_reales = []
    potenciales = [0]  # Phi_0 = 0
    costos_amortizados = []
    
    for i in range(1, m + 1):
        costo_real = 0
        idx = 0
        while idx < len(bits) and bits[idx] == 1:
            bits[idx] = 0
            costo_real += 1
            idx += 1
        
        if idx < len(bits):
            bits[idx] = 1
            costo_real += 1
        else:
            bits.append(1)
            costo_real += 1
            
        costos_reales.append(costo_real)
        potencial_actual = sum(bits)
        
        # Amortizado = c_i + Phi_i - Phi_{i-1}
        amortizado = costo_real + potencial_actual - potenciales[-1]
        costos_amortizados.append(amortizado)
        potenciales.append(potencial_actual)

    operaciones = list(range(1, m + 1))
    potenciales_ops = potenciales[1:]  # Tomar Phi_1 a Phi_m

    # Configuración de la figura
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Gráfico de barras: Costo Real
    bars = ax1.bar(operaciones, costos_reales, color='#3498db', alpha=0.6, width=0.6, label='Costo Real ($c_i$)')
    # Gráfico de línea: Costo Amortizado
    line_amort = ax1.plot(operaciones, costos_amortizados, color='#e74c3c', linewidth=2.5, linestyle='--', label=r'Costo Amortizado ($\hat{c}_i = 2$)')
    
    ax1.set_xlabel('Número de Operación ($i$)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Costo (pasos / flips de bit)', fontsize=12, color='#2c3e50', fontweight='bold')
    ax1.set_xticks(operaciones)
    ax1.grid(True, linestyle=':', alpha=0.6)

    # Segundo eje Y: Potencial Phi
    ax2 = ax1.twinx()
    line_pot = ax2.plot(operaciones, potenciales_ops, color='#2ecc71', linewidth=2, marker='o', markersize=4, label=r'Potencial ($\Phi_i = \text{bits } 1$)')
    ax2.set_ylabel(r'Potencial ($\Phi_i$)', fontsize=12, color='#27ae60', fontweight='bold')

    # Ajustes visuales de leyenda y título
    lines = [bars] + line_amort + line_pot
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left', frameon=True, facecolor='#ffffff', edgecolor='#bdc3c7')

    plt.title('Análisis Amortizado del Contador Binario (Método del Potencial)', fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig('grafica_analisis_amortizado.png', dpi=300)

# Generar el gráfico para 32 operaciones
graficar_analisis_amortizado_contador(32)