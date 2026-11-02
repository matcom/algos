**Problema:**  Da el invariante y el potencial de la búsqueda binaria, y la cota de información que la hace óptima.

Para la búsqueda binaria de una clave $x$ en un arreglo ordenado $A[0...n-1]$, el algoritmo mantiene dos índices $lo$ y $hi$ que delimitan la región de búsqueda.

```python
def busqueda_binaria(A, x):
    lo, hi = 0, len(A) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if A[mid] == x:
            return mid
        elif A[mid] < x:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
```

## 1. Invariante del ciclo

El invariante garantiza que si el elemento $x$ está contenido en $A$, debe encontrarse en el rango actual de índices $[lo, hi]$.

> Si $x$ pertenece $A$, entonces existe un $i$ que pertene a $[lo, hi]$ tal que $A[i]=x$.

**Demostración:**

1. **Caso Base:**
Inicialmente $lo = 0$ y $hi = n-1$. El rango $[lo, hi]$ cubre la totalidad del arreglo $A[0...n-1]$. Por tanto, si $x$ pertenece a $A$, tiene que estar en el rango $[0, n-1]$. El invariante se cumple.

2. **Paso Inductivo:**

Se calcula  $mid = \lfloor (lo+hi)/2 \rfloor$. 
* Si $A[mid] == x$, retornamos la posición y termina correctamente. 
* Si $A[mid] < x$, dado que $A$ esta ordenado, para todo $j< mid$ se cumple que $A[j] \le A[mid]$. Por tanto, $x$ no puede estar en $[lo, mid]$, la única manera de que $x$ pertenezca a $A$ es que esté en $[mid+1, hi]$. Luego al hacer $lo = mid+1$ la invariante se preserva.
* Si $A[mid]>x$, análogamente $x$ no puede estar en $[mid, hi]$. Se actualiza $hi = mid -1$, preservando la invariente en $[lo, mid-1]$.

3. **Conclusión:**
El ciclo termina cuando se encuentra $x$, retornando el índice, o cuando $[lo,hi]$ se vuelve vacío. Por el invariante, si $x$ estuviera en $A$ debería estar en un intervalo vacío, lo que no es posible, entonces retorna $-1$ ya que $x$ no pertenece a $A$.

## 2.Potencial:

Para demostrar que el algoritmo termina, sea $\Phi$ la distancia entre $lo$ y $hi$, que representa la cantidad de elementos restantes en el rango de búsqueda.

**Propiedades del potencial:**

1. **Acotado inferiormente:** El ciclo continua únicamente mientras $lo \le hi$, lo que implica que en cada iteración del ciclo $\Phi \ge 1$ y se detiene cuando $\Phi \le 0$.
2. **Decrecimiento estricto:** En cada iteración del ciclo, el nuevo rango se reduce a la mitad. Si la actualización es $lo = mid +1$, el nuevo potencial es $hi - mid \le \Phi/2 < \Phi$. Si la actualización es $hi = mid - 1$, el nuevo potencial es $mid - lo \le \Phi/2 < \Phi$.

Como $\Phi$ es una secuencia de enteros no negativos que decrece estrictamente en cada iteración, entonces el algoritmo termina en a lo sumo $\lfloor \log n \rfloor +1$ pasos. 

## 3. Cota de informacion que la hace óptima:

Para demostrar que la búsqueda binaria es óptima, utilizaremos el modelo de árboles de decisión de comparaciones.

1. **Argumento de Información:**
* Dado un arreglo $A$ de $n$ elementos, el problema de búsqueda tiene $n + 1$ resultados o salidas posibles: El elemento $x$ se encuentra en $[0,n-1]$ ($n$ salidas posibles) y de lo contrario, no se encuentra en $[0,n-1]$ (una salida posible).
* Todo algoritmo basado en comparaciones para este problema puede representarse como un árbol de decisión. Al buscar un valor $x$ en un arreglo ordenado, las comparaciones con los elementos producen tres respuestas posibles ($<, >, =$). Esto implicaría un árbol con tres ramas por nodo, lo que adaptado al lema 1 daría una cota de $\log_3(n+1)$. Para superar esto, el análisis se restringe a los casos en los que el elemento no está en el arreglo.
* Si el elemento no se encuentra, este cae exactamente en uno de los $n+1$ huecos existentes (antes del primer elemento, entre los elementos, o despues del ultimo elemento). En tales casos, el algoritmo jamás recibe la respuesta de igualdad ($=$), por lo que se emplean solo las dos ramas $<$ y $>$, lo que convierte esa parte en un árbol binario.
* **Lema 4:** Si dos valores caen en huecos distintos, un algoritmo correcto los lleva obligatoriamente a hojas distintas. Si terminaran en la misma hoja , el algoritmo no habría comparado con al menos un elemento intermedio, por tanto, un elemento igual a ese valor intermedio recibiría las mismas respuestas, seguiría el mismo camino y el algoritmo cometería el error de decir que 'no está' cuando en realidad si está.
* Dado que los $n+1$ huecos necesitan $n+1$ hojas distintas en la sección del árbol que utiliza solo las ramas $<$ y $>$, por el Lema 1 se concluye que hacen falta al menos $\lceil \log(n+1) \rceil$ comparaciones en el peor caso.
* **Optimalidad de la búsqueda binaria:** La búsqueda binaria alcanza esta cota de manera exacta. Cada comparación reduce el rango a la mitad, de modo que tras $\lceil \log(n+1) \rceil$ comparaciones que permiten aislar un único hueco, demostrando así que es óptima.