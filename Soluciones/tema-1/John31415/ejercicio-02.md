## Problema

Dé el invariante y la función potencial del algoritmo de búsqueda binaria, así como la cota de información que demuestra su optimalidad teórica.

---

## Solución

### 1. Cota de Información (Óptimo Teórico)

La **cota de información** (o cota inferior basada en el árbol de decisión) determina el número mínimo de comparaciones que cualquier algoritmo basado en comparaciones debe realizar en el peor de los casos para resolver el problema de búsqueda.

#### Análisis del Espacio de Resultados

Cuando buscamos un elemento en un arreglo ordenado de tamaño $N$, existen exactamente **$N + 1$ resultados posibles**:

* El elemento se encuentra en una de las $N$ posiciones válidas ($0, 1, 2, \dots, N-1$).
* El elemento no se encuentra en el arreglo ($1$ única posibilidad de fracaso).

#### Modelado mediante Árbol de Decisiones

Cada comparación binaria realizada por el algoritmo (por ejemplo, ¿es $A[\text{mid}] < x$?) bifurca el flujo en dos posibles respuestas: **Sí** o **No**. Esto se representa formalmente como un árbol de decisión binario, donde cada nodo interno es una comparación y cada hoja representa un resultado posible:

```text
                 ¿A[mid] == x?
                 /           \
             (Sí)             (No)
           Retorna        ¿A[mid] < x?
           posición       /          \
                      (Sí)            (No)
                   Buscar          Buscar
                   derecha        izquierda

```

Para poder distinguir de forma unívoca entre los $N + 1$ resultados posibles, el árbol binario de decisiones debe poseer al menos $N + 1$ hojas. Si denotamos como $h$ a la altura del árbol (que representa la cantidad máxima de comparaciones en el peor de los casos):

$$2^h \ge N + 1 \implies h \ge \lceil \log_2(N + 1) \rceil$$

#### Conclusión sobre la Optimalidad

La cota de información para la búsqueda es $\Omega(\log N)$. Ningún algoritmo basado en comparaciones puede resolver el problema en menos de $\lceil \log_2(N + 1) \rceil$ comparaciones en el peor de los casos. Dado que la **búsqueda binaria** particiona el espacio de búsqueda a la mitad en cada iteración, alcanza esta cota en un tiempo de $\mathcal{O}(\log N)$, demostrando formalmente que es un **algoritmo óptimo**.

---

### 2. Algoritmo de Referencia

```python
def binary_search(A, x):
    low = 0
    high = len(A) - 1
    while low <= high:
        mid = (low + high) // 2
        if A[mid] == x:
            return mid          # Éxito: encontrado
        elif A[mid] < x:
            low = mid + 1       # Descartar mitad izquierda
        else:
            high = mid - 1      # Descartar mitad derecha
    return -1                   # Fracaso: no existe

```

---

### 3. Invariante del Ciclo (Correctitud Parcial)

#### Declaración del Invariante ($I$)

> *"Si el elemento buscado $x$ existe en el arreglo $A$, entonces su índice debe pertenecer necesariamente al rango activo $[\text{low}, \text{high}]$."*

Formalmente:


$$x \in A[0 \dots N-1] \implies x \in A[\text{low} \dots \text{high}]$$

#### Demostración en Tres Fases

1. **Inicialización:**
Antes de entrar al ciclo por primera vez, $\text{low} = 0$ y $\text{high} = N - 1$. El subarreglo activo $A[\text{low} \dots \text{high}]$ coincide idénticamente con todo el arreglo $A[0 \dots N-1]$. Por ende, si $x$ está en el arreglo, trivialmente pertenece a este rango inicial. El invariante se cumple.
2. **Mantenimiento:**
Asumimos que el invariante es verdadero antes de una iteración. Durante el ciclo se calcula $\text{mid} = \lfloor (\text{low} + \text{high}) / 2 \rfloor$ y se evalúan tres casos:
* **Caso $A[\text{mid}] == x$:** El algoritmo halla el elemento y retorna $\text{mid}$ inmediatamente (correctitud por éxito).
* **Caso $A[\text{mid}] < x$:** Dado que el arreglo está ordenado crecientemente, todos los elementos desde $A[\text{low}]$ hasta $A[\text{mid}]$ son menores o iguales a $A[\text{mid}]$, y por tanto estrictamente menores que $x$. Esto descarta el subintervalo $[\text{low}, \text{mid}]$. Si $x$ existe en el arreglo, debe encontrarse en $[\text{mid} + 1, \text{high}]$. Al actualizar $\text{low} = \text{mid} + 1$, el nuevo rango $[\text{low}_{\text{nuevo}}, \text{high}]$ preserva la validez del invariante.
* **Caso $A[\text{mid}] > x$:** De forma análoga, todos los elementos desde $A[\text{mid}]$ hasta $A[\text{high}]$ son estrictamente mayores que $x$, descartando el subintervalo $[\text{mid}, \text{high}]$. Actualizar $\text{high} = \text{mid} - 1$ mantiene el invariante en el nuevo rango.


3. **Conclusión:**
El ciclo concluye cuando la condición de guarda deja de cumplirse, es decir, cuando $\text{low} > \text{high}$. En este punto, el rango $[\text{low}, \text{high}]$ se ha reducido a un conjunto vacío. Por el invariante, esto implica que si $x \in A$, debería pertenecer a un arreglo vacío, lo cual es una contradicción lógica. Por lo tanto, se deduce con certeza que $x \notin A$, validando la correctitud de retornar $-1$.

---

### 4. Función Potencial (Demostración de Terminación)

La función potencial $\Phi$ cuantifica el tamaño del espacio de búsqueda restante, permitiendo demostrar formalmente que el ciclo no entra en un bucle infinito.

#### Definición de $\Phi$

$$\Phi(\text{low}, \text{high}) = \max(0, \text{high} - \text{low} + 1)$$

#### Propiedades y Decrecimiento Estricto

1. **Entera y no negativa ($\Phi \ge 0$):**
Mediante la función $\max(0, \dots)$, se garantiza que $\Phi \ge 0$. Puesto que $\text{low}$ y $\text{high}$ son enteros, $\Phi$ siempre toma valores enteros no negativos ($\Phi \in \mathbb{Z}_{\ge 0}$).
2. **Decrecimiento estricto por iteración:**
En cada iteración válida ($\text{low} \le \text{high}$), el índice medio se define como $\text{mid} = \lfloor (\text{low} + \text{high}) / 2 \rfloor$, satisfaciendo $\text{low} \le \text{mid} \le \text{high}$. Al actualizar los punteros:
* Si se toma la rama $\text{low}_{\text{nuevo}} = \text{mid} + 1$:

$$\text{high} - \text{low}_{\text{nuevo}} + 1 = \text{high} - (\text{mid} + 1) + 1 = \text{high} - \text{mid}$$



Dado que $\text{mid} \ge \text{low}$, se cumple que $\text{high} - \text{mid} < \text{high} - \text{low} + 1$.
* Si se toma la rama $\text{high}_{\text{nuevo}} = \text{mid} - 1$:

$$\text{high}_{\text{nuevo}} - \text{low} + 1 = (\text{mid} - 1) - \text{low} + 1 = \text{mid} - \text{low}$$



Dado que $\text{mid} \le \text{high}$, se cumple que $\text{mid} - \text{low} < \text{high} - \text{low} + 1$.



En ambas ramas, el tamaño del espacio de búsqueda decrece estrictamente cumpliendo:


$$\Phi_{\text{siguiente}} \le \left\lfloor \frac{\Phi_{\text{actual}}}{2} \right\rfloor < \Phi_{\text{actual}}$$

#### Conclusión de Terminación

Como $\Phi$ representa una secuencia de enteros no negativos estrictamente decreciente ($\Phi_0 > \Phi_1 > \Phi_2 > \dots \ge 0$), la ejecución del ciclo no puede extenderse infinitamente. El número total de iteraciones está acotado superiormente por su valor inicial $\Phi_0 = N - 0 + 1 = N + 1$. Al reducirse al menos a la mitad en cada paso, el algoritmo garantiza su terminación en un máximo de $\lceil \log_2(N + 1) \rceil$ iteraciones.