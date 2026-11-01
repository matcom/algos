**Problema:** La mochila entera se resuelve con programación dinámica en $O(nW)$, donde $W$ es la capacidad. Mide el tamaño de la entrada en bits. ¿Es polinomial ese algoritmo? ¿En qué se parece a la primalidad por división?

## El algoritmo y su costo
La tabla $T[i][c]$ ($0 \le i \le n$, $0 \le c \le W$) guarda el mayor valor que se logra con los primeros $i$ objetos y capacidad $c$:
$$T[i][c] = \max\big(T[i-1][c],\; T[i-1][c-w_i] + v_i\big) \quad \text{si } w_i \le c,$$
$$y$$ $$T[i][c] = T[i-1][c] en otro caso$$

Cada una de las $(n+1)(W+1)$ celdas cuesta una cantidad constante de operaciones en el modelo RAM, así que el tiempo $\Theta(nW)$. Se usa $\Theta$ y no solo $O$ porque el algoritmo recorre la tabla completa en todas las entradas. 

## Medición del tamaño de la entrada en bits:
En la teoría de complejidad computacional, el tamaño de una instancia de entrada $|I|$ no se mide por el valor numérico de sus parámetros, sino por la cantidad de bits necesarios para codificarla en un modelo estándar.

Para el problema de la mochila entera, la entrada consta de:
* Los $n$ objetos, cada uno con su peso $w_i$ y su valor $v_i$;
* La capacidad de la mochila $W$

Escribir $W$ en binario requiere $b = \lfloor \log_2 W \rfloor + 1$ bits, luego $W \approx 2^b$. Si cada número tiene a lo sumo $b$ bits, el tamaño total es $$N = \Theta(n \cdot b).$$

**Sobre n:** $n$ no es un número escrito en binario sino la cantidad de objetos. Cada objeto hay que leerlo, asi que $n \le N$: $n$ es siempre polinomial en el tamaño de la entrada y nunca puede ser $2^b$. La única cantidad que se relaciona exponencialmente con los bits es $W$.


## Análisis de la complejidad temporal:
Reescribiendo el costo en función de los bits de $W$:
$$\Theta(nW) = \Theta(n \cdot 2^b).$$
Como $O$ solo da una cota superior, hay que ver instancias donde el costo sea realmente exponencial. Fijemos $n=100$ y $W=2^b$ con $b$ creciente. Entonces $N = \Theta(b)$ y el costo es $100 \cdot 2^b= 2^{\Theta(N)}$. Ningún polinomio $N^k$ acota $2^{cN}$ para $N$ grande, luego el algoritmo **no** es polinomial.
Un algoritmo es pseudopolinomial si su costo es polinomial en el valor de un número de la entrada pero no en su cantidad de bits. Aquí $nW$ es polinomial en $n$ y $W$, y exponencial en $b$.

## Semejanza con la Primalidad por División:
El problema de la mochila entera con programación dinámica guarda una analogía conceptual con el algoritmo de primalidad por división:
* En el caso de la primalidad por división, para determinar si un número entero $N$ es primo, un algoritmo por divisiones sucesivas evalúa los posibles  divisores desde 2 hasta $\sqrt{N}$. Su tiempo de ejecución en función del valor numérico de $N$ es $O(\sqrt{N})$. Sin embargo, si medimos el tamaño de la entrada en bits, el número de bits para representar a $N$ es $b=log_2N$, lo que implica que $N = 2^b$. Por tanto, el tiempo de ejecución en función del tamaño en bits es $O(2^{b/2})$, lo cual es exponencial respecto al tamaño de la entrada.
* En la primalidad por división el algoritmo parece rápido $(O(\sqrt{N}))$ si pensamos en $N$ como una magnitud numérica pequeña, pero es exponencial en bits.
* En la mochila entera, el algoritmo parece eficiente $(O(nW))$ si $W$ es un número pequeño, pero se vuelve exponencial si $W$ crece exponencialmente respecto a los bits que lo codifican.
* Ambos algoritmos son pseudopolinomiales: su complejidad es polinomial respecto al valor del parámetro numérico $(W \text{ o } \sqrt{N})$, pero se comportan de manera exponencial cuando la entrada se mide en función de su longitud en bits.