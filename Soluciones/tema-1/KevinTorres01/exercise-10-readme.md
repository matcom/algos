# Ejercicio 10 — Par más cercano en una dimensión

**Diseño y Análisis de Algoritmos · Tema 1 · Curso 2026**

> Par más cercano en una dimensión. Demuestra Ω(n log n) en árboles de decisión algebraicos por reducción desde distinción de elementos. Después di qué algoritmo de la conferencia 2 rompe la cota, en qué modelo, y adáptalo a una dimensión. (C2, C5)

---

## 1. Cota mínima (Ω(n log n)) por reducción (C5)

Para demostrar que el problema del par más cercano en una dimensión requiere al menos $\Omega(n \log n)$ comparaciones en el peor caso, utilizamos una **reducción** desde el problema de **distinción de elementos**. 

El problema de distinción de elementos consiste en, dado un arreglo de $n$ números reales, decidir si todos son distintos o si hay al menos un duplicado. El teorema de Ben-Or establece que este problema requiere $\Omega(n \log n)$ en el modelo de árboles de decisión algebraicos.

**La reducción:**
Dado un arreglo de $n$ números reales $x_1, x_2, \ldots, x_n$, construimos un conjunto de $n$ puntos en 1D:
$$
P = \{ (x_1, 0), (x_2, 0), \ldots, (x_n, 0) \}
$$
Esta transformación cuesta $O(n)$ y no realiza ninguna comparación.

La distancia euclidiana entre dos puntos en esta recta es $d((x_i, 0), (x_j, 0)) = |x_i - x_j|$. Por lo tanto, la distancia del par más cercano es **0 si y solo si** hay dos números iguales en el arreglo original.

**El algoritmo compuesto:**
Supongamos que existiera un algoritmo que resuelve el par más cercano en 1D en tiempo $o(n \log n)$. Podríamos construir un algoritmo para distinción de elementos con el siguiente procedimiento:
1. Transformar los $n$ reales en $n$ puntos en el eje $x$ (costo $O(n)$).
2. Ejecutar el algoritmo rápido de par más cercano (costo $o(n \log n)$).
3. Si la distancia mínima resultante es $0$, responder "Hay duplicados". Si es $> 0$, responder "Todos son distintos" (costo $O(1)$).

El costo total de este algoritmo sería $o(n \log n)$. Pero esto contradice el teorema de Ben-Or. Por lo tanto, asumir que existe un algoritmo de par más cercano en $o(n \log n)$ es imposible: el par más cercano en 1D también requiere $\Omega(n \log n)$ en árboles de decisión algebraicos.

## 2. El algoritmo que rompe la cota y su modelo (C2)

A pesar de la cota demostrada, existe un algoritmo **incremental y aleatorio** (Rabin, 1976; Kleinberg y Tardos) que resuelve el problema en **tiempo esperado $O(n)$**. 

Esto no es una contradicción, sino que el algoritmo opera en un **modelo de cómputo** distinto y más poderoso: la **Word RAM**. 

El algoritmo rompe la cota de los árboles de decisión algebraicos porque utiliza dos herramientas que ese modelo prohíbe:
1. **Función parte entera:** Calcula $\lfloor x \rfloor$, una operación discontinua que no es un polinomio (los árboles algebraicos solo pueden evaluar polinomios).
2. **Direccionamiento indirecto:** Utiliza el resultado de la parte entera como índice para acceder a una **tabla hash** (los árboles algebraicos solo pueden ramificar mediante el signo de un polinomio, no acceder a memoria por dirección).

## 3. Adaptación del algoritmo a una dimensión

El algoritmo original esbozado para 2D se simplifica significativamente en 1D (una recta numérica).

**Estructura:**
1. Se barajan los puntos al azar para obtener una secuencia $p_1, p_2, \ldots, p_n$.
2. Se mantiene la distancia mínima actual $\delta$ entre los puntos insertados.
3. Se usa una **tabla hash** para representar "cubetas" de ancho $\delta/2$ en la recta.

**Inserción de un nuevo punto $p$:**
1. Se calcula la cubeta de $p$ usando su parte entera: $b = \lfloor p / (\delta/2) \rfloor$.
2. Se consultan las cubetas adyacentes: $b-1$, $b$ y $b+1$.
3. Si no hay ningún punto en esas cubetas a distancia menor que $\delta$, se inserta $p$ en su cubeta y $\delta$ se mantiene.
4. Si se encuentra un punto más cercano, se actualiza $\delta$ a un nuevo $\delta'$ y **se reconstruye toda la tabla hash** usando el nuevo ancho $\delta'/2$.

**Análisis del costo esperado:**
- Sin contar las reconstrucciones, cada inserción cuesta $O(1)$ (3 accesos a la tabla hash).
- Por el **análisis hacia atrás**, si fijamos el conjunto de $i+1$ puntos insertados, la probabilidad de que el último punto sea uno de los dos que definen el nuevo par más cercano es a lo sumo $2/(i+1)$.
- Sumando sobre todas las inserciones, el costo esperado de las reconstrucciones es $\sum_{i=1}^{n} O(i) \cdot \frac{2}{i+1} = O(n)$.

**Conclusión:**
El algoritmo adaptado a 1D corre en tiempo esperado $O(n)$ y usa $O(n)$ de memoria. Al igual que en 2D, rompe la cota de $\Omega(n \log n)$ porque su funcionamiento depende de la función parte entera y del acceso a memoria por índice, herramientas que no están permitidas en el modelo de árboles de decisión algebraicos.