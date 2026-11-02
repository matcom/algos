**Problema:** Par más cercano en una dimensión. Demuestra $\Omega(n \log n)$ en árboles de decisión algebraicos por reducción desde distinción de elementos. Después di qué algoritmo de la conferencia 2 rompe la cota,en qué modelo, y adáptalo a una dimensión.

Para demostrar que el problema del par más cercano en una dimensión requiere $\Omega(n \log n)$ operaciones en el modelo de árboles de decisión algebraicos, vamos a hacer una reducción desde el problema de distinción de elementos.

## Distinción de elementos:
Dado un conjunto de $n$ números reales $X = {x_1, x_2, ..., x_n}$, decidir si todos los elementos son mutuamente distintos. Por el Teorema de Ben-Or aplicable a los árboles de decisión algebraicos, el problema de la distinción de elementos requiere en el peor de los casos un número de operaciones acotado por $\Omega(n \log n)$.

Supongamos por reducción a lo absurdo que existiera un algoritmo $A$ capaz de resolver el problema del par más cercano en una dimensión en el modelo de árboles de decisión algebraicos con un tiempo estrictamente menor de $\Omega(n \log n)$.
Entonces podríamos resolver el problema de la distinción de elementos utilizando dicho algoritmo $A$ mediante el siguiente procedimiento:
* Recibimos una instancia de distinción de elementos $X = {x_1, x_2, ..., x_n}$.
* Invocamos el supuesto algoritmo $A$ del par más cercano sobre el conjunto $X$. Esto nos devuelve la distancia mínima entre el par más cercano, que denotaremos como $\delta_{min}$.
* Luego, si $\delta_{min}=0$ , significa que existen al menos dos elementos idénticos en el conjunto $(x_i = x_j)$, por lo que no son distintos. Si $\delta_{min} > 0$, todos los elementos son estrictamente diferentes, por lo que si son distintos.

## Conclusión:
El tiempo total para resolver la distinción de elemento bajo esta reducción sería el tiempo del algoritmo $A$ más una comprobación $O(1)$. Si $A$ resolviera el par más cercano en $o(n log n)$, entonces la distinción de elementos se resolvería también en $o(n log n)$. Sin embargo, esto contradice el resultado matemático de que la distinción de elementos requiere $\Omega(n \log n)$ en árboles de decision algebraicos.
Por tanto, la suposición es falsa, y el problema del par más cercano en una dimensión tiene un límite inferior de $\Omega(n \log n)$ en el modelo de árboles de decisión algebraicos.

## Como se rompe la cota?
La cota inferior de $\Omega(n \log n)$ demostrada anteriormente solo es válida dentro del modelo de árboles de decisión algebraicos (o modelos basados en comparaciones), donde los elementos solo pueden examinarse mediante comparaciones algebraicas de la forma $xi < xj$ o evaluaciones de polinomios. Sin embargo, esta cota se rompe al cambiar de modelo computacional hacia el Modelo RAM.

### El algoritmo que rompe la cota
Utilizando algoritmos de ordenamiento en tiempo lineal basados en la estructura interna de los bits de los datos (como Counting Sort), podemos ordenar los elementos sin realizar compraraciones directas par a par.

Si los datos de entrada son números enteros, podemos resolver el problema del par más cercano en una dimensión en tiempo $O(n)$ mediante los siguientes dos pasos:
1. Aplicamos Counting Sort directamente sobre el arreglo $X$ de tamaño $n$. Esto nos devuelve el arreglo ordenado $x_1 <= x_2 <= ... <= x_n$, en un tiempo de $O(n)$.
2. Sabemos que en una dimensión se cumple que el par  de elementos más cercano siempre debe ser adyacente en el arreglo ordenado. $$\delta_{min} = min(x_i+1,x_i)$$
Por tanto , realizamos un recorrido sobre el arreglo ordenado de tamaño $n$, comparando solo los elementos continuos. Este paso requiere exactamanete $n-1$ comparaciones: $O(n)$.

**Coste total:** O(n)+O(n)= O(n).
Esto rompe formalmente la cota $\Omega(n \log n)$.