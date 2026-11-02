from collections import deque

def gale_shapley_incompleto(pref_a, pref_b):
    """
    Algoritmo de Gale-Shapley (Aceptación Diferida) con Listas Incompletas.
    
    Entradas:
      - pref_a: lista de listas. pref_a[a] contiene los receptores aceptables para 'a'.
      - pref_b: lista de listas. pref_b[b] contiene los proponentes aceptables para 'b'.
      
    Salida:
      - M: lista donde M[a] es el receptor emparejado con 'a' (o None si 'a' queda solo).
    """
    na, nb = len(pref_a), len(pref_b)
    
    # 1. Ranking invertido para que el receptor 'b' consulte su preferencia sobre 'a' en O(1)
    rango_b = [{a: pos for pos, a in enumerate(lista)} for lista in pref_b]
    
    # 2. Punteros de propuesta e inicialización de parejas
    siguiente = [0] * na
    pareja_de_b = [None] * nb
    
    # 3. Solo ingresan a la cola inicial los proponentes que tienen opciones aceptables
    libres = deque(a for a in range(na) if pref_a[a])
    
    while libres:
        a = libres.popleft()
        
        # Receptor al que le corresponde proponerle
        b = pref_a[a][siguiente[a]]
        siguiente[a] += 1
        
        actual = pareja_de_b[b]
        rechazado = False
        
        # Caso 1: b no listó a 'a' (a es inaceptable para b) -> rechazo inmediato
        if a not in rango_b[b]:
            rechazado = True
        # Caso 2: b está libre y 'a' es aceptable -> acepta provisionalmente
        elif actual is None:
            pareja_de_b[b] = a
        # Caso 3: b prefiere a 'a' sobre su pareja actual -> cambia
        elif rango_b[b][a] < rango_b[b][actual]:
            pareja_de_b[b] = a
            desplazado = actual
            # El proponente desplazado vuelve a la cola SOLO si le quedan opciones
            if siguiente[desplazado] < len(pref_a[desplazado]):
                libres.append(desplazado)
        # Caso 4: b prefiere a su pareja actual -> rechaza a 'a'
        else:
            rechazado = True
            
        # El proponente 'a' reintenta SOLO si fue rechazado y le quedan opciones en su lista
        if rechazado and siguiente[a] < len(pref_a[a]):
            libres.append(a)
            
    # Reconstrucción de la asignación final M
    M = [None] * na
    for b, a in enumerate(pareja_de_b):
        if a is not None:
            M[a] = b
            
    return M


# Ejemplo de uso
if __name__ == "__main__":
    pref_a = [
        [0, 1],    # a0 lista b0, b1
        [0],       # a1 lista b0
        [1, 2],    # a2 lista b1, b2
        [2]        # a3 lista b2
    ]
    pref_b = [
        [1, 0, 2, 3], # b0
        [0, 2, 1, 3], # b1
        [3, 2, 0, 1]  # b2
    ]
    
    M = gale_shapley_incompleto(pref_a, pref_b)
    print("Emparejamiento final M:", M)
    # Output: [1, 0, None, 2]  (a0 con b1, a1 con b0, a2 libre, a3 con b2)

