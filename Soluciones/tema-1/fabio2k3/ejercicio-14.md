# Solución ejercicio 14

Problema:
---------

Un arreglo A de n elementos distintos es una rotación de uno creciente: A = [a_r, ..., a_{n-1}, a_0, ..., a_{r-1}] con a_0 < a_1 < ... < a_{n-1}. Hay que devolver la posición p del mínimo , es decir el lugar donde está a_0

Las posiciones menores que p contienen elementos mayores que todos los de las posiciones >= p, y a partir de p el arreglo es creciente. Es decir si i < p <= j, entonces A[i] > A[j], y si p <= i < j , entonces A[i] < A[j].

¿Cómo podemos resolver este problema? Veamos el algoritmo
----------------------------------------------------------

def minimo_rotado(A):
    l = 0
    h = len(A) - 1

    while l < h:
        mid = (l + h) // 2
        if A[mid] > A[h]:
            l = mid + 1
        else:
            h = mid

    return l

La fuerza bruta (mirar los n elementos del arreglo) cuesta n - 1 comparaciones. La idea es descartar la mitad del intervalo con una sola comparación.


¿Es correcta nuestra solución?
------------------------------

Invariante (I): l <= p <= h, el mínimo está en A[l..h]

Inicialización del algoritmo: l = 0 y h = n - 1: p está en el arreglo.

Dentro del ciclo: con l < h, mid = (l + h) // 2 cumple l <= mid < h.

- Si A[mid] > A[h] no puede ser mid >= p, porque entonces p <= mid < h y por lo que planteamos A[mid] < A[h]. Entonces luego mid < p , así que p pertenece a [mid + 1, h] y (l = mid + 1) conserva la invariante "I".

- Si A[mid] < A[h] (son distintos): no puede ser mid < p, porque entonces mid < p <= h y como vimos anteriormente A[mid] > A[h], luego mid >= p, así que p pertenece [l, mid] y h = mid conserva "I"

Por ende al salir l = h y por "I" ese índice es p.

Terminación: Q = h - l + 1, es un entero mayor o igual que q. Con Q = s >= , la nueva Q es ⌊s/2⌋ que es la rama l = mid + 1, o ⌈s/2⌉ que es la rama h = mid. En ambos casos es <= ⌈s/2⌉ < s, estrictamente y el ciclo termina.

Costo:
------

Cada vuelta hace una comparación. Tras r vueltas Q <= ⌈n / 2^r⌉, que vale 1 cuando 2^r >= n. Por tanto el algoritmo hace a lo sumo ⌈log2 n⌉ comparaciones, con memoria O(1). 

Ahora, se puede mejorar nuestra solución?
-----------------------------------------

Teorema: todo algoritmo de comparaciones que halle el mínimo de un arreglo rotado de elementos distintos hace al menos ⌈log2 n⌉ comparaciones en el peor caso

Demostrémoslo:

Hay n salidas posibles. Las n rotaciones de un mismo arreglo creciente son entradas válidas, y en la rotación r el mínimo está en la posición (n - r) módulo n; son n posiciones distintas, así que hay n  respuestas correctas distintas.

Cada una necesita su hoja, el algoritmo ve respuestas de comparaciones, así que dos entradas que llegan a la misma hoja reciben la misma salida. Si sus respuestas correctas son distintas, se equivoca en una. 

Por lo tanto el árbol de decisión tiene al menos n hojas.

Altura => con elementos distintos cada comparación tiene dos resultados, así que el árbol de decisión es binario. Un árbol binario de altura h tiene a lo sumo 2^h hojas, porque cada nodo tiene a lo sumo dos hijos y entonces cada nivel tiene a lo sumo el doble de nodo que el anterior (el nivel h tiene a lo sumo 2^h). Como el árbol necesita al menos n hojas, 2^h >= n, por lo tanto h >= (log 2 n). la altura es un entero , h >= ⌈log2 n⌉.