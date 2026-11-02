**Problema:** Una pila con una operación minimo que cuesta $O(1)$ en el peor caso. Diseña la estructura, enuncia el invariante que la hace correcta y da el costo de cada operación.

## 1. Diseño de la estructura:

Para implementar una pila que soporte la operación `minimo()` en tiempo $O(1)$ en el peor caso, vamos a utilizar dos pilas: una `pila_principal` en donde se almacenará todos los elementos insertados en el orden original de una pila (`push` y `pop`), y una pila_minimo auxiliar que almacena los valores mínimos actuales de la pila principal.

**Ver implementación en min_stack.py**

**Funcionamiento:**
* `push(x)`: Se añade $x$ a la `pila_principal`, y si `pila_minimos` está vacía o $x \le pila\_minimo.top()$, se hace `push(x)` en esa pila también.
* `pop()`: Se extrae el elemento de la pila principal. Si este elemento es igual a `pila_minimos.top()`, también se hace `pop()` en esa pila.
* `minimo()`: Devuelve `pila_minimos.top()`.

## 2. Invariante de la estructura:
En cualquier estado de la ejecución, el elemento ubicado en el top de la pila de mínimos es estrictamente igual al valor mínimo de todos los elementos almacenados en la pila principal.

**Demostración:**
Hagamos una inducción sobre la secuencia de operaciones:

1. **Caso Base:** Al inicializar la estructura, ambas pilas están vacías, por lo que se cumple el invariante.
2. **Paso inductivo:** 
* Al insertar un elemento con `push(x)`: Si el elemento entrante $x$ es menor o igual que el mínimo actual, se coloca en la cima de `pila_minimos`, convirtiéndose correctamente en el nuevo mínimo global de los elementos almacenados. Si $x$ es mayor, el mínimo anterior sigue gobernando y se preserva en la cima de `pila_minimos`. Entonces el invariante se mantiene.

* Al eliminar un elemento con `pop()`: Si el elemento extraído de la pila principal no era el mínimo, la cima de `pilas_minimos` se mantiene igual, lo que es correcto porque los elementos restantes conservan su mismo mínimo. Si el elemento extraído era el mínimo actual, al retirarlo de `pila_minimos` se deja en el top al segundo elemento menor, que pasa a ser el nuevo mínimo de los elementos restantes. Entonces el invariante se mantiene.

3. Como el invariante garantiza que el top de `pila_minimos` siempre se refleja el valor mínimo real, entonces hacer `top()` resuelve la operación de manera correcta en $O(1)$.

## 3. Costo de cada operación en el peor caso
* `push(x)`: Realiza una sola inserción en la pila principal y otra en la pila auxiliar si cumple la condición. Ambas toman $O(1)$ en el peor caso.
* `pop()`: Realiza una sola extracción en la pila principal y otra en la pila auxiliar si cumple con la condición. Ambas toman $O(1)$ en el peor caso.
* `minimo()`: Solo consulta el elemento que esta en la cima de la pila auxiliar, lo que toma $O(1)$ en el peor caso.