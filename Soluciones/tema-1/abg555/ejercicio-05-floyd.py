class Node:
    # Un nodo de la lista:
    #   value = el dato
    #   next  = el nodo siguiente (None si la lista se termina)
    def __init__(self, value):
        self.value = value
        self.next = None


def has_cycle(head, trace=None):
    # Algoritmo de Floyd: slow avanza 1 nodo por vuelta y fast avanza 2.
    # Si se pasa una lista en trace, guarda (slow, fast) despues de cada vuelta.
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if trace is not None:
            trace.append((slow, fast))
        if slow is fast:
            return True
    return False


def has_cycle_set(head, seen=None):
    # Version con conjunto: guarda todos los nodos visitados.
    # Es correcta, pero usa O(n) memoria.
    if seen is None:
        seen = set()
    node = head
    while node is not None:
        if node in seen:
            return True
        seen.add(node)
        node = node.next
    return False


def has_cycle_bug(head):
    # Version con un error: solo revisa fast.next, no si fast es None.
    slow = fast = head
    while fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False


def make_list(mu, lam):
    # Construye una lista con mu nodos antes del ciclo y un ciclo de lam nodos.
    # Con lam = 0 no hay ciclo y la lista tiene mu nodos.
    nodes = [Node(i) for i in range(mu + lam)]
    for a, b in zip(nodes, nodes[1:]):
        a.next = b
    if lam > 0:
        nodes[-1].next = nodes[mu]
    head = nodes[0] if nodes else None
    return head, nodes


def node_at(head, i):
    # El nodo al que se llega desde head dando i pasos (None si la lista se acaba)
    node = head
    for _ in range(i):
        if node is None:
            return None
        node = node.next
    return node
