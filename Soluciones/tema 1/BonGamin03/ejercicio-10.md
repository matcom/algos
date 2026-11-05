# Ejercicio 10 

### El problema

Este problema nos pide abordar el problema del **Par más cercano en 1D**:
> Dados $n$ números reales $x_1, x_2, \dots, x_n \in \mathbb{R}$, encontrar el par de índices distintos $(i, j)$ con $i \neq j$ que minimiza la distancia $|x_i - x_j|$.

---

## Demostración de cota mínima $\Omega(n \log n)$

### Teorema
Cualquier algoritmo que resuelva el problema del par más cercano en $1\text{D}$ requiere $\Omega(n \log n)$ comparaciones/operaciones en el peor caso dentro del **modelo de árboles de decisión algebraicos**.

### Demostración por Reducción (desde Distinción de Elementos)

Siguiendo la teoría de reducciones para cotas mínimas (Conferencia 2, §8 y Conferencia 5, §1):

**Problema de origen (Distinción de Elementos):**
   Dados $n$ reales $y_1, y_2, \dots, y_n \in \mathbb{R}$, decidir si existen $i \neq j$ tales que $y_i = y_j$.
   - **Teorema de Ben-Or (1983):** Distinción de Elementos requiere $\Omega(n \log n)$ decisiones en el peor caso en el modelo de árboles de decisión algebraicos (Conferencia 2, §8).

**La Construcción (Reducción $f$):**
   Dada una instancia $Y = \{y_1, y_2, \dots, y_n\}$ de Distinción de Elementos, construimos directamente la entrada de Par Más Cercano 1D con los mismos elementos:
   $$X = Y = \{x_1, x_2, \dots, x_n\}, \quad \text{donde } x_i = y_i \text{ para todo } i = 1, \dots, n$$
   - La transformación toma costo $O(n)$ (simplemente copiar los elementos o pasarlos por referencia) y **no realiza ninguna prueba de signo de polinomios**.

**Preservación de la respuesta:**
   Sea $\delta^* = \min_{i \neq j} |x_i - x_j|$ la menor distancia encontrada por el problema del par más cercano en 1D sobre el conjunto $X$.
   - Si $\delta^* = 0$, significa que existen $x_i, x_j$ con $i \neq j$ tales que $|x_i - x_j| = 0 \implies x_i = x_j$. Por tanto, existen elementos iguales en $Y$ (respuesta **"SÍ"** para Distinción de Elementos).
   - Si $\delta^* > 0$, significa que para todo $i \neq j$, $|x_i - x_j| > 0 \implies x_i \neq x_j$. Por tanto, todos los elementos de $Y$ son distintos (respuesta **"NO"** para Distinción de Elementos).

**Conclusión de la cota:**
   Si existiera un algoritmo $\mathcal{A}$ capaz de resolver Par Más Cercano 1D en el modelo de árboles de decisión algebraicos con profundidad $o(n \log n)$, podríamos componerlo con nuestra reducción lineal $f$ y hacer una verificación final $h(\delta^*) = (\delta^* == 0)$. Esto nos daría un algoritmo para Distinción de Elementos de profundidad $o(n \log n)$, lo cual contradice directamente el Teorema de Ben-Or.

   Por lo tanto, **Par Más Cercano en 1D requiere $\Omega(n \log n)$ en árboles de decisión algebraicos**. $\blacksquare$

---

## Algoritmo que rompe la cota, su modelo y su adaptación a 1D

### ¿Qué algoritmo de la Conferencia 2 rompe la cota?
El **Algoritmo Incremental Aleatorio** de Rabin (1976) / Kleinberg & Tardos (Conferencia 2, §9). Resuelve el problema en costo esperado **$O(n)$**, rompiendo la cota $\Omega(n \log n)$.

### ¿En qué modelo opera?
Opera en el modelo **Word RAM** (o modelo con direccionamiento indirecto y función piso/parte entera $\lfloor \cdot \rfloor$).

**¿Por qué no contradice la cota mínima?** (Conferencia 2, §10 y Conferencia 5, §9):
Toda cota mínima está supeditada a un modelo restringido. La cota $\Omega(n \log n)$ aplica únicamente al *modelo de árboles de decisión algebraicos*, donde las únicas operaciones permitidas son evaluar el signo de un polinomio. 
El algoritmo incremental aleatorio utiliza operaciones que ese modelo no posee:
1. **Función Parte Entera ($\lfloor \cdot \rfloor$):** Permite discretizar el espacio real (no es continua ni lineal/algebraica acotada).
2. **Direccionamiento Indirecto / Tablas Hash:** Permite consultar una celda en memoria de costo $O(1)$ a partir del índice calculado.

---

### Adaptación del Algoritmo Incremental Aleatorio a 1D

En una dimensión, el espacio se divide en **intervalos de longitud $\delta$** (en lugar de celdas cuadradas de la rejilla 2D).

#### Estructura y Algoritmo:
1. Permutar aleatoriamente la entrada: $x_1, x_2, \dots, x_n$.
2. Inicializar $\delta = |x_1 - x_2|$ como la distancia mínima actual del par $\{x_1, x_2\}$.
3. Construir una rejilla unidimensional (tabla hash) con celdas de tamaño $r = \delta / 2$. Cada celda de índice $k = \lfloor x_i / r \rfloor$ guarda a lo sumo 1 punto.
4. Para cada nuevo punto $x_i$ (desde $i = 3$ hasta $n$):
   - Calcular su celda $k = \lfloor x_i / r \rfloor$.
   - Consultar el bloque adyacente de celdas (en 1D basta mirar las celdas en el rango $[k-2, k+2]$, es decir, 5 celdas en total).
   - **Caso A:** Si no hay ningún punto a distancia $< \delta$, $\delta$ no cambia. Insertamos $x_i$ en su celda $k$ en $O(1)$.
   - **Caso B:** Si se encuentra un punto $x_j$ tal que $|x_i - x_j| < \delta$:
     - Actualizamos $\delta_{nuevo} = |x_i - x_j|$.
     - Reconstruimos la tabla hash desde cero para los primeros $i$ puntos con el nuevo tamaño de celda $r_{nuevo} = \delta_{nuevo} / 2$.

#### Análisis de Costo (Análisis Hacia Atrás):
- **Invariante de la celda:** Dos puntos en la misma celda de tamaño $r = \delta/2$ distan a lo sumo $r < \delta$, lo que contradice la minimalidad de $\delta$. Por tanto, cada celda contiene **a lo sumo 1 punto**.
- **Probabilidad de Reconstrucción:** Al insertar el $i$-ésimo punto $x_i$, el par más cercano entre los primeros $i$ puntos cambia solo si $x_i$ forma parte del nuevo par más cercano. Condicionado al conjunto de los primeros $i$ puntos, la probabilidad de que $x_i$ sea uno de los dos puntos del par más cercano es a lo sumo $\frac{2}{i}$.
- **Costo Esperado Total:**
  $$\mathbb{E}[\text{Costo}] = O(n) + \sum_{i=3}^{n} \frac{2}{i} \cdot O(i) = O(n) + O(1) \sum_{i=3}^{n} 1 = O(n)$$

Demostrando que la adaptación en 1D resuelve el problema en **tiempo esperado $O(n)$ y espacio $O(n)$**.
``