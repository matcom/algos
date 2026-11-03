class EmptyStackError(Exception):
    """Se lanza al operar sobre una pila vacía."""
    pass


class MinStack:

    def __init__(self):
        self._data = [] 
        self._mins = [] 


    def push(self, x):
        """Inserta x en el tope. O(1) amortizado (potencial Phi = 2n - c)."""
        self._data.append(x)
        if not self._mins:
            self._mins.append(x)
        else:
            self._mins.append(min(self._mins[-1], x))

    def pop(self):
        if not self._data:
            raise EmptyStackError("pop() sobre pila vacía")
        self._mins.pop()
        return self._data.pop()

    def top(self):
        if not self._data:
            raise EmptyStackError("top() sobre pila vacía")
        return self._data[-1]

    def min(self):
        if not self._mins:
            raise EmptyStackError("min() sobre pila vacía")
        return self._mins[-1]

    def is_empty(self):
        return not self._data

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return f"MinStack(data={self._data}, mins={self._mins})"
