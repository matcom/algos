## Problema 3

Una pila con una operación mínimo que cuesta O(1) en el peor caso. Diseña la estructura, enuncia el invariante que la hace correcta y da el costo de cada operación.

### Respuesta

-Estructura:

```python
class Pila:
    def __init__(self):
        self._items = []
        self._mins = []

    def push (self, x):
        self._items.append(x)
        if not self._mins or x<= self._mins[-1]:
            self._mins.append(x)

    def pop(self):
        if len(self._items) == 0:
            raise Exception("Pila vacía")
        if self._items[-1] == self._mins[-1]:
            self._mins.pop()
        return self._items.pop()

    def peek(self):
        if len(self._items) == 0:
            raise Exception("Pila vacía")
        return self._items[-1]

    def min(self):
        if len(self._items) == 0:
            raise Exception("Pila vacía")
        return self._mins[-1]

```

Al usar dos pilas para mantener el mínimo, se mantienen lso costos de una pila normal, push, pop, peek  son todas O(1). Y como la función min() es como un peek pero en la pila de mínimos es O(1) también. 

En todo momento en la pila de mínimos contiene los elementos de la pila principal que eran menores o iguales a todos los que habían introducido en el momento en que ellos llegaron a la pila. De aquí que la pila de mínimos es no creciente desde el primer elemento introducido al último, ya que cada valor que entra es <= al anterior. Por lo tanto mins[-1] siempre es el mínimo de items. Y esto precisamente es la invariante ya que se mantiene en todas los momentos y es lo que permite que la solución sea correcta.