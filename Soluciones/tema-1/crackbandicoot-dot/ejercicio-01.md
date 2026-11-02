## Planteamiento

Sea $T(n)$ el tiempo de ejecución, y sea $n_1$ el mayor tamaño de entrada resoluble en una hora en la máquina antigua, de modo que $T(n_1) = H$ (una hora de trabajo de la máquina antigua). Una máquina 1000 veces más rápida hace $1000H$ de trabajo en la misma hora, así que el nuevo tamaño $n_2$ satisface

$$T(n_2) = 1000\,T(n_1).$$

Usamos la convención habitual de tratar $T(n) \approx c\,f(n)$, de modo que la constante $c$ se cancela. El factor de crecimiento es $k = n_2/n_1$.

## Θ(n²)

$$c\,n_2^2 = 1000\,c\,n_1^2 \;\Rightarrow\; \left(\frac{n_2}{n_1}\right)^2 = 1000 \;\Rightarrow\; k = \sqrt{1000} \approx 31,6.$$

El tamaño crece por un factor de aproximadamente **31,6**. Esto es independiente de $n_1$.

## Θ(n log n)

$$n_2 \log n_2 = 1000\, n_1 \log n_1.$$

Sustituimos $n_2 = k\,n_1$:

$$k\,n_1\,(\log n_1 + \log k) = 1000\, n_1 \log n_1 \;\Rightarrow\; k\left(1 + \frac{\log k}{\log n_1}\right) = 1000.$$

Entonces

$$k = \frac{1000}{1 + \frac{\log k}{\log n_1}}.$$

Esto es menor que 1000, y depende de $n_1$,nótese que:

- A medida que $n_1 \to \infty$, $\log k / \log n_1 \to 0$, así que $k \to 1000$ desde abajo. El crecimiento es “casi lineal”.
- Para cualquier $n_1$ fijo, $k < 1000$ pero mucho mayor que $\sqrt{1000}$.
