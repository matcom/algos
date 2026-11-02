import os
RUTA = os.path.join("Soluciones", "tema-1", "GlenRios")
os.makedirs(RUTA, exist_ok=True)  # crea la carpeta si no existe

class Nodo:
    def __init__(self, val):
        self.val = val
        self.next = None

def tiene_ciclo(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False

# Crear lista con ciclo
n = 10
nodos = [Nodo(i) for i in range(n)]
for i in range(n-1):
    nodos[i].next = nodos[i+1]
nodos[-1].next = nodos[3]  # ciclo en el nodo 3

print(tiene_ciclo(nodos[0]))  # True

# Sin ciclo
nodos[-1].next = None
print(tiene_ciclo(nodos[0]))  # False