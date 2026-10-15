# Ejercicio 3

## Diseño de la Estructura

Para obtener el valor mínimo en tiempo constante $O(1)$ sin empeorar las operaciones habituales de la pila, mantenemos **dos pilas internas**:

1. **`items`**: Pila convencional que almacena todos los elementos insertados.
2. **`min_sort`**: Pila auxiliar que almacena el mínimo acumulado en cada nivel.

### Operaciones:
* **`push(x)`**: 
  1. Se inserta $x$ en `items`.
  2. Se inserta en `min_sort` el valor $\min(x, \text{tope de } \mathtt{pila\_min})$. Si `min_sort` está vacía, se inserta $x$.
* **`pop()`**:
  1. Se realiza `pop()` en `items` y `min_sort` simultáneamente. Retorna el elemento eliminado de `items`.
* **`min()`**:
  1. Retorna el tope de `min_sort` sin eliminarlo.

---

## Código
```
class Stack () :
    def __init__(self):
        self.items = []
        self.min_sort = []

    def push(self, item):
        self.items.append(item)
        
        if not self.min_sort or item <= self.min_sort[-1]:
            self.min_sort.append(item)
        else:
            self.min_sort.append(self.min_sort[-1])
        
    def pop(self):
        self.min_sort.pop()
        return self.items.pop()

    def min(self):
        return self.min_sort[-1]

def main () :
    stack = Stack()
    stack.push(5)
    stack.push(2)
    print(stack.min())
    stack.push(8)
    print(stack.min())
    stack.push(1)
    print(stack.min())

if __name__ == "__main__":
    main()
        

```
## Invariante 

> **"Para cualquier estado de la pila con $k$ elementos, el $i$-ésimo elemento de `min_sort` (para todo $1 \le i \le k$) es igual al valor mínimo de los primeros $i$ elementos de `items` contando desde el fondo."**

### Demostración Inductiva (3 Pasos):

1. **Inicialización:** Antes de la primera inserción, ambas pilas están vacías ($k = 0$). El invariante se cumple de forma vacía.
2. **Mantenimiento:** Supongamos que el invariante se cumple para $k$ elementos. 
   * Al ejecutar `push(x)`, `items` pasa a tener $k+1$ elementos.
   * `min_sort` inserta $m_{k+1} = \min(x, m_k)$, donde $m_k$ es el mínimo de los primeros $k$ elementos por hipótesis de inducción. Por definición de mínimo, $\min(x, m_k)$ es el mínimo exacto del conjunto de los $k+1$ elementos.
   * Al ejecutar `pop()`, se eliminan simultáneamente los topes de ambas pilas, manteniendo la correspondencia biyectiva para los $k-1$ elementos restantes.
3. **Conclusión:** Dado que el tope de `min_sort` coincide exactamente con el mínimo del prefijo de tamaño $k$, la función `min()` devuelve el valor mínimo global de la pila actual en $O(1)$.

---

## 3. Costo de cada Operación (Peor Caso)

| Operación | Tiempo | Memoria Extra | Explicación |
| :--- | :---: | :---: | :--- |
| **`push(x)`** | $O(1)$ | $O(1)$ | Un apilamiento en cada pila y una comparación de números. |
| **`pop()`** | $O(1)$ | $O(1)$ | Un desapilamiento en cada pila. |
| **`min()`** | $O(1)$ | $O(1)$ | Lectura directa del tope de `min_sort`. |

* **Espacio total:** $O(n)$ en el peor caso, donde $n$ es el número total de elementos en la pila.