# Problema 10 ★★

**Enunciado.** Par más cercano en una dimensión. Demuestra $\Omega(n \log n)$ en árboles de decisión algebraicos por reducción desde distinción de elementos. Después di qué algoritmo de la conferencia 2 rompe la cota, en qué modelo, y adáptalo a una dimensión.

## Solución formal

**Cota mínima: $\Omega(n \log n)$ en árboles de decisión algebraicos.**

Recordemos el teorema de Ben-Or (1983): el problema de **distinción de elementos** (DE) requiere $\Omega(n \log n)$ en árboles de decisión algebraicos. DE recibe $n$ números reales $x_1, \ldots, x_n$ y decide si hay dos iguales.

Construimos una reducción de DE a par más cercano en 1D. Dada una instancia de DE con valores $x_1, \ldots, x_n$, construimos $n$ puntos sobre la recta:
$$
P = \{(x_1, 0), (x_2, 0), \ldots, (x_n, 0)\}.
$$
La distancia entre dos puntos es $|x_i - x_j|$. Entonces la distancia del par más cercano de $P$ es $0$ **si y solo si** dos de los $x_i$ son iguales. Resolver par más cercano en 1D resuelve DE.

Si existiera un algoritmo de par más cercano en 1D con profundidad $T(n) = o(n \log n)$ en árboles de decisión algebraicos, componiéndolo con esta construcción (que cuesta $O(n)$ y no usa pruebas de signo) obtendríamos un algoritmo de DE con profundidad $o(n \log n)$, contradiciendo a Ben-Or. Por tanto, par más cercano en 1D requiere $\Omega(n \log n)$ en ese modelo.

**El algoritmo que rompe la cota.**

El algoritmo incremental aleatorio de la Conferencia 2 (Rabin 1976; Kleinberg-Tardos §13.7) resuelve par más cercano en el plano en tiempo esperado $O(n)$. Rompe la cota porque usa dos cosas que el modelo de árboles de decisión algebraicos no tiene:

1. **La parte entera** $\lfloor q/(\delta/2) \rfloor$, que no es un polinomio ni continua. Un árbol de decisión algebraico solo puede evaluar el signo de polinomios de la entrada.
2. **Direccionamiento indirecto** (tabla hash): el resultado de la parte entera se usa como dirección para acceder a una celda. Un árbol de decisión solo ramifica según signos de polinomios, no accede a memoria por índice.

El azar **no** es lo que rompe la cota. Grigoriev, Karpinski, Meyer auf der Heide y Smolensky (1996) demostraron que DE sigue requiriendo $\Omega(n \log n)$ incluso en árboles de decisión algebraicos aleatorizados. El azar sirve para que el número esperado de reconstrucciones sea pequeño.

**Adaptación a una dimensión.**

En 1D, la rejilla se convierte en un conjunto de intervalos de longitud $\delta/2$. La celda de un punto $x$ es $\lfloor x/(\delta/2) \rfloor$. El algoritmo queda así:

1. Permutar los puntos $p_1, \ldots, p_n$ al azar.
2. Insertar $p_1, p_2$ y definir $\delta = |p_1 - p_2|$.
3. Para $i = 3, \ldots, n$:
   - Calcular la celda de $p_i$: $c = \lfloor p_i/(\delta/2) \rfloor$.
   - Mirar las celdas $c-1, c, c+1$ (a lo sumo 3 accesos). Como cada celda tiene a lo sumo un punto, esto es $O(1)$.
   - Si se encuentra un punto $q$ con $|p_i - q| < \delta$, actualizar $\delta = |p_i - q|$ y reconstruir la rejilla completa con el nuevo $\delta/2$. Costo $O(i)$.
   - Si no, insertar $p_i$ en su celda. Costo $O(1)$.

*Invariante.* Cada celda contiene a lo sumo un punto. Si dos puntos estuvieran en la misma celda, su distancia sería menor que $\delta/2 \cdot 2 = \delta$, contradiciendo la definición de $\delta$ como la distancia mínima entre los puntos insertados.

**Análisis hacia atrás.**

Fijemos el conjunto $S = \{p_1, \ldots, p_{i+1}\}$ y olvidemos el orden en que llegaron. El par más cercano de $S$ está determinado por $S$ (a lo sumo dos puntos, suponiendo que no hay empates). El paso $i+1$ reconstruye **si y solo si** $p_{i+1}$ es uno de los dos puntos de ese par. Como el orden de inserción es una permutación uniforme, condicionado a cuál es $S$, el elemento $p_{i+1}$ es uniforme entre los $i+1$ de $S$. Por tanto:
$$
\Pr[\text{reconstruir en el paso } i+1] \le \frac{2}{i+1}.
$$

*Costo esperado.* Por linealidad de la esperanza:
$$
E[\text{costo}] = O(n) + \sum_{i=2}^{n-1} \frac{2}{i+1} \cdot O(i) = O(n) + \sum_i O(1) = O(n).
$$
El número esperado de reconstrucciones es $\sum_{i=2}^{n-1} \frac{2}{i+1} \approx 2 \ln n$.

**Conclusión.** Par más cercano en 1D se resuelve en $O(n)$ esperado con el algoritmo aleatorio, rompiendo la cota $\Omega(n \log n)$ de los árboles de decisión algebraicos. La contradicción se resuelve porque el algoritmo usa la parte entera y el direccionamiento indirecto, que ese modelo no tiene. Toda cota mínima es relativa a un modelo.
