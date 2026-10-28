import math
import pandas as pd

def contar_comparaciones_busqueda_binaria(n, hueco_objetivo):
    """
    Simula la búsqueda binaria sobre n elementos para caer en un hueco específico.
    A es conceptualmente [0, 1, ..., n-1]
    Hueco k representa buscar un valor x tal que k-1 < x < k
    """
    lo = 0
    hi = n
    comparaciones = 0
    
    # Creamos un valor float ficticio para caer en el hueco deseado
    x = hueco_objetivo - 0.5 
    
    while lo < hi:
        mid = (lo + hi) // 2
        comparaciones += 1
        if mid == x: # Imposible por ser float vs int
            return comparaciones
        elif x < mid:
            hi = mid
        else:
            lo = mid + 1
            
    return comparaciones

def generar_tabla_optimalidad():
    resultados = []
    tamanios = [1, 3, 7, 15, 31, 63, 100, 1000]
    
    for n in tamanios:
        cota_teorica = math.ceil(math.log2(n + 1))
        
        # Probar todos los huecos posibles para hallar el peor caso
        peor_caso_real = 0
        for hueco in range(n + 1):
            comps = contar_comparaciones_busqueda_binaria(n, hueco)
            peor_caso_real = max(peor_caso_real, comps)
            
        resultados.append({
            "n (Elementos)": n,
            "Huecos (n+1)": n + 1,
            "Cota Teórica ceil(log2(n+1))": cota_teorica,
            "Peor Caso Búsqueda Binaria": peor_caso_real,
            "¿Es Óptimo?": "SÍ (Alcanza Cota)" if peor_caso_real == cota_teorica else "NO"
        })
        
    df = pd.DataFrame(resultados)
    return df

print("="*80)
print("TABLA DE COMPARACIÓN: COTA TEÓRICA DE INFORMACIÓN VS BÚSQUEDA BINARIA")
print("="*80)
df_resultado = generar_tabla_optimalidad()
print(df_resultado.to_string(index=False))