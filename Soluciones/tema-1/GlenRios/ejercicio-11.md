# Problema 11 ★★

**Enunciado.** La mochila entera se resuelve con programación dinámica en $O(nW)$, donde $W$ es la capacidad (lo vieron en Estructuras de Datos). Mide el tamaño de la entrada en bits, como en la sección 8 de la conferencia 1. ¿Es polinomial ese algoritmo? ¿En qué se parece a la primalidad por división?

## Solución formal

**La entrada y su tamaño en bits.** Una instancia de la mochila entera consiste en $n$ ítems, cada uno con un peso $w_i$ y un valor $v_i$ enteros no negativos, y una capacidad $W$, también entero no negativo. Supongamos que todos los pesos y valores están acotados por $W$; si no, se toma el máximo entre ellos. Cada peso o valor se escribe con $\lceil \log_2 W \rceil + 1$ bits, y hay $2n$ de ellos más la capacidad. Por tanto, el tamaño total de la entrada es:
$$
b = O(n \log W) + O(\log W) = O(n \log W).
$$

La programación dinámica clásica llena una tabla de tamaño $n \times (W+1)$, donde la celda $(i, c)$ guarda el mejor valor usando los primeros $i$ ítems con capacidad $c$. Cada celda se calcula en tiempo $O(1)$ a partir de las celdas anteriores, así que el tiempo total es $O(nW)$. La memoria también se puede reducir a $O(W)$ guardando solo la fila anterior.

Queremos saber si $O(nW)$ es polinomial en el tamaño de la entrada $b = O(n \log W)$. Para eso hay que expresar $nW$ en función de $b$, no de $W$. Usamos la identidad $W = 2^{\log_2 W}$. Sustituyendo:
$$
nW = n \cdot 2^{\log_2 W}.
$$
Ahora bien, $\log_2 W$ es exactamente el número de bits necesarios para escribir $W$ (salvo constantes). Si llamamos $k = \log_2 W$, entonces $W = 2^k$ y:
$$
nW = n \cdot 2^k.
$$
El tamaño de la entrada es $b = O(nk)$ (más un término $O(k)$ por la capacidad). Entonces $nW = n \cdot 2^k$ es **exponencial en $k$**, y $k$ aparece en $b$ de forma lineal. Por tanto, $nW$ no se puede acotar por ningún polinomio en $b$: crece como $n \cdot 2^k$ mientras que $b$ crece como $n \cdot k$. El cociente $nW / b = 2^k / k$ tiende a infinito cuando $k$ crece.

**Conclusión sobre la mochila.** El algoritmo $O(nW)$ es **pseudopolinomial**: es polinomial en el valor numérico $W$, pero exponencial en el número de bits $\log W$ que se necesitan para representarlo. No es un algoritmo polinomial en el tamaño de la entrada.

**Comparación con la primalidad por división.** El algoritmo de primalidad por división prueba divisores hasta $\sqrt{n}$ y cuesta $O(\sqrt{n})$ divisiones. El tamaño de la entrada es $b = \lceil \log_2 n \rceil + 1$ bits, así que:
$$
\sqrt{n} = \sqrt{2^b} = 2^{b/2}.
$$
Este costo es exponencial en $b$. Igual que en la mochila, el algoritmo es polinomial en el valor numérico $n$ pero exponencial en el número de bits. Es el mismo fenómeno: el costo depende del valor de un número de la entrada, no de su longitud en bits.

**Conclusión.** Tanto la mochila entera con DP como la primalidad por división son algoritmos pseudopolinomiales: su costo es polinomial en los valores numéricos de la entrada, pero exponencial en el tamaño de la entrada medido en bits.
