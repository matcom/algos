# Pregunta 13

En un splay tree que empieza como un camino de $n$ nodos se accede a las claves $1,\dots,n$ en orden. Acota el costo total con el lema de acceso y la cuenta de la sección 5 de la conferencia 4, y compáralo con lo que mide la sección 6. ¿Es ajustada la cota? (C4)

---

## Convenciones y entendimiento del problema

- **Árbol inicial.** Es el de `camino(n)`: la raíz es $n$ y cada clave $k$ es hija izquierda de $k+1$. La clave $1$ está a profundidad $n-1$.
- **Secuencia.** Se hacen $n$ accesos, $x_1, x_2, \dots, x_n$, donde $x_i$ es el nodo con clave $i$. Después de cada acceso se hace splay del nodo accedido, que queda en la raíz.
- **Costo real $c_i$.** Es el número de rotaciones del splay, y vale $1$ si el nodo ya es la raíz (convención de la sección 4). Es proporcional a la profundidad del nodo, así que incluye la búsqueda.
- **Tamaño y rango.** $s(v)$ es el número de nodos del subárbol de $v$, y $r(v)=\log_2 s(v)$. El potencial es $\Phi(T)=\sum_v r(v)$.
- **Dato clave.** El splay solo rota y nunca inserta ni borra, así que el árbol siempre tiene $n$ nodos. La raíz $t$ tiene $s(t)=n$ antes de cada acceso, y por tanto $r(t)=\log_2 n$ **siempre**.
- **Costo amortizado.** $a_i=c_i+\Phi_i-\Phi_{i-1}$, donde $\Phi_i$ es el potencial después del acceso $i$ y $\Phi_0$ el del camino inicial.

**Lema de acceso (sección 5).** El costo amortizado de hacer splay de $x$ en un árbol con raíz $t$ es a lo sumo $3\,(r(t)-r(x))+1$.

---

## Acota el costo total

El plan es el de la sección 5: acotar cada $a_i$ con el lema y sumar. Como $\Phi_{\text{final}}\ge\Phi_{\text{inicial}}$ no se cumple aquí, la diferencia de potenciales se paga aparte, una sola vez.

**Paso 1: despejar el costo real.** Sumando $a_i=c_i+\Phi_i-\Phi_{i-1}$ sobre $i=1,\dots,n$, los potenciales se telescopian:

$$\sum_{i=1}^n a_i=\sum_{i=1}^n c_i+\Phi_n-\Phi_0
\quad\Longrightarrow\quad
C:=\sum_{i=1}^n c_i=\sum_{i=1}^n a_i+\Phi_0-\Phi_n .$$

**Paso 2: acotar cada $a_i$ con el lema.** Antes de cada acceso la raíz tiene rango $\log_2 n$, así que

$$a_i\le 3\bigl(\log_2 n-r_i(x_i)\bigr)+1,$$

donde $r_i(x_i)$ es el rango de $x_i$ justo antes del acceso $i$. Como $s(x_i)\ge 1$, se tiene $r_i(x_i)\ge 0$, y entonces $a_i\le 3\log_2 n+1$. Sumando,

$$\sum_{i=1}^n a_i\le 3n\log_2 n+n.$$

**Paso 3: el potencial inicial.** En un camino, los subárboles tienen tamaños $1,2,\dots,n$ (esto lo dice la sección 5), así que

$$\Phi_0=\sum_{k=1}^{n}\log_2 k=\log_2 n!\le n\log_2 n,$$

porque $n!\le n^n$.

**Paso 4: el potencial final.** Todos los rangos son $\ge 0$, luego $\Phi_n\ge 0$. En realidad $\Phi_n\ge\log_2 n$, porque la raíz ya aporta eso, pero no hace falta.

**Paso 5: juntar.**

$$C=\sum a_i+\Phi_0-\Phi_n\;\le\;(3n\log_2 n+n)+n\log_2 n-0=4n\log_2 n+n .$$

$$\boxed{\,C\le 4\,n\log_2 n+n=O(n\log n)\,}$$

**Lectura.** La cota es $O(\log n)$ amortizado por acceso, más un pago único de $\Phi_0\le n\log_2 n$ por haber empezado en el peor árbol. Esto es lo que dice la sección 5 cuando indica que la condición $\Phi_{\text{final}}\ge\Phi_{\text{inicial}}$ "no se cumple, y la demostración lo resuelve pagando $\Phi_0$ aparte". Aquí ese pago aparece explícitamente. Su efecto real se ve en el primer acceso, que cuesta $n-1$ rotaciones y hace caer el potencial casi en esa misma cantidad.

---

## Comparación con la sección 6

La sección 6 mide exactamente esta situación: camino inicial, claves en orden, tres rondas. Hay que comparar tres cosas.

**1. La cota del lema frente a lo medido con splay.** El lema da, por acceso, $\le 4\log_2 n+1$. Con los valores de la tabla:

| $n$ | $4\log_2 n+1$ (cota) | splay medido | subir a la raíz medido |
|---|---|---|---|
| 100 | 27.6 | 4.2 | 50.5 |
| 200 | 31.6 | 4.2 | 100.5 |
| 400 | 35.6 | 4.3 | 200.5 |
| 800 | 39.6 | 4.4 | 400.5 |

La cota se cumple, como debe, porque el lema es un teorema. Pero crece como $\log n$, mientras que el costo medido es **prácticamente plano**, de alrededor de 4 rotaciones por acceso. La figura 3 lo muestra: la curva del splay es horizontal en ejes logarítmicos. Una pequeña parte del 4.2 es el primer acceso: cuesta $n-1$ y, repartido entre $3n$ accesos, aporta alrededor de $1/3$.

**2. Qué ocurre con la heurística de subir a la raíz.** La tabla da $n/2+\tfrac12$ por acceso, es decir $\Theta(n)$, con pendiente 1 en la figura 3. La razón está en la sección 5: una rotación simple es un zig, con costo amortizado $\le 3(r'(x)-r(x))+1$. Subir desde profundidad $d$ son $d$ rotaciones, y la suma da $3(r(t)-r(x))+d$. Los rangos se telescopian, pero los $1$ no. Esa $d$ es lo que el lema de acceso evita con el zig-zig, donde la concavidad absorbe el $+1$. Con esa heurística el argumento solo da $\Theta(n)$ por acceso, y la medición confirma que no es una debilidad de la prueba: el costo real es $\Theta(n)$. El total con subir a la raíz es $\Theta(n^2)$, frente a $O(n\log n)$ para splay.

**3. Qué dice cada cosa.** El lema es una cota superior que vale para toda secuencia y es **ciega a la estructura** de esta. La sección 6 es una medición sobre la secuencia concreta. Su resultado es que esta secuencia es difícil para subir a la raíz, porque repite el caso zig-zig, y fácil para splay. Para splay, el lema acierta en que el costo es $O(\log n)$ por acceso, pero lo que se observa es mucho menor.

---

## ¿Es ajustada la cota?

Hay que separar dos preguntas.

**(a) ¿Es ajustada para esta secuencia? No.** Cada acceso cuesta al menos $1$, así que $C\ge n$. Sabemos entonces

$$n\;\le\;C\;\le\;4n\log_2 n+n,$$

y la sección 6 sugiere que el valor real está en el extremo inferior: $\approx 4$ rotaciones por acceso, es decir $C=\Theta(n)$. La cota está a un factor $\log n$ del costo real (entre 6 y 9 veces mayor en la tabla, y creciendo). Esta medición es evidencia experimental y no una demostración, pero el resultado está probado en la literatura: es el teorema de acceso secuencial de Tarjan (1985), que da $O(n)$ para esta secuencia. Esa demostración **no está en la conferencia** y no la reproduzco aquí.

**(b) ¿Dónde se pierde?** La pérdida está en el lema, no en la suma. Este acota cada acceso por $3(\log_2 n-r(x_i))+1$, y en esta secuencia el nodo $x_i$ suele tener subárbol pequeño antes de acceder, de modo que $r(x_i)\approx 0$ y la cota por acceso se queda en $\approx 3\log_2 n$. El lema solo ve el tamaño del subárbol de $x_i$, y no que $x_i$ es **vecino** del acceso anterior. Además, la suma de potenciales paga $\Phi_0\approx n\log_2 n$ aunque en la práctica ese potencial se libera en el primer acceso y en unos pocos más. Ninguna elección de pesos en el lema generalizado arregla esto, porque con frecuencias uniformes da otra vez $O(n\log n)$. Para llegar a $O(n)$ hace falta un argumento distinto, el de acceso secuencial.

**(c) ¿Es ajustada como cota general? Sí.** Como cota para **toda** secuencia de $n$ accesos, $O(\log n)$ amortizado es óptimo salvo constantes. Hay secuencias, por ejemplo accesos a claves uniformemente aleatorias, para las que cualquier árbol binario de búsqueda necesita $\Omega(n\log n)$ en total, porque la profundidad media de $n$ nodos es al menos $\log_2 n-O(1)$. El lema no se puede mejorar sin mirar la secuencia.

**Conclusión.** $O(n\log n)$ es una cota correcta y es ajustada como garantía universal, pero **no es ajustada para esta secuencia**: el costo real es $\Theta(n)$. La comparación con la sección 6 enseña dos cosas. Primero, el lema de acceso es suficiente para separar splay ($O(n\log n)$) de subir a la raíz ($\Theta(n^2)$). Segundo, no basta para decir cuánto cuesta *exactamente* splay en secuencias con estructura.

## Código

**Fig. 1 – `fig1_problema_camino_inicial.png`.** Dibuja el árbol inicial `camino(8)`: raíz 8, cada clave $k$ hija izquierda de $k+1$ y la clave 1 a profundidad $n-1$. Junto a cada nodo muestra su tamaño $s(v)$, que va de $1$ a $n$. Con eso se ve de dónde sale $\Phi_0=\sum\log_2 k=\log_2 n!\le n\log_2 n$, el pago único del Paso 3 de la sección "Acota el costo total".

**Fig. 2 – `fig2_primeros_accesos.png`.** Muestra el árbol inicial y el estado tras acceder a las claves 1, 2, 3 y 4, con el nodo accedido resaltado y su costo real. El primer acceso cuesta 7 rotaciones ($n-1$) y deja el árbol mucho más equilibrado. Los siguientes cuestan 4, 3 y 1. Es la intuición de por qué el potencial se "libera" casi todo en el primer acceso.

**Fig. 3 – `fig3_animacion_splay.gif`.** Animación con $n=10$ que enseña cada paso del splay (zig, zig-zig, zig-zag) durante los 10 accesos en orden. El nodo accedido está en naranja y se ve cómo sube a la raíz. Sirve para ver la diferencia con subir a la raíz con rotaciones simples: el zig-zig reduce la profundidad del camino en lugar de limitarse a mover el nodo.

**Fig. 4 – `fig4_costo_por_acceso.png`.** Barras del costo real $c_i$ de cada acceso para $n=128$, en escala logarítmica. Aparece un único pico en el acceso 1 (127 rotaciones) y después todos los costos son pequeños. La línea roja marca la media sin ese primer acceso, de unas 2 a 4 rotaciones. Respalda la afirmación de que el costo real es casi constante y no $\log n$.

**Fig. 5 – `fig5_potencial.png`.** Curva del potencial $\Phi_i$ real tras cada acceso ($n=128$), con dos referencias: $n\log_2 n$, la cota que usé para $\Phi_0$, y $\log_2 n!$, su valor exacto. Muestra que el potencial arranca cerca de $n\log n$ y cae enseguida. También se ve que $\Phi_n\ge0$ y $\Phi_n\ge\log_2 n$, que son las dos propiedades del Paso 4.

**Fig. 6 – `fig6_cota_vs_medido.png`.** Es la comparación con la sección 6. Para $n$ de 25 a 800, en ejes log-log, enfrenta la cota del lema $4\log_2 n+1$ con el costo medio medido de splay y de la heurística de subir a la raíz. Splay queda casi plano, muy por debajo de la cota, que crece como $\log n$. Subir a la raíz crece como $n/2$ (la recta de referencia punteada), es decir $\Theta(n)$ por acceso.

**Fig. 7 – `fig7_total_y_holgura.png`.** Responde a "¿es ajustada la cota?". El panel izquierdo compara, para $n$ de 16 a 1024, el costo total medido $C$ con la cota $4n\log_2 n+n$ y con la cota inferior trivial $C\ge n$. El panel derecho grafica el cociente cota/costo real, que va de ~5 a ~9.4 y crece como $\log n$. Es la evidencia experimental de que la cota es correcta pero no ajustada para esta secuencia, donde el costo real parece $\Theta(n)$.

**Fig. 8 – `fig8_lema_por_acceso.png`.** Para cada acceso ($n=128$) dibuja el costo real $c_i$, el costo amortizado $a_i=c_i+\Phi_i-\Phi_{i-1}$ y la cota del lema $3(r(t)-r(x_i))+1$. El costo amortizado queda siempre por debajo del lema, así que el lema se verifica en esta ejecución. Además, $\sum a_i=534$ frente a $\sum\text{cotas}=1927$, lo que muestra dónde se pierde: el lema es ciego a que $x_i$ es vecino del acceso anterior.