# Ejercicio 2

## Enunciado
 Da el invariante y el potencial de la búsqueda binaria, y la cota de información que la hace óptima.
(C3, C5)
## Código
```
def binarySearch(arr, x):
    low = 0
    high = len(arr) - 1
    while low <= high:

        mid = low + (high - low) // 2

        # Check if x is present at mid
        if arr[mid] == x:
            return mid

        # If x is greater, ignore left half
        elif arr[mid] < x:
            low = mid + 1

        # If x is smaller, ignore right half
        else:
            high = mid - 1

    # If we reach here, then the element
    # was not present
    return -1
```

## 1. Invariante (Correctitud Parcial)

El invariante que garantiza la correctitud de la búsqueda binaria en cada iteración es:

> **"Si el elemento** $x$ **está en el arreglo, entonces se encuentra obligatoriamente dentro del rango de índices** $[lo, hi]$**."**

* **Inicialización:** Al inicio, $lo = 0$ y $hi = n - 1$. Todo el arreglo está contenido en este intervalo, por lo que el invariante se cumple.

* **Mantenimiento:** Al calcular el punto medio $mid$ y comparar, si descartamos una mitad del arreglo, ajustamos $lo$ o $hi$ de manera que el elemento buscado (si existe) jamás quede excluido del nuevo intervalo $[lo, hi]$.

* **Conclusión:** Cuando el ciclo termina porque $lo > hi$ sin haber hallado el elemento, el invariante garantiza que $x$ no estaba en ninguna parte del arreglo.

---

## 2. Potencial (Terminación)

El potencial que garantiza que el ciclo siempre termina es el tamaño del intervalo de búsqueda:

$$
m = hi - lo
$$

* **Por qué funciona:** Es una cantidad entera no negativa(precondición de que el arreglo esté ordenado) que **decrece estrictamente** en cada iteración gracias a la actualización correcta de los límites (como $lo = mid + 1$ o $hi = mid - 1$). Como un número entero no puede disminuir infinitamente, la reducción constante del intervalo asegura que el algoritmo terminará. Si se cometiera el error de actualizar sin desplazar el límite , el potencial dejaría de bajar y se produciría un bucle infinito.

---

## 3. Cota de Información

Demostramos la cota mínima en el **modelo de comparaciones** mediante un **árbol de decisión** siguiendo el argumento formal del *Sección 3 de la Conferencia 5*.

### Trampa de las 3 respuestas
En cada paso, al comparar $x$ con $A[m]$, un algoritmo de búsqueda binaria puede obtener 3 respuestas posibles ($<$, $=$ o $>$), lo que generaría un árbol ternario. Para acotar el peor caso, consideramos **únicamente los casos en los que $x$ no está en el arreglo**. 
En esos casos, ninguna comparación responde "$=$", por lo que el árbol se reduce a un **árbol binario** (solo 2 ramas por nodo: $<$ y $>$).

### Los 3 Pasos de la Demostración

1. **Los Huecos (Lema 4):** Un arreglo ordenado de $n$ elementos define exactamente $n + 1$ **huecos** o intervalos donde $x$ puede caer sin pertenecer al arreglo ($h_0$ antes de $A[0]$, $h_1$ entre $A[0]$ y $A[1]$, ..., $h_n$ después de $A[n-1]$). 
   Si $x_1$ y $x_2$ caen en huecos distintos, un algoritmo correcto **debe llevarlos a hojas distintas** del árbol de decisión. De no ser así, existiría un elemento del arreglo con el que no se comparó y el algoritmo fallaría en dar una respuesta correcta.

2. **Lema 1 (Árbol binario de decisión):** Un árbol binario de altura $h$ (el número de comparaciones en el peor caso) tiene a lo sumo $2^h$ hojas. Como necesitamos distinguir entre al menos $n + 1$ huecos (hojas distintas):

$$
2^h \ge n + 1
$$

3. **Conclusión y Optimalidad:** Aplicando logaritmo en base 2 y sabiendo que la altura $h$ es un número entero:

$$
h \ge \lceil \log_2(n + 1) \rceil
$$

Cualquier algoritmo basado en comparaciones requiere al menos $\lceil \log_2(n + 1) \rceil$ comparaciones en el peor caso para buscar un elemento. Dado que la búsqueda binaria alcanza exactamente esta altura en su árbol de decisión (separando los $n+1$ huecos en $\lceil \log_2(n+1) \rceil$ pasos), **la búsqueda binaria es óptima** en este modelo.