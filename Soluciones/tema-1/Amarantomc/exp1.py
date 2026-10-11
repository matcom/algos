class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

def detectar_ciclo_floyd(head):
    if not head or not head.next:
        return False, []

    tortuga = head
    liebre = head
    paso = 0
    traza = []

    while liebre and liebre.next:
        paso += 1
        tortuga = tortuga.next
        liebre = liebre.next.next
        
        t_val = tortuga.val if tortuga else "None"
        l_val = liebre.val if liebre else "None"
        traza.append((paso, t_val, l_val))

        if tortuga == liebre:
            return True, traza

    return False, traza

# --- Casos de Prueba e Ilustración en Tabla ---
def probar_algoritmo_floyd():
    print("=== CASO 1: Lista CON Ciclo (1 -> 2 -> 3 -> 4 -> 2 ...) ===")
    n1 = Node(1)
    n2 = Node(2)
    n3 = Node(3)
    n4 = Node(4)
    n1.next = n2
    n2.next = n3
    n3.next = n4
    n4.next = n2 # Crea un ciclo apuntando al nodo 2

    tiene_ciclo, traza = detectar_ciclo_floyd(n1)
    
    print(f"{'PASO':<6} | {'POSICIÓN TORTUGA':<18} | {'POSICIÓN LIEBRE':<18} | {'ESTADO':<15}")
    print("-" * 63)
    for p, t, l in traza:
        estado = "¡Colisión!" if t == l else "Avanzando"
        print(f"{p:<6} | {str(t):<18} | {str(l):<18} | {estado:<15}")
    
    print(f"\nResultado final: ¿Tiene ciclo? -> {tiene_ciclo}\n")

    print("=== CASO 2: Lista SIN Ciclo (1 -> 2 -> 3 -> 4 -> None) ===")
    m1 = Node(1)
    m2 = Node(2)
    m3 = Node(3)
    m4 = Node(4)
    m1.next = m2
    m2.next = m3
    m3.next = m4

    tiene_ciclo_2, traza_2 = detectar_ciclo_floyd(m1)
    print(f"{'PASO':<6} | {'POSICIÓN TORTUGA':<18} | {'POSICIÓN LIEBRE':<18} | {'ESTADO':<15}")
    print("-" * 63)
    for p, t, l in traza_2:
        print(f"{p:<6} | {str(t):<18} | {str(l):<18} | {'Avanzando':<15}")
    
    print(f"\nResultado final: ¿Tiene ciclo? -> {tiene_ciclo_2}")

if __name__ == "__main__":
    probar_algoritmo_floyd()