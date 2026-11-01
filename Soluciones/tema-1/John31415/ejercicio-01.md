Para encontrar en qué factor aumenta el tamaño de la entrada ($N$), igualamos el número de operaciones que la computadora puede realizar en una hora.

Si la computadora original procesa un tamaño de entrada $N_1$ en una hora, la nueva computadora (1000 veces más rápida) ejecutará **1000 veces más operaciones** en el mismo tiempo.

---

### 1. Algoritmo $\Theta(N^2)$

La relación de operaciones es:


$$(N_2)^2 = 1000 \cdot (N_1)^2$$

Despejando $N_2$:


$$N_2 = \sqrt{1000} \cdot N_1 \approx 31.62 \cdot N_1$$

El tamaño de la entrada crece por un factor de aproximadamente **31.6** ($\sqrt{1000}$).

---

### 2. Algoritmo $\Theta(N \log N)$

La relación de operaciones es:


$$N_2 \log_2(N_2) = 1000 \cdot N_1 \log_2(N_1)$$

Definiendo el factor de incremento $k = \frac{N_2}{N_1}$, la ecuación se transforma en:


$$k \cdot N_1 \log_2(k \cdot N_1) = 1000 \cdot N_1 \log_2(N_1)$$

Dividiendo por $N_1$ e expandiendo el logaritmo:


$$k (\log_2 N_1 + \log_2 k) = 1000 \log_2 N_1$$

$$k \left(1 + \frac{\log_2 k}{\log_2 N_1}\right) = 1000$$

Para valores de $N_1$ lo suficientemente grandes (donde $\log_2 N_1 \gg \log_2 k$), el término $\frac{\log_2 k}{\log_2 N_1}$ se vuelve muy pequeño, por lo que **$k \approx 1000$**.

Si consideramos valores prácticos típicos de $N_1$:

| $N_1$ inicial | Ecuación a resolver | Factor $k = N_2 / N_1$ |
| --- | --- | --- |
| $10^3$ | $k (10 + \log_2 k) = 10000$ | $\approx 547$ |
| $10^6$ | $k (20 + \log_2 k) = 20000$ | $\approx 704$ |
| $10^9$ | $k (30 + \log_2 k) = 30000$ | $\approx 778$ |
| $N_1 \to \infty$ | $k \to 1000$ | **$\approx 1000$** |

El tamaño de la entrada crece por un factor ligeramente menor a 1000 (típicamente entre **500 y 800** para rangos computacionales prácticos), tendiendo asintóticamente a **1000** a medida que $N_1 \to \infty$.

---

### Resumen de estimaciones

* **Para $\Theta(N^2)$:** El factor de crecimiento es **$\approx 31.62$** ($\sqrt{1000}$).
* **Para $\Theta(N \log N)$:** El factor de crecimiento es **$\approx 1000$** (en la práctica entre **$500$ y $800$** según el $N_1$ base).