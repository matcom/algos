# Ejercicio 5

## Definición del Problema y Algoritmo

Dado el nodo cabeza $head$ de una lista enlazada donde cada nodo $v$ tiene un único puntero $v.next$, determinar si existe un ciclo en la lista.

El **Algoritmo de Tortuga y Liebre de Floyd** utiliza dos punteros:

* $t$ (tortuga): avanza $1$ paso por iteración.

* $l$ (liebre): avanza $2$ pasos por iteración.

### Código formal

```
def tiene_ciclo(head):
    if head is None or head.next is None:
        return False
    
    t = head
    l = head
    
    while l is None and l.next is None:
        t = t.next
        l = l.next.next
        if t == l:
            return True
            
    return False

```

## Especificación Formal

Sea $G = (V, E)$ la estructura de la lista. Definimos el camino desde $head$ mediante la función sucesor $next(v)$.

* Si la lista **no tiene ciclo**, es una secuencia finita de $k \ge 0$ nodos distintos que termina en `None`.

* Si la lista **tiene ciclo**, consiste en un camino simple de longitud $u \ge 0$ desde $head$ hasta la entrada del ciclo, seguido de un ciclo simple de longitud $C \ge 1$.

* **Precondición:** $head$ es el puntero inicial de una lista enlazada válida (finita o con ciclo).

* **Postcondición:** Devuelve `True` si y solo si la lista contiene un ciclo; devuelve `False` en caso contrario.

## Demostración de Correctitud Parcial e Invariante

Queremos demostrar la equivalencia lógica: **Los punteros se encuentran (**$t = l$**) si y solo si hay un ciclo.**

### Caso 1: La lista NO tiene ciclo (Si $t = l \implies$ Hay ciclo)

Si la lista no tiene ciclo, es una secuencia finita de nodos. La liebre $l$ avanza el doble de rápido hacia `None`. El algoritmo simplemente alcanza `None` o `l.next == None` y retorna `False`. Por contradicción, si $t = l$ en algún nodo válido, se habría visitado un nodo dos veces desde la cabeza a distintas distancias, lo cual es imposible en un camino acíclico lineal. Por lo tanto, si retorna `True`, **necesariamente hay un ciclo**.

### Caso 2: La lista TIENE ciclo (Si hay ciclo $\implies t = l$)

Para demostrar que si hay un ciclo, la tortuga y la liebre se encontrarán en el mismo nodo dentro del ciclo, formulamos un **invariante de ciclo**.

#### Invariante de Ciclo

Sean $u \ge 0$ la longitud del prefijo acíclico y $C \ge 1$ la longitud del ciclo. Después de $i$ iteraciones del ciclo `while` (asumiendo que aún no ha terminado):

> *El puntero* $t$ *ha avanzado* $i$ *pasos desde* $head$*, y el puntero* $l$ *ha avanzado* $2i$ *pasos desde* $head$*. Además, si* $i \ge u$*, ambos punteros están dentro del ciclo y la distancia en sentido del ciclo desde* $t$ *hasta* $l$ *es de* $(i \bmod C)$ *nodos.*

#### Pasos de la demostración del Invariante:

**Inicialización (**$i = 0$**):**

   Antes de la primera vuelta, $t = head$ y $l = head$. Ambos han avanzado $0$ y $2(0) = 0$ pasos respectivamente. Si $u = 0$, ambos están al inicio del ciclo a una distancia $0 \bmod C = 0$. El invariante se cumple.

**Mantenimiento (**$i \to i + 1$**):**

   Supongamos que el invariante se cumple tras la iteración $i$. En la iteración $i+1$:

   * $t$ avanza a $t.next$, completando $i + 1$ pasos desde $head$.

   * $l$ avanza a $l.next.next$, completando $2(i + 1)$ pasos desde $head$.

   * Si $i + 1 \ge u$, ambos punteros se desplazan dentro del ciclo de longitud $C$. La distancia desde $t$ hasta $l$ medida en pasos a lo largo del ciclo es:
     

     $$
     d_{i+1} = (2(i + 1) - (i + 1)) \bmod C = (i + 1) \bmod C
     $$

     
     Se mantiene la propiedad inductiva.

**Conclusión:**

   Considere la iteración $i = u + (C - (u \bmod C)) \bmod C$. Para esta vuelta (o a lo sumo en la vuelta $i = u + C$), tenemos que $i \ge u$, luego ambos punteros están dentro del ciclo. La distancia relativa entre $l$ y $t$ es:
   

   $$
   d_i = i \bmod C
   $$

   
   Como podemos seleccionar un múltiplo de $C$ tal que $i \equiv 0 \pmod C$, existe un número finito de pasos $i \le u + C$ donde $(i \bmod C) = 0$. En ese momento $t$ y $l$ apuntan exactamente al mismo nodo, la condición de parada $t == l$ se satisface y el algoritmo retorna `True`.

## Terminación por Potencial

Para acotar el número de iteraciones y demostrar que el programa **siempre termina** (incluso en presencia de ciclos infinitos), definimos una función de potencial $\Phi: \text{Estado} \to \mathbb{Z}_{\ge 0}$.

Analizamos dos situaciones:

### Situación A: La lista NO tiene ciclo

Sea $N$ el número total de nodos de la lista acíclica.

* **Potencial:** $\Phi_A = N - \text{pasos}(l)$, donde $\text{pasos}(l)$ es el número de nodos avanzados por la liebre $l$.

* **Propiedades:**

  1. $\Phi_A \ge 0$ pues $l$ no puede avanzar más allá del final de la lista de tamaño $N$.

  2. En cada iteración, $l$ avanza $2$ posiciones, por lo que $\Phi_A$ decrece al menos en $2$ unidades (o $1$ en la última iteración).

  3. Al ser una cantidad entera estrictamente decreciente acotada inferiormente por $0$, el ciclo termina en a lo sumo $\lceil N/2 \rceil$ vueltas.

### Situación B: La lista TIENE ciclo

Sea $u$ la longitud del prefijo lineal y $C$ el tamaño del ciclo.

* **Potencial:**
  

  $$
  \Phi_B = \begin{cases} 2u - \text{pasos}(t) + C & \text{si } t \text{ no ha entrado al ciclo } (\text{pasos}(t) < u) \\ (C - (d \bmod C)) \bmod C & \text{si } t \text{ ya está en el ciclo } (\text{pasos}(t) \ge u) \end{cases}
  $$

  
  donde $d = \text{pasos}(l) - \text{pasos}(t)$ es la distancia recorrida de ventaja de $l$.

* **Propiedades:**

  1. $\Phi_B \ge 0$ por definición (es una distancia en un espacio discreto acotada por $C$).

  2. Mientras $t$ esté fuera del ciclo, en cada paso $\text{pasos}(t)$ aumenta en $1$, reduciendo $\Phi_B$.

  3. Una vez $t$ entra al ciclo, en cada iteración la liebre $l$ corta la distancia con $t$ en $1$ posición (ya que avanza $2$ mientras $t$ avanza $1$). Por lo tanto, el gap o separación decrece estrictamente en $1 \pmod C$ en cada vuelta.

  4. Dado que es un entero no negativo decreciente, alcanzará $\Phi_B = 0$ (momento en el que $t == l$) en una cantidad finita de pasos.

## Análisis de Complejidad y Cota

* **Complejidad Temporal:** $O(N)$

  * **Caso sin ciclo:** La liebre alcanza el final en $\le \lceil N/2 \rceil$ iteraciones. Cueste lo que cueste $N$, realiza $O(N)$ operaciones.

  * **Caso con ciclo:** La tortuga tarda $u$ pasos en llegar a la entrada del ciclo. En ese instante, la liebre está en alguna posición dentro del ciclo. A partir de ahí, la liebre tarda a lo sumo $C - 1$ pasos adicionales en alcanzar a la tortuga.

  * Número total de iteraciones $k \le u + C \le N$.

  * Cada iteración realiza un número constante $\mathcal{O}(1)$ de comparaciones y asignaciones de punteros.

  * **Tiempo Total:** $O(N)$ en el peor de los casos.

* **Complejidad Espacial (Memoria Auxiliar):** $O(1)$

  * Solo se requiere almacenar dos punteros auxiliares ($t$ y $l$), independientemente de la longitud de la lista $N$.

* **Cota Mínima:** Cota inferior $\Omega(N)$ en el peor de los casos, dado que cualquier algoritmo determinista debe inspeccionar al menos los punteros hasta la entrada del ciclo/final para no dar una respuesta errónea. El algoritmo de Floyd alcanza la cota óptima en tiempo lineal y memoria constante.