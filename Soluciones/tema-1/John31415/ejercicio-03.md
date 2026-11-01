## Problema

Diseñe una estructura de datos tipo Pila (*Stack*) que soporte la operación de consulta del valor mínimo (*min*) con un costo temporal en el peor caso de $\mathcal{O}(1)$. Enuncie el diseño detallado de la estructura, establezca formalmente el invariante que garantiza su correctitud y determine analíticamente el costo operacional de cada método en el peor caso.

---

## Solución

### 1. Diseño de la Estructura de Datos

Para lograr un tiempo de ejecución constante $\mathcal{O}(1)$ en todas las operaciones, incluyendo la consulta del mínimo, se implementa una estructura compuesta basada en el uso concurrente de **dos pilas internas** de tamaño dinámico:

1. **`stack` (Pila de Datos):** Almacena de manera secuencial todos los elementos insertados en la pila, preservando el orden natural de llegada de las operaciones.
2. **`min_stack` (Pila de Mínimos Auxiliar):** Mantiene un registro histórico de los valores mínimos vigentes correspondientes a cada estado evolutivo de la pila principal.

#### Especificación Formal de las Operaciones

* **`push(x)`:**
1. Inserta el elemento $x$ en la cima de `stack`.
2. Evalúa la condición de minimalidad: si `min_stack` se encuentra vacía, o si $x$ es menor o igual al elemento actual en la cima de `min_stack` ($x \le \text{cima}(\text{min\_stack})$), se inserta $x$ en `min_stack`. *(Nota: El uso del operador menor o igual es indispensable para gestionar correctamente elementos duplicados).*


* **`pop()`:**
1. Extrae y almacena el elemento en la cima de `stack` (sea $v = \text{cima}(\text{stack})$).
2. Evalúa si $v$ coincide con el mínimo actual: si $v = \text{cima}(\text{min\_stack})$, se extrae también la cima de `min_stack`.
3. Retorna el valor $v$.


* **`min()`:**
1. Retorna el elemento ubicado en la cima de `min_stack` sin modificar ni extraer la estructura.


* **`top()`:**
1. Retorna el elemento ubicado en la cima de `stack` sin modificar ni extraer la estructura.



---

### 2. Invariante de la Estructura (Correctitud Parcial)

#### Declaración del Invariante ($I$)

> *"En cualquier instante de la ejecución, el elemento situado en la cima de la pila auxiliar `min_stack` es exactamente equivalente al valor mínimo global de todos los elementos actualmente almacenados en la pila de datos `stack`."*

Formalmente, si denotamos como $\mathcal{S}$ al conjunto de elementos en `stack` y $\text{top}(\text{min\_stack})$ a su cima:


$$\text{top}(\text{min\_stack}) = \min(\mathcal{S})$$

#### Demostración Informal por Inducción sobre las Transiciones

1. **Caso Base (Estructura Vacía):**
Al inicializar la estructura, tanto `stack` como `min_stack` se encuentran vacías. El invariante se cumple de manera trivial al no existir elementos bajo consideración.
2. **Paso Inductivo ($\text{push}(x)$):**
Asumimos que el invariante se cumple antes de la inserción. Al insertar un nuevo elemento $x$:
* Si $x \le \text{top}(\text{min\_stack})$, $x$ se convierte en el nuevo valor mínimo de la colección ampliada. Al apilar $x$ en `min_stack`, su cima pasa a reflejar exactamente este nuevo mínimo, preservando $I$.
* Si $x > \text{top}(\text{min\_stack})$, el mínimo anterior sigue siendo estrictamente menor o igual que $x$, por lo que el mínimo global de `stack` no experimenta cambios. Omitir la inserción en `min_stack` mantiene el valor histórico correcto en la cima, preservando $I$.


3. **Paso Inductivo ($\text{pop}()$):**
Al extraer un elemento $v$ de la cima de `stack`:
* Si $v \neq \text{top}(\text{min\_stack})$, el elemento retirado no constituía el valor mínimo actual. Por lo tanto, el mínimo global de la colección restante permanece inalterado en la cima de `min_stack`, preservando $I$.
* Si $v = \text{top}(\text{min\_stack})$, el valor mínimo vigente es eliminado de la pila de datos. Al extraer simultáneamente la cima de `min_stack`, la estructura expone de manera inmediata el segundo menor valor histórico registrado, el cual pasa a ser el nuevo mínimo correcto del subconjunto remanente, preservando $I$.



---

### 3. Análisis de Costos (Peor Caso)

Dado que todas las operaciones fundamentales interactúan exclusivamente con las cimas de las pilas (implementadas internamente mediante arreglos dinámicos con inserción y borrado amortizado en el extremo, o listas enlazadas), el rendimiento temporal está completamente desacoplado del número total de elementos $N$ almacenados:

| Operación | Costo en el Peor Caso | Justificación Analítica |
| --- | --- | --- |
| **`push(x)`** | $\mathcal{O}(1)$ | Como máximo una inserción en `stack` y una inserción condicional en `min_stack`. |
| **`pop()`** | $\mathcal{O}(1)$ | Como máximo una extracción en `stack` y una comparación/extracción condicional en `min_stack`. |
| **`min()`** | $\mathcal{O}(1)$ | Consulta directa de la cima de `min_stack` sin recorrido ni búsqueda. |
| **`top()`** | $\mathcal{O}(1)$ | Consulta directa de la cima de `stack`. |