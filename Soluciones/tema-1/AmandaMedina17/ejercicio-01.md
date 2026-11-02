**Problema**: Una computadora mil veces más rápida. ¿Cuánto crece el tamaño de entrada que se resuelve en una hora con un algoritmo $\Theta(n^2)$? ¿Y con uno $\Theta(n \log n)$? Estima los dos factores.

**Algoritmo con complejidad  $\Theta(n^2)$:**

Sea $T(n) = c \cdot n^2$ la función de costo que representa el número de operaciones necesarias para procesar una entrada de tamaño $n$.

Sea $P$ la potencia de la computadora (cantidad de operaciones por segundo). Teniendo un tiempo fijo de una hora en segundos,  $t = 3600$ segundos, la capacidad total de operaciones disponibles es $O = P \cdot t$.

El tamaño máximo de entrada ($n$), que puede resolverse en ese tiempo tiene que satisfacer:
$$
c \cdot n^2 \le O \implies n = \sqrt{\frac{O}{c}}

$$


Luego, al usar una computadora 1000 veces más rápida, la capacidad total de operaciones pasa a ser  $O_{1000} = 1000 \cdot O$. Entonces, el tamaño máximo de entrada que puede resolverse en ese tiempo pasa a ser:
$$
c \cdot (n')^2 \le 1000 \cdot O \implies n' = \sqrt{1000} \cdot \sqrt{\frac{O}{c}} = \sqrt{1000} \cdot n

$$

**Conclusión para $\Theta(n^2)$:**
El tamaño de la entrada que se puede resolver en una hora aumenta en un factor de $\sqrt{1000}$. Aproximadamente  $32$ veces mas grande.

**Algoritmo con complejidad $\Theta(n \log n)$:** 

Sea $T(n) = c \cdot n \log n$ la función de costo que representa el número de operaciones necesarias para procesar una entrada de tamaño $n$.

Para una computadora normal el procedimiento es equivalente siendo  $O$ la capacidad total de operaciones disponibles en un tiempo $t$:
$$
c \cdot n \log n \le O \implies n \log n \le \frac{O}{c}
$$

Al incrementar la velocidad de la computador por 1000, la nueva capacidad total de operaciones es $O_{1000} = 1000 \cdot O$, entonces el tamaño de la entrada ($n'$) satisface:

$$
c \cdot n' \log n' \le 1000 \cdot O \implies n' \log n' = \frac{1000 \cdot O}{c} \implies n' \log n' = 1000 \cdot n \log n
$$

Luego, para hallar el factor $x$, decimos que  $n' = x \cdot n$ y sustituimos:

$$
(x \cdot n) \log(x \cdot n) = 1000 \cdot n \log n \implies x \cdot \log(x \cdot n) = 1000 \cdot \log n
$$
$$
x(\log x + \log n) = 1000 \cdot \log n \implies x\left(\frac{\log x}{\log n} + 1\right) = 1000
$$

Entonces, tomando el límite cuando $n$ tiende al infinito, sabiendo que $x > 1$, permanece acotado superiormente por 1000:
$$
\lim_{n \to \infty} \frac{\log x}{\log n} = 0 \implies \lim_{n \to \infty} x(1 + 0) = 1000 \implies x \to 1000
$$

Lo que nos quiere decir que cuando $n$ es demasiado grande, la fracción $\frac{\log x}{\log n}$ se vuelve insignificante. Por lo que se aproxima asintóticamente al valor de 1000 como se observa en la Figure_1.png.
