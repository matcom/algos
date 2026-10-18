# Ejercicio 13 — Splay tree: camino inicial, accesos ordenados

> **Enunciado:** En un splay tree que empieza como un camino de $n$ nodos se accede a las claves $1, \ldots, n$ en orden. Acota el costo total con el lema de acceso y la cuenta de la sección 5 de la conferencia 4, y compáralo con lo que mide la sección 6. ¿Es ajustada la cota?


## 1. La cuenta de la sección 5 (potencial telescópico)

Sea $\Phi_i$ el potencial tras el $i$-ésimo acceso, $\Phi_0$ el potencial del camino inicial, y $\hat{c}_i = c_i + \Phi_i - \Phi_{i-1}$. Sumando sobre $m$ accesos:

$$\sum_{i=1}^{m} c_i \;=\; \sum_{i=1}^{m} \hat{c}_i \;-\; (\Phi_m - \Phi_0) \;\leq\; \sum_{i=1}^{m} \hat{c}_i + \Phi_0$$

(pues $\Phi_m \geq 0$). Aplicando el lema de acceso término a término, con $r_i(t) = \log_2 n$ (la raíz siempre tiene el árbol entero):

$$\sum_{i=1}^{m} c_i \;\leq\; \sum_{i=1}^{m} \bigl[3(\log_2 n - r_i(x_i)) + 1\bigr] + \Phi_0 \;\leq\; m\,(3\log_2 n + 1) + \Phi_0.$$

Necesitamos $\Phi_0$. En el camino, el subárbol de la clave $k$ tiene $k$ nodos (las claves $1, \ldots, k$ cuelgan de ella), luego $s(k) = k$ y $r(k) = \log_2 k$. Así

$$\Phi_0 = \sum_{k=1}^{n} \log_2 k = \log_2(n!) \leq n \log_2 n.$$

Con $m = 3n$:

$$\sum_{i=1}^{3n} c_i \;\leq\; 3n\,(3\log_2 n + 1) + n \log_2 n \;=\; O(n \log n).$$

Esta es la cota que se obtiene "aplicando el lema y la cuenta de la sección 5". Es correcta pero no ajustada, y ahora veremos por qué y cuál es el costo real.



## 2. Qué hace realmente splay con accesos en orden creciente

### 2.1 Primer acceso: `splay(1)`

La clave 1 está al fondo del camino, profundidad $n-1$. El camino hasta la raíz es un zig-zig continuo (todo hijo izquierdo, abuelo también izquierdo). En cada paso zig-zig se rota primero el padre y luego $x$; tras $\lceil (n-1)/2 \rceil$ pasos $x$ queda en la raíz. Costo $n-1$ rotaciones (cada par zig-zig son 2 rotaciones; con $n-1$ niveles exactos).

Tras esto, el árbol se ha "plegado" sustancialmente: los antiguos nodos $2, 3, \ldots, n$ cuelgan del subárbol derecho de 1 en una estructura de profundidad logarítmica (el zig-zig produce el efecto de árbol balanceado en el camino de acceso; es la observación clásica de Sleator–Tarjan: hacer splay sobre el mínimo de un camino produce un árbol con profundidades $O(\log n)$ en promedio).

### 2.2 Accesos sucesivos $2, 3, \ldots, n$ en la primera ronda

Tras `splay(1)`, la clave 2 no está al fondo: está en el subárbol derecho de 1, y su profundidad es ya pequeña. El acceso `splay(2)` la sube; la reorganización deja el árbol aún más "plano" por la izquierda. Este patrón se repite: cada `splay(k)` encuentra $k$ a profundidad pequeña porque el acceso previo a $k-1$ lo dejó cerca de la raíz, y el zig-zig reacomoda el resto.

Este es el fenómeno medido en la sección 6 de la conferencia 4: al recorrer las claves en orden partiendo de un camino, splay da un costo por acceso plano, mientras que subir a la raíz da $\Theta(n)$ por acceso.

### 2.3 Rondas segunda y tercera

Al terminar la primera ronda el árbol está reorganizado; en las rondas siguientes el patrón ordenado es todavía más favorable (los accesos consecutivos están cerca). La sección 6 mide justamente tres rondas para amortiguar el efecto de la primera.




## 3. El costo real medido (sección 6)

La tabla de la conferencia 4, con `costo_por_acceso(splay, n, rondas=3)`:

| $n$ | splay (rot/acc.) | subir a la raíz (rot/acc.) | $\log_2 n$ |
|---|---|---|---|
| 100 | 4.2 | 50.5 | 6.6 |
| 200 | 4.2 | 100.5 | 7.6 |
| 400 | 4.3 | 200.5 | 8.6 |
| 800 | 4.4 | 400.5 | 9.6 |

**Lectura:**

- **Subir a la raíz:** $n/2$ rotaciones por acceso $\Rightarrow$ $\Theta(n)$ por acceso, $\Theta(n^2)$ total en una ronda. Es exactamente el ejercicio 4 de la conferencia 4.

- **Splay:** el costo por acceso es constante (oscila entre 4.2 y 4.4, sin crecer con $n$). Total en tres rondas: $\Theta(3n) = \Theta(n)$. En los ejes logarítmicos de la figura 3, splay tiene pendiente 0; subir a la raíz tiene pendiente 1.

Entonces:

> **Costo real de la secuencia:** $\Theta(n)$ (lineal en el número de accesos).

No $\Theta(n \log n)$. La cota del lema no es ajustada para esta secuencia.

## 4. ¿Por qué el lema da $O(n \log n)$ y el costo real es $O(n)$? (El paso delicado)

La razón es que el lema de acceso es una cota por acceso suelto, válida para cualquier acceso en cualquier momento, y por eso paga cada acceso como si hubiera que subir desde el fondo. Pero en esta secuencia concreta:

- El potencial inicial $\Phi_0 = n \log_2 n$ es grande y se "gasta" en el primer acceso, que es el único realmente caro ($n-1$ rotaciones). Los accesos siguientes encuentran el árbol ya reorganizado.

- Las diferencias $r_i(x_i)$ son pequeñas en promedio: tras `splay(k-1)`, el nodo $k$ está a profundidad $O(1)$ amortizada, así que $r(t) - r(x_i) \approx \log_2 n - \log_2(\text{tamaño del subárbol de } x_i)$, que es pequeña. El lema acota cada término por $3\log_2 n + 1$, pero el valor típico es $O(1)$.

Formalmente: el lema es una cota de peor caso amortizado por operación, y aquí el peor caso (acceso al fondo) ocurre esencialmente una sola vez. La suma telescópica

$$\sum c_i = \sum \hat{c}_i - (\Phi_m - \Phi_0)$$

tiene un término $-\Phi_0$ grande que la cota bruta $\sum \hat{c}_i + \Phi_0$ desaprovecha: en la práctica $\Phi_m$ no es 0, y $\Phi_m - \Phi_0$ absorbe buena parte del costo. La cota $O(n \log n)$ proviene de descartar esa cancelación.

Dicho de otro modo: el lema es correcto pero flojo cuando se aplica acceso a acceso sin explotar que la secuencia está ordenada y que el árbol se reorganiza. La cota de $\Theta(m \log n)$ es la garantía general de splay (peor caso para cualquier secuencia de $m$ accesos), y esta secuencia particular está muy por debajo de ella.

## 5. Respuesta a "¿es ajustada la cota?"

La cota $O(n \log n)$ que sale del lema + cuenta de la sección 5 es correcta pero **no ajustada**. Sobrestima el costo por un factor $\Theta(\log n)$.

La cota ajustada para esta secuencia es $\Theta(n)$, como confirma la medición de la sección 6 (costo por acceso constante, total lineal en $m = 3n$).

Además, el contraste con subir a la raíz es total: misma secuencia, misma estructura inicial, y allí el costo es $\Theta(n^2)$ por ronda. La diferencia está enteramente en el caso zig-zig (rotar primero el padre), como explica la sección 5 de la conferencia 4 al analizar por qué subir a la raíz no alcanza: sin agrupar las rotaciones de a dos, no aparece la cancelación $-2$ de la concavidad, y cada rotación se paga completa.

**Observación fina (por qué splay es "plano" aquí).** En un camino, hacer splay del mínimo $1$ con zig-zig repetido produce un árbol donde el camino original queda "doblado" en profundidad logarítmica. En la siguiente ronda, el acceso $2$ está ya a profundidad $O(\log n)$ (incluso $O(1)$ amortizado por el efecto acumulado), y así sucesivamente. Este es el mismo mecanismo que hace que splay tenga la propiedad de árbol estáticamente óptimo y la propiedad de secuencia de acceso, pero aquí basta la observación empírica de la sección 6: el costo por acceso es constante.