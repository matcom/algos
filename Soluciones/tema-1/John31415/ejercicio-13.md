## Problema

Considere un *Splay Tree* de $n$ nodos inicializado como un camino (lista degenerada) sobre el cual se realiza una secuencia de accesos en orden estrictamente creciente a las claves $1, 2, \dots, n$.

1. **Cota por Lema de Acceso:** Acote el costo total de la secuencia empleando el Lema de Acceso de Sleator y Tarjan y el análisis por función potencial.
2. **Comparación con la Sección 6:** Compare este resultado con las mediciones empíricas y conceptuales presentadas en la Sección 6.
3. **Ajustabilidad:** Determine si la cota obtenida mediante el Lema de Acceso es ajustada para este caso particular.

---

## Solución

### 1. Aplicación del Lema de Acceso

#### Asignación de Pesos y Rangos

Asignamos a cada nodo $v$ un peso constante $w(v) = 1$.

* El tamaño acumulado de la subárbol con raíz en $v$ se define como $W(v) = \sum_{u \in \text{subárbol}(v)} w(u)$, lo que satisface $1 \le W(v) \le n$.
* El rango de un nodo es $r(v) = \log_2 W(v)$.
* Para la raíz del árbol $t$, $W(t) = n$, por lo que $r(t) = \log_2 n$.
* Para cualquier nodo $x$, $W(x) \ge 1 \implies r(x) \ge 0$.

#### Costo Amortizado de un Splay Individual

Por el Lema de Acceso, el costo amortizado de la operación $\text{splay}(x)$ en un árbol con raíz $t$ está acotado superiormente por:

$$\hat{c}(x) \le 3(r(t) - r(x)) + 1$$

Dado que $r(t) = \log_2 n$ y $r(x) \ge 0$, el costo amortizado de cada acceso individual se acota como:

$$\hat{c}(x) \le 3 \log_2 n + 1 = \mathcal{O}(\log n)$$

#### Acotación del Costo Total Real de la Secuencia

Sumando el costo amortizado sobre los $n$ accesos consecutivos:

$$\sum_{i=1}^n c_i = \sum_{i=1}^n \hat{c}_i + \Phi_0 - \Phi_n$$

donde la función potencial global del árbol corresponde a la suma de los rangos: $\Phi = \sum_{v} r(v)$.

1. **Suma de costos amortizados:**

$$\sum_{i=1}^n \hat{c}_i \le \sum_{i=1}^n (3 \log_2 n + 1) = 3n \log_2 n + n = \mathcal{O}(n \log n)$$


2. **Diferencia de potencial ($\Phi_0 - \Phi_n$):**
* **Potencial inicial $\Phi_0$:** El árbol comienza como un camino de $n$ nodos. Los tamaños de las subárboles van desde $1$ hasta $n$, por lo que $\Phi_0 = \sum_{k=1}^n \log_2 k = \log_2(n!) = \Theta(n \log n)$.
* **Potencial final $\Phi_n$:** Todos los rangos satisfacen $r(v) \ge \log_2(1) = 0$, de donde $\Phi_n \ge 0$.
* **Crédito neto:** Por lo tanto, $\Phi_0 - \Phi_n \le \Theta(n \log n)$.



Combinando la suma amortizada con el balance de potencial inicial, el Lema de Acceso acota el costo real total mediante:

$$\text{Costo Total Real} = \sum_{i=1}^n c_i \le \mathcal{O}(n \log n)$$

---

### 2. Comparación con las Mediciones de la Sección 6

En la Sección 6 se analiza el comportamiento estructural del *Splay Tree* frente a heurísticas de auto-organización más simples (como *move-to-root* sin rotaciones dobles *zig-zig*).

* Mientras que *move-to-root* se degrada a un costo de $\Theta(n)$ por acceso sobre un camino degenerado (acumulando un costo cuadrático total de $\Theta(n^2)$), la operación *splay* de Tarjan y Sleator ejecuta un reestructurado radical del camino de acceso.
* Cada paso *zig-zig* sobre la secuencia $1, 2, \dots, n$ reduce aproximadamente a la mitad la profundidad de todos los nodos en el camino atravesado.
* Consecuentemente, a medida que se accede secuencialmente a los elementos, el árbol se "desenrolla" y se transforma de forma dinámica en una estructura altamente balanceada, reduciendo la distancia promedio de los accesos posteriores a un costo constante amortizado ($\mathcal{O}(1)$).

---

### 3. ¿Es ajustada la cota $\mathcal{O}(n \log n)$?

**No, la cota $\mathcal{O}(n \log n)$ derivada de la aplicación directa del Lema de Acceso no es ajustada para esta secuencia específica; constituye una sobreestimación holgada.**

#### Justificación Teórica

* **Costo Real $\mathcal{O}(n)$:** Tarjan y Sleator demostraron formalmente en su **Teorema del Acceso Secuencial** (*Sequential Access Theorem*) que acceder a todas las claves en orden $1, 2, \dots, n$ sobre un *Splay Tree* de $n$ nodos (independientemente de su forma o topología inicial) toma un tiempo total real de **$\mathcal{O}(n)$**, equivalente a $\mathcal{O}(1)$ pasos en promedio por acceso.
* **Causa de la Holgura del Lema:** El Lema de Acceso evalúa cada operación de forma aislada asignando una cota genérica de $\mathcal{O}(\log n)$ por paso. No logra capturar el efecto acumulativo de compresión del camino que generan las rotaciones *zig-zig* coordinadas durante una ráfaga de accesos ordenados, omitiendo el hecho de que la profundidad promedio colapsa rápidamente y vuelve el costo promedio estrictamente constante.