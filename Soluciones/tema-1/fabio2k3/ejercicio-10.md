# Solución Ejercicio 10

Tenemos que demostrar que: El par más cercano en una dimensión requiere Ω(nlogn) en árboles de decisión algebraicos.

Lo haremos por reducción desde distinción de elementos, dados n reales decidir si hay dos iguales, que por el teorema de Ben-Or requiere Ω(nlogn) en este modelo

=> Sea un árbol A que resuelve el par más cercano con profundidad T(n). Una entrada de distinción de elementos x1, x2, ..., xn ya es una entrada válida de par más cercano en la recta, así que la ejecutamos directamente en A.
Cada Hoja de A devuelve un par (i,j) y a le añadimos un nodo que pruebe el signo de xi - xj, si es 0, hay repetidos y si no, todos son distintos

Si hay valores iguales, la distancia mínima es 0, por lo que el par devuelto cumple xi = xj. Si todos son disitntos, todo par tiene una distancia positiva, incluido el devuelto, por ende es Correcto.

El árbol resultante resuelve distinción de elementos con profundidad T(n) + 1, que por teorema visto anteriormente esta profundidad es Ω(nlogn).

Por lo tanto T(n) = Ω(nlogn)

Ahora veamos que algoritmo rompe la cota y en qué modelo
----------------------------------------------------------

El algoritmo incremental aleatorio de la sección 9, rejilla en tabla hash, con costo esperado O(n)

Modelo => Word RAM aleatorizado con tabla hash, usa dos operaciones que un árbol de decisión algebraico no tiene:

. parte entera ⌊q / k⌋ que no es un polinomio ni es continua.

. Direccionamiento indirecto, usa el resultado como índice para buscar en la tabla.

No hay contradicción con Ben-Or, la cota vale para otro modelo, más débil. Una cota mínima va siempre unida a su modelo.


Hagamos la adaptación a uno dimensión:
--------------------------------------

Algoritmo => permutar los puntos al azar p1, p2, ..., pn e insertamos uno por uno, manteniendo k, la distancia mínima entre los ya insertados.
Empezamos con k = |p1 - p2|, y si k = 0 se para

Los puntos se guardan en una tabla hash indexada por la celda ⌊q / k⌋, es decir celdas de longitud k

Para insertar p con c = ⌊p/k⌋:
1- Consultamos las celdas c-1, c y c+1 , y actualizar k si algún punto está a distancia menor que k.

2- Si k bajó, reconstruir la rejilla con el nuevo k insertando todos los puntos hasta p inclusive, y si k = 0, para.

3- Si no bajó, guardamos p en su celda.

Invariante => cada celda tiene a lo sumo un punto. Dos puntos de la misma celda están a distancia menor que k, pero k es la mínima distancia entre los puntos insertados.

Correctitud: si q ya insertado cumple |p-q| < k, entonces |⌊p/k⌋ - ⌊q/k⌋| <= 1, así que q está en una de las 3 celdas consultadas, y cada una tiene a lo sumo un punto.

por lo tanto el nuevo k es min(k, min_q |p-q|), y por inducción sobre i, tras insertar pi el valor k es la distancia mínima entre p1, p2, ..., pi. Si la celda de p estaba ocupada por algún q, entonces |p-q| < k y k baja. Luego en el paso 3 la celda está libre, y la invariante se conserva.

Costo esperado: sin reconstrucciones, cada inserción hace 3 consultas , O(1). El paso i+1, reconstruye solo si p_[i+1] hizo bajar k estrictamente, es decir, si pertenece a todos los pares más cercanos de S = {p1, ..., p_[i+1]} y a lo sumo 2 puntos de S cumplen eso.
Como el orden es una permutación uniforme, p_[i+1] es uniforme dentro de S, así que: Pr[reconstruir] <= 2/(i+1).

Por linealidad de la esperanza => E[costo] <= O(n) + Σ (2/(i+1)) * O(i) = O(n).