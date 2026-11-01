## Problema

Dado el problema del **Par Más Cercano en una Dimensión (CP1D)**:

1. Demuestre mediante árboles de decisión algebraicos y una reducción desde el problema de distinción de elementos (*Element Uniqueness*) que la cota inferior es $\Omega(n \log n)$.
2. Identifique qué algoritmo de la literatura rompe dicha cota, especifique el modelo computacional en el que lo logra y adapte dicho algoritmo al caso unidimensional.

---

## Solución

### 1. Demostración de la Cota Inferior ($\Omega(n \log n)$) en Árboles de Decisión Algebraicos

Para demostrar que el problema del Par Más Cercano en 1D requiere $\Omega(n \log n)$ operaciones en el modelo de árboles de decisión algebraicos de grado acotado, empleamos una **reducción** desde el problema clásico de Distinción de Elementos (*Element Uniqueness* - EU).

#### Definición de los Problemas

* **Distinción de Elementos (EU):** Dados $n$ números reales $x_1, x_2, \dots, x_n$, decidir si existen $i \neq j$ tales que $x_i = x_j$.
* **Par Más Cercano 1D (CP1D):** Dados $n$ números reales $x_1, x_2, \dots, x_n$, encontrar la distancia mínima $\delta = \min_{i \neq j} \vert{}x_i - x_j\vert{}$.

#### Reducción en Tiempo $\mathcal{O}(n)$

1. Dada una instancia de EU con un conjunto $S = \{x_1, x_2, \dots, x_n\}$, esta se suministra directamente como entrada al algoritmo de CP1D.
2. Se obtiene como resultado la distancia mínima $\delta$.
3. Se evalúa la condición de unicidad:
* **Si $\delta = 0$:** Existen elementos duplicados $\implies$ Los elementos no son todos distintos (se retorna `True`).
* **Si $\delta > 0$:** No existen duplicados $\implies$ Todos los elementos son estrictamente distintos (se retorna `False`).



#### Cota Inferior

* De acuerdo con el teorema de Ben-Or (1983), el problema de Distinción de Elementos exige $\Omega(n \log n)$ pasos en el peor de los casos dentro del modelo de árboles de decisión algebraicos (analizando el número de componentes conexas del conjunto de soluciones en $\mathbb{R}^n$, cuya cota factorial da una altura mínima de $\log_2(n!) = \Omega(n \log n)$).
* Puesto que la reducción desde EU toma un tiempo lineal $\mathcal{O}(n)$, cualquier algoritmo para CP1D en dicho modelo algebraico requiere obligatoriamente realizar al menos $\Omega(n \log n)$ operaciones.

---

### 2. Algoritmo que Rompe la Cota, Modelo y Adaptación a 1D

#### Algoritmo y Modelo Computacional

El algoritmo que permite romper la cota $\Omega(n \log n)$ es el **algoritmo incremental y aleatorizado de Rabin (1976)**.

* **Modelo:** El modelo computacional en el que se rompe la cota es el de **Word RAM de costo unitario con hashing aleatorizado e indexación directa**.
* **Mecanismo:** El algoritmo logra superar la cota de comparación pura mediante el uso de la función de **piso entero** (cuantización/hashing para mapear celdas como $\lfloor q / \delta \rfloor$), una operación aritmética de memoria no disponible en los árboles de decisión algebraicos puros.
* **Tiempo Logrado:** $\mathcal{O}(n)$ en esperanza matemática (tiempo esperado).

#### Adaptación del Algoritmo a Una Dimensión (1D)

En el plano bidimensional (2D), la rejilla emplea celdas cuadradas de lado $\delta/2$ consultando bloques locales de $5 \times 5$ celdas. En 1D, simplificamos la estructura a un arreglo unidimensional o tabla hash de intervalos de longitud $\delta$ (o $\delta/2$):

1. **Estructura de Datos:** Dividimos la recta real en celdas de tamaño $S = \delta/2$. Cada punto $q$ se mapea a un índice de celda mediante la función de cuantización $I(q) = \lfloor q / S \rfloor$, almacenado en una tabla hash.
2. **Invariante:** Cada celda de tamaño $\delta/2$ contiene a lo sumo un punto.
3. **Orden Aleatorio:** Se aplica una permutación aleatoria uniforme sobre los $n$ puntos: $p_1, p_2, \dots, p_n$.
4. **Inserción Paso a Paso de $p_{i+1}$:**
* Al insertar un nuevo punto $p_{i+1}$, calculamos su celda contenedora $c = \lfloor p_{i+1} / (\delta/2) \rfloor$.
* Consultamos únicamente el entorno local de **5 celdas adyacentes** en 1D: la celda $c$ y sus dos vecinas a la izquierda y dos a la derecha ($[c-2, c-1, c, c+1, c+2]$).
* Puesto que cada celda alberga como máximo un punto, realizamos a lo sumo $5$ consultas de tiempo $\mathcal{O}(1)$ en la tabla hash.
* Si ningún punto en dichas celdas se encuentra a una distancia menor que $\delta$, insertamos $p_{i+1}$ y el valor de $\delta$ permanece inalterado. Costo: $\mathcal{O}(1)$.
* Si se halla un punto a una distancia $\delta' < \delta$, actualizamos $\delta = \delta'$, purgamos la tabla hash y reconstruimos la rejilla completa con el nuevo tamaño de celda $\delta'/2$, reinsertando los $i+1$ puntos procesados hasta el momento. Costo de reconstrucción: $\mathcal{O}(i)$.



#### Análisis Amortizado Aleatorizado (Costo Esperado)

Por un argumento de análisis retrospectivo, la probabilidad de que el $(i+1)$-ésimo punto insertado reduzca el valor de la distancia mínima vigente $\delta$ es a lo sumo $\frac{2}{i+1}$ (dado que a lo sumo $2$ puntos de los $i+1$ determinan el par más cercano actual).

Calculando el costo esperado por paso:


$$\mathbb{E}[\text{Costo paso } i+1] = \mathcal{O}(1) + \frac{2}{i+1} \cdot \mathcal{O}(i) = \mathcal{O}(1)$$

Sumando analíticamente sobre el total de $n$ puntos, el tiempo total esperado de ejecución del algoritmo adaptado a 1D es de **$\mathcal{O}(n)$**.