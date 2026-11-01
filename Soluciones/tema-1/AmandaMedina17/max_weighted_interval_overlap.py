class EventType:
    # Asignamos valores numéricos para garantizar la regla de desempate:
    # INICIO (0) se procesa ANTES que FIN (1) si coinciden en la misma coordenada 'x'.
    START = 0
    END = 1

class Event:
    def __init__(self, x, event_type, weight):
        self.x = x
        self.event_type = event_type
        self.weight = weight

    # Definición de la relación de orden total (<=_E) para la función sort()
    def __lt__(self, other):
        if self.x != other.x:
            return self.x < other.x
        # Si las coordenadas 'x' son iguales, el evento START va primero
        return self.event_type < other.event_type

def max_weighted_interval_overlap(intervals):
    """
    Calcula la intersección máxima de un conjunto de intervalos con peso.
    
    Parámetros:
        intervals: Lista de tuplas o listas con formato (l_i, r_i, w_i)
                   donde l_i <= r_i y w_i > 0.
                   
    Retorna:
        Una tupla (W_max, x_opt) con el peso máximo acumulado y la coordenada
        del punto donde se alcanza dicho máximo.
    """
    events = []
    
    # 1. Construcción de la lista discreta de 2n eventos
    for l, r, w in intervals:
        events.append(Event(l, EventType.START, w))
        events.append(Event(r, EventType.END, w))
    
    # 2. Ordenamiento de eventos en O(n log n) mediante la regla anti-ambigüedad
    events.sort()
    
    # 3. Inicialización de variables de estado del barrido
    current_weight = 0.0
    max_weight = 0.0
    x_opt = float('-inf')
    
    # 4. Simulación de la línea de barrido lineal O(n)
    for event in events:
        if event.event_type == EventType.START:
            current_weight += event.weight
        else: # EventType.END
            current_weight -= event.weight
            
        # Actualización del récord y registro del punto testigo
        if current_weight > max_weight:
            max_weight = current_weight
            x_opt = event.x
            
    return max_weight, x_opt


# ==========================================
# Ejemplo de Ejecución y Pruebas
# ==========================================
if __name__ == "__main__":
    # Formato de entrada: [l_i, r_i, w_i]
    intervalos_prueba = [
        (1.5, 4.0, 2.5),  # Intervalo 1: [1.5, 4.0] con peso 2.5
        (2.0, 6.0, 3.0),  # Intervalo 2: [2.0, 6.0] con peso 3.0
        (3.5, 7.0, 1.5),  # Intervalo 3: [3.5, 7.0] con peso 1.5
        (4.0, 5.0, 4.0)   # Intervalo 4: [4.0, 5.0] con peso 4.0 (coincide en x=4.0)
    ]
    
    max_w, x_best = max_weighted_interval_overlap(intervalos_prueba)
    
    print(f"--- Resultado del Algoritmo ---")
    print(f"Peso Máximo Acumulado (W_max): {max_w}")
    print(f"Coordenada Óptima (x_opt):     {x_best}")