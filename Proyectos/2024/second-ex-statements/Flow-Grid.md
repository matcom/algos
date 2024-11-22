# Grafos

## Grid

Un día iba David por su facultad cuando ve un cuadrado formado por $n \times n$  
cuadraditos de color blanco. A su lado, un mensaje ponía lo siguiente: "Las  
siguientes tuplas de la forma $(x_1, y_1, x_2, y_2)$ son coordenadas para pintar de  
negro algunos rectángulos. (coordenadas de la esquina inferior derecha y superior  
izquierda)" Luego se veían $k$ tuplas de cuatro enteros. Finalmente decía:  
"Luego de tener el cuadrado coloreado de negro en las secciones pertinentes, su  
tarea es invertir el cuadrado a su estado original. En una operación puede seleccionar  
un rectángulo y pintar todas sus casillas de blanco. El costo de pintar  
de blanco un rectángulo de $h \times w$ es el mínimo entre $h$ y $w$. Encuentre el costo  
mínimo para pintar de blanco todo el cuadrado."

En unos 10 minutos David fue capaz de resolver el problema. Desgraciadamente  
esto no es una película y el problema de David no era un problema  
del milenio que lo volviera millonario. Pero, ¿sería usted capaz de resolverlo  
también?

### Statement

Se tiene una cuadrícula cuadrada de tamaño $n \times n$. Algunas celdas están coloreadas de negro, mientras que las demás están coloreadas de blanco. En una operación, puedes seleccionar un rectángulo y colorear todas sus celdas de blanco. El costo para colorear un rectángulo de tamaño $h \times w$ es $min(h, w)$. Debes hacer que todas las celdas sean blancas con el costo total mínimo.

### Solution

Si utilizamos un rectángulo $[x1; x2) \times [y1; y2)$ con $x2 - x1 \leq y2 - y1$, podemos cambiarlo a $[x1; x2) \times [0, n)$ sin cambiar el costo. Además, podemos elegir $w$ rectángulos de ancho 1 en lugar de un rectángulo de ancho $w$, lo que tampoco cambiará el costo.

Por lo tanto, debemos elegir el número mínimo de columnas y filas de manera que todas las celdas negras estén cubiertas por al menos una columna o fila seleccionada. Si construimos un grafo bipartito, donde la parte izquierda representa las columnas y la parte derecha las filas, y hay una arista si la celda en la intersección de una fila y una columna está coloreada de negro, entonces la respuesta es el tamaño mínimo de la cobertura de vértices en este grafo. El tamaño mínimo de la cobertura de vértices es igual al tamaño de un emparejamiento máximo, que se puede encontrar utilizando flujo de red. Solo resta notar que podemos comprimir vértices idénticos, y tendremos $O(m)$ vértices en ambas partes.

COMPLEJIDAD TEMPORAL:
Con el algoritmo de Dinic, la complejidad es $O(m^4)$.
