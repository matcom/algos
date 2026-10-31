# Ejercicio 1: Una computadora mil veces más rápida

> **Enunciado.** Una computadora mil veces más rápida. ¿Cuánto crece el tamaño de entrada que se resuelve en una hora con un algoritmo Θ(n²)? ¿Y con uno Θ(n log n)? Estima los dos factores. (C1)


## 1. Enunciado preciso del problema

Antes de calcular nada, hay que fijar qué se está preguntando, porque el enunciado esconde dos decisiones que cambian la respuesta. Este es el primer reflejo que pide la conferencia 2: precisar el problema antes de proponer un algoritmo o un cálculo.

**Qué es la entrada.** Un algoritmo con costo $\Theta(n^2)$ o $\Theta(n \log n)$, donde $n$ es el tamaño de la entrada.

**Qué es la salida.** Dos factores de crecimiento: el factor $F$ por el que se multiplica el mayor $n$ que cabe en una hora cuando la computadora pasa de $S$ operaciones por segundo a $1000S$ operaciones por segundo.

**Precisiones que el enunciado no da y hay que fijar:**

- **El modelo de cómputo.** Contamos operaciones en el modelo word RAM: cada operación elemental cuesta 1. La velocidad de la máquina es el número de operaciones por segundo.

- **Las constantes.** Como el análisis es asintótico, trabajamos con las funciones $n^2$ y $n \log_2 n$ sin constantes multiplicativas. 

- **La base del logaritmo.** La base no importa dentro de $\Theta$, pero sí en el valor numérico del factor. Usamos $\log_2$ porque es la base natural en análisis de algoritmos (Teorema Maestro, árboles de decisión).

- **Qué significa "una hora".** El presupuesto de operaciones es $P = 3600 \cdot S$, donde $S$ es la velocidad en operaciones por segundo.

## 2. Observación clave

La pregunta no es "¿cuánto tarda el algoritmo con una entrada de tamaño $n$?", sino la inversa: ¿cuál es el mayor $n$ que cabe en un presupuesto fijo de operaciones?

Esto es exactamente lo que hace el código de la conferencia 1, §7, con la función `mayor_n`: buscar por búsqueda binaria el mayor $n$ tal que $\text{costo}(n) \leq P$.

Formalmente, si el costo es $T(n)$ y el presupuesto es $P$:

$$n_{\max}(P) = \max\{\, n \in \mathbb{N} : T(n) \leq P \,\}.$$

El factor que pide el ejercicio es

$$F = \frac{n_{\max}(1000\,P)}{n_{\max}(P)}.$$

Como $T$ es creciente, $n_{\max}$ está bien definida y $F > 1$.



## 3 Procedimiento (Caso $\Theta(n^2)$)

Sin constantes, $T(n) = n^2$. El mayor $n$ que cabe en el presupuesto $P$ es

$$n_{\max}(P) = \lfloor \sqrt{P} \rfloor.$$

Porque el costo del algoritmo es $\Theta(n^2)$, o sea, aproximadamente $n^2$ operaciones. Si queremos que quepa en el presupuesto $P$:

$$n^2 \leq P$$

Despejando $n$:

$$n \leq \sqrt{P}$$

Con la computadora original, el mayor $n$ es $\sqrt{P}$. Con la computadora $1000$ veces más rápida, el presupuesto es $1000\,P$, y el mayor $n$ es

$$n_{\max}(1000\,P) = \sqrt{1000P} = \sqrt{1000} \cdot \sqrt{P}.$$

## El factor

$$F_{n^2} = \frac{\sqrt{1000P}}{\sqrt{P}} = \sqrt{1000} = 10\sqrt{10} \approx 31{,}62.$$

## Interpretación

El tamaño de entrada crece por un factor $\sqrt{1000} \approx 31{,}6$. 
Es decir, cuando la computadora es mil veces más rápida, con un algoritmo cuadrático no se resuelven entradas mil veces más grandes, sino solo unas 32 veces más grandes que las que resolvía la computadora original. En otras palabras, el aumento de velocidad de la máquina se traduce en una mejora de apenas $32\times$ en el tamaño de entrada.


## Comprobación con una máquina de $10^9$ operaciones por segundo

$$P = \underbrace{10^9}_{\text{operaciones/segundo}} \times \underbrace{3600}_{\text{segundos en una hora}} = 3{,}6 \times 10^{12} \text{ operaciones}$$

Con la computadora mil veces más rápida:

$$P' = 1000 \times P = 3{,}6 \times 10^{15} \text{ operaciones}$$

**Computadora normal**

$$n_{\max}(P) = \lfloor \sqrt{P} \rfloor = \lfloor \sqrt{3{,}6 \times 10^{12}} \rfloor$$

$$\sqrt{3{,}6 \times 10^{12}} = \sqrt{3{,}6} \times 10^6 \approx 1{,}897 \times 10^6 = 1\,897\,366$$

Entonces:

$$n_{\max}(3{,}6 \times 10^{12}) = 1\,897\,366$$

**Computadora mil veces más rápida**

$$n_{\max}(P') = \lfloor \sqrt{3{,}6 \times 10^{15}} \rfloor$$

$$\sqrt{3{,}6 \times 10^{15}} = \sqrt{3{,}6} \times 10^{7{,}5} \approx 1{,}897 \times 10^7 \times \sqrt{10} \approx 5{,}999 \times 10^7$$

Más exactamente:

$$\sqrt{3{,}6 \times 10^{15}} = \sqrt{36 \times 10^{14}} = 6 \times 10^7 = 60\,000\,000$$

Entonces:

$$n_{\max}(P') = 60\,000\,000$$

**El factor**

$$F_{n^2} = \frac{60\,000\,000}{1\,897\,366} \approx 31{,}62$$

Que coincide con $\sqrt{1000} = 10\sqrt{10} \approx 31{,}62$. ✓

## 4. Procedimiento (Caso $\Theta(n \log n)$) 

Sea

$$f(n) = n \log_2 n.$$

En la computadora lenta:

$$n_1 \log_2 n_1 = C.$$

En la computadora rápida:

$$n_2 \log_2 n_2 = 1000\,C.$$

Queremos estimar

$$\frac{n_2}{n_1}.$$

## Método: cociente de las ecuaciones

Dividimos la ecuación de la computadora rápida entre la de la lenta:

$$\frac{n_2 \log_2 n_2}{n_1 \log_2 n_1} = 1000.$$

Sea

$$r = \frac{n_2}{n_1}.$$

Entonces $n_2 = r\,n_1$, y sustituyendo:

$$r \cdot \frac{\log_2(r\,n_1)}{\log_2 n_1} = 1000.$$

Usamos $\log_2(r\,n_1) = \log_2 r + \log_2 n_1$:

$$r\left(1 + \frac{\log_2 r}{\log_2 n_1}\right) = 1000.$$

## Aproximación para $n$ grande

Para $n_1$ grande, el término

$$\frac{\log_2 r}{\log_2 n_1}$$

es pequeño comparado con 1 mientras $r$ no sea exponencialmente grande. Si lo despreciamos en primera aproximación:

$$r \approx 1000.$$

Pero eso no es exacto: al crecer $n$, el factor $\log n$ también crece, así que se necesita un $r$ un poco menor que 1000 para compensar.

## Refinamiento

Volvemos a

$$r\left(1 + \frac{\log_2 r}{\log_2 n_1}\right) = 1000.$$

Llamemos

$$\varepsilon = \frac{\log_2 r}{\log_2 n_1}.$$

Entonces

$$r = \frac{1000}{1 + \varepsilon}.$$

Como $\varepsilon > 0$ (porque $r > 1$), se tiene

$$r < 1000.$$

Es decir, el factor es ligeramente menor que 1000.

## Estimación concreta

Tomemos un valor típico de referencia, por ejemplo $n_1 = 10^6$. Entonces

$$\log_2 n_1 = \log_2 10^6 \approx 19{,}93.$$

Probamos $r = 1000$:

$$\varepsilon = \frac{\log_2 1000}{19{,}93} \approx \frac{9{,}97}{19{,}93} \approx 0{,}500.$$

Entonces

$$r \approx \frac{1000}{1{,}500} \approx 666{,}7.$$

Comprobamos con $r = 667$:

$$\varepsilon = \frac{\log_2 667}{19{,}93} \approx \frac{9{,}38}{19{,}93} \approx 0{,}471,$$

$$r \approx \frac{1000}{1{,}471} \approx 679{,}8.$$

Iterando, se estabiliza alrededor de

$$r \approx 680\text{–}690.$$

Para $n_1$ más grande, $\log_2 n_1$ es mayor, $\varepsilon$ es menor, y $r$ se acerca más a 1000. Por ejemplo, con $n_1 = 10^{12}$:

$$\log_2 n_1 \approx 39{,}86, \quad \varepsilon \approx \frac{9{,}97}{39{,}86} \approx 0{,}25, \quad r \approx \frac{1000}{1{,}25} = 800.$$

## Interpretación

Con un algoritmo $\Theta(n \log n)$, el factor de crecimiento del tamaño de entrada es cercano a 1000, pero un poco menor, y depende de $n_1$:

$$\frac{n_2}{n_1} \approx 1000 \text{ menos una corrección logarítmica}.$$

En la práctica, para tamaños de entrada razonables, el factor está entre 600 y 900, y tiende a 1000 cuando $n_1 \to \infty$.