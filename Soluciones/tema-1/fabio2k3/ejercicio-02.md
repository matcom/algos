# Solución ejercicio 2:

Tenemos el problema de búsqueda binaria que es: Dado un arreglo Q con sus elementos ordenados y un valor x, devolvemos el índice donde se encuentra x en Q o devolvemos -1 en caso de que x no se encuentre en Q

Código de Nuestro Algoritmo:
----------------------------

def busqueda_binaria(Q, x):
    l = 0
    r = len(Q) - 1

    while l <= r:
        m = (l + r) // 2

        if Q[m] == x:
            return m

        elif Q[m] < x:
            l = m + 1

        else:
            r = m - 1

    return -1


Analicemos ahora su invariante:
--------------------------------

Antes de cada vuelta de nuestro ciclo se que cumple que: todo i < l cumple que Q[i] < x, y todo i > r cumple que Q[i] > x. Esto quiere decir en pocas palabras que todo lo que esté fuera de nuestro rango [l,r] no puede contener al valor que estamos buscando, es decir, x.

Al iniciar el algoritmo tenemos que l = 0 y que r = n - 1 (donde n es el tamaño de nuestro arreglo Q), así que nuestra condición que vimos anteriormente se cumple.

Luego al iniciar el ciclo vamos a suponer que nuestra condición se cumple, pero en este caso Q[m] != x (l <= r), pueden ocurrir dos situaciones distintas:

1- Q[m] < x => como el arreglo está ordenado entonces podemos afirmar que: todo i <= m cumple que Q[i] <= Q[m] < x, luego con el  nuevo l = m + 1, todo i < l cumple que Q[i] < x. La parte derecha no cambia.

2- Caso opuesto Q[m] > x => es exactamente lo mismo pero en otro sentido i >= m cumple que Q[i] >= Q[m] > x, entonces con el nuevo r = m - 1, todo i> m cumple Q[i] > x, por lo tanto se sigue cumple la condición que planteamos al inicio.

Por lo tanto podemos decir que el ciclo termina de dos formas: la primera es con Q[m] = x, donde devuelve el índice m, y la segunda es con l > r donde todo índice i cumple que i > m o i < l, así que ningún valor del arreglo vale x por ende nuestro algoritmo devuelve -1


Analicemos Potencial:
----------------------

Sea p = r - l + 1, tamaño del intervalo de los candidatos, p es entero y mayor o igual a 1 mientras el ciclo corre.

Ahora sea s = p al inicio de cada vuelta de nuestro ciclo, por ende m = l + (s - 1) / 2
                        ------------  => parte entera por debajo

Si no encontramos a x, el nuevo tamaño es:

- Rama Izquierda r = m - 1: m - l = (s - 1) / 2
- Rama Derecha (l = m + 1): r - m = (s - 1) - (s - 1) / 2 

Nota: las dos divisiones anteriores son parte entera por debajo.

En ambos casos el nuevo tamaño es 0 <= s/2 < s. El peor caso es la rama derecha , que esta descarta menos elementos. Como p es entero, este baja estrictamente y se mantiene mayor o igual a 0, el ciclo termina

Costo:
------

Después de k vueltas sin encontrar a x, p <= n/(2^k). La vuelta k + 1 solo se realiza si p >= 1, es decir 2^k <= n, que es lo mismo que decir k <= log2(n) parte entera baja. Por lo tanto el número de vueltas es como máximo: parte entera baja de log2(n) + 1 = parte entera baja de log2(n + 1)

Cada vuelta hace una comparación de tres resultados (Q[m] con respecto a x). El costo es o(log n) y el costo en memoria es de O(1).


Cota de información:
----------------------

Todo algoritmo de búsqueda en un arreglo que esté ordenado que contenga n elementos distintos usando búsqueda binaria necesitará al menos log2(n+1) comparaciones, esto en el peor de los casos.

Analicemos ahora distintas versiones.

1- COn comparaciones de dos resultados: tenemos n + 1 respuestas posibles , los n índices y la opción de NO está. Un árbol de decisión binaria tiene altura h, por ende a lo sumo tiene 2^h hojas entonces:

2^h >= n + 1  ==>>  h >= log2(n+1)

2- Con tres resultados: la rama = es la que termina el cálculo, así que no multiplica hojas. El argumento es el siguiente:

Para responder "x está en i?" nuestro algoritmo tiene que haber comparado x con Q[i] en ese momento. Si no, existe otra entrada Q' que difiere de Q solo en la posición i, en la que la respuesta correcta es distinta, pero el algoritmo no distingue Q de Q'.

Por lo tanto, cada uno de los n índices aparece como nodo de comparación en el árbol. Si descartamos las ramas =, queda un árbol binario ( > y <) de altura menor o igual que h, que tiene a lo sumo n < 2^h - 1, entonces h >= log2(n +1).

Por ende el costo de la búsqueda binaria es, log2(n+1), que coincide exactamente con la cota que hallamos, por esto es óptima en el modelo de comparaciones.

