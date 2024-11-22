# Greedy

## Videojuego

Estás creando un nivel para un videojuego. El nivel consiste en $n$ habitaciones dispuestas en un círculo. Las habitaciones están numeradas del $1$ al $n$. Cada habitación contiene exactamente una salida: completar la $j$-ésima habitación te permite pasar a la $(j+1)$-ésima habitación (y completar la $n$-ésima habitación te permite pasar a la $1$-era habitación).

Se te da la descripción del multiconjunto de $n$ cofres: el $i$-ésimo cofre tiene un valor de tesoro $c_i$.

Cada cofre puede ser de uno de dos tipos:

- cofre normal — cuando un jugador entra en una habitación con este cofre, recoge el tesoro y procede a la siguiente habitación;
- cofre trampa — cuando un jugador entra en una habitación con este cofre, el cofre se lo come vivo, y él pierde.

El jugador comienza en una habitación aleatoria, con cada habitación teniendo la misma probabilidad de ser elegida. Las ganancias del jugador son iguales al valor total de los tesoros que haya recogido antes de perder.

Se te permite elegir el orden en que los cofres se colocan en las habitaciones. Para cada $k$ de $1$ a $n$, coloca los cofres en las habitaciones de tal manera que:

- cada habitación contenga exactamente un cofre;
- exactamente $k$ cofres sean trampas;
- el valor esperado de las ganancias del jugador sea el mínimo posible.

Ten en cuenta que para cada $k$ la colocación se elige de manera independiente.

Se puede ver que está en la forma de $\frac{P}{Q}$ donde $P$ y $Q$ son enteros no negativos y $Q≠0$.

### Solution

Al principio, digamos que el valor esperado es igual al promedio de las ganancias totales en todas las posiciones y es igual a la suma de las ganancias en todas las posiciones dividida por $n$. Entonces podemos pasar a minimizar la suma.

Aprendamos cómo resolver la tarea para un $k$ fijo. Fijemos algún arreglo y rotamos las habitaciones de manera que la última habitación contenga un cofre trampa. Así que ahora tienes $cnt_1$ cofres normales, luego un único cofre trampa, $cnt_2$ cofres normales, un único cofre trampa, ..., $cnt_k$ cofres normales, un único cofre trampa. Todos los $cnt_i \geq 0$ y $\sum_{i=1}^{k} cnt_i = n - k$.

Observa algunos de estos intervalos de longitud $cnt_i$. El último cofre en el intervalo se toma de $cnt_i$ posiciones iniciales, el penúltimo se toma $cnt_i - 1$ veces, y así sucesivamente.

Ahora vamos a encontrar la mejor forma de elegir los $cnt_i$. Fija algunos valores de $cnt_i$. Observa el más pequeño de estos valores y el más grande de ellos. Sean los valores $x$ y $y$. Si difieren en al menos 2 ($x \leq y - 2$), entonces el resultado más pequeño siempre se puede lograr moviendo un cofre normal del más grande al más pequeño. (esto lleva demostración).

Ahora ya tenemos todos los $cnt_i$ establecidos. Lo único que queda es asignar los cofres de manera óptima. Escribe la unión de todas las secuencias de coeficientes de todos los intervalos $\bigcup_{i=1}^{n-k} [1,\dots,cnt_i - 1, cnt_i]$ y ordénalas en orden no decreciente. Es fácil demostrar que los cofres deben ordenarse en orden no creciente (es algo bastante clásico, puedes intentar demostrarlo mostrando que cualquier otro arreglo puede mejorarse fácilmente una vez más).

Eso nos permite escribir una solución en $O(n^2)$. Ordena todos los cofres al principio, luego para algún $k$, multiplica el valor del $i$-ésimo cofre por $\left\lfloor \frac{i}{k} \right\rfloor$ y suma los resultados.

Finalmente, aceleremos esto con sumas prefixadas. Observa que los primeros $k$ valores se multiplican por $0$, los segundos $k$ valores por $1$ y así sucesivamente. Si $n$ no es divisible por $k$, entonces el último bloque simplemente tiene una longitud menor que $k$. Por lo tanto, podemos calcular la respuesta para algún $k$ en $O(nk)$. Y eso es igual a $O\left(\sum_{k=1}^{n} nk\right) = O(n \log n)$.

COMPLEJIDAD TEMPORAL:
$O(n \log n)$.
