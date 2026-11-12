## Problema

Dada una nueva computadora capaz de ejecutar operaciones a una velocidad **$1000$ veces mayor** que la máquina original, determine en qué factor aumenta el tamaño de la entrada ($N$) que puede ser procesado en el mismo intervalo de tiempo (una hora) para dos complejidades algorítmicas distintas:

1. Un algoritmo con complejidad temporal $T(N) \in \Theta(N^2)$.
2. Un algoritmo con complejidad temporal $T(N) \in \Theta(N \log N)$.

Estime formalmente los dos factores de incremento $k = \frac{N_2}{N_1}$ correspondientes.

---

## Solución

### 1. Marco General

Sea $N_1$ el tamaño máximo de la entrada procesada por la computadora original en una hora, y $N_2$ el nuevo tamaño de entrada procesable por la nueva computadora en el mismo tiempo.

Dado que la nueva máquina dispone de una capacidad de cómputo $1000$ veces mayor por unidad de tiempo, el número total de operaciones ejecutables en una hora se multiplica por $1000$. Si $T(N)$ representa el número de operaciones realizadas por el algoritmo, la relación fundamental es:

$$T(N_2) = 1000 \cdot T(N_1)$$

Definimos el factor de escalamiento del tamaño de entrada como $k = \frac{N_2}{N_1}$, de modo que $N_2 = k \cdot N_1$.

Para obtener estimaciones numéricas, utilizaremos modelos representativos de cada complejidad, considerando que los términos dominantes describen el comportamiento del algoritmo para entradas suficientemente grandes. La notación $\Theta$ por sí sola no determina una expresión exacta del número de operaciones.

---

### 2. Algoritmo $\Theta(N^2)$

Para una complejidad cuadrática, consideramos el modelo $T(N) = c \cdot N^2$, donde $c > 0$ es una constante.

Sustituyendo en la relación operacional:

$$c \cdot N_2^2 = 1000 \cdot c \cdot N_1^2$$

Como $N_2 = k \cdot N_1$:

$$c \cdot (k \cdot N_1)^2 = 1000 \cdot c \cdot N_1^2$$

Simplificando las constantes y dividiendo ambos miembros entre $N_1^2$:

$$k^2 = 1000 \implies k = \sqrt{1000} \approx 31.6227$$

**Conclusión ($\Theta(N^2)$)**

El tamaño de la entrada puede crecer aproximadamente por un factor de $\sqrt{1000} \approx 31.62$. Esta estimación es independiente de $N_1$ bajo el modelo cuadrático considerado.

---

### 3. Algoritmo $\Theta(N \log N)$

Para una complejidad cuasilineal, consideramos el modelo $T(N) = c \cdot N \log_2 N$, donde $c > 0$ es una constante.

La relación operacional se establece como:

$$c \cdot (k \cdot N_1) \log_2(k \cdot N_1) = 1000 \cdot c \cdot N_1 \log_2(N_1)$$

Simplificando las constantes y dividiendo entre $N_1$:

$$k \cdot \log_2(k \cdot N_1) = 1000 \cdot \log_2(N_1)$$

Utilizando la propiedad del logaritmo $\log_2(a \cdot b) = \log_2 a + \log_2 b$:

$$k \cdot (\log_2 N_1 + \log_2 k) = 1000 \cdot \log_2 N_1$$

Dividiendo toda la expresión entre $\log_2 N_1$:

$$k \left(1 + \frac{\log_2 k}{\log_2 N_1}\right) = 1000$$

**Análisis Asintótico y Dependencia de $N_1$**

A diferencia del caso cuadrático, el factor $k$ depende explícitamente del tamaño inicial de la entrada $N_1$:

- **Límite asintótico:** Cuando $N_1 \to \infty$, el término $\frac{\log_2 k}{\log_2 N_1}$ tiende a cero. Por tanto:

$$\lim_{N_1 \to \infty} k = 1000$$

- **Valores prácticos:** Para tamaños finitos de entrada, el término $\frac{\log_2 k}{\log_2 N_1}$ no es despreciable y el factor de crecimiento es inferior a $1000$. Resolviendo numéricamente la ecuación trascendente para distintos valores de $N_1$, obtenemos:

| $N_1$ inicial | Ecuación equivalente a resolver | Factor de incremento ($k = \frac{N_2}{N_1}$) |
| --- | --- | --- |
| $10^3$ | $k(9.9658 + \log_2 k) = 9965.78$ | $\approx 524.50$ |
| $10^6$ | $k(19.9316 + \log_2 k) = 19931.57$ | $\approx 679.34$ |
| $10^9$ | $k(29.8974 + \log_2 k) = 29897.35$ | $\approx 757.61$ |
| $N_1 \to \infty$ | $k \cdot 1 = 1000$ | $\to 1000$ |

**Conclusión ($\Theta(N \log N)$)**

El factor de incremento depende del tamaño inicial de la entrada y se aproxima asintóticamente a $1000$. Para los tamaños considerados ($10^3 \leq N_1 \leq 10^9$), el factor efectivo oscila aproximadamente entre $524$ y $758$.

---

### Resumen de Resultados

- **Para $\Theta(N^2)$:** El factor de crecimiento estimado es independiente del tamaño inicial de la entrada y viene dado por $k = \sqrt{1000} \approx 31.62$.
- **Para $\Theta(N \log N)$:** El factor de crecimiento depende del tamaño inicial de la entrada. Para los tamaños prácticos considerados, se encuentra aproximadamente entre $524$ y $758$, y tiende a $1000$ cuando $N_1 \to \infty$.

**Observación:** Estos resultados son estimaciones obtenidas a partir de los modelos representativos $T(N)=cN^2$ y $T(N)=cN\log N$. La pertenencia a $\Theta(N^2)$ o $\Theta(N\log N)$, por sí sola, no garantiza esos factores exactos de escalamiento. 