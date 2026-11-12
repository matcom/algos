## 13. Splay tree desde un camino, accesos $1, \dots, n$ en orden (C4)

**La cota con el lema de acceso.** Con potencial $\Phi = \sum_x \log s(x)$, cada acceso tiene costo amortizado
$$\hat c \le 3\big(r(\text{raíz}) - r(x)\big) + 1 \le 3 \log n + 1,$$
porque $r(x) \ge 0$. El potencial inicial es el de un camino, $\Phi_0 = \sum_{k=1}^{n} \log k = \log n! \le n \log n$, y siempre $\Phi \ge 0$. Por el telescopio de C4 §2 (la cuenta de C4 §5, con $m = n$ accesos):
$$\sum_{i=1}^{n} c_i = \sum \hat c_i + \Phi_0 - \Phi_n \ \le\ n(3\log n + 1) + \log n! \ \le\ 4 n \log n + n.$$
**Total $O(n \log n)$**, aunque el primer acceso solo ya cueste $n - 1$ rotaciones (la clave 1 está en el fondo).

**Comparación con lo que mide C4 §6.** La tabla de C4 §6 da entre 4,2 y 4,4 rotaciones por acceso para $n$ de 100 a 800, sin crecer con $n$: un total del orden de $4{,}4\,n$, no de $n\log n$. Midiendo solo la primera ronda, desde el camino:

| $n$ | rotaciones reales | por acceso | cota $n(3\log n + 1) + \log n!$ |
|---|---|---|---|
| 100 | 416 | 4,16 | 2 618 |
| 1 000 | 4 374 | 4,37 | 39 427 |
| 10 000 | 44 112 | 4,41 | 527 090 |

La razón entre la cota y la realidad crece como $\log n$.

Un detalle de la medición: después de acceder a $1, \dots, n$ el árbol vuelve a ser un camino (con $n$ en la raíz), así que $\Phi_n = \Phi_0$ y el costo real es *exactamente* la suma de los amortizados. El término $\log n!$ no es lo que se pierde: lo que se pierde es la cota $3\log n + 1$ de cada acceso, que se cumple con mucha holgura en casi todos los accesos de esta secuencia.

**¿Es ajustada la cota?** Hay que separar dos preguntas.

*Para esta secuencia, no.* La cota inferior $\Omega(n)$ es inmediata: cada acceso cuesta al menos 1, y el primero $n-1$. Las mediciones (las de C4 §6 y la tabla de arriba) dan un costo por acceso constante, así que la cota $O(n\log n)$ sobra en un factor $\log n$. Lo que no se puede con las herramientas de C4 es *demostrar* que el total es $O(n)$. La pérdida no viene de haber acotado $r(x) \ge 0$: incluso usando el rango exacto de cada nodo justo antes de su acceso, la suma de las cotas del lema sigue creciendo como $n \log n$:

| $n$ | $\sum \big(3(r(\text{raíz}) - r(x)) + 1\big)$ con los rangos exactos | por acceso | costo real |
|---|---|---|---|
| 100 | 1 442 | 14,4 | 416 |
| 1 000 | 20 490 | 20,5 | 4 374 |
| 5 000 | 124 502 | 24,9 | 22 028 |

La cota del lema por acceso crece con $\log n$ y el costo real por acceso no. Así que lo que tenemos es un teorema, $O(n\log n)$, y una conjetura apoyada en el experimento, $\Theta(n)$. Es la situación de C2 §7: el experimento propone el enunciado, pero no lo demuestra.

*Como garantía sobre todas las secuencias, sí.* Se demuestra con el argumento de información de C5 §3. Fijemos $n$ y $m$, y miremos los $m$ accesos como un solo algoritmo de comparaciones cuya entrada es la secuencia $(k_1, \dots, k_m) \in \{1,\dots,n\}^m$. Cada paso de `buscar` compara la clave buscada con la de un nodo, con tres respuestas posibles, así que la ejecución completa es un árbol de decisión ternario.

- Dos secuencias distintas terminan en hojas distintas. Si difieren por primera vez en el acceso $i$, hasta ahí el árbol de búsqueda es el mismo en las dos, y el acceso $i$ termina con "$=$" en el nodo $k_i$ en una y en el nodo $k'_i \ne k_i$ en la otra: los caminos se separan.
- Hay entonces al menos $n^m$ hojas. El lema 1 de C5 adaptado a tres ramas (la misma inducción, con $3^h$ en lugar de $2^h$) da que alguna secuencia hace al menos $\log_3 n^m = m \log n / \log 3$ comparaciones.
- Un acceso a profundidad $d$ hace $d + 1$ comparaciones y cuesta $\max(d, 1) \ge (d+1)/2$ rotaciones.

Así que **alguna secuencia de $m$ accesos cuesta al menos $\frac{m\log n}{2\log 3} \approx 0{,}31\, m \log n$**, mientras que el lema da a lo sumo $m(3\log n + 1) + n\log n$. Para $m \ge n$ las dos cotas son $\Theta(m\log n)$: la garantía del lema es ajustada salvo constantes. El argumento vale para cualquier árbol binario de búsqueda que busque desde la raíz, no solo para splay.

La lección es la de C2 §6: garantía de peor caso y comportamiento sobre una entrada particular son cosas distintas. Compárese con subir a la raíz, que sobre esta misma secuencia cuesta $\Theta(n^2)$ (ejercicio 4 de C4).

---