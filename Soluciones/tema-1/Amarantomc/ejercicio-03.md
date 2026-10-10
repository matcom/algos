# Ejercicio 3: Una pila con operación mínimo que cuesta $O(1)$ en el peor caso

En una pila convencional (Stack), las operaciones básicas de inserción (`push`) y extracción (`pop`) operan en un tiempo de $O(1)$ en el peor caso. Sin embargo, consultar el elemento mínimo presente en la pila normalmente requeriría recorrer todos sus elementos, lo que costaría $O(n)$ en el peor caso, o mantenerlos ordenados, afectando el costo de las inserciones.

Queremos diseñar una estructura de datos basada en una pila que soporte las siguientes operaciones, **todas en el peor caso $O(1)$**:
- `push(x)`: Inserta el elemento $x$ en la cima de la pila.
- `pop()`: Remueve y devuelve el elemento de la cima de la pila.
- `top()`: Devuelve el elemento de la cima sin removerlo.
- `min()`: Devuelve el elemento mínimo actual contenido en la pila.

Para lograr un costo de $O(1)$ en la operación `min()`, la solución propuesta consiste en almacenar en la pila elementos compuestos en formato de tupla:

$$\text{Elemento en Pila} = (v, m)$$

Donde:
* $v$: El valor real insertado en la pila.
* $m$: El valor mínimo acumulado en la pila desde la base hasta este exacto elemento $v$.

### Diseño de la Estructura de Datos

* **`stack`**: Una única estructura lineal (como una lista) donde cada nodo o entrada contiene la tupla $(v, m)$.

#### Ilustración del Diseño

Consideremos la secuencia de inserciones: $5, 2, 8, 1, 3$.

```
Estado de la pila con tuplas (valor, mínimo_acumulado):

push(5)     push(2)         push(8)           push(1)           push(3)
                                                                
[ (5, 5) ]  [ (2, 2) ]      [ (8, 2) ]        [ (1, 1) ]        [ (3, 1) ]
            [ (5, 5) ]      [ (2, 2) ]        [ (8, 2) ]        [ (1, 1) ]
                            [ (5, 5) ]        [ (2, 2) ]        [ (8, 2) ]
                                              [ (5, 5) ]        [ (2, 2) ]
                                                                [ (5, 5) ]
```

## Invariante de la Estructura

Para demostrar la correctitud formal de esta variante definimos su invariante.


> *"Para cualquier estado de la pila tras un número arbitrario de operaciones, sea $S$ la secuencia de $k$ tuplas almacenadas $[(x_1, m_1), (x_2, m_2), \dots, (x_k, m_k)]$, donde $(x_k, m_k)$ es la cima, se cumple que para todo índice $i \in \{1, 2, \dots, k\}$, el segundo componente $m_i$ es exactamente el valor mínimo del subconjunto de valores de la pila desde la base hasta la posición $i$, es decir, $m_i = \min(\{x_1, x_2, \dots, x_i\})$."*

### Demostración del Invariante (por Inducción)

 **Inicialización:**
   Antes de realizar operaciones, la pila está vacía ($k = 0$). El conjunto de tuplas es vacío, por lo que el invariante se cumple de forma trivial.

 **Mantenimiento:**
   Supongamos que el invariante es válido para una pila con $k$ tuplas. Analizamos las operaciones:

- **Operación `push(x)`:**
  Si la pila está vacía ($k = 0$), se inserta la tupla $(x, x)$. El mínimo acumulado es $x$, que es correcto para un único elemento.
   Si la pila no está vacía, sea $(x_k, m_k)$ la tupla en la cima actual. El nuevo mínimo acumulado para el elemento $x$ se calcula como $m_{k+1} = \min(m_k, x)$. Se inserta la tupla $(x, m_{k+1})$.
  Por definición, este nuevo componente $m_{k+1}$ refleja correctamente el mínimo del prefijo ampliado de tamaño $k+1$. El invariante se mantiene.

- **Operación `pop()`:**
   Se elimina la tupla superior $(x_k, m_k)$. Al reducir el tamaño a $k-1$, la nueva cima vuelve a conservar intacto su componente de mínimo acumulado correcto para los elementos restantes. El invariante se mantiene.

 Dado que el invariante se inicializa correctamente y se mantiene en cada mutación (`push` y `pop`), consultar el mínimo equivale siempre a inspeccionar el segundo elemento de la cima de la pila, operando con plena correctitud.

## 3. Costo de cada Operación (Peor Caso)

| Operación | Descripción | Complejidad Temporal (Peor Caso) | Complejidad Espacial | 
| ----- | ----- | ----- | ----- | 
| `push(x)` | Crea una tupla $(x, \min)$ y la añade a la pila. | $\mathbf{O(1)}$ | $\mathbf{O(1)}$ | 
| `pop()` | Extrae la tupla superior de la pila. | $\mathbf{O(1)}$ | $O(1)$ | 
| `top()` | Consulta el primer componente de la tupla superior. | $\mathbf{O(1)}$ | $O(1)$ | 
| `min()` | Consulta el segundo componente de la tupla superior. | $\mathbf{O(1)}$ | $\mathbf{O(1)}$ | 

La estructura utiliza una sola estructura de datos lineal y empaqueta el estado del mínimo junto al valor, por lo que la operación `min()` solo consulta el segundo elemento de la tupla que está en `top()` y actualizar o mantener el minimo solo realiza operaciones  atómicas en este caso la comparación de 2 elementos,  manteniendo así una complejidad temporal estricta de $\mathcal{O}(1)$ en el peor caso.

## 4. Código de Simulación y Casos de Prueba

El siguiente script en Python implementa la pila basada en tuplas, verifica los invariantes y muestra una tabla detallada del estado paso a paso.

```
import sys

class TupleMinStack:
    def __init__(self):
        self.stack = []

    def push(self, x):
        if not self.stack:
            min_val = x
        else:
            min_val = min(x, self.stack[-1][1])
        self.stack.append((x, min_val))

    def pop(self):
        if not self.stack:
            raise IndexError("pop from empty stack")
        return self.stack.pop()[0]

    def top(self):
        if not self.stack:
            raise IndexError("top from empty stack")
        return self.stack[-1][0]

    def get_min(self):
        if not self.stack:
            raise IndexError("min from empty stack")
        return self.stack[-1][1]

# --- Casos de Prueba e Ilustración en Tabla ---
def probar_pila_tuplas():
    operaciones = [
        ("push", 5),
        ("push", 2),
        ("push", 8),
        ("min", None),
        ("push", 1),
        ("min", None),
        ("pop", None),
        ("min", None),
        ("pop", None),
        ("min", None)
    ]

    pila = TupleMinStack()
    
    print(f"{'OPERACIÓN':<15} | {'ARG':<5} | {'ESTADO DE LA PILA (VAL, MIN)':<35} | {'MÍNIMO RETORNADO':<18}")
    print("-" * 81)

    for op, val in operaciones:
        res = "-"
        if op == "push":
            pila.push(val)
            res = f"insertado {val}"
        elif op == "pop":
            res = f"removido {pila.pop()}"
        elif op == "min":
            res = str(pila.get_min())
        
        stack_str = str(pila.stack)
        arg_str = str(val) if val is not None else ""
        
        print(f"{op:<15} | {arg_str:<5} | {stack_str:<35} | {res:<18}")

if __name__ == "__main__":
probar_pila_tuplas()

```

### Salida esperada del script:

```
OPERACIÓN       | ARG   | ESTADO DE LA PILA (VAL, MIN)      | MÍNIMO RETORNADO  
---------------------------------------------------------------------------------
push            | 5     | [(5, 5)]                          | insertado 5       
push            | 2     | [(5, 5), (2, 2)]                  | insertado 2       
push            | 8     | [(5, 5), (2, 2), (8, 2)]          | insertado 8       
min             |       | [(5, 5), (2, 2), (8, 2)]          | 2                 
push            | 1     | [(5, 5), (2, 2), (8, 2), (1, 1)]  | insertado 1       
min             |       | [(5, 5), (2, 2), (8, 2), (1, 1)]  | 1                 
pop             |       | [(5, 5), (2, 2), (8, 2)]          | removido 1        
min             |       | [(5, 5), (2, 2), (8, 2)]          | 2                 
pop             |       | [(5, 5), (2, 2)]                  | removido 8        
min             |       | [(5, 5), (2, 2)]                  | 2                 

```