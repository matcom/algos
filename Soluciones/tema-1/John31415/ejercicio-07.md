## Problema

Dada la mediana de dos arreglos ordenados de longitud $n$ (definida como el $n$-ésimo menor elemento de la unión de ambos conjuntos con $2n$ elementos en total):

1. Diseñe un algoritmo con complejidad temporal en $\mathcal{O}(\log n)$.
2. Demuestre formalmente su correctitud utilizando un invariante de ciclo.
3. Determine y justifique la cota de información del problema.

---

## Solución

### 1. Diseño del Algoritmo en $\mathcal{O}(\log n)$

Para encontrar el $k$-ésimo elemento (donde $k=n$ para el cálculo de la mediana) de dos arreglos ordenados $A$ y $B$ de tamaño $n$, implementamos una búsqueda binaria sobre el número de elementos $i$ que se toman del arreglo $A$. Al seleccionar $i$ elementos de $A$, debemos tomar de manera complementaria $j=k-i$ elementos de $B$ para completar los $k$ elementos de la mitad inferior.

#### Condición de Partición Válida

Buscamos un índice de corte $i \in [0, k]$ que satisfaga simultáneamente las restricciones de cruce:

1. $A[i-1] \leq B[j]$
2. $B[j-1] \leq A[i]$

Una vez encontrado el índice válido, el $k$-ésimo menor elemento se obtiene directamente como $\max(A[i-1], B[j-1])$.

#### Implementación del Algoritmo

```python
def find_kth_element(A, B, k):
    n = len(A)

    # Aseguramos que A sea el arreglo más pequeño para acotar eficientemente la búsqueda
    if n > len(B):
        return find_kth_element(B, A, k)

    low = max(0, k - len(B))
    high = min(k, len(A))

    while low <= high:
        i = (low + high) // 2
        j = k - i

        # Elementos limítrofes (manejando los bordes con infinitos)
        A_left = A[i-1] if i > 0 else float('-inf')
        A_right = A[i] if i < len(A) else float('inf')
        B_left = B[j-1] if j > 0 else float('-inf')
        B_right = B[j] if j < len(B) else float('inf')

        if A_left <= B_right and B_left <= A_right:
            # Partición correcta encontrada
            return max(A_left, B_left)
        elif A_left > B_right:
            # Tomamos demasiados elementos de A, disminuimos i
            high = i - 1
        else:
            # Tomamos muy pocos elementos de A, aumentamos i
            low = i + 1

    return -1

```

#### Costo Temporal

Dado que el espacio de búsqueda para el índice $i$ abarca desde $0$ hasta $\min(k, n)$ y se reduce a la mitad en cada iteración del ciclo `while`, el número total de pasos es $\mathcal{O}(\log n)$.

---

### 2. Demostración de Correctitud con un Invariante

#### Declaración del Invariante ($I$)

*Si existe una partición válida, su índice de partición correcto $i^*$ (que representa el número de elementos aportados por $A$ en la partición óptima) se encuentra siempre dentro del rango activo actual $[low, high]$.*

#### Demostración en Tres Fases

1. **Inicialización:**
Antes de la primera iteración, definimos:

$$low = \max(0, k - \vert{}B\vert{}), \qquad high = \min(k, \vert{}A\vert{})$$



Estos límites garantizan que ambos arreglos puedan aportar exactamente $k$ elementos en conjunto, respetando sus respectivos tamaños. Por tanto, cualquier partición válida está inicialmente dentro del intervalo. El invariante se cumple.
2. **Mantenimiento:**
Asumimos que el invariante es válido antes de una iteración. Se calcula $i = \lfloor(low + high)/2\rfloor$ y $j = k - i$.
* Caso $A[i-1] > B[j]$: Estamos tomando demasiados elementos de $A$, por lo que cualquier partición válida debe tener un índice menor que $i$. Actualizamos $high = i - 1$. El invariante se preserva.
* Caso $B[j-1] > A[i]$: Estamos tomando demasiados elementos de $B$ y muy pocos de $A$, por lo que cualquier partición válida debe tener un índice mayor que $i$. Actualizamos $low = i + 1$. El invariante se preserva.
* Caso $A[i-1] \leq B[j]$ y $B[j-1] \leq A[i]$: Se ha encontrado una partición válida y el algoritmo retorna $\max(A[i-1], B[j-1])$.


3. **Terminación y Correctitud:**
Cuando se cumplen las dos condiciones de partición, los $k$ elementos seleccionados son exactamente los $k$ menores de la unión de ambos arreglos. Esto se debe a que cada arreglo está ordenado y las condiciones garantizan que ningún elemento de la mitad inferior sea mayor que uno de la mitad superior.
Por tanto, el mayor de los $k$ elementos seleccionados es:

$$\max(A[i-1], B[j-1])$$



que constituye el elemento buscado.
Además, las condiciones de descarte permiten eliminar sistemáticamente los índices incorrectos sin descartar una partición válida. Como el intervalo de búsqueda se reduce en cada iteración y contiene inicialmente una partición válida, la búsqueda termina encontrándola. Así, el algoritmo es correcto y tiene complejidad temporal $\mathcal{O}(\log n)$.

---

### 3. Cota de Información

La cota de información para este problema es:


$$\boxed{\Omega(\log n)}$$

#### Justificación mediante un Árbol de Decisión

Para justificar la cota inferior, consideremos dos arreglos ordenados de longitud $n$, con elementos distintos. Fijemos:


$$A = \{1, 2, \ldots, n\}$$

Construimos una familia de $n$ instancias diferentes para el arreglo $B$. Para cada $r \in \{1, 2, \ldots, n\}$, definimos:


$$B_r = \big(\underbrace{-(n-r), \ldots, -1}_{n-r \text{ elementos}}, \underbrace{n+1, \ldots, n+r}_{r \text{ elementos}}\big)$$

Si $r=n$, el primer segmento se considera vacío. Cada arreglo $B_r$ tiene exactamente $n$ elementos y está ordenado estrictamente de forma creciente.

En la unión de $A$ y $B_r$, los elementos quedan ordenados de la siguiente manera:


$$-(n-r), \ldots, -1, 1, 2, \ldots, n, n+1, \ldots, n+r$$

Existen exactamente $n-r$ elementos menores que $1$ y, por tanto, el $n$-ésimo menor elemento de la unión es precisamente:


$$\operatorname{mediana}(A, B_r) = A[r] = r$$

De esta manera, cada una de las $n$ instancias construidas produce un resultado diferente. Por tanto, cualquier algoritmo basado en comparaciones debe distinguir al menos $n$ resultados posibles.

En el modelo de comparación, un algoritmo puede representarse mediante un árbol de decisión binario, donde cada nodo interno corresponde a una comparación y cada hoja representa un resultado distinguible. Como los elementos de las instancias construidas son distintos, cada comparación tiene dos posibles resultados. Para resolver todas estas instancias, el árbol necesita al menos $n$ hojas.

Si denotamos como $h$ la altura del árbol, que representa el número máximo de comparaciones en el peor caso, se cumple:


$$2^h \geq n$$

De aquí se obtiene:


$$h \geq \lceil\log_2 n\rceil$$

Por consiguiente, cualquier algoritmo basado en comparaciones necesita, en el peor caso:


$$\boxed{\Omega(\log n)}$$


comparaciones.

Así, junto con el algoritmo presentado, cuya complejidad temporal es $\mathcal{O}(\log n)$, se obtiene una complejidad óptima de:


$$\boxed{\Theta(\log n)}$$