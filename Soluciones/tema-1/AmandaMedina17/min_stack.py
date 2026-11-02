class PilaMinima:
    def __init__(self):
        # Pila principal para almacenar todos los elementos
        self.pila_principal = []
        # Pila auxiliar para mantener el seguimiento de los mínimos
        self.pila_minimos = []

    def push(self, x):
        """Inserta un elemento en la pila en O(1)."""
        self.pila_principal.append(x)
        # Si la pila de mínimos está vacía o el nuevo elemento es menor o igual al actual mínimo, se guarda
        if not self.pila_minimos or x <= self.pila_minimos[-1]:
            self.pila_minimos.append(x)

    def pop(self):
        """Elimina y retorna el elemento superior de la pila en O(1)."""
        if not self.pila_principal:
            raise IndexError("La pila está vacía")
        
        elemento_eliminado = self.pila_principal.pop()
        
        # Si el elemento eliminado es el mínimo actual, también se extrae de la pila de mínimos
        if elemento_eliminado == self.pila_minimos[-1]:
            self.pila_minimos.pop()
            
        return elemento_eliminado

    def minimo(self):
        """Retorna el elemento mínimo de la pila en O(1) sin modificarla."""
        if not self.pila_minimos:
            raise IndexError("La pila está vacía")
        return self.pila_minimos[-1]

    def top(self):
        """Retorna el elemento superior sin eliminarlo."""
        if not self.pila_principal:
            raise IndexError("La pila está vacía")
        return self.pila_principal[-1]

    def esta_vacia(self):
        return len(self.pila_principal) == 0