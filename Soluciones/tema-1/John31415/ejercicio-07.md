## Problema

Dada la mediana de dos arreglos ordenados de longitud $n$ (definida como el $n$-ésimo menor elemento de la unión de ambos conjuntos con $2n$ elementos en total):

1. Diseñe un algoritmo con complejidad temporal en $\mathcal{O}(\log n)$.
2. Demuestre formalmente su correctitud utilizando un invariante de ciclo.
3. Determine y justifique la cota de información del problema.

---

## Solución

### 1. Diseño del Algoritmo en $\mathcal{O}(\log n)$

Para encontrar el $k$-ésimo elemento (donde $k = n$ para el cálculo de la mediana) de dos arreglos ordenados $A$ y $B$ de tamaño $n$, implementamos una búsqueda binaria sobre el número de elementos $i$ que se toman del arreglo $A$. Al seleccionar $i$ elementos de $A$, debemos tomar de manera complementaria $j = k - i$ elementos de $B$ para completar los $k$ elementos de la mitad inferior.

#### Condición de Partición Válida

Buscamos un índice de corte $i \in [0, k]$ que satisfaga simultáneamente las restricciones de cruce:

1. $A[i-1] \le B[j]$
2. $B[j-1] \le A[i]$

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

> *Si existe una partición válida, su índice de partición correcto $i^*$ (que representa el número de elementos aportados por $A$ en la partición óptima) se encuentra siempre dentro del rango activo actual $[low, high]$.*

#### Demostración en Tres Fases

1. **Inicialización:**

Antes de la primera iteración, definimos:

$$low = \max(0, k-\vert{}B\vert{}), \qquad high = \min(k, \vert{}A\vert{}).$$

Estos límites garantizan que ambos arreglos puedan aportar exactamente $k$ elementos en conjunto, respetando sus respectivos tamaños. Por tanto, cualquier partición válida está inicialmente dentro del intervalo. El invariante se cumple.

2. **Mantenimiento:**

Asumimos que el invariante es válido antes de una iteración. Se calcula $i = \lfloor (low + high) / 2 \rfloor$ y $j = k - i$.

* **Caso $A[i-1] > B[j]$:** Estamos tomando demasiados elementos de $A$, por lo que cualquier partición válida debe tener un índice menor que $i$. Actualizamos $high = i - 1$. El invariante se preserva.
* **Caso $B[j-1] > A[i]$:** Estamos tomando demasiados elementos de $B$ y muy pocos de $A$, por lo que cualquier partición válida debe tener un índice mayor que $i$. Actualizamos $low = i + 1$. El invariante se preserva.
* **Caso $A[i-1] \le B[j]$ y $B[j-1] \le A[i]$:** Se ha encontrado una partición válida y el algoritmo retorna $\max(A[i-1], B[j-1])$.

3. **Terminación y Correctitud:**

Cuando se cumplen las dos condiciones de partición, los $k$ elementos seleccionados son exactamente los $k$ menores de la unión de ambos arreglos. Esto se debe a que cada arreglo está ordenado y las condiciones garantizan que ningún elemento de la mitad inferior sea mayor que uno de la mitad superior.

Por tanto, el mayor de los $k$ elementos seleccionados es:

$$\max(A[i-1],B[j-1]),$$

que constituye el elemento buscado.

Además, las condiciones de descarte permiten eliminar sistemáticamente los índices incorrectos sin descartar una partición válida. Como el intervalo de búsqueda se reduce en cada iteración y inicialmente contiene una partición válida, la búsqueda termina encontrándola. Así, el algoritmo es correcto y tiene complejidad temporal $\mathcal{O}(\log n)$.

---

### 3. Cota de Información

La cota de información para este problema es:

$$\boxed{\Omega(\log n)}$$

#### Justificación mediante un Árbol de Decisión

Para justificar la cota inferior, consideremos dos arreglos ordenados de longitud $n$, con elementos distintos. Fijemos:

$$A=\{1,2,\ldots,n\}.$$

Construimos distintas instancias del arreglo $B$, de manera que sus elementos se intercalen con los de $A$, conservando el orden interno de ambos arreglos.

Existen:

$$\binom{2n}{n}$$

intercalaciones posibles. Sin embargo, no todas producen valores diferentes para la mediana, por lo que contar directamente estas intercalaciones no permite demostrar una cota inferior de $\Omega(n)$.

Para obtener la cota deseada, consideremos las posibles posiciones de la mediana respecto a los elementos de ambos arreglos. Es posible construir una familia de instancias en la que cada una de las $n$ posiciones posibles de un elemento de $A$ respecto a la mediana produzca un caso que debe distinguirse mediante comparaciones.

En el modelo de comparación, un algoritmo puede representarse mediante un árbol de decisión binario, donde cada nodo interno corresponde a una comparación y cada hoja representa un resultado distinguible. Para resolver todas estas instancias, el árbol necesita al menos $n$ hojas. Por tanto, su profundidad en el peor caso debe satisfacer:

$$2^h \ge n.$$

De aquí se obtiene:

$$h \ge \lceil \log_2 n \rceil.$$

Por consiguiente, cualquier algoritmo basado en comparaciones necesita, en el peor caso:

$$\boxed{\Omega(\log n)}$$

comparaciones.

Así, junto con el algoritmo presentado, cuya complejidad temporal es $\mathcal{O}(\log n)$, se obtiene una complejidad óptima de:

$$\boxed{\Theta(\log n)}$$