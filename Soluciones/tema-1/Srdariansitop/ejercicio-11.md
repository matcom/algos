# Pregunta 11

La mochila entera se resuelve con programación dinámica en $O(nW)$, donde $W$ es la capacidad (lo vieron en Estructuras de Datos). Mide el tamaño de la entrada en bits, como en la sección 8 de la conferencia 1. ¿Es polinomial ese algoritmo? ¿En qué se parece a la primalidad por división? 

---

# Introducción

**Convenciones.**
- Hay $n$ objetos. El objeto $i$ tiene peso entero $w_i \ge 1$ y valor entero $v_i \ge 0$.
- $W$ es la capacidad de la mochila, un entero positivo.
- Se puede suponer $w_i \le W$ para todo $i$, porque un objeto más pesado que la mochila nunca se usa.
- El problema consiste en elegir un subconjunto $S \subseteq \{1,\dots,n\}$ con $\sum_{i\in S} w_i \le W$ que maximice $\sum_{i\in S} v_i$.
- Se usa el modelo word RAM de la sección 9, y el costo es el del peor caso.

**Explicación del algoritmo.** Sea $T[i][c]$ el mayor valor que se obtiene usando solo los primeros $i$ objetos con capacidad $c$. La recurrencia es:

$$T[i][c]=\begin{cases} T[i-1][c] & \text{si } w_i > c,\\ \max\{\,T[i-1][c],\; T[i-1][c-w_i]+v_i\,\} & \text{si } w_i \le c,\end{cases}$$

con $T[0][c]=0$. La respuesta es $T[n][W]$. La tabla tiene $(n+1)(W+1)$ celdas y cada una se llena con un número constante de operaciones, así que el costo es $\Theta(nW)$ y la memoria también es $\Theta(nW)$ (reducible a $\Theta(W)$ guardando solo la fila anterior).

**Sinopsis.** Con $n=100$ y $W=10^6$ el algoritmo hace unos $10^8$ pasos, lo cual es rápido. Parece lineal en los datos, igual que la primalidad por división parecía barata porque $\sqrt{n}$ crece despacio. La conferencia 1 enseña que esa impresión viene de medir el costo contra el *valor* de un número y no contra su *tamaño*. La pregunta pide corregir eso y comparar el resultado con el caso de la primalidad.

---

# Mide el tamaño de la entrada en bits

Como en la sección 8, un algoritmo se mide en función del tamaño de su entrada, porque eso es lo que ocupa en memoria y lo que hay que leer. Un entero $x \ge 1$ escrito en binario ocupa $\lfloor \log_2 x\rfloor + 1$ bits, es decir $\Theta(\log x)$, y no $x$ bits. En la primalidad, $n$ es el valor y el tamaño es $\log_2 n$ bits. Aquí hay que repetir ese análisis con todos los números de la entrada.

**Codificación de la entrada.**

| Dato | Cantidad | Bits cada uno | Total |
|---|---|---|---|
| Pesos $w_i \le W$ | $n$ | $\Theta(\log W)$ | $\Theta(n\log W)$ |
| Valores $v_i \le V$ | $n$ | $\Theta(\log V)$ | $\Theta(n\log V)$ |
| Capacidad $W$ | 1 | $\Theta(\log W)$ | $\Theta(\log W)$ |

Por tanto el tamaño de la entrada es

$$N = \Theta\big(n(\log W + \log V)\big).$$

Para aislar el papel de $W$ se pueden tomar valores acotados por una constante, y entonces $N = \Theta(n\log W)$. Sea $b = \lfloor\log_2 W\rfloor + 1$ el número de bits de $W$. Como $2^{b-1} \le W < 2^b$:

$$W = 2^{\Theta(b)}.$$

**Costo en función del tamaño.** El costo $nW$ queda como $n\cdot 2^{\Theta(b)}$, y esa cantidad no está acotada por ningún polinomio en $N$. Lo demuestra una familia de instancias:

- **Con $n$ fijo** (por ejemplo $n=2$): $N=\Theta(b)$ y el costo es $\Theta(W)=2^{\Theta(N)}$, **exponencial** en el tamaño.
- **Con $n=b$** (tomando $W \approx 2^n$): $N=\Theta(n^2)$ y el costo es $n\,2^n = 2^{\Theta(\sqrt{N})}$, que **crece más rápido que cualquier polinomio** en $N$.

Basta una familia infinita de instancias donde el costo no sea polinomial para que el algoritmo no lo sea en el peor caso.

**Ilustración numérica** (con $n=100$ y $10^9$ celdas por segundo, como en la sección 8):

| Bits de $W$ | Celdas $\approx nW$ | Tiempo |
|---|---|---|
| 32 | $4.3\times10^{11}$ | unos 7 minutos |
| 64 | $1.8\times10^{21}$ | unos 58 000 años |
| 128 | $3.4\times10^{40}$ | inimaginable |

Duplicar el número de bits de $W$ eleva al cuadrado el costo, no lo duplica.

**Observación sobre la aritmética.** En la sección 9 se advierte que contar cada operación como 1 solo es razonable si los números caben en una palabra. Si $W$ tiene muchos bits, cada suma y cada comparación cuesta $O(b)$ en operaciones de bits, así que el costo real es aún mayor. Esto no cambia la conclusión: ni siquiera la cuenta más favorable, con costo 1 por operación, da un algoritmo polinomial. Además, la tabla misma ocupa $nW$ celdas, que es exponencial en $N$, así que la memoria también es exponencial.

---

# ¿Es polinomial el algoritmo?

**No.** Según la sección 8, un algoritmo es polinomial si su costo es polinomial en el tamaño de la entrada, medido en bits.

**Resultado.** El algoritmo de programación dinámica para la mochila entera, de costo $\Theta(nW)$, **no es polinomial** en el tamaño $N$ de la entrada.

**Demostración.** Por la sección anterior, en las instancias con $n$ fijo se tiene $N=\Theta(\log W)$, así que $W=2^{\Theta(N)}$. El costo $\Theta(nW)$ es entonces $2^{\Theta(N)}$, y ninguna función $N^c$ lo acota. $\blacksquare$

**Qué sí es.** El algoritmo es **pseudopolinomial**: su costo es polinomial en el *valor* de un número de la entrada ($W$) pero no en su cantidad de bits. La sección 8 cita la mochila con su tabla de $nW$ como el ejemplo clásico.

**Cuándo se comporta bien.**
- Si $W \le p(n)$ para algún polinomio $p$, es decir, si $W$ es pequeño respecto a $n$ (equivalente a escribirlo en unario), entonces $nW$ es polinomial en $N$. Esto explica por qué en la práctica funciona con capacidades moderadas.
- Con $W$ de 64 bits el algoritmo es impracticable, aunque la entrada ocupe pocas decenas de bytes.

**Aclaración importante.** Que este algoritmo no sea polinomial no prueba que el *problema* de la mochila no tenga algoritmo polinomial. Solo dice que *este* algoritmo no lo es. De hecho, la versión de decisión de la mochila es NP-completa, y por eso no se conoce ninguno. Ese es el vínculo con el Tema 3 que anuncia la conferencia.

---

# ¿En qué se parece a la primalidad por división?

Los dos algoritmos comparten la misma estructura de error, y se pueden comparar punto por punto.

**1. El costo depende del valor de un número, no de su tamaño.**
- Primalidad por división: el costo es $\sqrt{n}$ divisiones, con $n$ el valor. Como $n$ tiene $b=\Theta(\log n)$ bits, el costo es $2^{b/2}$.
- Mochila: el costo es $nW$, con $W$ el valor de la capacidad. Como $W$ tiene $b=\Theta(\log W)$ bits, el costo es $n\cdot 2^{b}$.

En ambos casos el costo es polinomial en el valor y **exponencial en el número de bits**, porque el valor es $2^{\Theta(b)}$. Los dos son pseudopolinomiales.

**2. Los dos engañan por la misma razón.** Con números pequeños ambos son rápidos: $\sqrt{n}$ crece más despacio que $n$, y $nW$ parece lineal en los datos. La impresión cambia al medir en bits, y los dos se vuelven inutilizables en cuanto el número tiene decenas de bits.

**3. Los dos se vuelven polinomiales si el número se escribe en unario.** Si $n$ (en primalidad) o $W$ (en la mochila) se representa con tantos símbolos como su valor, el tamaño de la entrada pasa a ser comparable al valor y el costo resulta polinomial.

**4. Ambos muestran por qué el tamaño se mide en bits.** El mismo argumento de la sección 8 se aplica a los dos: la entrada es lo que se lee y se guarda, y un número ocupa $\log$ de su valor.

**Diferencias.**

| | Primalidad por división | Mochila por programación dinámica |
|---|---|---|
| Costo en bits $b$ | $2^{b/2}$ | $n\cdot 2^{b}$ |
| ¿Existe algoritmo polinomial para el problema? | Sí: Miller-Rabin (aleatorio) y AKS (determinista, 2002) | No se conoce; el problema es NP-completo |
| Qué se concluye | El algoritmo es malo, el problema es fácil | El algoritmo es pseudopolinomial, y el problema probablemente es difícil en el peor caso |

**Conclusión.** En ambos casos un algoritmo cuyo costo es polinomial en el valor de un número no es polinomial en el tamaño de la entrada. Lo que los distingue es que para la primalidad existen otros algoritmos genuinamente polinomiales, mientras que para la mochila no se conoce ninguno.

# Código

**`01_valor_vs_bits.png`: un número ocupa log₂W bits, no W.** A la izquierda se ve que el número de bits necesarios para escribir W crece como una escalera muy lenta: W = 1024 necesita solo 11 bits. A la derecha, en escala logarítmica, se muestra el camino inverso: cada bit extra duplica el valor máximo representable (8 bits llegan a unos 256, 32 bits a unos 4.3×10⁹, 64 bits a unos 1.8×10¹⁹). Es la base de la sección "Mide el tamaño de la entrada en bits", porque muestra que W = 2^Θ(b).

**`02_tabla_dp.png`: la tabla T[i][c] de la programación dinámica.** Muestra la tabla completa para una instancia pequeña de 4 objetos, con pesos (2,3,4,5), valores (3,4,5,6) y capacidad W = 8. Tiene (n+1)(W+1) = 45 celdas, y la respuesta T[n][W] = 10 aparece enmarcada en rojo. Sirve para ver de dónde sale el costo Θ(nW) de la introducción: una celda por cada par (objeto, capacidad).

**`03_llenado_tabla.gif`: cómo se llena la tabla, celda por celda.** Es una animación de 36 cuadros, uno por cada celda calculada. En cada cuadro la celda actual va en rojo, la celda que corresponde a no usar el objeto va en verde y la que corresponde a usarlo va en naranja. El título muestra la cuenta exacta, por ejemplo T[4][8] = max(9, 4+6) = 10. Ilustra la recurrencia y muestra que cada celda cuesta O(1).

**`04_costo_vs_tamano.png`: el costo nW frente a los polinomios en N.** Fija n = 10 objetos y mide el tamaño N de la entrada en bits. La curva roja, nW = n·2^b, es una recta en escala logarítmica, o sea exponencial en N, y termina cruzando por encima de N², N³ y N⁵. Es la demostración gráfica de la sección "¿Es polinomial el algoritmo?": ningún polinomio en N alcanza a acotarlo.

**`05_tiempo_estimado.png`: cuánto tardaría en la práctica.** Usa n = 100 objetos y 10⁹ celdas por segundo, como en la sección 8 de la conferencia. Para W de 16 bits tarda milisegundos, con 32 bits unos 7 minutos, con 48 bits casi un año, con 64 bits unos 58 000 años y con 128 bits unos 10²⁴ años, muy por encima de la vida restante del Sol. Muestra por qué duplicar los bits de W eleva al cuadrado el costo y no lo duplica.

**`06_primalidad_vs_mochila.png`: la comparación con la primalidad por división.** Dibuja contra el número de bits b la primalidad por división (√x = 2^(b/2), en azul), la mochila (n·2^b, en rojo) y un algoritmo genuinamente polinomial en b (b³, en verde punteado). Las dos curvas exponenciales son rectas en escala logarítmica y la polinomial queda muy por debajo. Ilustra la sección "¿En qué se parece a la primalidad por división?": ambos son polinomiales en el valor pero exponenciales en los bits, y la mochila crece aún más rápido.

**`07_binario_vs_unario.png`: por qué cambia la respuesta según cómo se escribe el número.** Arriba se escribe el mismo número, W = 13, en binario (4 símbolos) y en unario (13 símbolos). Abajo se compara el tamaño de ambas representaciones al crecer W: la unaria crece linealmente y la binaria casi no crece. La brecha entre las dos es la que separa "polinomial en el valor" de "polinomial en el tamaño", y explica por qué la mochila sería polinomial si W se diera en unario.