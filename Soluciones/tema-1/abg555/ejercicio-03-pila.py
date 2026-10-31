class Node:
    # Un nodo de la pila:
    #   value = el elemento
    #   min   = el menor entre este elemento y todos los de abajo
    #   below = el nodo de abajo (None si no hay)
    def __init__(self, value, min, below):
        self.value = value
        self.min = min
        self.below = below


class MinStack:
    def __init__(self):
        self.top_node = None
        self.size = 0
        self.comparisons = 0

    def is_empty(self):
        return self.top_node is None

    def push(self, x):
        if self.top_node is None:
            new_min = x
        else:
            self.comparisons += 1
            new_min = x if x < self.top_node.min else self.top_node.min
        self.top_node = Node(x, new_min, self.top_node)
        self.size += 1

    def pop(self):
        if self.top_node is None:
            raise IndexError("pop en pila vacia")
        x = self.top_node.value
        self.top_node = self.top_node.below
        self.size -= 1
        return x

    def top(self):
        if self.top_node is None:
            raise IndexError("top de pila vacia")
        return self.top_node.value

    def minimo(self):
        if self.top_node is None:
            raise IndexError("minimo de pila vacia")
        return self.top_node.min

    def nodes(self):
        # los nodos de arriba hacia abajo (solo para las pruebas)
        node = self.top_node
        while node is not None:
            yield node
            node = node.below


class NormalStack:
    # Una pila normal: para el minimo recorre todos los elementos.
    def __init__(self):
        self.data = []
        self.comparisons = 0

    def is_empty(self):
        return not self.data

    def push(self, x):
        self.data.append(x)

    def pop(self):
        return self.data.pop()

    def top(self):
        return self.data[-1]

    def minimo(self):
        current_min = self.data[0]
        for x in self.data[1:]:
            self.comparisons += 1
            if x < current_min:
                current_min = x
        return current_min


class SavingStack:
    # Version que ahorra memoria: una segunda pila guarda solo los
    # elementos que eran el minimo cuando entraron.
    # Con strict=True usa < en vez de <=, y eso es un error.

    def __init__(self, strict=False):
        self.data = []
        self.mins = []
        self.strict = strict

    def is_empty(self):
        return not self.data

    def push(self, x):
        self.data.append(x)
        if not self.mins:
            self.mins.append(x)
        elif self.strict and x < self.mins[-1]:
            self.mins.append(x)
        elif not self.strict and x <= self.mins[-1]:
            self.mins.append(x)

    def pop(self):
        x = self.data.pop()
        if x == self.mins[-1]:
            self.mins.pop()
        return x

    def top(self):
        return self.data[-1]

    def minimo(self):
        return self.mins[-1]
