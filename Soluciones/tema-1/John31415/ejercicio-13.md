## Problema

Considere un Splay Tree de $n$ nodos inicializado como un camino (lista degenerada) sobre el cual se realiza una secuencia de accesos en orden estrictamente creciente a las claves $1, 2, \dots, n$.

1. **Cota por Lema de Acceso:** Acote el costo total de la secuencia empleando el Lema de Acceso de Sleator y Tarjan y el análisis por función potencial.
2. **Comparación con la Sección 6:** Compare este resultado con las mediciones empíricas y conceptuales presentadas en la Sección 6.
3. **Ajustabilidad:** Determine si la cota obtenida mediante el Lema de Acceso es ajustada para este caso particular.

---

## Solución

### 1. Aplicación del Lema de Acceso

#### Asignación de Pesos y Rangos

Asignamos a cada nodo $v$ un peso constante $w(v) = 1$.

* El tamaño acumulado del subárbol con raíz en $v$ se define como $W(v) = \sum_{u \in \text{subárbol}(v)} w(u)$, lo que satisface $1 \leq W(v) \leq n$.
* El rango de un nodo es $r(v) = \log_2 W(v)$.
* Para la raíz del árbol $t$, $W(t) = n$, por lo que $r(t) = \log_2 n$.
* Para cualquier nodo $x$, $W(x) \geq 1 \implies r(x) \geq 0$.

#### Costo Amortizado de un Splay Individual

Por el Lema de Acceso, el costo amortizado de la operación $\text{splay}(x)$ en un árbol con raíz $t$ está acotado superiormente por:


$$\hat{c}(x) \leq 3(r(t) - r(x)) + 1$$

Dado que $r(t) \leq \log_2 n$ y $r(x) \geq 0$, el costo amortizado de cada acceso individual se acota como:


$$\hat{c}(x) \leq 3 \log_2 n + 1 = \mathcal{O}(\log n)$$

#### Acotación del Costo Total Real de la Secuencia

Sumando el costo amortizado sobre los $n$ accesos consecutivos:


$$\sum_{i=1}^{n} c_i = \sum_{i=1}^{n} \hat{c}_i + \Phi_0 - \Phi_n$$

donde la función potencial global del árbol corresponde a la suma de los rangos:


$$\Phi = \sum_v r(v)$$

1. **Suma de costos amortizados:**

$$\sum_{i=1}^{n} \hat{c}_i \leq \sum_{i=1}^{n} (3 \log_2 n + 1) = 3n \log_2 n + n = \mathcal{O}(n \log n)$$


2. **Diferencia de potencial ($\Phi_0 - \Phi_n$):**
* **Potencial inicial $\Phi_0$:** El árbol comienza como un camino de $n$ nodos. Los tamaños de los subárboles van desde $1$ hasta $n$, por lo que:

$$\Phi_0 = \sum_{k=1}^{n} \log_2 k = \log_2(n!) = \Theta(n \log n)$$


* **Potencial final $\Phi_n$:** Todos los rangos satisfacen $r(v) \geq \log_2(1) = 0$, de donde $\Phi_n \geq 0$.
* **Crédito neto:** Por lo tanto:

$$\Phi_0 - \Phi_n \leq \Phi_0 = \log_2(n!) = \mathcal{O}(n \log n)$$





Combinando la suma amortizada con el balance de potencial inicial, el Lema de Acceso acota el costo real total mediante:


$$\text{Costo Total Real} = \sum_{i=1}^{n} c_i \leq \mathcal{O}(n \log n)$$

---

### 2. Comparación con las Mediciones de la Sección 6

En la Sección 6 se analiza el comportamiento estructural del Splay Tree frente a heurísticas de autoorganización más simples, como *move-to-root*, que no emplean rotaciones dobles *zig-zig*.

* **Move-to-root:** Puede degradarse a un costo de $\Theta(n)$ por acceso sobre un camino degenerado, acumulando un costo cuadrático total de $\Theta(n^2)$ cuando la orientación inicial del camino es desfavorable para la secuencia de accesos. Sin embargo, este comportamiento depende de la orientación inicial: si el camino está formado por hijos derechos con claves crecientes desde la raíz, los accesos en orden creciente pueden realizarse con un costo total de $\mathcal{O}(n)$.
* **Splay Tree:** La operación *splay* de Tarjan y Sleator ejecuta una reestructuración del camino de acceso mediante rotaciones simples y dobles (*zig*, *zig-zig* y *zig-zag*). Estas rotaciones modifican progresivamente la estructura del árbol y permiten aprovechar los patrones de acceso.
* **Comportamiento secuencial:** A medida que se accede secuencialmente a los elementos, las reestructuraciones realizadas permiten reducir el costo acumulado de los accesos. El Teorema de Acceso Secuencial establece que recorrer todas las claves en orden creciente tiene un costo total de $\mathcal{O}(n)$, independientemente de la forma inicial del árbol.

Por tanto, las mediciones empíricas de la Sección 6 deben interpretarse teniendo en cuenta tanto la configuración inicial de las estructuras como el patrón de acceso. El Splay Tree puede obtener un rendimiento lineal en esta secuencia incluso cuando parte de un árbol completamente degenerado.

---

### 3. ¿Es ajustada la cota $\mathcal{O}(n \log n)$?

No, la cota $\mathcal{O}(n \log n)$ derivada de la aplicación directa del Lema de Acceso no es ajustada para esta secuencia específica; constituye una sobreestimación.

#### Justificación Teórica

* **Costo Real $\mathcal{O}(n)$:** Sleator y Tarjan demostraron formalmente en su Teorema del Acceso Secuencial (*Sequential Access Theorem*) que acceder a todas las claves en orden $1, 2, \dots, n$ sobre un Splay Tree de $n$ nodos, independientemente de su forma o topología inicial, toma un tiempo total de $\mathcal{O}(n)$, equivalente a $\mathcal{O}(1)$ pasos en promedio por acceso.
* **Causa de la Holgura del Lema:** El Lema de Acceso evalúa cada operación mediante una cota genérica de $\mathcal{O}(\log n)$ por paso. No captura suficientemente el efecto acumulativo de las rotaciones coordinadas durante una secuencia de accesos ordenados. El Teorema de Acceso Secuencial aprovecha precisamente las propiedades globales de esta secuencia para establecer una cota lineal, sin que ello implique que cada rotación *zig-zig* reduzca a la mitad la profundidad de todos los nodos ni que el árbol resultante tenga necesariamente una estructura perfectamente balanceada.

Por consiguiente, la cota ajustada para el costo total de la secuencia es:


$$\boxed{\Theta(n)}$$