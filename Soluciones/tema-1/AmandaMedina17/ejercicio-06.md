**Problema:** Una matriz $n x n$ tiene filas y columnas ordenadas de forma creciente. Diseña un algoritmo que decida si contiene un valor $x$ en $O(n)$ comparaciones, demuestra su correctitud con un invariante, ydemuestra con un adversario que no se puede en $o(n)$.

Si intentamos buscar un elemento en la matriz comenzando desde la posicion $(0,0)$ no sabremos hacia donde avanzar, pues hacia la derecha y hacia abajo los números crecen. Análogamente pasa si comenzamos por el centro de la matriz, nos encontraremos en un callejón sin salida. 

La estrategia consiste en comenzar en la esquina superior derecha (fila 0, columna n-1). Si nos movemos hacia la izquierda, los valores de la fila disminuyen, y si nos movemos hacia abajo, los valores de la columna aumentan. Entonces, comparando el valor actual $M[i][j]$ con el valor buscado tendríamos:
* Si $M[i][j] == x$: Retorna verdadero, se encontró el valor.
* Si $M[i][j] > x$: Los elementos de la izquierda son más pequeños y todos los elementos que están abajo son más grandes, por tanto, sabemos con seguridad que $x$ no puede estar en esa columna. Descartamos la columna moviéndonos una posición a la izquierda $(j=j-1)$.
* Si $M[i][j] < x$: Los elementos de abajo son mayores que $x$ y los elementos de la izquierda son todos menores que $x$, por lo que $x$ no puede estar en esa fila. Descartamos toda la fila moviéndonos un paso hacia abajo $(i=i+1)$

**Análisis de la complejidad**
En cada iteración del ciclo solo podemos o incrementar $i$ o disminuir $j$. Dado que el índice $i$ solo puede incrementar $n$ veces y el índice $j$ solo puede disminuir $n$ veces, el ciclo realiza a lo sumo $2*n$ pasos. Es como dibujando una escalera. Por tanto, la complejidad temporal en el peor caso es $O(n)$ comparaciones.

**Demostración de correctitud con un invariante:**
Si el valor $x$ se encuentra dentro de la matriz $M$, entonces obligatoriamente tiene que estar en la submatriz resultante de eliminar en pasos anteriores las filas y columnas. Es decir, la submatriz que abarca las columnas desde $0$ hasta $j$ y las filas desde $i$ hasta $n-i$, siendo $i$ y $j$ en donde estamos parados en cada iteración. Las columnas eliminadas $(j+1...n+1)$  y las filas eliminadas $(0...i-1)$ se garantiza que no contienen a $x$.

**Demostración:**
1. Caso Base: Al iniciar el algoritmo, $i=0$ y $j =n-1$. La submatriz activa abarca toda la matriz. Ningún elemento ha sido descartado todavía por lo que cumple el invariante.

2. Paso inductivo: Suponiendo que el invariante es verdadero, al inicio de cada iteración:
* Si $M[i][j] == x$, se retorna $True$ de manera correcta.
* Si $M[i][j] > x$, sabemos por la ordenación de la matriz que todos los elementos ubicados por debajo de $(i,j)$ en la columna $j$ son mayores que $M[i][j]$ y por tanto mayores que $x$. Descartar la columna restándole $1$ a $j$ preservará el invariante.
* Si $M[i][j] < x$, todos los elementos situados a la izquierda de $(i,j)$ en la fila $i$ son menores que $M[i][j]$ y por tanto menores que $x$. Descartar la fila sumándole $1$ a $i$ preservará el invariante.

3. El ciclo termina cuando $i=n$ o $j=-1$, lo que indica que la submatriz de búsqueda se redujo a la matriz vacía sin haber encontrado a $x$. Por el invariante, si $x$ estuviera en la matriz debería encontrarse en esa matriz vacía, lo q es una contradicción, entonces se puede concluir que $x$ no está en la matriz.

**Demostración de la cota inferior por adversario**
Para demostrar que ningún algoritmo puede resolver este problema en un tiempo menor al lineal $(o(n))$, utilizamos la técnica del adversario.
* Supongamos que tenemos un algoritmo que va a encontrar a $x$ en la matriz haciendo menos de $n$ consultas a la matriz.
* Tendremos un adversario que rellena la matriz a medida que el algoritmo va consultando celdas. Su objetivo es contestar de forma que el algoritmo sepa la menor cantidad de información posible en cada paso, obligándolo a trabajar más.
* Como el algoritmo realiza k < n operaciones totales, por el Principio del Palomar va a quedar al menos una una fila y una columna completa que el algoritmo no va a mirar nunca.
* El adversario construye los valores de la matriz a lo largo de la diagonal principal o secundaria de modo que todas las celdas que el algoritmo si preguntó queden ordenadas. Sin embargo, el adversario deja libre y sin revisar la intersección de esa fila y columna que el algoritmo nunca consultó. Si el algoritmo se rinde y devuelve $False$, el adversario revela que justo en la celda que no miro estaba el valor $x$ (el algoritmo falla). Si el algoritmo devuelve $True$, el adversario revela que esa celda tenía un valor distinto de $x$ y que $x$ jamás estuvo en M (el algoritmo falla).
* En conclusión, el argumento del adversario demuestra que las restricciones de la matriz definen un camino crítico de tamaño $n$ (como la diagonal de la matriz). Si un algoritmo no revisa al menos un elemento por cada paso de ese camino entonces el adversario siempre puede construir una entrada válida donde el algoritmo se equivoca. Por tanto, para garantizar que un algoritmo nunca se equivoque, esta obligado a hacer al menos  $\Omega(n)$ comparaciones en el peor caso. Esto prueba formalmente que el algoritmo en $O(n)$ es óptimo y no se puede hacer en $o(n)$. 