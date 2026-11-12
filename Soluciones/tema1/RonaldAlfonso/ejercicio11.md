## 11.  ¿Es polinomial la mochila en $O(nW)$? (C1)

**Tamaño de la entrada en bits.** La entrada son $n$ pesos, $n$ valores y la capacidad $W$. Podemos suponer $w_i \le W$ (un objeto más pesado que la mochila se descarta). Si los números tienen a lo sumo $b$ bits, el tamaño es
$$N = \Theta(n\,b), \qquad b \approx \log W.$$

**Costo en función del tamaño.** $nW = n \cdot 2^{\log W} \approx n\cdot 2^{b}$. Con $n$ fijo, el costo es exponencial en $b$, que es parte del tamaño de la entrada. **No es polinomial: es pseudopolinomial** (C1 §8), polinomial en el *valor* de $W$ pero no en su número de bits. Si $W$ viniera escrito en unario, o si se supiera que $W \le n^c$, el mismo algoritmo sí sería polinomial.

Con números: $n = 100$ objetos con números de 64 bits es una entrada de unos $100 \cdot 2 \cdot 64 + 64 \approx 13\,000$ bits, y la tabla tendría $100 \cdot 2^{64} \approx 1{,}8\cdot 10^{21}$ celdas.

**En qué se parece a la primalidad por división.** Las dos cuentas parecen inofensivas porque se escriben en función de un número de la entrada ($\sqrt N$ divisiones, $nW$ celdas), y las dos son exponenciales en el tamaño: $2^{b/2}$ para un $N$ de $b$ bits, $n\cdot 2^b$ para una $W$ de $b$ bits. El error es el mismo: medir en el valor y no en los bits.

**En qué se diferencian.** Para la primalidad, C1 §8 da algoritmos polinomiales en $b$: el test de Miller-Rabin, que es aleatorio, y desde 2002 el de Agrawal, Kayal y Saxena, que es determinista. Así que el costo exponencial de la división era un defecto de *ese algoritmo*, no del problema. Para la mochila, las conferencias no dan ningún algoritmo polinomial en bits; C1 §8 solo anuncia que el ejemplo va a ser importante en el Tema 3. Con lo visto hasta ahora solo se puede decir dónde está la dificultad: cuando $W$ es pequeño (polinomial en $n$), la misma tabla ya es polinomial, así que lo que cuesta es que los números sean grandes.

---
