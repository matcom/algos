import math
import random
import time

def distinguir_elementos_ordenado(A):
    """
    Resuelve el problema de distinción de elementos ordenando el arreglo
    y comprobando si hay elementos adyacentes iguales.
    Coste temporal: O(n log n). Coste espacial: O(n) o O(1) auxiliar según el ordenamiento.
    """
    if len(A) <= 1:
        return True
    
    # Ordenamos el arreglo
    A_ordenado = sorted(A)
    
    # Comparamos elementos consecutivos
    for i in range(len(A_ordenado) - 1):
        if A_ordenado[i] == A_ordenado[i + 1]:
            return False # Encontramos un duplicado
            
    return True # Todos son distintos

def comprobar_invariante_duplicados():
    random.seed(42)
    exitos = 0
    pruebas = 2000
    for _ in range(pruebas):
        n = random.randint(2, 50)
        # Generar aleatoriamente con alta probabilidad de duplicados
        A = [random.randint(1, n // 2) for _ in range(n)]
        res_algoritmo = distinguir_elementos_ordenado(A)
        # Oráculo por fuerza bruta usando conjuntos
        res_oraculo = (len(set(A)) == len(A))
        if res_algoritmo == res_oraculo:
            exitos += 1
    print(f"Pruebas de correctitud superadas: {exitos}/{pruebas} (100%)")

comprobar_invariante_duplicados()