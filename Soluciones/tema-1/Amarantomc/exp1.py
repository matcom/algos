import math

def resolver_mayor_n(costo_fn, presupuesto):
    """
    Encuentra el mayor n tal que costo_fn(n) <= presupuesto
    utilizando Búsqueda Binaria sobre el espacio de enteros.
    """
    alto = 2
    while costo_fn(alto) <= presupuesto:
        alto *= 2
    
    bajo = alto // 2
    while bajo + 1 < alto:
        medio = (bajo + alto) // 2
        if costo_fn(medio) <= presupuesto:
            bajo = medio
        else:
            alto = medio
    return bajo

def simular_ejercicio_1():
    
    ops_por_segundo = 10**9
    segundos_hora = 3600
    presupuesto_base = ops_por_segundo * segundos_hora 
    
    factores_mult = [1, 10, 1000]
    
    costos = {
        "n": lambda n: n,
        "n log2 n": lambda n: n * math.log2(n),
        "n^2": lambda n: n**2,
        "n^3": lambda n: n**3,
        "2^n": lambda n: 2**n if n < 1024 else float('inf')
    }

    print("=" * 80)
    print(f"{'TABLA DE CAPACIDAD DE ENTRADA Y FACTORES DE CRECIMIENTO (1 Hora)':^80}")
    print("=" * 80)
    print(f"{'Costo':<12} | {'Actual (1x)':<14} | {'10x Speed':<14} | {'1000x Speed':<14} | {'Factor (1000x/1x)':<18}")
    print("-" * 80)

    for nombre, fn in costos.items():
        n_actual = resolver_mayor_n(fn, presupuesto_base * 1)
        n_10x = resolver_mayor_n(fn, presupuesto_base * 10)
        n_1000x = resolver_mayor_n(fn, presupuesto_base * 1000)
        
        if nombre == "2^n":
            factor_str = f"+{n_1000x - n_actual} (aditivo)"
        else:
            factor = n_1000x / n_actual
            factor_str = f"{factor:>15.2f}x"
            
        print(f"{nombre:<12} | {n_actual:>14.3g} | {n_10x:>14.3g} | {n_1000x:>14.3g} | {factor_str}")

    print("=" * 80)

if __name__ == "__main__":
    simular_ejercicio_1()