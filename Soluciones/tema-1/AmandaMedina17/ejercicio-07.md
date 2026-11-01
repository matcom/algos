**Problema:** Tenemos  dos arreglos, $A$ y $B$, ambos ordenados de menor a mayor, cada uno con longitud $n$. Queremos encontrar el $n$-ésimo menor elemento de la combinación de ambos (la mediana).

# Diseño del algoritmo
**Fuerza bruta:**
* Podríamos juntar los dos arreglos en uno solo ordenado y buscar el índice $n$. Pero eso tomaría $O(n)$ pasos porque tendríamos que mirar una cantidad lineal de elementos. Entones, ¿cómo podríamos obtener una velocidad logarítmica? Usaremos Divide y Vencerás, descartando mitades como en una búsqueda binaria.

* ¿Qué pasa si miramos los puntos medios de ambos arreglos? Supongamos que tomamos el punto medio del arreglo $A$ (lo llamaremos $mid_A$) y el punto medio del arreglo $B$ (lo llamaremos $mid_B$). Estos puntos medios dividen a cada arreglo en dos partes: la mitad izquierda con los elementos más pequeños y la mitad derecha con los elementos más grandes.

* Entonces, supongamos que estamos buscanodo el $k$-ésimo elemento menor (que en caso de la mediana k=n). Comparamos el valor de $A[\text{mid}_A]$ con el valor de $B[\text{mid}_B]$:
- Caso $A[\text{mid}_A]$ < $B[\text{mid}_B]$: Esto indica que todos los elementos que están a la izquierda de $mid_A$ en el arreglo $A$ son más pequeños que $B[\text{mid}_B]$ y que los elementos de la derecha de $mid_B$. Luego, podemos estar seguros de que esos elementos de la mitad izquierda de $A$, incluyendo a $A[\text{mid}_A]$, son demasiado pequeños para ser el $n$-ésimo elemento que buscamos y podemos descartalos.
- Caso $A[\text{mid}_A]$ >= $B[\text{mid}_B]$: Análogamente ocurre lo contrario del caso anterior, los elementos de la izquierda de $mid_B$ son menores y podemos descartarlos.

* Cada vez que descartamos una mitad el problema se hace más pequeño. Como ya sabemos cuantos elementos descartamos por debajo del valor que buscamos, actualizamos nuestro objetivo $k$ restándole la cantidad de elementos descartados. Y repetimos el mismo proceso con los subarreglos restantes.

* Este ciclo de recortar mitades continua reduciendo el tamaño del problema de forma exponencial. El algoritmo se detiene cuando:
    - Uno de los arreglos se queda vacío: Si esto pasa, significa que el $k$-ésimo menor (la mediana) solo ouede estar en el otro arreglo.
    - O el índice $k$ que buscamos se reduce a 1, que entonces la mediana sería el elemento más pequeño de ambos arreglos.

* Complejidad Temporal: Como en cada paso recursivo se desecha la mitad de uno de los arreglos, la recurrencia es  $T(n) = T(n/2) + \mathcal{O}(1)$, lo que por el Teorema Maestro resulta en un costo de $O(logn)$.

**Ver imagen en k_esimo_menor_medios.png**

**Ver implementación en find_kth_smallest.py**

# Demostración de correctitud y terminación:
## 1. Invariante de ciclo:
* El elemento $k$-ésimo menor global de los arreglos originales $A$ y $B$ coincide exactamente con el $k$-ésimo menor elemento de la unión de los subarreglos actuales $A[\text{lo}_A...\text{hi}_A]$ y $B[\text{lo}_B...\text{hi}_B]$. Ademas, $1 \le k \le (\text{hi}_A - \text{lo}_A + 1) + (\text{hi}_B - \text{lo}_B + 1)$.

**Demostración por inducción:**

**Caso Base:** Al comenzar la primera iteración se cumple que:
-  $\text{lo}_A = 0, \text{hi}_A = n - 1$
-  $\text{lo}_B = 0, \text{hi}_B = n - 1$
-  $\text{k} = \text{n}$

Los subarreglos actuales son $A$ y $B$ completos. Por tanto, el $n$-ésimo elemento de la unión de ambos, es el $n$-ésimo elemento global. El invariante se cumple.

**Paso inductivo:**
 
 Asumimos que el invariante de cumple al inicio de una iteración. Se calculan los índices medios  $\text{m}_A = \text{lo}_A + \lfloor k/2 \rfloor - 1$ y $\text{m}_B = \text{lo}_B + \lfloor k/2 \rfloor - 1$ y se evalúa $A[\text{m}_A]$ frente a $B[\text{m}_B]$:
- Caso $A[\text{m}_A]$ < $B[\text{m}_B]$: en el subarreglo actual de $A$, hay exactamente $\text{m}_A - \text{lo}_A + 1 = \lfloor k/2 \rfloor$ elementos en el segmento $A[\text{lo}_A \dots \text{m}_A]$. Como $A[\text{m}_A]$ < $B[\text{m}_B]$ y ambos arreglos están ordenados, todos los elementos de $A[\text{lo}_A \dots \text{m}_A]$ son estrictamentre menores que al menos $B[\text{lo}_B \dots \text{m}_B]$. Por ende, ningún elemento del segmento $A[\text{lo}_A \dots \text{m}_A]$ puede ocupar una posición mayor o igual a $k$ en la unión ordenada y es seguro descartar ese bloque actualizando $\text{lo}_A = \text{m}_A + 1$. Para mantener el invariante, restamos la cantidad de elementos descartados al objetivo: $k_{\text{nuevo}} = k - \lfloor k/2 \rfloor$.
- Caso $A[\text{m}_A] \ge B[\text{m}_B]$: Por simetría con el caso anterior, los elementos de $B[\text{lo}_B \dots \text{m}_B]$ son demasiado pequeños para ser el $k$-ésimo elemento global. Descartamos dicho segmento haciendo  $\text{lo}_B = \text{m}_B + 1$ y actualizamos $k_{\text{nuevo}} = k - \lfloor k/2 \rfloor$.

El algoritmo concluye en alguno de sus casos base:

- Si $A$ o $B$ queda vacío: si $A$ se queda sin elementos, el invariante garantiza que el objetivo es el elemento en la posición  $\text{lo}_B + k - 1$ de $B$ de B.
- Si $k=1$: Por el invariante, el elemento buscado debe ser el menor de la unión de los subarreglos actuales actualizados.

## 2. Demostración de terminación:
Para demostrar que el algoritmo siempre termina , aplicamos una función de potencial $\Phi = k$ (donde $k$ representa el orden relativo restante del elemento buscado). Este potencial esta acotado inferiormente por un valor no negativo, ya que durante toda la ejecución se cumple que $k \ge 1$. Además, en cada iteración del ciclo, descartamos al menos un bloque de tamaño $\lfloor k/2 \rfloor \ge 1$, por tanto el potencial decrece estrictamente en cada paso. Dado que $\Phi$ es una secuencia de números enteros estrictamente decreciente y acotada inferiormente por 1, es imposible que el ciclo se ejecute infinitamente.

# Cota mínima por información:
Demostremos que matemáticamente ningún algoritmo basado en comparaciones puede resolver este problema.
* En el modelo de comparaciones, cualquier algoritmo que resuelva el problema de encontrar en $n$-ésimo elemento de dos arreglos ordenados $A$ y $B$ puede ser representado como un árbol de decisión binario. Cada nodo del árbol representa una comparación entre un elemento de $A$ y un elemento de $B$, por ejemplo, $A[i] < B[j]$. Cada hoja representa una conclusión del algoritmo. El costo en el peor caso del algoritmo corresponde a la altura $h$ del árbol.
* Dados dos arreglos ordenados de tamaño $n$, existen múltiples configuraciones válidas de entrelazamiento que preservan el orden interno de cada secuencia. Para aislar con éxito el $n$-ésimo elemento global, el algoritmo debe ser capaz de distinguir entre estas posibles estructuras de orden relativo.
* Un árbol de decisión binario de altura $h$ puede poseer a lo sumo $2^h$ hojas (resultados posibles).Para que el algoritmo sea correcto ante cualquier instancia válida de los arreglos, el número de hojas debe ser al menos igual al número de configuraciones distinguibles del problema, el cual crece de forma exponencial con respecto al tamaño de los arreglos ($2^h \ge \text{Configuraciones}$). Aplicando logaritmo en base $2$ en ambos miembros de la desigualdad para despejar la altura $h$ (el número de comparaciones en el peor caso):$$h \ge \log_2(\text{Configuraciones}) = \Omega(\log n)$$