## Problema

Dada una matriz cuadrada $M$ de dimensiones $n \times n$ cuyas filas y columnas se encuentran ordenadas de forma estrictamente creciente, diseñe un algoritmo que determine la existencia de un valor objetivo $x$ en un costo temporal de $\mathcal{O}(n)$ comparaciones.

1. Enuncie y demuestre la correctitud del algoritmo utilizando un **invariante de ciclo**.
2. Demuestre formalmente mediante el **método del adversario** que no es posible resolver el problema en un número de comparaciones de orden estrictamente menor a $n$ ($o(n)$).

---

## Solución

### 1. Algoritmo en $\mathcal{O}(n)$ Comparaciones

Para buscar $x$ de manera eficiente, aprovechamos la propiedad de monotonía bidimensional iniciando la exploración en la **esquina superior derecha** de la matriz (fila $\text{row} = 0$, columna $\text{col} = n - 1$):

1. Comparamos el valor actual $M[\text{row}][\text{col}]$ con el objetivo $x$:
* **Si $M[\text{row}][\text{col}] == x$:** El elemento ha sido encontrado; retornamos `True`.
* **Si $M[\text{row}][\text{col}] > x$:** Dado que las filas están ordenadas crecientemente de izquierda a derecha, todos los elementos situados a la derecha en esa misma fila son estrictamente mayores que $x$. Por consiguiente, $x$ no puede encontrarse en la columna actual. Descartamos toda la columna decrementando el índice: $\text{col} = \text{col} - 1$.
* **Si $M[\text{row}][\text{col}] < x$:** Dado que las columnas están ordenadas crecientemente de arriba hacia abajo, todos los elementos situados hacia arriba en esa columna son estrictamente menores que $x$. Por consiguiente, $x$ no puede encontrarse en la fila actual. Descartamos toda la fila incrementando el índice: $\text{row} = \text{row} + 1$.


2. Repetimos el proceso hasta hallar $x$ o hasta que los índices salgan de los límites válidos de la matriz.

#### Análisis de Costo Temporal

En cada iteración del ciclo, el algoritmo decrementa la columna o incrementa la fila. Dado que la matriz posee $n$ filas y $n$ columnas, el número máximo de pasos de borde realizados es $2n$, lo que garantiza una complejidad estrictamente lineal de $\mathcal{O}(n)$ comparaciones en el peor de los casos.

---

### 2. Demostración de Correctitud con un Invariante

#### Declaración del Invariante ($I$)

> *"Si el elemento objetivo $x$ se encuentra contenido en la matriz $M$, entonces necesariamente pertenece a la submatriz rectangular activa delimitada por las filas desde $\text{row}$ hasta $n-1$ y las columnas desde $0$ hasta $\text{col}$."*

Formalmente:


$$x \in M \implies x \in M[\text{row} \dots n-1][0 \dots \text{col}]$$

#### Demostración en Tres Fases

1. **Inicialización:**
Antes de la primera iteración, $\text{row} = 0$ y $\text{col} = n - 1$. La submatriz activa abarca la totalidad de la matriz $M[0 \dots n-1][0 \dots n-1]$. Si $x$ está presente en la matriz, trivialmente pertenece a este rango completo. El invariante se cumple de forma inicial.
2. **Mantenimiento:**
Asumimos que el invariante es válido al inicio de una iteración arbitraria y evaluamos el elemento en $M[\text{row}][\text{col}]$:
* **Caso $M[\text{row}][\text{col}] == x$:** El algoritmo retorna `True` correctamente.
* **Caso $M[\text{row}][\text{col}] > x$:** Por el ordenamiento creciente horizontal, toda la porción restante de la columna $\text{col}$ ubicada a la derecha de la celda actual contiene elementos mayores que $x$. Actualizar $\text{col} = \text{col} - 1$ descarta dicha columna entera sin omitir ningún candidato válido. Si $x$ existía en la matriz original, sigue estando confinado en la nueva submatriz activa. El invariante se preserva.
* **Caso $M[\text{row}][\text{col}] < x$:** Por el ordenamiento creciente vertical, toda la porción de la fila $\text{row}$ situada hacia arriba contiene elementos menores que $x$. Actualizar $\text{row} = \text{row} + 1$ descarta dicha fila entera de manera segura. El invariante se preserva para el nuevo intervalo activo.


3. **Conclusión:**
El ciclo concluye cuando $\text{row} \ge n$ o $\text{col} < 0$, momento en el cual la submatriz activa se ha reducido a un conjunto vacío ($\emptyset$). Por el invariante, si $x$ estuviera en la matriz, debería pertenecer a un conjunto vacío, lo cual es lógicamente imposible. Por lo tanto, concluir que $x \notin M$ y retornar `False` es perfectamente correcto.

---

### 3. Demostración de Cota Inferior con el Método del Adversario ($\Omega(n)$)

Queremos demostrar que ningún algoritmo basado en comparaciones y propiedades estructurales puede decidir si $x$ está en la matriz realizando menos de $n$ comparaciones en el peor de los casos (es decir, que una cota de $o(n)$ es imposible).

#### Estrategia del Adversario

1. Supongamos por contradicción que existe un algoritmo supuestamente correcto que resuelve el problema realizando estrictamente $k < n$ comparaciones en el peor de los casos.
2. Puesto que el algoritmo ejecuta menos de $n$ consultas y la matriz contiene $n$ filas y $n$ columnas, por el principio del palomar (o por análisis de cobertura de filas), existirá **al menos una fila completa** (por ejemplo, la fila $r$ con $0 \le r < n$) que **nunca fue consultada** por el algoritmo mediante ninguna comparación directa ni indirecta.
3. El adversario no fija de antemano los valores exactos de esa fila $r$ no visitada. En su lugar, diseña dos escenarios de entrada perfectamente consistentes con todas las respuestas y comparaciones que el algoritmo *sí* realizó hasta ese momento:
* **Entrada 1 ($M_1$):** Una matriz válida donde la fila no visitada $r$ contiene al elemento objetivo $x$ (la respuesta correcta del problema es `True`).
* **Entrada 2 ($M_2$):** Una matriz idéntica a $M_1$ en todas las celdas consultadas, pero donde la fila $r$ *no* contiene a $x$ (la respuesta correcta del problema es `False`).


4. Como el algoritmo jamás inspeccionó ninguna celda de la fila $r$, la traza de ejecuciones, las comparaciones realizadas y los resultados devueltos fueron exactamente idénticos en ambas corridas. Por consiguiente, el algoritmo emitirá exactamente la misma respuesta final para ambas matrices.
5. Si el algoritmo responde `True`, se equivoca catastróficamente en la Entrada 2 ($M_2$); si responde `False`, se equivoca en la Entrada 1 ($M_1$).

#### Conclusión del Adversario

Para impedir que el adversario construya este escenario de ambigüedad y produzca un fallo de correctitud, cualquier algoritmo está obligado a inspeccionar suficientes regiones de la matriz como para no dejar ninguna "zona ciega" de tamaño proporcional a $n$. Esto obliga a realizar al menos $n$ comparaciones en el peor de los casos, demostrando formalmente que la cota inferior es $\Omega(n)$ y que una complejidad de $o(n)$ es imposible.