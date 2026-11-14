# Ejercicio 7

## El Problema 
### Enunciado Preciso
Dados dos arreglos ordenados $A$ y $B$, cada uno de longitud $n$, determinar el $n$-ésimo menor elemento del multiconjunto de tamaño $2n$ formado por los elementos de $A$ y $B$.

* **Entrada:** Dos arreglos $A[0 \dots n-1]$ y $B[0 \dots n-1]$, ambos ordenados de forma no decreciente ($A[0] \le A[1] \le \dots \le A[n-1]$ y $B[0] \le B[1] \le \dots \le B[n-1]$).
* **Salida:** El elemento que ocuparía el índice $n-1$ (indexación basada en 0) si $A$ y $B$ se fusionaran en una única secuencia ordenada de longitud $2n$.
* **Modelo de Cómputo:** Modelo de comparaciones (Conferencia 5). Acceso a los datos únicamente mediante preguntas relativas del tipo $A[i] \le B[j]$.

---

## El Algoritmo 

### Idea Algorítmica
Aplicamos **Divide y Vencerás** expresado de forma iterativa sobre un intervalo de búsqueda dinámico $[la \dots ra]$ en $A$ y $[lb \dots rb]$ en $B$. En todo momento mantenemos un número igual de elementos activos en ambos subarreglos ($ra - la + 1 = rb - lb + 1 = k$).

Comparamos las medianas de las regiones activas de $A$ y $B$:
1. Si $A[m_A] == B[m_B]$, esa mediana común es el elemento buscado.
2. Si $A[m_A] < B[m_B]$, los elementos $A[la \dots m_A]$ son demasiado pequeños para ser la mediana global, y los elementos $B[m_B \dots rb]$ son demasiado grandes. Descartamos ambas secciones simultáneamente.
3. Si $A[m_A] > B[m_B]$, descartamos la mitad superior de $A$ y la mitad inferior de $B$.

### Pseudocódigo Iterativo (`mediana_dos_arreglos`)

```python
def mediana_dos_arreglos(A, B):
    n = len(A)
    la, ra = 0, n - 1
    lb, rb = 0, n - 1
    
    while ra - la + 1 > 2:
        k = ra - la + 1
        ma = (la + ra) // 2
        mb = (lb + rb) // 2
        
        # Cantidad de elementos descartables por extremo
        d = (k - 1) // 2
        
        if A[ma] == B[mb]:
            return A[ma]
        elif A[ma] < B[mb]:
            la = la + d
            rb = rb - d
        else:
            ra = ra - d
            lb = lb + d
            
    # Caso base explícito cuando quedan 1 o 2 elementos por subarreglo
    k = ra - la + 1
    if k == 1:
        return min(A[la], B[lb])
    else:  # k == 2
        # El 2do menor entre A[la], A[ra], B[lb], B[rb]
        return max(A[la], B[lb])
```

---

## Demostración de Correctitud 

De acuerdo con la **Conferencia 3**, demostramos por separado la **Correctitud Parcial** (mediante Invariante de Ciclo) y la **Terminación** (mediante Potencial).

### Especificación
* **Precondición:** $A[0 \dots n-1]$ y $B[0 \dots n-1]$ están ordenados y tienen longitud $n \ge 1$.
* **Postcondición:** El algoritmo retorna el $n$-ésimo menor elemento de $A \cup B$.

---

### Invariante de Ciclo (Correctitud Parcial)

Definimos el Invariante $I$ al inicio de cada iteración del ciclo `while`:

> **Invariante $I$:**
> 1. Los rangos activos tienen longitudes iguales: $ra - la + 1 = rb - lb + 1 = k \ge 1$.
> 2. Se han descartado exactamente $la$ elementos por la izquierda de $A$ y $(n - 1 - rb)$ elementos por la derecha de $B$ (o viceversa), cumpliendo que la suma de elementos descartados por la izquierda en $A$ y $B$ es igual a la suma de elementos descartados por la derecha:
>    $$la + lb = (n - 1 - ra) + (n - 1 - rb)$$
> 3. El $n$-ésimo menor elemento de la entrada original $A[0 \dots n-1] \cup B[0 \dots n-1]$ es el $k$-ésimo menor elemento de la unión de los rangos activos $A[la \dots ra] \cup B[lb \dots rb]$.

---

#### Inicialización
Antes de la primera vuelta:
* $la = 0, ra = n - 1 \implies ra - la + 1 = n$.
* $lb = 0, rb = n - 1 \implies rb - lb + 1 = n$.
* Ambas longitudes son $k = n$, satisfaciendo la condición 1.
* Los elementos descartados por los extremos son $0$: $la + lb = 0 + 0 = 0$ y $(n - 1 - ra) + (n - 1 - rb) = 0 + 0 = 0$, satisfaciendo la condición 2.
* El rango activo es la totalidad de los arreglos $A$ y $B$. El $n$-ésimo menor de $A \cup B$ es por definición el $n$-ésimo menor del rango activo. Se satisface la condición 3.

#### Mantenimiento
Supongamos que el invariante $I$ se cumple antes de una iteración donde $k = ra - la + 1 > 2$. Sean $m_A = \lfloor (la + ra) / 2 \rfloor$ y $m_B = \lfloor (lb + rb) / 2 \rfloor$. La cantidad descartable por extremo es $d = \lfloor (k - 1) / 2 \rfloor \ge 1$.

* **Si $A[m_A] == B[m_B]$:**
  * En $A[la \dots ra]$, hay exactamente $(m_A - la)$ elementos estrictamente menores que $A[m_A]$.
  * En $B[lb \dots rb]$, hay exactamente $(m_B - lb)$ elementos estrictamente menores o iguales que $B[m_B]$.
  * Como $m_A - la = \lfloor (k-1)/2 \rfloor$ y $m_B - lb = \lfloor (k-1)/2 \rfloor$, la cantidad total de elementos menores o iguales a $A[m_A]$ dentro del rango activo es:
    $$(m_A - la) + (m_B - lb) + 1 = 2 \cdot \left\lfloor \frac{k-1}{2} \right\rfloor + 1$$
  * Sumando los $la + lb$ elementos descartados a la izquierda (que por hipótesis inductiva son todos $\le$ a los activos), $A[m_A]$ resulta tener exactamente $la + lb + k - 1 = n - 1$ elementos menores o iguales a él en la unión global.
  * Por tanto, $A[m_A]$ es el $n$-ésimo menor elemento y el algoritmo finaliza retornando la respuesta correcta.

* **Si $A[m_A] < B[m_B]$:**
  * El algoritmo actualiza $la' = la + d$ y $rb' = rb - d$.
  * **Verificación de Condición 1:** $ra - la' + 1 = (ra - la + 1) - d = k - d$. $rb' - lb + 1 = (rb - lb + 1) - d = k - d$. Ambos rangos reducidos mantienen la misma longitud $k' = k - d$.
  * **Verificación de Condición 2:** Los descartes agregados son $d$ por la izquierda en $A$ y $d$ por la derecha en $B$. La suma de descartes por la izquierda pasa a ser $la' + lb = la + lb + d$, y por la derecha $(n - 1 - ra) + (n - 1 - rb') = (n - 1 - ra) + (n - 1 - rb) + d$. Ambas sumas continúan siendo iguales.
  * **Verificación de Condición 3 (Descarte Válido):**
    * Todos los elementos $A[la \dots la+d-1]$ son $\le A[m_A] < B[m_B]$. Hay al menos $d$ elementos en $A$ y $(rb - m_B + 1)$ elementos en $B$ que son $\ge B[m_B]$. En consecuencia, ningún elemento en $A[la \dots la+d-1]$ puede tener suficientes elementos superiores para llegar a ser el $k$-ésimo menor en el conjunto activo.
    * De forma simétrica, todos los elementos $B[rb-d+1 \dots rb]$ son $\ge B[m_B] > A[m_A]$, haciendo imposible que pertenezcan a los primeros $k$ menores.
    * Descartar $d$ elementos menores por un extremo y $d$ elementos mayores por el otro desplaza la posición del objetivo relativo en el rango activo a $k' = k - d$.

* **Si $A[m_A] > B[m_B]$:**
  * Por simetría exacta con el caso anterior, se actualizan $ra' = ra - d$ y $lb' = lb + d$, conservando la validez del invariante $I$.

En todos los casos, el invariante $I$ **se mantiene verdadero para la siguiente iteración**.



#### Conclusión
El ciclo termina cuando la condición de salida $ra - la + 1 \le 2$ se satisface.
Al terminar el ciclo, por la condición 3 del invariante $I$, sabemos que el problema original se reduce a encontrar el $k$-ésimo menor elemento en $A[la \dots ra] \cup B[lb \dots rb]$, donde $k \in \{1, 2\}$:

1. **Si $k = 1$:** La unión activa tiene 2 elementos: $\{A[la], B[lb]\}$. El 1-er menor de 2 elementos es $\min(A[la], B[lb])$. El algoritmo retorna exactamente este valor.
2. **Si $k = 2$:** La unión activa tiene 4 elementos: $A[la] \le A[ra]$ y $B[lb] \le B[rb]$. El $2$-do menor de estos 4 elementos ordenados por parejas no puede ser ni $\min(A[la], B[lb])$ (que es el 1-er menor) ni $\max(A[ra], B[rb])$ (que es el 4-to menor). Por ende, el 2-do menor elemento de la unión activa es $\max(A[la], B[lb])$. El algoritmo devuelve este valor.

Por lo tanto, la respuesta devuelta por el algoritmo cumple con la postcondición. $\blacksquare$

---

### Terminación (Demostración por Potencial)

Sea $\Phi(la, ra) = ra - la + 1 = k$ la función de potencial definida sobre las variables de estado del ciclo.

1. **Entero y No Negativo:** Puesto que $ra \ge la$ mientras el ciclo se ejecuta, $\Phi \in \mathbb{Z}^+$.
2. **Decrecimiento Estricto:** En cada vuelta del ciclo donde $k > 2$, se descartan $d = \lfloor (k - 1) / 2 \rfloor \ge 1$ elementos. El nuevo potencial pasa a ser:
   $$\Phi' = k - d = k - \left\lfloor \frac{k - 1}{2} \right\rfloor = \left\lceil \frac{k + 1}{2} \right\rceil$$
   Para todo $k > 2$, se cumple estrictamente que $\Phi' < k$.

---


## Análisis de Complejidad 

1. **Tiempo:** 
   En cada paso del ciclo hacemos $O(1)$ comparaciones e incrementos de índices, y el rango activo de tamaño $k$ se reduce a $k' \le \lceil (k+1)/2 \rceil$.
   
   Escribiendo el árbol de ejecución (como en la Conferencia 2):
   * Nivel 0: Tamaño $n$, costo $O(1)$
   * Nivel 1: Tamaño $n/2$, costo $O(1)$
   * Nivel 2: Tamaño $n/4$, costo $O(1)$
   * $\dots$
   * Nivel $\log_2 n$: Tamaño $1$, costo $O(1)$

   Hay a lo sumo $\lfloor \log_2 n \rfloor + 1$ niveles, y cada nivel realiza un número constante de operaciones. Sumando el trabajo a lo largo de los niveles:
   $$T(n) = \sum_{i=1}^{\lceil \log_2 n \rceil} O(1) = O(\log n)$$

2. **Memoria:** 
   El algoritmo es puramente iterativo y solo almacena $O(1)$ variables enteras (`la`, `ra`, `lb`, `rb`, `ma`, `mb`, `d`, `k`).
   $$M(n) = O(1)$$


---

## Cota de Información

Siguiendo las metodologías de la **Conferencia 5**, analizamos la cota mínima de comparaciones mediante el modelo de árboles de decisión.

### Teorema
Todo algoritmo en el modelo de comparaciones que determine el $n$-ésimo menor elemento de dos arreglos ordenados de tamaño $n$ requiere **al menos $\Omega(\log n)$ comparaciones** en el peor caso.

### Demostración (Argumento de Información)
1. **Espacio de Salidas Posibles:** Consideremos el conjunto de entradas donde todos los elementos de $A$ y $B$ son distintos. El $n$-ésimo menor elemento global puede ser cualquier elemento de $A[0 \dots n-1]$ o cualquier elemento de $B[0 \dots n-1]$. Existen $2n$ posibles respuestas para la salida del algoritmo.
2. **Altura del Árbol de Decisión:** Un algoritmo de comparaciones correcto debe asociar cada respuesta a una hoja de su árbol de decisión binario. Por tanto, el árbol de decisión debe tener al menos $L \ge 2n$ hojas.
3. **Cota de la Altura:** Por el Lema 1 de la Conferencia 5, un árbol de decisión binario de altura $h$ (donde $h$ representa el número de comparaciones en el peor caso) tiene a lo sumo $2^h$ hojas. Por consiguiente:
   $$2^h \ge L \ge 2n \implies h \ge \log_2(2n) = \log_2 n + 1$$

Esto demuestra que el peor caso requiere al menos $\lceil \log_2 n + 1 \rceil \in \Omega(\log n)$ comparaciones.
