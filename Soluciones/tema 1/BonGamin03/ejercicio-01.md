# Ejercicio 1 

## Enunciado
Una computadora mil veces más rápida. ¿Cuánto crece el tamaño de entrada que se resuelve en una hora con un algoritmo $\Theta(n^2)$? ¿Y con uno $\Theta(n \log n)$? Estima los dos factores. (Conferencia 1)

---

## Modelo Formal
Sea $T(n)$ la cantidad de operaciones ejecutadas para procesar una entrada de tamaño $n$. Si la nueva computadora es **1000 veces más rápida**, en la misma cantidad de tiempo disponible (una hora) puede realizar **1000 veces más operaciones**.

Por tanto, si $n$ es el tamaño de entrada resolbible en la computadora original y $n'$ es el nuevo tamaño resolbible en el mismo tiempo, la relación fundamental de trabajo viene dada por:

$$T(n') = 1000 \cdot T(n)$$

---

## Parte 1: Algoritmo $\Theta(n^2)$

### 1. Deducción Algebraica
Asumimos $T(n) = c \cdot n^2$ para alguna constante $c > 0$.

Sustituyendo en la relación fundamental:
$$c \cdot (n')^2 = 1000 \cdot c \cdot n^2$$

Dividiendo entre $c$ en ambos lados:
$$(n')^2 = 1000 \cdot n^2$$

Tomando raíz cuadrada en ambos lados:
$$n' = \sqrt{1000} \cdot n$$

Calculando el valor numérico de $\sqrt{1000}$:
$$\sqrt{1000} \approx 31.62277$$

### 2. Factor Estimado
* **Factor de crecimiento ($\Theta(n^2)$):** $\approx \mathbf{31.62}$
* **Conclusión:** El tamaño de la entrada que se puede resolver en una hora se **multiplica por aproximadamente $31.62$**.

---

## Parte 2: Algoritmo $\Theta(n \log n)$

### 1. Planteamiento Ecuacional
Asumimos $T(n) = c \cdot n \log_2 n$ para alguna constante $c > 0$.

Sustituyendo en la relación fundamental:
$$c \cdot n' \log_2 n' = 1000 \cdot c \cdot n \log_2 n$$

Dividiendo entre $c$:
$$n' \log_2 n' = 1000 \cdot n \log_2 n \quad \text{--- (Ecuación 1)}$$

---

### 2. Deducción de la Aproximación Algebraica (Paso a Paso)

#### Paso 2.1: Aplicar logaritmo para aproximar $\log_2 n'$
Tomamos logaritmo en base 2 a ambos lados de la Ecuación 1:

$$\log_2(n' \log_2 n') = \log_2(1000 \cdot n \log_2 n)$$

Aplicando propiedades de logaritmos ($\log(a \cdot b) = \log a + \log b$):

$$\log_2 n' + \log_2(\log_2 n') = \log_2(1000) + \log_2 n + \log_2(\log_2 n)$$

Dado que la función doble logaritmo $\log_2(\log_2 x)$ crece de manera extremadamente lenta, para valores de entrada prácticos la diferencia entre $\log_2(\log_2 n')$ y $\log_2(\log_2 n)$ es despreciable ($\log_2(\log_2 n') \approx \log_2(\log_2 n)$).

Cancelando estos términos en ambos lados:

$$\log_2 n' \approx \log_2(1000) + \log_2 n$$

Como $\log_2(1000) \approx 9.96578$:

$$\log_2 n' \approx \log_2 n + 9.965 \quad \text{--- (Ecuación 2)}$$

---

#### Paso 2.2: Sustituir $\log_2 n'$ en la Ecuación 1
De la Ecuación 1, despejamos $n'$:

$$n' = \frac{1000 \cdot n \log_2 n}{\log_2 n'}$$

Sustituimos el valor aproximado de $\log_2 n'$ (obtenido en la Ecuación 2) en el denominador:

$$n' \approx \frac{1000 \cdot n \log_2 n}{\log_2 n + 9.965}$$

---

#### Paso 2.3: Reorganizar en forma de factor de escala
Factorizamos $\log_2 n$ en el denominador:

$$\log_2 n + 9.965 = \log_2 n \left( 1 + \frac{9.965}{\log_2 n} \right)$$

Sustituyendo esto en la fracción:

$$n' \approx \frac{1000 \cdot n \log_2 n}{\log_2 n \left( 1 + \frac{9.965}{\log_2 n} \right)}$$

Cancelamos el término $\log_2 n$ presente en el numerador y en el denominador:

$$n' \approx \frac{1000 \cdot n}{1 + \frac{9.965}{\log_2 n}}$$

Reescribiendo la expresión para aislar el factor multiplicativo respecto a $n$:

$$n' \approx 1000 \cdot n \cdot \left( \frac{1}{1 + \frac{9.965}{\log_2 n}} \right)$$

---

### 3. Estimación del Factor según el Tamaño de Entrada $n$

A diferencia del caso $\Theta(n^2)$, el factor de crecimiento para $\Theta(n \log n)$ depende ligeramente del tamaño original de la entrada $n$:

| Tamaño inicial $n$ | $\log_2 n$ | Factor multiplicativo $\left( \frac{n'}{n} \right)$ |
| :--- | :--- | :--- |
| **$n = 10^3$** | $\approx 10.00$ | $\frac{1000}{1 + \frac{9.965}{10.00}} = \frac{1000}{1.9965} \approx \mathbf{500.88}$ |
| **$n = 10^6$** | $\approx 19.93$ | $\frac{1000}{1 + \frac{9.965}{19.93}} = \frac{1000}{1.5000} \approx \mathbf{666.67}$ |
| **$n = 10^9$** | $\approx 29.90$ | $\frac{1000}{1 + \frac{9.965}{29.90}} = \frac{1000}{1.3333} \approx \mathbf{750.00}$ |
| **$n \to \infty$** | $\infty$ | $\lim_{n \to \infty} \frac{1000}{1 + \frac{9.965}{\log_2 n}} = \mathbf{1000.00}$ |

---