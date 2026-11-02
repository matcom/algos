## Problema

Considere el algoritmo de incremento de un contador binario en una máquina de Turing de una cinta (con el cabezal ubicado inicialmente en el bit menos significativo -LSB- y regresando a él al finalizar).
Demuestre formalmente mediante el método de la función potencial que una secuencia de $m$ operaciones de incremento consecutivas, partiendo desde el valor inicial $0$, requiere un costo total de $\mathcal{O}(m)$ pasos, a pesar de que una única operación en el peor caso pueda costar $\Theta(\log m)$ pasos.

---

## Solución

### 1. Mecánica de la Máquina de Turing y Costo en el Peor Caso

En la representación binaria del contador, un incremento simula la propagación de un acarreo de derecha a izquierda:

1. El cabezal se desplaza hacia la izquierda desde el LSB, encontrando $t$ bits $1$ consecutivos, los cuales transforma en $0$.
2. Al hallar el primer bit $0$ (o una casilla en blanco $\_$), lo cambia a $1$ y detiene la propagación del acarreo.
3. Finalmente, el cabezal retorna hacia la derecha recorriendo exactamente tantas casillas como retrocedió, volviendo a posicionarse en el LSB.

Para el conteo de pasos, consideramos que al actualizar el primer $0$ (o blanco), el cabezal también se desplaza una posición hacia la izquierda antes de invertir el sentido y regresar. Por tanto, el recorrido de retorno tiene la misma longitud que el recorrido inicial.

#### Costo de una Operación Individual

Si el contador tiene $k$ bits y todos son $1$ (por ejemplo, $n=2^k-1$, representado como $111\dots1$), se produce el peor caso para esa longitud:

* El recorrido hacia la izquierda toma $k+1$ pasos ($k$ unos convertidos a ceros más el cambio del cero final a uno).
* El retorno hacia la derecha toma $k+1$ pasos.

Por lo tanto, el costo de esa operación es:


$$c_i = 2(k+1) = \Theta(\log(n+1))$$

En las primeras $m$ operaciones, el contador toma valores desde $0$ hasta $m-1$. Por tanto, el máximo número de unos consecutivos que pueden encontrarse desde el LSB es $\lfloor\log_2 m\rfloor$. Así, el peor costo individual dentro de la secuencia es:


$$c_{\max} = 2(\lfloor\log_2 m\rfloor+1) = \Theta(\log m)$$

---

### 2. Análisis Amortizado mediante el Método del Potencial

Para demostrar que el costo acumulado de $m$ incrementos es $\mathcal{O}(m)$, definimos una función potencial $\Phi$ que penalice o premie el estado de la estructura en función del número de bits $1$ presentes en la cinta.

#### Definición de la Función Potencial

Sea $S_i$ el estado del contador binario tras la $i$-ésima operación de incremento. Definimos:


$$\Phi(S_i) = 2 \cdot (\text{número de bits } 1 \text{ presentes en la representación binaria tras la operación } i)$$

#### Propiedades Fundamentales de $\Phi$:

1. **Valor inicial:** $\Phi(S_0) = 0$, puesto que al iniciar en $0$ no existen bits $1$ en la cinta.
2. **No negatividad:** $\Phi(S_i) \geq 0$ para todo $i \geq 0$, ya que la cantidad de bits $1$ es siempre un entero no negativo.

---

### 3. Cálculo del Costo Amortizado ($\hat{c}_i$)

Supongamos que en la $i$-ésima operación el contador posee $t \geq 0$ bits $1$ consecutivos en sus posiciones menos significativas antes de cambiar.

1. **Costo real ($c_i$):**
* El cabezal recorre los $t$ unos transformándolos en ceros ($t$ pasos a la izquierda).
* Cambia el siguiente $0$ (o espacio en blanco) a $1$ ($1$ paso a la izquierda).
* Regresa hasta el LSB recorriendo $t+1$ casillas ($t+1$ pasos a la derecha).
* **Total real:**

$$c_i = t + 1 + (t + 1) = 2t + 2$$




2. **Cambio de potencial ($\Delta\Phi_i = \Phi(S_i) - \Phi(S_{i-1})$):**
* Se destruyen $t$ bits $1$ (que pasan a $0$), reduciendo el potencial en $2t$.
* Se crea $1$ nuevo bit $1$ (el cero que pasa a $1$), aumentando el potencial en $+2$.
* **Total cambio:**

$$\Delta\Phi_i = 2 \cdot (1 - t) = 2 - 2t$$




3. **Costo amortizado ($\hat{c}_i$):**

$$\hat{c}_i = c_i + \Delta\Phi_i = (2t + 2) + (2 - 2t) = 4$$



El costo amortizado de cada operación de incremento es una constante exacta: $\hat{c}_i = 4$.

---

### 4. Conclusión del Costo Total

Por la propiedad fundamental del análisis amortizado, el costo total de una secuencia de $m$ operaciones se relaciona con la suma de sus costos amortizados mediante:


$$\sum_{i=1}^{m} c_i = \sum_{i=1}^{m} \hat{c}_i + \Phi(S_0) - \Phi(S_m)$$

Dado que $\Phi(S_0) = 0$ y $\Phi(S_m) \geq 0$:


$$\sum_{i=1}^{m} c_i \leq \sum_{i=1}^{m} \hat{c}_i = \sum_{i=1}^{m} 4 = 4m$$

Queda demostrado formalmente que el costo total de $m$ incrementos consecutivos desde $0$ está acotado superiormente por $4m$, lo que establece una complejidad total de $\mathcal{O}(m)$.

---

### 5. Interpretación Intuitiva (Método de Contabilidad)

* A cada incremento se le cobra una tarifa fija de $4$ monedas (costo amortizado).
* $2$ monedas pagan directamente los pasos asociados a la escritura del nuevo bit $1$ ($1$ paso de ida y $1$ de vuelta).
* Las $2$ monedas restantes se almacenan como crédito adjunto a ese nuevo bit $1$.
* Cuando en operaciones futuras dicho bit $1$ deba ser destruido (convertido en $0$ por propagación de acarreo), sus $2$ monedas de crédito acumuladas pagan exactamente los $2$ pasos reales necesarios para realizar la transición y retornar sobre él.