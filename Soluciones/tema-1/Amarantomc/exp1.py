import time
import sys

def mochila_dp(pesos, valores, W):
    """
    Algoritmo clásico de Programación Dinámica O(n*W)
    """
    n = len(pesos)
    
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        w_i = pesos[i - 1]
        v_i = valores[i - 1]
        for w in range(1, W + 1):
            if w_i <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - w_i] + v_i)
            else:
                dp[i][w] = dp[i - 1][w]
                
    return dp[n][W]

def simular_ejercicio_2():
    n = 100 # Número fijo de elementos
    # Generar pesos y valores arbitrarios
    pesos = [(i % 20) + 1 for i in range(n)]
    valores = [(i % 50) + 10 for i in range(n)]
    
    print("=" * 85)
    print(f"{'DEMOSTRACIÓN DE COMPLEJIDAD PSEUDOPOLINOMIAL EN LA MOCHILA O(n W)':^85}")
    print("=" * 85)
    print(f"{'Bits de W (b_W)':<15} | {'Valor W':<12} | {'Tamaño Tabla (n*W)':<20} | {'Tiempo (ms)':<15} | {'Ratio T(b)/T(b-1)':<15}")
    print("-" * 85)

    tiempo_anterior = None

    for bits in range(10, 20): # Incrementamos la cantidad de bits de W de 10 a 25 bits
        W = 2**bits
        
        # Para evitar problemas de memoria en la demo, detenemos la simulación si W sobrepasa los 2^24
        inicio = time.perf_counter()
        res = mochila_dp(pesos, valores, W)
        fin = time.perf_counter()
        
        duracion_ms = (fin - inicio) * 1000
        ratio_str = f"{duracion_ms / tiempo_anterior:.2f}x" if tiempo_anterior and tiempo_anterior > 0 else "N/A"
        tiempo_anterior = duracion_ms
        
        print(f"{bits:<15} | {W:<12,} | {n * W:<20,} | {duracion_ms:<15.3f} | {ratio_str:<15}")

    print("=" * 85)

if __name__ == "__main__":
    # Ajustamos el límite de recursión por seguridad
    sys.setrecursionlimit(2000)
    simular_ejercicio_2()