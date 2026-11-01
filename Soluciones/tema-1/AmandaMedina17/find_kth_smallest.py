def find_kth_smallest(array_a, array_b, k):
    """
    Encuentra el k-ésimo elemento menor entre dos arreglos ordenados 
     utilizando descarte de mitades inferiores.
    """
    lo_a, hi_a = 0, len(array_a) - 1
    lo_b, hi_b = 0, len(array_b) - 1
    
    while True:
        # Caso base 1: Si el arreglo A se quedó sin elementos activos
        if lo_a > hi_a:
            return array_b[lo_b + k - 1]
            
        # Caso base 2: Si el arreglo B se quedó sin elementos activos
        if lo_b > hi_b:
            return array_a[lo_a + k - 1]
            
        # Caso base 3: Si buscamos el primer elemento absoluto (k = 1)
        if k == 1:
            return min(array_a[lo_a], array_b[lo_b])
            
        # Tomamos la mitad de k para comparar posiciones medias
        half = k // 2
        
        # Calculamos los índices medios dentro de los límites activos
        mid_a = min(lo_a + half - 1, hi_a)
        mid_b = min(lo_b + half - 1, hi_b)
        
        # Comparamos los valores medios y descartamos la mitad inferior correspondiente
        if array_a[mid_a] < array_b[mid_b]:
            # Descartamos la mitad inferior de array_a
            elements_discarded = mid_a - lo_a + 1
            k -= elements_discarded
            lo_a = mid_a + 1
        else:
            # Descartamos la mitad inferior de array_b
            elements_discarded = mid_b - lo_b + 1
            k -= elements_discarded
            lo_b = mid_b + 1

if __name__ == "__main__":
    A = [3, 7, 12, 18, 25]
    B = [5, 10, 15, 20, 30]
    n = len(A)
    
    # Para encontrar la mediana (el n-ésimo menor elemento, es decir, k = 5)
    median = find_kth_smallest(A, B, k=n)
    print(f"La mediana (5° elemento menor) es: {median}")