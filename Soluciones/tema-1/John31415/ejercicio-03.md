## Problema

Diseñe una estructura de datos tipo Pila (*Stack*) que soporte la operación de consulta del valor mínimo (*min*) con un costo temporal en el peor caso de $\mathcal{O}(1)$. Enuncie el diseño detallado de la estructura, establezca formalmente el invariante que garantiza su correctitud y determine analíticamente el costo operacional de cada método en el peor caso.

---

## Solución

### 1. Diseño de la Estructura de Datos

Para lograr un tiempo de ejecución constante $\mathcal{O}(1)$ en todas las operaciones, incluyendo la consulta del mínimo, se implementa una estructura compuesta basada en el uso concurrente de **dos pilas internas**:

1. **`stack` (Pila de Datos):** Almacena de manera secuencial todos los elementos insertados en la pila, preservando el orden natural de llegada de las operaciones.
2. **`min_stack` (Pila de Mínimos Auxiliar):** Mantiene un registro de los elementos que constituyen mínimos de sus respectivos prefijos en la pila principal, incluyendo los valores repetidos.

Ambas pilas se implementan mediante listas enlazadas, de manera que las operaciones sobre sus cimas tengan costo constante en el peor caso.

#### Especificación Formal de las Operaciones

* **`push(x)`:**
1. Inserta el elemento $x$ en la cima de `stack`.
2. Evalúa la condición de minimalidad: si `min_stack` se encuentra vacía, o si $x$ es menor o igual al elemento actual en la cima de `min_stack` ($x \leq \text{cima}(\text{min\_stack})$), se inserta $x$ en `min_stack`. *(El uso del operador menor o igual es indispensable para gestionar correctamente elementos duplicados).*


* **`pop()`:**
1. Extrae y almacena el elemento en la cima de `stack` (sea $v = \text{cima}(\text{stack})$).
2. Evalúa si $v$ coincide con el mínimo actual: si $v = \text{cima}(\text{min\_stack})$, se extrae también la cima de `min_stack`.
3. Retorna el valor $v$.


* **`min()`:**
1. Retorna el elemento ubicado en la cima de `min_stack` sin modificar ni extraer la estructura.


* **`top()`:**
1. Retorna el elemento ubicado en la cima de `stack` sin modificar ni extraer la estructura.



Las operaciones `pop()`, `min()` y `top()` requieren que la pila no esté vacía. En caso contrario, se produce un error por violación de la precondición.

---

### 2. Invariante de la Estructura (Correctitud Parcial)

#### Declaración del Invariante ($I$)

> *En cualquier instante de la ejecución, `min_stack` contiene, en el mismo orden relativo, exactamente aquellos elementos de `stack` que constituyen mínimos de sus respectivos prefijos, incluyendo los elementos repetidos. Por tanto, si `stack` no está vacía, la cima de `min_stack` es el mínimo global de todos los elementos almacenados en `stack`.*

Formalmente, consideremos que los elementos de `stack`, desde el fondo hasta la cima, forman la secuencia $S=(s_1,s_2,\dots,s_m)$. Entonces, `min_stack` contiene la secuencia $M$ formada por los elementos $s_i$ que cumplen:

$$s_i \leq s_j \quad \forall j < i$$

Para $i=1$, la condición se considera satisfecha por vacuidad.

De esta propiedad se deduce que:

$$\begin{cases} M = \varnothing & \text{si } S = \varnothing,\\ \text{cima}(M) = \min(S) & \text{si } S \neq \varnothing. \end{cases}$$

#### Demostración Informal por Inducción sobre las Transiciones

1. **Caso Base (Estructura Vacía):**
Al inicializar la estructura, tanto `stack` como `min_stack` se encuentran vacías. El invariante se cumple trivialmente, pues no existen elementos bajo consideración ni mínimos que registrar.
2. **Paso Inductivo (`push(x)`):**
Asumimos que el invariante se cumple antes de la inserción. Al insertar un nuevo elemento $x$:
* Si `min_stack` está vacía o $x \leq \text{cima}(\text{min\_stack})$, $x$ se convierte en un nuevo mínimo del prefijo ampliado. Al apilar $x$ en `min_stack`, se preserva la propiedad del invariante.
* Si $x > \text{cima}(\text{min\_stack})$, el mínimo anterior sigue siendo menor que $x$, por lo que el nuevo elemento no constituye un mínimo de su prefijo. Omitir su inserción en `min_stack` mantiene la correspondencia entre ambas pilas.


3. **Paso Inductivo (`pop()`):**
Al extraer un elemento $v$ de la cima de `stack`, se presentan dos casos:
* Si $v \neq \text{cima}(\text{min\_stack})$, el elemento retirado no constituye un mínimo de su prefijo. Por tanto, no está registrado en `min_stack` y basta con eliminarlo de `stack`. La secuencia de mínimos de prefijos restantes no experimenta cambios, preservando el invariante.
* Si $v = \text{cima}(\text{min\_stack})$, el elemento retirado constituye un mínimo de su prefijo y está registrado en la cima de `min_stack`. Al extraerlo también de la pila auxiliar, el mínimo correspondiente al prefijo anterior queda expuesto en su cima. Este elemento representa correctamente el nuevo mínimo de los elementos restantes de `stack`, preservando el invariante.



Por inducción, el invariante se mantiene después de cualquier secuencia válida de operaciones. En particular, cuando la pila no está vacía, la cima de `min_stack` contiene siempre el mínimo global de los elementos almacenados en `stack`, garantizando la correctitud de la operación `min()`.

---

### 3. Análisis de Costos (Peor Caso)

Dado que ambas pilas se implementan mediante listas enlazadas y todas las operaciones fundamentales interactúan exclusivamente con sus cimas, el rendimiento temporal es independiente del número total de elementos $N$ almacenados:

| Operación | Costo en el Peor Caso | Justificación Analítica |
| --- | --- | --- |
| **`push(x)`** | $\mathcal{O}(1)$ | Una inserción en `stack`, una comparación y, como máximo, una inserción condicional en `min_stack`. Cada operación sobre una lista enlazada tiene costo constante. |
| **`pop()`** | $\mathcal{O}(1)$ | Una extracción en `stack` y, como máximo, una comparación y una extracción condicional en `min_stack`. |
| **`min()`** | $\mathcal{O}(1)$ | Consulta directa de la cima de `min_stack` sin recorrido ni búsqueda. |
| **`top()`** | $\mathcal{O}(1)$ | Consulta directa de la cima de `stack`. |

Por tanto, todas las operaciones solicitadas tienen complejidad temporal $\mathcal{O}(1)$ en el peor caso.