## Problema

Dado el problema del Par Más Cercano en una Dimensión (CP1D):

1. Demuestre mediante árboles de decisión algebraicos y una reducción desde el problema de distinción de elementos (*Element Uniqueness*) que la cota inferior es $\Omega(n \log n)$.
2. Identifique qué algoritmo de la literatura rompe dicha cota, especifique el modelo computacional en el que lo logra y adapte dicho algoritmo al caso unidimensional.

---

## Solución

### 1. Demostración de la Cota Inferior ($\Omega(n \log n)$) en Árboles de Decisión Algebraicos

Para demostrar que el problema del Par Más Cercano en 1D requiere $\Omega(n \log n)$ operaciones en el modelo de árboles de decisión algebraicos de grado acotado, empleamos una reducción desde el problema clásico de Distinción de Elementos (*Element Uniqueness*, EU).

#### Definición de los Problemas

* **Distinción de Elementos (EU):** Dados $n$ números reales $x_1, x_2, \dots, x_n$, decidir si existen $i \neq j$ tales que $x_i = x_j$.
* **Par Más Cercano 1D (CP1D):** Dados $n$ números reales $x_1, x_2, \dots, x_n$, encontrar la distancia mínima:

$$\delta = \min_{i \neq j} \vert{}x_i - x_j\vert{}$$



#### Reducción en Tiempo $\mathcal{O}(n)$

1. Dada una instancia de EU con un conjunto $S = \{x_1, x_2, \dots, x_n\}$, esta se suministra directamente como entrada al algoritmo de CP1D.
2. Se obtiene como resultado la distancia mínima $\delta$.
3. Se evalúa la condición de unicidad:
* Si $\delta = 0$: Existen elementos duplicados $\implies$ Los elementos no son todos distintos (se retorna `True`).
* Si $\delta > 0$: No existen duplicados $\implies$ Todos los elementos son estrictamente distintos (se retorna `False`).



Esta reducción requiere únicamente tiempo constante adicional, por lo que su costo total es $\mathcal{O}(n)$, incluyendo la lectura de la entrada y la evaluación del resultado.

#### Cota Inferior

* De acuerdo con el teorema de Ben-Or (1983), el problema de Distinción de Elementos exige $\Omega(n \log n)$ pasos en el peor de los casos dentro del modelo de árboles de decisión algebraicos (analizando el número de componentes conexas del conjunto de soluciones en $\mathbb{R}^n$, cuya cota factorial da una altura mínima de orden $\log_2(n!) = \Omega(n \log n)$).
* Puesto que la reducción desde EU toma tiempo lineal $\mathcal{O}(n)$, cualquier algoritmo para CP1D en dicho modelo algebraico requiere obligatoriamente realizar al menos $\Omega(n \log n)$ operaciones. De lo contrario, se obtendría un algoritmo para EU con complejidad inferior a su cota conocida.

---

### 2. Algoritmo que Rompe la Cota, Modelo y Adaptación a 1D

#### Algoritmo y Modelo Computacional

El algoritmo que permite romper la cota $\Omega(n \log n)$ es el algoritmo aleatorizado de Rabin (1976) para el problema del par más cercano, que utiliza una estructura de rejilla y *hashing*. En su variante incremental, procesa los puntos en orden aleatorio y reconstruye la rejilla cuando disminuye la distancia mínima vigente.

* **Modelo:** El modelo computacional en el que se rompe la cota es una Real RAM de costo unitario, con operaciones aritméticas sobre números reales, función piso, generación de números aleatorios y acceso indirecto mediante una tabla hash cuyas operaciones tienen costo esperado $\mathcal{O}(1)$.
* **Mecanismo:** El algoritmo logra superar la cota de comparación pura mediante el uso de la función de piso entero (cuantización y *hashing* para mapear celdas como $\lfloor q/\delta \rfloor$), una operación aritmética de direccionamiento que no está disponible en los árboles de decisión algebraicos puros.
* **Tiempo logrado:** $\mathcal{O}(n)$ esperado para la variante incremental aleatorizada.

Este resultado no contradice la cota inferior anterior, ya que el modelo Real RAM con función piso y direccionamiento indirecto mediante *hashing* es más potente que el modelo de árboles de decisión algebraicos.

#### Adaptación del Algoritmo a Una Dimensión (1D)

En el plano bidimensional (2D), la rejilla emplea celdas cuadradas y consulta un entorno local de celdas vecinas. En 1D, simplificamos la estructura a una tabla hash de intervalos de longitud $\delta/2$:

1. **Estructura de Datos:** Dividimos la recta real en celdas de tamaño $S = \delta/2$, donde $\delta$ es la distancia mínima entre los puntos procesados. Cada punto $q$ se mapea a un índice de celda mediante la función de cuantización:

$$I(q) = \left\lfloor \frac{q}{S} \right\rfloor$$



Este índice entero se almacena en una tabla hash. La función piso permite trabajar también con coordenadas negativas.
2. **Invariante:** Mientras $\delta > 0$ sea la distancia mínima entre los puntos procesados, cada celda de tamaño $\delta/2$ contiene a lo sumo un punto. De lo contrario, dos puntos de una misma celda estarían separados por una distancia estrictamente menor que $\delta$, contradiciendo su definición.
3. **Orden Aleatorio:** Se aplica una permutación aleatoria uniforme sobre los $n$ puntos: $p_1, p_2, \dots, p_n$.
4. **Inicialización:**
Si $n < 2$, no existe ningún par que pueda evaluarse. En caso contrario, calculamos:

$$\delta = \vert{}p_1 - p_2\vert{}$$



Si $\delta = 0$, encontramos inmediatamente dos puntos coincidentes y retornamos dicha distancia. En caso contrario, construimos una tabla hash con celdas de tamaño $S = \delta/2$ e insertamos los dos primeros puntos.
5. **Inserción Paso a Paso de $p_{i+1}$:**
* Al insertar un nuevo punto $p_{i+1}$, calculamos su celda contenedora:

$$c = \left\lfloor \frac{p_{i+1}}{\delta/2} \right\rfloor$$


* Consultamos únicamente las 5 celdas adyacentes en 1D: la celda $c$ y sus dos vecinas a la izquierda y dos a la derecha:

$$[c - 2, c - 1, c, c + 1, c + 2]$$


* Esta vecindad es suficiente porque cualquier punto situado a una distancia estrictamente menor que $\delta$ del nuevo punto debe pertenecer necesariamente a una de esas cinco celdas.
* Puesto que cada celda alberga como máximo un punto, realizamos a lo sumo $5$ consultas de tiempo esperado $\mathcal{O}(1)$ en la tabla hash.
* Si ningún punto en dichas celdas se encuentra a una distancia menor que $\delta$, insertamos $p_{i+1}$ y el valor de $\delta$ permanece inalterado. Costo esperado: $\mathcal{O}(1)$.
* Si se encuentra un punto a una distancia $\delta' < \delta$, actualizamos $\delta$ al mínimo entre las distancias encontradas y reconstruimos la tabla hash con el nuevo tamaño de celda $\delta'/2$, reinsertando los $i+1$ puntos procesados hasta el momento. Costo esperado de reconstrucción: $\mathcal{O}(i+1)$.
* Si $\delta' = 0$, se ha encontrado un par de puntos coincidentes y el algoritmo termina inmediatamente.



#### Análisis Amortizado Aleatorizado (Costo Esperado)

Por un argumento de análisis retrospectivo, la probabilidad de que el $(i+1)$-ésimo punto insertado reduzca el valor de la distancia mínima vigente $\delta$ es a lo sumo:


$$\Pr[\delta_{i+1} < \delta_i] \leq \frac{2}{i+1}$$


donde $\delta_i$ representa la distancia mínima entre los primeros $i$ puntos procesados.

Para justificar esta cota, consideremos los primeros $i+1$ puntos y fijemos, mediante un criterio determinista de desempate, uno de sus pares más cercanos. Si el último punto insertado no pertenece al par fijado, ambos elementos permanecen entre los primeros $i$ puntos. Por tanto, la distancia mínima anterior no podría ser mayor que la nueva distancia mínima, lo que implica que esta no habría disminuido.

En consecuencia, para que se produzca una reducción de $\delta$, el último punto debe ser uno de los dos extremos del par más cercano fijado. Como el orden de inserción es una permutación aleatoria uniforme, la probabilidad de este suceso es como máximo $\frac{2}{i+1}$.

Calculando el costo esperado por paso:


$$\begin{aligned} \mathbb{E}[\text{Costo paso } i+1] &= \mathcal{O}(1) + \Pr[\delta_{i+1} < \delta_i] \cdot \mathcal{O}(i+1) \\ &= \mathcal{O}(1) + \frac{2}{i+1} \cdot \mathcal{O}(i+1) \\ &= \mathcal{O}(1) \end{aligned}$$

Sumando analíticamente sobre el total de $n$ puntos, por linealidad de la esperanza:


$$\mathbb{E}[T(n)] = \sum_{i=2}^{n-1} \mathcal{O}(1) = \mathcal{O}(n)$$

Por tanto, el tiempo total esperado de ejecución del algoritmo adaptado a 1D es $\mathcal{O}(n)$.